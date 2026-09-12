# O-15F14-M — CP2 추첨 실행 전 기록

- 상태: `PREREGISTERED_ALGORITHM / RESULT_NOT_YET_RUN`.
- 승인: [CP2 절차 승인](../canon/CHICAGO_2020_21_CP2_APPROVAL.json). 고정 입력: [동명 JSON](NBA_2021_DRAW_PREREGISTRATION.json).
- 범위: 2021 드래프트 전체 60개 원소유 순번, CHI/MIN 핵심 픽 잠정 결산. 선수 지명·전 구단 거래 소유권 감사는 별도다.

## 고정 입력

K1/BPM F038의 전체 1,080경기와 L2 동서부 플레이인 패킷을 사용한다. Chicago 31승·Minnesota 24승을 포함한 30팀 승수, 14개 추첨 참가팀과 16개 플레이오프 팀을 입력 JSON에 저장한다. 원권위 파일 SHA-256을 검사하며 후속 결과 파일이 원입력을 변경하지 않는다.

CP2로 허용된 것은 잠정 결과다. `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, 설계·원고 CLOSED를 유지한다. 이미 승인된 조건부 작업 절차를 추첨 뒤 다시 묻지 않는다.

## 결과를 보기 전에 고정한 알고리즘

1. seed 본문은 기존 규약의 `first-rebound|nba-lottery|2021|v1`이다. UTF-8 SHA-256 32바이트를 seed로 사용한다. 다른 seed 후보를 만들지 않는다.
2. 난수 블록은 `SHA256(seed_bytes + b'|' + domain_utf8 + b'|' + counter_uint64_big_endian)`이다. counter는 domain별 0부터 시작한다. 256비트 정수를 n으로 나누기 전 `2^256`에서 n의 배수가 되는 경계 이상을 버려 모듈러 편향을 없앤다.
3. 동률은 추첨 참가팀과 플레이오프 팀을 나눠 처리한다. 동일 멤버·승수·순서 구간인 기존 CLE/OKC와 DEN/LAC 추첨은 각각 OKC→CLE, LAC→DEN을 유지한다. 바뀐 그룹은 팀 약어 사전순에서 Fisher–Yates를 실행한다. domain은 `tie:` 뒤에 쉼표로 이은 사전순 팀 약어다. 경기 순위용 H2H는 사용하지 않는다.
4. 확률 슬롯은 14개 기본 조합 수를 사용한다. 동률 그룹의 슬롯 합계를 균등 배분하고 남은 1개는 동률 순서 앞 팀에 준다. 1,000개 배분 총합을 검사한다. CHI/NOP의 9~10 슬롯 합계는 75이므로 38/37로 나뉜다.
5. 1~14에서 고른 4개 수의 조합 1,001개를 사전순으로 나열한다. 추첨 전 팀 순서대로 조합을 연속 배정하고 마지막 `[11,12,13,14]`는 미배정이다. 이 조합표는 작품 시뮬레이터의 고정 구현이며 NBA의 실제 팀별 조합표를 복사했다는 뜻이 아니다. 같은 가중치의 균등 조합 추첨이다.
6. `lottery` domain에서 0~1000 균등 인덱스를 뽑는다. 미배정이나 이미 당첨된 원소유 팀이면 같은 픽을 다시 뽑고 모든 시도를 로그에 남긴다. 네 당첨팀 뒤에 미당첨팀을 추첨 전 순서로 붙인다. 보유 구단이 같은 두 자산도 원소유 팀은 서로 다르므로 별도 참가한다.
7. 15~30은 플레이오프 참가팀의 정규시즌 성적순이다. 2라운드는 전체 30팀 성적순이고, 동률 팀은 **최종 1라운드 원소유 순서의 역순**이다. 플레이오프 팀/추첨팀 경계를 넘는 동률도 이 규칙으로 연결한다.
8. 전체 60개 순번을 만든 뒤 CHI 자체 1R, MIN top3 보호, CHI/NOP 2R 스왑을 조건부 판정한다. 최종 선수·향후 성공·이야기 선호는 난수 입력에 넣지 않는다.

핵심 절차는 [NBA의 2021 동률 공지](https://www.nba.com/news/ties-broken-for-order-of-selection-in-2021-nba-draft), [Pacers의 당시 설명](https://www.nba.com/pacers/news/pacers-hoping-good-fortune-2021-draft-lottery), [조합 미배정 설명](https://www.nba.com/magic/news/how-nba-draft-lottery-works)을 대조했다. 2017 자료는 미배정 조합에만 사용하고 당시 상위 3픽 제도를 가져오지 않는다. [2021 실제 결과표](https://pr.nba.com/2021-nba-draft-lottery-results/)는 2라운드 순서의 별도 검증 fixture다. 현재 시점 제도 변경을 2021에 적용하지 않는다.

## 실행·검증 규칙

이 입력·알고리즘·승인 파일을 먼저 GitHub 브랜치에 게시하고 commit SHA를 확보한다. 그 SHA를 `--preregistered-commit`에 넣어 최초 실행한다. 테스트는 합성 seed와 알려진 실역사 fixture만 사용하며 작품 seed 결과를 사전 탐색하지 않는다.

결과 파일을 생성한 뒤 같은 입력·알고리즘으로 재생성하여 바이트 일치를 확인하는 것은 재현 검증이다. 마음에 드는 결과를 고르는 재추첨이 아니다. 버그가 발견되면 원실행·수정 이유를 보존하고 숨겨서 결과를 교체하지 않는다.
