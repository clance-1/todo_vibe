"""애플리케이션 설정을 출력하는 유틸리티 스크립트.

`app.config`의 주요 설정값(예: `SQLALCHEMY_DATABASE_URI`)과 `instance_path`
등을 빠르게 확인할 때 사용합니다.
"""

import sys
from pathlib import Path
# ensure project root is on sys.path when running this script
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app
print('SQLALCHEMY_DATABASE_URI=', app.config['SQLALCHEMY_DATABASE_URI'])
print('instance_path=', app.instance_path)
