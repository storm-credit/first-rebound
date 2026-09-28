# R01 O-15F14-AX — 결과 비공개 서부 대진 산술 반증

- 범위: Claude CLI에 F038 서부 상위 10팀의 승수·기존 동률 순서, BOS/IND 승수, L2 플레이인 결과, NBA 1–8/2–7/3–6/4–5 규칙, 두 날짜의 **가정된 한 경기 반전**만 제공했다. [AX 결론 문서](../research/O15F14AX_DEN_LAL_SEED_CAUSAL_SENSITIVITY.md)와 생성 JSON·코드는 제공하지 않았다. CLI `-p --max-turns 1 --output-format text --no-session-persistence`, 읽기/수정 도구 사용 없음.
- 독립성: **주어진 숫자의 산술·대진 논리**에 한정된 결과 비공개 검문. 승수·날짜·NBA 규칙의 독립 원자료 확인이나 완성 설계 G16 검수는 아니다.

| Claude의 검토 요지 | 처분 |
|---|---|
| 4/15 BOS–LAL 반전: DEN 3–DAL 6, LAL 5, Denver가 이기면 PHX/POR 승자 가능 | **수용.** [F038/L2 입력 재현](../simulation/CHICAGO_2020_21_K1_L2_SEED_SENSITIVITY.json)과 일치. 새 승수 동률 없음. |
| 2/14 LAL–DEN 반전: LAC 3, DEN 4–LAL 5, Denver가 이기면 UTA/MEM 승자 가능 | **수용.** 같은 재현 결과와 일치. 새 승수 동률 없음. |
| DEN/LAC 47승의 기존 동률 순서가 4/15 시험에서 새로 결정적이고 이전에는 사실상 무의미했다는 설명 | **기각.** 기존 F038 자체가 DEN 3·LAC 4여서 3–6/4–5 상대와 브래킷 절반을 이미 결정했다. 4/15에 새 동률이 생긴 것은 아니다. 이 시험은 기존 순서를 그대로 쓰며 별도 타이브레이커 증명으로 승격하지 않는다. |
| 제한된 입력만으로 BOS 35승이 동부의 다른 팀과 동률인지 모른다는 유보 | **범위 제한.** CLI 프롬프트에는 동부 전체 승수를 주지 않았다. 실제 [F038 전체 입력](../simulation/NBA_2020_21_FULL_SEASON.json)에서 IND 34, WAS 33, CHI 31 등이므로 BOS 35의 새 동률은 없다. 생성 도구는 전체 F038 동부를 검사한다. |
| 반전 가정은 Davis 건강·경기 점수·플레이오프 승자를 증명하지 않음 | **수용.** A1/F5/K의 `HOLD` 유지. |

Codex는 [2/14](https://statsdmz.nba.com/pdfs/20210214/20210214_LALDEN_book.pdf)·[4/15](https://statsdmz.nba.com/pdfs/20210415/20210415_BOSLAL_book.pdf) NBA 공식 경기책과 F038/L2 저장소 입력을 별도로 확인했다. Claude가 동일 원자료를 다시 읽은 것은 아니며, 이번 검수 수를 NBA 출처 증가나 `G16 PASS`로 세지 않는다. 결과 판정: **두 반전 산술 수용, 과장된 동률 설명 기각, 건강/결과 HOLD**.
