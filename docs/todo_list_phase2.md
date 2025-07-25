# To-Do List: MyCMSSimpleV5 기능 확장 (Phase 2)

이 문서는 "prd_phase2_feature_expansion.md" 문서를 기반으로 작성된 Phase 2 개발 To-Do 리스트입니다. 각 기능은 백엔드, 프론트엔드, 데이터 구조 관점에서 세분화되었습니다.

---

## 1. 카테고리 및 태그 시스템

### 1.1. 백엔드 (`app/`)
*   [ ] **`post_parser.py` 수정:**
    *   [ ] YAML Front Matter 파싱 시 `category` (문자열)와 `tags` (리스트) 필드를 읽어오는 로직 추가.
    *   [ ] 태그가 쉼표로 구분된 문자열일 경우, 리스트로 변환하는 처리 로직 추가.
*   [ ] **`builder.py` 수정:**
    *   [ ] 모든 게시물에서 사용된 전체 카테고리 및 태그 목록을 수집하는 함수 구현.
    *   [ ] 수집된 카테고리별로 아카이브 페이지 생성 로직 추가:
        *   [ ] 특정 카테고리에 속한 글 목록 필터링.
        *   [ ] `templates/public_category_archive.html` 템플릿을 사용하여 `_site/category/{카테고리명}.html` 파일 생성.
    *   [ ] 수집된 태그별로 아카이브 페이지 생성 로직 추가:
        *   [ ] 특정 태그를 포함하는 글 목록 필터링.
        *   [ ] `templates/public_tag_archive.html` 템플릿을 사용하여 `_site/tags/{태그명}.html` 파일 생성.
*   [ ] **`app.py` 수정:**
    *   [ ] 글 저장/수정 시 `category`, `tags` 데이터를 받아 Front Matter에 저장하는 로직 수정.

### 1.2. 프론트엔드 (`templates/`)
*   [ ] **`post_form.html` 수정:**
    *   [ ] '카테고리'를 입력할 `<input type="text">` 필드 추가.
    *   [ ] '태그'를 입력할 `<input type="text">` 필드 추가 (placeholder로 "쉼표로 구분하여 입력" 안내).
*   [ ] **`public_post.html` 수정:**
    *   [ ] 글 본문 상단 또는 하단에 카테고리 및 태그 목록 표시.
    *   [ ] 각 카테고리/태그에 해당 아카이브 페이지로 이동하는 링크 추가.
*   [ ] **`public_index.html` 수정:**
    *   [ ] 각 글 목록 아이템에 카테고리/태그 표시.
    *   [ ] (선택) 사이드바 등에 전체 카테고리/태그 클라우드 표시.
*   [ ] **신규 템플릿 생성:**
    *   [ ] `public_category_archive.html`: 카테고리별 글 목록을 표시하는 템플릿.
    *   [ ] `public_tag_archive.html`: 태그별 글 목록을 표시하는 템플릿.

---

## 2. 이미지 관리 기능

### 2.1. 백엔드 (`app/`)
*   [ ] **`app.py`에 신규 엔드포인트 추가:**
    *   [ ] `@app.route('/upload/image', methods=['POST'])` 라우트 생성.
    *   [ ] `request.files`에서 이미지 파일을 받아 `static/images` 디렉터리에 저장하는 로직 구현.
    *   [ ] `werkzeug.utils.secure_filename`을 사용하여 파일명을 안전하게 처리.
    *   [ ] 업로드 성공 시, 저장된 이미지의 URL(예: `/static/images/image.png`)을 JSON 형식으로 반환.
*   [ ] **`app.py` 설정 추가:**
    *   [ ] `app.config['IMAGE_UPLOAD_FOLDER']` 설정 추가 및 `static/images` 디렉터리 존재 여부 확인/생성 로직 추가.

### 2.2. 프론트엔드 (`templates/`)
*   [ ] **`post_form.html` 수정:**
    *   [ ] Markdown 입력 `<textarea>` 근처에 '이미지 업로드' `<input type="file" accept="image/*">` 버튼 추가.
    *   [ ] 이미지 파일 선택 시, `fetch` API를 사용하여 `/upload/image` 엔드포인트로 비동기 POST 요청을 보내는 JavaScript 코드 작성.
    *   [ ] 업로드 성공 후, 반환된 이미지 URL로 Markdown 이미지 태그를 생성하여 `<textarea>`에 삽입하거나 클립보드에 복사하는 기능 구현.

### 2.3. 디렉터리 구조
*   [ ] `static/images/` 디렉터리 생성 및 `.gitignore`에 추가되지 않도록 확인.

---

## 3. 정적 페이지 관리

### 3.1. 백엔드 (`app/`)
*   [ ] **파서 로직 추가 (`app/utils.py` 또는 신규 파일):**
    *   [ ] `content/pages/` 디렉터리에서 Markdown 파일을 읽고 파싱하는 함수 구현 (기존 `post_parser` 재활용/확장).
*   [ ] **`app.py`에 신규 라우트 추가:**
    *   [ ] `/pages`: 페이지 목록을 보여주는 라우트.
    *   [ ] `/pages/new`: 새 페이지 작성 폼을 보여주는 라우트.
    *   [ ] `/pages/edit/<slug>`: 기존 페이지 수정 폼을 보여주는 라우트.
    *   [ ] `/pages/delete/<slug>`: 페이지를 삭제하는 라우트.
*   [ ] **`builder.py` 수정:**
    *   [ ] `content/pages/` 디렉터리의 `.md` 파일을 HTML로 변환하여 `_site/{slug}.html` 형태로 저장하는 로직 추가.

### 3.2. 프론트엔드 (`templates/`)
*   [ ] **신규 템플릿 생성:**
    *   [ ] `pages_list.html`: 페이지 목록 관리 템플릿 (기존 `posts_list.html` 기반으로 작성).
    *   [ ] `page_form.html`: 페이지 작성/수정 폼 템플릿 (기존 `post_form.html` 기반으로 작성).
    *   [ ] `public_page.html`: 최종 방문자에게 보여질 개별 페이지 템플릿.
*   [ ] **`base.html` 수정:**
    *   [ ] 관리자 화면 네비게이션에 '페이지 관리' 메뉴 추가.
    *   [ ] (선택) 빌드된 사이트의 헤더나 푸터에 정적 페이지 목록('소개' 등) 링크 자동 생성.

### 3.3. 디렉터리 구조
*   [ ] `content/pages/` 디렉터리 생성.

---

## 4. 사이트 전역 설정 관리

### 4.1. 백엔드 (`app/`)
*   [ ] **설정 관리 로직 추가 (`app/utils.py`):**
    *   [ ] `config.json` 파일을 읽고 쓰는 함수 구현 (`load_config`, `save_config`).
*   [ ] **`app.py` 수정:**
    *   [ ] 애플리케이션 시작 시 `config.json`을 로드하여 `app.config` 또는 `g` (전역 컨텍스트)에 저장.
    *   [ ] `@app.route('/settings', methods=['GET', 'POST'])` 라우트 추가.
        *   `GET` 요청 시: `config.json` 내용을 읽어 템플릿에 전달.
        *   `POST` 요청 시: 폼 데이터를 받아 `config.json` 파일에 저장.
*   [ ] **`builder.py` 및 모든 템플릿 렌더링 로직 수정:**
    *   [ ] 템플릿 렌더링 시, 로드된 `config` 객체를 함께 전달하여 `{{ config.blog_title }}` 형태로 사용 가능하도록 수정.

### 4.2. 프론트엔드 (`templates/`)
*   [ ] **신규 템플릿 생성:**
    *   [ ] `settings.html`: 사이트 설정을 수정할 수 있는 폼을 포함하는 템플릿.
*   [ ] **기존 모든 템플릿 수정 (`base.html`, `public_*.html` 등):**
    *   [ ] 하드코딩된 블로그 제목, 저자명 등을 `{{ config.blog_title }}`와 같은 템플릿 변수로 교체.
*   [ ] **`base.html` 수정:**
    *   [ ] 관리자 화면 네비게이션에 '설정' 메뉴 추가.

### 4.3. 파일 구조
*   [ ] 프로젝트 루트에 `config.json` 파일 생성 및 기본값 작성.
    ```json
    {
      "blog_title": "My Blog",
      "author_name": "Your Name"
    }
    ``` 