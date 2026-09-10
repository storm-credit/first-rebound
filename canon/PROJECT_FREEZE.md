# Project Freeze v0.30

- 상태: `PARTIAL_FREEZE`
- 변경 권한: 사용자 명시 승인
- 정식 제목: `HOLD`
- 태그라인 후보: 《처음 배운 것은 리바운드였다》

## 로그라인

한국 고교에서 농구를 늦게 배운 압도적 신체 재능의 소년이 미국 프렙과 NCAA를 거쳐 NBA에 도전하고, 매년 약점을 지워 공격 1옵션과 마지막 선택을 함께 책임지는 투웨이 슈퍼스타로 성장한다.

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
- 최종 선수상: 리바운드·전환을 고유 뿌리로 삼아 림 압박·엘보 공격·패스·클러치 선택까지 확장한 공격 1옵션급 투웨이 SF/PF
- 진로 구조: 주인공은 한국 고교 → 미국 프렙 고교 → 2017-18 Villanova NCAA → 2018 NBA Draft → Chicago Bulls 원클럽 프랜차이즈 경로. 라이벌은 같은 한국 고교 → 장기 부상·재활 → 2018-20 Gonzaga NCAA → 2020 NBA Draft → 서부 팀 경로
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

## v0.25 PARTIAL ADDITIONS — Atlanta 생산성·피로·경기 영향 방법

- Atlanta에서 제거된 Spellman 805.0분과 주인공 621.9분+실명 수취자 183.1분의 같은 분만 비교한다. 새 선수의 절대 기여를 실제 기준선 위에 더하지 않는다.
- 실제 선수의 2018-19 per-36·BPM을 추가분에 직접 복사하지 않는다. 공통 평균 `-2.75`, pseudo-minutes 750, band와 주인공 `LOW -4.25 / BASE -2.75 / HIGH -1.25`는 외부 교정 전 후보값이며 정본 prior가 아니다.
- 주인공 박스 생산성 36분당 10.0점·7.5리바운드·1.8어시스트·1.3스틸·0.9블록·TS .500도 비교·교정 후보이지 최종 시즌 기록이나 실행 입력이 아니다.
- 피로는 이전 부하만 시간순으로 계산하고 새 부상을 자동 생성하지 않는다. M24/M72/M7 계수·G League 0.85·임계값은 외부 교정 전 `HOLD`다.
- 검증되지 않은 라인업·우정·Young과의 케미 상호작용은 0이다. 박스 생산성과 영향 prior를 이중 합산하지 않는다.
- LOW 교체효과는 대체측 LOW-donor HIGH, HIGH는 대체측 HIGH-donor LOW로 계산해 comparator 불확실성을 상쇄하지 않는다.
- 승률 변환 `k`는 Atlanta 원점수차 표준편차로 정하지 않는다. 독립 표본 교정 전 `LOGIT_SCALE_HOLD`이며 경기 전 양방향 no-vig closing moneyline이 없는 경기도 실행하지 않는다.
- latent seed는 `FIRST_REBOUND|R09|ATL_2018_19|PRIOR_v1`, SHA-256은 `228aac4642a599e4545ed878efda7952bf04bf1b0ad73b20b217d44f5aa19cab`다.
- event ID는 `ATL_2018_19_G001..G082`이고, `h=(BE64(SHA256(seed|event_id)) >> 11) / 2^53`으로 고정한다.
- LOW·BASE·HIGH가 같은 latent를 공유한다. 결과가 하나라도 갈리면 `SENSITIVE/HOLD`이며 정확한 대체 점수는 만들지 않는다.
- 상세 권위는 `simulation/ATLANTA_2018_19_PLAYER_PRODUCTION_PRIORS.md`와 계산 원장의 `ATL Priors` 시트다.

## v0.25 RESEARCH_HOLD

- Atlanta 82경기별 경기 전 양방향 closing moneyline·no-vig `pB`
- 생산성 수축 평균·pseudo-minutes·band와 피로 계수·가중·임계값의 외부 교정 또는 fallback 승인
- 경기 전 기대 대비 독립 표본을 이용한 logit scale `k` 교정
- 주인공·Spellman·네 수취자의 전체 player-game workload와 시간순 피로 상태
- conditional latent 실행·대체 승패·상대팀 기록
- 정확한 개인 시즌 박스스코어·온오프·대체 점수
- 비플레이오프 14팀 순위·2019 로터리·Dallas 보호픽·드래프트 보드

## v0.26 LOCKED ADDITIONS — 연차별 상승과 투웨이 지배자 상한

- 대학의 수비·리바운드 전문 역할은 주인공의 최종 한계가 아니라 NBA 생존을 위한 출발점이다.
- 주인공은 NBA에서 이전 시즌에 노출된 약점을 매년 교정하며, 최종적으로 플레이오프 공격 1옵션과 중요 수비 매치업을 함께 맡는 투웨이 슈퍼스타가 된다.
- 최종 공격은 단순한 연결이 아니다. 리바운드 직후 전환 S+, 접촉 돌파·림 마무리, 엘보·미드포스트, 숏롤·라이브 패스를 결합해 상대 수비 계획의 중심이 된다.
- 만능형은 시작 설정이 아니라 성장 결과다. 새 기술은 약점 노출→비용→교정→제한적 사용→상대 재대응→플레이오프 자동화 순서를 거친다.
- 매년 기술 기준선은 올라가지만 득점·효율·팀 승수·외부 평가는 부상·역할·스카우팅 때문에 W자로 흔들릴 수 있다.
- 정점에서는 리그 최고의 선수와 시대 지배를 다툴 수 있다. 다만 정확한 MVP·파이널 MVP·올NBA·올디펜시브·우승 횟수와 연도는 결과 계산 전까지 잠그지 않는다.
- 고난도 풀업 3점과 가드식 장기 타이트 핸들은 상대적 한계로 남긴다. 모든 기술을 S로 만들지 않는다.
- 공격 부하가 커지면 82경기 내내 상대 에이스를 전담하지 않는다. 수비 S 출력은 플레이오프·클러치에서 선택적으로 사용한다.
- 결말의 마지막 패스는 공격 능력 부족이나 승부 회피가 아니다. 직접 해결 능력을 증명한 최상위 1옵션이 더 나은 승리 선택을 책임지는 완성이다.
- 상세 권위는 `design/PROTAGONIST_ASCENSION_DOMINANCE_MODEL.md`다.

## v0.26 RESEARCH_HOLD

- 2019-20~2022-23 Atlanta의 새 player-minute·사용률·선발·클로징 배정
- Atlanta 원클럽 공동 코어 또는 정당한 가치 이적 선택
- Trae Young과의 공격 권한, Murray·Hunter·Huerter·Collins·Griffin·Bey 거래 연쇄
- 전성기 정확 시즌·개인 기록·효율·수상·우승·부상
- 2028 본편 종결과 720~840화 연재 배분

## v0.27 LOCKED DIRECTION — Chicago 원클럽·동서부 라이벌

- 주인공의 장기 NBA 팀은 **Chicago Bulls**다. 팀을 옮겨야만 S급이 되는 구조를 사용하지 않고, Chicago에서 원클럽 프랜차이즈 스타로 성장한다.
- `단독 프랜차이즈`는 신인 때부터 기존 간판을 삭제한다는 뜻이 아니다. Zach LaVine의 기존 공격 간판 기능을 보존하고, 주인공은 조력자→공동 에이스→최우선 코어 순으로 상승한다.
- 주인공은 동부, 핵심 라이벌은 서부에 둔다. 정확한 서부 팀과 지명 순번은 후속 4안 비교 전까지 `HOLD`다.
- Chicago의 실제 2018년 22순위는 최우선 착지 후보지만 **정확 순번은 아직 LOCK하지 않는다.** Villanova 저사용 선수가 22순위에 오르는 팀 보드·워크아웃 근거와 22~60 드래프트 재판정이 먼저다.
- v0.15~v0.26의 Atlanta 30순위·Erie 6경기·43경기 621.9분·Trae/Huerter/Collins 관계·Spellman 연쇄는 활성 정본에서 해제한다. 삭제하지 않고 폐기 분기와 검증 방법의 기록으로 보존한다.
- 1라운드 rookie-scale, 투웨이 계약 금지, NBA 본무대, 짧은 G League assignment 가능, 자기관리 재발, 실존 선수 분·공로 보존 원칙은 유지한다.
- 정확한 Chicago 루키 분·선발·G League 일정·깊은 관계 3명·승수·로터리·계약·우승은 `HOLD`다.

## v0.27 RESEARCH_HOLD

- 2018 Chicago 22순위 팀 보드·워크아웃·신체 측정과 정확 지명 순번
- Chandler Hutchison의 변경 팀·순번과 2018 Draft 22~60 재판정
- Chicago 2018-19 82경기 player-minute donor·자기관리 비용·Windy City 배정
- 2019 Coby White와 2020 Patrick Williams 드래프트 경로
- 2021 Vučević·DeRozan·Lonzo·Caruso·Markkanen 거래·계약 연쇄
- LaVine의 잔류/이별과 공동 에이스에서 프랜차이즈 승계까지의 공정한 역할
- 라이벌의 2020 서부 팀·순번·베테랑 관계

## v0.28 PARTIAL ADDITIONS — 2018 Draft 팀보드·연쇄 재판정

- 드래프트 설계 순서는 **가상 선수 프로필→실제 기준선→순번별 삽입→가능안끼리 서사 비교→나비효과 폐쇄→정본 승격**으로 잠근다.
- Golden State 28의 Chandler Hutchison 선택은 당시 즉시 투입 가능한 다목적 수비 윙 요구에 맞아 `TEAM_BOARD_PASS / DRAFT_NIGHT_PRIMARY_CANDIDATE`다. 정확 착지는 아직 `HOLD`다.
- Portland 24는 Anfernee Simons의 두 차례 워크아웃과 최고 상한 선택 원칙을 우선해 `SIMONS_KEEP_LEAN`; Hutchison은 반증용 contingency로 둔다.
- Golden State가 28에서 Hutchison을 택할 경우 Jacob Evans의 첫 후속 착지는 Portland 37이 현행 `PRIMARY_LEAN`이다. Detroit 42와 Orlando 43은 후순위 대안이며 전부 정본이 아니다.
- Portland 37 Evans가 성립하면 Gary Trent Jr.의 첫 포획은 Lakers 39가 `PRIMARY_LEAN`, Detroit 42가 대안, Lakers 47이 하한선이다. Lakers는 드래프트 전날 39순위 픽 자체의 거래에 합의했으므로 거래 구조는 PASS지만 내부 선호 증거 전 LOCK하지 않는다.
- `Trent 39→Bonga 44 Washington→Sanon 미지명/Olimpija`가 현행 주 후보 사슬이다. San Antonio 49는 LOW, Charlotte 55는 같은 기능의 대안이며 Tony Carr 51은 유지 STRONG이다. 이 지점에서 드래프트 보드 경계는 PASS지만 정확 결과는 정본이 아니다.
- 2019 Spellman–Damian Jones 거래는 복원 가능, 2020 Russell–Wiggins 거래는 계약 구조 PASS·정확 Hutchison 자산 HOLD다.
- Portland에 Trent가 없으므로 2021 Powell–Trent 거래는 원형 불성립이며 `NO_TRADE_BASELINE`부터 다시 계산한다.
- Bonga가 Lakers에 없더라도 Trent가 같은 3년 최소급 구조를 받으면 2019-20 급여가 $1,416,852로 같아 2019 Anthony Davis 거래의 cap mechanics는 복원 가능하다. Trent의 Washington 이동과 2021 RFA·Chicago 거래 파급은 다시 계산한다.
- 이 v0.28은 Chicago 원클럽·동서부 라이벌 방향을 변경하지 않는다. 주인공의 정확 22순위, 신체 수치, 루키 분·기록은 계속 `HOLD`다.

## v0.28 RESEARCH_HOLD

- Lakers의 39순위 내부 보드에서 Trent 대 Bonga 선호
- Trent 39 Lakers 대 42 Detroit 최종 팀보드
- Lakers의 Trent/Bonga·Washington의 익명 선호 반증과 Sanon 49/55 대안
- 2019 Anthony Davis 거래로 Washington에 이동한 Trent의 역할·2021 RFA·Chicago 거래 파급
- Trent 부재 시 2021 Portland–Toronto 거래와 Norman Powell 행선지
- Hutchison의 2020 역할·가치와 Russell–Wiggins 거래의 정확 보조 자산
- Chicago 22부터 60까지 전체 연쇄의 인과 경계와 정확 지명 순번

## v0.29 PARTIAL ADDITIONS — 연도별 우선순위·2021 거래 구조 감사

- 실제 NBA의 매년 로스터·계약·픽·드래프트·이적은 기본값으로 전수 대조한다. 주인공·라이벌이 입력을 바꾼 사건만 심층 재계산한다.
- 미래 거래는 드래프트 나비효과의 blocker를 찾기 위해 구조를 미리 감사할 수 있다. 그러나 거래의 실제 발생은 앞선 시즌의 승수·로터리·로스터를 시간순으로 계산하기 전 LOCK하지 않는다.
- Chicago에 Hutchison이 없는 조건에서도 `Chicago: Theis+Green / Washington: Gafford / Boston: Wagner+Kornet`의 3팀 5인 거래는 2020-21 급여 매칭을 통과한다. Troy Brown Jr.와 Trent는 Washington에 남는다. 이전 `최소 6인` 표기는 O-15F5에서 선수 수 오기로 정정했다.
- 위 거래는 Chicago가 실제와 같은 2021 마감일 매수·Vučević 후속 보강 동기에 도달할 때의 `CONDITIONAL_STRUCTURE_PASS`다. 사건 발생 자체는 O-15B~D 전까지 `HOLD`다.
- Washington의 Trent는 3년 계약 종료 뒤 qualifying offer가 있으면 2021 RFA가 되고, 거래로 이어진 Bird 서비스에 따라 Washington이 cap을 넘겨 재계약할 제도 경로가 있다. 정확 QO·계약·행선지는 대체 역사 2019-21 생산 전까지 `HOLD`다.
- Portland에 Trent가 없으면 실제 Powell 거래는 원형 불성립이다. Hood만으로 급여는 맞지만 Trent의 젊은 득점·RFA 가치는 대체되지 않으므로 `PORTLAND_NO_TRADE_PRIMARY`에서 시작한다.
- Powell의 정확한 2021 행선지와 Portland의 이후 플레이오프 분·Bird rights·2022 거래는 해당 시즌 원장에서 계산한다. Evans·Simons·Little에게 Trent나 Powell의 실제 성과를 자동 이전하지 않는다.
- 상세 권위는 `simulation/2021_WASHINGTON_CHICAGO_PORTLAND_TRANSACTION_CASCADE.md`다.

## v0.29 RESEARCH_HOLD

- Washington Trent와 Troy Brown Jr.의 2019-21 player-game·분·슈팅·시장가치
- Washington의 Trent qualifying offer·재계약·별도 거래
- Chicago의 대체 2020-21 성적·Vučević 거래·마감일 매수 동기와 5인 거래 발생 여부
- Portland Evans의 2018-21 생산·계약 구조와 Toronto가 수용할 자산가치
- Powell의 2021 마감일 타팀 행선지 또는 Toronto 잔류와 2021 자유계약
- Portland의 Powell 부재 후 정규시즌·플레이오프 분, 2021-22 roster와 2022 Clippers 거래 파급

## v0.30 PARTIAL ADDITIONS — Chicago 루키 donor·Windy City·자기관리

- Chicago 루키는 실제 Hutchison의 드래프트·로스터 기능을 대체하지만 Hutchison의 오른발 부상은 상속하지 않는다.
- LaVine·Markkanen·Dunn·Carter·Porter·Lopez·Arcidiacono·Holiday·Portis의 실제 분은 우선 0분 차감으로 보호한다.
- 1월 25일까지 Hutchison의 실제 44경기·894.6분을 1차 player-game 슬롯으로 사용하되, 2018년 12월 7일 자기관리 비용과 2019년 1월 9·11·12일 Windy City 개발창은 주인공 NBA 분에서 제외한다.
- 1월 25일까지 40경기·11선발·798:02, 이후 33경기 476분이며 시즌 역할선은 **73경기·11선발·1,274:02·평균 17.45분**으로 `PROVISIONAL_LOCK`한다.
- 자기관리 재발 후보는 2018년 12월 4일 원정 뒤 밤샘 게임→12월 5일 영상·컨디셔닝 체크인 지각→12월 7일 약 10~12분 NBA 로테이션 기회 상실이다. 정확 시작 시각·지각 분수·벌금은 `HOLD`이며 급여 삭감을 자동 적용하지 않는다.
- Windy City 후보 배정은 2019년 1월 7~13일이고, 1월 11~12일 홈 2연전에서 경기당 24~28분의 세컨드사이드 판단·POA/스크린 내비게이션 반복을 목표로 한다.
- Windy City 배정은 1라운드 표준 NBA 계약을 유지하는 assignment이며 투웨이 전환이 아니다. CBA상 misconduct 징계 목적으로 사용하지 않고, 12월 지각과 한 달 이상 분리된 개발 결정으로 둔다.
- 해당 개발창에서 Chicago의 1월 9·11·12일 NBA 슬롯 85분을 동시에 사용할 수 없다. G League 52분도 실제 Windy City 선수들의 240분에서 분산 차감한다.
- 후반 추가 476분의 같은 날짜 donor는 Selden 137·Harrison 119·Blakeney 61·Luwawu-Cabarrot 73·Alkins 27·Brandon Sampson 35·JaKarr Sampson 24분이다. 한 경기 최대 6분만 차감하고 실제 당일 출전분을 최소 6분 남긴다.
- 주인공이 빠진 네 경기의 실제 Hutchison 슬롯 96:35는 Harrison·Parker·Selden·Blakeney·Portis에게 같은 날짜 돌려준다. `Hutchison 894:37 + 실존 선수 순차감 379:25 = 주인공 1,274:02`로 전체 분을 보존한다.
- 상세 권위는 `simulation/CHICAGO_2018_19_PLAYER_GAME_DONOR_VECTOR.md`와 `simulation/CHICAGO_2018_19_RESERVE_RECEIVER_ALLOCATION.md`, 맹점 검토는 `reviews/R02_3Z_CHICAGO_ROOKIE_DONOR_ASSIGNMENT_REVIEW.md`다.

## v0.30 RESEARCH_HOLD

- 73경기·11선발·1,274:02의 개인 박스스코어와 생산성 prior
- 변경된 로테이션의 2018-19 승수·Hoiberg 해임·Holiday/Porter 거래 영향
- 2019 standings·lottery·Coby White 보드와 2020 Patrick Williams 보드

## v0.30 O-15C3 ADDITIONS — 2019 lottery·Coby White

- Chicago의 2018-19 대체 성적은 margin residual 강건성 범위 **22~24승**에서 정확값을 `HOLD`한다.
- 이 전 범위에서 Chicago는 리그 4번째 lottery seed와 1순위 확률 12.5%를 유지한다.
- seed와 조합 배정이 바뀌지 않았으므로 실제 2019 lottery 추첨 결과인 **전체 7순위**를 보존한다. 재추첨하지 않는다.
- Chicago는 7순위에서 **Coby White를 지명**한다. 2019 당시 장기 포인트가드 필요와 저사용률 SF/PF 주인공의 역할 분리가 근거이며 후대 성과는 선택 근거가 아니다.
- Coby·LaVine·주인공의 2019-20 정확 분·선발·사용률·박스는 새 player-game donor 원장 전 `HOLD`다.
- 2020 lottery 결과와 Patrick Williams 지명은 2019-20 결과 뒤 재판정하며 자동 보존하지 않는다.

## v0.30 O-15C4 PARTIAL ADDITIONS — Chicago 2년차 분 예산

- 2019-20 실제 기준선은 65경기·22승 43패·17명 출전·총 15,675분 11초·325선발이다. 취소된 17경기를 복원하지 않는다.
- 활성 Chicago 세계선에 없는 Hutchison의 실제 28경기·10선발·526:48은 주인공의 1차 직접 슬롯이다. Hutchison의 부상과 경기별 출전은 상속하지 않는다.
- 주인공 2년차 범위는 60~65경기·14~22선발·1,320~1,470분이며, BASE 계산안은 **63경기·18선발·1,395분**이다.
- BASE는 Hutchison 526:48과 Valentine·Harrison·Arcidiacono·Mokoka·Strus·Young의 868:12에서만 조달한다. LaVine·Satoransky·Coby·Markkanen·Dunn·Carter·Porter·Gafford·Kornet·Felicio는 0분 차감으로 보호한다.
- 2년차 핵심 업그레이드는 약한 손 운반·클로즈아웃 돌파이며, grab-and-go·숏롤 첫 패스의 완성은 2020-21보다 앞당기지 않는다.
- BASE 63경기·18선발·1,395분은 같은 날짜 player-game·선발 자리 보존 전 `PRECALC_CANDIDATE`다. 개인 박스·승수·2020 lottery·Patrick Williams는 계속 `HOLD`다.

## v0.30 O-15C5 PARTIAL ADDITIONS — Chicago 2년차 player-game

- O-15C4의 BASE 63경기는 독립 결장 원인이 없는 후보였으므로 **65경기·18선발·1,395분**으로 교정해 `PROVISIONAL_LOCK`한다. LOW/HIGH 범위와 이후 시즌 내구성은 잠그지 않는다.
- 실제 65경기의 Chicago 팀 총 15,675:11을 경기별로 보존한다. 취소된 17경기와 실제 없던 실존 선수 출전일은 만들지 않는다.
- 18선발은 실제 Hutchison 선발 10자리와 실제 Harrison 선발의 시간순 최초 8자리에서 이전한다. 새 선발 자리를 만들지 않는다.
- Hutchison·Valentine·Harrison·Arcidiacono·Mokoka·Strus·Young의 시즌 순차감 합계는 1,395:00으로 O-15C4 예산을 유지한다.
- 보호 10인의 시즌 순감은 0이다. donor 희박 경기 연결을 위한 Markkanen·Dunn gross 19:34는 다른 날짜에 전량 반환하며 생산성의 순이전으로 세지 않는다.
- LaVine·Satoransky·Coby·Porter와 센터 4인의 경기별 분은 실제와 동일하다.
- 정확 개인 박스·효율·온오프·승수·2020 standings/lottery·Patrick Williams 보드는 O-15C6 이후까지 `HOLD`다.

## v0.30 O-15C6A PARTIAL ADDITIONS — Chicago 2년차 생산성 prior

- O-15C1의 2018 드래프트 윙 9명을 재선택 없이 두 번째 NBA 시즌까지 추적한다. 2년차 성공자만 골라 비교군을 바꾸지 않는다.
- 주인공 2년차 BASE는 **12.0득점·9.0리바운드·2.2어시스트·1.6스틸·0.9블록/36, TS .530·3PA 3.0·3P .320·USG 15.0%**다.
- 65경기·1,395분 환산 중심은 약 465득점·349리바운드·85어시스트·62스틸·35블록, 경기당 7.15득점·5.37리바운드다. 정확 정수 박스는 `HOLD`다.
- 2년차 핵심 성장은 약한 손 운반·closeout attack·감속 뒤 짧은 패스다. LaVine의 1차 득점과 Coby·Satoransky의 가드 possession을 침범하지 않는다.
- donor 1,395분의 관측 귀속량과 주인공 BASE 차이는 약 -112득점·+107리바운드·-15어시스트·-11스틸·+13블록이다. 이는 선수 귀속 변화이며 팀 생산성 변화가 아니다.
- single net rating·BPM으로 승패를 실행하지 않는다. causal impact·65경기 outcome·2020 standings/lottery·Patrick Williams는 O-15C6B까지 `HOLD`다.

## v0.30 O-15C6B PARTIAL ADDITIONS — Chicago 2년차 outcome·2020 lottery

- 실제 65경기 최종 점수차와 같은 날짜 player-game delta에 BPM·NBA NET_EB 두 proxy를 적용한다. 무피로 기본은 BPM 21/22/22승, NET_EB 22/22/24승이다.
- back-to-back 두 번째 밤 9경기에 주인공 rating -0.5~-1.0점/48분 stress를 적용해도 attainable set은 **21·22·24승**이다. exact 승수는 `HOLD`다.
- 실제와 달라지는 경기는 모두 실제 1점 차인 2019-10-23 Charlotte, 2019-11-23 Charlotte, 2019-12-09 Toronto뿐이다. 실제 2점 차 이상 경기 반전은 없다.
- 2020 lottery 입력은 Chicago 22-43 seed 7, Charlotte 23-42 seed 8, Washington 24-40 seed 9다. bubble 최종 Washington 25-47을 lottery seed 계산에 쓰지 않는다.
- 21·22승 분기는 Chicago seed 7을 유지해 실제 4순위 추첨 사건을 조건부 보존할 수 있다. 24승 분기는 Charlotte와 seed를 교환해 Chicago seed 8이므로 공개 고정 seed 재추첨이 필요하다.
- 정확 Chicago 승수·lottery seed·pick은 O-15C6C까지 `HOLD`다. 실제 4순위가 유지돼도 18선발·1,395분 SF/PF 주인공과 성장시간이 겹치므로 Patrick Williams 지명은 `REOPEN_REQUIRED / HOLD`다.

## v0.30 O-15C6C PARTIAL ADDITIONS — RAPTOR 교차검증·lottery 작가 게이트

- FiveThirtyEight modern RAPTOR를 제3 impact 계열로 사용한다. 기존 sophomore 9인의 Q1/median/Q3에서 주인공 LOW -2.7·BASE -1.8·HIGH -1.0 prior를 고정한다.
- donor RAPTOR는 league-average 0으로 1,000분 수축한다. primary 결과는 20/21/22승이고, 500~2,000분 regularizer·fatigue stress에서는 19~22승이다.
- BPM·NET_EB·RAPTOR_EB를 모두 합친 model-risk tail은 19~24승이다. tail을 동일 가중하거나 평균내 exact 승수로 쓰지 않는다.
- 세 계열의 BASE와 second-night stress만 보면 **21~22승**, Chicago 2020 lottery **seed 7**이 공통이다.
- 총괄 추천은 exact 승수 21~22 `HOLD`를 유지하면서 seed 7·1순위 7.5%·실제 4순위 추첨 사건만 보존하는 A안이다. 이는 `AUTHOR_APPROVAL_REQUIRED / NOT_CANON`이다.
- 실제 4순위가 승인돼도 Patrick Williams 지명은 자동 보존하지 않는다. 4순위 당시 보드는 주인공과의 성장시간 중복을 포함해 재심사한다.

## v0.30 O-15C7 PARTIAL ADDITIONS — 2020 lottery A안·조건부 4순위 보드

- 작가 선택 A를 반영한다. Chicago 2019-20 exact 성적은 **21~22승 `HOLD`**, 2020 lottery seed 7·1순위 확률 7.5%·실제 전체 4순위 추첨 사건은 `LOCKED`다.
- 전체 4순위 보유와 Patrick Williams 실제 지명은 별도 사건이다. Patrick은 자동 보존하지 않는다.
- 실제 Edwards·Wiseman·Ball이 1~3순위에서 모두 지명된 조건의 5인 보드는 **Haliburton > Avdija > Williams > Vassell > Okoro**다. 이는 `CONDITIONAL_BOARD_PASS`이며 정확 지명이 아니다.
- 가상 라이벌은 같은 2020 Draft의 1순위급 후보다. 라이벌의 서부 팀·순번이 1~3순위 보드와 4순위 가용선수를 바꿀 수 있으므로 Chicago 정확 지명은 `UPSTREAM_RIVAL_BLOCKER / HOLD`다.
- Patrick은 실제 Chicago 프런트의 운동능력·다포지션 수비·상한 선호 때문에 후보로 생존한다. 그러나 2년차 주인공과 SF/PF 수비·성장시간이 가장 크게 겹쳐 조건부 3순위로 하향한다.
- 다음 인과 단계는 O-15D 거래가 아니라 O-15E 라이벌의 2020 서부 착지·상위 1~3순위 팀보드다. 이 상류 보드가 닫힌 뒤 Chicago 4순위와 2020-21 roster를 재실행한다.

## v0.30 O-15E1 PARTIAL ADDITIONS — 라이벌 Minnesota 1순위

- 작가 선택 A를 반영해 라이벌은 **2020 Draft 전체 1순위로 Minnesota Timberwolves에 지명**된다. 거래 없는 직접 지명이며 팀·순번은 `AUTHOR_APPROVED / LOCKED`다.
- 이 선택은 라이벌의 정확 신체·공격형·성격·신인 기록·사용률·베테랑 멘토를 자동 승인하지 않는다. 해당 항목은 계속 `HOLD`다.
- Anthony Edwards는 삭제하거나 Golden State 2순위로 자동 이동시키지 않는다. Golden State 2→Charlotte 3→Chicago 4를 각 팀의 당시 보드로 다시 판정한다.
- 주 분기는 **Wiseman 2 `RETENTION_STRONG_LEAN` → Edwards 3 `PRIMARY_LEAN` → LaMelo 4 `PRIMARY_LEAN / AUTHOR_GATE`**다.
- Charlotte가 Edwards와 Ball을 동시에 비교한 공개 내부 보드는 확인되지 않았다. 반대 분기 `Charlotte Ball 3 → Chicago Edwards 4`를 유지하며 2~4순위 exact 선택은 아직 정본이 아니다.
- 상세 권위는 `simulation/2020_DRAFT_TOP4_SEQUENTIAL_BOARD.md`, 맹점 검토는 `reviews/R01_2020_DRAFT_TOP4_SEQUENTIAL_BOARD_REVIEW.md`다.

## v0.30 O-15E2 PARTIAL ADDITIONS — 2020 Draft 상위 4순위

- 작가 선택을 반영해 정확한 상위 4순위는 **Minnesota 가상 라이벌 → Golden State James Wiseman → Charlotte Anthony Edwards → Chicago LaMelo Ball**이다. 네 지명은 `AUTHOR_APPROVED / LOCKED`다.
- Charlotte가 LaMelo를 유지하고 Chicago가 Edwards를 받는 분기는 `REJECTED_HISTORICAL_CONTINGENCY`로 비교 이력에만 남긴다.
- Chicago의 LaMelo 4순위는 Coby White·LaVine의 분·볼 소유·수비 비용을 없애지 않는다. 이 비용은 2020-21 player-game 원장에서 지불한다.
- Patrick Williams는 삭제하지 않는다. Cleveland 5순위 Okoro 유지 `STRONG_LEAN`, Atlanta 6순위 Okongwu 유지 `LEAN`, Detroit 7순위 Patrick을 `PRIMARY_LEAN / AUTHOR_GATE`로 둔다.
- Patrick이 Detroit 7순위로 가면 Killian Hayes를 8순위부터, Atlanta 6순위로 가면 Onyeka Okongwu를 7순위부터 다시 계산한다. 재착지 선택과 밀려난 선수 연쇄가 닫히기 전 2020-21 roster·승패를 확정하지 않는다.
- 상세 권위는 `simulation/2020_DRAFT_PATRICK_WILLIAMS_RELANDING_BOARD.md`, 맹점 검토는 `reviews/R01_2020_DRAFT_PATRICK_RELANDING_REVIEW.md`다.

## v0.30 O-15E3 PARTIAL ADDITIONS — Patrick Williams Detroit 7순위

- 작가 선택 A를 반영해 **Cleveland Isaac Okoro 5 → Atlanta Onyeka Okongwu 6 → Detroit Patrick Williams 7**을 `AUTHOR_APPROVED / LOCKED`로 둔다.
- Atlanta가 Patrick을 6순위로 지명하는 분기는 `REJECTED_HISTORICAL_CONTINGENCY`다. Detroit promise 보도는 공식 구단 확인이 아니라 작가 선택을 보조한 동시대 정황으로만 취급한다.
- Patrick에게 밀린 실제 7순위 Killian Hayes는 삭제하지 않는다. New York 8순위부터 새 팀보드에 넣는다.
- 8~12순위 실제 지명인 Obi Toppin·Deni Avdija·Jalen Smith·Devin Vassell·Tyrese Haliburton 유지는 팀별 근거를 통과한 주안이다. 정확 LOCK은 다음 작가 결정에 포함한다.
- 첫 활성 분기는 New Orleans 13순위다. Hayes 13순위를 `PRIMARY_LEAN / AUTHOR_GATE`, Kira Lewis Jr. 유지를 대안으로 둔다.
- A Hayes 13이면 Kira를, B Lewis 13이면 Hayes를 Boston 14순위부터 다시 계산한다. 이 연쇄가 닫히기 전 Chicago 2020-21 roster·승패를 확정하지 않는다.
- 상세 권위는 `simulation/2020_DRAFT_KILLIAN_HAYES_RELANDING_BOARD.md`, 맹점 검토는 `reviews/R01_2020_DRAFT_KILLIAN_HAYES_RELANDING_REVIEW.md`다.

## v0.30 O-15E4 PARTIAL ADDITIONS — Killian Hayes New Orleans 13순위

- 작가 선택 A를 반영해 **New York Obi Toppin 8 → Washington Deni Avdija 9 → Phoenix Jalen Smith 10 → San Antonio Devin Vassell 11 → Sacramento Tyrese Haliburton 12 → New Orleans Killian Hayes 13**을 `AUTHOR_APPROVED / LOCKED`로 둔다.
- 이에 따라 2020 Draft 정확 1~13순위가 정본화됐다. New Orleans의 실제 Kira Lewis 13 유지분기는 `REJECTED_HISTORICAL_CONTINGENCY`다.
- 공개되지 않은 New Orleans의 Hayes–Lewis 내부 head-to-head가 확인된 것으로 쓰지 않는다. 정확 선택은 작가가 당시 평가와 포인트가드 선택 의사를 함께 보존해 결정한 것이다.
- Hayes에게 밀린 Kira Lewis Jr.는 삭제하지 않는다. Boston 14순위의 Aaron Nesmith는 Ainge·Stevens의 직접 평가 때문에 `RETENTION_STRONG_LEAN`이다.
- 첫 활성 분기는 Orlando 15순위다. 실제 Cole Anthony 유지가 `RETENTION_LEAN / AUTHOR_GATE`, Kira 15순위가 contingency다.
- A Nesmith 14·Cole 15 유지면 Kira를, B Nesmith 14·Kira 15면 Cole을 Detroit가 통제한 16순위부터 재판정한다. 이 연쇄가 닫히기 전 Chicago 2020-21 roster·승패를 확정하지 않는다.
- 상세 권위는 `simulation/2020_DRAFT_KIRA_LEWIS_RELANDING_BOARD.md`, 맹점 검토는 `reviews/R01_2020_DRAFT_KIRA_LEWIS_RELANDING_REVIEW.md`다.

## v0.30 O-15E5 PARTIAL ADDITIONS — Nesmith 14·Cole Anthony 15 유지

- 작가 선택 A를 반영해 **Boston Aaron Nesmith 14 → Orlando Cole Anthony 15**를 `AUTHOR_APPROVED / LOCKED`로 둔다. 이에 따라 2020 Draft 정확 1~15순위가 정본화됐다.
- Orlando가 Kira Lewis를 15순위에 지명하는 분기는 `REJECTED_HISTORICAL_CONTINGENCY`다. 이 결정은 공개되지 않은 Cole–Kira 내부 head-to-head가 확인됐다는 뜻이 아니다.
- Kira는 삭제하지 않고 Detroit가 통제한 16순위부터 재판정한다. 실제 16순위는 Portland가 행사한 뒤 Houston을 거쳐 Detroit로 이동했고, Christian Wood sign-and-trade·Trevor Ariza·보호 픽이 결합된 거래다.
- 실제 Detroit는 Hayes 7로 포인트가드를 확보한 뒤 Isaiah Stewart를 16번에서 지명했다. 현재 세계선은 Patrick 7이라 가드 공백이 남고 Detroit가 Kira를 실제 워크아웃했으므로 **Kira 16 `PRIMARY_LEAN / AUTHOR_GATE`**를 주안으로 둔다.
- Weaver가 Stewart를 특정 후보로 두고 16순위 픽을 확보했다는 구단 회고가 있으므로 Stewart 16 유지를 실현 가능 대안으로 보존한다. 가드 필요나 실제 픽 어느 한쪽으로 자동 LOCK하지 않는다.
- A Kira 16이면 Stewart를, B Stewart 16 유지면 Kira를 Oklahoma City가 통제한 17순위부터 다시 계산한다. 선수 변경과 16순위 거래 경제를 분리해 검산한다.

## v0.30 O-15E6 PARTIAL ADDITIONS — Kira Lewis Jr. Detroit 16순위

- 작가가 직전 총괄 추천을 이어서 진행하도록 승인해 **Detroit 통제 16순위 Kira Lewis Jr.**를 `AUTHOR_APPROVED / LOCKED`로 둔다. 이에 따라 2020 Draft 정확 1~16순위가 정본화됐다.
- Isaiah Stewart 16 유지는 `REJECTED_HISTORICAL_CONTINGENCY`로 보존한다. 이는 Detroit의 비공개 Kira–Stewart 내부 head-to-head가 확인됐다는 뜻이 아니다.
- Stewart는 삭제하지 않고 Oklahoma City가 통제한 17순위부터 재판정한다. OKC의 Pokuševski 목적 상향 거래 때문에 Poku 17 유지가 `RETENTION_STRONG_LEAN`이다.
- Dallas는 외곽 수비형 윙 Josh Green 18 유지 `RETENTION_LEAN`, Stewart가 19번까지 남으면 별도 픽을 통제한 Detroit가 Stewart를 회수하는 안을 `PRIMARY_LEAN / AUTHOR_GATE`로 둔다.
- 총괄 추천은 **Pokuševski 17 → Josh Green 18 → Stewart 19**다. 이 경우 Saddiq Bey를 Miami 20순위부터 재판정한다. 정확 17~19순위는 작가 승인 전 `HOLD`다.
- 16순위 Wood 거래, 17순위 Rubio 3팀 거래, 19순위 Kennard–Shamet 3팀 거래를 선수 한 명의 이동으로 자동 유지·소멸시키지 않는다.

## v0.30 O-15E7 PARTIAL ADDITIONS — Pokuševski 17·Josh Green 18·Stewart 19

- 작가가 직전 총괄 추천을 이어서 진행하도록 승인해 **Oklahoma City Pokuševski 17 → Dallas Josh Green 18 → Detroit Isaiah Stewart 19**를 `AUTHOR_APPROVED / LOCKED`로 둔다. 이에 따라 2020 Draft 정확 1~19순위가 정본화됐다.
- Stewart 17과 Stewart 18 분기는 `REJECTED_HISTORICAL_CONTINGENCY`로 보존한다. 이는 OKC·Dallas의 비공개 내부 보드가 확인됐다는 뜻이 아니다.
- Stewart에게 밀린 Saddiq Bey는 삭제하지 않고 Miami 20순위부터 재판정한다.
- Miami는 명시적 빅맨 필요 때문에 Precious Achiuwa 20 유지, Philadelphia는 Morey의 lottery급·포지션 필요 평가 때문에 Tyrese Maxey 21 유지를 각각 `RETENTION_STRONG_LEAN`으로 둔다.
- Denver는 Bey를 동시대 공식 프로필에서 팀과 강하게 연결된 후보로 검토했고 Bey가 실제 19순위 가치이므로 **Bey 22 `PRIMARY_LEAN / AUTHOR_GATE`**를 주안으로 둔다.
- 총괄 추천은 **Achiuwa 20 → Maxey 21 → Bey 22**다. 이 경우 Zeke Nnaji를 Minnesota 통제 23순위부터 재판정하며 Denver 통제 24순위의 RJ Hampton과 함께 계산한다.

## v0.30 O-15E8 PARTIAL ADDITIONS — Achiuwa 20·Maxey 21·Saddiq Bey 22

- 작가가 직전 총괄 추천을 이어서 진행하도록 승인해 **Miami Precious Achiuwa 20 → Philadelphia Tyrese Maxey 21 → Denver Saddiq Bey 22**를 `AUTHOR_APPROVED / LOCKED`로 둔다. 이에 따라 2020 Draft 정확 1~22순위가 정본화됐다.
- Bey 20과 Bey 21 분기는 `REJECTED_HISTORICAL_CONTINGENCY`로 보존한다. 이는 세 팀의 비공개 내부 head-to-head가 확인됐다는 뜻이 아니다.
- Bey에게 밀린 Zeke Nnaji는 삭제하지 않고 Minnesota 통제 23순위부터 재판정한다.
- Minnesota는 25·33순위를 지불해 23순위 Bolmaro를 얻은 목적 상향 거래 때문에 **Bolmaro 23 `RETENTION_STRONG_LEAN`**이다.
- 실제 Denver는 자기 22순위로 Nnaji를 먼저 지명하고 별도 4팀 거래로 Hampton 24를 얻었다. Nnaji가 24번까지 남으면 Denver가 회수하는 안을 **`PRIMARY_LEAN / AUTHOR_GATE`**로 둔다.
- 총괄 추천은 **Bolmaro 23 → Zeke Nnaji 24**다. 이 경우 R.J. Hampton을 New York 통제 25순위부터 재판정한다. 정확 23~24순위는 작가 승인 전 `HOLD`다.

## v0.30 O-15E9 PARTIAL ADDITIONS — Bolmaro 23·Zeke Nnaji 24

- 작가가 직전 총괄 추천을 이어서 진행하도록 승인해 **Minnesota Leandro Bolmaro 23 → Denver Zeke Nnaji 24**를 `AUTHOR_APPROVED / LOCKED`로 둔다. 이에 따라 2020 Draft 정확 1~24순위가 정본화됐다.
- Nnaji 23과 Hampton 24 분기는 `REJECTED_HISTORICAL_CONTINGENCY`로 보존한다. 이는 Minnesota·Denver의 비공개 내부 head-to-head가 확인됐다는 뜻이 아니다.
- Nnaji에게 밀린 R.J. Hampton은 삭제하지 않고 New York 통제 25순위부터 재판정한다.
- New York Quickley 25, Boston Pritchard 26, Utah Azubuike 27, Minnesota McDaniels 28, Toronto Flynn 29, Memphis Bane 30은 각각 슈팅 필요·직접 선호·역할·목적 거래 근거 때문에 유지 주안이다.
- Hampton의 첫 합리적 재착지는 Dallas 31순위다. Dallas가 Hampton과 실제 사전 인터뷰를 했고 Hampton이 실제 24순위보다 7계단 내려왔지만, Tyrell Terry의 Luka 옆 슈팅 적합성과 공개 Hampton–Terry 내부 비교 부재 때문에 **`PRIMARY_LEAN / AUTHOR_GATE`**로 둔다.
- 총괄 추천은 **실제 25~30 유지 → R.J. Hampton 31**이다. 이 경우 Tyrell Terry를 Charlotte 통제 32순위부터 재판정한다. 정확 25~31순위는 작가 승인 전 `HOLD`다.
- 25·27·28·30순위의 거래는 선수 선택 변화만으로 자동 유지·소멸하지 않는다.

## v0.30 O-15E10 PARTIAL ADDITIONS — 실제 25~30 유지·R.J. Hampton 31

- 작가가 직전 총괄 추천을 이어서 진행하도록 승인해 **New York Quickley 25 → Boston Pritchard 26 → Utah Azubuike 27 → Minnesota McDaniels 28 → Toronto Flynn 29 → Memphis Bane 30 유지 → Dallas R.J. Hampton 31**을 `AUTHOR_APPROVED / LOCKED`로 둔다. 이에 따라 2020 Draft 정확 1~31순위가 정본화됐다.
- Hampton 26과 Tyrell Terry 31 분기는 `REJECTED_HISTORICAL_CONTINGENCY`로 보존한다. 이는 Boston·Dallas의 비공개 내부 head-to-head가 확인됐다는 뜻이 아니다.
- Hampton에게 밀린 Tyrell Terry는 삭제하지 않고 Charlotte 통제 32순위부터 재판정한다.
- 실제 Charlotte는 LaMelo 3으로 playmaking을 얻은 뒤 Carey 32와 추가 비용을 낸 Richards 42로 센터층을 보강했다. 현재 세계에서는 Edwards 3이 LaMelo의 창출 기능을 그대로 대체하지 않으므로 Terry 32 검토가 강해진다.
- Graham·Rozier가 남아 있고 Carey·Richards의 센터 보강 목적도 분명하므로 **Tyrell Terry 32 `PRIMARY_LEAN / AUTHOR_GATE`**로 둔다. 공개 Terry–Carey 내부 보드는 확인되지 않았다.
- 총괄 추천은 **Tyrell Terry 32**다. 이 경우 Vernon Carey Jr.를 LA Clippers 통제 33순위부터 재판정한다. 정확 32순위는 작가 승인 전 `HOLD`다.
- Charlotte의 42순위 Nick Richards 권리 거래는 32순위 선택 변화만으로 자동 유지·소멸하지 않는다.

## v0.30 O-15E11 PARTIAL ADDITIONS — Tyrell Terry Charlotte 32순위

- 작가가 직전 총괄 추천을 이어서 진행하도록 승인해 **Charlotte Tyrell Terry 32**를 `AUTHOR_APPROVED / LOCKED`로 둔다. 이에 따라 2020 Draft 정확 1~32순위가 정본화됐다.
- Vernon Carey Jr. 32 유지 분기는 `REJECTED_HISTORICAL_CONTINGENCY`로 보존한다. 이 결정은 Charlotte의 공개 Terry–Carey 내부 head-to-head가 확인됐다는 뜻이 아니다.
- Carey는 삭제하지 않고 LA Clippers가 통제한 33순위부터 재판정한다.
- Clippers Oturu 33, Oklahoma City Maledon 34, Memphis Tillman 35, Dallas Tyler Bey 36, Oklahoma City Krejčí 37, Detroit Saben Lee 38, Utah Hughes 39, Sacramento Woodard 40, San Antonio Tre Jones 41은 목적 거래·직접 역할 때문에 유지 주안이다.
- Charlotte는 실제로 2024 2라운드 지명권을 내고 42순위 센터 슬롯을 취득했고, 실제 같은 보드에서 Carey를 Richards보다 먼저 선택했다. 작가 승인으로 **실제 33~41 유지 → Charlotte Carey 42**를 `AUTHOR_APPROVED / LOCKED`로 둔다. 정확 1~42순위가 정본화됐다.
- Nick Richards 42 유지와 Clippers Carey 33은 `REJECTED_HISTORICAL_CONTINGENCY`로 보존한다. Richards는 삭제하지 않고 43순위부터 재판정한다.
- Sacramento Ramsey 43부터 LA Clippers Scrubb 55까지는 역할·stash·권리 거래 때문에 유지 주안이다. Chicago Simonović 44는 같은 빅 포지션의 첫 충돌이지만 새 프런트의 장기 관찰과 stash 기능을 보존한다.
- Charlotte는 Edwards 3·Terry 32로 가드 개발 자원이 늘었고 실제 두 센터 보강 방향은 남는다. 작가 승인으로 **실제 43~55 유지 → Charlotte Nick Richards 56**을 `AUTHOR_APPROVED / LOCKED`로 둔다. 정확 1~56순위가 정본화됐다.
- Grant Riller 56 유지와 Chicago Richards 44는 `REJECTED_HISTORICAL_CONTINGENCY`로 보존한다. Riller는 삭제하지 않고 57순위부터 재판정한다.
- Brooklyn Perry 57, Philadelphia Paul Reed 58, Toronto Jalen Harris 59, Milwaukee Sam Merrill 60은 직접 권리 거래·구단 평가를 보존해 `AUTHOR_APPROVED / LOCKED`로 둔다.
- 작가 승인으로 **실제 57~60 유지 → Riller 미지명 자유계약 시장**을 `AUTHOR_APPROVED / LOCKED`로 둔다. 2020 Draft 1~60 연쇄가 정본화됐다.
- Toronto Riller 59와 Milwaukee Riller 60은 `REJECTED_HISTORICAL_CONTINGENCY`로 보존한다. Riller의 정확 팀·표준/투웨이/Exhibit 10 계약은 2020-21 opening roster 원장까지 `HOLD`한다.
- 세계관 설정집은 이미 정본 문서에 누적 중이다. `World Bible v1.0`은 드래프트 하나의 종료가 아니라 NBA 거래·장기 커리어·전체 구조·통합/독립 검수·작가 승인까지 닫힌 뒤 승격한다.

## v0.30 O-15F PARTIAL ADDITIONS — Chicago 2020-21 opening roster·역할 기준선

- 실제 Chicago opening roster는 표준계약 15명 + 투웨이 2명이다. 대체 세계에서는 `Chandler Hutchison→주인공`, `Patrick Williams→LaMelo Ball`로 두 표준계약 자리만 1대1 치환하며 별도 방출을 만들지 않는다.
- LaMelo는 Patrick과 같은 전체 4순위 rookie-scale 슬롯을 사용한다. 주인공은 2018 정확 지명 순번이 `HOLD`이므로 Hutchison과 정확 급여가 같다고 잠그지 않고 1라운드 표준계약 계층만 유지한다.
- 역할 provisional BASE는 주인공 68경기·58선발·1,938분·28.5 MPG, LaMelo 64경기·32선발·1,760분·27.5 MPG다. 이는 결과 정본이 아니라 O-15F1 player-game 제작 목표다.
- 합계 3,698분에서 Patrick 1,983분과 Hutchison 64분의 직접 대체 pool 2,047분을 빼면 1,651분이 추가로 필요하다. 이 분은 Satoransky·Valentine·Arcidiacono를 우선하고 Coby·Temple을 제한적으로 검토하되 같은 날짜 active list·선발 5자리·포지션을 보존한다.
- 첫날 선발은 Coby–LaVine–주인공–Markkanen–Carter를 provisional base로 둔다. LaMelo는 첫 가드 교체와 두 번째 유닛 1차 창출자로 시작하며 게임 10~20 평가 뒤 선발 전환을 검토한다. 정확 전환일은 `HOLD`다.
- LaMelo의 실제 Charlotte 51경기·신인왕·손목 부상은 Chicago 결과로 복사하지 않는다. 손목 사건은 `INJURY_EVENT_HOLD`다.
- Vucevic 거래와 Washington–Chicago–Boston 3팀 거래는 대체 세계의 2021-03-24까지 성적·수요가 계산되기 전 발생을 잠그지 않는다. Hutchison 부재 때문에 후자는 실제 원형 그대로는 발생할 수 없다.
- Riller의 미지명 시장 진입은 LOCK이지만 정확 팀·계약 종류는 Chicago opening roster만으로 결정되지 않아 계속 `HOLD`다.
- 상세 권위는 `research/CHICAGO_2020_21_OPENING_ROSTER_BASELINE.md`와 `simulation/CHICAGO_2020_21_ROLE_ARCHITECTURE.md`다.

## v0.30 O-15F1 PARTIAL ADDITIONS — Chicago 2020-21 마감일 전 player-game

- 실제 2020-12-23~2021-03-24 Chicago 기준선은 43경기·19승 24패·팀 10,420:02·215선발이다. 승패는 분 배정에 사용하지 않은 식별 기준선이며 alternate 결과가 아니다.
- 같은 날짜 보존을 통과한 마감일 전 역할은 주인공 43경기·43선발·1,219분, LaMelo 43경기·25선발·1,191분이다. 두 값은 `PREDEADLINE_ROLE_PROVISIONAL_LOCK`이며 개인 생산성·승패를 잠그지 않는다.
- 주인공은 Patrick Williams의 42선발과 Patrick 결장일의 Garrett Temple 한 선발을 이어받는다. LaMelo는 첫 18경기 bench 적응 뒤 2021-02-01부터 선발하고 Coby 18선발·Satoransky 7선발을 대체한다.
- Patrick 1,192:50과 Hutchison 63:35의 직접 pool 1,256:25를 제거한다. 두 가상 선수의 합계 2,410분과의 차이 1,153:35는 Satoransky 330:00·Valentine 360:00·Arcidiacono 139:22·Coby 220:00·Temple 80:38·Porter 23:35에서 같은 날짜로 이전한다.
- Coby는 43경기·18선발·1,142:04, Temple은 35경기·11선발·896:49를 유지한다. LaVine·Markkanen과 센터진의 경기별 분은 실제와 같다.
- Young은 2021-03-12의 0:38을 실제 출전일인 2020-12-31에 반환하는 gross bridge만 사용하며 시즌 net·경기·선발은 모두 실제와 같다.
- LaMelo가 마감일 전 43경기 모두 active인 것은 Chicago 고유 부상 입력이 없는 계산 BASE다. Charlotte 손목 사건을 영구 삭제하지 않으며 이후 부상은 `INJURY_EVENT_HOLD`다.
- O-15F3 43경기 outcome 전에는 실제 19승 24패·Vučević 거래·3팀 거래를 alternate 정본으로 쓰지 않는다.
- 상세 권위는 `simulation/CHICAGO_2020_21_PREDEADLINE_PLAYER_GAME.md`다.

## v0.30 O-15F2 PARTIAL ADDITIONS — Chicago 2020-21 마감일 전 생산성 prior

- 주인공 3년차 BASE는 **14.5득점·9.8리바운드·3.2어시스트·1.7스틸·1.0블록/36, TS .555·3PA 3.6·3P .335·USG 17.0%**다. 1,219분 환산 참고선은 11.42점·7.72리바운드·2.52어시스트다.
- 주인공 비교군은 2018-19 루키 9인을 2020-21까지 재선택 없이 추적한다. Jacob Evans의 NBA 0분을 탈락 표본으로 보존한다.
- LaMelo Chicago BASE는 **18.0득점·6.8리바운드·7.2어시스트·1.7스틸·0.4블록/36, TS .535·3PA 6.0·3P .335·USG 21.5%**다. 1,191분 환산 참고선은 13.85점·5.23리바운드·5.54어시스트다.
- LaMelo의 Charlotte 손목 전 41경기·21선발·1,174:03 관측치는 약 20.0득점·7.36리바운드·7.70어시스트/36, TS .562다. Chicago BASE는 LaVine·Coby·Satoransky와의 권한 중복 때문에 이를 수축하며 실제 신인왕 기록을 복사하지 않는다.
- Patrick·Hutchison 전량과 여섯 secondary donor의 순차감 비율에 해당하는 관측 제거량은 851.77득점·405.63리바운드·213.77어시스트·63.13스틸·38.25블록이다.
- 두 가상 선수 BASE와 제거 pool의 차이 +234.72득점·+151.17리바운드·+132.79어시스트·+50.68스틸·+8.85블록·+76.95턴오버는 **선수 귀속 변화**다. 팀 총득점·팀 리바운드·승수에 직접 더하지 않는다.
- 43경기 event별 BASE 기대 박스·donor 선형 제거량 입력은 `PASS`지만 causal impact와 score-margin 변환은 `HOLD`다.
- exact 정수 박스·LaMelo 손목 사건·alternate 마감일 성적·Vučević 및 3팀 거래 발생은 계속 `HOLD`다.
- 상세 권위는 `simulation/CHICAGO_2020_21_PREDEADLINE_PLAYER_PRODUCTION_PRIORS.md`다.

## v0.30 O-15F3 PARTIAL ADDITIONS — Chicago 2020-21 마감일 전 outcome

- 실제 43경기·19승 24패·최종 점수차와 10개의 back-to-back second-night를 기준선으로 고정한다.
- BPM·RAPTOR_EB-1000·2021-03-24 cutoff E_NET_EB-1000의 세 계열을 같은 점수차 잔차에 적용한다. 박스 귀속 증가를 impact rating과 이중 합산하지 않는다.
- BASE와 피로 stress의 중심 기록은 **19~21승**, 동부 위치는 **8~10위권**이다. exact 19·20·21승과 정확 seed는 `HOLD`다.
- 중심 반전 후보는 실제 1점 차였던 2020-12-27 Golden State전과 2021-01-30 Portland전이다. 19승은 둘 다 유지, 20승은 Portland만 반전, 21승은 둘 다 반전한다.
- Young 0:38 bridge는 세 proxy 모두 시즌 impact 합계 0·승패 변화 0경기다. outcome-neutral이어도 분 보존 원장에서는 유지한다.
- 모든 중심 기록에서 Chicago는 플레이인 경쟁·마감일 매수 경계에 남는다. `BUYER_MOTIVE_PASS`는 실제 Vučević 패키지 발생을 뜻하지 않는다.
- 실제 Vučević 거래·3팀 거래·LaMelo 손목 사건·exact 개인 박스는 계속 `HOLD`다. 다음 인과 단계는 O-15F4 Vučević 팀보드다.
- 상세 권위는 `simulation/CHICAGO_2020_21_PREDEADLINE_OUTCOME_ROBUSTNESS.md`다.

## v0.30 O-15F4 PARTIAL ADDITIONS — Chicago 2021 Vučević 거래 팀보드

- 실제 `Vučević+Aminu ↔ Carter+Porter+2021/2023 top-4 보호 1라운드`는 당시 성립 가능한 A안이지만 대체 정본으로 자동 유지하지 않는다.
- LaMelo가 21.5% 사용률의 추가 1차 창출을 공급하므로, 29.9% 사용률의 30세 Vučević가 주는 공격 허브 가치의 한계효용은 실제 Chicago보다 낮다.
- 총괄 추천은 **B — 1라운드 지출 없이 Carter를 유지하는 저사용률 수비 빅 보강 경로**다. 이는 필요 변화에 따른 추천이며 정확 Theis·McGee·buyout 영입을 뜻하지 않는다.
- A 실제 Vučević 패키지, B 저비용 센터 보강, C 무거래는 모두 `AUTHOR_GATE / HOLD`다. 작가 승인 전 거래 발생·마감일 뒤 승수·2021 pick을 잠그지 않는다.
- 작가가 B를 선택하면 Hutchison 없는 `Theis+Green` 3팀 5인 구조와 다른 저비용 빅·타깃 실패를 O-15F5에서 별도 비교한다. 3팀 거래를 Vučević 결정과 합치지 않는다.
- 이후 Carter 성장·실제 2021/2023 픽 선수·Chicago 성적은 사후 결과이며 2021-03-25 당시 선택의 역선택 근거로 사용하지 않는다.
- 상세 권위는 `simulation/CHICAGO_2021_VUCEVIC_TRADE_BOARD.md`다.

## v0.30 O-15F4 AUTHOR ADDITIONS — 저비용 센터 방향 승인

- 작가는 O-15F4 B를 승인했다. Chicago는 실제 Vučević 패키지를 실행하지 않고 **1라운드를 쓰지 않는 저비용 센터 보강을 우선**한다.
- A 실제 Vučević 패키지는 `REJECTED_HISTORICAL_CONTINGENCY`, C 무거래는 `FAILURE_CONTINGENCY`로 보존한다.
- 이 승인은 정확 Theis+Green 5인 거래나 다른 센터 영입을 확정하지 않는다. O-15F5에서 당시 가격·급여·상대 동기를 다시 통과해야 한다.
- Carter·Porter·2021·2023 1라운드는 이 단계에서 Chicago 자산으로 남지만, 정확 거래 선택 뒤 다시 변동할 수 있다.
- 원고 게이트는 계속 `CLOSED`다.

## v0.30 O-15F5 PARTIAL ADDITIONS — Chicago 2021 저비용 센터 거래 보드

- 기존 `최소 6인` 명칭은 선수 수 오기다. 이동하는 고유 선수는 Gafford·Kornet·Theis·Green·Wagner 다섯 명이며 활성 명칭을 **3팀 5인 거래**로 정정한다. 급여 합계와 이동 방향은 변하지 않는다.
- A는 `Chicago: Gafford+Kornet → Theis+Green`, `Washington: Wagner → Gafford`, `Boston: Theis+Green → Wagner+Kornet` 구조다. Brown·Trent는 Washington에 남는다.
- Chicago outgoing $3,767,981 / incoming $6,517,981 / 허용 $6,693,967, Washington $2,161,920 / $1,517,981, Boston $6,517,981 / $4,411,920으로 세 팀 급여 매칭과 roster count를 통과한다.
- Washington의 Gafford 수요와 Boston의 세금 절감 동기는 유지된다. Chicago는 Theis의 저사용률 스크린·수비와 Green의 수비 에너지를 얻지만, Vučević가 없는 세계에서는 값싼 Gafford를 만료계약 Theis로 바꾸는 비용이 실제보다 크다.
- 총괄 추천은 **A — Theis·Green 3팀 5인 거래**다. 구조·가격·당시 세 팀 동기를 가장 구체적으로 통과하지만 정확 사건은 `AUTHOR_GATE / HOLD`다.
- B 다른 저비용 빅은 `SECONDARY_MARKET`, C 타깃 실패·무거래는 `FAILURE_CONTINGENCY`다. 어느 안도 1라운드, Carter, Porter를 지출하지 않는다.
- 정확 거래 선택 뒤에만 마감일 뒤 29경기와 2021 lottery·여름 계약 연쇄를 계산한다. 원고 게이트는 계속 `CLOSED`다.
- 상세 권위는 `simulation/CHICAGO_2021_LOW_COST_CENTER_BOARD.md`와 `simulation/CHICAGO_2021_THEIS_GREEN_TRANSACTION_LEDGER.csv`다.

## v0.30 O-15F5 AUTHOR / O-15F6 ADDITIONS — 2026-09-09

- 작가의 “이어서진행”으로 A의 Theis·Green 3팀 5인 선수 이동을 승인한다. 상태는 `AUTHOR_APPROVED_PLAYER_ROUTE`; 정확 현금·보너스·당일 리그 장부는 `EXECUTION_DETAILS_HOLD`다. D-426의 작가 선택 대기는 이 범위에서 대체된다.
- Chicago는 Carter·Porter·두 1라운드를 보존한다. Orlando의 Vučević·Aminu 별도 경로는 닫히지 않았다.
- 실제 후반 29경기는 12-17·6,960:03·145선발이다. 이는 비교 기준선이며 대체 결과가 아니다.
- 주인공 30분·LaMelo 28분·Carter 26분의 전 경기 가용성 조건에서 Porter 0분과 가변 상한 안은 29경기 총분·선발을 보존한다. Porter 고정 12분은 5경기 28:44 초과다.
- opening의 주인공 68/58/1,938·LaMelo 64/32/1,760 목표는 `REOPEN_REQUIRED_POSTDEADLINE`다. 전반 역할과 충돌하는 임의 결장·벤치 강등을 만들지 않는다. 72경기 조건부 합계를 시즌 정본으로 잠그지 않는다.
- 다음 O-15F6B는 거래 세부·가용성·5인 조합 감사다. 생산성·승패·2021 lottery·여름 계약과 원고 게이트 CLOSED를 유지한다.
- 상세 권위: `simulation/CHICAGO_2020_21_POSTDEADLINE_CAPACITY.md`.

## v0.30 O-15F6B AUDIT ADDITIONS — 2026-09-09

- A 선수 이동 작가 승인은 유지하며 재선택하지 않는다. 공개 근거가 확보되지 않은 거래 보너스·당일 리그 장부는 `EXECUTION_DETAILS_HOLD`다.
- O-15F6 기존 조건부 용량은 최대 2빅 정책에서 Porter 0분 7경기·가변 상한 6경기가 실패한다. 최대 3빅을 허용하면 전 경기 성립하며, 2빅 정책은 NBA 규정이 아니다.
- 같은 날짜 빅→가드·윙 47:05/41:08 순이전과 03-31 Young→Satoransky 선발 교체를 적용한 최소 변경 후보는 두 안 29/29 조합 검산을 통과한다. 정확 분·선발·가용성·전술 효율은 `NOT_CANON`으로 유지한다.
- Hampton Dallas 31순위 정본으로 실제 Denver–Orlando Gordon 거래의 입력이 바뀐다. Hampton을 Denver 자산으로 재사용하거나 Nnaji를 자동 대체하지 않는다.
- 다음은 O-15F6C 상대 거래 보드·가용성·수비 역할 연결이다. 생산성·outcome·lottery·여름 계약·원고는 잠그지 않는다.
- 상세 권위: `simulation/CHICAGO_2020_21_POSTDEADLINE_EXECUTION_AUDIT.md`.

## v0.30 O-15F6C AUDIT ADDITIONS — 2026-09-09

- Denver는 Bey22·Nnaji24, Hampton은 Dallas31이라는 기존 정본을 Gordon 보드에 적용한다. A Harris·Nnaji·보호 미래1R은 협상 기준 추천이며 `EXACT_EVENT_HOLD`다.
- 24번 지명을 취득한 비용은 Hampton 부재로 환급되지 않는다. 대체 Nnaji의 24번 급여는 실제22번 급여와 구분한다.
- Chicago의 단독 결장 87조건 시험에서 Carter 17/29·LaMelo 26/29·Porter 29/29가 조합 증명을 통과했다. 실패 12/3/0은 명시적 상한·선발 정책의 한계이며 실제 부상 일정·확률·승패가 아니다.
- 주인공은 LaMelo 공백 때문에 즉시 전업 PG가 되거나 Carter 공백 때문에 완성형 센터가 되지 않는다. 역할 대응과 성장 단계의 비용을 함께 검토한다.
- 다음 O-15F6D: 거래 실행 조건·선행 픽 의무·Carter 비상 선발/분 대안. 원고는 `CLOSED`다.
- 상세 권위: `simulation/ORLANDO_DENVER_2021_GORDON_BOARD.md`, `simulation/CHICAGO_2020_21_AVAILABILITY_ROLE_RESPONSE.md`.

## v0.30 O-15F6D AUDIT ADDITIONS — 2026-09-09

- Carter 단독 공백 116정책조건 감사 완료. 선발 중첩 축소·Theis 비상30분·Young/Felicio 비상 대응을 단계별 조건부 증명으로 보존한다. 마지막 정책 29/29 통과는 실제 가용성·전력·승수 LOCK이 아니다.
- Gordon 정확 거래·전체 급여·선행 픽 이연 문구는 HOLD다. 비연속 연도 시험을 실제 계약 문구로 승격하지 않는다.
- 후반 직접 일정은 19상대·29경기, Denver 직접 경기0·Orlando1. 미정 Orlando 분기와 다른 상대의 입력 수집을 구분해 O-15F7로 이동한다.
- 설정집 진행은 7매크로 중1완료·1진행·5대기. 버전 숫자나 문서 수를 완료율로 쓰지 않는다. 설계/원고 CLOSED·manuscript_allowed false 유지.

## v0.30 O-15F7 AUDIT ADDITIONS — 2026-09-09

- 후반 실제 양 팀815행·관련300명 cutoff 관측·조건부174박스 귀속 입력을 감사 근거로 보존한다. 주인공/LaMelo의 기존 per36 prior를 유지하며 새 후반 성장 보너스를 부여하지 않는다. 정확 개인/팀 기록 LOCK이 아니다.
- LaMelo 단독 공백 잔여3조건은 실제 분 복원·Coach's Decision DNP 벤치 후보로 대응 가능하다. 전업PG 주인공·실제 부상 일정·무부상 승격은 없다.
- GSW·MIN·CHA·DET·TOR·ORL·BOS의10경기는 상대 변경 분을 계산해야 한다. 나머지19경기는 제한된 검토 범위의 기준선 후보다.
- 무표본14명의 rate는 비워 두며0impact로 간주하지 않는다. 기대 박스 차이를 score-margin에 직접 더하지 않고 다음 양 팀 impact 입력으로 연결한다. 최종72경기 결합 전 전반 모델의 상대 고정 한계를 회수한다.
- 다음 O-15F8. PROJECT_FREEZE v0.30 PARTIAL, 설계/원고 CLOSED·manuscript_allowed false 유지.

## v0.30 O-15F8 AUDIT ADDITIONS — 2026-09-09

- 상대39조건·변경20개 조합·234개 양 팀 영향 입력을 조건부 감사 근거로 보존한다. 기존 Chicago 분·성장 prior는 유지하며 실제 거래·가용성·시즌 사건으로 승격하지 않는다.
- RAPTOR는2021 정규시즌만 사용한 회고적 한 계열이다. 216개 수치 조건28경기의 승패 방향 유지와 Minnesota18조건의 손익분기점을 후반 exact 승수·라이벌 실력 prior로 사용하지 않는다.
- Kira의 cutoff28출전 관측을 보충한다. 라이벌·Riller·Hall·Langford 관련 미정 박스 계수는 유지하며 박스 차이를 점수차에 더하지 않는다.
- Gordon A·Powell 잔류·Fournier·Hall 계약 등은 개별 조건이며 승인된 시즌 경로가 아니다. 전반 상대 고정 한계와 Porter 관측 범위 차이는 최종 연결 전에 회수한다.
- O-15F8 입력 범위 종료. 다음 O-15F9는 독립 영향 계열 교차검증과 시즌 연결 조건이다. v0.30 PARTIAL·설계/원고 CLOSED·manuscript_allowed false 유지.
- 상세 권위: `simulation/CHICAGO_2020_21_POSTDEADLINE_PAIRED_REVIEW.md`.

## v0.30 O-15F9 AUDIT ADDITIONS — 2026-09-09

- RAPTOR·BPM 두 계열의 후반2106조건을 조건부 감사 근거로 보존한다. 두 수축 지표의 후반12승 방향과 원BPM의 Minnesota 극하방 꼬리는 실제 승수·라이벌 능력 승인이 아니다.
- 새 BPM 보관본은3/25까지 관측 범위로 검증했다. 원래3/24 cutoff prior와 구분하며 마감일 당시 협상 정보로 사용하지 않는다. 무표본 선수의 리그 범위 stress도 개인 prior가 아니다.
- 전반 Porter rating을 후반과 같은 전 팀 RAPTOR로 정렬했다. 전반 양 팀1144행에서10팀18경기의 상대 변화가 남음을 특정했다. 과거19~21승과 새 상대 고정 진단을 평균해 exact 기록으로 선택하지 않는다.
- O-15F9 비교 범위 종료. 다음 O-15F10 전반 상대18경기 조건부 입력과72경기 연결이다. 같은 후반 분·민감도 감사를 새 입력 없이 반복하지 않는다.
- v0.30 PARTIAL·설계/원고 CLOSED·manuscript_allowed false 유지. 상세 권위: `simulation/CHICAGO_2020_21_IMPACT_CROSSCHECK.md`.


## v0.30 O-15F10 AUDIT ADDITIONS — 2026-09-09

- 전반43경기와 후반29경기를 연결한 기준선 진단을 보존한다. 10팀18경기는 선수 초 1:1 교체 벡터로 만들고, 나머지25경기는 제한적 기준선 후보로 남긴다.
- Minnesota·Denver 연장전의 실제 팀 총초를 보존한다. 48분 절삭이나 0분 선수의 가용성 발명은 없다.
- RAPTOR RS EB와 BPM 3/25 EB의 72경기 산술값은 조건부 진단이며 정본 시즌 승수·순위가 아니다. 전반·후반 경로는 `selected=false`다.
- 다음 O-15F11은 Portland·Golden State 전반 접전부터 상대 분 조합을 선택한다. 프로젝트는 v0.30 PARTIAL, 설계/원고 CLOSED·manuscript_allowed false를 유지한다.


## v0.30 O-15F11 AUDIT ADDITIONS — 2026-09-09

- O-15F10의 기준선 수치 판정은 정정한다. 전반 상대 상수 혼입·계열별 prior 누락·전반 피로·본문 표 오류를 교정했다. 기존 BASE31–41을 확정 기록이나 현행 연결값으로 사용하지 않는다.
- 전반18접촉은10개 교체 벡터·8개 미배정 경로였음을 정정한다. GSW와LAL처럼 제거 선수 없는 경로도 기준선 자동 확정 대상이 아니다.
- Portland·Golden State3경기11안·198조건의 분·5인 조합·양 팀 점수차 계산을 완료했다. 기존 선수 분담/POR·Hutchison 비활성/GSW는 작업 추천이며 실제 사건 승인이 아니다.
- BASE 추천안에서1/5 Portland는 두 지표 양수, GSW·1/30 Portland는 지표 부호가 달라 미정으로 남긴다. Evans는 지표별 동일 계수로 두 날짜를 연결한다. 미지 계수를0으로 대체하거나 계열 평균으로 승패를 고르지 않는다.
- 다음 O-15F12는 나머지15전반 접촉·라이벌·시즌 조건 연결. v0.30 PARTIAL·설계/원고 CLOSED·manuscript_allowed false 유지.


## v0.30 O-15F12 AUDIT ADDITIONS — 2026-09-10

- 잔여15전반 접촉29개 분 배정안·522개 조건 검산으로 전반18접촉의 조건부 분 입력을 완료했다. 실제 신규등록·가용성·계약 선택과 분 증명을 구분한다.
- 전반43+후반29의6개조건부 경로·216개 시즌 조건을 연결했다. 라이벌은 지표별 동일 유효rating으로 두 날짜를 계산하며 능력 prior를 확정하지 않는다.
- BASE 중심 후보는31~33승에 해당하며 GSW·Portland 두 접전의 지표 불일치를 유지한다. 최종 승패·순위·플레이인·픽을 선택한 것이 아니다.
- Fournier Boston미합류안은 Orlando 잔류/새행선지 미계산 때문에 통합에서 제외한다. 나머지 공통 거래·가용성도 명시된 조건이다.
- Chicago 승수 변화와 상대 변화는 합계0으로 보존했다. Chicago 외 경기의 리그전체 파급은 별도다.
- 다음 O-15F13 시즌 결산·순위·픽 보드. 같은 분 감사를 새 입력 없이 반복하지 않는다. v0.30 PARTIAL·설계/원고 CLOSED·manuscript_allowed false 유지.


## 2026-09-10 O-15F13 조건부 시즌 결산·순위·픽 감사

- 권위: `simulation/CHICAGO_2020_21_STANDINGS_PICK_BOARD.md` 및 동명JSON; 총괄 검토 `reviews/R01_O15F13_STANDINGS_PICK_REVIEW.md` (`NOT_INDEPENDENT`).
- 공개 편집 정규경기1080개 기준선과 Chicago72경기 대조,BASE72조건의31/32/33승 후보·상대 승수 이전 검산 완료. 다른1008경기 실제유지 진단이며 대체 리그 정본이 아니다.
- 조건부동부11/11/10위,CHI-CHA3승0패.33승은RAPTOR피로0만이며 접전 지표 불일치·최종시즌 미선택 유지.
- POR/LAL/GSW의 서부 경계를 재개방. 자체2021/2023첫픽 보유와 성적순서·추첨결과를 분리한다. 드래프트동률에포스트시즌H2H를 사용하지 않는다.2021정확조합원문 미확보로 odds/추첨 HOLD.
- 다음O-15F14는 리그 경계 파급·시즌 선택 선행 조건 회수. 매작업종료 전체7행 체크표·남은6매크로 표시.
- v0.30 PARTIAL·DESIGN_GATE CLOSED·manuscript_allowed false 유지. 원고 미작성.
