# R01 — O-15G14 양 팀 분·공격기회 자체 검토

- 대상: [G14 결과](../simulation/CHICAGO_2021_22_PAIRED_REVIEW.md).
- 판정: `PARTIAL_CONDITIONAL_INPUT_PASS / NOT_INDEPENDENT`.
- 독립 검수·완성 시즌·작가 승인으로 계상하지 않는다.

## 핵심 오류 방지

1. **미래 prior 혼입:** 상대17명의1,087행은2020–21만 허용한다. 날짜/시즌을2021–22로 바꾼 음성 검사를 통과했다. 목표3경기78행은 별도 사후 예산이고 개막 예측에 쓰지 않는다.
2. **점수/포제션 허위 인증:** 선수TOV 합계에 별도 팀 실책이 포함됐다고 가정하지 않는다. FGA/FTA/TOV 통제 배분은 team score·효율·승수와 분리하며 결과 필드는 null이다.
3. **상대 실제 명단 자동 복사:** DET Patrick/Kira/Stewart와G7 Suggs, ORL Mobley/Herbert 및Carter CHI, SAC 별도두거래/Metu후속을 확인했다. 미확보 등록·급여·픽을 조건으로 남긴다.
4. **이전 방향을 영구 금지로 확대:** T4의2020–21 Hood POR 방향은2022 MIL 소속의 영구 부정이 아니다. 중간 방출·FA·등록 근거가 미확보라는 정확한 경계로 수정했다.
5. **출전분 허위 완성:** CHI3/DET1/SAC1의5인 증명만 240분을 인정한다. ORL은 현재 지정 가드/36분 규칙 아래12분 HOLD이며 전체 구단 불능 판정이 아니다.
6. **Questionable을Out으로 변경:** Mitchell 실제 상태를 그대로 두고 SAC 분안의 미출전을 수동 조건으로 명시한다. Green Probable도 의료 허가가 아니다.
7. **빈 prior를0으로 충전:** Suggs24분 누락은 네 정책 전체를 HOLD시킨다. 미래 NBA 관측과 대학 수치를 즉석에서 동일단위로 합치지 않는다.
8. **성장 비용 소거:** B14A의P기회를 유지하면2/16 동료 실책 가중치는0.663배가 필요하다. 이를 검증된 실책 개선 또는 주인공 성장의 단독 인과효과로 표현하지 않는다.
9. **재현 불안정:** 고정/잔여 집합의 합산 순서를 정렬해 별도 PYTHONHASHSEED에서도 같은 출력이 생성되게 했다. 저장증명 재현에 scipy가 필요하지 않다.

## 실행 검증

```text
python tools/build_chicago_2021_22_paired.py --check
PYTHONHASHSEED=13 python tools/build_chicago_2021_22_paired.py --check
python -m unittest discover -s tools -p test_chicago_2021_22_paired.py
python tools/build_chicago_2021_22_growth.py --check
python -m unittest discover -s tools -p test_chicago_2021_22_growth.py
python tools/build_chicago_2021_22_inputs.py --check
python -m unittest discover -s tools -p test_chicago_2021_22_inputs.py
python -m unittest discover -s tools -p test_chicago_2021_22_role_plan.py
python tools/build_cp2_design_packets.py --check
git diff --check
```

신규11·기존22검사와G14/G13/G12/CP2 재현, 변경 JSON·상대 링크·공백 검사를 통과한 변경만 기존 CP2 승인에 따라 PR→main으로 반영한다. 원본78행/전년도1,087행 계보 해시와 원격 blob/tree를 대조한다. 원격 CI 미설정을 CI PASS라고 보고하지 않는다.

총24팀·정책 조건 중16숫자/8HOLD,12양팀 조건 중4만 양쪽숫자다. 실제 분·생산성·시즌 선택0, 신규 공식 숫자 박스 대조0, 전체 독립검수0을 유지한다. 다음은 Suggs 개막 이전 환산과 ORL12분 역할 대안이며 문체 독서·D1 정확실행의 잔여 상태도 유지한다. 전체1완료·6진행/남은6개, v0.30 PARTIAL·설계/원고CLOSED·author/season/exact/manuscript false.
