# R01 — G15BL 계약 날짜·명단 검토 기록

- 대상: [G15BL](../research/O15G15BL_DETROIT_JAN23_STANLEY_CONTRACT_AND_HARDSHIP_GATE.md). 새 작가확정·정본/게이트 변경 0건.
- 검수 질문을 분리했다: Antigravity는 공식 페이지 수집, NotebookLM은 제한 출처의 날짜·상태 연결, Codex는 저장소의 명단 등급 대조, Claude는 문서만 본 독립 반증.

| 단계 | 실행·결과 | 채택 범위 |
|---|---|---|
| Antigravity CLI | 절대 경로 `agy.exe`에 Cruise 공식 호출 기록과 Detroit 1/16 구단 기사 두 URL만 제시. `--print-timeout 70s --output-format json` 실행은 `status=SUCCESS`였으나 `response=""`와 print timeout을 반환했다. | **본문 수집 0건**으로 기록. 정상 실행을 자료 확인 성공이라고 세지 않았다. |
| NotebookLM CLI | Cruise 호출 기록이 신규 출처 `093e5b2b-30d4-4c7c-8bd9-125345f8571f`로 수집됐다. 이 출처만 제한 질의해 Stanley의 12/25·1/8·1/21 각각 10일 계약과 급여/예외 정보 부재를 확인. 이어 공식 1/23 19:30 ET 부상 보고 출처 `c8189748-40fd-473a-afcc-f7cc35b396dd`와 함께 질의해 Grant/Olynyk 프로토콜, Garza/Frank 재적응 `Out`을 분리했다. Detroit 1/16 HTML은 이번 source add 응답에서 수집되지 않았다. | 공식 출처의 날짜·의료행 확인에만 사용. NotebookLM이 예외 승인 또는 대체 건강을 판정하지 않는다. |
| Codex 저장소 교차검사 | G15AF의 P0-B **10월 표준 16인**과 G15AB의 1/23 Stanley `10:37`, G15BK의 McGruder 거래 취소 분기를 연결했다. 기존 G15AF·G15AB·G15BK 검사기를 재실행하고 링크·diff를 확인한다. | Stanley 1월 긴급 계약은 10월 기본 한 자리 초과를 해결하지 않는다는 범위. 새 정확 명단이나 240분 증명 없음. |
| Claude 문서 단독 반증 | 외부 도구 없이 G15BL 문서만 제공. 핵심 인과에 blocker 없음. 10/20 기준 시점, `+1`의 출처, Pickett/Smith 상태 표현, 예외 증빙 문서의 명시를 지적했다. | 10/20은 G15AF의 개막 가정, `+1`은 Plumlee 잔류, Stanley를 투웨이로 재분류하지 않는다고 수정했다. 리그 승인·임시 규칙·대체 건강 명부를 필요한 증빙으로 명시했다. Golden State 경기 날짜는 결론에 필요하지 않아 추가 승격하지 않았다. |

잔여 `HOLD`: 1/21 계약서와 해당 COVID 긴급 allowance 승인·급여, 대체 2021 계약/표준 15인 해소, 대체 1/21·1/23 건강 및 활동, Stanley의 실제 역할·분·공격 비용. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`.
