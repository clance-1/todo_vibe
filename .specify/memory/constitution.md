<!--
Sync Impact Report

- Version change: unknown -> 1.0.0
- Modified principles: (new) 간결성 — 교육 데모 우선; 사용자 중심성; 테스트-퍼스트(경량); 관찰성 & 디버깅; 버전관리 및 라이선스
- Added sections: Constraints & Tech Stack; Development Workflow
- Removed sections: none
- Templates requiring updates:
	- .specify/templates/plan-template.md ✅ updated
	- .specify/templates/tasks-template.md ✅ updated
	- .specify/templates/spec-template.md ⚠ pending (checked, no change required)
- Follow-up TODOs: none
-->

# todo_total Constitution

## Core Principles

### 간결성 — 교육 데모 우선
프로젝트의 모든 결정은 '데모용 교육 효과'를 최우선으로 해야 한다. 구현은 가능한 한 간단하고 이해하기 쉬워야 하며,
불필요한 아키텍처 복잡성은 금지된다. 이유 설명과 예시 코드가 포함되어야 하며, 학습자가 빠르게 실행하고 수정해볼 수 있어야 한다.

### 사용자 중심성 (접근성 및 개인정보 최소화)
기본 사용자 흐름(할 일 추가/수정/완료/삭제)은 명확하고 직관적이어야 하며, 키보드 접근성과 화면 판독기 호환성을
우선 고려한다. 개인 정보는 최소한만 수집하며, 사용자 데이터는 로컬 스토리지 또는 명시된 저장소에만 보관된다. 이 원칙은
MUST: 데모에서 불필요한 원격 수집을 하지 않을 것.

### 테스트-퍼스트 (경량, 비협상적 가이드)
핵심 사용자 시나리오(생성·수정·완료·삭제·목록)는 자동화된 테스트로 명시되어야 한다. 데모 성격을 고려해 테스트는 경량으로
유지하되, 각 P1 사용자 스토리에 대해 최소 하나의 통합/기능 테스트를 포함하는 것은 MUST이다.

### 관찰성 & 디버깅
데모는 디버깅이 쉬워야 하며, 개발자용 로그(콘솔 또는 구조화 로그)를 제공해야 한다. 에러는 사용자에게 친숙한 메시지로 노출하고,
개발 시에는 상세 스택트레이스를 확인할 수 있어야 한다. 이 원칙은 문제 재현과 빠른 피드백에 목적이 있다.

### 버전관리 및 라이선스
프로젝트는 의미 있는 버전 태깅(semver)을 사용한다: 초기 공개는 `1.0.0`로 간주한다. 변경 유형에 따라 MAJOR/MINOR/PATCH 규칙을
적용하며, 저장소는 명확한 오픈소스 라이선스(MIT 권장)를 포함해야 한다.

## Constraints & Tech Stack
- 목표: 학생들이 로컬에서 빠르게 실행 가능한 단일 리포지토리 데모.
- 권장 스택: Python + Flask(권장) 또는 Vanilla JavaScript/TypeScript + 간단한 정적 HTML/CSS. Flask를 주 스택으로 사용하며,
  Python 버전은 3.8 이상(권장 3.11). 프레임워크 사용 시 교육적 설명과 실행·디버깅 가이드가 동반되어야 한다.
- 테스트: `pytest` 권장. 각 P1 사용자 시나리오에 대해 최소 하나의 통합/기능 테스트를 포함해야 한다.
- 데이터 보존: 로컬스토리지(프론트엔드) 또는 간단한 파일 기반 저장소/인메모리(데모용). 외부 서비스 의존은 최소화.

## Development Workflow
- 브랜치 전략: `main`은 데모용 안정 버전, 기능 개발은 `feature/*` 브랜치에서 이루어져야 한다.
- PR 요구사항: 변경은 간단한 설명, 데모 동작 스크린샷(또는 실행 방법), 관련 테스트를 포함해야 한다.
- 배포/데모 기준: P1 사용자 시나리오가 통과하는지 확인 후 데모에 사용 가능.

## Governance
- 헌법의 수정은 Pull Request로 제안되어야 하며, 최소 한 명의 메인테이너 승인과 문서화된 마이그레이션/변경 요약을 포함해야 한다.
- 버전 정책: 새 원칙 추가 또는 기존 원칙의 의미 변경은 MAJOR 버전 증가로 간주한다. 원칙의 표현(문구 수정, 오타 등)은 PATCH.
- 규정 준수 검토: 주요 릴리스 전에는 `Constitution Check`를 실행하여 핵심 원칙(특히 테스트와 개인정보 최소화)이 충족되는지 검증한다.

**Version**: 1.0.0 | **Ratified**: 2026-01-20 | **Last Amended**: 2026-01-20
