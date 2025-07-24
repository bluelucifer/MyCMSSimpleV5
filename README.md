# My Simple CMS

GitHub Pages를 위한 간단한 블로그 CMS입니다. Flask로 개발된 관리 도구로 마크다운 글을 작성하고, 정적 사이트로 빌드하여 GitHub Pages에 배포할 수 있습니다.

## 🚀 주요 기능

- ✍️ **마크다운 에디터**: 실시간 미리보기와 함께 글 작성
- 📝 **글 관리**: 글 목록, 수정, 삭제 기능
- 🎨 **깔끔한 UI**: Tailwind CSS로 제작된 모던한 인터페이스
- 📱 **반응형 디자인**: 모바일과 데스크톱 모두 지원
- 🚀 **원클릭 배포**: GitHub Pages로 자동 배포
- 💻 **코드 하이라이팅**: Prism.js를 사용한 문법 강조

## 📋 요구사항

- Python 3.7+
- Git
- GitHub 계정

## 🛠️ 설치 및 실행

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/MyCMSSimpleV5.git
cd MyCMSSimpleV5
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\Scripts\activate     # Windows
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행

```bash
python run.py
```

브라우저에서 `http://127.0.0.1:5000`으로 접속하면 관리자 페이지가 나타납니다.

## 📝 사용법

### 글 작성

1. 관리자 페이지에서 "새 글 작성" 버튼 클릭
2. 제목, 날짜, 카테고리 입력
3. 마크다운으로 내용 작성 (오른쪽에서 실시간 미리보기 확인)
4. "저장" 버튼 클릭

### 블로그 배포

1. 글 목록 페이지에서 "블로그 배포" 버튼 클릭
2. 자동으로 정적 사이트가 빌드되고 `gh-pages` 브랜치에 푸시됩니다
3. GitHub Pages 설정에서 `gh-pages` 브랜치를 소스로 설정

### GitHub Pages 설정

1. GitHub 저장소 → Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` 선택
4. 몇 분 후 `https://your-username.github.io/your-repo-name`에서 블로그 확인

## 📁 프로젝트 구조

```
MyCMSSimpleV5/
├── app/                    # Flask 애플리케이션
│   ├── app.py             # 메인 애플리케이션
│   ├── post_parser.py     # 마크다운 파싱
│   ├── builder.py         # 정적 사이트 빌드
│   └── utils.py           # 유틸리티 함수
├── content/posts/         # 마크다운 글 저장소
├── templates/             # Jinja2 템플릿
│   ├── base.html          # 기본 레이아웃
│   ├── posts_list.html    # 글 목록 (관리자)
│   ├── post_form.html     # 글 작성/수정 폼
│   ├── public_index.html  # 블로그 메인 페이지
│   └── public_post.html   # 블로그 글 페이지
├── static/                # 정적 파일 (CSS, JS, 이미지)
├── _site/                 # 빌드된 정적 사이트 (자동 생성)
├── run.py                 # 실행 스크립트
└── requirements.txt       # Python 의존성
```

## 🎨 커스터마이징

### 블로그 제목 변경

`templates/public_index.html`과 `templates/public_post.html`에서 "My Simple Blog" 부분을 원하는 제목으로 변경하세요.

### 스타일 수정

템플릿 파일들에서 Tailwind CSS 클래스를 수정하여 디자인을 변경할 수 있습니다.

### 새로운 기능 추가

`app/app.py`에 새로운 라우트를 추가하고, 해당 템플릿을 만들어 기능을 확장할 수 있습니다.

## 🔧 개발 모드

개발 중에는 Flask의 디버그 모드가 활성화되어 있어 코드 변경 시 자동으로 서버가 재시작됩니다.

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다!

---

**Happy Blogging!** 🎉 