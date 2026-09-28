# G11/G14 문서 단독 맹점 검수 — 2026-09-28

- 범위: 검수자에게 `design/HOUSE_STYLE_FOUNDATION.md`와 `context-packs/README.md` 두 문서만 제공했다. 독서 원장, CP2 샘플 JSON, 생성기, 이전 검토 결론은 제공하지 않았다.
- 성격: 결과물에서 의심할 지점을 찾는 source-blind 1회. NBA 원자료 독립 조사나 G16 전체 설계 검수는 아니다.
- 판정: **부분 수용 / G11·G14 FINAL_HOLD 유지**. 아래의 지적을 정본·코드와 다시 대조한 뒤 수용 범위를 나눴다.

| 문서 단독 지적 | 대조 결과와 처리 |
|---|---|
| 설계 샘플과 실제 회차 Pack, 닫힌 게이트의 표시가 YAML 목록에 명시되지 않음 | **표현 결함 수용.** 실제 `CP2_DESIGN_VALIDATION_SAMPLES.json`과 생성기는 `purpose=DESIGN_VALIDATION_ONLY_NOT_EPISODE_PACK`, 최상위 `actual_episode_packs=0`, 샘플·최상위 `manuscript_allowed=false`, `author_locked=false`를 이미 검사한다. `context-packs/README.md`의 현재 샘플 설명에 표시했다. 코드 결함으로 세지 않는다. |
| 주장별 출처가 해시에 어떻게 연결되는지와 상태 허용값이 불명확함 | **문서 결함 수용.** 생성기는 `allowed_facts`의 문구·순서와 `fact_evidence.claim`을 일치시키고, `source_paths`를 해시 고정된 `source_links`에 연결하며 `CANON_FUNCTION/CANDIDATE/CONDITIONAL_RESULT`만 허용한다. README에 이 매핑과 해시 검사의 한계를 명시했다. |
| 스타일 관찰·누적 독서 주장에 이 두 문서만으로 확인할 수 있는 회차별 증거가 없음 | **검수 범위에 따른 미검증으로 유지.** 전체 접근·독서 원장은 `research/STYLE_REFERENCE_ACCESS.md`, 회차별 관찰은 `research/STYLE_READING_OBSERVATIONS.json`, 기능 비교는 `research/STYLE_FUNCTION_COMPARISON.md`에 있다. 이 검수자는 해당 원장을 읽지 않았으므로 85/110 독서를 독립 확인한 것으로 세지 않는다. |
| 문단·대화 등 원고 규칙의 실제 적용 검사가 없음 | **사실.** 원고·대사 샘플은 0개이고 설계/원고 게이트가 `CLOSED`다. 집필 후 검사는 후행 항목으로 남기며 원고 샘플을 만들지 않는다. |
| S1 제한 시점의 전환 규칙이 Context Pack 검증에 없음 | **후행 검증 필요.** 현재 두 CP2 팩은 설계 샘플로 단일 `pov_character` 값만 검증한다. S1은 추천이지 정본 시점 잠금이 아니다. 실제 회차의 경계·정보 경로가 정해진 뒤 전환 근거를 별도 필드/검사로 설계한다. 현행 샘플에 가상의 시점 전환을 추가하지 않는다. |

이 검수의 수용 항목은 README의 의미 명시 2건이다. CP2 샘플 내용, NBA 역사 사실, 작가 선택, 원고 허가를 바꾸지 않는다. `PROJECT_FREEZE v0.30 PARTIAL`, G11·G14 최종 `HOLD`, G16 전체 독립 검수 미착수, 실제 회차 Pack 0개, 설계/원고 `CLOSED`를 유지한다.
