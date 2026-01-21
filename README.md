# todo_vibe

간단한 교육용 Flask ToDo 데모 애플리케이션

**개요**

- 이 저장소는 수업 및 실습용으로 만든 간단한 ToDo 웹 애플리케이션입니다. 기본 기능으로 회원가입/로그인, 할 일 생성·수정·삭제, 카테고리와 완료 표시를 제공합니다.
- UI는 Bootstrap 5 기반으로 리팩터링되었고, Alembic 마이그레이션과 Docker 지원을 포함합니다.

**주요 기능**

- 사용자 인증(간단한 데모용)
- 할 일 CRUD (제목, 설명, 카테고리, 마감일, 완료 상태)
- 카테고리별 색상 표시 및 간단한 필터링
- RESTful API 엔드포인트 및 통합 테스트

**사전 준비**

- Python 3.8 이상(권장 3.11)
- 권장: 가상환경 사용
- 선택: Docker Desktop (Postgres 사용 시)

**설치 및 실행 (로컬, SQLite)**

1. 가상환경 생성 및 활성화

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. 의존성 설치

```powershell
pip install -r requirements.txt
```

3. 애플리케이션 실행

```powershell
python app.py
```

웹 브라우저에서 http://localhost:5000 접속

**Docker + Postgres로 실행**

1. Docker로 서비스 빌드 및 시작

```bash
docker-compose up --build -d
```

2. http://localhost:5000 접속

로컬 개발용 기본 Postgres 자격정보는 `docker-compose.yml`을 참조하세요.

**테스트**

로컬에서 제공되는 테스트 실행 (SQLite 사용)

```bash
python -m pytest
```

통합 테스트는 `tests/test_api_full.py`에 포함되어 있습니다.

**마이그레이션**

Alembic 설정이 포함되어 있습니다. DB 마이그레이션 적용:

```bash
alembic upgrade head
```

**구조 요약**

- app.py: 진입점
- app_schemas.py: 요청/응답 스키마 유효성 검사
- templates/: Jinja2 템플릿
- static/: 정적 파일(css)
- tests/: 단위 및 통합 테스트
- specs/ 및 docs/: 설계·사양·체크리스트

**보안 주의**

현재 데모 구현은 교육 목적으로 간단히 처리되어 있습니다. 특히 비밀번호 저장/비교가 안전한 해시 방식으로 되어 있지 않다면 절대 운영 환경에 배포하지 마십시오. 실제 서비스로 전환 시 `werkzeug.security` 기반 해싱으로 대체해야 합니다.

**기여**

기여는 환영합니다. 작은 버그 수정이나 문서 개선부터 시작해 주세요. 기여 가이드라인은 `docs/CONTRIBUTING.md`(있다면)를 참조하십시오.

---

필요하시면 이 README에 영문 버전이나 자세한 개발 가이드를 추가해 드리겠습니다.

