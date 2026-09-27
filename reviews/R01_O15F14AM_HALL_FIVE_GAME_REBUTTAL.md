# R01 — O-15F14-AM 5경기 부하 상한 제한 반증

- Claude CLI `haiku --restricted --tools ''`에 AM 문서와 두 계산 코드 본문을 텍스트로 전달해 **읽기 전용 반증**을 받았다. 외부 NBA 원문을 직접 읽히지 않았고 새 독립 원자료는 0건이다. 앞선 AL 검토 시도의 무응답은 이 실행 성공으로 소급하지 않는다.
- Codex는 Claude의 일곱 지적을 [원분 입력](../simulation/NBA_2020_21_FINAL859_MINUTES.json), [재현 코드](../tools/screen_orlando_hall_five_game_load.py), [AM 문서](../research/O15F14AM_ORLANDO_HALL_FIVE_GAME_OBSERVED_LOAD.md)에 대조했다.

| 지적 | 판정·처리 |
|---|---|
| 5/13 `Questionable`인데 Bamba가 입력에 있을 수 있다 | **표현 수정**. K1의 5/13 원경기·대체 분 사전에 Bamba가 모두 없고, 따라서 코드가 부재 분기를 실행한다. `Questionable=Out`이라는 새 진단은 만들지 않는다. |
| Nnaji 16분의 사실 근거 불명 | **수용**. 16분은 기존 F4 화면의 선별용 모델 상한이지 원역사 최대/의료 허가가 아님을 AM에 명시했다. Vučević 36분도 같은 성격이다. |
| `10개` 비교 단위와 피로 계수 불명 | **표현 수정**. `5경기 × RAPTOR/BPM 2방법` 및 K1 계수 0.5/경기 2,880초를 명시했다. 피로 모델의 실증 타당성은 별도 `HOLD`. |
| 5/9 계약 생략과 5경기 Hall 처리 범위 불명 | **수용**. 4월 계약 보존·5/9 신규 계약 생략·5경기 등록/출전 없음과 미확정 분/건강을 분리했다. |
| Bamba 원경기 상한, 추가 분 선별이 코드에 없는 듯하다 | **기각**. 새 코드의 `actual_seconds` cap와 기본 코드의 `additions = players ∩ caps.keys()` 및 행별 추가 분 합계 단언이 있다. 원자료/코드 실행 없이 제기된 의문이다. |

AM의 수치 재현은 통과했으나 Claude의 텍스트 반증은 경기 의무기록·리그 등록/계약 원장이나 시즌 인과의 인증이 아니다. F4/A1/A3·K와 전체 2번 종료는 `HOLD`, freeze/설계·원고 게이트는 불변이다.
