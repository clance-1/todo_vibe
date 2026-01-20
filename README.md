# todo_total - Demo Flask ToDo App

간단한 교육용 ToDo 데모(Flask)

Prerequisites

- Python 3.8+ (권장 3.11)
- 권장: 가상환경 사용

설치

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

실행

```powershell
python app.py
```

테스트

```powershell
pytest -q
```

Notes

- 이 데모는 교육/디버깅 용도로 인메모리 저장소를 사용합니다. 실제 영구 저장이 필요하면 README의 지시에 따라 파일 또는 DB로 전환하세요.
