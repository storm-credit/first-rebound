# R01 O-15F14-AU — DEN–LAL 비교 입력의 도구별 검수

| 역할 | 실제 범위 | 처분 |
|---|---|---|
| Antigravity 수집 | 절대 경로 `agy.exe`에 NBA 5/3 박스 URL 본문을 `read_url_content/view_file`로 읽도록 요청했다. 45초 print timeout, `status=SUCCESS`, `response=""`, 사용 토큰 0. | **본문 증거 0건.** CLI 실행 성공을 출처 수집 성공으로 세지 않는다. |
| NotebookLM 출처 연결·한정 분석 | 비정본 F4/F5 작업실 `a3f30584-3a9d-4a8b-8960-b661615d98e9`에 NBA 공식 5/3 경기책 파일을 출처 `70328aad-7ab8-4858-beca-7f27216d317d`로 추가. 새 대화 `b318d850-5fb6-42e9-898c-887759f0be82`에서 **그 출처만** 질의했다. | Lakers 93–89, McGee 12:24, Nnaji·James·Schröder 결장, Davis 33:06을 1쪽에서 인용했고 Codex 직접 판독과 일치했다. **같은 공식 PDF의 재독**이지 새 독립 출처가 아니다. 5/22·23 PDF는 NotebookLM 분석 범위 밖이다. |
| Codex 출처·저장소 | NBA 공식 5/3 DEN–LAL, 5/22 POR–DEN, 5/23 LAL–PHX 경기책의 최종 박스/Inactive 행을 직접 대조. 저장소 F5 국소 JSON의 5/3 McGee 치환 `744초`와 두 점수차를 확인. | 원역사 사실과 단일 경기 국소 민감도만 통과. 대체 시리즈의 건강·5인조·승패는 `HOLD`. |
| Claude 제한 반증 | 처음엔 긴 문서 단독 요청이 응답 없이 중단됐다. 이어 **출처를 직접 보지 못한다고 밝힌** 짧은 사실 요약만 전달해 논리 반증을 받았다. | May 3 원역사 승리/분과 POR·PHX 상대 플레이오프 기용을 DEN–LAL 새 시리즈로 이식하지 말라는 결론을 채택. “McGee 12:24는 Hartenstein/Bey에게 속한다”는 문장은 **자동 분배 근거가 없으므로 기각**. James/Schröder가 새 시리즈에서 반드시 출전한다거나 May 3의 Lakers 홈 경기가 모든 새 경기와 홈코트가 다르다는 단정도 채택하지 않는다. |

Claude의 제한 응답은 원문/JSON 독립 확인이나 G16 감사가 아니다. 위 세 공식 PDF를 세 **역사적 관측 경기**로만 세며, 같은 문서를 여러 도구가 읽은 횟수를 원자료 건수로 부풀리지 않는다. 결과물 단독 source-blind 검수는 이번에 별도로 수행하지 않았다. F5·A1/A3·K_METHOD_EVENTS와 2번 매크로는 계속 `HOLD`; `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`.

직접 회수한 공식 PDF의 SHA-256: `20210503_DENLAL` `2afee840cc5a9899bb485ea59aa51d8c394e3752fec948109e87c18cd6e5386a`; `20210522_PORDEN` `23362aa3f7b3332e543ea28d25e9aff54d5ddb89d97a29801e71f4e829bc10d1`; `20210523_LALPHX` `f6dea38257ed7d83ea210d1f1e87a7734c38c08dc01eed8c574deed0f81d60ca`. 임시 회수본 자체는 저장소에 추가하지 않는다.
