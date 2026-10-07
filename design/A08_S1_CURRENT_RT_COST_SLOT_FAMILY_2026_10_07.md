# A08-S1 현재 FY22 RT1–RT4 비용·자리 함수

기존 E40의 역할 제안과 같은 가상 에이전트에게 전달할 조건부 비교표다. 2022-07-07 stage2 현재 192개 명명 드래프트권 공개 범주 셀을 원 전체비용 셀과 조인하고, 검토된 576행 legacy 보정에서 중복 캠프 예약 $4,372,601을 제거했다. 과거 stretch 보수 $16,371,000의 보수적 보호는 남겼다. 기존 G8의 48×4 부분 예산 차이는 현재 금액에 더하지 않았다.

| 정책 | 현재 normal 공개 외곽 구간, H_B 제외 | 보수적 apron 전액 스크린 | 명단 조건 |
|---|---:|---:|---|
| RT1 Bradley 옵션 유지·Valentine 유지 | $150,860,604–$229,414,291 | $150,860,604–$192,553,291 | 기존 STD −0 + 실제 서명 대체 0..0 + 실제 서명 신인 ≤15 |
| RT2 Bradley 옵션 거절·Valentine 유지 | $148,824,276–$230,377,963 | $148,824,276–$193,516,963 | 기존 STD −1 + 실제 서명 대체 0..1 + 실제 서명 신인 ≤15 |
| RT3 Bradley 유지·Valentine 방출 | $150,860,604–$232,414,291 | $150,860,604–$195,553,291 | 기존 STD −1 + 실제 서명 대체 0..1 + 실제 서명 신인 ≤15 |
| RT4 Bradley 옵션 거절·Valentine 방출 | $148,824,276–$236,377,963 | $148,824,276–$196,516,963 | 기존 STD −2 + 실제 서명 대체 0..2 + 실제 서명 신인 ≤15 |

표의 하한은 대체선수 미서명, 상한은 떠난 자리마다 최소계약을 제안할 수 있는 경우 각각 $3m 공개 보수 스크린과 명단 미달 가능액을 보수적으로 예약한 값이다. $3m를 실제 최소계약 급여로 선택한 것이 아니다. 원 CBA는 전년 캡 대비 매년 조정하므로 2017→2022 단일 비율로 11행의 법정 정확 반올림을 증명하지 않았다. 별도 공개 2022–23 급여표의 YOS별 보고점 ±$10을 조건부 제안 범위로 사용하고 실제 서명·정확 UPC를 인증하지 않는다. 예컨대 0YOS 일반 FA 보수 보고점 $1,017,781의 제안은 0/1YOS 세금 규칙에 따라 2YOS 보고점 $1,836,090의 보수적 상단 $1,836,100으로 에이프런 스크린을 따로 비교한다. 하한의 $0은 선수 계약이 아니라 미서명이다. RT4가 기존 서명 13명인 조합에서 둘 다 이탈하고 대체선수가 없으면 11명일 수 있어 incomplete charge I_R을 0–$3m로 별도 예약한다. 다른 유효 FA 보류 인원이 cap-count를 메울 수 있으므로 실제 I_R은 미선택이며, apron에 법정 산입된다고 주장하지 않는 보수적 전액 스크린이다. RT2·RT4의 Bradley 옵션 거절 후 FA 보류액 H_B를 권리 유지 시 normal에 별도로 더한다. 유효 권리 포기 시 H_B=0이며 실제 포기는 선택되지 않았다. 현재 공개 자료만으로 H_B의 값을 정하지 않는다.

Valentine 방출 RT3·RT4는 기존 live $2,193,930를 빼고 같은 전액 공개보수 $2,193,930를 보호급여/legacy 예약으로 되돌려 놓았다. 실제 지급·합의액 또는 방출이 확정됐다는 뜻이 아니다. Bradley 옵션 거절 RT2·RT4만 기존 live $2,036,328를 빼며, 대체 센터 q_C를 별도 더한다. 에이전트 자료에는 여섯 범주별 변환과 192×4 조건식이 JSON에 있다.

최종 표준 15자리/투웨이 2자리, 새 신인 실제 서명, CBA 권리·보류액, 추가 예외·하드캡, 모든 선수 계약·프런트 RT 선택은 미확정이다. E40 뒤 같은 자료 전달만 관측하며 새 회차·최종 기능은 0. 전체 A08/G13·원고 게이트는 닫혀 있다.

## 법규·수치 근거

- [2017 NBA–NBPA CBA, Article II §6·Exhibit C·Article VII §12(f)(2)(ii)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf): 전시즌 YOS별 최소 보수의 매년 조정과 0/1YOS 일반 FA의 2YOS 세금 기준.
- [NBA 2022–23 샐러리캡 공지](https://www.nba.com/news/nba-salary-cap-for-2022-23-season-set-at-just-over-123-million): 적용 캡연도와 공개 캡 수준.
- [2022–23 공개 최소급여표](https://www.hoopsrumors.com/2022/07/nba-minimum-salaries-for-2022-23.html): 11개 YOS 보고점. 이는 원 CBA의 공식 반올림 인증이나 개별 계약 영수증이 아니다.

세 원문 raw 바이트의 SHA-256·크기·임시 캐시 경로와 읽은 페이지/표는 JSON `raw_source_evidence`에 있다.

## 출처

- `design/A08_FINITE_FUNCTION_BATCH_2026_10_07.json` — LF SHA-256 `b84f4d08ede9015934b6d91287c21588bee9443fbaa8bf9ae6d3b1804f8c3b07`
- `research/CHICAGO_2022_COMBINED_CONTRACT_COST_MATRIX_2026_10_07.json` — LF SHA-256 `1ba9e120872bdfab40f26fe2b56a6cff8c6265d94280ea84b5970ffb0d537d33`
- `research/CHICAGO_2022_FULL_COST_ROSTER_FAMILY_2026_10_07.json` — LF SHA-256 `16830b560cf4f2008053ac236202010ff87188f42536a5d36870433933feccf0`
- `research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json` — LF SHA-256 `bf8087a89af09a817c0a3eb5d4df906a906575a56016c873912db00eccdca9db`
- `research/CHICAGO_2022_LEGACY_CARRY_REFINEMENT_2026_10_07.json` — LF SHA-256 `ec95c68e5f4fb0ae6a799f2c74705c5c733945719c740b0349bf128be6832c81`
- `simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json` — LF SHA-256 `7d3ab9d0d9e4234e728d4549616acaf84d5b57c4110603cf0114c8bf2c55b8d4`
- `tools\build_a08_s1_current_rt_cost_slot_family.py` — LF SHA-256 `322b049c52bc8acaa1b2dcde65f4cd4d4a7d3ab06041b26606c0886984b965b7`
