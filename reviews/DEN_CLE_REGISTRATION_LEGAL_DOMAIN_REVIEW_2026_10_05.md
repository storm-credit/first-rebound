# DEN/CLE 등록 법적 범위 독립 종료 검수

기준 main `a7238c6c4d58a88d5f8cd7f6713fa1876eec8f9e` / PR #414. [연구 문서](../research/DEN_CLE_REGISTRATION_LEGAL_DOMAIN_2026_10_05.md), [재현 JSON](../research/DEN_CLE_REGISTRATION_LEGAL_DOMAIN_2026_10_05.json), [생성기](../tools/build_den_cle_registration_domain.py)를 검문했다.

## 수집과 독립 검수

별도 Codex 수집자는 frozen 공식 feed 실물·DEN 공식 거래쪽·CLE Cook/Martin 원문·기존 CLE3/24 경기책·계약 기간/일정을 직접 대조했다. 고유15그룹/21행, Clark 날짜 충돌, Cook 만료가 파생값이라는 점과 13명 예외의 TW 보정을 보고했다. CLE 전수 거래 가이드 미회수 및 기사 HTML shell/새 PDF timeout을 사실대로 구분했다.

부모 Codex는 같은 원자료를 실제 읽고 2019 규약 PDF78의 임시 비활동 예외까지 추가 대조했다. DEN3/24 공식 PDF는 웹 본문으로 직접 읽었지만 로컬 원본 요청은 timeout이었다. 이 미회수를 숨기지 않는다. 원문 표기가 다른 Clark 해제일·Stevens/Kabengele 기간을 임의 통일하지 않았다.

다른 Codex 독립 검수자는 실제 생성기와 JSON을 읽고 `--check --self-test`를 실행했다. **실질 결함을 발견하지 못했으며 DEN_CLE_DATED_REGISTRATION 하나만 LEGAL_BOUND_PASS로 전환 가능**하다고 판정했다. 53일×DEN 양분기·CLE53일, 13명9일 및 활동12+비활동1+TW비활동2의 법적 가능 배치, Cook/Kabengele/Rivers 만료/후속, Stevens 전환을 수용했다. Saddiq Bey와 Nnaji는 유효 첫 신인계약이라는 명시된 범위이며 McGee/C2 승인 생략이 보존된다.

## 기계 검문과 제외

음성4종은 Stevens 전환 누락, Harrison 잘못된 계약 종류, Cook 만료계약을 후속 서명까지 유지, 13명 기간2주 초과를 거부한다. 저장 출력과 생성값의 전체 대조는 명단/날짜 임의 변경을 거부한다. 원장은 세 필수 분기와 실제 존재하는 증인들을 연결한다.

법적 계약/급여/자격·TW 서비스 자격의 범위는 유지한다. 건강·8명 bench 가용·실제 활동 명단/분·리그 접수·후속 계약의 작가 선택·전체 급여/예외/매칭/픽은 여기서 인증하지 않는다. 다른10법적행, 모델/K/시즌/원고 플래그는 보존한다. 법적2완료/10HOLD·F0/5·A0/3·K0/4·season_selected=false·manuscript_allowed=false.

[기계 검문 기록](DEN_CLE_REGISTRATION_DOMAIN_CHECKS_2026_10_05.json): 각53일·DEN2분기/CLE1분기·고유15그룹/21행·5개10일·음성4종. 다른 법적행/모델/K/시즌/원고 상태 보존을 대조했다.

## V2 실행

NotebookLM은 [출처 등록](DEN_CLE_REGISTRATION_NLM_SOURCE_2026_10_05.json) 14.746초와 [분석](DEN_CLE_REGISTRATION_NLM_2026_10_05.json) 45.904초에 실제 응답을 회수했다. 날짜충돌 양분기·13명 임시배치/TW 보정·만료일 계산과 직접사실 구분·등록PASS/전체실행HOLD의 양립을 수용했다. 인용6개는 같은 파생 출처1개이며 독립 원자료 인증 증가0이다. 같은 파생 문서 인용은 독립 NBA 원자료 수를 늘리지 않는다. 이번 배치 추가 Antigravity 실행 NOT_RUN; 같은 작업 회차에서 이미 [빈 응답](S2_COHORT_AG_2026_10_05.json)을 회수했으며 불변 실패를 반복하지 않았다. Claude 기존 한도 후 NOT_RUN·전체 결과물 source-blind NOT_RUN. Codex 수집·저장소 재현·별도 반증을 각 역할대로 기록한다.

미완료 큰묶음6·최종회차기능0·실제 Context Pack0. PROJECT_FREEZE v0.30 PARTIAL·설계/원고 CLOSED·원고0.
