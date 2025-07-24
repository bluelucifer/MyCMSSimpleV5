import os
import frontmatter
import markdown
from datetime import datetime
import re

def get_posts_dir():
    """포스트 디렉터리 경로 반환"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content', 'posts')

def create_slug(title):
    """제목으로부터 슬러그 생성"""
    # 한글, 영문, 숫자만 남기고 소문자로 변환
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    # 공백을 하이픈으로 변경
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def get_all_posts():
    """모든 포스트를 가져와서 날짜순으로 정렬"""
    posts = []
    posts_dir = get_posts_dir()
    
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
        return posts
    
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(posts_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    
                    # 메타데이터 추출
                    post_data = {
                        'filename': filename,
                        'title': post.metadata.get('title', '제목 없음'),
                        'date': post.metadata.get('date', datetime.now().strftime('%Y-%m-%d')),
                        'category': post.metadata.get('category', ''),
                        'slug': post.metadata.get('slug', create_slug(post.metadata.get('title', filename[:-3]))),
                        'content': post.content
                    }
                    posts.append(post_data)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue
    
    # 날짜순으로 정렬 (최신순)
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts

def get_post_by_slug(slug):
    """슬러그로 특정 포스트 가져오기"""
    posts = get_all_posts()
    for post in posts:
        if post['slug'] == slug:
            return post
    return None

def save_post(old_slug, title, content, date, category=''):
    """포스트 저장"""
    posts_dir = get_posts_dir()
    
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
    
    # 슬러그 생성
    slug = create_slug(title)
    
    # 파일명 생성
    if isinstance(date, str):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
    else:
        date_obj = date
    
    filename = f"{date_obj.strftime('%Y-%m-%d')}-{slug}.md"
    filepath = os.path.join(posts_dir, filename)
    
    # 기존 파일이 있고 슬러그가 변경된 경우 기존 파일 삭제
    if old_slug and old_slug != slug:
        old_post = get_post_by_slug(old_slug)
        if old_post:
            old_filepath = os.path.join(posts_dir, old_post['filename'])
            if os.path.exists(old_filepath):
                os.remove(old_filepath)
    
    # Front matter와 내용 작성
    post = frontmatter.Post(content)
    post.metadata['title'] = title
    post.metadata['date'] = date
    post.metadata['category'] = category
    post.metadata['slug'] = slug
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        return True
    except Exception as e:
        print(f"Error saving post: {e}")
        return False

def delete_post(slug):
    """포스트 삭제"""
    post = get_post_by_slug(slug)
    if not post:
        return False
    
    posts_dir = get_posts_dir()
    filepath = os.path.join(posts_dir, post['filename'])
    
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except Exception as e:
        print(f"Error deleting post: {e}")
    
    return False

def markdown_to_html(content):
    """마크다운을 HTML로 변환"""
    return markdown.markdown(content, extensions=['codehilite', 'fenced_code']) 