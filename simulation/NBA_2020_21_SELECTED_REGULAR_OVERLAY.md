# 2020–21 단일 BPM 정규시즌 — 승인 치환의 완전 입력 적용

2026-10-07 / 기준 main `94a672bd`. [실행 JSON](NBA_2020_21_SELECTED_REGULAR_OVERLAY.json), [생성·검문기](../tools/build_2020_21_selected_regular_overlay.py).

기존 [K1 기본 결합](NBA_2020_21_K1_BASE_INPUT_JOIN.json)의1080경기·2160팀 경기 선수초를 보존하면서, 승인된 J1/F4/F5/C2 방향과 [건강·시즌 설계 위임](../canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json) 아래 작업 출전분을 적용했다. 원고는 작성하지 않았다. 정확 K1 경로·Hall5/9 재계약 생략·McGee 거래 생략·C2 복귀 계약 생략이 입력에서 바뀌면 생성기가 거부한다.

## 원입력과 적용 순서

| 치환 | 최초 팀 경기 수 | 최종 적용 수 | 완전 벡터 원입력 |
|---|---:|---:|---|
| J1 Terry3/30 이후 휴가 | 27 | 27 | POLICY_REPLACEMENT_MINUTES의 J1_TERRY_LEAVE / LOW_MINUTES |
| F4 Hall5/9 재계약 생략 | 5 | 5 | HALL_FIVE_GAME_LOAD_SCREEN의 candidate_minutes(단위초) |
| F5 McGee 거래 생략 | 25 | 23 | FINAL859 벡터에 Denver McGee→Hartenstein, Cleveland Hartenstein→McGee |
| C2 Varejão 복귀 생략 | 5 | 5 | C2_COMPLETE_WORKING_MINUTES의 전체 벡터 |
| F5 기존 화면 밖 E/CHI_POST 네 분기 | 4 | 4 | 기본 전체 벡터의 거래 후 선수만 잔류 상대 선수로 치환 |
| 최종 고유 팀 경기 | 66−2 | 64 | 고유 경기62개 |

F4는 더 보수적인 [후속5경기 부담 벡터](ORLANDO_2020_21_HALL_FIVE_GAME_LOAD_SCREEN.json)를 기존 위임 아래 감독·건강 작업 모델로 선택했다. 최초 감도 화면은 수정하지 않았다. Bamba의 원역사 양의 출전3경기에서 추가분0을 유지하지만 이 원분 상단이 새 세계의 의료적 허가라는 뜻은 아니다. Vucevic·Wagner·Nnaji의 새 분 역시 감독 모델이다.

C2의5/5·5/7 전체 벡터에는 이전 F5 Hartenstein 제거분이 이미 포함돼 있다. `complete_replacement_history`의 두 행은 F5 벡터를 C2 벡터로 **대체**하며 더하지 않는다. 같은 팀 자원의 다른 중복 적용은 거부한다. McGee의 C2 출전 합계는3681초이고 Varejão2156초와 Hartenstein1525초를 한 번씩만 재배정한다.

각 치환은 실명5인조 증인으로 전체 선수초와 공통 clock을 맞춘다. Denver11행은 원증인의 McGee 이름을 Hartenstein으로 바꾸며 실제 분은 보존한다. 선발도 F5의 candidate_starters로 치환하고 J1/F4/C2의 명시된 선발을 연결한다. 제거 선수가 선발에 남지 않으며 선발5명·양수 분·해당5인조180초 이상의 증인을 검문한다. Cleveland14행의 저장된 조건부 증인 및 C2새5행의 증인을 연결한다. 선형계획 증인의 존재는 실제 감독 판단·효율·의료·등록 접수 증명이 아니다. 전체2160행의 교체 순서를 생성하거나 인증하지 않았다.

## F5 범위 누락 네 행 수리

2026-10-07 후속 전수명단 검문에서 FINAL859 화면 밖 네 행이 과거 실제 거래 선수를 유지한 오류를 찾았다. DEN 4/9 SAS전579초·4/28 NOP전691초는 McGee→Hartenstein, CLE 4/17 CHI전962초·4/21 CHI전973초는 Hartenstein→McGee로 수리했다. 원역사 기본자료는 바꾸지 않고 작업 입력의 해당 선수만 치환한다. 나머지2156팀 벡터·모든 선발/팀시계·기존107증인은 보존했다. 새 네 증인은 `CONSTRUCTED_UNIFORM_MATROID_EXISTENCE_ONLY`이며 과거 관측 증인으로 인증하지 않는다. 1080승패·순위 변경0이다. [전후 전수 검문](../reviews/F5_FOUR_SOURCE_BRANCH_COMPLETION_REVIEW_2026_10_07.json)과 [재현기](../tools/audit_2020_21_f5_source_branch_completion.py)는 네 행 중 하나라도 과거 거래 선수를 복원하면 거부한다.

## 1080경기 승패를 한 평점법으로 다시 계산

[단일 점수차 결합 도구](../tools/audit_2020_21_selected_margin_join.py)가1008개의 비시카고 표현과72개의 시카고 표현에 J1을 반영한1080경기 기준 상수·미확인 평점 계수를 제공한다. 그 위에 J1을 제외한37개 팀의 **완성 벡터 차이**를 적용한다. `cc.form`의 선수초 효과와 기존0.5 B2B 양수 delta 부하 항을 함께 계산하고, 공유 Fictional Rival 평점1.0252302025782687과 같은 BPM 실증 스트레스 범위를 전 시즌에 사용한다. 미확인 평점은0으로 채우지 않는다.

시카고 상대 경기의 추가 피로는 기존 `UPSTREAM_CHI_ONLY` 계산 범위를 보존한다. 그외 경기는 해당 팀의 B2B 여부에 따라 노출 차이를 계산한다. RAPTOR 결과를 섞지 않는다. 기존 화면의 구간을 단순히 더한 결과를 새 검산으로 부르지 않는다.

| 양 팀 치환 경기 | J1 CHA 기준 홈 상수 | F5 CLE 반영 뒤 홈 구간 | 재계산 승자 |
|---|---:|---:|---|
| 2021-04-14_CHA_CLE | −14.3930888428 | −14.56892978 | CLE |
| 2021-04-23_CHA_CLE | +4.7450204978 | +4.54383311 | CHA |

두 경기 모두 CHA와CLE 전체 분 벡터를 연결하고 홈/원정 부호를 적용했다. CLE 추가 피로 항은 두 날짜 모두 B2B가 아니라0이다. 기존 J1의 CHA 피로는 기준 표현에 이미 들어 있으므로 다시 넣지 않는다.

1080개 홈 구간을 전부 새로 평가한 결과 미결정0, 초기 K1 승자와의 차이0이었다. CHI31승·MIN24승, 전체 승수 합계1080을 유지한다. `initial_k1_winner`는 비교 원본이며 `winner`는 새 평가 결과다. 미결정이 생기면 원승자를 임의 복사하지 않고 null로 남긴다. 가장 가까운0 경계까지의 거리는0.06403817이다. 이것은 확률·실제 점수·실제 승패 인증이 아니다.

## 시간·건강·출처 경계

이 파일은 양수 선수의 availability를 **작가 위임 작업 모델**로 선택한다.0분 선수의 건강은 null이고0분 이유도 미선택으로 둔다. 양수 분이나0분을 실제 의학적 허가·결장·방출·전체 등록 명단으로 바꾸지 않는다. 전체 명단·오프데이 건강·이후 새로운 접촉 사건·포제션·경기 박스의 완전 인증은 별도다.

원입력 clock 차이6행(−1초4개·+1초1개·−3초1개)의 선수초는 수정하지 않고 `source_clock_gaps_retained`로 표시했다. J1의1개3180초 경기와 다른 기존 OT clock도 작업 입력으로 보존하며, 전 경기를 무조건2880초로 바꾸지 않는다. 단위 보정을 새로 선택할 때는 분·점수차를 다시 연결해야 한다.

저장소 해시는 UTF-8 BOM 제거·CRLF/CR→LF 정규화 후 계산한다. `source_sha256`와 `margin_join_source_sha256`는 연결된 원입력을 표시한다. 기존 원자료의 회수 기록을 새 수집 성공으로 계수하지 않았다. Antigravity·NotebookLM·Claude는 이 하위 구현에서 실행하지 않았다.

사실: 기존 원자료·승인된 생략 방향. 추론: 실증 평점 범위의 수치 효과. 작가 위임 선택: 후속F4 분과 전체 양수 availability 작업 모델. 미인증: 실제 등록·의료·전체 건강·전체 법적 실행·시즌 최종 승인. 해당 인증과 `manuscript_allowed`는 모두false다. freeze v0.30 PARTIAL·설계/원고 CLOSED·원고0을 유지한다. 루트 외부 검문은 대기다.

재생성: `python -B -X utf8 tools/build_2020_21_selected_regular_overlay.py --self-test`
확인: `python -B -X utf8 tools/build_2020_21_selected_regular_overlay.py --check --self-test`

기본 입력은 원출처 재구성 대조를 통과해야 한다. 음성 검사는 McGee 중복 가산, 제거 선수·선발 재삽입, 팀 자원 중복, 양 팀 입력 누락, 승자 변조, 출처·권한·의료·시즌 변조11건, 원권위 K1/F4/F5/C2 방향 변경4건, 팀 총합을 보존한 기본 입력의 선수초 재분배1건을 거부한다. 중앙 상태 파일·이전 후보 파일은 이 생성기로 수정하지 않는다.
