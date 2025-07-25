import os
import shutil
from jinja2 import Environment, FileSystemLoader
from app.post_parser import get_all_posts, markdown_to_html, get_all_categories, get_all_tags, get_posts_by_category, get_posts_by_tag

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
    
    # 카테고리 아카이브 페이지 생성
    try:
        categories = get_all_categories()
        category_template = env.get_template('public_category_archive.html')
        
        # category 디렉터리 생성
        category_dir = os.path.join(site_dir, 'category')
        os.makedirs(category_dir, exist_ok=True)
        
        for category in categories:
            category_posts = get_posts_by_category(category)
            # 각 포스트의 마크다운을 HTML로 변환
            for post in category_posts:
                post['html_content'] = markdown_to_html(post['content'])
            
            category_html = category_template.render(category=category, posts=category_posts)
            
            # 카테고리 파일명을 안전하게 생성
            safe_category = category.replace(' ', '-').replace('/', '-')
            category_filename = f"{safe_category}.html"
            
            with open(os.path.join(category_dir, category_filename), 'w', encoding='utf-8') as f:
                f.write(category_html)
                
    except Exception as e:
        print(f"Error building category pages: {e}")
    
    # 태그 아카이브 페이지 생성
    try:
        tags = get_all_tags()
        tag_template = env.get_template('public_tag_archive.html')
        
        # tags 디렉터리 생성
        tags_dir = os.path.join(site_dir, 'tags')
        os.makedirs(tags_dir, exist_ok=True)
        
        for tag in tags:
            tag_posts = get_posts_by_tag(tag)
            # 각 포스트의 마크다운을 HTML로 변환
            for post in tag_posts:
                post['html_content'] = markdown_to_html(post['content'])
            
            tag_html = tag_template.render(tag=tag, posts=tag_posts)
            
            # 태그 파일명을 안전하게 생성
            safe_tag = tag.replace(' ', '-').replace('/', '-')
            tag_filename = f"{safe_tag}.html"
            
            with open(os.path.join(tags_dir, tag_filename), 'w', encoding='utf-8') as f:
                f.write(tag_html)
                
    except Exception as e:
        print(f"Error building tag pages: {e}")
    
    print(f"Site built successfully in {site_dir}") 