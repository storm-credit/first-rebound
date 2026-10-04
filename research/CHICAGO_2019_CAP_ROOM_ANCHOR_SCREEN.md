# Chicago 2019 cap-room 앵커의 조건부 수치 검문

2026-10-04 후속 [실제 캡 공간 취득 시점의 예외 산입 경계](CHICAGO_2019_ROOM_ACQUISITION_BOUNDARY.md): Satoransky 취득이 적법한 §6(j)(2) 캡 공간 실행으로 닫히면 직전 산입액을 유한하게 좁히는 조건부 경로다. I§1(kkk)의 일반 Room과 실제 캡 차액을 구분한다. 거래 수단·수취 Salary·전체 당일 상태는 아직 HOLD이며 아래 부분합·R/Δ를 0이나 실제 실행으로 승격하지 않는다.

2026-10-03 기준 main `6aa84ff68910068f10c426e58a9ef7ce34edf1ed`. S2의 CHI_TEAM_SALARY 잔여를 기존 승인된 2019 영입 시점부터 유한하게 추적하는 조사다. **전체 R 상한 인증이 아니며 법적12행 HOLD 유지**. [수치·출처 원장](CHICAGO_2019_CAP_ROOM_ANCHOR_SCREEN.json).

## 확인한 근거

- **사실:** [NBA 2019 Chicago 전망](https://www.nba.com/30teams30days/2019/chi)은 캡 공간 사용과 Young·Satoransky 영입을 기술한다. 거래일 차지 표는 아니다. [2019 캡 발표](https://www.nba.com/news/nba-salary-cap-2019-20-season-set-10914-million)의 캡은 $109,140,000이다.
- **사실:** [NBA 7/1 QO 안내](https://www.nba.com/news/guide-qualifying-offers-options-2019)는 6/30 기준 Arcidiacono 제안을 확인한다. 7/7 지속·금액은 인증하지 않는다.
- **2차 원역사 입력:** [Hoops Rumors 4/23 집계](https://www.hoopsrumors.com/2019/04/2019-nba-offseason-salary-cap-digest-chicago-bulls.html)의 보장10인 $81,055,004·Asik 포함액 $3,000,001·Hutchison $2,332,320·Arc 제안 예상액 $1,818,486을 사용한다. 이 페이지의 예상 캡/White 보류액을 확정 입력으로 복사하지 않는다.
- **2차 계약 이력:** [Young](https://www.salaryswish.com/players/thaddeus-young)의 7/6·2019 기본급 $12,900,000, [Satoransky](https://www.salaryswish.com/players/tomas-satoransky)의 7/7·기본급 $10,000,000을 대조했다. [Arcidiacono](https://www.salaryswish.com/players/ryan-arcidiacono) 이력은 QO $1,878,854 / hold $1,620,564로 달라, 4월 예상액을 7/7 실제 금액으로 올리지 않는다.
- **기존 승인:** [2019 명단 연구](CHICAGO_2019_20_ROSTER_MINUTE_BASELINE.md)의 White #7 및 영입 유지 범위를 재사용한다. 주인공의 정확 순번·연도별 급여를 새로 선택하지 않는다.

## 계산과 반례

P2는 주인공 2019–20 급여, P3는 2020–21 급여다. Asik 제거·당시 계약 차지 유지·Satoransky의 cap-room 취득 등 아직 미인증 전제를 적용한 탐색이다.

| 항목 | Arc 4월 예상액을 넣은 탐색 | Arc 항목을 제외한 넓은 탐색 |
|---|---:|---:|
| 7/7 알려진 부분합(P2 제외) | $105,748,289 | $103,929,803 |
| cap+$100,000에서 뺀 잔여(P2 제외) | $3,491,711 | $5,310,197 |
| 기존 2020–21 부분합+Young 보너스+캠프3명 전액을 연결한 상수 | $131,676,740 | $133,495,226 |
| #16 P2 80% / P3 120%, Δ=0 가상 시험 | $132,842,140 | $134,660,626 |
| 세금선 $132,627,000 대비 초과 | $215,140 | $2,033,626 |

부분합은 `81,055,004−3,000,001−2,332,320+5,307,120+12,900,000+10,000,000(+1,818,486)`이다. White 입력은 새로 읽은 [계약 이력](https://www.salaryswish.com/players/coby-white)의 비교값이며 거래일 적용 상태는 미인증이다. 7/8 Gafford나 7월 중순 계약을 앞당겨 빼지 않는다. Asik 제거액을 2020 R에서 다시 차감하지 않는다.

연결 식은 `상수+(P3−P2)+Δ`이며 Δ는 이월 차지의 증가/재진입과 이후 미포함 사건이다. **Δ=null**. 표의 Δ=0은 반례를 위한 가상 대입이며 실제 0 인증이 아니다. 캠프 $4,372,601도 기존 연간 전액 스트레스이며 전체 부상/분쟁 의무의 법적 상한이 아니다.

[2018 신인 스케일](https://basketball.realgm.com/nba/info/rookie_scale/2019)의 #16 P2 scale100% $2,549,000·P3 $2,670,500을 각각80%·120%로 넣었다. P2=$2,039,200, P3=$3,204,600. 두 해를 무단으로 같은120%에 묶으면 첫 열이 $131,822,540으로 내려간다. 이 축소를 전체 도메인 증인으로 사용할 수 없다. #16은 기존16~30 보수적 시험 범위이며 Chicago 지명권/서사 채택이 아니다.

## CBA에서 확인한 이월 경계

[NBA July 2017 CBA PDF](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf)를 직접 내려받아 텍스트를 대조했다. SHA256 `66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a`, 633쪽. 기존 NBPA PDF와 구판 위치를 소급 교체하지 않는다. 아래 PDF 쪽은 **1기준**이며 시각 대조는 이번 NOT_RUN.

- VII §6(j)(2), 인쇄212 / PDF234: cap 아래 팀의 계약 수취는 Room+$100,000 경계. 이는 이번 2019 앵커 후보의 규칙이며 2020 코로나 수정 전문을 회수한 것이 아니다.
- VIII §1(c)(i), 인쇄272 / PDF294: 첫 두 시즌·첫 옵션연도의80~120% 범위는 연도별 개별 협상이다. 동일 비율을 자동 강제하지 않는다.
- VII §4(e)(3), 인쇄189 / PDF211: 특정 시즌 서면 제외된 미서명1R도 다음 July1 재산입될 수 있다. 2019 현재 차지가0이었다는 사실만으로 2020 권리가 없다고 할 수 없다.

**추론:** 이미 승인된 2019 앵커의 당시 알려진 부분합과 이후 추가 사건을 연결하는 접근은 유한하다. **후보:** 7/7 QO·차지와 제외 권리/미래채무·이후 변경을 닫은 뒤 S2 상한 증인으로 재검문한다. **작가확정:** 이번 신규0. `R=null`, `Δ=null`, F0/5·A0/3·K0/4·미완료6·PARTIAL/CLOSED·원고0 유지.

검수와 도구 회수 범위는 [이번 검토](../reviews/CHICAGO_2019_CAP_ANCHOR_REVIEW.md)에 기록한다.

후속 [Arc 차지 네 분기](CHICAGO_2019_ARC_CHARGE_DOMAIN.md)는 NBA작성2019 최소급여표의2YOS $1,620,564와 유효QO분기 $1,820,564 하한을 연결한다. 위4월예상액 탐색은 기존이력이며 실제당일값으로승격하지 않는다. 모라토리엄협상보도와사후통지급여를구분해Arc/Kornet에같은규칙을적용한다. 전체R/Δ상한은여전히null이다.
