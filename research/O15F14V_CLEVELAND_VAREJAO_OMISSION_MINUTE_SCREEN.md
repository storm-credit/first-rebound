# O-15F14-V — Cleveland Varejão 영입 생략안의 5경기 분 검문

- 기준: `main` `727d733` / PR #277 병합 뒤. 선행 [Cleveland 5월 추가 자리](O15F14U_CLEVELAND_VAREJAO_HARDSHIP_F5.md)의 **C2 후보만** 검산한다.
- 판정: `FIVE_GAME_MINUTE_OBSERVED / CONDITIONAL_LINEUP_AND_LOCAL_RATING_PASS / HEALTH_AND_SEASON_HOLD`.
- 재현: [C2 화면 JSON](../simulation/CLEVELAND_2020_21_VAREJAO_OMISSION_SCREEN.json), [`screen_cleveland_varejao_omission.py`](../tools/screen_cleveland_varejao_omission.py). Windows에서는 종속 기존 도구의 기본 텍스트 읽기를 위해 `PYTHONUTF8=1`로 실행한다.
- 작가 확정은 3/25 McGee–Hartenstein 거래 **생략**까지다. Varejão 영입 생략, 분 배분, 건강, 최종 승패는 확정되지 않았다.

## 원역사 5경기와 대체 분 부담

출전 초는 NBA 공식 경기책의 **최종 박스**에 맞춘다. 같은 PDF에 분기별 박스가 반복되고 PDF 텍스트 추출은 이름·숫자 열을 어긋나게 놓기도 하므로, 첫 페이지의 최종 박스와 [NBA 선수별 경기 목록](https://www.nba.com/stats/player/2760/boxscores?Season=2020-21&SeasonType=Regular+Season)을 교차 대조했다. 분기별 Varejão 합계를 최종 출전 시간으로 읽지 않는다.

| 대체 세계 K1 경기 ID | 공식 경기책 | 원역사 Varejão | 기존 F5 선택 화면의 McGee 조건부 분 | C2에서 Varejão 분을 모두 McGee에게 줄 때 | 원역사 결과 |
|---|---|---:|---:|---:|---|
| `2021-05-05_CLE_POR` | [5/5 POR–CLE](https://statsdmz.nba.com/pdfs/20210505/20210505_PORCLE_book.pdf) | 6:37 = 397초 | 12:50 = 770초 | **19:27 = 1,167초** | CLE 105–141 POR |
| `2021-05-07_DAL_CLE` | [5/7 CLE–DAL](https://statsdmz.nba.com/pdfs/20210507/20210507_CLEDAL_book.pdf) | 4:37 = 277초 | 12:35 = 755초 | **17:12 = 1,032초** | CLE 90–110 DAL |
| `2021-05-09_CLE_DAL` | [5/9 DAL–CLE](https://statsdmz.nba.com/pdfs/20210509/20210509_DALCLE_book.pdf) | 16:23 = 983초 | 기존 화면 없음 | **16:23 = 983초** | CLE 97–124 DAL |
| `2021-05-12_CLE_BOS` | [5/12 BOS–CLE](https://statsdmz.nba.com/pdfs/20210512/20210512_BOSCLE_book.pdf) | 3:12 = 192초 | 기존 화면 없음 | **3:12 = 192초** | CLE 102–94 BOS |
| `2021-05-14_WAS_CLE` | [5/14 CLE–WAS](https://statsdmz.nba.com/pdfs/20210514/20210514_CLEWAS_book.pdf) | 5:07 = 307초 | 기존 화면 없음 | **5:07 = 307초** | CLE 105–120 WAS |

Varejão 출전 합계는 **2,156초 = 35:56**. 5/5·7의 397+277=674초는 기존 [McGee 거래 생략 화면](../simulation/DENVER_2020_21_MCGEE_NONTRADE_SCREEN.json)의 Hartenstein→McGee **770+755초와 별도**다. 따라서 그 화면의 14경기·50개 평점 비교는 C2 전체의 검산이 아니다. 5경기에서 원역사 Varejão 분을 모두 McGee에게 주는 단일 후보는 기존 1,525초와 새 2,156초를 합쳐 **3,681초 = 61:21**의 McGee 조건부 출전이다. 5/5·7 두 경기의 조건부 McGee 분은 각각 19:27·17:12로 48분 상한 안에 있다. 이는 5인조 동시성, 출장 가능, 연속 경기 체력, 경기 결과를 증명하지 않는다.

## C2 국소 화면 결과

도구는 위 다섯 `OBSERVED_HELD` 선수별 초에서 Varejão를 빼고, 5/5·7에만 Hartenstein도 빼며, 두 선수의 초를 McGee에게 준다. 원래 선발 5명은 유지하고 기존 F5의 Cleveland `handler/center/wing` 역할 정의를 적용했다. 5인조 선형계획 해는 **5/5경기 존재**했다. 각 선수 분 합계와 매 경기 총 240분을 충족한다. 이 해는 실경기 교체 순서나 건강 승인 기록이 아니다.

| 경기 | RAPTOR 조건부 승패 방향 | BPM 조건부 승패 방향 | 주의 |
|---|---|---|---|
| 5/5 POR | 원역사 CLE 패 방향 유지 | 유지 | 전날 경기로 인한 국소 피로 조정 포함 |
| 5/7 DAL | 원역사 CLE 패 방향 유지 | 유지 | 원역사 Hartenstein 분도 이동 |
| 5/9 DAL | 원역사 CLE 패 방향 유지 | 유지 | 기존 F5 화면 밖 첫 경기 |
| 5/12 BOS | 원역사 CLE 승 방향 유지 | 유지 | BPM 홈 점수차 범위 **+7.49~+8.20**, 실제 +8 |
| 5/14 WAS | 원역사 CLE 패 방향 유지 | 유지 | 기존 F5 화면 밖 마지막 경기 |

따라서 **5경기×2방법=10/10 방향 유지**는 이 단일 분 배분과 원역사 점수차 기준의 **국소 감도 결과**다. BPM 3/25 스냅샷에 Varejão 평점이 없어 다섯 경기 모두 경험적 리그 범위로 묶은 구간이다. 후보 점수차 범위가 0을 가로지르지 않았어도 그 구간은 선수 예측치나 최종 승패 보증이 아니다.

[F14F 전체 리그 조건부 화면](../simulation/NBA_2020_21_FULL_SEASON.json)의 해당 다섯 경기 점수차 구간에도 C2의 국소 변화 구간을 **구간 덧셈의 바깥 경계**로 적용했다. 그 화면에 이미 반영된 상대팀 조건부 입력을 보존한 보수적 합에서 두 평점법 **10/10 방향 유지**다. 5/12의 가장 가까운 승리 구간은 BPM 홈 **+7.49~+8.20**이고, 나머지 네 경기 구간도 0에서 떨어진다. 이는 F14F의 이미 열린 거래·가용성 가정과 C2 분 가정을 결합한 수치 경계일 뿐 K1의 완전한 새 시즌 재실행이 아니다. 새 건강/감독 선택·후속 거래가 생기면 재계산해야 한다.

## 아직 닫히지 않은 경계

1. 5/9·12·14에 기존 F5 화면 행이 없는 이유는 원역사 Cleveland의 Hartenstein **출전 분을** 치환한 화면이기 때문이다. McGee 대체 건강·감독 선택을 0분 또는 자동 출장으로 확정할 수 없다.
2. C2라면 Varejão 5/4 및 후속 계약 사건을 생략한다. [선행 등록 검문](O15F14U_CLEVELAND_VAREJAO_HARDSHIP_F5.md)의 5/4 일반 15+투웨이 2는 다른 계약 사건을 보존한 **조건부 자리 산술**이다. 5월 전체 날짜별 등록·급여와 선수별 건강을 다시 연결해야 한다.
3. 위 표의 원역사 점수는 새 세계 점수나 승패가 아니다. 5경기 국소 5인조·두 평점법 방향과 **F14F 기존 상대팀 조건부 구간과의 보수적 합**은 검산했지만, 5/12 Cleveland 승리의 8점 차를 포함한 **새 건강·거래 파급과 전체 K1 시즌 원장**을 다시 계산하기 전에는 K1 승수 불변을 말할 수 없다.
4. C1 Varejão 유지도 별도 후보로 남는다. C1은 대체 세계 hardship 허가·부상 예후가 미확정이고, C2는 분/체력·성과·계약 파급이 미확정이다. 어느 쪽도 작가 선택 요청을 보낼 만큼 비교 비용이 완성되지 않았다.

**사실:** 공식 5경기 박스의 원역사 출전 시간·점수, 기존 화면의 5/5·7 조건부 McGee 초. **추론:** 같은 다른 분을 보존하고 Varejão만 빼면 2,156초 재배정이 필요하다. **후보:** C2의 McGee 단독 흡수 5경기와 10개 국소 방향 유지. **작가확정:** McGee 거래 생략 방향만. F5·A1·K 등록/거래/시즌 `HOLD`; F 전체 `0/5`, A 최종 `0/3`, K 종료 `0/4`. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`.
