import json
import os

DATA_DIR = "user_data"

def ensure_data_dir():
    """데이터 저장 디렉토리 확인 및 생성"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def get_file_path(student_id):
    """학생 ID를 기반으로 안전한 파일 경로 생성"""
    # 파일명에 쓸 수 없는 특수문자 제거
    safe_id = "".join([c for c in student_id if c.isalnum() or c in (' ', '_', '-', '(', ')')])
    return os.path.join(DATA_DIR, f"{safe_id}.json")

def save_user_data(student_id, student_data=None, parent_data=None, prescription=None, cache_key=None):
    """사용자 데이터(학생, 부모, 결과)를 JSON 파일로 저장"""
    ensure_data_dir()
    file_path = get_file_path(student_id)
    
    # 기존 데이터 로드 (덮어쓰기 방지)
    current_data = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        except Exception:
            pass
    
    # 데이터 업데이트
    if student_data is not None:
        current_data['student_data'] = student_data
    if parent_data is not None:
        current_data['parent_data'] = parent_data
        
    # 처방전 결과 캐싱 (키와 결과를 함께 저장)
    if prescription is not None and cache_key is not None:
        if 'prescriptions' not in current_data:
            current_data['prescriptions'] = {}
        current_data['prescriptions'][cache_key] = prescription
        
    # 파일 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(current_data, f, ensure_ascii=False, indent=2)

def load_user_data(student_id):
    """학생 ID로 저장된 데이터 불러오기"""
    file_path = get_file_path(student_id)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    return None