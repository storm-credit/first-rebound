# Chicago 2020-21 Postdeadline Capacity Audit

- 단계: O-15F5-AUTHOR → O-15F6
- 기준일: 2026-09-09
- 판정: `AUTHOR_APPROVED_PLAYER_ROUTE / CONDITIONAL_MINUTE_CAPACITY_PASS / AVAILABILITY_AND_LINEUPS_HOLD`
- 선행 main: `183b9e61af4de4f19cc7fea2b63eff8b42e783ef`
- 원고 게이트: `CLOSED`

> 후속 감사: `CHICAGO_2020_21_POSTDEADLINE_EXECUTION_AUDIT.md` (O-15F6B). 아래는 O-15F6 당시 용량 검산 이력이다. 최신 조건부 5인 조합·수정 후보·미결 파급은 후속 문서를 따른다.

## 작가 선택과 사건 경계

직전 응답은 “이어서”를 A 승인으로 해석한다고 명시했고, 작가는 2026-09-09 “이어서진행”으로 계속을 지시했다. A의 선수 이동을 승인 기록으로 통합한다. Chicago는 Gafford·Kornet을 보내 Theis·Green을 받고, Washington은 Wagner를 보내 Gafford를 받으며, Boston은 Theis·Green을 보내 Wagner·Kornet을 받는다. Carter·Porter·두 1라운드는 Chicago에 남고 Brown·Trent는 Washington에 남는다.

승인은 선수 이동 선택에 적용된다. 기존 O-15F5가 남긴 현금·trade bonus·unlikely bonus·당일 cap/tax 장부는 `EXECUTION_DETAILS_HOLD`로 계속 공개한다. 이를 이미 확인한 리그 승인으로 표현하지 않는다. 아래 원장은 선택된 선수 이동이 실행된다는 조건의 계산이며 원고용 확정 출전 기록이 아니다.

## 실제 기준선과 출처

NBA V3 박스를 보존한 공개 미러의 part 1을 추출했다. 미러는 NBA와 별도 독립 출처가 아니다. 추출 전 마감일 전 43경기·625,202초를 기존 정본 원장과 대조해 정확히 재현했다. 후반 29경기는 실제 12승 17패, 417,603초 = **6,960분 03초**, 선발 145자리다. 전체 시즌 합계 1,042,805초는 17,380분 05초이며 초기 정수분 기준선 17,380분과 5초의 표시 차이만 있다. 분 단위 박스를 다시 초로 정밀화했다고 주장하지 않는다. 원자료의 초 합계 잔차를 보존한다.

- 미러: https://github.com/NocturneBear/NBA-Data-2010-2024
- 파일: `regular_season_box_scores_2010_2024_part_1.csv`
- 다운로드 SHA-256: `ca9636d08c577e3d752f69e32f90b173f4c3374c15f4dc8494b655049fdfc557`
- 시작 경기 공식 확인: https://www.nba.com/bulls/game/0022000697-bulls-vs-spurs-san-antonio-tx-03-27-2021 (104-120)
- 종료 경기 공식 확인: https://www.nba.com/bulls/game/0022001068-bucks-vs-bulls-chicago-il-05-16-2021 (118-112)
- 개별 경기 URL은 `CHICAGO_2020_21_POSTDEADLINE_ACTUAL.csv`에 보존한다.

## 계산 규칙 — 결과를 보고 배정하지 않음

1. 실제 Patrick·Vučević·Aminu·Brown을 대체 Chicago 원장에서 제거한다. 합계 116,535초 = 1,942:15다.
2. 주인공 30분, LaMelo 28분, Carter 26분을 매 경기 조건부 용량 입력으로 둔다. 의학적 전 경기 가용성 확정이 아니다.
3. Theis는 실제 Chicago 출전일과 분을 비교 기준으로 쓰되 24분을 상한으로 낮춘다. Green의 실제 분은 기준선으로 보존한다. 두 선수의 실제 출전 기록을 정본으로 복사하지 않는다.
4. 부족한 분은 Satoransky→Valentine→Arcidiacono→Coby→Temple 순서로 같은 날짜에 차감한다. 기존 10/6/0/20/16분 하한은 유지하며 원래 그보다 적게 뛴 선수의 분을 하한까지 새로 만들지 않는다.
5. 잉여분은 Carter(30분 상한)→Young→Theis→Temple 순으로 반환한다. Young의 gross 증가도 원장에 남긴다.
6. 선발은 주인공이 Patrick, LaMelo가 당시 PG, Carter가 당시 센터 자리를 대체한다. 선발 다섯 자리의 수학적 보존만 통과하며 포지션·stint 조합의 전술적 성립은 별도다.

## Porter 세 조건과 결과

| 조건 | 의미 | 결과 |
|---|---|---|
| PORTER_ZERO | Porter 0분을 하한 조건으로 시험 | 29경기 총분·선발 보존 |
| PORTER_12_STRESS | Porter가 매 경기 12분을 요구하는 상한 압력 | 5경기 합계 28:44 초과, 실행 가능한 원장 아님 |
| PORTER_CAPPED | 12분 입력에서 하한을 지킨 다른 선수에게 더 차감할 수 없으면 Porter 분을 낮춤 | 29경기 총분·선발 보존, Porter 합계 319:16 |

실패 날짜는 05-06 7:30, 05-07 1:53, 05-11 5:57, 05-13 2:29, 05-16 10:55다. 마지막 경기의 Porter 분은 1:05까지 줄어야 한다. 따라서 `PORTER_CAPPED`는 의학적으로 건강한 Porter의 권장 로테이션이 아니라 고정된 코어 분·donor 하한의 비용을 보여 주는 용량 검산이다. 모든 조건의 승패 열은 실제 기준선이며 대체 승패 결과가 아니다.

## 기존 시즌 prior 재개방

전반 승인값에 이 29경기 가용성 조건을 더하면 주인공은 72경기·72선발·2,089분, LaMelo는 72경기·54선발·2,003분이다. 이 값은 **가용성 조건의 산술 결과**이지 신체 내구성이나 시즌 기록 LOCK이 아니다.

기존 opening prior는 주인공 68경기·58선발·1,938분, LaMelo 64경기·32선발·1,760분이었다. 이미 전반에 주인공 43선발, LaMelo 25선발을 사용했으므로 낡은 목표를 맞추기 위한 임의 결장·벤치 강등은 만들지 않는다. 해당 prior의 상태를 `REOPEN_REQUIRED_POSTDEADLINE`로 낮추고 실제 가용성·전술 역할 뒤 새 시즌 합계를 계산한다.

## 남은 실제 비용과 다음 작업

- Carter·Porter의 Orlando 분·선발·부상 사건을 Chicago에 복사하지 않는다. Porter의 2021-04-09 공식 Magic preview에 기재된 왼발 통증은 비교 증거다. Chicago에서 같은 발병일·결장 기간이라는 결론은 아니다: https://www.nba.com/magic/orlando-magic-indiana-pacers-game-preview-story-20210409
- LaMelo Charlotte 손목 부상과 주인공 부상·결장은 가용성 감사에서 별도 판정한다. 새 사건을 증거 없이 만들어 분을 맞추지 않는다.
- Theis·Carter·Young·Markkanen을 포함한 48분 센터와 96분 가드/윙의 실제 5인 조합은 아직 증명하지 않았다. 총분·선발 5자리 PASS를 lineup PASS로 표현하지 않는다.
- Orlando는 Carter·Porter·Chicago 두 픽을 받지 않는다. Vučević·Aminu의 별도 행선지와 Chicago–Orlando 직접 대결을 재계산해야 한다. 실제 Orlando 로스터를 상대 기준선으로 자동 유지하지 않는다.
- Washington Brown·Trent 잔류, Gafford 이동, Boston Wagner·Kornet 이후 경로도 별도 접촉 사건이다.

다음은 **O-15F6B 거래 세부·가용성·5인 조합 감사**다. 그 뒤에만 생산성·후반 outcome·2021 lottery와 여름 계약을 닫는다. 새로운 작가 선택 질문은 이번 단계에 없다.

## 재현

`node tools/build_chicago_2020_21_postdeadline.mjs` — 저장된 실제 추출표에서 조건부 원장 재생성.

`node tools/verify_chicago_2020_21_postdeadline.mjs` — 29경기·실제 기준선·세 조건·donor·선발·실패 경계 검산.
