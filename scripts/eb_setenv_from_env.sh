#!/usr/bin/env bash
set -euo pipefail

# Build SQLALCHEMY_DATABASE_URI from environment variables and set it in EB
# Expects: RDS_MASTER_USERNAME, RDS_MASTER_PASSWORD, RDS_HOST, RDS_PORT (optional), RDS_DB (optional), EB_ENV_NAME, EB_APP_NAME

: ${RDS_MASTER_USERNAME:?RDS_MASTER_USERNAME is required}
: ${RDS_MASTER_PASSWORD:?RDS_MASTER_PASSWORD is required}
: ${RDS_HOST:?RDS_HOST is required}
: ${RDS_PORT:=5432}
: ${RDS_DB:=postgres}
: ${EB_APP_NAME:?EB_APP_NAME is required}
: ${EB_ENV_NAME:?EB_ENV_NAME is required}

: ${AWS_REGION:=ap-southeast-2}

SQLALCHEMY_DATABASE_URI="postgresql+psycopg://${RDS_MASTER_USERNAME}:${RDS_MASTER_PASSWORD}@${RDS_HOST}:${RDS_PORT}/${RDS_DB}"

echo "Setting EB environment variable SQLALCHEMY_DATABASE_URI for ${EB_ENV_NAME} (app: ${EB_APP_NAME})"

eb init "${EB_APP_NAME}" --region "${AWS_REGION}" || true
eb use "${EB_ENV_NAME}" || true
eb setenv SQLALCHEMY_DATABASE_URI="$SQLALCHEMY_DATABASE_URI"

echo "Done."
