# O-15F14-M / O-15G1 자체 검토

- 상태: `LOCAL_CHECKS_PASS / NOT_INDEPENDENT`.
- 추첨 사전 게시 커밋: `2f77a4eac597dc7eaab0127ec4d83123e42b5c85`.

## 수용 범위

- CP2 승인은 절차만. author/season/exact/manuscript false 유지.
- 작품 seed 최초 실행 전에 입력/알고리즘/tree 공개. 당첨 반복 HOU는 로그 보존·같은 픽 재추첨. 1001조합/1000배정, top4, 60원소유 순번.
- 2R 동률은 최종1R 역순. 실제2021 전체2R fixture, MIN보호3/4, CHI/NOP스왑 양방향 검사.
- 2021 네 안 모두15자리. 지명되지 않은 선수·예비비를 계약/매칭 급여로 변환하지 않음. 원고/경기 점수 없음.
- 주인공4년차 옵션 계산은 기존 Carter7순위의 공개 $6,920,027과 교차 대조. 정확 주인공 순번 미확정.
- MLE 계산에서 미지정 예비비를 제거했다. 추가실제cap산입액 최소 $878,908이 필요한 경계를 공개해 ‘예산 여유=예외 자격’ 오류 차단.
- 정상일240분은 포지션 산술 배분. 경기별 실제5인 교대/효율·82경기총분 검증으로 확대하지 않음.
- 2022 48조건에서 비납세 가능조건과 tax/apron 초과 반례 모두 보존. 이전 F/I/K 반례와 합치지 않음.

## 실행 검증

`PYTHONPATH=tools python -m unittest tools/test_2021_provisional_draft.py tools/test_chicago_2021_23_continuation.py -v`: 9개 PASS.

두 builder의 JSON 바이트 재현 및 `git diff --check` PASS. 사전 입력/알고리즘 해시 불변도 확인했다. 원격 CI 실행 여부는 실제 PR 조회 결과로 별도 보고한다. 독립 검수 완료가 아니다.

## 잔여 경계

정확 건강/charge/Hall 승인, 2021 전구단 소유권/선수보드, 백업C 실제 계약, 2022–23 결과/픽·2023 규정/대표팀 사건은 HOLD. 결말·장기 경로 추천으로 이어갈 수 있으나 최종 세계관 통합 PASS·원고 개방은 불가하다.
