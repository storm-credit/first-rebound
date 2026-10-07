# NBA 2022–23 핵심 잔류 가격 가족

REVIEW_PENDING_CONSTRAINED_CORE_PRICE_FUNCTIONS_NOT_SELECTED

동결 NPC 포트폴리오의 명명된 11명에 가격 함수와 원 계약 분기를 연결했다. 새 합의·시장수락·팀 전체비용은 확정하지 않는다. 살아 있는 원 UPC/유효 옵션은 그대로 보존한다.

| 선수/팀 | 첫해 제안 구간 | 기간 | 원 만료/옵션 경계 |
|---|---:|---:|---|
| James Harden / BKN | $33,000,000–$43,279,250 | 2년 | UFA_OR_PO |
| Kyrie Irving / BKN | $36,000,000–$43,279,250 | 3년 | UFA_OR_PO |
| Miles Bridges / CHA | $25,000,000–$30,913,750 | 4년 | RFA |
| Collin Sexton / CLE | $16,000,000–$20,000,000 | 4년 | RFA |
| Jalen Brunson / DAL | $25,000,000–$30,913,750 | 4년 | UFA |
| Kawhi Leonard / LAC | $40,000,000–$43,279,250 | 4년 | UFA_AFTER_SELECTED_LAST_PO |
| Josh Hart / NOP | $12,000,000–$16,000,000 | 3년 | UFA_AFTER_SELECTED_ONE_YEAR_QO |
| Lonzo Ball / NOP | $20,000,000–$25,000,000 | 4년 | UFA_AFTER_SELECTED_ONE_YEAR_QO |
| Deandre Ayton / PHX | $28,000,000–$30,913,750 | 4년 | RFA |
| Norman Powell / TOR | $18,000,000–$22,000,000 | 4년 | UFA_AFTER_SELECTED_LAST_PO |
| Bradley Beal / WAS | $40,000,000–$43,279,250 | 5년 | UFA_OR_PO |

## 법적 반환과 경제 권고

루트가 가격 합의 가족을 채택할 수 있도록 만료 분기의 기존 minimum 함수를 동일 선수 Bird 가격으로 교체하는 반환을 제공한다. 추가 minimum UPC나 두번째 슬롯을 더하지 않는다. 추천 상단으로 전액 보호·0–8% 인상·마지막 PO 또는 옵션 없음의 합의 형태를 실제 계산한다. 91개 함수 끝점 검문은 실제 계약 91개가 아니다. 각 원 계약이 허용하는 status만 적용한다. 새 보너스 0은 명시된 합의 제안이며 원 Γ 부재증명이 아니다.
Harden/Irving/Beal의 FY22 옵션은 원 기한 내 행사 또는 적법 불행사 뒤 합의로 분리한다. Kawhi/Powell은 이미 선택된 FY21 마지막 PO, Hart/Lonzo는 선택된 1년 QO의 만료가 입력이다. 후대 다른 팀 새 UPC를 원 세계 계약으로 복사하지 않는다.
Bird는 직전 3시즌 표준계약과 I1(yy)의 허용 양도 이력을 보존하는 명명된 가족 조건이다. Harden의 HOU→BKN trade는 자격 연속성을 끊는 FA 이동이 아니다. 단순 프로파일 UnderContract를 동일 UPC/자격 증명으로 쓰지 않는다. 자격 조건을 만족하지 않으면 높은 가격 함수는 실행되지 않고 해당 EarlyBird/NonBird/min 한도만 적용한다.
II7 전체 최대는 cap25/30/35%와 prior Salary105% 중 큰 값이다. 제안 구간은 cap비율 이하의 충분부분집합이며 상위 priorSalary 분기를 0으로 지우지 않는다. 비상장 인센티브/서명·양도 보너스를 실제 0으로 인증하지 않는다.
Bridges 가격은 감도만 남긴다. root 권고는 새 UPC 없음·CHA FA/QO 권리/보류액 보존이다. [NBA 공식 2023-04-14](https://www.nba.com/news/nba-suspends-miles-bridges-for-30-games-without-pay)의 미서명/82결장 보고를 읽었으나 April 징계를 Oct 금지로 소급하지 않았다. 직접 HTTP 1회403은 원본문 채택0이고 web 본문 관측과 구분했다.
정규 hold150/190%, RSC 두번째 옵션 후250/300%, RFA QO/FRN와 apron 별도 정의를 보존한다. 새 서명은 해당 hold를 대체한다. 기존 Γ와 기타 비용은 유지하고 팀 다른 TaxTeamSalary B를 넣어 비반복/반복 tax 함수의 추가액을 계산한다. B=0이나 전체 팀 apron PASS는 선언하지 않는다.
추천 구간은 실제 공개 계약의 비교 가격과 동일팀 유지 이익을 참고한 가상 합의 제안이다. 다른 팀의 보장/PO/노트레이드 조항·후대 부상·거래는 복사하지 않았다. Bridges는 제도적 불확실성을 포함하여 합의 실행 권고에서 제외한다.

## 출처와 다음 유한 입력

- [OPTIONS](https://www.nba.com/news/2022-free-agency-options-and-qualifying-offers): raw `174da28c8f8f2fcd473eb009976c54e5c01f1b6b3275cfba6d1c32d520789971`; 본문 locator `[26, 36, 37, 79, 81, 89]`. Harden/Beal:POdeclined;Irving:POexercised;Ayton/Bridges/Sexton:RFA. Historical actions only.
- [HARDEN](https://www.nba.com/news/harden-agrees-to-2-year-68-6m-deal-with-76ers): raw `630044f9d4d8c2e9a143805efb6673bf66ec3df644da07240cfea2ba7aa3fbf9`; 본문 locator `[8]`. Reported:firstyear≈33m,declinedPO≈47.4m;2year≈68.6m.
- [BEAL](https://www.nba.com/news/bradley-beal-2022-nba-free-agency): raw `7bd6d58e2293a96b198d58c478627b669d6e1259f3765524c0d0002d63b672a5`; 본문 locator `[7, 8]`. Reported:5year≈251m;declinedPO≈36.4m.
- [BRUNSON](https://www.nba.com/news/jalen-brunson-2022-nba-free-agency): raw `b826e3f0aeb057df5d08f1ebc9093b5f302501eeffa28283a7429fe5f089812c`; 본문 locator `[2, 6]`. Reported:4year≈104m;NYKdestination is not adopted.
- [AYTON](https://www.nba.com/news/deandre-ayton-2022-nba-free-agency): raw `b650ce28ee5fca560940e6df7db4c54a40b5a16e95efa6a3013bb2fa959edad3`; 본문 locator `[3, 8]`. Reported:4year≈133m;PHXmatchedoffer is not adopted.
- [SEXTON](https://www.nba.com/news/donovan-mitchell-traded-to-cavs): raw `78656b4e4bf06352a186d9918874942aa33c1a3b6e51292c40d5090527b29240`; 본문 locator `[24]`. Reported:4year≈72m;UTAS&Tbundle is not adopted.
- [REVIEW2021](https://www.nba.com/news/2021-nba-free-agency-review): raw `c3ced7842aaf894b1d171f73559adab6ea24a11da79409cdc58d2fc0f4e570eb`; 본문 locator `[18, 20]`. Reported:Powell5year90m;Lonzo4year85m. Altered world has different2021UPCs.
- [KAWHI](https://www.nba.com/news/report-kawhi-leonard-plans-to-re-sign-with-clippers): raw `988f1189813fb5ebca6757d5ff2d28820bbdc5973f47fbaa0b1d0e51dc7ff64a`; 본문 locator `[3]`. Reported:2021new4year176m;altered world retains original2021option instead.
- [HART](https://www.nba.com/news/pelicans-sign-josh-hart-to-3-year-contract-extension): raw `1ff4e457f03fb137e0b803b44ab686625333f330bedc623dac4f02fd5f96dc3e`; 본문 locator `[8]`. Reported:3yearup-to38m/12mguaranteed;altered world2021ordinaryQO instead.
- [BRIDGES_QO](https://www.nba.com/hornets/news/charlotte-hornets-extend-qualifying-offers-to-miles-bridges-and-cody-martin): raw `b7da8c46074f8b994ec2ada25bc91355866b13ee57a818473ca50f04c1645838`; 본문 locator `[2]`. ClubannouncedQOJune28,2022;actualpublicQO is not alternate-worlddelivery.
- [BRIDGES_CONTEXT](https://www.nba.com/news/hornets-forward-miles-bridges-arrested-on-eve-of-free-agency): raw `49a9d3cf541ad51714a50074a4a8b414aae2b032d5cefc591439bffae630e939`; 본문 locator `[18]`. Preincidentmax-demandreport;unresolvedinstitutionalcontext. No alternateincident/clearance certified.
- [IRVING](https://www.nba.com/news/kyrie-irving-decides-to-exercise-37m-option-with-nets): raw `8e8dc50177520976640bc28d92cef5d0d3ec2f5d50805b0853cc80e0f4681417`; 본문 locator `[16, 19, 29]`. Reported:2022PO≈37m;opt-in is not alternate-worldchoice.
- [LONZO](https://www.nba.com/news/report-lonzo-ball-agrees-to-4-year-deal-with-chicago-bulls): raw `3f437bb31753dd7956007c4f7b9cdfbfe796181840121e8def66a589311e18c3`; 본문 locator `[12]`. Reported:4year85m;actualChicagoS&T is not adopted.
- [NBA_CAP2022_REUSED](https://pr.nba.com/nba-salary-cap-2022-23-season/): raw `2e76093cfc91b6257f18cddd25441090118f36bd8a942259fbc340438ff5e57f`; 본문 locator `NBA official June30 release opening two paragraphs`. 2022cap/tax primary release.

13개 NBA 원 HTML은 계약금액의 보도 맥락이며 사적 UPC 원문이 아니다. Hornets QO 발표는 직접 구단 발표다. OPTIONS 페이지의 오래된 Aug1 자유계약 문장은 2022 일정 근거로 채택하지 않는다. 2022 Bird 창은 reviewed LaVine calendar를 재사용한다. 원 CBA29쪽의 raw/추출 SHA를 JSON에 보존했다.

다음: 적법 expiry/decline 및 가격 합의 후보를 root가 채택하고 팀별 B_normal/B_apron/B_tax를 동일 날짜 원 Γ와 결합한다. N23/A23, 실제 notice/consent/fee, 전체 macro3/시즌/원고는 미인증이다.

| 큰 묶음 | 현행 |
|---|---|
| 1 초기 설계 | 완료 |
| 2 S2 유한시즌 | 완료·재개0 |
| 3 후속 커리어 | 진행·가격 가족 후보 |
| 4 전체 경력 | 미완료 |
| 5 기능 설계 | 현행 누적 등록기 참조·Pack0 |
| 6 설정집 | PARTIAL |
| 7 원고 | CLOSED |

미완료 큰 묶음5 / 6번까지4. v0.30 PARTIAL·CLOSED·중앙/REGISTER/선택 승격0.
