# 2021–22 Chicago 위임 건강·가용성 작업 선택

상태: `AUTHOR_DELEGATED_DESIGN_SELECTION_PROPOSED_WITH_82_DATE_STATES_EXECUTED_FOR_ROOT_REVIEW`. M1 carrier의 82개 날짜에 **NORMAL 58개 / COBY_OUT 24개**를 배정했다. Chicago의 양수 분 선수와 12명 작업 명단도 각 날짜에서 같은 선택 행에 연결했다. 이는 가상 운영 선택이며 실제 의료 판정이나 법적 명단 인증이 아니다.

## 실제 역사와 선택을 분리한 지점

- 2021-11-14 NBA 공식 부상 보고서 3쪽은 Coby White를 Out(왼쪽 어깨 관리)으로 적는다. 원 PDF 36,062바이트 SHA-256 `ff6dbd0355dd063026af4d93d857d32d41bf38e22ae467f55a4cbe0c14bfb8ee`를 임시 캐시에 회수했다.
- 실제 11월 15일 Lakers전 Coby의 출전은 10:57이다. 11월 17일 10:29, 19일 10:54도 기존 관측 원장에 있다. 선택한 `COBY_OUT`은 이 세 실제 출전을 부정하지 않는다. 대체 세계에서 18분짜리 기존 NORMAL 역할을 아직 쓰지 않고 **결장을 3경기 연장하는 별도 가상 선택**이다.
- 11월 21일 원장의 실제 출전은 20:59로 첫 NORMAL 선택의 보수적 역할 기준이다. 이후 미출전일을 임상 사유로 단정하지 않고 운영상 비가용으로 모델링했다.
- NBA 게임 페이지의 10:57은 검색 색인과 기존 원장에서 교차했으며 페이지 원바이트는 HTTP 403/iframe 때문에 확보하지 못했다. 원바이트 인증으로 주장하지 않는다.

## 비교와 범위

- **권고 58/24:** 첫 13경기 OUT, 실제 제한 출전 3경기에는 명시적 대체세계 OUT, 11월 21일부터 출전 앵커가 있는 날짜 NORMAL, 이후 미출전/제한 8경기 OUT.
- **61/21 대안:** 실제 첫 3회 출전을 보존하지만 10분대 관측에 기존 18분 NORMAL을 곧바로 대입한다. 이번에는 선택하지 않았다.
- **69/13 대안:** 첫 13회만 OUT이며 이후의 원장 미출전·제한일도 NORMAL로 놓는다. 기존 원장에 비해 근거가 약하다.
- LIMITED 신규 상태는 이후 donor·5인 블록·명단을 새로 계산하면 가능하다. 현재 82일 상태 연결을 위해 필수 조건으로 만들지 않았다.
- 상대 29팀 가용성은 `NOT_MODELED` typed null이다. Chicago 외 건강·승패·연장·전 경기 시간순 5인 교대·실제 계약/의료·원고 허가는 모두 미완료다. 15+2는 기존 조건부 carrier의 작업 명단이다.

## 출처

- [NBA 2021-11-14 공식 부상 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-11-14_05PM.pdf), 3쪽.
- [NBA Bulls 2021-11-15 경기표](https://www.nba.com/bulls/game/0022100209-bulls-vs-lakers-los-angeles-ca-11-15-2021): 공식 검색 색인 10:57, 원바이트 미회수.
- [Bulls 복귀 전망 공지](https://www.nba.com/bulls/news/coby-white-and-patrick-williams-injury-updates): 정확 복귀 허가로 사용하지 않음.
- 날짜별 JSON의 `selected_carrier_source.pointer`가 기존 M1 조건부 행으로 연결된다. 원천 파일의 정규화 SHA-256은 JSON `source_hashes`에 기록했다.

