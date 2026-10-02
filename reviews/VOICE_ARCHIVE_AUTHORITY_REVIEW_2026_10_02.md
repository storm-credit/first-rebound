# 인물 관계·음성 문서의 폐기 분기 권위 교정

- 기준 main: `0af8c586e31c4c148efaa163048003cbd34c55bb`.
- 대상: [Player Relationship & Voice Model](../design/PLAYER_RELATIONSHIP_VOICE_MODEL.md).
- 문제: 문서 상단은 Chicago 원클럽이 우선한다고 이미 말했지만 §4의 ‘정본 관계’ 표는 Trae를 장기 핵심 동료로 제시하고 Indiana 뒤에 ‘현재 팀도HOLD’라고 썼다. §10~11의 Atlanta 개발 감사·College Park 미참가/운용도 개별 절만 읽으면 현행 주인공 경로로 오인할 수 있었다. `HOUSE_STYLE_FOUNDATION.md`는 이 문서를 적용 권위로 참조한다.

## 수정 범위

1. Trae/Huerter/Collins 세 관계 행을 폐기 Atlanta 비교안으로 명시했다. 해당 선수의 실제 농구·과거 조사 기록은 삭제하지 않았고 새로운 상대/친분으로 변환하지 않았다.
2. Indiana 동료안은 비선택 이력, 현행 팀은 승인된 Chicago 원클럽으로 교정했다. 장기 동료 기능 후보는 기존 Chicago–Minnesota 패킷을 참조하며 최종 패스 수신자HOLD와 고정 동료 결승득점·팀승리를 구분했다.
3. §3/10/11의 스태프·개발·G League·EVIDENCE_AUDIT_PASS를 Atlanta 역사 조사 범위로 제한하고 Chicago/Windy City 인증으로 이식하지 않도록 했다. §8의 세 선수 음성도 해당 분기 비교 후보로 한정했다.

기존 대학 관계·주인공 말투·실존 인물 방화벽·반복 트레이너 HOLD·2019 Kobe 접점은 보존한다. 새 NBA 사실0·작가확정0·새 인물 관계/지명/시즌0·원고0이다. 공통 writing §22의 파일 존재와 실행 권위 구분을 적용했다. 새 장면/문체 기계 비율이나 게이트를 추가하지 않는다.

## 검증 범위

- Codex: freeze/STORY_BIBLE/CAREER_TIMELINE의 Chicago 권위와 diff 대조, 변경행과 기존 상단 주의문의 일치 확인, `git diff --check` PASS.
- 현재 CP2샘플2 JSON과 생성기는 이 파일을 직접 source hash에 포함하지 않는다. House Style 문서 자체/42소막/샘플 사건은 불변이며 샘플 재생성으로 수를 늘리지 않았다. 직접 hash 미포함은 전체 전이 의존성 자동 검사 성공을 뜻하지 않는다.
- Antigravity/NotebookLM/Claude: 이번 문서 권위 교정 NOT_RUN. 새 외부 사실 수집·문체 기능 분석이 아닌 기존 승인과 구판 표기의 대조다. 과거 서비스 성공/timeout을 이번 독립 검수로 재계수하지 않는다.
- 전체 source-blind/G16: NOT_RUN.

별도 읽기 전용 Codex 감사는 지정diff의 문제0개를 보고했다. Freeze v0.27의Atlanta세관계 활성해제·기록보존, 기존대학관계, Chicago원클럽/최종수신자HOLD/고정결말, 역사감사범위를 대조했다. 이는 해당 문서의 제한 감사이며 전체PASS는 아니다.

## 전체 진행

| 번호 | 현재 진행 | 남은 항목 |
|---|---|---|
| 1 | 2020 드래프트 연쇄 완료 | 0 |
| 2 | Chicago2020–21 진행 | F0/5 A0/3 K0/4·법적12 HOLD·미선택 건강/시즌 |
| 3 | M1/G1A 승인 방향 반영 | 정확 계약·급여·등록·자산·시즌 |
| 4 | 17시즌 후보 골격 | 선행 시즌·수상·건강 확정 |
| 5 | 14막42소막780배분·5약속 연결 | 최종 회차 기능0 |
| 6 | 독서110/110·비교10/10·관계 권위 교정 | 정확P3/FULL_TEXT_FINAL/G11최종/S1최초 승인·실제Pack0(샘플2)·원계획 접근부채15 |
| 7 | 통합·독립·작가 승인 대기 | G15/G16/G17 |

미완료 큰묶음6. Freeze v0.30 PARTIAL·설계/원고 CLOSED 유지. 이 교정이 실제 문체 적용·6번 최종 종료를 뜻하지 않는다.
