# O-15G15AR — 8월 Detroit 실명 선수 이탈의 미충원 차지와 9월 거래 경계

- 기준: `main` `b71f590`, [G15AQ 세 계약 누적 부족](O15G15AQ_DETROIT_LEE_CAP_ROOM_AND_NONBIRD_ROUTE.md)과 [G15AF 개막 명단](O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.md). 판정: `NAMED_EXIT_THRESHOLD_ONLY / COUNTERPARTY_AND_PICK_HOLD / SEPT_TRADE_NOT_AUG_RELIEF`.
- Chicago 2020–21 정확 시즌이 진행 중이며 Detroit 2021–22는 조건부 미래 검증이다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, 신규 작가확정 0건.

## 원역사 시간 경계

[NBA 2021 거래 추적표](https://www.nba.com/news/2021-offseason-trade-tracker)와 [9월 Nets–Detroit 기사](https://www.nba.com/news/nets-trade-deandre-jordan-to-pistons)는 **9/4**에 Detroit가 Sekou Doumbouya·Jahlil Okafor를 내주고 DeAndre Jordan, 2022·2024(WAS)·2025(GSW)·2027의 2라운드 픽 네 장과 현금을 받았다고 기록한다. [SalarySwish Jordan 계약표](https://www.salaryswish.com/players/deandre-jordan)는 2021–22 원계약 급여 후보 `$9,881,598`, 뒤의 9/7 바이아웃 잔여 cap hit 후보 `$7,875,533`을 싣는다. 두 선수의 [G15AJ 급여 후보](O15G15AJ_DETROIT_AUG6_NAMED_SALARY_LEDGER.md)는 합계 `$5,743,703`이다. 이 2차 금액을 그대로 비교하면 Jordan 수취 순간 급여가 `$4,137,895` **증가**, 뒤의 바이아웃 잔여와만 비교해도 `$2,131,830` **증가**한다. 현금·픽의 가치와 Team Salary 감소를 혼동하지 않는다. 바이아웃 금액/시각을 8/6에 소급한 실제 사건으로 주장하지 않는다.

[NBA 거래 추적표](https://www.nba.com/news/2021-offseason-trade-tracker)는 이후 **10/6 Brooklyn→Houston**에서 Sekou와 2024년 2라운드 픽을 Houston에 보내고 Brooklyn이 현금을 받은 사실도 기록한다. [Basketball-Reference Houston 거래표](https://www.basketball-reference.com/teams/HOU/2022_transactions.html)는 그 픽을 **Brooklyn 자체 2024년 2라운드 픽**이라고 분류한다. 9/4 Detroit가 받은 **Washington 경유 2024 픽과 동일하다고 할 수 없다**. [HoopsRumors 당시 기사](https://www.hoopsrumors.com/2021/10/nets-trading-doumbouya-to-rockets-acquiring-sumner-from-pacers.html)는 Houston 지급 현금을 `$110,000`, Brooklyn 송출 픽을 비보호라고 전하지만 둘 다 2차 보도 수치다. 이는 **다른 팀이 다른 시점에 픽을 붙여 선수 계약을 송출한 원역사 사례**일 뿐이다. P0-B Detroit가 8/6 Houston과 거래했다는 증거도, 당시 Houston의 수용 가능 캡/예외나 Detroit의 해당 픽 보유 증거도 아니다. 9월 Brooklyn 거래가 달라지면 그때 받은 픽 네 장과 Jordan/바이아웃, 10월 Houston 거래의 출처도 다시 연결해야 한다.

Jordan의 `$9,881,598`은 **9/4 수취 순간** 원계약 후보이고 `$7,875,533`은 **9/7 바이아웃 뒤** 잔여 후보로 서로 다른 시점이다. 전자를 9/4 비교에, 후자를 바이아웃 뒤 비교에만 사용한다. 어느 금액도 8/6에 실제 존재했다고 놓지 않는다.

## P0-B에서 순급여 0인 가상 이탈의 조건부 산술

[G15AP](O15G15AP_SABEN_LEE_HOLD_AND_SEQUENCE_CORRECTION.md) 기준 Olynyk 이전 P0-B는 **12명·미충원0·명목 room `$12,361,772`**다. 아래 시험은 기존 계약 중 Sekou `$3,613,680`, Okafor `$2,130,023`을 8/6 Olynyk보다 **먼저** 내보내고 **돌아오는 선수 급여·보장 잔액 0**이라고 가정한다. 각 선수 이탈 때 12명 아래로 떨어진 자리에 0년 경력 최저급 후보 `$925,258`의 미충원 차지를 즉시 넣고, Olynyk·Lyles 새 표준계약 때 한 자리씩 제거한다. Lee·Frank는 기존 FA/QO 금액의 **교체**라 인원은 늘지 않는다. 이것은 거래 상대·픽·현금·예외 적격성을 전혀 통과시키지 않은 수학적 **상한형 이탈 시험**이다.

이 표의 입금 급여는 Olynyk 첫해 `$12,195,122`, Lee FA Amount `$925,258`→계약 `$1,489,065`(순증 `$563,807`), Lyles 첫해 `$2,500,000`, Frank QO `$1,939,350`→계약 `$3,000,000`(순증 `$1,060,650`)이다. 모두 [G15AJ/G15AQ의 2차 수치](O15G15AQ_DETROIT_LEE_CAP_ROOM_AND_NONBIRD_ROUTE.md)이며 공식 계약 원본은 아니다.

| 8/6 Olynyk 전 가상 이탈 | 이탈 직후 인원/미충원 | 이탈 직후 room | Olynyk→Lee→Lyles 뒤 room | 후속 Frank QO→`$3m` 뒤 room |
|---|---:|---:|---:|---:|
| 없음 | 12/0 | `$12,361,772` | `-$2,897,157` | `-$3,957,807` |
| Sekou만 | 11/1 | `$15,050,194` | `+$716,523` | `-$344,127` |
| Okafor만 | 11/1 | `$13,566,537` | `-$767,134` | `-$1,827,784` |
| Sekou+Okafor | 10/2 | `$16,254,959` | `+$2,846,546` | `+$1,785,896` |

Sekou 단독 이탈은 **세 계약까지만** 명목 부족을 없애며 Frank까지 같은 cap room 수단으로 잇는 시험은 `$344,127` 부족이다. 두 선수의 급여 합을 이탈 직후 room에 한 번에 더하는 계산은 틀리다. 직후에는 미충원 차지 최대 두 자리 때문에 순 개선이 작고, Olynyk/Lyles를 실제로 서명하면 그 차지가 순서대로 제거된다. 이 표의 양수는 다른 FA Amount·예외·인센티브·보장급이 없고 각 거래가 허용된다는 증거가 아니다.

## 거래·인물·장기 연쇄의 미해결 비용

1. **거래 상대와 대가:** 순급여 0 수취자가 누구인지, 그 팀의 8/6 cap room/트레이드 예외/로스터 자리, Detroit가 내줄 보호 조건 있는 실제 픽을 아직 특정하지 못했다. 10/6 Houston 사례의 픽을 그대로 복사하지 않는다.
2. **원역사 9월 경로:** Sekou 또는 Okafor가 이미 이탈했다면 Brooklyn의 **두 선수 수취**·Jordan/픽 네 장/현금 원거래를 그대로 복제할 수 없다. [G15AF](O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.md)의 조건부 개막 16명도 이 새 거래로 처음부터 재계산해야 한다.
3. **농구 비용:** Sekou·Okafor의 포워드/센터 자리와 앞코트 분, Charlotte가 Plumlee를 받지 못하는 원역사 분기, Olynyk·Stewart 및 2022-01-23 Detroit 경기의 등록/가용성·상대 생산성은 이 cap 산술로 해결되지 않는다.
4. **후속 계약:** Livers와 Diallo, 8/10 Joseph room MLE, 기타 FA/예외·방출 보장액까지 잇는 완전 Team Salary는 `HOLD`다.

## 검증 레이어

| 단계 | 실제 관측과 한계 |
|---|---|
| Antigravity CLI | `read_url_content→view_file`로 NBA의 9월 Jordan 거래 기사 **본문을 회수**, 실제 날짜·선수·픽 네 장·현금을 확인. 8월 가상 거래의 증명은 아니다. |
| NotebookLM CLI | 업로드된 2017 CBA PDF **한 출처**에서 Article VII §4(f)의 12명 미달 차지와 선수 송출·새 서명 때의 인원 변화를 재독했다. 거래 상대/2021 Detroit 사실은 이 문서에 없다. |
| Codex | NBA 거래 원문과 2차 급여를 분리하고 [JSON](O15G15AR_DETROIT_NAMED_EXIT_AND_ROSTER_CHARGE.json)·[검사기](../tools/check_o15g15ar_detroit_named_exit.py)로 사건별 인원·미충원 차지를 계산했다. |
| Claude | [문서 단독 반증](../reviews/R01_O15G15AR_NAMED_EXIT_BLIND.md)을 별도 판정한다. |

**사실:** NBA가 기록한 9/4·10/6 거래의 날짜·선수·픽 방향, CBA의 미충원 차지 규칙. **추론:** 명시한 P0-B/2차 급여/순급여 0 이탈 가정의 표 산술. **후보:** 8/6 실제 수취팀·픽 대가·미보장액·전체 cap 장부·로스터/분 대체. **작가확정:** 0건.

다음은 8/6 이전 거래 수취팀과 픽·트레이드 예외/로스터 자리를 **이름·날짜·계약**으로 입증하거나 다른 실명 경로를 제시하는 것이다. 확인 전에는 P0-B를 같은 8/6 세 계약과 9월 Nets 거래/개막 명단까지 연속 실행할 수 있다고 판정하지 않는다. Chicago 정확 시즌과 G14/G16/G17은 `HOLD`; 전체 7행 1완료·1진행·5대기, 남은 큰 작업 6개.
