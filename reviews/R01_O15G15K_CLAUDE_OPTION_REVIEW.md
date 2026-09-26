# O-15G15K Claude 제한 반증과 원문 대조

- 입력: G15K 초안 본문만 Claude CLI 새 세션에 전달. `claude --model haiku --tools '' --max-turns 1 --no-session-persistence -p`로 응답 완료. 외부 원문을 Claude가 직접 읽은 검수는 아니며 **제한적 반증**이다.
- 상태: `CLAUDE_LIMITED_RUN / NOT_G16_PASS`. 새 작가확정·거래/계약 사건 없음.

| 지적 | 판정 | 대조와 조치 |
|---|---|---|
| 3/25 T2 분기와 옵션 시험 범위가 모호 | **수용** | G15K에 3/25 원역사 패키지 미실행이라는 뜻과 7/29→10/16 비용 시험에 한한 `WORKING_PRIOR`를 명시. [T2 승인](../canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json)은 Vučević의 잔여 시즌만 직접 승인한다. |
| 분기 전 무릎 시술과 이후 의료 변화가 모순 | **표현 정밀화** | [Orlando의 2020-12-02 시술 발표](https://www.nba.com/magic/orlando-magic-al-farouq-aminu-undergoes-procedure-right-knee-20201202)는 이전 사건이고, 3/25 뒤 회복·시장 평가는 다른 질문이다. G15K에 이 경계를 적었다. |
| DeRozan 거래와 옵션의 관계가 불명확 | **표현 정밀화** | [G15G](../research/O15G15G_AMINU_DEROZAN_CAUSAL_LEDGER.md)는 Chicago가 원패키지로 Aminu를 얻지 않으면 8/11 원거래의 송출 자산 하나가 없음을 이미 검증했다. G15K에도 명시. 옵션 행사 자체가 DeRozan 거래를 일으킨다고 쓰지 않는다. |
| O15A/O15C 자리 반례와 Preston 픽 거래의 연결 부족 | **표현 정밀화** | [G15H](../research/O15G15H_ORLANDO_DATED_REGISTRATION_WITNESS.md)의 Herbert PG/Gravett PG 조건부 16/17명과 초과 1/2명을 명시했다. [G15F](../research/O15G15F_ORLANDO_OFFSEASON_BRANCH_COSTS.md)의 Orlando 33번 Preston 권리를 Herbert로 쓰는 경우 픽/현금 대가를 함께 제거한다. 이는 옵션과 **병렬 의존**이다. |
| 옵션 통지 조항 미확보 | **유효 HOLD** | 공개 계약서·리그 통지 기록이 없어 정확 통지일을 확정하지 않는다. Claude가 제안한 5/18 또는 5/21 임의 선택은 **기각**한다. [5/18 기사](https://www.nbcsports.com/nba/news/report-al-farouq-aminu-exercising-10183800-player-option-with-bulls)는 계획 보도다. |
| ‘2019 Aminu–Chicago 계약’, ‘Chicago가 Herbert 지명’이라는 전제 | **사실 오류로 기각** | Aminu의 [2019 계약은 Orlando와 체결](https://www.nba.com/magic/magic-sign-al-farouq-aminu-20190706)됐고, [G15F](../research/O15G15F_ORLANDO_OFFSEASON_BRANCH_COSTS.md)의 Herbert33 후보도 Orlando 픽이다. 이 잘못된 전제로 정본을 고치지 않는다. |

**독립성 한계:** Claude는 초안만 봤고 2019 계약서나 실제 리그 옵션 통지를 확보하지 않았다. 이 검토를 사실 출처나 G16 전체 독립 검수로 세지 않는다. 별도의 결과물 단독 검수는 [R02](R02_O15G15K_SOURCE_BLIND_REVIEW.md)에 기록한다.
