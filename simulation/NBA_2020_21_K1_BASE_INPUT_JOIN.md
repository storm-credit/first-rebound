# 2020–21 K1 정규시즌 단일 작업 입력: 원천 보존 기본 결합

상태: `COMPLETE_BASE_JOIN_NOT_APPROVED_OVERLAY_FINAL`. 선택된 K1 / BPM F038의 승자 1080경기와
팀별 선수 출전 초 2160행을 공식 일정 event ID로 연결했다.
원천 구성: 기존 LOW_MINUTES 분기 2045행,
시카고 트레이드 전 관측·도너 86행,
트레이드 후 PORTER_ZERO 시카고 29행.

시계 차이(`필요 초 - 원천 합계`) 분포: -3: 1, -1: 4, 0: 2154, 1: 1. 0이 아닌 행의 선수별 초는
수정하지 않았다. 각 행에 원천 파일·선택자와 적용하지 않은 차이를 기록했다.
선택된 전반 상대팀 분기는 INTEGRATED_PATHS / CLOSE_GAME_PATHS의 선수 초와 기존 5인 조합
증인을 사용했다. 후반 시카고는 POSTDEADLINE_LINEUP_AUDIT의 최소 변경 선수 초,
후보 선발 5명과 구간 증인을 사용했다. 증인이 없는 행의 `lineup_witness`는 null이며
새 5인 조합을 생성하지 않았다. 감사 산출물의 1e-8초 수준 부동소수 잔차는
`solver_float_residual_seconds`로 따로 보존한다.

승자표는 K1 추천 원본을 그대로 참조하며 NBA_2020_21_FULL_SEASON의
F038 `season_bridge[114]` 조건 및 평점 구간과 교차 확인했다. CHI 31승,
MIN 24승. J1, F4, F5, C2의 승인된 예외를 분 단위로
적용하고 겹치는 경기의 승패를 재계산하는 일은 이 기본 결합에 포함되지 않는다.
따라서 시즌 실행, 법률·계약, 건강 전체 및 원고 게이트는 열리지 않았다.

재생성: `python tools/collect_2020_21_single_policy_base_inputs.py --write`
검증: `python tools/collect_2020_21_single_policy_base_inputs.py --check`
