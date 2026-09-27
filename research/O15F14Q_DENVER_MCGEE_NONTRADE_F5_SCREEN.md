# O-15F14-Q — Denver McGee 거래 생략 경로 선별

- 상태: `F5_LOCAL_SENSITIVITY / AUTHOR_DIRECTION_SELECTED / EXACT_EXECUTION_HOLD`.
- 후속 선택: [작가 응답](../canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json)은 거래 생략을 선택했다. 이 문서의 국소 검사는 선택 전 산출물이므로 최종 경기·시즌 PASS가 아니다.
- 계산: [`screen_denver_mcgee_nontrade.py`](../tools/screen_denver_mcgee_nontrade.py), [25경기 결과 JSON](../simulation/DENVER_2020_21_MCGEE_NONTRADE_SCREEN.json).
- 기존 K1·L2 추천이나 859경기 원장을 바꾸지 않는다. `author_locked=false`, `season_selected=false`.

## 거래 사실과 대체 세계 후보

[Denver 구단 발표](https://www.nba.com/nuggets/news/javale-mcgee-back-2021325)와 [Cleveland 구단 발표](https://www.nba.com/cavaliers/releases/hartenstein-trade-210326)에 따르면 원역사 2021년 3월 거래에서 McGee는 Denver로, Hartenstein과 2라운드 지명권 두 장은 Cleveland로 이동했다. [NBA 공식 거래표](https://www.nba.com/news/2020-21-nba-trade-tracker)는 이 거래가 승인됐다는 원역사 사실을 확인한다. 정확 두 픽의 보호·예외·당일 charge는 [F5 현행 원장](../simulation/NBA_2021_EXECUTION_RESOLUTION.md)의 경계를 따른다.

T1~T4 작가 방향 승인에는 McGee 거래가 없다. **후보 F5-N**은 이 별도 거래를 생략하여 McGee가 Cleveland에, Hartenstein이 Denver에 계속 남는 경우다. 이는 원역사 진술이나 작가 확정이 아니다. 이 후보에는 McGee 수취 TPE와 해당 두 2R 이전이 발생하지 않는다. Gordon T1 픽과 혼합하지 않는다.

## 국소 분·승패 스트레스

K1 LOW 분 원장의 Denver 11경기에서 McGee의 양수 분 합계 9,252초를 Hartenstein에게 같은 경기·같은 길이로 치환했다. 변경 없는 Cleveland 관측 14경기에서는 Hartenstein의 15,273초를 McGee에게 치환했다. 각 경기 최고 치환 분은 Denver 24.37분, Cleveland 27.22분으로 선별 상한 36분 안이다. Denver의 기존 11개 5인조 분해에서 동일 센터 역할로 이름을 바꾼 조합은 기존 역할 검사 11/11 통과했다. Cleveland는 원장에 5인조가 없으므로 **후보 포지션 집합**으로 정확한 선수별 초·선발 180초를 만족하는 5인조 LP를 새로 풀어 **14/14 통과**했다. 4/11 CLE–NOP는 Dellavedova의 2,063초만으로 48분 내내 볼핸들러를 세울 수 없어 Osman을 조건부 보조 핸들러로 둔 경우에만 통과한다. 이 가정은 실제 감독의 배치나 선수 건강을 입증하지 않는다. [JSON](../simulation/DENVER_2020_21_MCGEE_NONTRADE_SCREEN.json)에 경기별 증인과 가정한 역할을 남겼다.

RAPTOR·BPM 각 25개, 총 **50개 경기·방법의 국소 점수차 비교에서 승자 방향 반전 또는 미해결은 0건**이다. 가장 작은 후보 절대 점수차는 Detroit–Cleveland 4월 19일 BPM 3.73점, Lakers–Denver 5월 3일 BPM 4.10점이다. 이 검사는 해당 한 경기의 출전 분·평점만 치환한 것이다. 다른 팀의 후속 선택, 건강, 수비 매치업, 플레이오프, 시즌 누적 기록의 보존을 입증하지 않는다.

## F5 판단

후보 F5-N은 원거래의 **정확 TPE 잔액·2023 2R 보호 후 종료/이월·2027 2R 이전**을 사용할 필요가 없는 대체 사건이다. 대신 Denver가 McGee를 얻지 못하는 이유와 Cleveland가 그를 계속 보유하는 사건, 양 팀 전체 등록·급여·선수 의향, Denver/Cleveland의 25경기 외 후속 영향을 확인해야 한다. Cleveland가 Hartenstein 없이 치른 다른 경기와 Denver의 플레이오프 로테이션은 이 25행에 포함되지 않는다. 공개 기본급 차액은 McGee $4,200,000 − Hartenstein $1,620,564 = $2,579,436이지만, 이 값을 당일 팀 charge나 총 비용으로 확정하지 않는다.

작가는 F5-N을 선택했다. 원거래 유지안은 비교 이력이다. T1~T4를 재승인받지 않는다. F5-N의 전체 등록·비용·건강/플레이오프 파급을 정리하기 전까지 F5·`K_TRANSACTIONS`는 `HOLD`다. D1의 F 전체 PASS `0/5`, A 최종 채택 `0/3`, K 종료 `0/4` 및 `PROJECT_FREEZE v0.30 PARTIAL`·설계/원고 `CLOSED`는 그대로다.
