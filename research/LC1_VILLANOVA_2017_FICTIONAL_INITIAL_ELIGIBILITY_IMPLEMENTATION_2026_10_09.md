# Villanova 2017 가상 초기 자격 구현 — 2026-10-09

상태: **구체 가상 qualifying family 선택 / 독립 검문 대기**. 실제 개인 성적표·SAT 결과·Eligibility Center 인증을 뜻하지 않는다.

## 기존 결함과 유지 범위

원 `COLLEGE_EXIT_PACKET.md`의 영어 후보 2.0+1.0–1.5=3.0–3.5는 당시 영어4 요건에 미달한다. 과거 원본과 PASS 문구는 수정하지 않았다. 새 후행 구현은 한국4학기+미국프렙3학기, 2016년3월 전학, 2017년5–6월 졸업, Villanova 늦은 오퍼/입학 방향과 기존 SAT1280–1320 범위를 유지한다.

## 16개 고유 핵심 단위

| ID | 범주 | 학교/과목 범주 | 이수 학기 | 단위 | 가상4점 성적 |
|---|---|---|---|---:|---:|
| K-E1 | English | academicEnglishreading/composition I;distinctgrade9core-equivalent | 1,2 | 1 | 2 |
| K-E2 | English | academicEnglishreading/composition II;distinctgrade10core-equivalent | 3,4 | 1 | 2 |
| K-M1 | Mathematics | algebraI-or-higher course I, grade9equivalent | 1,2 | 1 | 2 |
| K-M2 | Mathematics | geometry/algebraI-or-higher course II, distinctgrade10content | 3,4 | 1 | 2 |
| K-S1 | NaturalPhysicalScience | physicalscience, collegeprepgrade9equivalent | 1,2 | 1 | 2 |
| K-S2 | AdditionalEMS | biology, distinctgrade10collegeprepscience | 3,4 | 1 | 2 |
| K-H1 | SocialScience | worldhistory/geography course I, grade9equivalent | 1,2 | 1 | 2 |
| K-H2 | SocialScience | Koreanhistory/socialstudies course II, distinctgrade10content | 3,4 | 1 | 2 |
| K-L1 | AdditionalAcademic | Koreanacademiclanguage/literature I, recognizednon-Englishlanguagecorearea | 1,2 | 1 | 3 |
| K-L2 | AdditionalAcademic | Koreanacademiclanguage/literature II, distinctadvancedcontent | 3,4 | 1 | 3 |
| US-E3 | English | regularcollegeprep composition/rhetoric A+B, not remedialorbasicESL | 5,6 | 1 | 3 |
| US-E4 | English | regularcollegeprep literature/analyticalwriting A+B, distinctcontentconcurrentFallwithUS-E3 | 6,7 | 1 | 3 |
| US-M3 | Mathematics | algebraII A+B, not repeatofK-M1orK-M2 | 5,6 | 1 | 3 |
| US-S3 | NaturalPhysicalScience | chemistrywithlaboratory A+B, distinctfromKphysicalscienceandbiology | 5,6 | 1 | 3 |
| US-H3 | AdditionalAcademic | civics/government A+B, distinctfromKworld/Koreanhistory | 6,7 | 1 | 3 |
| US-L3 | AdditionalAcademic | Spanish I A+B, newforeignlanguagecourse | 5,6 | 1 | 3 |

범주 합계: **영어4·수학3·자연/물리과학2·추가 E/M/S1·사회2·추가 핵심4=16**. 한국10+미국6. 과학 필수2의 하나는 US-S3 실험 화학이다. 생물 K-S2는 추가 E/M/S1로 한 번만 계산한다. 한국어·문학의 두 단위는 추가 핵심이며 영어4에 재사용하지 않는다.

한국 영어 과목을 영어 핵심 범주, 한국어·문학을 추가 비영어 언어 범주로 인정하는 것은 이 **가상 기관의 qualifying family 명시 조건**이다. 한국 과목명만으로 실제 NCAA 환산을 인증하지 않는다. 미국 영어 두 과목은 다른 정규 college-prep 내용이며 기초 ESL·보충 출석·같은 과목 재이수로 단위를 만들지 않는다.

## 7학기 시계와 10/7

| 학기 | 범위 | 핵심 단위 |
|---:|---|---:|
| 1 | 2014.03–2014summer | 2.5 |
| 2 | 2014lateAugust–2015.02 | 2.5 |
| 3 | 2015.03–2015summer | 2.5 |
| 4 | 2015lateAugust–2016.02 | 2.5 |
| 5 | 2016.03transfer→2016springtermend | 2 |
| 6 | 2016fall→before2017springtermstart | 3 |
| 7 | 2017spring→MayJunegraduationwindow | 1 |

미국 첫 봄은3월 중도 편입 이후 승인된 수업·평가로 반단위 내용을 끝내는 가족이다. 편입 전1–2월 결석 시간을 이수로 계산하거나 숨은8번째 학기를 추가하지 않는다. 여름 핵심 단위는0이며 마지막 학기 뒤 여름 과목으로10/7을 복구하지 않는다. 필수 농구시간을 임의 취소하는 대신 기존 의무 study hall·튜터링이 추가 개인훈련/게임 시간을 줄이는 비용을 유지한다.

6학기 끝, 7학기 시작 전 고정10: **K-E1, K-E2, US-E3, K-M1, K-M2, US-M3, K-S1, K-H1, K-H2, K-L1**. 그중 영어·수학·과학7은 K-E1, K-E2, US-E3, K-M1, K-M2, US-M3, K-S1. 고정10의 성적은 23/10=2.300이며 마지막 학기 성적으로 교체하지 않는다. 6학기까지 전체 인정 단위15, 온전한1단위 과정14개를 마쳤고 마지막 두 반단위로16을 채운다. 전부 국제 학적10/7 예외는 사용하지 않는다.

## GPA·당시 시험 index

- 한국 후보10단위의 quality points22 + 미국6단위18 = **40/16=2.500**. C8단위/B8단위, A·honors 가산0. 실제 한국 성적의 환산 결과가 아니라 낮은 과거 성적과 이후 학습 비용을 보존하는 구체 가상 입력이다.
- 2017–18 공식 manual printed165(PDF zero-index176)의 qualifier row에서 **GPA2.500 → oldSAT820 또는 ACT sum68**을 직접 읽었다. ACT는 composite68이라는 뜻이 아니며 P의 ACT 응시를 추가하지 않는다.
- 같은 판 Figure14-3 printed194(PDF zero-index205)에서 **newSAT900 → oldSAT820**을 직접 확인했다. 기존 선택 newSAT1280–1320은 그 최소900을 모두 넘는다. 실제 한 점수나1280의 exact oldSAT 환산값은 선택하지 않는다.
- 2016가을 또는2017봄의 공개 national SAT 시험일을 쓰는 조건부 시계이며, 정확 일자는 미배정이다. 대학 전일제 등록/수업 참석 전에 시험을 끝낸다. campus residual/regional시험, 구 SAT와 신 SAT section 혼합, essay 가산은 없다.

[당시 NCAA 공식 manual](https://ncaa.soutronglobal.net/Public/Default/en-US/DownloadImageFile.ashx?objectId=3865&ownerId=9176&ownerType=0)의 공개 요건을 이 가족에 적용한 것이다. 기존7행 source 검수는 당시 규칙의 근거 수락이며, 이번에 직접 읽은 GPA/index/concordance와 구체16단위 적용에 대한 독립 검문은 별도다.

## 기관·인물 접근과 남은 범위

I1 늦은 봄 오퍼/입학 안내 → I2 5–6월 졸업·최종 성적표 제출 안내 → I3 여름 EC academic/amateurism·Villanova compliance 완료 통지 → I4 등록/공식 출전의 기존 순서를 보존한다. 학교의 졸업에는 NCAA16 이외 원래 의무도 남으며16을 학교 전체 졸업 학점이라고 주장하지 않는다. GPA·시험이 입학처 판단·amateurism·13counter·주전 권한을 대신하지 않는다.

인물은 당시 자신의 공부와 실제 받은 안내만 안다. 이 새 설계 수치가 과거 학습·오퍼 장면의 선행 지식으로 들어가지 않는다. 실제 개인 문서·NLI·의료 인증을 새 완료 게이트로 요구하지 않는다. 새 사건/원고0, 원111/현재54/중앙 파일 수정0, 실제Pack0, 전체G08/선택역사LOCK/G13/G14 false, v0.30 PARTIAL/CLOSED.

생산자 검산: 16고유ID·6범주·7학기 합계·first10/EMS7·고정성적 보존·GPA2.500·실제 당시index/concordance 확인 PASS. **가상 학업 적용의 독립 검문은 대기**.
