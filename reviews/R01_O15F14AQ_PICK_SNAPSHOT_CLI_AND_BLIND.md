# O-15F14-AQ — 구단 픽 스냅샷의 도구별 검문

- 범위: [원역사 픽 출처·조건부 계산](../simulation/NBA_2021_ASSET_CHAIN.md). `F2/F3=HOLD`.

| 단계 | 실제 실행 | 증거 한계 |
|---|---|---|
| Codex 원자료 | Orlando 구단의 [2021-06-10 기사](https://www.nba.com/magic/news/orlando-magic-have-great-opportunity-add-several-quality-players-through-draft-next-few-years-20210610) 공개 HTML에서 픽 열거 문단을 직접 판독. BOS/MEM 2025 뒤 2R, BOS 2027 2R, DEN 2025 top5 1R 확인 | 구단 편집 기사이며 3/25 원계약·전체 보호/우선권/미전달 종료 문구가 아니다. |
| Antigravity CLI 수집 | 설치 절대경로 `agy.exe -p ... --print-timeout 45s --output-format json` 실행. `read_url_content`가 기사 본문 대신 추적 스크립트만 반환했다고 답함 | `status=SUCCESS`는 기사 수집 성공이 아니다. 이번 본문 증거 **0건**. |
| NotebookLM CLI 분석 | URL 소스 직접 추가는 `Could not add url source` 실패. 처음 붙인 여러 줄 텍스트도 실제로는 URL 한 줄만 저장돼 삭제했다. 이후 **Codex가 옮긴 요약**을 단일 줄 pasted-text 출처 `e8b7b235-cff2-455f-961b-8c2bb56f9f5c`로 저장하고 `nlm content source`에서 515자를 확인한 다음 해당 출처만 질의 | 세 픽 요약과 빠진 조항을 반환했지만 NBA 본문을 독립 판독한 것이 아니다. 원자료 증가 **0건**. |
| Codex 원장·재현 | `research/NBA_2021_L_ASSET_CHAIN_SOURCES.json`에 구단 스냅샷을 추가하고 `tools/build_2021_asset_chain.py`의 결과 필드와 UTF-8 입출력을 재현. 기존 6개 검사를 통과 | 원역사 픽 권리의 1차 보강만 반영. 대체세계 최종 지명·정확 F2/F3는 미선택. |
| Claude source-blind 반증 | 이전 원문/분석 없이 결과 요약만 `haiku --tools '' --max-turns 1`로 제공 | 3/25 우선권과 후속 시뮬레이션의 미확인 조항이 HOLD인지 확인하라는 지적 수용. 실제 기사 직접 조회는 하지 않았으므로 “Codex도 요약만 읽었다”는 추정은 기각. 2021년 6월 기사를 “June 2025”라고 부른 날짜 오류도 기각. |

동일한 NBA 기사 하나를 Codex·두 CLI·Claude의 독립 원자료 네 건으로 세지 않는다. `BOS_2027_2R_full_priority_and_terms_verified=false`, `gordon_after_preceding_conversion=null`, `gordon_terminal_conversion=null` 및 미래 결과 미선택을 재현 JSON에서 유지한다. 구단 기사가 묵언한 것을 ‘보호 없음’으로 읽지 않는다. F `0/5`, A `0/3`, K `0/4`, 7행 1완료·1진행·5대기·미완료 6개, freeze v0.30 PARTIAL·설계/원고 `CLOSED`.
