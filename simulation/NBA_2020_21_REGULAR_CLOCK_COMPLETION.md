# 2020–21 정규시즌 시계·5인조 작업 입력

상태: `CONDITIONAL_1080_GAME_CLOCK_COMPLETE_WORKING_INPUT_ONLY`. 선택된 BPM 1,080경기와 2,160팀을 소비하여
기존 원천의 6개 초 차이만 새 작업 모델로 최소 보정했다. 원천 선수 초는
`simulation/NBA_2020_21_SELECTED_REGULAR_OVERLAY.json`에 그대로 남아 있으며 이 파일에는 보정 전 값·원천 주소·선택규칙을 함께 남겼다.

|날짜|팀|선택 선수|초 보정|BPM 효과|적용 피로 벌점|
|---|---|---|---:|---:|---:|
|2020-12-31|CHI|Denzel Valentine|-1|+0.00034856|+0.00000000|
|2021-01-10|LAC|Terance Mann|-1|+0.00023405|+0.00000000|
|2021-01-15|OKC|Aleksej Pokusevski|+1|-0.00076030|+0.00000000|
|2021-01-25|BOS|Robert Williams III|-1|-0.00083690|+0.00000000|
|2021-03-12|CHI|Denzel Valentine|-1|+0.00034856|+0.00000000|
|2021-03-12|MIA|Precious Achiuwa|-3|+0.00133842|+0.00000000|

모든 팀의 합계는 경기 길이의 5배, 개인 초는 경기 길이 이하이다. 기존
107개 5인조 구간은 원천 그대로 검증해 재사용했고,
나머지 2053개는 5인 동시 투입의 **수학적 존재증인**이다.
구간 배열 순서는 실제 교대 순서가 아니며 포지션·전술·감독 선택을 증명하지 않는다.
승자는 1,080경기 모두 같은 방향이며 CHI 31승,
MIN 24승이다. 전체 건강·활성 명단·계약·시즌 확정·원고 게이트는 CLOSED다.

재생성: `python tools/build_2020_21_regular_clock_completion.py --write`
검증: `python tools/build_2020_21_regular_clock_completion.py --check`
