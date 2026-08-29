# Project Freeze v0.18

- 상태: `PARTIAL_FREEZE`
- 변경 권한: 사용자 명시 승인
- 정식 제목: `HOLD`
- 태그라인 후보: 《처음 배운 것은 리바운드였다》

## 로그라인

한국 고교에서 농구를 늦게 배운 압도적 신체 재능의 소년이 미국 프렙과 NCAA를 거쳐 NBA에 도전하고, 개인의 재능이 아니라 팀의 마지막 선택을 책임지는 투웨이 포워드로 성장한다.

## LOCKED

### 장르와 현실 규칙

- 현실 역사 스포츠 성장 웹소설
- 회귀, 시스템, 빙의, 초능력 없음
- 실제 시대와 제도를 존중하되 주인공이 접촉한 역사 결과는 인과에 따라 달라질 수 있음
- 실존 기록은 출처 확인 전까지 정본에 넣지 않음

### 성장 불변값

- 시작 상태: 한국 고교에서 농구를 늦게 시작한 초보
- 초기 신장: 약 196cm
- 최종 신장: 약 203cm
- 초기 인식: 운동능력은 압도적이나 기술·전술·팀 이해가 부족한 빅맨형 원석
- 최종 선수상: 리바운드, 수비, 전환, 패스, 제한적 창조를 갖춘 다재다능한 투웨이 SF/PF
- 진로 구조: 주인공은 한국 고교 → 미국 프렙 고교 → 2017-18 Villanova NCAA → 2018 NBA Draft 30순위 Atlanta → NBA. 라이벌은 같은 한국 고교 → 장기 부상·재활 → 2018-20 Gonzaga NCAA → 2020 NBA Draft → NBA
- 언어/문화: 영어와 생활문화 경험은 있으나 미국 엘리트 농구의 계급·코칭·라커룸·스카우팅 문법은 새로 배움

### 중심 질문과 변화

- 중심 질문: **재능만 있던 사람이 팀의 마지막 선택을 맡길 수 있는 선수가 될 수 있는가?**
- 시작 상태: 공을 잡으면 자신이 끝내야 한다고 믿음
- 종결 상태: 승리를 위해 자신이 끝내지 않는 선택까지 책임짐

### 결말 불변 기능

NBA 파이널 7차전 마지막 국면에서 주인공은 수비에 성공하고 결정적 리바운드를 잡는다. 직접 영웅 슛을 강행하지 않고 전진해 더 나은 위치의 동료에게 패스한다. 동료의 결승 득점으로 팀이 승리한다.

정확한 시즌, 팀, 상대, 점수, 실존 선수 배치는 역사 시뮬레이션 전까지 고정하지 않는다.

## UNDER REVIEW

- 정식 제목
- 미국 프렙 이동 연도와 체류 기간
- 주인공의 2017-18 Villanova 초기 자격·입학과 실제 로스터 역할
- 결말 시즌

이전의 `1998 시작 / 2004 드래프트`와 2009 추천은 유효 정본이 아니다. `design/ERA_SELECTION.md`의 2018 E0가 v0.3 정본이다.

## 모티브 방화벽

- 《슬램덩크》: 농구 초보가 종목과 팀을 사랑하게 되는 성장 기능만 참고
- 데니스 로드맨: 위치 선정·박스아웃·볼 궤적 읽기 등 리바운드 연구 항목만 참고
- 《ONE GAME》: 현실 NCAA→NBA 경로와 장기 성장 기능 비교
- 《라스트 댄스 - NBA DREAM》: NBA 연재 보상과 시대 인지도 비교
- 금지: 참고작의 문장·장면 배열·대사·외형·관계·회귀 장치·실존 선수 인생 복제

## v0.3 LOCKED ADDITIONS

- NBA 입성: 2018 NBA Draft
- 코비 브라이언트의 2020년 사망과 팬데믹: 외부 고정축. 회귀나 구원 서사로 변경하지 않음
- 동년배 핵심 라이벌도 NBA에서 별도 성공: 당시안은 한국 엘리트 → 미국 명문 프렙 → Duke급 블루블러드 → 2020 1순위였으나, v0.13의 ACL·NCAA 레드셔츠 경로가 대체
- 주인공과 라이벌의 가치 분리: 주인공은 리바운드·스위치 수비·전환·연결, 라이벌은 1차 이점 생성과 득점
- 전술 변화는 배경 지식이 아니라 출전시간·역할·계약·플레이오프 생존을 바꾸는 성장축
- 한 Sub-Act에는 핵심 전술 문제 1개, 필요할 때만 보조 문제 1개

## v0.3 UNDER REVIEW

- 정확한 출생월·학년·재분류·NCAA 체류 기간
- 라이벌의 당시 프렙 학교·대학명 검토는 v0.13에서 프렙 폐기, v0.14에서 Gonzaga 선택으로 대체. 현행 HOLD는 2020년 실제 지명 팀·순번
- 2018 아시안게임은 v0.17에서 양 선수 불참·실제 동메달 유지로 해소. 2023 공동 도전 결과는 R09 HOLD
- 첫 NBA 팀은 v0.15에서 Atlanta로 해소. 파이널 시즌은 계속 `HOLD`

## v0.4 LOCKED ADDITIONS

- 천재성·BQ 상세 권위는 `canon/TALENT_BQ_MODEL.md`
- 주인공은 신체 천재로 먼저 발견되고 공간인지 천재성이 늦게 확장되는 대기만성형 농구 천재
- 초기 BQ는 순간 공간지각만 비범하고, 전술 언어·역할·선택 체계는 낮음
- 라이벌은 기술·전술·경기 운영이 일찍 발현된 조기완성형 농구 천재
- 둘은 약점을 보완해도 1차 창조와 2차 연결이라는 핵심 천재성을 서로 복제하지 않음
- 의미 있는 성장에는 실패→해석→훈련→비용→경기 검증→새 카운터 사슬이 필요

정확한 신체 수치·연도별 성장·학습 기간은 R02/R04 연구 전까지 HOLD다.


## v0.5 LOCKED ADDITIONS

- 주인공과 핵심 라이벌은 둘 다 1999년생 같은 학년이며 2015년 같은 가상 고교·농구부에서 출발
- 주인공은 공부와 규칙에 의미를 못 느끼고 꿈이 없는 저에너지·회피형 문제아로 농구를 시작한다. 평소에는 조용하지만 자존심이 긁히거나 승부가 시작될 때만 짧게 반응한다
- 라이벌은 같은 나이지만 기술·BQ·훈련 습관이 조기 완성된 엘리트
- 주인공은 2016년 미국으로 먼저 이동해 2017-18 NCAA와 2018 NBA Draft에 도전
- 라이벌의 당시 프렙→Duke급 경로는 v0.13의 2017 ACL→2018 NCAA 0경기 레드셔츠→2019-20 복귀 경로가 대체
- NBA 개발 기본 방향은 1라운드 후반 표준 계약과 G리그 배정. 이 v0.5 시점의 팀·픽 HOLD는 v0.15에서 Atlanta 30순위로 해소
- 반복 기술 지도자는 가상 트레이너 한 명, 코비 접점은 2019년 짧은 훈련 기능만 유지

## v0.5 RESEARCH_HOLD

- 1999년생 주인공의 정확한 생일과 2018 Draft 연령 계산
- 2017 미국 고교 졸업·한국 학점 이전·2017-18 NCAA 역사 자격
- 같은 고교와 미국 프렙의 실명·입학·비자·학사 조건
- 2018 Summer League·대표팀 일정 충돌은 v0.17에서 주인공 불참으로 해소. 2023 NBA 캠프 충돌은 R09 HOLD
- 2019 코비 훈련의 실제 접근 경로와 날짜

상세 연표 권위는 `canon/CAREER_TIMELINE.md`다.


## v0.6 LOCKED ADDITIONS

- 주인공이 체육관에 들어가는 외부 계기는 학교생활 사고 뒤 감독이 제공한 조건부 관리형 기회
- 농구부는 징계 회피 특혜가 아니며 출석·학업보충·훈련 준수가 유지 조건
- 주인공이 훈련에 남는 내적 동기는 같은 학년 엘리트 라이벌에게 완패하고도 경쟁자로 인정받지 못한 자존심
- 주인공이 농구에 정착하는 감정적 동기는 첫 리바운드와 아웃렛으로 팀에 필요해진 경험
- 첫 성공은 완성된 기술이 아니라 반복 학습을 시작하는 증거
- 정확한 사고·징계·담임/생활지도부/감독 권한과 첫 경기 종류는 R03 한국 학교 고증 전까지 HOLD


## v0.7 LOCKED ADDITIONS — v0.6 입문 계기 대체

- 주인공의 문제는 폭력·싸움·양아치 사고가 아니라 삶과 진로에서 이유를 찾지 못한 무목표 상태다.
- 무목표가 수업 회피로, 즉시 보상을 주는 친구·PC방·게임으로, 밤샘과 수면 붕괴로, 지각·무단결석으로 이어지는 순환을 사용한다.
- 게임은 단일 원인·중독 악역·농구 BQ 치트키가 아니다. 사회적인 놀이이자 현실 회피의 증상이며, 농구 입문 뒤에도 습관은 점진적으로 변한다.
- 체육관 진입 인과는 **만성 지각·결석 → 늦은 등교 뒤 체육관 관중석 회피 → 감독의 조건부 체험 훈련 → 동갑 라이벌에게 완패 → 첫 리바운드·아웃렛으로 팀 기여**로 잠근다.
- 감독은 우연한 운동 반응을 보고 체험 기회만 줄 수 있다. 담임·생활지도부의 출결·학업 처분을 없애거나 선수 자리를 보장하지 않는다.
- 농구를 계속하는 이유는 체육관에 숨을 곳이 생겨서가 아니라, 자존심과 첫 팀 기여를 거치며 처음으로 다음 날 학교에 올 이유가 생기기 때문이다.
- 정확한 결석 일수, 출석 경고 단계, 교내 권한 분담, 체험 훈련 허용 절차는 R03 한국 학교 고증 전까지 HOLD다.

v0.6의 '학교생활 사고 뒤 관리형 기회' 표현은 역사 기록으로만 남기며, 현재 입문 정본은 v0.7이 우선한다.


## v0.8 LOCKED ADDITIONS — v0.5 커리어 경로 대체

- 주인공은 NCAA에 진학하지 않는다. 미국 프렙 고교 졸업 뒤 2017-18 G리그에서 NBA 계약 전 프로 시즌을 치르고 2018 NBA Draft에 진입한다.
- 2017-18 주인공의 G리그 신분은 NBA 배정·투웨이·Ignite·Select Contract가 아니다. 리그 표준 계약과 선수 풀 경로를 사용하는 독립 G리그 선수다.
- 2018 Draft 뒤 NBA 소속으로 받는 G리그 배정은 프리드래프트 시즌과 구분한다.
- 라이벌은 한국 고교 최종 과정에서 장기 재활이 필요한 부상을 입는다. 계획적 프렙 1년은 폐기하고, 부상 회복 뒤 NCAA에서 복귀를 증명해 2020 Draft 전체 1순위 수준에 도달한다. v0.13은 ACL·레드셔츠, v0.14는 Gonzaga를 구체 경로로 잠근다.
- 라이벌의 정확한 부상 부위·2018-19 학적·대학명은 v0.13~v0.14가 대체했으며, 개별 의료·장학금·기록만 HOLD다.
- 부상은 동일한 실존·만화 장면을 복제하지 않으며, 시간 지연뿐 아니라 재활·몸 사용·경기 운영의 비용을 남긴다.
- 주인공의 학업 결핍은 사라지지 않는다. NCAA를 포기한 선택의 결과로 불안정한 급여·로스터 경쟁·성인 프로와의 경기 비용을 치른다.

v0.5의 '주인공 2017-18 NCAA'와 '라이벌 2018-19 계획적 프렙'은 현행 정본이 아니다. 상세 권위는 `canon/CAREER_TIMELINE.md` 현행판이다.


## v0.9 LOCKED ADDITIONS — v0.8 주인공 경로 대체

- 주인공의 2017-18 프리드래프트 G리그 경로를 폐기하고 NCAA Division I Villanova University 한 시즌으로 교체한다.
- 2017-18 Villanova의 실제 NCAA 우승은 유지한다. 주인공은 기존 핵심 선수의 기록과 공로를 빼앗는 에이스가 아니라 수비·리바운드·전환으로 성장하는 후순위 로테이션 선수다.
- Jalen Brunson은 주장·프로 준비 선배, Mikal Bridges는 포지션·수비 멘토, Donte DiVincenzo는 가장 가까운 대학 동료라는 공개적 농구 관계 기능만 사용한다.
- 실존 선수에게 검증되지 않은 사생활·악행·허구 명언을 부여하지 않으며, 한 경기에서 만난 상대를 자동으로 절친으로 만들지 않는다.
- 2018 NCAA 결승의 중심 공로와 Final Four MOP는 실제 기록을 유지한다. 주인공의 결정적 기여는 역사 시뮬레이션 뒤 한 경기·한 기능으로 제한한다.
- 주인공은 2018 NBA Draft 1라운드 후반 표준 계약을 기본 방향으로 유지한다. 드래프트 뒤 G리그는 필요시 NBA 소속 개발 배정으로만 사용하고 투웨이를 기본값으로 두지 않는다.
- Villanova 입학·NCAA 초기 자격, 한국·미국 성적표와 핵심과목, 장학금·리크루팅, 실제 로테이션 영향은 검증 전 HOLD다.

v0.8의 프리드래프트 G리그 경로는 역사 기록으로만 남기며, 현행 커리어 정본은 v0.9가 우선한다.


## v0.10 LOCKED ADDITIONS — 책임 성장축

- 농구는 주인공의 무기력을 즉시 치료하지 않는다. 반복되는 약속·결과·팀 관계가 내일을 위해 오늘을 조절할 이유를 만든다.
- 성숙의 순서는 **자존심으로 출석 → 외부 조건 때문에 자기관리 → 팀이 믿을 수 있도록 준비 → 강제 없이 프로 루틴 유지 → 인정 없이도 옳은 선택 책임**이다.
- 게임·낮은 에너지·무심한 태도·승부욕은 제거하지 않는다. 평소 말수는 적고 친한 친구들과만 자연스럽게 어울린다. 변화의 증거는 외향성이 아니라 출석·시간관리·실수 인정·역할 수행·선택의 책임이다.
- 한국 고교에서 농구부 출석만 먼저 개선되고 수업·수면은 점진적으로 따라온다. 생활 전체가 한 사건으로 교정되지 않는다.
- 미국 프렙에서는 한 차례 실제 기회 상실 뒤 누가 깨우지 않아도 학업·훈련·게임의 순서를 관리하기 시작한다.
- Villanova 우승은 개인 완성이 아니라 끝까지 준비한 집단에 속했다는 증명이다.
- 대학 우승·1라운드 지명 뒤 NBA 신인기에 짧은 자기관리 재발을 두고, 강제 없는 프로 루틴을 재확립한다.
- 상시 허세형·분위기 메이커 성격은 사용하지 않는다. 허세는 무시당했을 때 자존심을 감추려고 튀어나오는 짧은 방어 반응으로만 제한한다.
- BQ 성장과 책임 성장은 분리한다. 전술을 읽는 능력이 높다고 약속을 지키는 사람이 되는 것은 아니다.
- 상세 권위는 `canon/CHARACTER_RESPONSIBILITY_ARC.md`다.

## v0.11 LOCKED ADDITIONS — Villanova 자격·역할 안전선

- 주인공은 2017-18 Villanova에서 공식 경기에 출전할 수 있는 NCAA Division I `full qualifier`여야 한다. 첫해 경기 출전이 불가능한 academic redshirt는 현행 경로의 대안이 아니다.
- 한국 학교 문제는 지각·결석·낮은 성적이지만 학년 전체 낙제나 핵심과목 전부 실패로 만들지 않는다. 한국 중3·고1과 미국 프렙 기록을 합쳐 핵심과목 자격을 증명한다.
- 2017 역사 기준의 16개 핵심과목, 10/7 진행, 최소 2.300 핵심 GPA, SAT/ACT sliding scale, 졸업 증빙, Eligibility Center 학업·athletics 인증을 모두 통과해야 한다.
- 주인공의 Villanova 역할은 32~36경기, 선발 0회, 평균 8.5~10.5분의 후순위 수비·리바운드 전문 역할을 기준으로 한다.
- 실제 선수의 분을 공짜로 만들지 않는다. Samuels·Cosby-Roundtree의 일부 개발 분, 후순위 분, Bridges·Paschall·Spellman 등 핵심진의 경기당 합계 약 2~3분을 재배분한다.
- 대표 기여 경기는 2018 NCAA East Regional Final Texas Tech전으로 선택한다. 기능은 박스아웃·스위치 수비·팀 리바운드이며, 실제 Paschall 14리바운드와 Cosby-Roundtree 7리바운드의 중심 공로를 유지한다.
- 정확한 개인 기록·교체 시점은 R09 인과 시뮬레이션 전까지 HOLD다. 이 v0.11 시점의 Draft 순번 HOLD는 v0.15에서 30순위로 해소됐다.
- 상세 권위는 `research/VILLANOVA_ELIGIBILITY_ROTATION_MODEL.md`다.

## v0.11 RESEARCH_HOLD

- 선택 프렙과 NCAA approved course list
- 한국 중3·고1 과목별 핵심과목 환산
- 실제 SAT/ACT 점수와 Villanova 자체 입학 심사
- Villanova 장학금 슬롯과 늦은 리크루팅 경로
- Texas Tech전 정확한 분·기록 재분배

## v0.12 LOCKED ADDITIONS — 대학 종료 패킷

- 주인공의 미국 학교는 실존 명문고가 아니라 **가상 뉴잉글랜드 소규모 보딩 프렙**으로 둔다. 실존 학교는 국제학생·기숙사·학업지원·농구 노출 기능의 검증 모델로만 사용한다.
- 주인공은 한국 고1을 마친 뒤 2016년 3월 미국 프렙에 중도 편입한다. 한국 중3·고1 네 학기와 미국 프렙 세 학기를 합친 7학기 과정으로 2017년 5~6월 조기졸업한다.
- NCAA 10/7 요건은 2017년 마지막 학기 전에 충족한다. 마지막 학기는 16개 핵심과목 총량과 학교 졸업 부족분을 마감하는 단계이며, 자격을 한 학기에 몰아 복구하지 않는다.
- 한국 중3·고1 기록은 영어·수학·과학·사회·한국어/추가 핵심의 약 10단위 후보로 사용하고, 미국 프렙에서 최소 6단위를 보충하는 범주 구조를 사용한다. 개별 과목의 NCAA 환산은 `HOLD`다.
- Villanova 입학시험 안전선은 SAT 1280~1320 범위로 둔다. 정확한 한 점수는 사용 시점까지 정하지 않는다.
- Villanova 영입은 **가상 프렙 감독의 영상·학점 감사표 추천 → 허용된 평가 기간의 실전 확인 → 2016-17 성장·학업 재확인 → 2017년 봄 늦은 체육장학금** 한 경로로 잠근다.
- 대학 감독은 입학처·compliance·Eligibility Center의 결정을 대신하지 않는다. 주인공은 full qualifier와 대학 입학 승인을 모두 받아야 한다.
- `control/COLLEGE_ARC_SCOPE_GATE.md`는 `COLLEGE_ARC_SCOPE_COMPLETE`다. 대학의 정확한 40경기·캠퍼스·과목·교체 기록은 전체 Act Map 또는 R09에서 실제 필요가 생기기 전까지 다시 열지 않는다.
- 상세 권위는 `research/COLLEGE_EXIT_PACKET.md`다.

## v0.12 RESEARCH_HOLD

- 주인공의 정확한 생일과 2017 졸업일
- 가상 프렙의 정식 교명·개별 과목·졸업 감사
- 한국 개별 과목의 2017 Eligibility Center 환산
- 정확한 핵심 GPA·SAT 한 점수·Villanova 입학 내부 판단
- 2017-18 장학금 counter 최종 감사와 서명일
- Texas Tech전 정확한 분·기록 재분배

## v0.13 LOCKED ADDITIONS — 라이벌 ACL·레드셔츠 경로

- 라이벌은 2017년 9월 후보창의 한국 고교 공식 경기에서 비접촉 방향 전환 중 **오른쪽 무릎 ACL 완전파열**을 입는다. 고의 파울·충돌·보복 사건은 사용하지 않는다.
- 2017년 10월 ACL 재건술을 받고 단계별 재활을 시작한다. 정확한 경기·수술일·graft·동반 반월상연골 손상은 `HOLD`다.
- 2018년 가을 부상 전부터 영입하던 NCAA Division I 대학에 체육장학금 선수로 입학한다. 이 v0.13 시점의 대학명 `HOLD`는 v0.14에서 Gonzaga로 해소됐고, NLI·scholarship counter 세부만 계속 `HOLD`다.
- 2018-19은 공식 경기 0회의 전통적 비경기 레드셔츠다. 이미 사용한 시즌을 hardship waiver로 되돌리는 medical-redshirt 구조가 아니다.
- 2019-20 redshirt freshman으로 복귀 시즌을 치르고 2020 NBA Draft 전체 1순위 수준을 다시 획득한다. 부상 전 명성만으로 1순위를 자동 보장하지 않는다.
- 복귀 첫해에는 폭발력·효율·부하 관리의 변동을 남긴다. 부상이 신체 강화 이벤트가 되거나 6개월 만에 완전 복귀하지 않는다.
- 부상 뒤 플레이 변화는 급격한 방향전환 일변도에서 감속·두 발 정지·템포·풀업·선제 패스를 함께 쓰는 1차 창조자로 확장되는 것이다. 주인공의 연결자 기능을 복제하지 않는다.
- 2020 NCAA 포스트시즌 취소는 복귀 증명의 마지막 무대를 잃는 외부 고정축으로 유지한다.
- 상세 권위는 `research/RIVAL_INJURY_REDSHIRT_MODEL.md`다.

## v0.13 RESEARCH_HOLD

- 라이벌의 정확한 부상 경기·수술일·graft·동반 손상
- 기능검사·접촉훈련 복귀·의료 clearance 수치
- NCAA full-qualifier 개별 학업 인증
- 부상 전 오퍼와 장학금을 유지할 NCAA 대학명 — v0.14에서 Gonzaga로 해소
- 2018-19 scholarship counter·NLI·대학 의료 권한
- 2019-20 정확한 기록·출전시간·부하 관리
- 2020 Draft 의료검사와 실제 지명 팀·순번 파급

## v0.14 LOCKED ADDITIONS — 라이벌 Gonzaga 경로

- 라이벌의 NCAA 대학은 **Gonzaga University**다. Duke·Kentucky·Oregon과 2018-20 로스터·역할 충돌을 비교한 뒤 선택한다.
- 2018년 가을 Gonzaga에 체육장학금 학생선수로 입학하고 2018-19 공식 경기 0회 레드셔츠로 재활·학업·팀 적응을 병행한다.
- 2019-20 redshirt freshman으로 복귀해 선발 SG/SF이자 주된 외곽 1차 창조자가 된다. 정확한 선발·분·점유율·개인 기록은 R09까지 `HOLD`다.
- 시즌 초 약 25~29분, 후반 약 29~32분의 역할 범위를 설계 안전선으로 두되 기존 Gonzaga 선수 총분과 충돌하면 R09에서 좁힌다.
- 깊은 실존 관계는 Joel Ayayi·Corey Kispert·Filip Petrusev 세 명을 상한으로 둔다. Rui Hachimura·Brandon Clarke 등은 공개 팀 환경의 기준선일 뿐 추가 절친·비밀 멘토로 확장하지 않는다.
- 대표 경기는 2019년 11월 28일 Oregon전과 2020년 3월 10일 Saint Mary's WCC 결승 두 개만 둔다. 실제 점수와 개인 기록은 자동 보존하지 않는다.
- 2019-20 WCC 정규시즌·토너먼트 우승 기능은 유지하지만 실제 31승 2패는 R09 재계산 전 기준선이다.
- NCAA 전국우승은 없다. 2020 포스트시즌 취소는 그대로 유지한다.
- `control/RIVAL_COLLEGE_SCOPE_GATE.md`는 `RIVAL_COLLEGE_SCOPE_COMPLETE`다. R09·Act Map·회차 직전 검수 사유가 없으면 대학 세부를 추가하지 않는다.
- 상세 권위는 `research/RIVAL_NCAA_SCHOOL_SELECTION.md`다.

## v0.14 RESEARCH_HOLD

- Gonzaga의 2017 국제 스카우팅 접점·구두 오퍼·NLI 서명일
- 2018-19 scholarship counter와 실제 한 자리 재배분
- 라이벌의 개별 NCAA full-qualifier·입학 인증
- 대학 의료진 권한·기능검사·full-contact clearance 수치
- 2019-20 실제 총분·선발·점유율·개인 기록·승패 재계산
- 2020 Draft 의료검사와 실제 지명 팀·순번 파급

## v0.15 LOCKED ADDITIONS — 주인공 Atlanta 30순위 착지

- 주인공의 첫 NBA 팀은 **Atlanta Hawks**, 지명 순번은 **2018 NBA Draft 전체 30순위**다.
- 계약은 투웨이가 아니라 1라운드 NBA rookie-scale 표준 계약이다. G League에서는 NBA 계약을 유지한 assignment 선수다.
- 실제 30순위 Omari Spellman의 존재를 삭제하지 않는다. 변경된 팀·순번은 R09 드래프트 보드 재계산까지 `HOLD`다.
- 2018-19 본무대는 NBA다. Atlanta 약 38~50경기·10~16분, Erie 약 4~10경기·24~30분을 시뮬레이션 안전선으로 두되 실제 총분과 충돌하면 줄인다.
- 깊은 실존 관계는 Trae Young·Kevin Huerter·John Collins 세 명을 상한으로 둔다. Vince Carter는 공개적 베테랑 기준선일 뿐 비밀 스승으로 확장하지 않는다.
- 루키 핵심 전술 문제는 비슈터 공간 복구와 약한 쪽 수비·전환 연결 두 개만 둔다.
- NCAA 우승·1라운드 지명 뒤 밤샘 게임이 잠깐 되살아 아침 영상·컨디셔닝 일정에 늦는다. 직접 비용은 예정됐던 NBA 로테이션 기회 상실이다.
- 뒤이은 Erie 배정은 징계가 아니라 닫힌 NBA 자리 대신 실전 반복을 확보하는 개발 결정이다. 게임을 끊는 것이 아니라 훈련·회복 뒤로 순서를 바꾸며 자율적 프로 단계에 진입한다.
- `control/NBA_LANDING_SCOPE_GATE.md`는 `NBA_LANDING_SCOPE_COMPLETE`다. R09·R11·Act Map·회차 직전 검수 사유가 없으면 루키 세부를 추가하지 않는다.
- 상세 권위는 `research/PROTAGONIST_2018_DRAFT_LANDING.md`다.

## v0.15 RESEARCH_HOLD

- 주인공의 정확한 Draft 선언·생일·2017 졸업 1년 경과 계산
- Atlanta 개별 워크아웃·계약 서명일·rookie-scale 액수
- Spellman을 포함한 2018 Draft 후반 보드 재배치
- 2023 두 선수의 NBA 소속팀·대표팀 허가·보험·캠프 일정 결합
- Atlanta 2018-19 총분·승패·개인 기록 재계산
- 자기관리 지각·NBA 기회 상실·Erie 배정의 정확한 날짜
- 2019-20 College Park 추가 배정 필요 여부

## v0.16 LOCKED ADDITIONS — 광고·신발·멘토 생태계

- 주인공은 2018 Draft 뒤 **PUMA**와 footwear/apparel 계약을 맺는다. PUMA의 2018 농구 재진입·신인 영입·한국 시장 성장 전략에서 도출한 가상 계약이며, 실제 영입 사실처럼 쓰지 않는다.
- 라이벌은 2020 Draft·의료 검토 뒤 **adidas**와 계약한다. 팬데믹 때문에 계약 시점·행사·금액이 자동 보장되지 않으며 정확한 서명일은 2020 Draft 팀 선택 뒤 확정한다.
- 둘 다 대학 재학 중 개인 유료 광고를 하지 않는다. 2021 NIL 정책을 2017-20에 소급하지 않는다.
- 주인공의 rookie-scale 기간과 라이벌의 데뷔 전에는 소매 시그니처 슈즈를 주지 않는다. player-exclusive 색상과 한국 캠페인도 성과·계약 검증 전 `HOLD`다.
- 주인공의 실존 스타 직접 훈련 접점은 2019 Kobe Bryant 1회 중심으로 제한한다. Michael Jordan·Shaquille O'Neal·Jay-Z는 개인 멘토가 아니다.
- Jordan은 2018-20 Charlotte 구단주·브랜드 아이콘, Shaq는 당시 공개 방송 평가자다. Shaq의 Reebok Basketball 사장 역할은 2023년 이후이므로 초기 계약에 소급하지 않는다.
- 코치·의료진·가상 트레이너·가상 에이전트·가상 브랜드 매니저의 권한을 분리한다. 주인공과 라이벌은 서로 다른 에이전트를 둔다.
- `control/COMMERCIAL_RELATIONSHIP_SCOPE_GATE.md`는 `COMMERCIAL_RELATIONSHIP_FOUNDATION_COMPLETE`다. R08·R09·R11·Act Map의 재개 사유 없이는 광고·유명인 세부를 더하지 않는다.
- 상세 권위는 `research/SHOE_SPONSOR_MENTOR_ECOSYSTEM.md`다.

## v0.16 RESEARCH_HOLD

- 두 신발 계약의 정확한 보장액·기간·인센티브·종료 조항
- 주인공 PUMA 계약일·한국 캠페인·player-exclusive 제품화
- 라이벌 adidas 계약일·팬데믹 촬영·2020 Draft 팀 충돌
- 두 가상 에이전트와 브랜드 매니저의 이름·소속·수수료
- 2019 Kobe 훈련의 실제 초청자·장소·날짜
- 라이벌 NBA 팀 내부의 베테랑 멘토 후보
- Jordan·Shaq 공개 접점의 Act 필요 여부

## v0.17 LOCKED ADDITIONS — 국가대표·병역 일정

- 2018 아시안게임에는 주인공과 라이벌 모두 참가하지 않는다. 주인공은 Atlanta의 Utah·Las Vegas Summer League와 루키 개발 일정에 남고, 라이벌은 ACL 재활을 계속한다.
- 주인공이 접촉하지 않은 2018 한국 남자농구의 실제 동메달은 비접촉 기준선으로 유지한다.
- 두 사람이 다시 같은 유니폼을 입는 국가대표 경로는 2023 Hangzhou 아시안게임 공동 도전으로 잠근다.
- 2023 공동 도전은 결과 보장이 아니다. 실제 한국 7위에 두 선수를 더해 금메달을 자동 확정하지 않고, 최종 12인·실제 출전·모든 경기·대진 변화를 R09에서 다시 계산한다.
- 아시안게임은 NBA-FIBA 합의의 자동 출전 보장 대회로 취급하지 않는다. NBA 소속팀 허가·보험·의료자료·캠프 결장을 독립 비용으로 둔다.
- 두 선수는 1999년생이므로 2024년 계속 국외 체류를 위한 허가 시한이 2023 선택을 압박한다.
- 아시안게임 금메달은 예술체육요원 편입 성적 요건이지 완전 면제가 아니다. 실제 출전·편입 절차와 이후 복무·군사교육·특기활용 봉사 의무를 삭제하지 않는다.
- `control/NATIONAL_TEAM_MILITARY_SCOPE_GATE.md`는 `NATIONAL_TEAM_MILITARY_FOUNDATION_COMPLETE`다.

## v0.17 RESEARCH_HOLD

- 2023 두 선수의 NBA 소속팀·계약·부상 상태와 구단별 허가
- 대표팀 최종 12인에서 빠지는 선수와 포지션·분 재배분
- 조별리그부터 순위결정전까지 전 경기·대진·메달 결과
- 예술체육요원 편입 성립과 당시 정확한 군사교육·봉사 행정 일정

## v0.18 LOCKED ADDITIONS — 승수·드래프트 인과 프로토콜

- 실제 드래프트 결과는 보존 목표가 아니다. 입력이 같을 때만 유지하고, 경기 승패·시즌 순위·로터리 시드·보호픽·픽 소유권이 바뀌면 결과도 다시 계산한다.
- 접촉 경기의 승패를 먼저 확정하고 시즌 승수·순위·타이브레이커를 계산한 뒤에만 드래프트 순서를 만든다.
- 로터리 참가팀·시드·확률이 실제와 같으면 실제 추첨 결과를 외부 확률 사건으로 유지한다. 하나라도 바뀌면 공개 고정 seed와 해당 연도 규정으로 재추첨한다.
- 고정 seed 규칙은 `SHA-256("first-rebound|nba-lottery|{draft_year}|v1")`이며 결과를 본 뒤 다시 뽑지 않는다.
- 보호픽·양도·스왑 조건은 실제 최종 결과를 복사하지 않고 재계산된 순번에 적용한다.
- 드래프트 보드가 바뀌면 각 팀은 남은 선수·당시 필요·프런트·의료·계약을 기준으로 다시 선택한다. 전 선수를 기계적으로 한 칸씩 미루지 않는다.
- 2018은 주인공보다 앞서 지명된 1~29순위와 Doncic–Young 거래를 유지하고 30~60순위를 재판정한다.
- 2019 Atlanta의 실제 8·10순위는 보장값이 아니다. Atlanta·Dallas 승수와 보호픽 조건이 바뀌면 로터리와 양도 결과도 바뀐다.
- 라이벌은 2020 `1순위급 후보`이지 실제 1순위 고정값이 아니다. 팀 필요·ACL 의료자료·팬데믹 스카우팅을 거쳐 실제 순번을 결정하며, 1순위가 되면 Edwards 이하 보드도 다시 계산한다.
- 상세 권위는 `simulation/DRAFT_CAUSALITY_PROTOCOL.md`다.

## v0.18 RESEARCH_HOLD

- 2018 Draft 30~60 팀별 대안 보드와 Omari Spellman 후속 경로
- 2018-19 Atlanta 82경기 접촉 분류·총분·승수·최종 순위
- 2019 로터리 시드·확률·Dallas 보호픽·대안 보드
- 2019-20 NBA 승수·2020 로터리·라이벌 실제 지명 팀과 순번
- 로터리 공식 조합 배분을 구현한 재현 가능한 R09 실행 코드와 로그

## v0.19 LOCKED ADDITIONS — Atlanta 2018-19 인과 기준선

- Atlanta의 실제 2018-19 정규시즌 82경기·29승 53패·9,294득점을 R09 불변 기준선으로 잠근다. 이는 대체 세계 결과가 아니라 비교 출발점이다.
- 실제 연장 횟수로 계산한 경기 총 선수분은 19,855분이다. 공개 로스터 정수 분 합계 19,853분과의 2분 차이는 반올림 감사차이며 새 분으로 사용하지 않는다.
- 주인공의 NBA 신인 안전선은 42~46경기·14~16분·588~736분으로 좁힌다. 정확 기록은 아니다.
- 1차 출전시간 donor는 실제 30순위 Omari Spellman의 805분이다. Young·Huerter·Collins의 핵심 육성 분은 우선 보호한다.
- 주인공이 DNP 또는 Erie여도 Spellman 부재가 남으므로 해당 Atlanta 경기를 자동 비접촉으로 두지 않는다. 82경기 모두 최소 `ROSTER` 접촉이다.
- 대체 승패·점수는 아직 만들지 않는다. 실제 결과를 보고 접전만 뒤집거나 영향 계수를 맞추는 행위를 금지한다.
- Atlanta 단독 승수로 2019 로터리를 확정하지 않는다. 2018 Draft 30~60에서 Spellman의 새 팀과 그 팀 승패 파급까지 닫혀야 `FINAL`이 가능하다.
- 2018 Draft 30~60은 모든 픽을 원장상 확인하되 실제 선택 유지 픽은 짧게 통과하고 `CHANGED/CASCADE`만 심층 비교한다. 대형 드래프트를 같은 깊이로 과설계하지 않는다.
- 현재 판정은 `BASELINE_PASS / COUNTERFACTUAL_HOLD`다. 상세 권위는 `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.md`와 `.xlsx`다.

## v0.19 RESEARCH_HOLD

- Atlanta 경기별 선수 가용성·실제 player-game 분·주인공 donor vector
- 주인공 자기관리 실패·잃는 로테이션 경기·Erie assignment 날짜
- 경기 전 승률 pB·rotation/availability/fatigue 영향 prior·고정 game hash 실행
- 2018 Draft 30~60 대안 보드와 Spellman 새 팀·계약·2018-19 파급
- 상대팀 승패·타이브레이커·2019 비플레이오프 14팀과 lottery
- Dallas pick top-5 보호·양도와 Atlanta 대안 지명·거래

## v0.20 LOCKED ADDITIONS — 2018 Draft 30~60 압축 대안 보드

- 주인공이 Atlanta 30번에서 Omari Spellman을 대체한 뒤에도 31~60번을 기계적으로 한 칸씩 이동시키지 않는다.
- 30~60순위 31개 픽 중 27개는 실제 선택·거래를 유지하고 30·49·56·58번만 바꾼다.
- Omari Spellman은 San Antonio 49번으로 이동한다. 당시 Spurs 워크아웃과 슈팅·패싱·역할 이해도 평가를 선택 근거로 쓴다.
- 49번에서 밀린 Chimezie Metu는 Dallas 56번, 56번에서 밀린 Ray Spalding은 Denver 58번으로 이동한다.
- Thomas Welsh는 삭제하지 않는다. 이 단계에서는 미지명 뒤 Denver 투웨이 역할 후보였으나, v0.22 계약·슬롯 검산에서 중복 불가로 폐기된다.
- Atlanta 34번과 Charlotte의 Devonte' Graham 권리 거래는 유지한다. Atlanta가 30번으로 개발형 포워드 슬롯을 이미 채웠고 Charlotte가 미래 2라운드 두 장을 지급한 거래 입력이 변하지 않았다.
- Spellman에게 Atlanta의 실제 805분을 San Antonio에서 복사하지 않는다. 대체 슬롯의 출발 기준은 실제 Metu의 2018-19 NBA 29경기·145분이다.
- 2018 후반 드래프트 보드는 닫혔지만 San Antonio의 날짜별 분·승패 파급 전에는 2019 standings·lottery를 `FINAL`로 만들지 않는다.
- 상세 권위는 `simulation/2018_DRAFT_30_60_ALTERNATE_BOARD.md`와 `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`다.

## v0.20 RESEARCH_HOLD

- San Antonio의 2018-19 Metu NBA/G League 날짜별 이동과 Spellman 대체 분
- Spellman의 Spurs 계약·Austin assignment·가용성·직접 대결 두 경기 파급
- Dallas의 Metu와 Denver의 Spalding 계약·NBA/G League 분 파급
- Denver가 Welsh에게 미지명 투웨이 슬롯을 다시 줄 수 있는지 여부 — v0.22에서 중복 불가로 해소
- 두 번째 팀 파급 뒤 Atlanta·상대팀 승패·2019 standings·lottery

## v0.21 LOCKED ADDITIONS — Spurs 두 번째 팀 역할 기준선

- San Antonio 49번 Omari Spellman은 실제 Metu의 저레버리지 신인 개발 슬롯을 대체한다.
- 실제 Metu 기준선은 NBA 29경기·0선발·145.4분·평균 5.0분, Austin 26경기·710.4분·평균 27.3분이다.
- Spellman BASE는 29경기·145.4분·0선발이다. 사전 허용 범위는 NBA 24~31경기·120~180분·평균 4~6분, Austin 20~28경기다.
- Metu는 투웨이가 아니라 다년 NBA 계약을 유지한 assignment 선수였다. Spellman도 같은 계약 계층으로 둔다.
- 145.4분을 넘는 HIGH의 추가 34.6분에는 경기 날짜·실제 공여자·가용성 증거가 필요하다. 없으면 BASE로 되돌린다.
- 2019년 3월 6일·4월 2일 Atlanta 직접 대결에서 Metu는 모두 0분이었다. Spurs 쪽 대체 접촉은 `NO_DIRECT_MINUTES`다.
- San Antonio의 실제 48승 34패는 비교 기준선이지 대체 세계 확정 결과가 아니다. 경쟁 구간 출전이 생길 때만 해당 경기 승패 검토를 연다.
- 큰 드래프트는 모든 팀을 같은 깊이로 확장하지 않는다. 계약층→실제 분 침범→경기층 순으로 조건부 확장한다.
- 상세 권위는 `simulation/SPURS_2018_19_SECOND_TEAM_IMPACT.md`와 `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`다.

## v0.21 RESEARCH_HOLD

- Spellman의 정확한 Spurs/Austin assignment 날짜와 NBA player-game 분
- 145.4분 초과 시 추가 34.6분의 날짜별 심부 로테이션 donor
- Atlanta 주인공의 두 Spurs전 출전 여부·분·경기 영향
- Dallas Metu·Denver Spalding/Welsh의 계약·로스터·분 파급
- Atlanta player-game·상대팀 승패·2019 standings·lottery

## v0.22 LOCKED ADDITIONS — Dallas·Denver 연쇄 계약층

- Dallas 56번 Chimezie Metu는 실제 Ray Spalding의 정규 NBA 계약+Texas Legends 배정 계층을 대체한다.
- Dallas BASE는 실제 Spalding의 NBA 1경기·1분과 Texas Legends 29경기다. Spurs에서의 Metu 145.4분을 Dallas에 복사하지 않는다.
- 실제 Dallas가 2019년 1월 31일 Spalding을 방출한 사실은 기준선이지만, 대체 세계에서 Metu를 같은 날 방출하는지는 `TRANSACTION_HOLD`다.
- Denver 58번 Ray Spalding은 실제 Thomas Welsh의 투웨이 슬롯을 대체한다. BASE는 NBA 11경기·36분과 G League 20경기다.
- Denver의 다른 투웨이 자리인 DeVaughn Akoon-Purcell은 보호한다. 따라서 Welsh를 Denver에 다시 투웨이로 등록하는 중복안은 폐기한다.
- Welsh는 삭제하지 않고 미지명 자유계약 시장으로 돌리되, 새 팀·리그·계약은 증거 전까지 `UNDRAFTED_FREE_AGENT_MARKET_HOLD`다.
- 2018년 10월 24일·12월 12일 Dallas전과 11월 15일·12월 8일 Denver전에서 실제 대체 선수의 출전은 모두 0분이다. 상대 팀 쪽 접촉은 `NO_DIRECT_MINUTES`다.
- Metu가 Dallas 1분, Spalding이 Denver 36분을 넘을 때만 해당 날짜의 실제 donor·가용성·경쟁 구간 검토를 연다.
- 현재 판정은 `CASCADE_CONTRACT_PASS / GAME_OUTCOMES_HOLD`다. 상세 권위는 `simulation/DALLAS_DENVER_2018_19_CASCADE_IMPACT.md`와 `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`다.

## v0.22 RESEARCH_HOLD

- Dallas가 2019년 1월 31일 Metu를 방출할지, 다른 선수를 정리할지 여부
- Metu 1분·Spalding 36분 초과 시 날짜별 player-game donor와 경쟁 구간
- Welsh의 미지명 뒤 새 계약 팀·리그·시점
- Atlanta 주인공의 Dallas·Denver 직접 대결 4경기 출전 여부·분·경기 영향
- Atlanta player-game·상대팀 승패·2019 standings·lottery

## v0.23 LOCKED ADDITIONS — Atlanta 날짜별 donor vector

- 실제 Omari Spellman의 2018-19 Atlanta 46경기 날짜와 공개 경기별 분 합계 805.0분을 1차 donor vector로 잠근다.
- 주인공의 결과 비의존 출전 규칙은 `Spellman donor ≥7.0분`, 경기당 `MIN(16.0, donor)`다.
- 이 규칙의 44경기·636.0분에서 2018년 11월 19일 예정 14.1분을 자기관리 실패의 직접 비용으로 뺀다.
- 주인공 NBA 신인 기준선은 **43경기·621.9분·14.46 MPG·0선발**이다.
- 2018년 11월 19일은 다구간 원정 뒤 첫 홈 경기의 아침 영상·컨디셔닝 일정에 늦어 로테이션 기회를 잃는 날짜다. 실제 승패·점수차는 선택 근거가 아니다.
- Erie 개발 assignment는 **2018년 12월 7일부터 22일까지**이며 실제 Erie 일정 6경기를 사용한다. 같은 날짜 Atlanta NBA 분은 모두 0이다.
- Erie의 6경기·24~30 MPG 범위는 잠그되 정확한 G League 개인 박스스코어는 `HOLD`다.
- 이 배정은 11월 19일 지각의 직접 징계가 아니라 별도의 개발 권한 결정이다. Spellman의 실제 오른쪽 엉덩이·발목 부상은 주인공에게 복사하지 않는다.
- Atlanta의 805.0분은 주인공 621.9분과 `ATL_REMAINDER_POOL` 183.1분으로 날짜별 보존한다.
- `ATL_REMAINDER_POOL`은 가상 선수가 아닌 감사용 회계 브리지다. 동일 날짜 실제 가용 수취자를 확정하기 전 개인 박스스코어·경기 영향·승패를 만들지 않는다.
- 접촉 분류는 `DIRECT 43 / ROSTER 39 / IDENTICAL 0`이다.
- 현재 판정은 `ATL_DONOR_VECTOR_PASS / OUTCOME_HOLD`다. 상세 권위는 `simulation/ATLANTA_2018_19_PLAYER_GAME_DONOR_VECTOR.md`와 `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`다.

## v0.23 RESEARCH_HOLD

- `ATL_REMAINDER_POOL` 183.1분의 동일 날짜 실명 수취자
- 주인공과 수취자의 경기별 득점·리바운드·슈팅·온오프
- 경기 전 승률 pB·rotation/availability/fatigue 영향 prior·고정 game hash 실행
- 대체 승패·상대팀 승패·전체 standings·2019 lottery
- Dallas pick top-5 보호·양도와 Atlanta 대안 지명·거래

## v0.24 LOCKED ADDITIONS — Atlanta 실명 reserve receiver allocation

- v0.23의 `ATL_REMAINDER_POOL` 183.1분을 29개 동일 날짜·31개 배정 행으로 전부 해소한다.
- 수취 분은 Justin Anderson 105.6분, Alex Poythress 48.6분, Miles Plumlee 17.5분, Daniel Hamilton 11.4분이다.
- B.J. Johnson은 감사 후보로 포함하지만 0분이다. 잔여분과 겹치는 유일한 2019년 3월 1일에 Anderson이 같은 박스스코어에 등재돼 있다.
- 수취자는 같은 날짜 ESPN Atlanta 박스스코어의 `PLAY/DNP-CD` 등재가 있어야 한다. 미등재 선수는 건너뛴다.
- Anderson이 재활로 빠진 첫 16경기에는 Poythress→Hamilton→Plumlee→B.J. Johnson 순, 2018년 11월 19일 복귀 뒤에는 Anderson을 첫 순위로 둔다.
- 조정 경기분은 각 선수의 실제 2018-19 단일 경기 최고분을 넘지 않는다. 상한은 Anderson 31·Poythress 26·Hamilton 23·Plumlee 19·B.J. Johnson 19분이다.
- `DNP-CD` 수취 날짜는 대체 세계의 추가 출전으로 계산하지만 실제 득점·효율은 복사하지 않는다.
- Spellman -805.0분 + 주인공 621.9분 + 네 수취자 183.1분 = 0.0분이며 공개 정수 선수분 합계 19,853분도 보존한다.
- 현재 판정은 `ATL_RECEIVER_ALLOCATION_PASS / PRODUCTION_OUTCOME_HOLD`다. 상세 권위는 `simulation/ATLANTA_2018_19_RESERVE_RECEIVER_ALLOCATION.md`와 `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`다.

## v0.24 RESEARCH_HOLD

- 주인공과 네 수취자의 경기별 득점·리바운드·슈팅·온오프
- 추가 출전이 다음 경기 피로·부상·가용성에 미치는 영향
- 경기 전 승률 pB·rotation/availability/fatigue 영향 prior·고정 game hash 실행
- 대체 승패·상대팀 승패·전체 standings·2019 lottery
- Dallas pick top-5 보호·양도와 Atlanta 대안 지명·거래
