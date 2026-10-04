# Denver–Cleveland 2020–21 — 전체 기간 등록 증인

기준 main `a7238c6c4d58a88d5f8cd7f6713fa1876eec8f9e` / PR #414. [생성기](../tools/build_den_cle_registration_domain.py)와 [실명 명단·사건 JSON](DEN_CLE_REGISTRATION_LEGAL_DOMAIN_2026_10_05.json)은 2021-03-25~05-16의 각 팀 53일을 생성한다. Denver의 Clark 해제일은 두 분기를 유지한다. 독립 검수 완료 후 해당 등록 필드만 LEGAL_BOUND_PASS로 판정했다.

## 사실·추론·후보·작가확정

| 등급 | 적용 |
|---|---|
| 사실 | 고정 NBA 공식 feed의 DEN7그룹/13행·CLE9그룹/11행, 공유 거래를 합친 고유15그룹/21행. DEN 구단 가이드 전체 거래쪽, CLE 구단 roster의 Cook·Martin 계약 이력, 거래 전 공식 경기책의 명단 |
| 추론 | 공표한 10일 시작일과 CBA 기간 규칙·기존 팀 일정으로 만료일 계산; 정원을 만족하는 등록 배치 존재 |
| 후보 | 공표 계약/방출 사건의 대체세계 이월과 적법한 당일 순서. 실제 계약 선택·건강·접수 시각 미인증 |
| 작가확정 | 기존 McGee/Hartenstein 거래 생략·Varejão 두 5월 계약 생략·T1 및 드래프트 치환만 재사용. 새 확정0 |

## 원자료와 날짜 충돌

- [NBA movement 원자료](https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json)의 9,927행 고정 스냅샷에서 두 팀 관련 모든 그룹을 추출한다. SHA `3d9d7a6dd7ccd39ddfdd1799a26ef9901b44682d85a26f05239b468a8ae92e3a`. 원본 행은 JSON에 저장하며 정의한 공개 목록 밖 모든 미공표 사건 부재를 주장하지 않는다.
- [Denver 공식 2021–22 가이드](https://kseblobstorage.blob.core.windows.net/sitefiles/pdf/DN_MediaGuide_2122_Digital.pdf) 인쇄279/PDF281의 해당 시즌 전체 거래 목록을 직접 읽었다. Clark 해제는 **guide4/9 vs feed4/8**이며 두 분기 모두 보존한다. TW 교체와 Rivers 두 계약도 대조했다.
- [Cleveland 공식 2022–23 roster PDF](https://cdn.nba.com/teams/uploads/sites/1610612739/2022/10/08-roster.pdf)의 Cook 인쇄172/PDF12·Martin 인쇄201/PDF41을 직접 읽었다. Cook3/12·3/22의 두 10일 계약과 Martin4/28 TW가 feed와 일치한다. CLE 별도 가이드의 전수 거래쪽은 미회수이며 전수 목록은 고정 feed에 근거한다.
- [CLE3/24 공식 경기책](https://statsdmz.nba.com/pdfs/20210324/20210324_CLECHI_book.pdf)의 박스12+inactive5=17, 기존 TW Thomas/Stevens를 제외한 일반15를 재대조했다. [DEN3/24 공식 경기책](https://statsdmz.nba.com/pdfs/20210324/20210324_DENTOR_book.pdf)은 웹 PDF 본문에서 박스14+inactive3=17을 직접 확인했다. 로컬 요청은 timeout이어서 DEN 경기책 원본 지문은 미회수다.

Stevens4/14와 Kabengele5/1의 feed ROS 표기와 기존 구단 발표 multi-year 표기는 서로 합치지 않는다. 어느 기간 표기든 당해 시즌 일반계약1자리라는 공통 범위만 사용한다. Varejão5/14 계약 형식의 원역사 충돌도 남기며 기존 C2 경로는 두 5월 계약을 모두 생략하므로 해당 형식을 임의 확정하지 않는다.

## 승인 경로와 날짜별 명단

DEN 원역사 #22 Nnaji/#24 Hampton 자리는 기존 승인 #22 **Saddiq Bey**/#24 Nnaji로 연결한다. 유효한 첫 rookie-scale 계약이라는 법적 범위에서 둘 다 일반계약이다. T1은 Harris·Nnaji→Gordon·Clark, McGee 거래는 생략하여 Hartenstein DEN/McGee CLE가 유지된다. C2는 Varejão의 5/4·14 계약을 생략한다.

| 팀 | 구간 | 일반 | TW |
|---|---|---:|---:|
| DEN | 3/25–4/7 | 15 | 2 |
| DEN | 4/8 | Clark 분기별14/15 | 2 |
| DEN | 4/9–4/19 | 14 | 2 |
| DEN | 4/20–5/16 | 15 | 2 |
| CLE | 3/25 | 15 | 2 |
| CLE | 3/26–3/31 | 14 | 2 |
| CLE | 4/1–4/9 | 13 | 2 |
| CLE | 4/10–4/13 | 14 | 2 |
| CLE | 4/14–4/19 | 15 | 1 |
| CLE | 4/20 | 14 | 1 |
| CLE | 4/21–4/27 | 15 | 1 |
| CLE | 4/28–5/16 | 15 | 2 |

Cook 첫 계약도 창 밖 선행 증거에 포함한다. CBA II§9(a)의 `10일 또는3경기 중 긴 기간`으로 계산한 만료는 Cook3/12–21·3/22–31, Kabengele4/10–19·4/21–30, Rivers4/20–29다. 각 기간 세 번째 경기보다 10일이 길거나 같고, 시즌 종료 전에 종료된다. **3/31은 원문에 직접 적힌 방출일이 아니라 기간/일정 파생값**이다. Kabengele4/20 공백, Rivers4/30·Kabengele5/1 만료 뒤 새 일반계약을 별도 사건으로 처리한다.

## 일반13명 임시 예외의 배치 증명

[공식 2017 CBA](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf) XXIX§1–2, 인쇄390/PDF412와 [2019 NBA 규약](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf) §6.02–6.03, 인쇄69/PDF78을 직접 읽었다. 일반13명 자동통과가 아니라 **활동12+비활동1**의 최대2주 연속 임시 예외를 적용한다. 해당 두 원문에는 누적28일 조건이 없으며 후대 규정을 2021로 소급하지 않는다.

4/1–9의9일에 가능한 구성은 일반 active12+일반 inactive1+TW inactive2다. 비활동 최소도 임시1+TW2=3, 구성값3이므로 TW 보정을 충족한다. 일반14/15명에는 일반 active12+일반 inactive2/3와 해당 TW 비활동 인원을 연결한다. **배치 가능성을 증명한 것이며 실제 경기 활성 명단·8명 건강·TW 서비스 자격을 인증한 것은 아니다.** 유효 계약·적법한 급여/자격·TW 서비스 자격의 법적 범위 전제를 유지하며 실제 활동 실행은 A1/K의 별도 증인이다.

## 검수 범위

공개 source ID와 기존 승인 변환을 직접 재실행하고 해제/만료→서명, Stevens TW 종료→일반, 후속 계약의 중복 자리 없음을 검문한다. 현재 음성4종은 전환 누락·Harrison 잘못된 계약 종류·Cook 만료 계약을 후속 서명까지 유지·13명 상태2주 초과를 거부한다. 출력 수정/날짜 누락은 `--check`의 전체 재현 대조로 거부한다.

`DEN_all_dates / CLE_all_dates / prior_and_followup_contracts`를 실제 코드/JSON 독립 재검수와 원장 검사로 통과시켰다. 다른10법적HOLD·F0/5·A0/3·K0/4를 보존한다. 전체 비용·매칭/픽·건강/분·실제 계약 선택/접수·F5 전체·시즌은 별도 HOLD다. freeze v0.30 PARTIAL·설계/원고 CLOSED·원고0·미완료 큰묶음6.

```powershell
C:/Python314/python.exe -B -X utf8 tools/build_den_cle_registration_domain.py --cache-dir 'C:/Users/Storm Credit/AppData/Local/Temp' --check --self-test
```
