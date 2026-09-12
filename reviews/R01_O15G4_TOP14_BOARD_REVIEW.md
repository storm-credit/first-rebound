# O-15G4 자체 검토 — 상위14의 네 순차 보드

`SELF_REVIEW / NOT_INDEPENDENT`. 선수 선택 입력은 공개 근거에 기초한 창작 제안이며 계산기가 구단 선호의 진실을 증명하지 않는다.

## 확인한 변경

G3 Moody 조건을 실제 선행 후보 비교로 좁혔다. DB1은 NOP9 Moody/CHI10 Duarte, DB2는 NOP9 Bouknight/CHI10 Moody, DB3은 GSW7 Moody/TOR8 Franz/NOP9 Giddey, DB4는 CHI10 Sengun이다. 네 안은 동시에 발생하지 않는다. 1~14를 순차 처리하며 각 선택 때 남은 비교 최소3명을 보존한다.

2020 정본에서 Detroit에 Patrick뿐 아니라 Kira16·Stewart19가 있고 Bey는 Denver에 있다는 점을 반영했다. Orlando는 Vucevic·Aminu·Nnaji를 유지하고 Carter/Hampton/Chicago1R을 얻지 않았다. Toronto Powell 잔류·Washington Trent/Brown 잔류, NOP Hayes 보유도 반영했다. 실제 구단 소개의 반대 로스터를 복사하지 않는다.

## 검사와 제한

- 신규5개 unittest: Chicago 후보 선점, 모든 비교 후보의 가용성, 중복/비교 부족 거부, 같은10순위 예산/센터 재설계 분리, 전체드래프트/추첨/최종정본 오승격 방지.
- 최초 실행에서 M의 원소유 순서를 문자열로 읽은 스키마 오류를 발견했다. 실제 `pick/origin` 객체와 `MIN_first.owner`를 읽도록 고쳐 다시 통과했다. 선행 M 파일은 수정하지 않았다.
- 56행 중복 없음·15자리 유지·CHI10 비용 차이0. 미래 계약·옵션·경기력은 이 결과가 아니다.
- 15~60의46픽과 CHI39 가용성은 미판정. DB1의 Ziaire/Sengun 등 추적 후보를 하류에 남겼으며 전체 나비효과 닫힘을 주장하지 않는다.
- 비공개 의료/워크아웃/내부 보드와 새 감독 사건은 HOLD. 실제 후대 NBA 성과를2021 선택 근거에 사용하지 않았다.

JSON 재현·diff 검사·기존 설계 Pack 해시를 게시 전 확인한다. 원격 CI 조회는 로컬 검증과 별도로 보고한다. 최종 author/season/exact/manuscript false, v0.30 PARTIAL·설계/원고 CLOSED, 남은큰작업6개.
