# -*- coding: utf-8 -*-
"""
CareerBridge ML 모델 관리 모듈
TabTransformer 모델 로딩 및 예측 처리
"""

import torch
import torch.nn as nn
import pandas as pd
import joblib
import numpy as np
import streamlit as st
from pathlib import Path

# TabTransformer 모델 정의
class TabTransformer(nn.Module):
    def __init__(self, num_cats_per_col, num_numeric, d_model=32, n_heads=4, n_layers=2, dropout=0.1, num_classes=8):
        super().__init__()
        self.cat_embeddings = nn.ModuleList([nn.Embedding(n, d_model) for n in num_cats_per_col])
        self.num_linears = nn.ModuleList([nn.Linear(1, d_model) for _ in range(num_numeric)])

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=n_heads,
            dim_feedforward=d_model*4,
            dropout=dropout,
            batch_first=True,
            activation="gelu",
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.norm = nn.LayerNorm(d_model)

        self.fc = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_model, num_classes),
        )

    def forward(self, x_cats, x_nums):
        cat_tokens = [emb(x_cats[:, i]) for i, emb in enumerate(self.cat_embeddings)]
        num_tokens = [lin(x_nums[:, i].unsqueeze(-1)) for i, lin in enumerate(self.num_linears)]
        tokens = torch.stack(cat_tokens + num_tokens, dim=1)
        out = self.transformer(tokens)
        pooled = out.mean(dim=1)
        pooled = self.norm(pooled)
        return self.fc(pooled)


@st.cache_resource
def load_model():
    """모델 및 전처리 도구 로드 (캐싱)"""
    device = torch.device("cpu")
    model_path = Path(__file__).parent.parent / "models"
    
    try:
        # 전처리 도구 로드
        cat_encoders = joblib.load(model_path / "cat_encoders.pkl")
        scaler = joblib.load(model_path / "scaler.pkl")
        target_le = joblib.load(model_path / "target_label_encoder.pkl")
        
        cat_cols = list(cat_encoders.keys())
        num_cols = scaler.feature_names_in_.tolist()
        
        # 모델 로드
        num_cats_per_col = [len(enc.classes_) for enc in cat_encoders.values()]
        num_numeric = len(num_cols)
        
        model = TabTransformer(
            num_cats_per_col, 
            num_numeric, 
            num_classes=len(target_le.classes_)
        ).to(device)
        
        model.load_state_dict(torch.load(model_path / "best_model.pth", map_location=device))
        model.eval()
        
        return {
            "model": model,
            "cat_encoders": cat_encoders,
            "scaler": scaler,
            "target_le": target_le,
            "cat_cols": cat_cols,
            "num_cols": num_cols,
            "device": device
        }
    except Exception as e:
        st.error(f"❌ 모델 로딩 오류: {str(e)}")
        return None


def predict_job(student_data: dict, parent_data: dict):
    """학생+부모 데이터를 받아 직무 예측"""
    
    # 모델 로드
    model_data = load_model()
    if model_data is None:
        return None
    
    model = model_data["model"]
    cat_encoders = model_data["cat_encoders"]
    scaler = model_data["scaler"]
    target_le = model_data["target_le"]
    cat_cols = model_data["cat_cols"]
    num_cols = model_data["num_cols"]
    device = model_data["device"]
    
    # 통합 데이터 생성
    combined_dict = {**student_data, **parent_data}
    
    # 희망직무일치수준 계산
    if student_data.get('학생_희망직무') == parent_data.get('부모_희망직무'):
        combined_dict['희망직무일치수준'] = '거의 동일'
    else:
        combined_dict['희망직무일치수준'] = '완전 다름'
    
    # DataFrame 생성
    df = pd.DataFrame([combined_dict])
    
    # 범주형 인코딩
    for c in cat_cols:
        if c in df.columns:
            try:
                df[c] = cat_encoders[c].transform(df[c].astype(str))
            except ValueError as e:
                st.warning(f"⚠️ 인코딩 오류 ({c}): {e}")
                df[c] = 0
    
    # 수치형 스케일링
    for c in num_cols:
        if c not in df.columns:
            df[c] = 0
    
    df[num_cols] = scaler.transform(df[num_cols])
    
    # 텐서 변환
    X_c = torch.tensor(df[cat_cols].values, dtype=torch.long).to(device)
    X_n = torch.tensor(df[num_cols].values, dtype=torch.float32).to(device)
    
    # 예측
    with torch.no_grad():
        logits = model(X_c, X_n)
        probs_original = torch.softmax(logits, dim=1).cpu().numpy()[0]
    
    # 희망직무 가중치 조정 (50% 감소)
    probs_adjusted = probs_original.copy()
    student_hope = student_data.get('학생_희망직무')
    
    try:
        hope_idx = list(target_le.classes_).index(student_hope)
        original_hope_prob = probs_adjusted[hope_idx]
        probs_adjusted[hope_idx] = original_hope_prob * 0.5
        
        # 감소한 확률을 다른 직무들에 재분배
        reduced_prob = original_hope_prob - probs_adjusted[hope_idx]
        num_other_jobs = len(probs_adjusted) - 1
        
        if num_other_jobs > 0:
            for i in range(len(probs_adjusted)):
                if i != hope_idx:
                    probs_adjusted[i] += reduced_prob / num_other_jobs
    except ValueError:
        st.warning(f"⚠️ 희망직무 '{student_hope}'를 타겟 클래스에서 찾을 수 없음")
    
    # 정규화
    probs = probs_adjusted / probs_adjusted.sum()
    
    # Top 3 추출
    top3_indices = np.argsort(probs)[::-1][:3]
    top3_jobs = [target_le.inverse_transform([idx])[0] for idx in top3_indices]
    top3_probs = [float(probs[idx]) for idx in top3_indices]
    
    return {
        "top3_jobs": top3_jobs,
        "top3_probs": top3_probs,
        "all_probs": probs.tolist(),
        "student_hope": student_hope,
        "parent_hope": parent_data.get('부모_희망직무')
    }
