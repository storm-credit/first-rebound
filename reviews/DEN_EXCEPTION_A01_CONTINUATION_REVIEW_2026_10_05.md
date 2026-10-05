# Denver 역사 상한·A01 입문 인과 후속 검수

기준 main `9391fab` / PR416 이후. 판정 **역사 기준 상한 확보 / A01 국소 핵심 3단위 대조 완료 / 대체세계 비용·최종 회차·실제 Pack HOLD**.

## 2번 — null이던 역사 상한을 채운 근거

[초기 수집 패킷](../research/DEN_2020_EXCEPTION_EXECUTION_EVIDENCE_2026_10_05.md)의 계획 보도와 서명만으로 실제 예외를 인증하지 않았다. 그 뒤 [3/22 후속 보고](https://bleacherreport.com/articles/2937467-ranking-every-nba-team-by-its-trade-asset-war-chest)를 직접 읽고 국소 독립 검수자가 적용 상태의 공개 근거로 채택 가능하다고 판단했다. 일반적인 반올림값을 정확액으로 바꾸지 않는다.

[역사 상한 원장](../research/DEN_HARDCAP_POST_SIGNING_REPORT_2026_10_05.json)은 정확 금액을 별도 계보에 연결한다.

1. [NBA 2019 공식 발표](https://pr.nba.com/nba-salary-cap-for-2019-20-season-set-at-109-140-million/)와 [2020 합의 발표](https://pr.nba.com/nba-nbpa-2020-21-season/)의 cap은 모두109,140,000, 2020 tax는132,627,000이다. [후속 이사회 승인](https://pr.nba.com/nba-board-of-governors-approves-adjustments-to-collective-bargaining-agreement/)과 양측 수정 전문의 차이도 보존했다.
2. [NBA 작성 October2019 CBA101 원문 미러](https://nyc3.digitaloceanspaces.com/sportsarchive-documents/prod/63f2840a2a9ad/2019-20-CBA-101-October-2019.pdf) PDF10의 이전 apron offset은6,301,000이다. 공식 호스트라고 표시하지 않는다. 공개 정밀도는0.001million이다.
3. 공식2017 CBA PDF240의 cap변화율 절반 조정에서 cap변화0이므로 offset 유지: `132,627,000 + 6,301,000 = 138,928,000`.

별도 Codex `independent_finish_scope`가 실제 원본문·숫자 출처·PDF를 대조했다. 특정 역사 상한에 한정한 **S2 공개 근거 기반 법적 추론**을 계수할 수 있으며, 2020 수정 전문 미회수만으로 이 연결을 계속 차단할 필요는 없다고 판정했다. 정확 리그 장부·예외 접수증이나 다른 개정 조항 인증으로 표시하지 않는다. web본문 회수와 로컬HTTP403도 원장에서 구별했다.

[비교 생성기](../tools/build_den_f5_cost_comparator.py)는 이 원장을 실제 입력에 연결한다. `HIST_UPPER`와 그 한정 근거 확인을 채웠다. Gordon/Clark 보너스 차이 및 전체 `DELTA_OTHER`는 여전히null이다. 공통 계약 선언만으로 거래 보너스 발생·배분·포기 동의를0으로 처리하는 방식은 S2 전체 구간 증명을 대신하지 못한다. F3 중간 거래 순서·matching·픽까지 확대하지 않는다. **대체 비용 법적 추가PASS0**.

## 6번 — 확정 입문 핵심의 3단위 연결

- [기존 오프닝](../design/A01_OPENING_BLUEPRINT.md): 제안 종료까지4 Beat·5주장. 검사에서 이후 상태 메모로 freeze·gate 지문2개가 STALE임을 발견했다. 실제 diff와 잠긴 v0.7 핵심/CLOSED 조항을 재대조하고 최종 지문을 갱신했다. 사건을 다시 설계하거나 승인하지 않았다.
- [첫 체험](../design/A01_FIRST_TRIAL_BLUEPRINT.md): 첫 훈련 참여→동갑 첫 완패, 2 Beat·정본3주장·추론3개. 참여에서의 제한 수락은 학교 조건 완료와 구별한다.
- [첫 기여](../design/A01_FIRST_CONTRIBUTION_BLUEPRINT.md): 자존심 잔류→리바운드·아웃렛·팀득점→팀에 필요하다는 자기 느낌, 3 Beat·정본5주장·비용 추론2개. 리바운드/패스/득점을3회차로 부풀리지 않는다.

독립 Codex `nba_legal_next`가 새 두 파일·Story Bible·책임 성장축·freeze를 직접 읽고 검문했다. 숨은 대사·동작·점수·학교 허가·게임 삭제·기술 완성·타인 속마음 승격은 발견하지 못했다. **명료화1건 수용:** 책임 성장축의 패배 다음날 자발적 재방문은 알려진 상대시간으로 보존하고 C1과의 정확 대응·달력 날짜만 미정으로 분리했다. 부모가 실제 수정·원본 대조를 완료했다.

현재성 검사기를 세 국소 단위에 적용하고 검수 본문 지문·원본 지문·전 단위 종료→다음 진입을 함께 대조한다. 이3단위는 A01의 이미 확정된 입문 핵심이며 전체 한국 단계·36슬롯·최종 회차 기능표·씬 구현·G13/G14 사용 권위의 완료는 아니다.

## V2 실제 실행

| 도구/단계 | 결과 |
|---|---|
| Antigravity | 68.699초 종료0·검색4단계DONE·terminal SUCCESS지만 답변빈값/회수false. [실제 기록](DEN_EXCEPTION_AG_2026_10_05.json). 직접 수집한 원문을 AG 회수라고 세지 않음 |
| NotebookLM | 초기 파생 패킷 등록13.376초, 단일 지정출처 질의34.068초 회수·인용3개. [등록](DEN_EXCEPTION_NLM_SOURCE_2026_10_05.json) / [응답](DEN_EXCEPTION_NLM_2026_10_05.json). 후속 역사 상한 입력 이전 분석이며 독립 원자료 증가0 |
| Codex | 원자료 직접 수집/숫자 연결/비교식/인과 단위 및 지문 대조 |
| 독립 Codex | 역사 상한의 한정 증거 연결, 새 두 국소 설계 실제 파일 반증. 전체 설계 source-blind 검수를 대체하지 않음 |
| Claude | 기존 SESSION_USAGE_LIMIT 이후 이번 NOT_RUN |
| 전체 source-blind | NOT_RUN / G16 전체 미완료 |

## 남은 범위

법적2완료/10HOLD·F0/5 A0/3 K0/4·2020–21 전체 실행HOLD. 최종 회차 기능0·실제Pack0·국소 핵심 Blueprint3·미완료 큰묶음6. freeze v0.30 PARTIAL·설계/원고CLOSED·새 작가확정0·원고0. 다음 비용 종료 증인은 **확보한 역사 상한에 더할 모든 비공통 차액 상단**이다.
