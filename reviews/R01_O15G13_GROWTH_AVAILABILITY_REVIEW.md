# R01 — O-15G13 생산성·가용성 자체 검토

- 판정: `CONDITIONAL_INPUT_PASS / NOT_INDEPENDENT`.
- 대상: [G13 검토](../simulation/CHICAGO_2021_22_GROWTH_REVIEW.md).
- 독립 검수: 미실시. 작업자가 별도 점검했으며 전체 G16 통과로 계상하지 않는다.

## 확인한 오류 가능성과 처리

1. **미래 기록 누출:** 생산성 함수는 2020–21 비교행과 개막 이전 대학 총합만 받는다. 2021–22로 바꾼 season/미래 날짜를 거부하고, 미래 보고서를 바꿔도 생산성은 동일하다.
2. **가짜 환산 정밀도:** Duarte의887분은 대학 페이지 표시값이다. NBA환산 계수는 수동 가설, 다섯 비교자는 편의 표본이며 통계적 보정/신뢰구간이라고 부르지 않는다.
3. **성장 비용 삭제:** 주인공 공격 확대 시 TOV와 공격 종료량이 증가한다. 같은32분에서 비교하며 리바운드·스틸·블록의 분당 수치는 동결한다. 라이브 패스 완성을5년차에서 앞당기지 않는다.
4. **2점/3점 이중 계상:** `PTS=2FGM+3PM+FTM`, 각 성공≤시도, 대학 REB=ORB+DRB를 확인했다. 슛 위치별 박스를 추정하지 않는다.
5. **복합 결장 수신자 오류:** 2/16에는 G11 LaVine 단독 대체안의 수신자 Caruso/Duarte도 Out이므로 그대로 쓸 수 없다. 새70분 증명에서 전개자 부족이 드러난 최초 배분은 버리고 Coby SG분을 재배치했다. 최종안은 모든 조합에LaMelo 또는Coby가 있다.
6. **보고일과 경기일:** 1/23 보고서의Markkanen은1/24 경기 사유다. Questionable/Probable은확정Out/허가로 바꾸지 않고 투웨이 파견은 의료와 분리했다.
7. **그린 이중 사용:** 1/23 Green도Out이므로70분안의Green수신분을 재사용하지 않는다. 별도56분안은Stanley SF10·Duarte14유지로 검산했다. Green추가부재 음성 검사를 보존했다.
8. **박스 합계=점수차 오류:** Caruso공백 득점귀속+0.79도 전력 향상을 뜻하지 않는다. 모든팀점수차·효율·승수는null이다.

## 검증 명령

```text
python tools/build_chicago_2021_22_growth.py --check
python -m unittest discover -s tools -p test_chicago_2021_22_growth.py
python tools/build_chicago_2021_22_inputs.py --check
python -m unittest discover -s tools -p test_chicago_2021_22_inputs.py
python -m unittest discover -s tools -p test_chicago_2021_22_role_plan.py
python tools/build_cp2_design_packets.py --check
git diff --check
```

새8검사·기존14검사, 파생재현·입력해시·상대링크 점검을 통과한 경우만 PR→main으로 넘긴다. 실제대체 날짜별분0·최종시즌 미선택, generic사유6행과코비맥락12행은별도HOLD다. canon/manuscripts/context-packs는변경하지 않는다. 전체1완료·6진행·남은6개와모든닫힌게이트를유지한다.
