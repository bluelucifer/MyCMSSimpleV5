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

def parse_tags(tags_input):
    """태그 입력을 리스트로 변환"""
    if not tags_input:
        return []
    
    if isinstance(tags_input, list):
        return [tag.strip() for tag in tags_input if tag.strip()]
    
    # 쉼표로 구분된 문자열을 리스트로 변환
    if isinstance(tags_input, str):
        return [tag.strip() for tag in tags_input.split(',') if tag.strip()]
    
    return []

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
                        'tags': parse_tags(post.metadata.get('tags', [])),
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

def save_post(old_slug, title, content, date, category='', tags=''):
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
    post.metadata['tags'] = parse_tags(tags)
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

def get_all_categories():
    """모든 포스트에서 사용된 카테고리 목록 반환"""
    posts = get_all_posts()
    categories = set()
    for post in posts:
        if post.get('category'):
            categories.add(post['category'])
    return sorted(list(categories))

def get_all_tags():
    """모든 포스트에서 사용된 태그 목록 반환"""
    posts = get_all_posts()
    tags = set()
    for post in posts:
        if post.get('tags'):
            tags.update(post['tags'])
    return sorted(list(tags))

def get_posts_by_category(category):
    """특정 카테고리의 포스트들 반환"""
    posts = get_all_posts()
    return [post for post in posts if post.get('category') == category]

def get_posts_by_tag(tag):
    """특정 태그의 포스트들 반환"""
    posts = get_all_posts()
    return [post for post in posts if tag in post.get('tags', [])]

def markdown_to_html(content):
    """마크다운을 HTML로 변환"""
    return markdown.markdown(content, extensions=['codehilite', 'fenced_code']) 