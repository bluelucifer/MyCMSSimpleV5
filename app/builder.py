import os
import shutil
from jinja2 import Environment, FileSystemLoader
from app.post_parser import get_all_posts, markdown_to_html

def get_site_dir():
    """사이트 빌드 디렉터리 경로 반환"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_site')

def get_templates_dir():
    """템플릿 디렉터리 경로 반환"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')

def get_static_dir():
    """정적 파일 디렉터리 경로 반환"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')

def build_site():
    """정적 사이트 빌드"""
    site_dir = get_site_dir()
    templates_dir = get_templates_dir()
    static_dir = get_static_dir()
    
    # _site 디렉터리 초기화
    if os.path.exists(site_dir):
        shutil.rmtree(site_dir)
    os.makedirs(site_dir)
    
    # static 폴더 복사
    if os.path.exists(static_dir):
        shutil.copytree(static_dir, os.path.join(site_dir, 'static'))
    
    # Jinja2 환경 설정
    env = Environment(loader=FileSystemLoader(templates_dir))
    
    # 모든 포스트 가져오기
    posts = get_all_posts()
    
    # 메인 페이지 생성 (index.html)
    try:
        index_template = env.get_template('public_index.html')
        index_html = index_template.render(posts=posts)
        
        with open(os.path.join(site_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(index_html)
    except Exception as e:
        print(f"Error building index page: {e}")
    
    # 개별 포스트 페이지 생성
    try:
        post_template = env.get_template('public_post.html')
        
        for post in posts:
            # 마크다운을 HTML로 변환
            post['html_content'] = markdown_to_html(post['content'])
            
            # 포스트 페이지 렌더링
            post_html = post_template.render(post=post)
            
            # 파일 저장
            post_filename = f"{post['slug']}.html"
            with open(os.path.join(site_dir, post_filename), 'w', encoding='utf-8') as f:
                f.write(post_html)
                
    except Exception as e:
        print(f"Error building post pages: {e}")
    
    print(f"Site built successfully in {site_dir}") 