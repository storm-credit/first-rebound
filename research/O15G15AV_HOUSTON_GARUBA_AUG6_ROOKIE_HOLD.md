# O-15G15AV — Houston 8/6 Garuba 지명 순번·급여 경계

- 기준: `main` `9a7c4a8`, [G15AT 별도 예외](O15G15AT_HOUSTON_SEPARATE_HARDEN_EXCEPTION_SCREEN.md)와 [G15AU Detroit 대가](O15G15AU_DETROIT_AUG6_CONSIDERATION_LEDGER.md). 판정: `DB1_PICK_21_HOLD_PRESSURE / HOUSTON_AUG6_TEAM_SALARY_HOLD`.
- 범위: Detroit→Houston Sekou **가상** 2021-08-06 거래의 Houston 수취 비용. Chicago 2020–21 정확 시즌이 선행 미완료이며 이 문서는 조건부 2021–22 연구다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, 작가확정 0건.

## 날짜와 지명권을 분리

| 층위 | 확인된 입력 | 8/6 장부에서의 의미 |
|---|---|---|
| 원역사 드래프트 | [NBA 공식 2021 결과](https://www.nba.com/news/2021-nba-draft-results-picks-1-60)에서 Houston은 Garuba를 **23번**에 지명했다. | 원역사 23번은 대체 드래프트 순번이 아니다. |
| 조건부 DB1~DB4 | [G6 1라운드 비교](../simulation/NBA_2021_FIRST_ROUND_CONTINUATION.md)의 추가 거래 제한안은 Houston이 Garuba를 **21번**에 지명한다. [전체 비교 JSON](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.json)도 같다. | 채택되지 않은 21번 후보. Houston의 8/6 팀 급여를 원역사 23번으로 복사하면 비용을 낮춰 잡는다. 다른 드래프트 거래를 채택하면 이 입력부터 재계산한다. |
| 원역사 계약 시간 | [Houston의 Green 8/5 계약 발표](https://www.nba.com/rockets/news/rockets-sign-jalen-green)와 [Garuba 8/16 계약 발표](https://www.nba.com/rockets/news/rockets-sign-usman-garuba)는 서로 다른 시점이다. [Houston 8/6 Summer League 명단](https://www.nba.com/rockets/news/rockets-announce-roster-nba-summer-league-2021)은 NBA 표준 계약 명단이 아니다. | 원역사 Garuba의 **8/16** 서명은 대체세계의 서명일로 고정할 수 없다. 원역사 8/6 미서명 상태를 대체세계 무비용으로 해석하지 않는다. |

[2017 NBA–NBPA CBA Article VII §4(e)(1)–(3)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)는 1라운드 지명 직후 권리 보유 팀의 Team Salary에 해당 순번 스케일 **120% hold**를 넣는다. §4(e)(2)의 해외팀 계약 제외는 계약일과 **정규시즌 첫날 중 늦은 날**부터 적용되므로 단순한 Real Madrid 경력만으로 2021-08-06 hold를 0으로 만들지 못한다. §4(e)(3)의 당해 시즌 미서명 선택에는 팀·선수의 서면 절차가 필요하며, 대체 Houston이 이를 했다는 자료도 없다. 서명했다면 hold 대신 **실제 NBA 계약 급여**를 넣는다. 따라서 8/6 조건부 장부의 분기는 `미서명 hold / 실제 계약 급여 / §4(e)(3) 서면 제외`이고, 세 번째를 사실로 전제하지 않는다.

## 21번과 23번의 크기: 검토용 2차 표

[RealGM 2021–22 rookie scale](https://basketball.realgm.com/nba/info/rookie_scale/2022)의 첫해 100% 금액은 21번 `$2,127,700`, 23번 `$1,961,100`이다. 같은 표의 **120% 작업상 계산**은 21번 `$2,553,240`, 23번 `$2,353,320`, 차이 `+$199,920`이다. 이는 순번만 바꿔 본 민감도이며 **NBA의 실제 Houston Team Salary 원장이나 계약서가 아니다**. [다른 2차 전재](https://www.kentucky.com/sports/college/kentucky-sports/ex-cats/article253001143.html)는 21번 첫해 스케일을 `$2,127,600`으로 적으므로 정확 달러 단위는 공식 2021–22 scale/리그 장부가 확보될 때 재검산한다. 현재 안전한 크기 판정은 **약 `$0.20m` 증가**다. 나머지 신인 Green·Şengün·Christopher의 권리/계약 시점과 다른 거래 급여까지 합친 8/6 Team Salary는 아직 미완성이다.

이 추가 비용은 [G15AT의 Harden 예외 후보 `$5,019,920 − $3,613,680 = $1,406,240`](O15G15AT_HOUSTON_SEPARATE_HARDEN_EXCEPTION_SCREEN.md)라는 **예외 자체의 수치 잔액에서 차감하지 않는다**. 별도 Team Salary·명단/사인 앤드 트레이드 제한 검문에 더해야 한다. 8/7 [Theis 공식 수취](https://www.nba.com/rockets/news/rockets-acquire-daniel-theis) 이후의 제약도 별도 재검산 대상이다. 약 `$0.20m` 차이만으로 Sekou 거래가 불가능하거나 성사됐다고 판정하지 않는다. Houston의 대가 요구·Detroit 자산/현금·양측 동의, 이후 9/4 Nets와 10/6 Brooklyn 연쇄는 [G15AU](O15G15AU_DETROIT_AUG6_CONSIDERATION_LEDGER.md)의 `HOLD` 그대로다.

## 검증 레이어와 다음 입력

| 역할 | 이번 관측 |
|---|---|
| Anti-Gravity 수집 | Houston Garuba 구단 URL을 `read_url_content→view_file`로 요청했다. CLI는 25초 print 제한 뒤 `SUCCESS` 메타데이터와 **빈 응답**을 반환했다. 구단 본문 Evidence Pack `0건`. |
| NotebookLM 분석 | 같은 구단 URL을 비정본 작업실에 `nlm source add --wait`로 추가했으나 `Could not add url source` 오류. 이 URL에 대한 출처 연결 분석 `NOT_RUN`. |
| Codex 원문·저장소 | NBA 구단 발표·드래프트 결과, CBA §4(e), DB1~DB4 순번, 2차 scale의 곱셈과 서로 다른 정밀도·시간 경계를 대조했다. |
| Claude 반증 / source-blind | Claude CLI의 파일 직접 검토는 `max_turns` 종료로 답변이 없었고, 표준 입력으로 넘긴 재시도도 제한 시간에 출력이 없어 중단했다: `RUN / NO_REVIEW_RESULT`. source-blind `NOT_RUN`. 기존 G15AT/AU의 제한 검토를 재검증 횟수로 옮기지 않는다. |

**사실:** 원역사 23번과 Houston 발표일, CBA의 120%·해외 계약/서면 제외 규칙. **추론:** 대체 21번의 약 `$0.20m` 추가 급여 압력. **후보:** DB1~DB4 21번 지명 및 8/6 Sekou 수취. **작가확정:** 0건. 다음에는 Houston의 **8/6 공식 리그 거래 예외 잔액·전체 Team Salary/명단·서면 제외/실제 계약·Theis 후 apron**을 확보하고, Detroit의 검증된 대가와 함께 같은 날짜로 시험한다. 그전에는 거래/장기 커리어 경로를 정본으로 올리지 않는다.
