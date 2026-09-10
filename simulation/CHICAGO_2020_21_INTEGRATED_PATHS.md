# O-15F12 전반 잔여 접촉·라이벌·72경기 조건부 연결

- 기준일: 2026-09-10
- 상태: `CONDITIONAL_72_GAME_PATHS_CONNECTED / FINAL_SEASON_HOLD`
- 선행 main: `197637f762ca0b1571162b68eb7acd9928018209` / PR #142
- PROJECT_FREEZE v0.30 PARTIAL / DESIGN_GATE CLOSED / manuscript_allowed false
- 총괄 검토: `NOT_INDEPENDENT`

## 이번에 닫힌 범위

전반의 나머지 15접촉 날짜에 29개 출전 시간 배정안을 만들고 모두 5인 조합을 증명했다. 이전 O-15F11의 Portland·GSW 3경기와 합쳐 전반 18개 접촉 경기의 조건부 분 입력이 있다. 나머지 25전반 경기는 기존의 제한적 실제 상대 기준선이다.

전후반에 동일한 지표별 성장 prior·피로 정책·라이벌 실력 변수를 적용해 6개의 날짜 간 일관된 72경기 경로를 연결했다. 선수 역할 범위 2종×라이벌 24/28/32분으로 6경로이며, 각각 Chicago Porter 2조건×지표2계열×성장prior3종×피로3조건을 비교해 216개 시즌 조건이다. 각 구단의 모든 가능한 조합을 전수 탐색한 결과는 아니다.

## 잔여 상대 시간 배정

아래 분은 사실 기록이 아니라 팀 내 역할을 비교하기 위한 목표다. 같은 선수가 여러 날짜에 서로 다른 팀으로 나타나지 않도록 고정했다. 타팀에서 겪은 부상·개인 사유를 새 팀에 복사하지 않는다.

| 팀·날짜 수 | 기본 시간 / 확대 시간 | 조달·보존 |
|---|---|---|
| Washington 3경기 | Trent 24 / 28분 | Bonga 제거, Brown·Mathews·Bertans·Avdija 등의 시간을 순서대로 재배분 |
| Dallas 2경기 | Hampton 12 / 18분 | Terry 제거, Burke·Hinton·Hardaway 등의 시간 조정. 실제 Terry 16초에 고정하지 않음 |
| Charlotte 1경기 | Edwards 24 / 28분, Terry 6분 | LaMelo 제거, Caleb Martin·Bridges 시간 조정 |
| New Orleans 2경기 | Killian Hayes 16 / 20분 | Kira 제거. 2/10 잔여 분은 Alexander-Walker, 3/3 새 분은 Bledsoe·Redick·Hart에게서 조달 |
| Detroit 2경기 | Patrick/Kira 28/20분 또는30/24분 | Bey 제거, Smith Jr.·Lee·Wright 등의 분 조정 |
| Denver 2경기 | Bey 20 / 24분 | Hampton의 실제 0분을 복사하지 않고 Cancar·Green·Millsap·Barton에서 조달 |
| Lakers 2경기 | 실제 상대 분 유지 1조건 | AD·Trent 상류 연쇄와 기존 로스터 유지가 전제; 세계선 무영향 확정 아님 |
| Minnesota 1경기 | 라이벌 24 / 28 / 32분 | Edwards 제거, McDaniels·Okogie 분 조정, Towns 실제 분 유지 |

12개 날짜×2안 + Lakers2개×1안 + Minnesota1개×3안 =29안이다. 선발은 Bonga→Trent, Bey→Patrick, Edwards→라이벌로 필요한 자리만 이전한다. 확대 시간은 더 좋은 결과를 보장하지 않으며 건강상 허용 시간도 아니다.

분석용 팀 시간에서 관측 잔차 ±1초만 보정하고 원자료 총초·보정 대상·보정량을 함께 저장했다. Minnesota 2/24와 Denver 3/19는 실제 연장 구간인 53분, 팀 합계265분을 유지한다. 대체 세계에서도 반드시 연장전이 열린다는 사건 승인은 아니다.

역할 제약상 센터 공백을 남기지 않도록 Denver 3/1 Hartenstein +39초, Minnesota 2/24 Naz Reid +7초를 배정하고 같은 팀 다른 시간으로 보전했다. 이는 자료 오기 정정과 구분된 모형상 시간 이동이다. Nnaji를 전업 센터로 바꾸거나 명단에 없는 Russell에게 출전을 주지 않는다.

## 거래 조건의 일관성

공통 조건은 Chicago Theis·Green 승인 경로, Portland의 Trent 부재·기존 선수 분담, GSW의 Wiggins 핵심 이동 유지·Hutchison 비활성, Powell의 Toronto 잔류, Gordon A의 Harris/Nnaji 이동·Vučević Orlando 잔류·Hall 가용성, Fournier의 Orlando→Boston 이동이다. Chicago A 이외의 거래·등록·가용성은 조건부다.

Fournier의 Boston 미합류안은 이번 72경기 경로에서 제외했다. 기존 Orlando 입력은 Fournier 이탈을 가정하므로, Boston행을 없애면서 새 행선지나 Orlando 잔류 분을 계산하지 않으면 불완전한 거래 조합이 된다. 선행 O-15F8/O-15F9의 단일 경기 비교안은 이력으로 보존한다.

기본·확대 시간별 Charlotte Edwards/Terry, Detroit Patrick/Kira 정책을 전후반에 연결했다. 라이벌 24/28/32분도 두 Minnesota전에 같은 정책을 적용한다. Portland의 Evans 활성 대안과 GSW Hutchison 활성 대안은 O-15F11에 남아 있으며 이번6경로의 범위 밖이다.

## 조건부 시즌 수치

표는 72경기에서 Chicago 점수차가 양수인 경기 수다. 라이벌은 O-15F9에 저장한 지표별 리그 관측 범위 전체에서 한 값을 두 날짜에 함께 적용한다. 이 범위는 라이벌의 승인된 실력·확률 분포·절대 상하한이 아니다. 정확0인 경계는 미정으로 별도 기록하며 패배로 세지 않는다.

| 지표 | 성장 가정 | 조건부 양수 경기 수 |
|---|---|---:|
| RAPTOR_RS_EB | LOW | 30~31 |
| RAPTOR_RS_EB | BASE | 32~33 |
| RAPTOR_RS_EB | HIGH | 35 |
| BPM_MAR25_EB | LOW | 30~31 |
| BPM_MAR25_EB | BASE | 31 |
| BPM_MAR25_EB | HIGH | 36 |

**BASE 중심 후보는31~33승에 해당한다.** LOW/HIGH를 포함한30~36을 전체 세계선의 최종 성적 범위로 해석하지 않는다. 이것은 명시된6경로·가용성 가정·회고적 영향 지표·선형 시간 환산의 조건부 산출물이다. 상대 전술 적응과 역할 확대에 따른 효율 변화도 확정하지 않았다. 실제 시즌 기록·순위·플레이인·픽은 아직 선택하지 않는다.

예시 작업 조건(기본 시간·라이벌28분·Porter ZERO·BASE·피로0.5)에서는 RAPTOR32, BPM31이다. 이 예시의 RAPTOR은 실제 Chicago 기록 대비 +1승, 상대 Portland -1승으로 상쇄된다. BPM은 양쪽 변화0이다. 각 rating 구간마다 Chicago 승수 변화와 상대 팀별 변화 합계가0인지 검사했으며, Chicago가 이기면서 상대도 이기는 이중 집계는 없다. 이는 Chicago와 맞붙은 경기의 이전량뿐이며 타팀 전체 시즌 재계산은 아니다.

GSW 12/27과 Portland 1/30의 두 지표 부호 차이는 남겼다. 지표를 평균내서 미세한 양수를 승리로 고르지 않는다. 기존 원장의 전반19~21승은 다른 입력 단계의 역사적 결과이며 이번값과 평균내지 않는다.

## 라이벌과 다른 미지 선수

라이벌의 rating은 두 Minnesota전의 유효 영향력을 나타내는 동일한 변수다. Towns·Russell과의 창조 역할 조정 비용을 제외한 순수 재능 수치라고 부르지 않으며 추가 시너지 보너스를 더하지 않는다. 역할 비용 자체를 실측한 것도 아니다.

위 예시 조건의 Chicago 점수차는 RAPTOR에서 2/24 `6.35970825 − (28/48)r`, 4/11 `−5.65204183 − (28/48)r`다. 저장된 후반 계수는 선행 원장의 소수 반올림을 유지한다. 손익분기는 각각 약10.9024와−9.6892이며 해당 리그 관측 범위 안에서는 Chicago가 전반전 양수·후반전 음수다. BPM에서도 이 예시의 부호는 같다. 더 높은 신인 능력이나 역할 가정은 새로운 입력이지 현재 상한 밖이라는 이유로 불가능한 선수가 아니다.

BPM snapshot에 없는 Hall·Riller·Langford를0으로 채우지 않았다. 이번 포함 경로의 Hall·Riller는 기존 리그 관측 범위 전체에서도 각 해당 경기 부호가 변하지 않음을 별도 구간으로 검산했다. Langford가 포함된 Boston 미합류안은 위 거래 불완전성 때문에 통합 범위에서 제외됐다. 표본이 없는 선수의 영향이 영원히 중요하지 않다는 뜻은 아니다.

## 재현·종료 조건

- `python tools/build_chicago_2020_21_integrated_paths.py`: 저장된29개 조합 증명과522개 상대 영향 입력,6개 72경기 경로·216개 시즌 조건 검증.
- `python tools/test_chicago_2020_21_integrated_paths.py`: 공유 rating에서 불가능한 승리 조합 방지,0점 경계 처리,미지선수 구간 부호 반전 거부,상대 승수 이전 방향 검증.
- 새 선수 분을 바꿀 때만 `--write`로 새 조합을 생성한다.

O-15F12의 잔여15경기 조건부 분·양 팀 영향·72경기 경로 연결은 완료했다. 새 입력 없이 동일 분 감사를 반복하지 않는다. 다음 O-15F13은 **시즌 결산·순위·픽 영향 보드**다.31/32/33 중심 후보의 차이가 나는 날짜와 상대 승수 이전량을 사용하고, 남은 실제 거래·가용성 선택과 리그의 다른 경기 파급을 구분한다. 작가의 최종 시즌 선택 전에 비교 가능한 결산 보드를 먼저 완성한다.

자료는 O-15F9 `PREDEADLINE_PAIRED_OBSERVATIONS.csv`와`O15F9_PROVENANCE.json`, 지표 입력`IMPACT_CROSSCHECK.json`, O-15F11`CLOSE_GAME_PATHS.json` 및 각 드래프트/거래 정본이다. 새 수치·변경 없는 기존 조합을 독립 증거로 재집계하지 않는다.
