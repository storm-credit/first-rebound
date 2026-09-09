# O-15F11 Portland·Golden State 접전 경로

- 상태: `CLOSE_GAME_ALLOCATION_AND_SENSITIVITY_PASS / SEASON_HOLD`
- 선행 main: `e74e3da37cd91bd4bf305c494394084ddac6eca9` / PR #141
- 총괄 자체 검토: `NOT_INDEPENDENT`
- PROJECT_FREEZE v0.30 PARTIAL / DESIGN_GATE CLOSED / manuscript_allowed false

## 연결 계산 정정

O-15F10의 기준선 진단은 상대 교체 상수를 전반에 섞으면서 미지 rating을 누락했고, RAPTOR/BPM별 주인공·LaMelo prior를 scenario 하나로 덮어썼다. 전반 연전 피로를 반영하지 않았고 문서 표도 JSON과 일치하지 않았다. 따라서 이전 PASS의 수치 정확성 부분을 철회했다.

이제 O-15F9의 `pre_opponent_held_inputs`를 그대로 연결한다. 43개 전반 날짜와 29개 후반 날짜의 중복을 금지하고 같은 날짜의 후반 분기들이 상대 효과 제거 후 동일해지는지도 검사한다. 미지 상대 계수는 기준선에서 사용하지 않는다. 교체 메뉴의 모든 선수를 미지 선수로 바꿔도 기준선이 같아야 하는 회귀 검사를 추가했다. 정정된 표는 `CHICAGO_2020_21_SEASON_CONNECTION.md`에 있다.

GSW·LAL처럼 실제 제거 선수가 없는 접촉도 `LIMITED_BASELINE`로 바꾸지 않는다. 기존 18경기 접촉 중 10경기만 1:1 벡터가 있었으며 8경기는 미배정이었다. 이번에는 그중 GSW 1경기와 Portland 2경기를 실제 분 대안으로 전진시켰다.

## Portland 4개 작업안

두 날짜에 동일한 정책을 적용한다. Evans 실력은 같은 지표 안에서 한 값으로 묶고 날짜별로 유리한 값을 고르지 않는다. RAPTOR와 BPM 수치 자체를 같은 능력 단위로 간주하지 않는다.

| 안 | 1/5 Evans 분 | 1/30 Evans 분 | 판단 |
|---|---:|---:|---|
| 기존 선수 분담 | 0 | 0 | 총괄 추천 작업안. 기존 가드·윙에게 역할을 분산 |
| Evans 최대 12분 | 12:00 | 12:00 | 등록·가용성·실력이 확인될 때 비교할 보조 안 |
| Evans 최대 24분 | 18:36 | 24:00 | 양의 제거 시간 범위 안의 확대 스트레스 |
| Trent 분 전량 이전 | 18:36 | 36:42 | 종전 1:1 치환의 부담을 보여 주는 비교안 |

추천은 이번 두 경기의 조건부 분 모델에 한정한다. Evans의 방출·부상·계약 종료나 미래 무출전을 선택한 것이 아니다. 급격한 증분 분은 자동으로 같은 효율을 유지하지 않으므로 승패 모델의 한계로 남긴다.

기존 선수 분담의 정확한 추가 시간은 다음과 같다.

| 날짜 | 제거 | 추가 |
|---|---|---|
| 1/5 | Trent 18:36 | Simons +10:00, Little +8:36 |
| 1/30 | Trent 36:42 | Simons +8:00, Hood +10:00, Little +10:00, Anthony +8:42 |

1/5 Little은 실제 `DNP - Coach's Decision` 행이 있는 조건부 벤치 후보다. 1/30 McCollum·Nurkic의 부상 DNP를 추가 시간으로 복원하지 않았다. Lillard의 실제 시간도 늘리지 않았다. 1/30 Trent 선발 자리는 Simons가 맡는 조건이며 선발 5인도 증명했다. 전 선수 40분 이하는 이번 계산의 운영 상한일 뿐 의학적 허용 시간은 아니다.

## Golden State 3개 작업안

Russell–Wiggins 핵심 이동을 유지하는 공통 조건 아래 Hutchison 비활성, 12분, 24분을 비교했다. 비활성안을 후반 3/29의 기존 조건과 연결하는 작업 기준으로 추천한다. Hutchison이 실제로 어디에 등록됐는지는 아직 미확정이며, 활성안은 GSW 잔류·등록·가용성까지 가정한 스트레스다.

12분은 Oubre·Mulder에게서 각각 6분을 이전한다. 24분은 Oubre 10분·Mulder 10:34·Lee 3:26에서 이전한다. 실제 Chicago의 Hutchison 출전 여부를 다른 팀 가용성으로 복사하지 않는다.

## 양 팀 점수차

모형은 선행 pace 100 / 48분 정규화를 유지한다. `Chicago 점수차 = 상대 고정 점수차 - 상대 전력 변화`이며 상대 점수차는 정확히 반대 부호다. 표는 BASE prior·피로 0에서 추천 작업안의 계산이다.

| 날짜·상대 | RAPTOR EB | BPM 3/25 EB | 판정 |
|---|---:|---:|---|
| 12/27 GSW | +0.1699 | -0.5156 | 계열 불일치 |
| 1/5 Portland | +4.2752 | +3.6866 | 이 조건에서 Chicago 우세 |
| 1/30 Portland | +0.0995 | -0.0640 | 계열 불일치·극접전 |

12/27은 연전 둘째 날이다. 피로 0.5를 적용하면 RAPTOR -0.3718, BPM -1.0572로 둘 다 음수다. 이는 실제 피로가 0.5였다는 추정이 아니다. 1/30에 두 지표의 평균을 내거나 미소한 양수를 확정 승리로 바꾸지 않는다.

Evans 12분 안의 1/30 손익분기 rating은 RAPTOR -1.1752, BPM -1.0739다. 각 지표에서 Evans가 이 값보다 낮으면 Chicago 점수차가 양수, 높으면 음수다. 등호는 미정이다. 미래 표본이 없는 Evans를 rating 0으로 채우지 않는다. 1/5·1/30 공동 rating 구간도 JSON에 보존했으며, 이는 실제 승리 확률이나 두 날짜의 독립 선택이 아니다.

## 검증 범위와 다음

11개 분 배정(Portland 4정책×2날짜·GSW 3안), 198개 양 팀 영향 조건(11×2계열×3prior×3피로)을 검사했다. 모든 배정에 센터·볼 운반자·윙이 포함된 5인 조합 증명이 있고, 팀 총 240분·선발 조합 최소 3분·선수별 배정 시간·DNP 후보 조건을 만족한다. 조합 증명은 실제 교체 순서나 전술 우월성의 증거가 아니다. Portland의 1/5 24분 상한안과 전량 이전안은 동일 벡터이므로 11안을 모두 독립된 증거로 세지 않는다.

이번 3경기는 계산 완료, 승패 미확정으로 처리한다. 다음 O-15F12는 전반 나머지 15접촉 경기의 분 배정과 Minnesota 라이벌 계수를 같은 시즌 조건에 연결한다. 이번 두 접전의 계열 불일치는 그대로 전달하고 동일 감사를 반복하지 않는다. 최종 가용성·거래·순위·픽은 미완료다.

재현: `python tools/build_chicago_2020_21_close_games.py`; 새 분 입력을 바꿀 때만 `--write`로 조합을 재생성한다.

## 자료 계보

- 실제 분·DNP: O-15F9 `PREDEADLINE_PAIRED_OBSERVATIONS.csv`, 자료 계보 `O15F9_PROVENANCE.json`.
- 지표·성장 가정: O-15F9 `IMPACT_CROSSCHECK.json`; RAPTOR는 2021 RS 회고치, BPM은 3/25 snapshot이다. 미래 거래 협상 시점의 정보로 사용하지 않는다.
- 드래프트·거래 조건: `2018_DRAFT_28_43_EVANS_CASCADE.md`, `2021_WASHINGTON_CHICAGO_PORTLAND_TRANSACTION_CASCADE.md`.
- [NBA 공식 1/5 경기 요약](https://www.nba.com/watch/video/game-recap-bulls-111-trail-blazers-108-75e714): 실제 Chicago 111–108 Portland 기준선 확인. 이 공식 요약으로 선수별 분을 전수 검증했다고 주장하지 않는다.
