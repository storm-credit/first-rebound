# Atlanta 2019-23 Role-Minute Precalculation

- 상태: `PRECALC_PASS_WITH_TRANSACTION_BLOCKERS / NOT_CANON`
- 기준일: 2026-09-04
- 적용 범위: 주인공의 Atlanta 2~5년차 정규시즌 역할·분 범위와 실존 선수 donor 우선순위
- 선행 정본: 2018-19 43경기·621.9분·평균 14.46분·0선발, Erie 6경기
- 후행 게이트: 거래 선행조건 해소 → player-game donor vector → 생산성·승패 계산
- 원고 게이트: `CLOSED`

## 1. 총괄 판정

Atlanta 2~5년차는 다음 범위에서만 계산을 계속할 수 있다.

| 시즌 | 후보 경기·평균분 | 후보 총분 | 후보 사용률 띠 | 역할 상한 | 판정 |
|---|---:|---:|---:|---|---|
| 2019-20 | 52~60경기·17~19분 | 900~1,100분 | 12~15% | 8~10번째 윙/포워드 | `RANGE_CANDIDATE` |
| 2020-21 | 58~66경기·20~23분 | 1,200~1,450분 | 13~16% | 수비형 7~9번째 자원·플레이오프 매치업 카드 | `RANGE_CANDIDATE` |
| 2021-22 | 60~70경기·20~23분 | 1,250~1,500분 | 14~17% | 좋은 주전 후보·하프코트 약점 노출 | `RANGE_CANDIDATE` |
| 2022-23 | 66~76경기·26~29분 | 1,750~2,050분 | 16~19% | 주전급 투웨이 연결자·가치 트레이드 가능 | `TRANSACTION_DEPENDENT_RANGE` |

이는 기록 확정값이 아니다. 총분은 가능한 설계 창이고, 사용률은 주인공이 끝낸 포제션의 대략적 상한을 통제하는 역할 띠다. 경기 수·선발·정확한 평균분·개인 기록은 player-game 원장 전까지 `HOLD`다.

성장은 일부러 완만하게 둔다. 2020-21 플레이오프 경험 뒤에도 2021-22 정규시즌 분이 폭증하지 않으며, 2022-23의 상승은 Huerter 이탈만으로 설명하지 않고 실제 로스터 거래 선택이 달라진 결과여야 한다.

## 2. 실제 분 기준선

NBA 공식 팀 선수 통계의 정규시즌 총분을 기준으로 역할 충돌을 나눴다. 소수점은 NBA 공식 데이터가 제공하는 경기시간을 분으로 환산한 값이며, 아래 수치는 대체 세계의 결과가 아니다.

| 시즌 | 보호할 핵심 기능 | 실제 저·중역할 윙/가드 후보군 총분 | 설계상 사용 가능성 |
|---|---|---:|---|
| 2019-20 | Young 2,120.2·Hunter 2,017.9·Huerter 1,760.4·Reddish 1,550.7·Collins 1,363.2 | Bembry·Carter·Crabbe·Graham·Turner·Wallace·Parsons·Brown·Watson 약 3,103.2분 | 충분하지만 실존 선수별 잔존 기능·경기 가용성 필요 |
| 2020-21 | Young 2,124.6·Huerter 2,126.0·Capela 1,898.4·Collins 1,848.1·Bogdanović 1,305.4·Gallinari 1,221.9 | Hill·Snell·Goodwin·Knight·Fernando·Mays 약 3,899.1분 | 주된 donor 창. Hunter·Reddish의 실제 출전분은 보호 |
| 2021-22 | Young 2,651.9·Huerter 2,188.5·Capela 2,041.5·Bogdanović 1,848.5·Collins 1,662.6·Hunter 1,577.2·Wright 1,452.5 | Luwawu-Cabarrot·Lou Williams·Dieng·Hill·Knox와 단기 대체 선수 약 2,649.6분 | 가능하지만 코로나 대체분을 주인공의 무결석 보너스로 전부 회수 금지 |
| 2022-23 | Murray 2,693.4·Young 2,540.7·Collins 2,129.6·Hunter 2,125.6·Okongwu 1,848.6·Capela 1,730.1·Bogdanović 1,508.6·Jalen Johnson 1,041.6 | Griffin·Bey·Justin Holiday·Forrest·Krejčí·Culver·Mathews·Martin·Williams 약 3,174.1분 | 숫자는 충분하지만 Griffin 지명·Bey 거래를 실제대로 둔 채 전부 차감하면 불가 |

`후보군 총분`은 꺼내 쓸 수 있는 예산이 아니다. 주인공에게 옮길 수 있는지 검사해야 할 모집단이며, 각 실존 선수의 계약·지명·거래·선발 기능을 먼저 보존한다.

## 3. 2019 거래 선행조건 — 새로 발견한 BLOCKER

실제 Atlanta는 2019년 7월 8일 Omari Spellman을 Golden State에 보내고 Damian Jones와 2026년 2라운드 픽을 받았다. 현행 정본에서는 Spellman이 2018 Draft 49순위로 San Antonio에 이미 지명됐다. 따라서 이 실제 거래는 같은 자산으로 성립할 수 없다.

직접 결과는 세 가지다.

1. Damian Jones의 Atlanta 55경기·886.9분·27선발은 자동 존재하지 않는다.
2. Golden State의 2026년 2라운드 픽도 Atlanta에 자동 이전되지 않는다.
3. 주인공은 SF/PF이므로 Jones의 센터 분을 통째로 받을 수 없다. 제한적 스몰볼 5만 가능하다.

Jones 거래가 없는데 실제 로스터를 그대로 복사하면 `없는 자산으로 선수를 받은 오류`가 된다. 반대로 Jones 886.9분을 주인공 성장분으로 쓰면 Collins의 25경기 결장 구간과 실제 센터 수비 부담을 무시한다.

### 해소 후보 — 아직 선택 금지

| 안 | 구조 | 장점 | 비용 |
|---|---|---|---|
| A | Jones 대신 실제 2019 시장의 별도 최소계약 센터 확보 | Hunter·Parsons 등 선행 거래를 덜 건드림 | 정확한 자유계약 풀·계약액·다른 팀 기회비용 재검증 |
| B | Miles Plumlee를 보낸 Parsons 거래를 수정해 센터를 잔류시킴 | 내부 센터 분을 즉시 확보 | Solomon Hill·Parsons·Memphis 자산과 Atlanta 캡 연쇄가 바뀜 |
| C | Jones를 다른 자산으로 Golden State에서 영입 | 실제 센터와 역할 보존 | 대체 자산·2026 픽·Golden State 수용 동기 필요 |
| D | Fernando·Len·Collins와 시즌 중 보강으로 센터 분을 분산 | 새 장기 계약 최소화 | Collins 징계 구간과 Fernando 신인 부담 때문에 가장 위험 |

현재 총괄 우선 검토는 A안이다. 그러나 실제 2019 자유계약 센터와 Atlanta 캡·로스터 자리를 대조하기 전에는 선택하지 않는다.

## 4. 시즌별 donor 구조

### 2019-20 — 900~1,100분

- 1차 후보: DeAndre' Bembry의 915.4분 중 일부
- 2차 후보: Vince Carter 875.6분, Allen Crabbe 521.9분, Evan Turner 251.5분, Treveon Graham 266.4분의 일부
- 보호: Hunter·Reddish의 신인 개발분, Young·Huerter·Collins의 핵심 기능
- 금지: Jones의 미성립 886.9분을 주인공에게 일괄 이전
- 역할: 세컨드 유닛의 3/4번 수비·리바운드, 코너 캐치 뒤 직선 돌파와 첫 패스
- G League: 추가 College Park 배정은 기본값에서 제외

가장 낮은 역사 훼손안은 Bembry·Carter·만료 베테랑의 분을 여러 경기에서 조금씩 줄이는 것이다. 한 명을 지워 1,000분을 만드는 방식은 사용하지 않는다.

### 2020-21 — 1,200~1,450분

- 1차 후보: Solomon Hill 1,513.5분의 일부
- 2차 후보: Tony Snell 992.1분과 Brandon Goodwin 619.6분의 일부
- 제한 후보: Nathan Knight·Bruno Fernando의 일부 4/5번 분
- 보호: Capela·Collins의 센터/림 기능, Gallinari·Bogdanović의 슈팅·창조, Hunter·Reddish의 실제 출전분
- 역할: 정규시즌 스위치 수비와 grab-and-go 사용, 부상 공백을 메우는 포워드

Hill과 Snell은 실제로 생산적 리더·멘토 기능도 가졌다. 주인공이 생겨도 둘을 자동 미계약 처리하지 않는다. 총분은 줄일 수 있으나 라커룸·슈팅 기능을 모두 삭제하지 않는다.

실제 Atlanta가 2021 플레이오프 경로를 유지할 경우에만 14~18경기·약 11~16분, 총 155~285분의 조건부 창을 둔다. 실제 Hill 145.1분과 Snell 65.7분이 1차 donor 후보다. Young·Huerter·Collins·Capela·Bogdanović의 실제 중심 공로는 보호한다.

### 2021-22 — 1,250~1,500분

- 1차 후보: Timothé Luwawu-Cabarrot 684.8분의 대부분 또는 일부
- 2차 후보: Solomon Hill 139.4분과 비핵심 단기 대체 선수 분
- 제한 후보: Lou Williams·Gorgui Dieng·Cam Reddish의 일부. 역할과 거래 결과를 함께 재계산해야 함
- 보호: Delon Wright의 수비·플레이오프 기능, Jalen Johnson의 실제 개발분, 핵심 7인의 중심 기능
- 역할: 20분대 수비 연결자. 주전 결장 시 선발하지만 고정 선발은 아님

코로나 대체계약 분을 전부 받는 계산은 주인공만 건강 프로토콜에서 면제하는 오류가 된다. 주인공의 결장일도 실제 리그 환경과 같은 규칙으로 생성해야 하며, 단기 선수 분의 무조건 회수는 400분 아래로 제한하는 것을 권장한다.

실제 Miami 1라운드 경로가 유지될 경우에만 5경기·16~22분, 총 80~110분의 조건부 창을 둔다. Luwawu-Cabarrot의 실제 22.1분만으로는 부족하므로 다른 8인 로테이션의 분을 줄이는 player-game 근거가 필요하다. 이것이 공격 약점 때문에 닫는 라인업에서 빠지는 시즌이어야 한다.

### 2022-23 — 1,750~2,050분

이 시즌은 단순 분 재배분으로 닫히지 않는다. 실제 Atlanta는 2022년 16순위로 AJ Griffin을 뽑아 1,401.4분을 사용했고, 2023년 2월 Saddiq Bey를 영입해 정규시즌 628.6분을 사용했다. 이미 성장한 주인공이 있다면 같은 윙 투자 두 건의 동기가 약해진다.

- 1차 구조 후보: 2022년 16순위에서 다른 포지션 또는 장기 개발 선수를 선택해 순수 윙 분 700~1,100분 확보
- 2차 구조 후보: Bey 거래를 하지 않아 500~630분과 지출 픽 보존
- 3차 후보: Justin Holiday·Forrest·Krejčí 등 저·중역할 분 200~400분
- 보호: Murray의 두 번째 볼 운반, Hunter의 주전 윙 기능, Collins·Capela·Okongwu의 프런트코트, Bogdanović의 벤치 창조, Jalen Johnson의 개발분

Huerter의 2021-22 2,188.5분이 사라졌다는 이유만으로 주인공에게 같은 분을 복사하지 않는다. 실제로는 Murray 2,693.4분, Griffin 1,401.4분과 다른 윙들이 그 구조를 채웠다.

실제 Boston 1라운드 경로가 유지될 경우에만 6경기·24~28분, 총 144~168분의 조건부 창을 둔다. Bey 거래가 사라지면 그의 실제 플레이오프 132.7분이 1차 donor가 될 수 있으나, 남은 분과 라인업은 다시 계산한다.

## 5. 계약 게이트

주인공의 4년 rookie-scale 계약은 2021-22 뒤 끝난다. 따라서 2022-23 Atlanta 5년차는 계약 사건 없이는 존재하지 않는다.

| 경로 | 구조 | 서사 기능 | 계산 위험 |
|---|---|---|---|
| 2021 rookie extension | 플레이오프 상승 직후 장기 합의 | 팀의 선제 신뢰 | 역할이 아직 작으면 금액·권한 설득이 어려움 |
| 2022 restricted free agency | Atlanta가 qualifying offer로 권리를 유지한 뒤 재계약 | 시장의 저평가와 자기 가치 갈등 | 타 팀 offer sheet·캡·매칭 여부 계산 필요 |

총괄 잠정 선호는 2022 제한적 자유계약 재계약이다. 2021-22의 정체와 2022-23 가치 상승을 분리하고 2023 가치 트레이드의 계약 자산도 만들 수 있다. 정확한 기간·보장액·옵션·트레이드 제한은 `CONTRACT_HOLD`다.

## 6. 정확 계산 전 사전등록 규칙

1. 시즌별 실제 240분×경기와 연장분을 먼저 잠근다.
2. 주인공의 실제 가용일·결장일을 결과와 무관한 규칙으로 만든다.
3. 각 출전일에 같은 포지션·라인업 기능의 실존 donor를 지정한다.
4. 핵심 선수의 실제 분을 줄일 때는 줄어든 기능과 후속 계약·평가를 함께 기록한다.
5. 거래가 달라지면 선수를 삭제하지 않고 새 팀·계약·분의 2차 원장을 연다.
6. 정규시즌 분이 닫힌 뒤에만 플레이오프 진출·대진을 계산한다.
7. 실제 플레이오프 분은 해당 경로가 생존한 경우에만 조건부 donor로 사용한다.
8. 개인 박스스코어·온오프·승패는 R09 생산성 prior가 승인되기 전 생성하지 않는다.

## 7. 이번 단계의 결론

다음 네 가지는 계산 후보로 통과한다.

- 2019-20 900~1,100분의 저사용 윙 로테이션
- 2020-21 1,200~1,450분과 조건부 플레이오프 매치업 카드
- 2021-22 1,250~1,500분의 정체 구간
- 2022-23 거래 선택 변화가 전제된 1,750~2,050분의 주전급 연결자

다음 네 가지는 선행 해소 없이는 잠글 수 없다.

- 2019 Spellman→Jones 거래 붕괴 뒤 대체 센터
- 2021 extension 대 2022 restricted free agency
- 2022 No.16 지명과 2023 Bey 거래
- 시즌별 player-game donor와 플레이오프 생존

## 8. 확인 근거

- [NBA Stats — Atlanta 2019-20 선수 정규시즌 총분](https://www.nba.com/stats/team/1610612737/players-traditional?Season=2019-20&SeasonType=Regular%20Season&PerMode=Totals)
- [NBA Stats — Atlanta 2020-21 선수 정규시즌 총분](https://www.nba.com/stats/team/1610612737/players-traditional?Season=2020-21&SeasonType=Regular%20Season&PerMode=Totals)
- [NBA Stats — Atlanta 2021-22 선수 정규시즌 총분](https://www.nba.com/stats/team/1610612737/players-traditional?Season=2021-22&SeasonType=Regular%20Season&PerMode=Totals)
- [NBA Stats — Atlanta 2022-23 선수 정규시즌 총분](https://www.nba.com/stats/team/1610612737/players-traditional?Season=2022-23&SeasonType=Regular%20Season&PerMode=Totals)
- [NBA Stats — Atlanta 2020-21 플레이오프 총분](https://www.nba.com/stats/team/1610612737/players-traditional?Season=2020-21&SeasonType=Playoffs&PerMode=Totals)
- [NBA Stats — Atlanta 2021-22 플레이오프 총분](https://www.nba.com/stats/team/1610612737/players-traditional?Season=2021-22&SeasonType=Playoffs&PerMode=Totals)
- [NBA Stats — Atlanta 2022-23 플레이오프 총분](https://www.nba.com/stats/team/1610612737/players-traditional?Season=2022-23&SeasonType=Playoffs&PerMode=Totals)
- [Atlanta Hawks — Spellman을 보내고 Jones·2026 2라운드 픽을 받은 실제 거래](https://www.nba.com/hawks/hawks-acquire-damian-jones-from-golden-state-warriors)
- [Golden State Warriors — 같은 Spellman·Jones 거래의 상대 구단 기록](https://www.nba.com/warriors/news/warriors-acquire-spellman-20190708)
- [Atlanta Hawks — Hill·Plumlee를 보내고 Parsons를 받은 실제 거래](https://www.nba.com/hawks/news/hawks-acquire-chandler-parsons-memphis-grizzlies)
- [Atlanta Hawks — 2020 Solomon Hill 영입](https://www.nba.com/hawks/news/atlanta-hawks-sign-free-agent-forward-solomon-hill)
- [Atlanta Hawks — 2022년 16순위 AJ Griffin 지명](https://www.nba.com/hawks/news/atlanta-hawks-select-aj-griffin-with-the-no-16-pick-and-acquire-the-draft-rights-to-the-51st-pick-tyrese-martin-in-the-2022-nba-draft)
- [Atlanta Hawks — 2023 Saddiq Bey·Bruno Fernando 거래](https://www.nba.com/hawks/news/the-hawks-acquire-saddiq-bey-and-bruno-fernando-on-nba-trade-deadline)
- [NBA — 2018 1라운더의 2022 qualifying offer·RFA 사례](https://www.nba.com/news/cavaliers-extend-qualifying-offer-to-collin-sexton)
