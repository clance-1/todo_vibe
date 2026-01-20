# Feature Specification: 학생용 ToDo 데모 (Flask)

**Feature Branch**: `001-flask-todo-app`
**Created**: 2026-01-20
**Status**: Draft
**Input**: User description: "학생들 종합적 학습을 위한 난이도가 낮은 todo app: 1) 할일은 3개의 카테고리로 분류되며 고유색을 가진다 : 학습(적색), 개인(청색), 업무(녹색); 2) 날짜별로 할일 목록을 저장 할수 있다; 3) 날짜및 카테고리로 필터링 기능을 가진다.; 4) 사용자및 할일 목록등은 DB에 저장되며, 로그인한 사람의 목록 내역만 보인다.; 5) 로그인 페이지와 할일 목록 페이지는 별도로 분리된다."

## Clarifications

### Session 2026-01-20

- Q: 가입 방식 — 데모용으로 어떻게 처리할까요? → A: 자체 회원가입 허용 (간단한 아이디(username)와 비밀번호로 즉시 등록).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 기본 CRUD (Priority: P1)

사용자는 본인 계정으로 로그인한 뒤 자신의 할 일을 생성하고, 수정하고, 완료표시하고, 삭제할 수 있다. 각 항목은 제목, 카테고리(학습/개인/업무), 날짜(YYYY-MM-DD), 완료 여부를 가진다.

**Why this priority**: 핵심 학습 흐름을 구성하므로 데모의 최소 가치 제공(핵심 기능).

**Independent Test**: 자동화된 통합 테스트로 '회원가입 → 로그인 → 할일 생성 → 목록 조회 → 수정 → 삭제' 흐름을 검증.

**Acceptance Scenarios**:

1. **Given** 사용자가 로그인되어 있다, **When** 새 할일을 제목/카테고리/날짜로 생성하면, **Then** 생성된 항목이 목록에 표시된다.
2. **Given** 항목이 존재할 때, **When** 항목을 수정하거나 완료 표시하면, **Then** 변경 내용이 저장되어 목록에 반영된다.
3. **Given** 항목이 존재할 때, **When** 항목을 삭제하면, **Then** 목록에서 제거된다.

---

### User Story 2 - 필터링 및 색상 표시 (Priority: P1)

사용자는 날짜와 카테고리로 목록을 필터링할 수 있다. 각 카테고리는 고유색(학습=적색, 개인=청색, 업무=녹색)으로 시각적으로 구분된다.

**Why this priority**: 학습용 시각적 구분과 날짜별 계획 확인이 교육 목적상 필수적이다.

**Independent Test**: 특정 날짜/카테고리로 생성된 항목들이 필터에 따라 정확히 반환되는지 자동화 테스트로 확인.

**Acceptance Scenarios**:

1. **Given** 여러 날짜/카테고리의 항목이 존재할 때, **When** 날짜 필터를 적용하면, **Then** 해당 날짜의 항목만 반환된다.
2. **Given** 여러 항목이 존재할 때, **When** 카테고리 필터를 적용하면, **Then** 해당 카테고리의 항목만 반환된다.

---

### User Story 3 - 사용자 계정 분리 및 페이지 분리 (Priority: P2)

사용자는 계정을 생성하고 로그인해야 하며, 로그인된 사용자만 자신의 할일 목록을 볼 수 있다. 로그인 화면과 할일 목록 화면은 별도 페이지로 분리된다.

**Why this priority**: 개인별 데이터 격리와 데모 흐름 안내를 위해 필요하다.

**Independent Test**: 회원가입/로그인 흐름을 자동화 테스트로 검증하고, 비로그인 상태에서 `todos` 페이지 접근이 차단되는지 확인.

**Acceptance Scenarios**:

1. **Given** 사용자가 등록되어 있을 때, **When** 올바른 자격증명으로 로그인하면, **Then** 할일 목록 페이지로 이동하고 본인 데이터만 보여진다.
2. **Given** 비로그인 상태에서 할일 페이지에 접근하면, **When** 시도하면, **Then** 로그인 페이지로 리다이렉트된다.

---

### Edge Cases

- 동일 날짜/동일 카테고리로 중복된 제목을 가진 항목을 생성하려는 경우: 허용하되 UI에서 명확히 표시.
- DB 연결 실패: 사용자 친화적 에러 메시지와 재시도 권장.
- 잘못된 날짜 포맷 입력: 입력 검증(YYYY-MM-DD) 및 오류 반환.
- 비인가 접근(다른 사용자의 항목 수정/삭제) 시 403/404 처리.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 시스템은 사용자가 자체적으로 계정을 생성하고 로그인할 수 있어야 한다 (self-registration 허용, username/password 기반; 최소 입력: 아이디와 비밀번호).
- **FR-002**: 로그인한 사용자는 자신의 할일을 생성(Create)할 수 있어야 한다. 항목 속성: `title`, `category`, `date`(YYYY-MM-DD), `completed`.
- **FR-003**: 사용자는 자신의 할일을 수정(Update) 및 삭제(Delete)할 수 있어야 한다.
- **FR-004**: 시스템은 사용자별 데이터 분리를 보장해야 하며, 로그인한 사용자만 자신의 목록을 조회(Read)할 수 있다.
- **FR-005**: 시스템은 날짜 및 카테고리로 필터링 기능을 제공해야 한다 (쿼리 파라미터 또는 UI 필터).
- **FR-006**: 카테고리는 세 가지로 제한되어야 한다: `study`, `personal`, `work` (각각 색상 매핑 필요).
- **FR-007**: 모든 주요 사용자 흐름(P1)은 자동화된 테스트로 검증되어야 한다.

### Key Entities *(include if feature involves data)*

- **User**: id, username, password_hash
- **Todo**: id, user_id, title, category (study|personal|work), date (YYYY-MM-DD), completed, created_at

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: P1 사용자 시나리오(등록→로그인→할일 생성→조회→수정→삭제)를 포함한 자동화 통합 테스트가 100% 통과해야 한다.
- **SC-002**: 날짜 또는 카테고리 필터 쿼리로 요청 시, 테스트 데이터 세트에서 기대되는 항목만 반환되어야 하며(정확도 100%), 관련 테스트가 포함되어야 한다.
- **SC-003**: 로그인한 사용자는 다른 사용자의 항목을 조회/수정/삭제할 수 없어야 하며(보안 제어), 관련 액세스 제어 테스트가 포함되어야 한다.
- **SC-004**: UI에서 각 카테고리는 지정된 색상으로 표시되어야 한다(학습=적색, 개인=청색, 업무=녹색) — 수동 데모 검사 또는 스냅샷 테스트로 확인.

## Assumptions

- 인증은 간단한 username/password로 처리하고, 세션 기반 로그인(예: Flask-Login)을 사용한다.
- 초기 저장소는 로컬 SQLite로 가정한다(배포 시 다른 DB로 변경 가능).
- 날짜 형식은 `YYYY-MM-DD`로 통일한다.
 - 등록 방식: 데모 목적상 `self-registration`(사용자 직접 가입)을 허용한다(아이디+비밀번호). 배포 시 설정으로 변경 가능.

## Implementation Notes (non-mandatory)

- 프론트엔드는 간단한 템플릿과 최소한의 JS로 구성한다(로그인 페이지, 할일 페이지 분리).
- 색상 매핑은 CSS 클래스(`cat-study`, `cat-personal`, `cat-work`)로 관리한다.
- 테스트는 `pytest`와 Flask 테스트 클라이언트를 사용한다.

---

**문서 작성자**: 자동 생성 (요청자 기준)
**검토 요청**: 주요 이해관계자(교육자)에게 배포 후 피드백 반영
# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]  
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
