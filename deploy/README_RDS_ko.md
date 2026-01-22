# RDS 연동 배포 가이드 (한국어)

이 문서는 이 저장소를 AWS Elastic Beanstalk(이하 EB) + RDS(Postgres)로 안전하게 배포하기 위한 단계별 가이드입니다. 로컬 테스트, RDS 생성, 보안그룹, 마이그레이션, CI 통합 및 배포 검증 절차를 포함합니다.

요약
- 목표: EB에 애플리케이션을 배포하고, RDS(Postgres)를 영구 데이터 저장소로 사용하도록 설정합니다.
- 전제: AWS 계정 및 적절한 IAM 권한(AmazonRDSFullAccess, AWSElasticBeanstalkFullAccess 등)이 필요합니다.

1. 준비사항
- AWS 리전: `ap-southeast-2` (시드니) — 이 가이드는 이 리전을 기준으로 예시를 제공합니다.
- DB 엔진/버전: `postgres` (예: 17)
- RDS 인스턴스 식별자(예): `todo-db`
- 마스터 사용자: `willtek` (예시)
- 인스턴스 클래스: `db.t4g.micro` (개발용), 스토리지: 20 GiB
- EB 애플리케이션/환경 이름: 예 `my-todo-app` / `My-todo-app-env`

2. 네트워크/보안 (중요)
1) EB 환경이 사용하는 VPC와 보안그룹(SG)을 확인합니다. EB 인스턴스(또는 ELB)가 RDS에 접속할 수 있도록 RDS 보안그룹에 EB SG의 인바운드를 허용해야 합니다.

예: EB 환경의 리소스 조회
```bash
aws elasticbeanstalk describe-environment-resources --environment-name My-todo-app-env --region ap-southeast-2
```

2) RDS용 보안그룹 생성 및 EB SG 허용(예)
```bash
# VPC_ID와 EB_SG_ID는 위 명령 또는 콘솔에서 확인
aws ec2 create-security-group --group-name todo-rds-sg --description "Allow EB access to Postgres" --vpc-id $VPC_ID
aws ec2 authorize-security-group-ingress --group-id $RDS_SG_ID --protocol tcp --port 5432 --source-group $EB_SG_ID
```

3. RDS 인스턴스 생성 (예시: AWS CLI)
> 주의: 아래 커맨드는 실제 비밀번호를 평문으로 전달하므로, 자동화 파이프라인에서는 Secrets Manager/SSM Parameter Store 사용을 권장합니다.

```bash
aws rds create-db-subnet-group --db-subnet-group-name todo-subnet-group --db-subnet-group-description "subnets for todo rds" --subnet-ids $SUBNET_ID1 $SUBNET_ID2 --region ap-southeast-2

aws rds create-db-instance \
  --db-instance-identifier todo-db \
  --db-instance-class db.t4g.micro \
  --engine postgres \
  --engine-version 17 \
  --allocated-storage 20 \
  --master-username willtek \
  --master-user-password '<YOUR_DB_PASSWORD>' \
  --vpc-security-group-ids $RDS_SG_ID \
  --db-subnet-group-name todo-subnet-group \
  --backup-retention-period 7 \
  --no-publicly-accessible \
  --region ap-southeast-2

aws rds wait db-instance-available --db-instance-identifier todo-db --region ap-southeast-2

# 엔드포인트 조회
aws rds describe-db-instances --db-instance-identifier todo-db --query 'DBInstances[0].Endpoint.Address' --output text --region ap-southeast-2
```

4. EB에 환경변수 설정 (SQLALCHEMY_DATABASE_URI)
1) 연결 문자열 형식(예)
```
postgresql+psycopg://<USER>:<PASSWORD>@<RDS_ENDPOINT>:5432/<DB_NAME>
```

2) EB CLI로 설정 (로컬에서 `eb`가 설치되어 있고 EB가 초기화되어 있다고 가정)
```bash
export SQLALCHEMY_DATABASE_URI='postgresql+psycopg://willtek:YOUR_PASSWORD@todo-db.xxxxxx.ap-southeast-2.rds.amazonaws.com:5432/postgres'
eb init my-todo-app --region ap-southeast-2
eb use My-todo-app-env
eb setenv SQLALCHEMY_DATABASE_URI="$SQLALCHEMY_DATABASE_URI"
eb deploy
```

또는 앞서 추가한 `scripts/eb_setenv_from_env.sh` 스크립트를 사용하여 환경변수를 한번에 설정할 수 있습니다.

5. 마이그레이션 적용 (Alembic)
- 권장 방식: 배포 파이프라인에서 `alembic upgrade head`를 실행하여 스키마를 최신으로 적용합니다.
- 로컬에서 수동 실행 예:
```bash
export SQLALCHEMY_DATABASE_URI='postgresql+psycopg://willtek:YOUR_PASSWORD@<RDS_ENDPOINT>:5432/postgres'
alembic upgrade head
```

6. 백업 및 롤백 전략
- 배포 전 스냅샷 생성 권장:
```bash
aws rds create-db-snapshot --db-instance-identifier todo-db --db-snapshot-identifier before-deploy-$(date +%s) --region ap-southeast-2
```
- 마이그레이션 실패 시 가능한 복구:
  - 스냅샷으로 복원 또는
  - `alembic downgrade <revision>` (downgrade가 안전한 경우)

7. CI 통합 (GitHub Actions) — 핵심 포인트
- 반드시 민감 정보는 GitHub Secrets로 저장하세요(`RDS_MASTER_USERNAME`, `RDS_MASTER_PASSWORD`, `RDS_HOST`, `RDS_DB`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` 등).
- CD 워크플로에서 권장 단계:
  1. 빌드 및 이미지 푸시
  2. (선택) RDS 스냅샷 생성
  3. `alembic upgrade head` 실행(환경변수로 RDS 연결 문자열 제공)
  4. `eb setenv`로 EB에 `SQLALCHEMY_DATABASE_URI` 설정
  5. `eb deploy`

예시 워크플로 스텝(요약):
```yaml
- name: Run DB migrations
  env:
    SQLALCHEMY_DATABASE_URI: ${{ secrets.RDS_DATABASE_URL }}
  run: |
    pip install -r requirements.txt
    alembic upgrade head
```

8. 배포 후 검증(스모크 테스트)
- 애플리케이션에 새 리소스 생성 요청을 보내고(Routes 또는 API), RDS에 쿼리하여 레코드가 존재하는지 확인합니다.

예) 간단한 검증 순서
1) `curl -X POST https://<YOUR_APP>/api/todos` 로 `smoke-test` 항목 생성
2) `psql` 또는 SQLAlchemy 스크립트로 RDS에서 해당 레코드 조회

9. 운영 고려사항
- 운영 환경에서는 `master` 계정을 직접 사용하기보다 권한을 분리한 운영용 DB 계정을 사용하세요.
- 모니터링: RDS CloudWatch 지표(연결 수, CPU, IOPS)와 EB 헬스 체크를 모니터링하세요.
- 보안: 비밀번호는 Secrets Manager/Parameter Store에 보관하고 접근은 최소 권한으로 설정하세요.

첨부: 문제 해결 팁
- 테이블이 생성되지 않음: EB 환경변수(`SQLALCHEMY_DATABASE_URI`)가 올바른지 확인, `SKIP_DB_CREATE` 환경변수 확인, 앱 로그에서 예외(권한/접속) 확인
- 인스턴스에서 Postgres 컨테이너가 동작함: 소스 번들에 `docker-compose.yml`이 포함되어 EB가 Compose 배포를 수행했을 가능성 있음(리포지토리에서 Compose 파일 제거 권장).

더 도와드릴까요?
- Terraform/CloudFormation 템플릿 생성
- GitHub Actions 워크플로에 마이그레이션/스냅샷 스텝 추가(실제 커밋·PR 생성은 요청 시)
