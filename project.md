# 프로젝트 파일 구조 및 설명

## 📚 프로젝트 개요
AI 에이전트 엔지니어링의 실습 코드베이스입니다. 7개 이상의 실제 비즈니스 도메인에 대한 프로덕션 수준의 AI 에이전트 시스템을 구현하고 있습니다.

---

## 🗂️ 루트 레벨 파일들

### 설정 및 구성 파일

#### `pyproject.toml`
- **목적**: 프로젝트 메타데이터 및 의존성 관리
- **주요 내용**:
  - 프로젝트 이름: `building-applications-with-ai-agents`
  - Python 버전 요구사항: `>=3.12,<3.13`
  - 핵심 의존성: OpenAI, LangChain, LangGraph, LangChain Community 등
  - pytest 설정 및 테스트 경로 정의
  - uv 패키지 매니저 설정
- **사용처**: `uv sync` 명령으로 의존성 설치 시 참조

#### `uv.lock`
- **목적**: 의존성 잠금 파일
- **주요 내용**: 정확한 버전과 해시로 재현 가능한 빌드 보장
- **관리**: uv가 자동 생성 및 관리

#### `conftest.py`
- **목적**: pytest 전역 설정 및 테스트 환경 구성
- **주요 기능**:
  - `src/` 디렉토리를 `sys.path`에 추가
  - 모든 테스트에서 `import common...` 등의 임포트가 가능하도록 설정
- **사용처**: pytest 실행 시 자동으로 로드됨

#### `pytest.ini`
- **목적**: pytest 실행 옵션 및 경고 필터링
- **주요 설정**:
  - Pydantic 관련 deprecation 경고 무시
- **사용처**: pytest 실행 시 자동 적용

#### `README.md`
- **목적**: 프로젝트 전체 문서 및 가이드
- **주요 내용**:
  - 프로젝트 개요 및 핵심 가치 제안
  - 설치 방법 (uv 사용)
  - 사용법 및 예제
  - 디렉토리 구조 설명
  - 7개 도메인 에이전트 상세 정보
  - 기술 스택 및 참고 자료
- **대상**: 개발자, 기여자, 학습자

---

## 📁 src/ - 소스 코드 메인 디렉토리

### `src/__init__.py`
- **목적**: src를 Python 패키지로 인식
- **내용**: 일반적으로 비어있거나 최소한의 초기화 코드

---

## 📁 src/common/ - 프레임워크 독립적인 공통 모듈

### `src/common/__init__.py`
- **목적**: common을 Python 패키지로 인식

### `src/common/graph_rag.py`
- **목적**: Graph RAG (Retrieval Augmented Generation) 구현
- **주요 기능**:
  - 문서 청킹 (chunk splitting)
  - 엔티티 및 관계 추출
  - 지식 그래프 구축
  - 커뮤니티 감지 (Leiden 알고리즘)
  - 커뮤니티별 계층적 요약 생성
  - 질의 기반 답변 생성
- **사용 시나리오**: 복잡한 문서에서 지식을 추출하고 질문에 답변

---

## 📁 src/common/a2a/ - Agent-to-Agent 통신

### `src/common/a2a/agent_server.py`
- **목적**: JSON-RPC 2.0 기반 에이전트 서버
- **주요 기능**:
  - Agent Card 제공 (`/.well-known/agent.json`)
  - 에이전트 기능 발견 가능
  - JSON-RPC 메서드 노출
- **프로토콜**: 표준화된 에이전트 간 통신

### `src/common/a2a/agent_client.py`
- **목적**: 에이전트 서버와 통신하는 클라이언트
- **주요 기능**:
  - Agent Card 검색
  - JSON-RPC 요청 전송
  - 응답 처리

---

## 📁 src/common/evaluation/ - 평가 프레임워크

### `src/common/evaluation/ai_judge.py`
- **목적**: LLM 기반 에이전트 출력 품질 평가
- **평가 항목**:
  - 정확성
  - 완전성
  - 적절성
- **방법**: GPT-4 등을 판단자로 활용

### `src/common/evaluation/batch_evaluation.py`
- **목적**: 대규모 테스트 세트 자동 평가
- **주요 기능**:
  - JSONL 평가 데이터셋 로드
  - 에이전트 실행 및 결과 수집
  - 메트릭 계산 및 리포트 생성
- **사용법**: `--dataset`, `--graph_py` 인자로 실행

### `src/common/evaluation/distribution_shifts.py`
- **목적**: 데이터 드리프트 및 성능 저하 모니터링
- **주요 기능**:
  - 입력/출력 분포 변화 감지
  - 성능 메트릭 추이 분석
  - 알림 및 경고 생성

### `src/common/evaluation/memory_evaluation.py`
- **목적**: 에이전트의 메모리 능력 평가
- **평가 항목**:
  - 단기 메모리 (대화 컨텍스트)
  - 장기 메모리 (지식 유지)
  - 컨텍스트 일관성

### `src/common/evaluation/metrics.py`
- **목적**: 표준화된 평가 메트릭 정의
- **주요 메트릭**:
  - Tool Recall/Precision (도구 호출 정확도)
  - Parameter Accuracy (매개변수 정확성)
  - Phrase Recall (응답 적합성)
  - Task Success (작업 성공률)

### `src/common/evaluation/README_Evaluations.md`
- **목적**: 평가 프레임워크 사용 가이드
- **내용**: 평가 방법론, 메트릭 설명, 예제

### `src/common/evaluation/scenarios/` - 도메인별 평가 데이터셋

각 JSONL 파일은 특정 도메인의 평가 시나리오를 포함합니다:

#### `ecommerce_customer_support_evaluation_set.jsonl`
- **도메인**: 전자상거래 고객 지원
- **시나리오 수**: ~15개
- **테스트 케이스**: 주문 환불, 취소, 주소 변경

#### `financial_services_account_management.jsonl`
- **도메인**: 금융 서비스
- **시나리오 수**: ~20개
- **테스트 케이스**: 사기 탐지, 계좌 동결, 대출 신청

#### `healthcare_patient_intake_and_triage.jsonl`
- **도메인**: 의료 환자 접수
- **시나리오 수**: ~18개
- **테스트 케이스**: 환자 등록, 증상 평가, 예약

#### `it_help_desk_system_administration.jsonl`
- **도메인**: IT 헬프데스크
- **시나리오 수**: ~22개
- **테스트 케이스**: 액세스 관리, 비밀번호 재설정, 문제 해결

#### `legal_document_review_case_management.jsonl`
- **도메인**: 법률 문서 검토
- **시나리오 수**: ~16개
- **테스트 케이스**: 계약 검토, 사례 연구, 규정 준수

#### `security_operations_center_analyst.jsonl`
- **도메인**: 보안 운영 센터 (SOC)
- **시나리오 수**: ~19개
- **테스트 케이스**: 위협 조사, 로그 분석, 인시던트 분류

#### `supply_chain_logistics_management.jsonl`
- **도메인**: 공급망 관리
- **시나리오 수**: ~17개
- **테스트 케이스**: 재고 관리, 배송 추적, 공급업체 관계

#### `supply_chain_multi_agent.jsonl`
- **도메인**: 공급망 멀티 에이전트
- **특징**: 여러 에이전트 간 협업 시나리오

---

## 📁 src/common/mcp/ - Model Context Protocol

### `src/common/mcp/MCP_math_server.py`
- **목적**: 수학 계산 서버 (MCP 프로토콜)
- **기능**: 안전한 수식 평가 및 계산
- **통신**: stdin/stdout 기반 JSON 메시지

### `src/common/mcp/MCP_weather_server.py`
- **목적**: 날씨 정보 서버 (MCP 프로토콜)
- **기능**: 날씨 데이터 제공
- **통신**: stdin/stdout 기반 JSON 메시지

---

## 📁 src/common/observability/ - 관찰성 스택

### `src/common/observability/loki_logger.py`
- **목적**: Loki 로그 집계 시스템 연동
- **주요 기능**:
  - `log_to_loki(label, message)` 함수
  - JSON 형식 로그 전송
  - 레이블 기반 로그 분류
- **엔드포인트**: `http://localhost:3100`

### `src/common/observability/instrument_tempo.py`
- **목적**: OpenTelemetry / Tempo 분산 추적
- **주요 기능**:
  - 스팬(span) 계측
  - 분산 트레이싱
  - 성능 모니터링
- **엔드포인트**: OTLP `localhost:3200`

### `src/common/observability/docker-compose.yaml`
- **목적**: 로컬 관찰성 스택 실행
- **서비스**:
  - Loki (로그 집계)
  - Tempo (분산 추적)
  - Promtail (로그 수집)
- **실행**: `docker-compose up -d`

### 기타 설정 파일들
- `*-config.yaml`: Loki, Tempo, Promtail 설정 파일

---

## 📁 src/fine_tuning/ - 모델 파인튜닝

### `src/fine_tuning/__init__.py`
- **목적**: fine_tuning을 Python 패키지로 인식

### `src/fine_tuning/supervised_fine_tuning.py`
- **목적**: SFT (Supervised Fine-Tuning) 구현
- **방법**: 지도 학습 기반 모델 최적화
- **데이터**: `training_data/sft_it_help_desk_training_data.jsonl`
- **목표**: IT 헬프데스크 도메인 특화 모델

### `src/fine_tuning/direct_preference_optimization.py`
- **목적**: DPO (Direct Preference Optimization) 구현
- **방법**: 선호도 데이터로 모델 정렬
- **데이터**: `training_data/dpo_it_help_desk_training_data.jsonl`
- **장점**: RLHF보다 간단하고 효율적

### `src/fine_tuning/reinforcement_learning_with_verifiable_rewards.py`
- **목적**: RLVR (RL with Verifiable Rewards) 구현
- **방법**: 검증 가능한 보상 기반 강화학습
- **데이터**: `training_data/rlvr_it_help_desk_training_data.jsonl`
- **특징**: 명확한 보상 신호로 정확한 학습

### `src/fine_tuning/skill_selection_fine_tuning/`
- **목적**: 스킬 선택 능력 파인튜닝
- **방법**: GRPO (Group Relative Policy Optimization) 등
- **목표**: 적절한 스킬/도구 선택 능력 향상

### `src/fine_tuning/training_data/`
- **내용**: 파인튜닝용 훈련 데이터셋 (JSONL 형식)
- **파일들**:
  - `sft_it_help_desk_training_data.jsonl`
  - `dpo_it_help_desk_training_data.jsonl`
  - `rlvr_it_help_desk_training_data.jsonl`

---

## 📁 src/frameworks/ - 에이전트 프레임워크 구현

### `src/frameworks/__init__.py`
- **목적**: frameworks를 Python 패키지로 인식

---

## 📁 src/frameworks/autogen_agents/ - Microsoft Autogen

### `src/frameworks/autogen_agents/autogen_mcp_client.py`
- **목적**: Autogen에서 MCP 클라이언트 사용
- **기능**: MCP 프로토콜 도구 통합

### `src/frameworks/autogen_agents/calculator_tool_use.py`
- **목적**: 계산기 도구 사용 예제
- **기능**: 수학 계산 에이전트

### `src/frameworks/autogen_agents/web_surfer_agent.py`
- **목적**: 웹 검색 및 탐색 에이전트
- **기능**: 웹 브라우징, 정보 수집

---

## 📁 src/frameworks/langchain/ - LangChain

### `src/frameworks/langchain/calculator_tool_use.py`
- **목적**: LangChain 계산기 도구 사용
- **기능**: 체인 기반 계산

### `src/frameworks/langchain/hierarchical_skill_selection.py`
- **목적**: 계층적 스킬 선택 메커니즘
- **방법**: 트리 구조 기반 스킬 탐색
- **사용 시나리오**: 복잡한 스킬 계층 구조

### `src/frameworks/langchain/semantic_skill_selection.py`
- **목적**: 의미론적 스킬 선택
- **방법**: 의미 유사도 기반 매칭
- **사용 시나리오**: 자연어 요청에 적합한 스킬 찾기

### `src/frameworks/langchain/langchain_embedding_skill_selection.py`
- **목적**: 임베딩 기반 스킬 선택
- **방법**: 벡터 유사도 검색
- **장점**: 빠르고 확장 가능

### `src/frameworks/langchain/stock_price_tool_use.py`
- **목적**: 주식 가격 조회 도구
- **기능**: 금융 데이터 API 연동

### `src/frameworks/langchain/wikipedia_tool_use.py`
- **목적**: Wikipedia 검색 도구
- **기능**: 정보 검색 및 요약

---

## 📁 src/frameworks/langgraph_agents/ - LangGraph 에이전트

### 학습 패턴 구현

#### `src/frameworks/langgraph_agents/reflexion.py`
- **목적**: Reflexion 패턴 구현
- **기능**: 실패로부터 학습, 전략 개선
- **방법**: 자기 반성 및 계획 수정

#### `src/frameworks/langgraph_agents/experiential_learning.py`
- **목적**: 경험 기반 학습
- **기능**: 과거 경험을 활용한 의사결정
- **방법**: 경험 데이터베이스 구축 및 검색

#### `src/frameworks/langgraph_agents/semantic_memory_langgraph.py`
- **목적**: 장기 기억 관리
- **기능**: 지식 유지 및 회상
- **방법**: 의미론적 메모리 저장소

#### `src/frameworks/langgraph_agents/short_term_memory.py`
- **목적**: 단기 기억 관리
- **기능**: 대화 컨텍스트 유지
- **방법**: 세션 상태 관리

### 도구 및 통합

#### `src/frameworks/langgraph_agents/langgraph_mcp_client.py`
- **목적**: LangGraph에서 MCP 도구 사용
- **기능**: MCP 프로토콜 통합

#### `src/frameworks/langgraph_agents/langgraph_tool.py`
- **목적**: LangGraph 커스텀 도구 정의
- **기능**: 도구 래퍼 및 유틸리티

---

## 📁 src/frameworks/langgraph_agents/ecommerce_customer_support/

### `customer_support_agent.py`
- **목적**: 전자상거래 고객 지원 에이전트
- **도구**:
  - `refund_order`: 주문 환불 처리
  - `cancel_order`: 주문 취소
  - `change_delivery_address`: 배송지 변경
- **평가 세트**: `ecommerce_customer_support_evaluation_set.jsonl`

### `customer_support_agent_with_traceloop.py`
- **목적**: Traceloop 관찰성 통합 버전
- **추가 기능**: 추적 및 모니터링

---

## 📁 src/frameworks/langgraph_agents/financial_services/

### `financial_services_agent.py`
- **목적**: 금융 서비스 에이전트
- **도구**:
  - `detect_fraud`: 사기 탐지
  - `freeze_account`: 계좌 동결
  - `loan_application`: 대출 신청 처리
  - `dispute_resolution`: 분쟁 해결
- **평가 세트**: `financial_services_account_management.jsonl`

---

## 📁 src/frameworks/langgraph_agents/healthcare/

### `healthcare_patient_intake_agent.py`
- **목적**: 의료 환자 접수 에이전트
- **도구**:
  - `register_patient`: 환자 등록
  - `symptom_assessment`: 증상 평가
  - `schedule_appointment`: 예약 스케줄링
  - `verify_insurance`: 보험 확인
- **평가 세트**: `healthcare_patient_intake_and_triage.jsonl`

---

## 📁 src/frameworks/langgraph_agents/it_helpdesk/

### `it_helpdesk_agent.py`
- **목적**: IT 헬프데스크 에이전트
- **도구**:
  - `provision_access`: 사용자 액세스 제공
  - `reset_password`: 비밀번호 재설정
  - `troubleshoot_system`: 시스템 문제 해결
  - `create_ticket`: 티켓 생성
- **평가 세트**: `it_help_desk_system_administration.jsonl`

---

## 📁 src/frameworks/langgraph_agents/legal/

### `legal_document_review_agent.py`
- **목적**: 법률 문서 검토 에이전트
- **도구**:
  - `review_contract`: 계약 검토
  - `case_research`: 사례 연구
  - `client_intake`: 고객 접수
  - `compliance_monitoring`: 규정 준수 모니터링
- **평가 세트**: `legal_document_review_case_management.jsonl`

---

## 📁 src/frameworks/langgraph_agents/soc/

### `soc_analyst_agent.py`
- **목적**: 보안 운영 센터 분석가 에이전트
- **도구**:
  - `investigate_threat`: 위협 조사
  - `analyze_logs`: 로그 분석
  - `triage_incident`: 인시던트 분류
  - `isolate_host`: 호스트 격리
- **평가 세트**: `security_operations_center_analyst.jsonl`

---

## 📁 src/frameworks/langgraph_agents/supply_chain/

### `supply_chain_logistics_agent.py`
- **목적**: 공급망 물류 에이전트 (단일)
- **도구**:
  - `manage_inventory`: 재고 관리
  - `track_shipment`: 배송 추적
  - `vendor_relations`: 공급업체 관계
  - `warehouse_operations`: 창고 운영
- **평가 세트**: `supply_chain_logistics_management.jsonl`

### `supply_chain_logistics_multi_agent.py`
- **목적**: 멀티 에이전트 공급망 시스템 (기본)
- **구조**: 여러 전문 에이전트 간 협업
- **평가 세트**: `supply_chain_multi_agent.jsonl`

### `ray_supply_chain_multi_agent.py`
- **목적**: Ray 기반 분산 멀티 에이전트
- **특징**:
  - 분산 병렬 처리
  - 높은 확장성
  - 대규모 워크로드 처리
- **요구사항**: Ray 클러스터

### `redis_streams_multi_agent_supply_chain.py`
- **목적**: Redis Streams 기반 이벤트 드리븐 시스템
- **특징**:
  - 비동기 메시지 전달
  - 이벤트 소싱
  - 느슨한 결합
- **요구사항**: Redis 서버

### `temporal_supply_chain_multi_agent.py`
- **목적**: Temporal 워크플로우 오케스트레이션
- **특징**:
  - 내구성 있는 워크플로우
  - 자동 재시도
  - 장기 실행 프로세스
- **요구사항**: Temporal 서버

---

## 📁 src/frameworks/open_ai/ - OpenAI 고급 기능

### `automated_design_of_agentic_systems.py`
- **목적**: ADAS (Automated Design of Agentic Systems)
- **기능**: 에이전트 시스템 자동 설계 및 메타 최적화
- **사용 시나리오**: 에이전트 아키텍처 자동 생성

### `realtime_voice_agent.py`
- **목적**: 실시간 음성 대화 에이전트
- **기능**: 저지연 음성 입출력
- **사용 시나리오**: 음성 고객 지원, 대화형 인터페이스

---

## 📁 tests/ - 테스트 스위트

### `tests/__init__.py`
- **목적**: tests를 Python 패키지로 인식

---

## 📁 tests/evaluation/ - 평가 유틸리티 테스트

### `tests/evaluation/test_ai_judge.py`
- **목적**: AI Judge 평가 로직 테스트
- **검증 항목**:
  - 판단 정확성
  - 메트릭 계산
  - 엣지 케이스 처리

### `tests/evaluation/test_memory_evaluation.py`
- **목적**: 메모리 평가 시스템 테스트
- **검증 항목**:
  - 단기/장기 메모리 측정
  - 컨텍스트 유지 능력

---

## 📁 tests/frameworks/ - 프레임워크 통합 테스트

### `tests/frameworks/langgraph_agents/test_langgraph_customer_support_agent.py`
- **목적**: 전자상거래 에이전트 통합 테스트
- **검증 항목**:
  - 도구 호출 정확성
  - 응답 품질
  - 엔드-투-엔드 시나리오

---

## 📁 tests/observability/ - 관찰성 테스트

### `tests/observability/test_loki_logger.py`
- **목적**: Loki 로거 기능 테스트
- **검증 항목**:
  - 로그 전송
  - 레이블 처리
  - 에러 핸들링

### `tests/observability/test_instrument_tempo.py`
- **목적**: Tempo 추적 계측 테스트
- **검증 항목**:
  - 스팬 생성
  - 트레이스 전파
  - OTLP 전송

---

## 📁 tests/fine_tuning/ - 파인튜닝 테스트

### `tests/fine_tuning/test_function_calling_fine_tuning.py`
- **목적**: 함수 호출 파인튜닝 테스트
- **검증 항목**:
  - 훈련 데이터 로드
  - 모델 훈련 프로세스
  - 파인튜닝 결과 검증

---

## 🎯 핵심 워크플로우

### 1. 에이전트 개발 워크플로우
```
1. 도메인 선택 → 2. 도구 정의 → 3. 에이전트 구현 → 4. 평가 세트 작성 → 5. 배치 평가 실행
```

### 2. 평가 워크플로우
```
1. 평가 데이터 준비 (JSONL) → 2. batch_evaluation.py 실행 → 3. 메트릭 분석 → 4. 개선 사항 식별
```

### 3. 파인튜닝 워크플로우
```
1. 훈련 데이터 수집 → 2. SFT/DPO/RLVR 선택 → 3. 훈련 실행 → 4. 평가 및 배포
```

### 4. 관찰성 워크플로우
```
1. Docker Compose 시작 → 2. 에이전트에 계측 추가 → 3. Loki/Tempo 대시보드 모니터링
```

---

## 📊 기술 스택 요약

| 카테고리 | 기술 |
|---------|------|
| **프레임워크** | LangChain, LangGraph, Autogen, OpenAI |
| **언어** | Python 3.12 |
| **패키지 관리** | uv |
| **LLM** | OpenAI GPT-4, GPT-5 |
| **분산 처리** | Ray, Redis Streams, Temporal |
| **관찰성** | Loki, Tempo, OpenTelemetry |
| **테스트** | pytest |
| **컨테이너** | Docker, Docker Compose |
| **지식 그래프** | Graph RAG (커뮤니티 감지) |

---

## 🚀 빠른 시작 가이드

### 1. 환경 설정
```bash
uv sync
cp .env.example .env
# .env에 OPENAI_API_KEY 입력
```

### 2. 간단한 에이전트 실행
```bash
uv run python ch02/simple_customer_support_agent.py
```

### 3. 특정 도메인 에이전트 실행
```bash
uv run python src/frameworks/langgraph_agents/ecommerce_customer_support/customer_support_agent.py
```

### 4. 평가 실행
```bash
uv run python -m src.common.evaluation.batch_evaluation \
  --dataset src/common/evaluation/scenarios/ecommerce_customer_support_evaluation_set.jsonl \
  --graph_py src/frameworks/langgraph_agents/ecommerce_customer_support/customer_support_agent.py
```

### 5. 관찰성 스택 시작
```bash
cd src/common/observability
docker-compose up -d
```

### 6. 테스트 실행
```bash
uv run pytest tests/ -q
```

---

## 📖 학습 경로

### 초급 (1-2주)
1. `ch02/simple_customer_support_agent.py` - 기본 에이전트 구조 이해
2. `README.md` - 프로젝트 전체 개요
3. 단일 도메인 에이전트 실행 및 분석

### 중급 (2-4주)
4. 스킬 선택 메커니즘 (계층적, 의미론적, 임베딩)
5. 학습 패턴 (Reflexion, Experiential Learning)
6. 평가 프레임워크 사용

### 고급 (4주+)
7. 멀티 에이전트 시스템 (Ray, Redis, Temporal)
8. Graph RAG 구현
9. 파인튜닝 (SFT, DPO, RLVR)
10. 프로덕션 관찰성 및 모니터링

---

## 🔧 개발 팁

### 새 도메인 에이전트 추가
1. `src/frameworks/langgraph_agents/<domain>/` 디렉토리 생성
2. 도구 정의 및 에이전트 구현
3. `src/common/evaluation/scenarios/<domain>_evaluation_set.jsonl` 평가 세트 작성
4. `tests/frameworks/langgraph_agents/test_<domain>_agent.py` 테스트 작성

### 디버깅
- Loki 로그: `http://localhost:3100`
- Tempo 트레이스: `http://localhost:3200`
- pytest 상세 출력: `pytest -v --tb=short`

### 성능 최적화
- 임베딩 캐싱 활용
- 배치 처리로 API 호출 최소화
- Ray로 병렬 처리

---

## 📚 참고 문서 위치

- **전체 가이드**: `README.md`
- **평가 가이드**: `src/common/evaluation/README_Evaluations.md`
- **책 링크**: [O'Reilly - Building Applications with AI Agents](https://www.oreilly.com/library/view/building-applications-with/9781098176495/)

---

**마지막 업데이트**: 2025-11-29
**프로젝트 버전**: 0.1.0

