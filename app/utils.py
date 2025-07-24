import subprocess
import os

def run_git_command(command):
    """Git 명령 실행"""
    try:
        # 프로젝트 루트 디렉터리로 이동
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        result = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"Git command executed: {' '.join(command)}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        
        return result
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Git command failed: {' '.join(command)}\nError: {e.stderr}"
        print(error_msg)
        raise Exception(error_msg)
    except FileNotFoundError:
        error_msg = "Git이 설치되어 있지 않거나 PATH에 없습니다."
        print(error_msg)
        raise Exception(error_msg) 