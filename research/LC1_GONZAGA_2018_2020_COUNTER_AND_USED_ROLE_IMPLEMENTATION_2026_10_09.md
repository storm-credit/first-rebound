# Gonzaga2018–2020: counter와 사용 역할의 유한 구현

- 상태: 생산자 작성·검산 완료 / 독립 검문 대기.
- 승인 학교·0경기 레드셔츠·WCC 두 우승·NCAA 취소 방향을 소비한다. 실제 개인 성적표·장학 원장·임상 인증이 아니다.
- 전체33경기·시즌31–2/15–1·개인 시즌 합계는 이 두 대표 경기로 확정하지 않는다.

## 공식 자료와 가상 조건

공식2018 명단15명과2019 명단13명을 직접 회수했다. [2018 Quick Facts](https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/gozags.com/documents/2018/10/8/Quick_Facts.pdf)는 Lang·Pennington을 walk-on으로 명시한다. 공개 명단과 이 표현만으로 비공개 지급 원장을 복원하지 않는다. 각 counter의 가상 입력은 JSON 이름별 행에 명시했다.

[2018–19 규정](https://iuhoosiers.com/documents/download/2018/9/28/2018_19_NCAA_D1_Manual.pdf)의15.5.1(a)/15.5.5.1과 [2019–20 NCAA 원문](https://ncaa.soutronglobal.net/Public/Default/en-US/DownloadImageFile.ashx?objectId=4036&ownerType=0&ownerId=9184)의 같은 조항을 각각 읽었다. 2019판은452쪽이며 printed213/219에 해당한다. 운동능력에 따른 aid는0경기에도 counter다. 정원13은 공개 로스터 인원 한도가 아니다.

|학년도|공개 명단|가상 명단(라이벌 추가)|counter|비counter 가상 입력|
|---|---:|---:|---:|---|
|2018–19|15|16|13|Lang·Pennington·Alex Martin: countable aid 없음|
|2019–20|13|14|13|Will Graves: countable aid 없음; Lang은 봄 aid 수령시 연간1회 산입|

Alex Martin·Graves의 aid 분류와 나머지 이름별 aid는 명시 가상 합법 가족이며 실제 장학 여부를 단정하지 않는다. 실제 기존 aid 취소·기부금 우회·부상 면제·14번째 counter를 만들지 않았다.

## 레드셔츠와 복귀

T0는2018가을 정규학기 최소 전일제 등록과 첫 수업이 함께 성립한 때다. 실제 학사일을 임의 고정하지 않는다. 5년 시계는T0에 시작하고0경기 첫해도 흐른다. 2018–19 intercollegiate 경기0 / competition season0, 2019–20 참여로 first competition season1이다. 축구4경기 예외·medical hardship·2020취소에 따른 자동 환급을 쓰지 않았다.

원 ACL 방향과 누적 full-contact/반복 피벗 허용 조건을 유지한다. 초기25–29분, 후기29–32분 범위와 경기 뒤 반응·급정지 부담을 유지하며 재부상·임상수치·새 사적 증명 gate는 없다.

## 두 대표 경기와 실제 밀려나는 기회

### 2019-11-28 C03-OREGON

[공식 원역사 박스](https://gozags.com/sports/mens-basketball/stats/2019/oregon/boxscore/7261) / 선택 가상 점수 73–72. 같은 점수는 이 사용창의 설계 선택이고 변화가 없다는 실제 인과 인증이 아니다.

|선수|원분→선택분|원FGA→선택FGA|원득점→선택득점|
|---|---:|---:|---:|
|Petrusev, Filip|40→40|15→15|22→22|
|Kispert, Corey|42→39|12→10|17→13|
|Tillie, Killian|27→27|11→11|7→7|
|Woolridge, Ryan|41→30|7→4|5→3|
|Gilder, Admon|21→12|5→2|2→2|
|Ayayi, Joel|31→26|8→6|13→8|
|Timme, Drew|23→23|4→4|7→7|
|Fictional Rival|0→28|0→10|0→11|

Gilder loses his starting slot and9minutes, Woolridge11minutes and10 modeled first-action calls; Ayayi5minutes/2 calls, Kispert3minutes/2 calls. Petrusev’s40minutes and22points survive. Rival11points/3turnovers with2of3FT is an imperfect early return, not an invulnerable solo win.

Selected narrow overtime win retains interior scoring and Kispert/Ayayi outside makes. Rival’s early creation uses10 donor FG attempts; the option to reset through Woolridge/Petrusev is retained instead of attempting every closing attack. Team still needs Petrusev22, Kispert13, Ayayi8, Timme7 and Tillie7; Oregon retains72points and Pritchard/Duarte substantial attempts. Same final score is an explicit bounded fictional endpoint, not a forecast or actual no-butterfly-effect proof.

초기 half-court first-action 모델 총량 56를 유지한다. 실제 광학 touches/전체 possession 통계가 아니다. 라이벌 새 calls는 이름별 donor에서 이동한다. 선택 TO3도 비용으로 남으며 선택 전체 리바운드·파울·PBP를 인증하지 않는다.

### 2020-03-10 C03-SMC

[공식 원역사 박스](https://gozags.com/sports/mens-basketball/stats/2019-20/3-seed-saint-mary-s/boxscore/7495) / 선택 가상 점수 84–66. 같은 점수는 이 사용창의 설계 선택이고 변화가 없다는 실제 인과 인증이 아니다.

|선수|원분→선택분|원FGA→선택FGA|원득점→선택득점|
|---|---:|---:|---:|
|Ayayi, Joel|36→29|13→10|17→12|
|Kispert, Corey|37→33|11→9|12→11|
|Petrusev, Filip|25→25|5→5|10→10|
|Tillie, Killian|21→21|7→7|9→9|
|Woolridge, Ryan|25→15|4→2|4→2|
|Timme, Drew|26→26|8→8|17→17|
|Gilder, Admon|25→15|10→6|15→10|
|Arlauskas, Martynas|2→2|0→0|0→0|
|Zakharov, Pavel|1→1|0→0|0→0|
|Lang, Matthew|1→1|0→0|0→0|
|Graves, Will|1→1|0→0|0→0|
|Fictional Rival|0→31|0→11|0→13|

Woolridge loses his starting slot and10minutes/7 modeled first-action calls, Gilder10minutes/6 calls, Ayayi7minutes/5 calls, Kispert4minutes/4 calls. Ayayi remains starter, Kispert33minutes. Rival largest individual initiation allocation22/60 does not eliminate other creators. Timme17points/26minutes and Petrusev10points/25minutes survive; rebound and short-roll duties remain independent.

Selected WCC tournament-title win keeps the interior pair’s11of13FG and secondary guards’ scoring. Rival11FG attempts are taken from named perimeter donors, not added atop their attempts;13points remains below Timme17. Saint Mary’s retains66points including Ford27 and Fitts17. Same historical score is selected only in this used window; season31–2 and15–1 are not thereby selected.

초기 half-court first-action 모델 총량 60를 유지한다. 실제 광학 touches/전체 possession 통계가 아니다. 라이벌 새 calls는 이름별 donor에서 이동한다. 선택 TO2도 비용으로 남으며 선택 전체 리바운드·파울·PBP를 인증하지 않는다.

## 관계·정보 경계

깊은 대학 관계는 Ayayi/Kispert/Petrusev3명만이다. Ayayi의 연결/재공급, Kispert의 준비된 외곽 공간, Petrusev의 post/short-roll 결정권을 보존했다. 다른 실존 선수는 공개 농구 배경이다. 현실 인물의 사생활·심리·실제 발언을 만들지 않았다. P는 경기 이후 공개 정보나 명시 전달만 알 수 있으며 라이벌의 사적 aid/재활 notice를 전지적으로 알지 못한다.

[NCAA Board2020-03-12 회의록](https://ncaaorg.s3.amazonaws.com/committees/d2/mc_mgmt/Apr2020D2MC_Agenda.pdf)의PDF zero40/item5에서 취소를 직접 확인했다. WCC 두 우승은 기존 선택이고 NCAA 전국우승은 없다. 취소가2020드래프트1순위의 자동 보증은 아니다.

## 검산·외부 도구·한계

21개 생산자 검산: 명단15/13·연간counter13/13·두 게임225+225/200+200분·득점 산식·슛 용량·donor 분/FGA·선발5명·first-action 모델 총량·소스 SHA. 독립 peer PASS를 주장하지 않는다. Antigravity/NotebookLM/Claude/source-blind는 이번 packet NOT_RUN이며 공식 직접 수집과 생산자 검산만 실행했다.

남은 일은 독립 검문과 후행 소비자 source join이다. 현재 자료로 실제 개인 EC/aid/임상 인증 또는 전체33게임 재계산을 종료요건으로 새로 요구하지 않는다. 공적2023대표팀/병역 선택은 HOLD다. 원111/54·중앙 상태·Git 수정0.

## 전체 진행7행

|번호|항목|현재 상태|
|---:|---|---|
|1|2020드래프트 연쇄|완료|
|2|Chicago2020–21|완료|
|3|2021–23거래·계약|완료|
|4|장기 커리어|승인 NBA 유한 실행 보존; 초기 경로·대표팀 종속 잔여|
|5|결말·전체 구조|54역사/14막42소막 현재 인과 준비; 전체 LOCK 잔여|
|6|집필 규격·Context Pack|111회 Blueprint 준비; actual 권한 미LOCK/Pack0|
|7|통합·독립·작가 승인|전체 최종 검수/명시 원고 승인 잔여|

**미완료 큰 묶음4개,6번까지3개.** v0.30 PARTIAL / 설계·원고 CLOSED / actualPack0·원고0·일정0.
