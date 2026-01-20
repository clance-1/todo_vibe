import sys
from pathlib import Path
# ensure project root is on sys.path when running this script
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app
print('SQLALCHEMY_DATABASE_URI=', app.config['SQLALCHEMY_DATABASE_URI'])
print('instance_path=', app.instance_path)
