from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from datetime import datetime
from app.post_parser import get_all_posts, get_post_by_slug, save_post, delete_post
from app.builder import build_site
from app.utils import run_git_command

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# 설정
app.config['POSTS_DIR'] = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content', 'posts')
app.config['SITE_DIR'] = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_site')
app.config['SECRET_KEY'] = 'your-secret-key-here'

@app.route('/')
def index():
    """메인 페이지 - 글 목록으로 리다이렉트"""
    return redirect(url_for('posts_list'))

@app.route('/posts')
def posts_list():
    """글 목록 페이지"""
    posts = get_all_posts()
    return render_template('posts_list.html', posts=posts)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    """새 글 작성 페이지"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
        category = request.form.get('category', '')
        
        if title and content:
            success = save_post(None, title, content, date, category)
            if success:
                return redirect(url_for('posts_list'))
        
    return render_template('post_form.html', post=None)

@app.route('/posts/edit/<slug>', methods=['GET', 'POST'])
def edit_post(slug):
    """글 수정 페이지"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        date = request.form.get('date')
        category = request.form.get('category', '')
        
        if title and content:
            success = save_post(slug, title, content, date, category)
            if success:
                return redirect(url_for('posts_list'))
    
    post = get_post_by_slug(slug)
    if not post:
        return redirect(url_for('posts_list'))
    
    return render_template('post_form.html', post=post)

@app.route('/posts/delete/<slug>', methods=['POST'])
def delete_post_route(slug):
    """글 삭제"""
    success = delete_post(slug)
    return redirect(url_for('posts_list'))

@app.route('/preview', methods=['POST'])
def preview():
    """마크다운 미리보기"""
    import markdown
    
    content = request.json.get('content', '') if request.is_json else request.form.get('content', '')
    html = markdown.markdown(content)
    
    return jsonify({'html': html})

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    """사이트 빌드 및 GitHub Pages 배포"""
    try:
        # 사이트 빌드
        build_site()
        
        # Git 명령 실행
        run_git_command(['git', 'add', '.'])
        commit_message = f"Blog update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        run_git_command(['git', 'commit', '-m', commit_message])
        run_git_command(['git', 'push', 'origin', 'gh-pages'])
        
        message = "배포가 성공적으로 완료되었습니다!"
        
    except Exception as e:
        message = f"배포 중 오류가 발생했습니다: {str(e)}"
    
    posts = get_all_posts()
    return render_template('posts_list.html', posts=posts, message=message)

if __name__ == '__main__':
    app.run(debug=True) 