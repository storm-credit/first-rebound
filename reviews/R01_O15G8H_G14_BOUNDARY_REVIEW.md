# O-15G8H / G14 경계 검토 — 2026-09-28

- 범위: M1 뒤 Chicago 2021 여름 A 방향의 정본 기록과 CP2 설계 샘플의 내용 무결성.
- 분류: `INTERNAL_SECOND_READER / NOT_G16_INDEPENDENT_REVIEW`.

## 확인

1. 사용자 응답은 `A: Caruso·성장 코어 (권고)`이다. M1은 앞선 별도 선택이다. A/C/D 중 A의 **방향**만 작가 선택으로 기록하고, Caruso·Green 등 개별 선수 수락·SQ1·명단·cap·시즌은 HOLD로 보존했다.
2. 기존 CP2 검사는 출처 해시와 용도를 검사했으나 `allowed_facts` 변조, 루트/샘플 `author_locked=true`, 중복 `source_links`를 통과시켰다. 내부 검토자가 메모리 변조로 이 반례를 재현했다.
3. 수정된 검사는 현재 소스에서 생성한 설계 샘플의 본문과 저장된 본문을 비교하고, 작가 잠금과 출처 중복을 검사한다. 허용 사실 변조·작가 잠금·중복 링크를 대상으로 한 회귀 검사 2개를 추가했다.
4. A06의 A 선택은 2020–21 결과에 소급하지 않고, A13의 선택은 2028 Caruso/Green 소속이나 실제 계약 수락을 정하지 않는다.

## 검증과 한계

`python tools/build_cp2_design_packets.py --check`, `python tools/test_cp2_design_packets.py`(9개), `git diff --check` 통과. 샘플 2개의 출처·생성 내용 일치만 증명하며, 전체 780회차 기능표·실제 회차 Pack·G11 딥리드·독립 원고 검수는 아니다. Anti-Gravity·NotebookLM·Claude·source-blind는 이번 변경에 `NOT_RUN`; 같은 자료를 반복 검토한 횟수로 독립성을 주장하지 않는다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED` 유지.
