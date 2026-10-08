# 2023 public residual model candidates

- Status: `TWO_FICTIONAL_RESIDUAL_CANDIDATES_COMPUTED_PENDING_ROOT_SELECTION_AND_INDEPENDENT_REVIEW`
- JSON LF SHA256: `704b23773a53d8b27cfae9191a907fd9f891e986bc5ab2a44e360f27920c0d52`
- 2案 모두 CANDIDATE. 잔차법 채택·시즌승수·정확대진·MVP·우승은 총괄의 후행수락 전이다.

## 직접 읽은 공식 원자료

NBA Stats LeagueGameLog2022–23 팀단위 response를 repo상대 `Temp/fr-threepeat-2023-public-variance/leaguegamelog-response.bin`에서 직접 읽었다. RAW SHA `391862ab046a01dcdb399075f8616b3364a6ceb86559adf473f77d2830a635d1` /390234bytes, HTTP200 수집metadata. 새취득0. 원retrieval.json의 actual_residual_executed:false는 수집당시표시로 보존했다.

[공식 NBA Stats 요청](https://stats.nba.com/stats/leaguegamelog?Counter=0&DateFrom=&DateTo=&Direction=DESC&LeagueID=00&PlayerOrTeam=T&Season=2022-23&SeasonType=Regular%20Season&Sorter=DATE)

2460팀행을1230경기쌍으로 조인했다. 각쌍의 날짜/MIN같음·점수차반대·PTS차와PLUS_MINUS같음·1승1패를검산했다. 실제CHI40–42/82경기:75경기는양팀MIN240,7경기는265/290. 리그전체 정규시간1151/연장79경기다. 실제NPC기록은 FACT reference이며 대체세계NPC승수로 복구하지 않는다. 개인stat/부상/private의도는 추출·선택하지 않는다.

## reference expected margin과 중심화

모든79연장경기는 팀평균·home추정·잔차pool에서 제외한다. 연장최종점수는48분점수차가 아니며 새0OT경기점수로 복사하지 않는다.

1. `mu[t] = 실제MIN240 팀경기의 PLUS_MINUS 평균`.
2. `h_ref = 1151 formalhome regulation게임에서 (실제home점수차 − mu[home] + mu[away]) 평균`.
3. `refExpectedCHI = mu[CHI] − mu[opp] ± h_ref`.
4. `rawResidual = actualCHIregMargin − refExpectedCHI`.
5. CHI75행rawResidual의 평균을빼 centeredResidual75합을정확0으로한다.

CHI정규시간mean=`112/75`≈1.493333, h_ref≈2.595700386, 제거한CHI잔차평균≈-0.176845827, centered잔차populationSD≈14.419778976. 정확fraction·30팀각reg게임수·sum/mean·raw행포인터는 JSON에있다.

이 값은 retrospective서술통계다. formalhome은MATCHUPvs표시이고 실제지리적홈효과의인과추정이아니다. 중립/해외경기·실제로스터/건강/거래/전술/상대대응/측정오차도잔차에남을수있다. 이를 새세계의같은날disturbance로수입하는가정은 FACT가아니다. 선수의미래일정결과사전지식으로쓰지않는다.

## 두 가상안의 시산

새3phaseCHIproxy−원상대proxy±원homeeffect+B2B차/2에 centeredResidual을더한다. 잔차1NBAreferencepoint→1modelmarginunit은별도명시가상스케일가정이다. 새홈효과와referenceh_ref를중복더하지않고 원상대rating·원home2/중립0·B2Bhalf를유지한다.

| 안 | 정규시간75 잔차 | 실제OT참조7 처리 | CHI | 동부 | 조건부R1 | 원1R슬롯 |
|---|---|---|---|---:|---|---:|
| A_NEUTRAL_OT | 같은날centered75 | 잔차0 | 55–27 | 5 | BOS | 21 |
| B_EMPIRICAL_OT | 같은날centered75 | 고정hash 경험pool7draw | 52–30 | 6 | PHI | 20 |

두안의75경기승수는같이48승이다. 두안의차이는7OT참조경기에사용한잔차처리뿐이다. A는7승/B는4승을얻는다. 원하는58승에맞춰계수·잔차scale·seed·pool을조정하지않았다. 같은성장입력의zero-variance79–3은진단만이며 세번째후보안이나시즌채택이아니다.

A안은알수없는연장day잔차를0으로놓는단순가정이다. 실제연장경기의정규시간마진0을새경기의사실로대체했다는주장이아니다. 다만강해진CHI가모두이겨 missingvariance가승수에는유리하게작동한다.

B안은regulation75centeredpool에서7회withreplacementdraw한다. pool은GAME_DATE/GAME_ID순. `FR_THREEPEAT_2023_OT_EMPIRICAL_V1|rawSHA|targetGAME_ID`의 SHA256첫8bytesbigendian정수 mod75가index다. seed1개만사용했으며 결과를본뒤거부/재추출하지않았다. pool평균0과7실현draw평균0은다르며 후자의재중심화0. 모든7draw의key/hash/index/원reggame/residual은JSON에서재현가능하다.

권고는B다. 이유는알수없는7OT일에도변동성을남기는범위이고, 원하는승수·대진때문이아니다. regulation일의무조건부분포가closeOT일을대표한다는것은추가가정이다. hashdraw는가상한실현이며 실제OT예측·독립무작위과정·정확counterfactual식별인증이아니다. 권고≠선택.

## paired승패·30순위·권리 영향

- 원1148 nonCHI경기는baseline /rows 포인터로재사용하고새JSON에복사하지않았다. CHI82의승자가바뀌면같은경기상대의패자도바뀐다. 두안각30팀82GP,리그1230승/1230패,paireddelta합0을재계산했다.
- 기존순위함수의head-to-head/디비전/컨퍼런스/eligibleworkingcriteria/restart로30seed를재계산했다. 원규칙근거한계는유지하고새2023원문을취득했다고하지않는다. 이번두안에서는point-differentialHOLD가발생하지않았다. 모델잔차마진을실제득실점으로써tie를억지해소하지않는다.
- CHI는각E5/E6로플레이인없이직행한다. 조건부BOS4/PHI3R1이고상대homecourt. 아직series날짜/득점/우승·playin승자선택0. 다른1148의NPCzero-variance가그대로이므로30기록은기계적일관성검산이지리그전체현실성PASS가아니다.
- 실제cached2019Bylaws PDF86/printed77의7.02(a)(iii),(b),(c)를다시읽어역순·drafttie추첨규칙을확인했다. 모든CHI보다승수가높은팀은각conference상위6에포함되므로다른playin승자가CHI원픽의상대위치를바꾸지않는다. CHI동률팀0. A/B의1R원픽21/20이며unadjusted2R전체origin51/50(라운드내21/20)이다. 2RholderWAS를유지하며forfeiture삭제뒤최종지명번호로인증하지않는다.
- 옛CHI16/Jaquez15earlier-availabilitywitness는새20/21의근거가아니다. 이전선수선택·픽권리/새scale를연결해야한다. 실제Miami18픽을편의상복원하여Jaquez가반드시앞에서나간다고도하지않는다. 새트레이드/권리/루키선택0.

## 경계와 검산

FACT원점수/기록과REFERENCE_ESTIMATE와CANDIDATE잔차수입을명시분리했다. 새가상점수null/개인statnull/부상null/모델OT0. 원점수→0OT복사0. 정규시간75잔차sum0,82date/home/awayuniquejoin,pairedwins,3phase36/41/5,두30순위/원픽방향을자체검산했다. 독립PASS·root채택은아니다.

원생성기/자료/중앙/Git편집0. 새primary수집0. 전82개인박스·새사적증명·전1230원문취득게이트0. C01공적메달/병역미선택,actualBlueprint/G13/G14/wholeLOCKfalse,Pack0/원고0/CLOSED.

## 프로젝트 진행

| 그룹 | 상태 |
|---|---|
| 1 | 완료 이력·2015–18 접근/대학/드래프트 보존 |
| 2 | 완료 이력·2018–21 팀/역할/가격/실패 보존 |
| 3 | 기존 완료 이력 보존·2022PHI패/고정계약 유지;2023성장/결과 사용점 수리 진행 |
| 4 | 2023–25 목표 선택·성장/역할 입력 생산;순위/대진/수상 실행 전 |
| 5 | 2025짧은 본편 기능 배치·새N 미산정 |
| 6 | 독서110/110 보존·새Blueprint/집필규격 검증 전·Pack0 |
| 7 | 통합·독립검수·최종승인 미완료 |

미완료4개/6번까지3개.
