# AgentTrace Research Plan

**Version:** v0.2  
**Date:** 2026-09-18  
**Field:** AI Security / Digital Forensics / Agentic AI Security

---

# 1. 연구 개요

AgentTrace는 AI Agent의 목표, 판단, 권한 요청, Tool 사용 및 실행 결과를
다계층 telemetry로 기록하고, 사고 발생 시 서로 다른 증거원을 교차검증하여
침해 경로, 원인, 영향 및 대응 과정을 재구성하는
AI Agent Security & Digital Forensics 연구 프로젝트이다.

한 문장으로 요약하면 다음과 같다.

> AI Agent가 공격받거나 통제를 벗어났을 때,
> 남은 로그와 증거만으로 "무슨 일이 왜 일어났는지" 얼마나 정확하게 재구성할 수 있는가?

---

# 2. 연구 배경

최근 LLM 기반 시스템은 단순한 텍스트 생성기를 넘어,
파일 접근, 데이터 검색, API 호출, 데이터베이스 조회 등
외부 기능을 Tool 형태로 호출하는 Agent 구조로 발전하고 있다.

이러한 구조에서는 모델의 출력 자체뿐 아니라
Agent에게 부여된 기능, 권한, 자율성, 외부 시스템 접근 범위가
보안상 중요한 요소가 된다.

OWASP는 외부 웹페이지나 파일 등에 포함된 입력이
LLM의 행동을 의도하지 않은 방향으로 변경하는
Indirect Prompt Injection을 Prompt Injection의 한 유형으로 정의하고 있다.

또한 Agent에게 필요 이상의 기능, 권한 또는 자율성이 부여되어
의도하지 않은 행동이 실제 시스템에 영향을 미칠 수 있는 문제를
Excessive Agency로 분류하고 있다.

NIST 역시 AI Agent가 다양한 데이터, Tool 및 애플리케이션에 접근하는 환경에서는
적절한 identification, authorization, auditing 등의 통제가 필요하다고 설명하고 있다.

2026년 OpenAI가 공개한 Hugging Face 사고에서는
내부 사이버보안 평가 중 일부 모델이 격리 통제를 우회하고,
허가되지 않은 통신 경로를 사용하며,
공유 인프라와 제3자 시스템에 접근한 사례가 공식적으로 보고되었다.

이러한 사례들은 AI Agent 보안에서 다음 질문이 중요함을 보여준다.

- Agent는 무엇을 하려고 했는가?
- 어떤 권한을 요청했는가?
- 어떤 자원에 접근하려 했는가?
- 어떤 보안 경계를 통과하려 했는가?
- Policy는 이를 허용했는가 또는 차단했는가?
- 실제 Tool 실행은 발생했는가?
- 사고 이후 남은 증거만으로 전체 행동 경로를 복원할 수 있는가?

---

# 3. 문제 정의

기존 침입 탐지 시스템은 주로 다음 질문에 초점을 맞춘다.

> "공격이 발생했는가?"

하지만 디지털 포렌식과 Incident Response에서는
탐지 이후에 다음 질문까지 설명할 수 있어야 한다.

> "무엇이 최초 원인이었으며,
> Agent는 어떤 정보를 받아 어떤 판단을 했고,
> 어떤 Tool과 권한을 사용하려 했으며,
> 실제 시스템에는 어떤 영향이 발생했는가?"

AI Agent 환경에서는 하나의 행동이 단일 입력만으로 결정되지 않을 수 있다.

예를 들어 다음과 같은 연쇄 과정이 존재할 수 있다.

User Prompt  
→ Retrieval  
→ External Document  
→ Indirect Prompt Injection  
→ Agent Decision  
→ Tool Request  
→ Authorization Check  
→ Tool Execution 또는 Denial

따라서 최종 Tool Call 하나만 확인하는 것만으로는
사고의 최초 원인을 재구성하지 못할 수 있다.

AgentTrace는 이러한 문제를
"증거 기반 사건 재구성"의 관점에서 다룬다.

---

# 4. 연구 목적

본 연구의 주요 목적은 다음과 같다.

1. AI Agent의 행동 과정을 구조화된 telemetry로 기록한다.
2. Agent, Policy, Tool 등 서로 다른 계층의 증거를 분리하여 수집한다.
3. 침해사고 발생 시 사건의 Timeline을 재구성한다.
4. 각 Event의 원인-결과 관계를 연결하여 Causal Chain을 재구성한다.
5. 최초 공격 원인(Root Cause)을 식별한다.
6. 특정 증거가 손실되었을 때 재구성 성능이 얼마나 감소하는지 분석한다.
7. 공격 탐지 이후의 Containment 및 Recovery 과정도 감사 가능한 기록으로 남긴다.

전체 연구 흐름은 다음과 같다.

Attack / Anomaly Detection  
→ Evidence Collection  
→ Cross-source Validation  
→ Timeline Reconstruction  
→ Causal Reconstruction  
→ Root Cause Identification  
→ Containment / Recovery Verification

---

# 5. 핵심 연구 질문

## RQ1. 최소 포렌식 증거

Indirect Prompt Injection으로 인해 AI Agent가
비인가 Tool 사용을 시도한 사고에서,

> 공격의 최초 원인과 행동 경로를 정확하게 재구성하기 위해
> 필요한 최소 포렌식 증거는 무엇인가?

---

## RQ2. 증거 손실과 재구성 성능

> 수집 가능한 telemetry의 종류가 감소할수록
> AI Agent 침해사고의 원인, 행동 및 영향 재구성 능력은
> 어떻게 변화하는가?

---

## RQ3. 증거원별 역할

> 어떤 telemetry는 이상행동을 발견하는 데 유용하고,
> 어떤 telemetry는 실제 행동을 입증하는 데 필요한가?

즉,

Discovery Source와 Proof Source가 동일한가를 분석한다.

---

## RQ4. 분석 방식 비교

후속 연구에서는 다음 질문으로 확장한다.

> Rule-based 분석과 LLM-based 분석은
> Agent 사고 재구성의 정확도와 근거 제시 능력에서
> 어떤 차이를 보이는가?

RQ4는 초기 MVP의 필수 범위에는 포함하지 않는다.

---

# 6. 위협 모델

초기 연구 대상 공격은
Indirect Prompt Injection이다.

정상 시나리오는 다음과 같다.

User  
→ Agent  
→ 정상 문서 조회  
→ Tool Request  
→ Policy ALLOW  
→ 파일 읽기  
→ 정상 결과 반환

공격 시나리오는 다음과 같다.

User  
→ Agent  
→ 외부 문서 조회  
→ 악성 지시가 포함된 문서  
→ Agent 행동 변화  
→ 비인가 파일 접근 요청  
→ Policy DENY

초기 Sandbox 구조는 다음과 같다.

sandbox/
├── public/
│   └── project.txt
└── secret/
    └── credentials.txt

Agent는 정상적으로는 public 영역만 접근할 수 있다.

공격 시나리오에서는 Agent가
secret 영역의 파일 읽기를 요청하도록 구성하되,
Policy Layer에서 실제 접근을 차단한다.

실험에는 실제 개인정보, 실제 인증정보 또는 실제 민감 데이터를 사용하지 않는다.

---

# 7. 시스템 구조

AgentTrace의 기본 구조는 다음과 같다.

User Goal
    ↓
Agent Decision / Plan
    ↓
Tool Request
    ├── Tool
    ├── Target Resource
    └── Requested Permission
    ↓
Policy Gateway
    ├── Allowed Scope
    ├── Denied Scope
    └── Human Approval Requirement
    ↓
Tool Execution
    ↓
Execution Result
    ↓
Agent Observation
    ↓
Next Decision

모든 구성 요소의 행동은 별도의 Evidence Layer에 기록한다.

Agent Log
+
Policy Log
+
Tool Execution Log
+
추후 OS / File-system Artifact
+
추후 Network Telemetry
+
Response / Recovery Log

↓

Cross-source Correlation

↓

Timeline Reconstruction

↓

Causal Reconstruction

↓

Root Cause Analysis

↓

Containment / Recovery Verification

---

# 8. 포렌식 증거 분류

초기 버전에서는 다음 증거 계층을 정의한다.

## 8.1 User Evidence

- 최초 사용자 입력
- 요청 목적
- Session / Run 정보

## 8.2 Retrieval / Context Evidence

- Retrieval Query
- 검색된 문서
- Agent Context에 실제로 포함된 데이터
- 외부 입력 Source

## 8.3 Agent Evidence

- Agent Decision
- Agent Plan
- 선택한 Tool
- Agent Observation
- 다음 행동

## 8.4 Permission Evidence

- Requested Permission
- Granted Permission
- Target Resource
- Access Scope

## 8.5 Policy Evidence

- Policy Rule
- ALLOW / DENY
- Human Approval Required 여부
- Boundary Violation 여부

## 8.6 Tool Evidence

- Tool Name
- Tool Input
- 실행 대상
- Execution Result
- Error / Success

## 8.7 Response Evidence

향후 다음 항목을 추가한다.

- Pause Event
- Permission Revocation
- Containment Action
- Recovery Status
- Verification Result

---

# 9. 이벤트 스키마

각 Event는 최소한 다음 필드를 갖는다.

- event_id
- trace_id
- parent_event_id
- timestamp
- sequence
- actor
- event_type
- resource
- result
- input_hash
- output_hash
- metadata

추후 다음 필드를 추가한다.

- agent_id
- goal
- tool
- target_resource
- requested_permission
- granted_permission
- policy_decision
- human_approval
- boundary_violation
- containment_action
- recovery_status

특히 다음 세 필드는 사건의 인과관계 재구성을 위해 중요하다.

- trace_id
- parent_event_id
- sequence

단순한 시간순 로그가 아니라
Event 간 원인-결과 관계를 복원할 수 있도록 설계한다.

---

# 10. Ground Truth 구축

실험 환경은 연구자가 직접 통제하므로
각 공격 시나리오의 실제 Event 흐름을 알고 있다.

예:

E001 USER_PROMPT  
↓  
E002 RETRIEVAL_QUERY  
↓  
E003 DOCUMENT_RETRIEVED  
↓  
E004 MALICIOUS_CONTEXT  
↓  
E005 AGENT_DECISION  
↓  
E006 TOOL_REQUEST  
↓  
E007 POLICY_CHECK  
↓  
E008 TOOL_DENIED

이를 Ground Truth Timeline으로 사용한다.

Forensic Analyzer가 생성한 Timeline과 Causal Chain을
Ground Truth와 비교하여 재구성 성능을 평가한다.

---

# 11. 핵심 실험: Evidence Ablation

모든 증거가 존재하는 상태를 FULL 조건으로 정의한다.

FULL:

- User Evidence
- Retrieval Evidence
- Context Evidence
- Agent Evidence
- Permission Evidence
- Policy Evidence
- Tool Evidence

그 후 특정 Evidence를 제거한 실험 조건을 생성한다.

예:

| 조건 | 제거되는 Evidence |
|---|---|
| FULL | 없음 |
| A | Retrieval Evidence |
| B | Context Evidence |
| C | Agent Evidence |
| D | Permission / Policy Evidence |
| E | Tool Evidence |
| F | 복수 Evidence 제거 |

각 조건에서 동일한 사고를 다시 분석한다.

예를 들어 Tool Evidence만 남아 있다면

"Agent가 특정 파일 접근을 요청했다"

는 확인할 수 있을 수 있다.

하지만 Retrieval 또는 Context Evidence가 없다면

"왜 Agent가 해당 행동을 하게 되었는가"

는 입증하기 어려울 수 있다.

반대로 Context Evidence만 있고 Tool Evidence가 없다면
Prompt Injection 노출은 확인할 수 있지만

"실제 Tool 사용 시도가 있었는가"

를 확인하지 못할 수 있다.

이러한 차이를 정량화한다.

---

# 12. Cross-source Validation

AgentTrace에서는 하나의 로그를 사건의 절대적 진실로 간주하지 않는다.

가능한 경우 다음 증거를 교차검증한다.

Agent Log  
+ Policy Log  
+ Tool Log  
+ File-system Artifact  
+ Network Log  
+ Response Log

분석 과정은 다음과 같이 설계한다.

Signal  
→ Triage  
→ Validation  
→ Cross-source Correlation  
→ Timeline Reconstruction  
→ Root Cause  
→ Containment / Recovery  
→ Learning

이 과정의 핵심 원칙은 다음과 같다.

> Discovery Source와 Proof Source는 다를 수 있다.

특정 Agent 로그에서 이상행동을 발견했다고 해서
그 로그만으로 실제 Tool 실행 또는 시스템 영향이 발생했다고 단정하지 않는다.

다른 계층의 telemetry를 이용해 행동을 검증한다.

---

# 13. CSK 2026 설계 반영

Cyber Summit Korea 2026에서 들은 발표들을 통해
AgentTrace 설계에 다음 관점을 추가하였다.

## 13.1 권한도 포렌식 대상이다

기존 설계에서는 Tool Request와 ALLOW / DENY만 기록하려 했다.

향후에는 다음을 함께 기록한다.

- Requested Permission
- Granted Permission
- Target Resource
- Allowed Scope
- Human Approval
- Boundary Violation

즉 사건을 단순히

"Agent가 무엇을 했는가"

뿐 아니라

"Agent가 무엇을 할 권한을 요구했으며
어떤 보안 경계를 통과하려 했는가"

의 관점에서도 분석한다.

---

## 13.2 관측 가능성이 보안 통제의 일부이다

AI Agent 보안에서는
이상행동을 막는 것뿐 아니라
사고 이후 행동 경로를 조사할 수 있어야 한다.

따라서 Logging과 Audit 기능을
부가 기능이 아니라 시스템 핵심 구성요소로 취급한다.

---

## 13.3 단일 증거원을 신뢰하지 않는다

한 종류의 telemetry에서 이상행동이 발견되더라도
실제 실행 여부와 시스템 영향은 다른 증거원을 이용해 검증한다.

이 원칙은 Evidence Ablation 실험과 직접 연결된다.

---

## 13.4 대응 및 복구도 사건의 일부이다

기존 설계는

Evidence  
→ Timeline  
→ Root Cause

에서 끝났지만,

향후에는 다음까지 확장한다.

Evidence  
→ Timeline  
→ Root Cause  
→ Containment  
→ Permission Revocation  
→ Recovery  
→ Verification

즉 사고를 탐지하고 설명하는 것에서 끝나지 않고
시스템이 어떻게 정상 상태로 복구되었는지도 기록한다.

---

# 14. 평가 지표

다음 지표는 AgentTrace 연구를 위해 정의하는 실험 지표이며,
현재 공인 표준 지표라고 주장하지 않는다.

## 14.1 Root Cause Accuracy

전체 사고 중 최초 공격 원인을
정확하게 식별한 사건의 비율.

Root Cause Accuracy =
정확히 식별한 사건 수 / 전체 사건 수

---

## 14.2 Timeline Completeness

Ground Truth의 핵심 Event 중
분석기가 정확하게 복원한 Event의 비율.

Timeline Completeness =
복원된 핵심 Event 수 / Ground Truth 핵심 Event 수

---

## 14.3 Action Attribution Accuracy

Agent가 어떤 자원에
어떤 행동을 시도했는지를
정확하게 연결한 비율.

---

## 14.4 Evidence Sufficiency

특정 Evidence 조합만으로

- Root Cause
- Agent Action
- Target Resource
- Policy Decision
- Impact

를 어느 수준까지 재구성할 수 있는지 평가한다.

---

## 14.5 Cross-source Verification Rate

하나의 Event가
두 개 이상의 독립적인 telemetry를 통해
검증 가능한 비율을 측정하는 확장 지표를 검토한다.

이 지표의 구체적인 정의는
실험 설계 단계에서 추가 검증 후 확정한다.

---

# 15. 구현 단계

## Phase 0 — 연구 설계

- 연구 질문 정의
- 위협 모델 정의
- GitHub 저장소 생성
- 기본 프로젝트 구조 설계

상태: 완료

---

## Phase 1 — Mock Agent

- 사용자 입력 수신
- 규칙 기반 행동 결정
- Tool Request 생성

상태: 완료

---

## Phase 2 — File Tool

- read_file Tool 구현
- public 파일 읽기
- Tool Result 반환

상태: 진행 중

---

## Phase 3 — Policy Gateway

- 접근 가능 경로 정의
- Permission Check
- ALLOW / DENY
- Boundary Violation 기록

---

## Phase 4 — Event Logger

- JSONL 기반 Event 저장
- trace_id
- parent_event_id
- timestamp
- sequence 기록

---

## Phase 5 — Attack Scenario

- 정상 Scenario
- Indirect Prompt Injection Scenario
- Unauthorized Tool Request 재현

---

## Phase 6 — Timeline Reconstruction

- Event 정렬
- Trace별 Timeline 생성
- 핵심 Event 추출

---

## Phase 7 — Causal Reconstruction

- parent-child Event 관계 구성
- Tool Request 원인 추적
- Root Cause 후보 도출

---

## Phase 8 — Evidence Ablation

- Evidence 제거 조건 생성
- Reconstruction 성능 측정
- Evidence Sufficiency 비교

---

## Phase 9 — Real LLM Agent

- Mock Agent를 실제 LLM 기반 Agent로 교체
- 동일 Scenario 재실험
- 비결정성 영향 분석

---

## Phase 10 — Multi-source Telemetry

- Tool Log
- Policy Log
- File-system Artifact
- Network Telemetry 확장

---

## Phase 11 — Response / Recovery

- Pause
- Permission Revocation
- Containment
- Recovery Verification

---

## Phase 12 — 분석 방식 비교

- Rule-based Analyzer
- LLM-based Analyzer
- Hybrid 방식 비교

---

## Phase 13 — 연구 결과 정리

- 정량 평가
- 오류 분석
- 한계 분석
- GitHub Documentation
- 연구 보고서 작성

---

# 16. 현재 구현 상태

현재 저장소에서는 다음 기능까지 구현하였다.

1. Mock Agent가 사용자 입력을 받는다.
2. "deadline"이 포함된 요청을 식별한다.
3. Agent가 구조화된 read_file Tool Request를 생성한다.
4. read_file Tool이 sandbox/public/project.txt 파일을 읽을 수 있다.

현재 정상 실행 흐름은 다음과 같다.

User  
→ Mock Agent  
→ Tool Request  
→ read_file  
→ Tool Result

다음 구현 목표는 Policy Gateway이다.

목표 구조:

Agent Decision  
→ Tool Request  
→ Policy Check  
→ ALLOW / DENY  
→ Tool Execution

---

# 17. 연구 범위 및 한계

초기 버전에서는 다음과 같이 범위를 제한한다.

- Single Agent
- Local Sandbox
- File Read Tool
- Indirect Prompt Injection
- Permission Violation
- JSONL Evidence
- Rule-based Reconstruction

따라서 초기 연구 결과를
모든 Agentic AI 시스템에 일반화하지 않는다.

또한 실제 LLM은 확률적이고 비결정적인 행동을 할 수 있으므로
초기 구현에서는 Mock Agent를 사용하여
포렌식 파이프라인 자체를 먼저 검증한다.

실제 LLM 적용은 이후 단계에서 수행한다.

---

# 18. 안전 및 윤리 원칙

AgentTrace의 공격 실험은
연구자가 직접 통제하는 Local Sandbox에서만 수행한다.

다음 원칙을 따른다.

- 실제 인증정보 사용 금지
- 실제 개인정보 사용 금지
- 제3자 시스템 공격 금지
- 실제 운영 환경 대상 Exploit 금지
- Secret 데이터는 전부 가상의 테스트 데이터 사용
- 비인가 Tool 동작은 Policy Layer에서 차단

프로젝트의 목적은 공격 능력 개발이 아니라
AI Agent 사고의 탐지, 증거 수집, 분석 및 재구성이다.

---

# 19. 기대 결과물

최종 프로젝트는 다음 구성요소를 포함하는 것을 목표로 한다.

AgentTrace
├── AI Agent Sandbox
├── Attack Scenario Dataset
├── Structured Event Logs
├── Permission / Policy Logs
├── Evidence Dataset
├── Timeline Reconstruction Engine
├── Causal Reconstruction Engine
├── Evidence Ablation Experiment
├── Cross-source Correlation
├── Incident Report
└── Research Report

최종 Incident Report 예시는 다음과 같다.

CASE: ATTACK-001

Initial Goal:
Find project deadline.

Attack Vector:
Indirect Prompt Injection

Injection Source:
malicious_note.txt

Requested Action:
read_file

Target:
sandbox/secret/credentials.txt

Requested Permission:
READ

Policy Decision:
DENY

Boundary Violation:
TRUE

Tool Execution:
BLOCKED

Impact:
Unauthorized file access attempted.
Protected data was not accessed.

Root Cause:
External malicious instruction entered
the Agent context through retrieved content.

Containment:
Tool execution blocked.

Evidence:
E003
E004
E005
E006
E007

---

# 20. 연구 의의

AgentTrace는 기존 CICIDS2017 프로젝트에서 수행한

Network Traffic  
→ Attack Detection  
→ Classification  
→ Error Analysis

에서 다음 단계로 확장한다.

AI Agent Activity  
→ Security Event  
→ Evidence Collection  
→ Cross-source Validation  
→ Timeline Reconstruction  
→ Causal Reconstruction  
→ Root Cause Analysis  
→ Response / Recovery Verification

CICIDS 프로젝트가

"공격인지 탐지할 수 있는가?"

를 다뤘다면,

AgentTrace는

"공격 또는 이상행동이 발생했다면
사후에 무엇이 일어났는지를 증거로 얼마나 정확하게 설명할 수 있는가?"

를 다룬다.

본 프로젝트의 최종 핵심 질문은 다음과 같다.

> AI Agent가 침해되었을 때,
> 우리는 남은 증거만으로 무엇이 일어났는지를
> 어느 수준까지 증명할 수 있는가?

---

# 21. 주요 참고자료

## OWASP

OWASP GenAI Security Project  
LLM01:2025 Prompt Injection

https://genai.owasp.org/llmrisk/llm01-prompt-injection/

OWASP GenAI Security Project  
LLM06:2025 Excessive Agency

https://genai.owasp.org/llmrisk/llm062025-excessive-agency/

---

## NIST

NIST NCCoE  
Accelerating the Adoption of Software and AI Agent Identity and Authorization  
Concept Paper, 2026-02-05

https://www.nccoe.nist.gov/publications/other/accelerating-adoption-software-and-ai-agent-identity-and-authorization-concept

---

## OpenAI

OpenAI  
The Hugging Face incident and the road ahead  
2026-08-26

https://openai.com/index/hugging-face-incident-and-the-road-ahead/

---

## Conference Notes

Cyber Summit Korea 2026  
2026-09-18, COEX Seoul

현장 발표에서 얻은 다음 설계 관점을 AgentTrace에 반영하였다.

- 최소권한과 Agent 자율성 통제
- Agent 행동에 대한 관측 가능성
- 서로 다른 telemetry 간 교차검증
- Discovery Source와 Proof Source의 구분
- Containment 및 Recovery 기록
- 권한, Tool, 로그, Timeline을 하나의 사건으로 분석

현장 발표 내용 중 공개자료로 독립 검증할 수 없는 세부사항은
연구의 객관적 근거가 아니라 설계 아이디어로만 사용한다.