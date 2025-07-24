# To-Do List: GitHub Pages 단순 CMS 개발

이 문서는 "GitHub Pages 단순 CMS" 프로젝트의 PRD를 기반으로 작성된 상세 개발 To-Do 리스트입니다. 각 태스크는 AI IDE의 도움을 받아 1시간 이내 구현 목표를 염두에 두고 세분화되었습니다.

---

## 1. 초기 환경 설정 및 프로젝트 구조

*   [ ] 프로젝트 루트 디렉터리 생성 (`MyCMSSimpleV5` 아래에서 작업 시작).
*   [ ] Python 가상 환경 생성 및 활성화:
    *   `python -m venv .venv`
    *   `source .venv/bin/activate` (macOS/Linux) 또는 `.venv\Scripts\activate` (Windows)
*   [ ] 필요한 Python 패키지 설치:
    *   `pip install Flask markdown python-frontmatter`
*   [ ] 기본 디렉터리 구조 생성:
    *   `app/` (Flask 애플리케이션 코드가 들어갈 곳)
    *   `content/posts/` (사용자가 작성한 Markdown 파일 저장)
    *   `templates/` (Jinja2 템플릿 파일 저장)
    *   `static/` (Tailwind CSS, 이미지 등 정적 파일 저장)
    *   `_site/` (빌드된 정적 HTML 파일 출력 경로 - GitHub Pages 배포용)
    *   `docs/` (PRD, To-Do 리스트 등 문서)
*   [ ] `.gitignore` 파일 생성 및 다음 항목 추가:
    *   `.venv/`
    *   `__pycache__/`
    *   `*.pyc`
    *   `_site/` (빌드된 결과는 Git으로 관리하지 않음)
*   [ ] `app/__init__.py` 또는 `app/app.py` 등 Flask 애플리케이션 시작 파일 생성 (예: `app/app.py`).

## 2. 백엔드 개발 (Flask 애플리케이션)

### 2.1. Flask 애플리케이션 기본 설정
*   [ ] `app/app.py`에 Flask 앱 초기화 코드 작성.
    ```python
    from flask import Flask, render_template, request, redirect, url_for, jsonify
    import os
    
    app = Flask(__name__)
    app.config['POSTS_DIR'] = os.path.join(os.getcwd(), 'content', 'posts')
    app.config['SITE_DIR'] = os.path.join(os.getcwd(), '_site')
    # ... 기타 설정
    ```
*   [ ] 기본 라우트 (`/`) 설정 (글 목록 페이지로 리다이렉트 또는 직접 렌더링).

### 2.2. Markdown 파일 처리 로직 (`app/post_parser.py` 또는 `app/utils.py`)
*   [ ] `content/posts/` 폴더에서 Markdown 파일 목록을 읽는 함수 구현:
    *   [ ] 파일 경로를 순회하며 `.md` 파일 식별.
    *   [ ] `python-frontmatter` 라이브러리를 사용하여 각 파일의 YAML Front Matter 및 본문 파싱.
    *   [ ] 파싱된 데이터(제목, 날짜, slug 등)를 딕셔너리 또는 객체 리스트 형태로 반환.
    *   [ ] 날짜 기준으로 최신순으로 정렬하는 로직 포함.
*   [ ] 개별 Markdown 파일의 내용을 HTML로 변환하는 함수 구현:
    *   [ ] `markdown` 라이브러리를 사용하여 Markdown 텍스트를 HTML로 변환.

### 2.3. 글 관리 기능 엔드포인트 (`app/routes.py` 또는 `app/app.py`에 직접 구현)
*   [ ] **글 목록 페이지 (`/` 또는 `/posts`):**
    *   [ ] `@app.route('/')` 또는 `@app.route('/posts')` 데코레이터 설정.
    *   [ ] `post_parser`에서 글 목록 데이터를 불러와 `render_template`로 `posts_list.html`에 전달.
*   [ ] **새 글 작성 페이지 (`/posts/new`):**
    *   [ ] `@app.route('/posts/new', methods=['GET', 'POST'])` 설정.
    *   [ ] `GET` 요청 시 빈 글 작성 폼 렌더링 (`post_form.html`).
    *   [ ] `POST` 요청 시 폼 데이터(제목, 내용 등)를 받아 새 Markdown 파일 생성:
        *   [ ] 파일명 `YYYY-MM-DD-slug.md` 형식으로 자동 생성.
        *   [ ] YAML Front Matter와 본문 내용을 포함하여 `content/posts/`에 저장.
        *   [ ] 저장 후 글 목록 페이지로 리다이렉트.
*   [ ] **글 수정 페이지 (`/posts/edit/<slug>`):**
    *   [ ] `@app.route('/posts/edit/<slug>', methods=['GET', 'POST'])` 설정.
    *   [ ] `GET` 요청 시 해당 `slug`의 Markdown 파일 내용을 불러와 폼에 채우고 `post_form.html` 렌더링.
    *   [ ] `POST` 요청 시 폼 데이터를 받아 기존 Markdown 파일 업데이트 (파일명 변경 시 고려).
        *   [ ] 저장 후 글 목록 페이지로 리다이렉트.
*   [ ] **미리보기 기능 (`/preview`, AJAX 요청):**
    *   [ ] `@app.route('/preview', methods=['POST'])` 설정.
    *   [ ] `request.json` 또는 `request.form`으로 Markdown 텍스트를 받아 `post_parser`의 HTML 변환 함수 호출.
    *   [ ] 변환된 HTML을 `jsonify`로 반환.
*   [ ] **글 삭제 기능 (`/posts/delete/<slug>`, POST 또는 GET 요청 허용):**
    *   [ ] `@app.route('/posts/delete/<slug>', methods=['POST'])` 설정.
    *   [ ] 해당 `slug`의 Markdown 파일을 `content/posts/`에서 찾아 삭제.
    *   [ ] 삭제 후 글 목록 페이지로 리다이렉트.

### 2.4. 빌드 및 배포 로직 (Flask 엔드포인트)
*   [ ] **빌드 함수 (`app/builder.py` 또는 `app/utils.py`):**
    *   [ ] `_site/` 디렉터리 존재 여부 확인 및 생성/초기화 (기존 파일 삭제).
    *   [ ] `static/` 폴더의 모든 내용을 `_site/static/`으로 복사.
    *   [ ] **메인 페이지 (`index.html`) 생성:**
        *   [ ] 글 목록 데이터를 사용하여 `templates/public_index.html` 템플릿 렌더링.
        *   [ ] 렌더링된 HTML을 `_site/index.html`로 저장.
    *   [ ] **개별 글 페이지 생성:**
        *   [ ] `content/posts/`의 각 Markdown 파일을 순회.
        *   [ ] 각 파일을 HTML로 변환하고 `templates/public_post.html` 템플릿에 전달하여 렌더링.
        *   [ ] 렌더링된 HTML을 `_site/<slug>.html` 형태로 저장.
*   [ ] **배포 엔드포인트 (`/publish`):**
    *   [ ] `@app.route('/publish')` 설정 (GET 또는 POST).
    *   [ ] 빌드 함수 호출.
    *   [ ] Python `subprocess` 모듈을 사용하여 다음 Git/GitHub CLI 명령어 실행:
        *   `git add .` (새로 생성된 `_site/` 폴더와 그 내용 추가)
        *   `git commit -m "Blog update: $(date +'%Y-%m-%d %H:%M:%S')"` (현재 시각을 포함한 커밋 메시지)
        *   `git push origin main` (또는 GitHub Pages 설정에 따른 브랜치, 보통 `main` 또는 `gh-pages`)
    *   [ ] Git 명령 실행 결과를 UI에 반환하거나 성공/실패 메시지와 함께 리다이렉트.

## 3. 프론트엔드 개발 (HTML, Jinja2, Tailwind CSS)

### 3.1. 기본 레이아웃 및 Tailwind CSS 설정
*   [ ] `templates/base.html` Jinja2 템플릿 생성:
    *   [ ] `<!DOCTYPE html>`, `<html>`, `<head>`, `<body>` 기본 구조.
    *   [ ] `{% block title %}` 설정.
    *   [ ] Tailwind CSS CDN 링크 포함 (`<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">`).
    *   [ ] 공통 헤더 (`<header>`) 및 푸터 (`<footer>`) 섹션 정의 (Tailwind CSS 클래스 적용).
    *   [ ] `{% block content %}` 정의.
*   [ ] (선택사항: Tailwind CLI를 통한 빌드 시) `tailwind.config.js` 및 `postcss.config.js` 파일 생성. (CDN 사용 시 불필요).

### 3.2. 관리 도구 UI 템플릿 (`templates/`)
*   [ ] **글 목록 페이지 (`posts_list.html`):**
    *   [ ] `{% extends 'base.html' %}` 사용.
    *   [ ] "새 글 작성" 버튼 (`/posts/new` 링크).
    *   [ ] "블로그 배포" 버튼 (`/publish` 링크 또는 POST 요청).
    *   [ ] Jinja2 `{% for post in posts %}` 루프를 사용하여 글 목록 테이블 또는 카드 형태로 표시.
        *   [ ] 각 글의 제목, 작성일.
        *   [ ] "수정" 버튼 (링크: `/posts/edit/{{ post.slug }}`).
        *   [ ] "삭제" 버튼 (폼을 이용한 POST 요청 또는 JavaScript `confirm`과 함께 GET 요청).
    *   [ ] Tailwind CSS 클래스를 사용하여 목록 및 버튼 스타일링.
*   [ ] **새/수정 글 작성 페이지 (`post_form.html`):**
    *   [ ] `{% extends 'base.html' %}` 사용.
    *   [ ] 제목 (`<input type="text">`), 작성일 (`<input type="date">`), 카테고리 (`<input type="text">`) 입력 필드.
    *   [ ] Markdown 내용을 입력할 `<textarea id="markdown-input">` (높이 조절).
    *   [ ] Markdown 미리보기 영역 (`<div id="preview-output">`).
    *   [ ] "저장" 버튼 (`<button type="submit">`).
    *   [ ] JavaScript를 사용하여 `<textarea>` 내용 변경 시 `/preview` 엔드포인트로 AJAX 요청을 보내 미리보기 영역 업데이트.
        *   [ ] `fetch` API 사용.
        *   [ ] `setTimeout`으로 입력 지연 후 미리보기 업데이트하여 서버 부하 감소.
    *   [ ] Tailwind CSS 클래스를 사용하여 폼 요소 및 레이아웃 스타일링.

### 3.3. 퍼블리싱될 블로그 페이지 템플릿 (`templates/`)
*   [ ] **메인 페이지 템플릿 (`public_index.html`):**
    *   [ ] 빌드 시 사용될 템플릿. (관리 도구와는 별개).
    *   [ ] 블로그 제목, 로고 등 헤더 영역.
    *   [ ] 글 목록 (최신 글 위주, 제목 클릭 시 개별 글로 이동).
    *   [ ] 푸터 영역.
    *   [ ] Tailwind CSS 적용.
*   [ ] **개별 글 페이지 템플릿 (`public_post.html`):**
    *   [ ] 빌드 시 사용될 템플릿.
    *   [ ] 글 제목, 작성일, HTML 변환된 본문 내용 표시.
    *   [ ] Tailwind CSS 적용.

## 4. Git / GitHub Pages 연동

*   [ ] **`app/utils.py` (또는 별도 모듈)에 Git 명령 실행 함수 구현:**
    *   [ ] `run_git_command(command)`: `subprocess.run`을 사용하여 Git 명령 실행, 결과 반환.
*   [ ] **`/publish` 엔드포인트에서 Git 명령 호출:**
    *   [ ] `run_git_command(['git', 'add', app.config['SITE_DIR']])` (또는 `git add .` 후 `git reset`으로 다른 파일 제외)
    *   [ ] `run_git_command(['git', 'commit', '-m', commit_message])`
    *   [ ] `run_git_command(['git', 'push', 'origin', 'main'])`
*   [ ] Git 명령 실행 시 발생하는 에러(예: Git 설치 안됨, 로그인 안됨, 커밋할 변경사항 없음)에 대한 기본적인 예외 처리 및 사용자에게 메시지 전달.

## 5. 테스트 및 개선

*   [ ] Flask 개발 서버 실행 (`flask run`).
*   [ ] 웹 브라우저에서 `http://127.0.0.1:5000` 접속 확인.
*   [ ] "새 글 작성" 기능으로 글 작성 후 저장 확인 (`content/posts/`에 파일 생성).
*   [ ] 글 목록 페이지에 새로 작성된 글 표시 확인.
*   [ ] "수정" 기능으로 글 내용 수정 및 저장 확인.
*   [ ] "미리보기" 기능이 실시간으로 동작하며 Tailwind CSS가 적용되는지 확인.
*   [ ] "배포" 버튼 클릭 후 GitHub 리포지토리에 푸시되는지 확인.
*   [ ] GitHub Pages URL로 접속하여 빌드된 블로그가 정상적으로 보이는지 (메뉴, 글 내용, 스타일) 확인.
*   [ ] "삭제" 기능으로 글 삭제 확인.
*   [ ] 1시간 개발 목표를 위한 기능 최소화 및 단순화.
*   [ ] Flask 앱 구동 시 표시되는 기본 메시지 외에, 사용자에게 의미 있는 피드백 메시지 제공 (예: "배포 성공!", "파일 저장 완료!"). 