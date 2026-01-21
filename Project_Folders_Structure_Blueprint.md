# Project Folders Structure Blueprint

마지막 업데이트: 2026-01-21

## 목적
이 문서는 저장소의 폴더 구조를 해석하고, 일관된 코드 조직을 유지하기 위한 권장 구조, 명명 규칙, 파일 배치 패턴 및 개발자 내비게이션 지침을 제공합니다. 자동 감지 결과에 따라 Flask 기반 Python 애플리케이션(데모) 구조에 초점을 맞춰 설명합니다.

---

**1. 자동 감지 요약**

- 감지된 프로젝트 유형: Python (Flask 웹 애플리케이션)
  - 근거: `app.py`, `app_schemas.py`, `requirements.txt`, `templates/`, `static/` 존재
- 데이터베이스 / 인프라: Alembic 마이그레이션(`alembic/`) 및 `docker-compose.yml` 존재 → 로컬 Postgres 시나리오 지원
- 모노레포 여부: 아니오(단일 애플리케이션 저장소)
- 마이크로서비스 여부: 아니오(단일 서비스 앱)
- 생성된 항목(제외 대상): `__pycache__` 등 파생/빌드 아티팩트가 존재함(분석에서는 제외 권장)

**스캔 통계(워크스페이스 스캔 결과)**
- 총 항목(검색 결과 기준): 68개 항목 감지(근사)
- 주요 디렉터리별 대략 파일 수(근사):
  - `templates/`: 4
  - `static/`: 1
  - `tests/`: 2 (+`__pycache__` 항목들)
  - `specs/`: 8+ 문서
  - `alembic/`: 2 (env.py + versions/0001_initial.py)
  - `scripts/`: 4
  - 루트 파일(예): `app.py`, `app_schemas.py`, `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `README.md`

---

**2. 구조 개요**

- 아키텍처 접근: 레이어·기능 혼합형(작은 규모 앱에 적합)
  - 엔트리 포인트: `app.py` (Flask 앱 + 라우트 정의)
  - 데이터 모델 / 스키마: `app_schemas.py` (Pydantic 기반 요청/응답 검증)
  - 템플릿 뷰: `templates/` (Jinja2)
  - 정적 자원: `static/`
  - 마이그레이션: `alembic/`
  - 개발/운영 스크립트: `scripts/`
  - 사양·문서: `specs/`, `docs/`

- 조직 원칙(관찰된 것)
  - 클린하고 작은 코드베이스는 기능별 파일을 루트에 두고 관련 서브폴더(템플릿, static, scripts)로 분리
  - 테스트는 `tests/` 에 집중 배치
  - 인프라·환경 설정 파일(Dockerfile, docker-compose.yml, alembic.ini)은 루트에 위치

---

**3. 디렉터리 시각화 (Markdown 목록, 깊이 3)**

- /
  - `app.py` — 애플리케이션 진입점, 라우트 및 API 엔드포인트
  - `app_schemas.py` — Pydantic 모델(유효성 검사)
  - `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `alembic.ini`, `README.md`
  - `templates/`
    - `base.html`
    - `login.html`
    - `register.html`
    - `todos.html`
  - `static/`
    - `style.css`
  - `tests/`
    - `test_app.py`
    - `test_api_full.py`
  - `specs/`
    - `001-flask-todo-app/` (plan.md, quickstart.md, spec.md 등)
  - `alembic/`
    - `env.py`
    - `versions/0001_initial.py`
  - `scripts/`
    - `add_user.py`, `debug_api.py`, `list_users.py`, `print_config.py`
  - `.github/`, `.specify/` (CI/agents 및 템플릿 등)
  - `instance/` (런타임 DB: `todo.db`) — 런타임 아티팩트

> 제외 권장: `__pycache__/`, 가상환경 디렉터리 등 자동 생성 폴더는 저장소 내부에 보관하지 않는 것이 좋습니다.

---

**4. 주요 디렉터리 분석**

- `app.py`
  - 역할: Flask 앱 구성, 라우트(웹/REST API) 정의, DB 초기화
  - 특징: 데모용 단일 파일 아키텍처; 소규모 앱에서 빠른 이해 및 수정에 유리
  - 권장: 비즈니스 로직이 늘어나면 블루프린트 또는 패키지(예: `app/` 서브패키지)로 분리

- `app_schemas.py`
  - 역할: `TodoCreate`, `TodoUpdate` 같은 Pydantic 모델로 유효성 검사
  - 권장: 스키마가 늘어나면 `schemas/` 폴더로 분리

- `templates/` & `static/`
  - 역할: 프런트엔드 템플릿 및 스타일; `base.html` 상속 패턴 사용
  - 권장: 자바스크립트/이미지가 추가되면 `static/js/`, `static/img/` 등으로 세분화

- `tests/`
  - 역할: 단위·통합 테스트 보관
  - 관찰: `tests/test_api_full.py`는 API 통합 시나리오, `tests/test_app.py`는 기본 앱 동작 테스트
  - 권장: 테스트는 기능별(또는 모듈별)로 하위 폴더로 확장

- `alembic/`
  - 역할: DB 마이그레이션 관리
  - 관찰: 초기 마이그레이션 포함
  - 권장: 마이그레이션 적용 전 `alembic.ini` 및 환경변수 사용 방법 문서화

- `specs/`, `docs/`
  - 역할: 설계·요구·체크리스트 문서
  - 권장: specs에 투명한 참조(예: T-번호)를 남겨 작업 추적성을 유지

---

**5. 파일 배치 패턴**

- 라우트·엔드포인트: 현재 `app.py`에 집중. 규모가 커지면 `routes/` 또는 Blueprint 기반의 패키지로 분리
- 데이터 모델과 DB 관련: 현재 SQLAlchemy 모델이 `app.py`에 포함되어 있음 → 권장: `models.py` 또는 `models/`로 이동
- 스키마/유효성: `app_schemas.py` → `schemas/`로 확장
- 스크립트: `scripts/`에 도구 스크립트 배치(예: 사용자 추가, 디버그 헬퍼)
- 설정: 민감 정보는 `.env` 또는 환경변수로 분리. `docker-compose.yml`과 `Dockerfile`은 인프라 정의용으로 루트 유지

---

**6. 명명 및 조직 규칙 권장사항**

- 파일명: 소문자와 밑줄(`snake_case`) 사용(`app_schemas.py`, `test_api_full.py` 등)
- 디렉터리: 기능별 그룹화(예: `models/`, `schemas/`, `routes/`, `services/`)
- 테스트: `tests/{module}_test.py` 또는 `tests/test_{module}.py` 패턴 일관성 유지
- 템플릿: `templates/{blueprint}/{view}.html`로 블루프린트 분리 권장(큰 앱일 경우)

---

**7. 개발자 내비게이션 및 워크플로우**

- 시작하기(로컬 SQLite 빠른 실행):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

- Docker로 실행(로컬 Postgres):

```bash
docker-compose up --build -d
```

- 테스트 실행:

```bash
python -m pytest
```

- 권장 개발 순서:
  1. 새로운 DB 변경 → `alembic revision --autogenerate -m "msg"` → `alembic upgrade head`
  2. 기능 개발 → 테스트 추가
  3. CI: `.github/workflows/ci.yml`에서 pytest 실행 확인

---

**8. 빌드 및 출력 구조**

- 빌드 산출물: 현재 Python 프로젝트로 별도 빌드 단계 없음. Docker 이미지가 빌드 산출물 역할
- 런타임 아티팩트: `instance/todo.db` (SQLite) — `.gitignore`에 포함 권장
- 마이그레이션: `alembic/versions/`에 커밋된 마이그레이션 스크립트

---

**9. 기술별 조직 팁 (Python / Flask)**

- 소규모 → 단일 `app.py` 방식 허용
- 중간 이상 규모 → 패키지 구조 권장 예시:
  - `app/__init__.py` (팩토리 패턴)
  - `app/models.py` 또는 `app/models/`
  - `app/routes/` 또는 `app/blueprints/`
  - `app/schemas/`
  - `tests/` (동일 구조 반영)
- 환경 설정: `config.py` 또는 `instance/config.py` 사용 권장
- 비밀번호: 반드시 해시로 전환(예: `werkzeug.security.generate_password_hash`)

---

**10. 확장성 및 진화 전략**

- 기능 확장시 권장 단계:
  1. 로직을 기존 `app.py`에서 모듈로 추출
  2. Blueprint로 라우트 분리
  3. 서비스/비즈니스 로직을 `services/`로 이동
  4. DB 모델을 `models/`로 정리
- 마이크로서비스로 분리 필요시:
  - 서비스 경계(예: 인증, 할일, 알림)를 먼저 문서화
  - 각 서비스는 별도 리포지토리 또는 `services/` 하위 폴더(모노레포 선택 시)로 이동

---

**11. 구조 유지·강제화(사용자 정의 템플릿 및 검사)**

- 권장 도구:
  - CI에서 `pytest` 실행 및 `flake8`/`ruff` 같은 린터 적용
  - PR 템플릿과 코드소유자 규칙으로 구조 변경 검토 강제
- 템플릿(예시): `.specify/templates/`에 이미 템플릿이 존재하므로 이를 확장해 새 파일/디렉터리 생성 가이드 제공

---

**유지 보수**

- 이 문서는 코드 구조 변경 시 업데이트해야 합니다. 마지막 업데이트: 2026-01-21
- 권장: 주요 구조 변경(폴더 재배치, 블루프린트 추가 등) 시 이 문서에 변경 이유와 영향 범위를 기록하십시오.

---

부가 요청: 원하시면
- ASCII 트리 또는 테이블 형태의 시각화로 변환
- 영문 버전 생성
- CI에 구조 검사(간단한 스크립트) 추가

원하시는 추가 작업을 알려주세요.

---

## 부록: ASCII 트리 (깊이 3)

```
todo_total/
├─ app.py
├─ app_schemas.py
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
├─ alembic.ini
├─ README.md
├─ Project_Folders_Structure_Blueprint.md
├─ templates/
│  ├─ base.html
│  ├─ login.html
│  ├─ register.html
│  └─ todos.html
├─ static/
│  └─ style.css
├─ tests/
│  ├─ test_app.py
│  └─ test_api_full.py
├─ specs/
│  └─ 001-flask-todo-app/
│     ├─ plan.md
│     ├─ quickstart.md
│     └─ spec.md
├─ alembic/
│  ├─ env.py
│  └─ versions/
│     └─ 0001_initial.py
├─ scripts/
│  ├─ add_user.py
│  ├─ debug_api.py
│  ├─ list_users.py
│  └─ print_config.py
├─ .github/
└─ .specify/
```

## 부록: 테이블 뷰 (경로 / 목적 / 콘텐츠 유형 / 규칙)

| 경로 | 목적 | 콘텐츠 유형 | 규칙 / 권장사항 |
|---|---|---:|---|
| / | 애플리케이션 진입점, 설정 | `app.py`, `Dockerfile`, `requirements.txt`, `docker-compose.yml`, `alembic.ini` | 핵심 실행 파일을 루트에 두고, 민감한 설정은 환경변수로 관리 |
| templates/ | 서버 렌더링 뷰(템플릿) | `.html` (Jinja2) | `base.html` 상속 패턴 사용, 큰 앱은 템플릿 하위폴더로 분리 |
| static/ | 정적 자원 (CSS, JS, 이미지) | `style.css`, (추가: `js/`, `img/`) | 정적 파일은 `static/` 하위에 정리, 캐시 전략 문서화 |
| tests/ | 단위 및 통합 테스트 | `test_*.py` | 테스트는 기능별로 그룹화, CI에서 자동 실행 |
| specs/ 및 docs/ | 설계·사양·체크리스트 | 마크다운 문서 | 사양 변경 시 참조 및 T-번호 기록 유지 |
| alembic/ | DB 마이그레이션 | `env.py`, `versions/*.py` | 마이그레이션은 커밋, 배포 전 `alembic upgrade head` 적용 |
| scripts/ | 개발/운영 보조 스크립트 | `.py` 스크립트 | 반복적 작업은 스크립트화, 설명서 포함 |
| instance/ | 런타임 아티팩트(로컬 DB) | `todo.db` | `.gitignore`에 추가 권장 (로컬 전용)
| .github/ | CI / 워크플로우 / 에이전트 템플릿 | 워크플로우, prompts | CI는 테스트·린트 실행을 포함하도록 구성 |
| .specify/ | 프로젝트 템플릿 및 에이전트 컨텍스트 | 템플릿, 스크립트 | 템플릿을 기준으로 파일 생성 규약 적용 |

---

파일 시각화가 추가되었습니다. 필요하면 깊이 수준을 변경하거나 파일 수 통계를 더 상세히 포함해 드리겠습니다.
