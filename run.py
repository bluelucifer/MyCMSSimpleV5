#!/usr/bin/env python3
"""
My Simple CMS - Flask 애플리케이션 실행 스크립트
"""

from app.app import app

if __name__ == '__main__':
    print("🚀 My Simple CMS가 시작됩니다!")
    print("📝 관리자 페이지: http://127.0.0.1:5000")
    print("✨ 새 글 작성: http://127.0.0.1:5000/posts/new")
    print("🔧 Ctrl+C로 종료할 수 있습니다.")
    print("-" * 50)
    
    app.run(debug=True, host='127.0.0.1', port=5000) 