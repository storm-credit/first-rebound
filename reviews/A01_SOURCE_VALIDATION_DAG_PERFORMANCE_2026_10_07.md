# A01 출처 검문 DAG 중복 수리 — 한정 성능 감사

[검문 기록](A01_SOURCE_VALIDATION_DAG_PERFORMANCE_2026_10_07.json). 기준 main `75a1d526e78ef53fbf3e72fa7cad8899a57debf9`의 작업 변경이다. 기존 E4~E9 생성기 6파일만 수리했으며 이야기·작가 선택·중앙 상태를 변경하지 않았다.

## 원인과 실제 수리

각 final E_n은 직전 E_(n-1)을 직접 검문하고 CF도 검문했다. CF.build가 같은 직전 E를 다시 전체 검문하므로 한 단계마다 조상 호출이 두 배로 반복됐다.

중복된 직접 predecessor.validate만 제거했다. `previous == working.load(root, predecessor.OUTPUT)` 전체 객체 대조를 추가하고 CF.validate의 전체 출처 재구성·조상 검문을 유지한다. 두 독립 loader가 같은 exit만 유지하면서 다른 필드를 바꿔도 거부한다. 캐시·mtime 지름길·해시 생략0이다.

| E9 한 번 build 측정 | 시간 | build/validate 호출 | 결과 |
|---|---:|---:|---|
| 수리 전 실제 저장 입력 | 3.410초 | 1,147 | VALID |
| 수리 후 파생 지문11개 메모리 재현 | 0.140초 | 39 | VALID |
| 루트 지문 갱신 후 실제 저장 입력 | 0.096초 | 39 | VALID·저장 E9 전체 객체 일치 |

초기 E1/E2/E3 각 build64→1, trial160→3, followup96→2다. 세 측정은 단일 제한 실행이고 import 시간은 제외했다. OS cache 상태를 통제한 분포 실험이 아니며 전체 CP2 테스트 시간이나 이후 함수 전체 성능을 인증하지 않는다. 최종0.096초 측정은 실제 저장 파일을 읽었고 출력의 전체 객체가 저장 E9와 정확히 같았다.

## 의미와 실패 제어

E4→CF08→E5→CF09→E6→CF10→E7→CF11→E8→CF12→E9의 정확11개 파생 객체를 메모리에서 현재 지문으로 재현했다. 재귀 객체에서 `source_rev_sha256`/`source_sha256`만 제외하면 모든 나머지 필드가 이전 저장 결과와 같았다. 이 에이전트의 파생JSON 파일 수정0이다. 루트가 실제 파생 지문을 한 번 갱신했으며 그 뒤 현재 E9를 직접 읽고 재구성했다.

- E4~E9 최종 exit 변조6건 모두 거부.
- E4 독립 loader만 E3의 non-entry `whole_g13_complete` 필드를 반전: 전체 객체 대조로 거부.
- 두 loader가 같은 잘못된 E3 exit와 새 raw SHA를 읽음: CF07의 원 source-current 검문으로 거부.

## 적용 조건

CF가 바로 그 직전 final 객체를 **실제로 load하고 validate**하는 경우에만 중복 제거가 성립한다. A02 E1은 CF01이 E9를 검문하므로 같은 수리가 가능하다. A02 E2의 CF02는 CF01을 검문하며 final E1을 검문하지 않으므로 E2의 E1.validate는 유지해야 한다. 두 read의 equality만으로 존재하지 않는 상위 검문을 만들 수 없다.

추가 cache utility는 작성하지 않았다. E10/E11·중앙 CP2·원장·staging/commit은 이 에이전트가 수정하지 않았다. 전체 G13/원고 허가를 바꾸는 작업이 아니다.

## 전체 진행표

[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md), 미완료 큰묶음6개. 이번 감사는 중앙 상태를 변경하지 않는다.

| 번호 | 작업 | 현황 |
|---:|---|---|
| 1 | 2020 드래프트 연쇄 | 완료 |
| 2 | Chicago 2020–21 | 법적12/12·F5/5; 유한 실행 연결 통합 검문 중 |
| 3 | 2021–23 거래·계약 | 승인 방향 보존·후속 정확 실행 미완료 |
| 4 | 장기 커리어 | 선행 연결 대기 |
| 5 | 결말·전체 구조 | 골격 완료·전체 기능표 미완료 |
| 6 | 집필 규격·Context Pack | 기능11/780·미배치769; A01 9/36·A02 2/54·실제Pack0 |
| 7 | 통합·독립·최종 승인 | 진행 중·CLOSED |

PROJECT_FREEZE v0.30 PARTIAL·설계/원고 CLOSED·원고0.
