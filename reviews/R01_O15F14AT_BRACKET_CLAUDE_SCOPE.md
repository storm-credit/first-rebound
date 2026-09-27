# R01 O-15F14-AT — K1/L2 대진 제한 반증

- 범위: Claude CLI에 F038 서부 1~10번과 L2 세 경기 승자, NBA 1–8/2–7/3–6/4–5 규칙을 **텍스트로 제공**해 논리 검토했다. 저장소 원본 JSON·NBA 원문을 Claude가 직접 읽은 독립 출처 검증은 아니다. 선행 저장소 읽기 요청은 응답 없이 중단했고, 두 번째 범위 제한 질의만 결과를 얻었다.
- 확인: Claude는 UTA–MEM, PHX–POR, DEN–LAL, LAC–DAL의 네 1라운드 짝을 반환했다. 원역사 Denver–Portland 1라운드 6경기·Denver–Phoenix 2라운드 4경기를 K1+L2의 경기별 실행 증거로 쓰지 말라는 판정은 채택했다.
- **기각:** Claude는 “Denver–Portland는 이 대진에서 어느 라운드에도 없다”고 단정했다. Denver가 Lakers를 이기고 Portland가 Phoenix를 이기면 **2라운드 Denver–Portland가 가능**하다. Portland의 Phoenix전 패배를 확정한 오류이므로 그 문장을 기각하고 [대진 문서](../simulation/CHICAGO_2020_21_K1_L2_BRACKET_BRIDGE.md)에 두 2라운드 갈래를 명시했다.
- 추가 한계: 동일 상대가 2라운드에서 재등장해도 원역사의 날짜·순서·홈코트·분·득점·부상을 그대로 복사할 수 없다. K1/L2는 `selected=false`의 조건부 입력이다. 본 검토는 F5·A3·K_METHOD_EVENTS 통과나 G16 독립 감리를 뜻하지 않는다.
- 도구 구분: 신규 외부 증거 수집이 없으므로 Antigravity·NotebookLM은 `NOT_RUN`; Codex가 두 원본 JSON을 재현 도구로 대조했고 NBA 공개 규칙을 별도로 확인했다. Claude는 제한된 논리 반증이며 그 출력의 과잉 결론을 Codex가 바로잡았다.
