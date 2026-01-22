RDS / CD 연결 안내

이 문서는 GitHub Actions를 사용해 애플리케이션을 빌드하고 RDS에 대해 마이그레이션한 뒤 Elastic Beanstalk에 배포하는 과정에서 필요한 설정과 시크릿을 정리합니다.

필수 GitHub Secrets
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` : AWS 권한을 가진 자격증명 (RDS/EB 조작 권한 포함)
- `DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN` : Docker Hub에 이미지 푸시용
- `RDS_MASTER_USERNAME` : 예: willtek
- `RDS_MASTER_PASSWORD` : 예: willtek1234!! (절대 리포지토리에 직접 저장하지 마세요)
- `RDS_HOST` : RDS 엔드포인트(예: todo-db.xxxx.ap-southeast-2.rds.amazonaws.com)
- `RDS_PORT` : 보통 `5432`
- `RDS_DB` : 데이터베이스 이름(없으면 `postgres` 사용)
- `RDS_INSTANCE_IDENTIFIER` : 예: `todo-db` (스냅샷 등에서 사용)
- `EB_APP_NAME` : Elastic Beanstalk 애플리케이션 이름
- `EB_ENV_NAME` : Elastic Beanstalk 환경 이름
- (선택) `RDS_CREATE_SNAPSHOT` : `true`로 설정하면 배포 전에 스냅샷을 생성합니다

간단한 흐름
1. GitHub Actions(`.github/workflows/aws-deploy-with-rds.yml`)가 트리거됩니다.
2. Docker 이미지를 빌드해 Docker Hub로 푸시합니다.
3. (선택) RDS 스냅샷을 생성합니다.
4. 리포지토리의 Alembic 마이그레이션을 실행해 스키마를 업그레이드합니다.
5. EB 환경변수 `SQLALCHEMY_DATABASE_URI`를 RDS 연결 문자열로 설정하고 `eb deploy`를 실행합니다.

주의사항
- Secrets에 저장된 비밀번호는 안전하게 관리하세요 (GitHub Secrets 권장).
- RDS의 보안그룹이 EB 인스턴스(또는 ELB)의 보안그룹에서의 인바운드를 허용하도록 설정되어야 합니다.
- 마이그레이션 전 백업(스냅샷)을 권장합니다.

추가 요청
- 원하시면 이 레포에 Terraform 템플릿을 추가해 RDS를 자동으로 생성하도록 도와드릴 수 있습니다.
