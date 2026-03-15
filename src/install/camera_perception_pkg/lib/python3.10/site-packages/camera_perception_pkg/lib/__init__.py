import os
import types
import importlib.util

def get_path(file_name=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    return file_path


def load_module(module_file):
    file_path = get_path(module_file)
    print(f'\n[INFO] 라이브러리 로드 시도: {file_path}\n')
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

    spec = importlib.util.spec_from_file_location('camera_perception_func_lib', file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

camera_perception_func_lib = load_module("camera_perception_func_lib.py")
