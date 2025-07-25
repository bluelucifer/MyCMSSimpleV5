import subprocess
import os
import frontmatter
import markdown
from datetime import datetime
import re
import json

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

def get_pages_dir():
    """페이지 디렉터리 경로 반환"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content', 'pages')

def create_page_slug(title):
    """제목으로부터 페이지 슬러그 생성"""
    # 한글, 영문, 숫자만 남기고 소문자로 변환
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    # 공백을 하이픈으로 변경
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def get_all_pages():
    """모든 페이지를 가져와서 제목순으로 정렬"""
    pages = []
    pages_dir = get_pages_dir()
    
    if not os.path.exists(pages_dir):
        os.makedirs(pages_dir)
        return pages
    
    for filename in os.listdir(pages_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(pages_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    page = frontmatter.load(f)
                    
                    # 메타데이터 추출
                    page_data = {
                        'filename': filename,
                        'title': page.metadata.get('title', '제목 없음'),
                        'slug': page.metadata.get('slug', create_page_slug(page.metadata.get('title', filename[:-3]))),
                        'content': page.content,
                        'created_at': page.metadata.get('created_at', datetime.now().strftime('%Y-%m-%d'))
                    }
                    pages.append(page_data)
            except Exception as e:
                print(f"Error reading page {filename}: {e}")
                continue
    
    # 제목순으로 정렬
    pages.sort(key=lambda x: x['title'])
    return pages

def get_page_by_slug(slug):
    """슬러그로 특정 페이지 가져오기"""
    pages = get_all_pages()
    for page in pages:
        if page['slug'] == slug:
            return page
    return None

def save_page(old_slug, title, content):
    """페이지 저장"""
    pages_dir = get_pages_dir()
    
    if not os.path.exists(pages_dir):
        os.makedirs(pages_dir)
    
    # 슬러그 생성
    slug = create_page_slug(title)
    
    # 파일명 생성
    filename = f"{slug}.md"
    filepath = os.path.join(pages_dir, filename)
    
    # 기존 파일이 있고 슬러그가 변경된 경우 기존 파일 삭제
    if old_slug and old_slug != slug:
        old_page = get_page_by_slug(old_slug)
        if old_page:
            old_filepath = os.path.join(pages_dir, old_page['filename'])
            if os.path.exists(old_filepath):
                os.remove(old_filepath)
    
    # Front matter와 내용 작성
    page = frontmatter.Post(content)
    page.metadata['title'] = title
    page.metadata['slug'] = slug
    page.metadata['created_at'] = datetime.now().strftime('%Y-%m-%d')
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(page))
        return True
    except Exception as e:
        print(f"Error saving page: {e}")
        return False

def delete_page(slug):
    """페이지 삭제"""
    page = get_page_by_slug(slug)
    if not page:
        return False
    
    pages_dir = get_pages_dir()
    filepath = os.path.join(pages_dir, page['filename'])
    
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except Exception as e:
        print(f"Error deleting page: {e}")
    
    return False

def page_markdown_to_html(content):
    """페이지 마크다운을 HTML로 변환"""
    return markdown.markdown(content, extensions=['codehilite', 'fenced_code'])

def get_config_file_path():
    """설정 파일 경로 반환"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')

def load_config():
    """설정 파일 로드"""
    config_path = get_config_file_path()
    
    # 기본 설정
    default_config = {
        "blog_title": "My Simple Blog",
        "author_name": "블로거",
        "blog_description": "간단한 CMS로 만든 블로그",
        "posts_per_page": 10,
        "github_username": "",
        "twitter_username": "",
        "email": ""
    }
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 기본 설정과 병합 (새로운 설정 키가 추가된 경우 대비)
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        else:
            # 설정 파일이 없으면 기본 설정으로 생성
            save_config(default_config)
            return default_config
    except Exception as e:
        print(f"Error loading config: {e}")
        return default_config

def save_config(config):
    """설정 파일 저장"""
    config_path = get_config_file_path()
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False 