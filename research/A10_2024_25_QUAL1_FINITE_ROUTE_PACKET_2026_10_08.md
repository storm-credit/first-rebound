# A10-S3 QUAL1 — 2024–25 유한 자격 경로 비교

## 원 출구와 현재 위치

원 CP2의 A10-S3 출구는 **첫 우승창의 미완성**이다. 등록된 국소 기능은 자기 공격과 동료 기능의 공백을 다음 준비에 가져가되 우승 자격·최우선 권한·팀 결과를 확정하지 않는다. 최신 막출구 overlay는 QUAL1의 합법적 자격/시리즈 창을 별도로 남긴다. 2024-10-23 GAME1의 실패·재시도와 LaVine 공동 역할 비용은 이미 실행됐으므로 반복하지 않는다.

QUAL1은 플레이오프에 참가할 수 있는 가상 팀 자격을 명시하고, 한 동부 상대와 한 시리즈 창에서 베테랑·벤치가 지불하는 부담을 관측하는 다음 단위다. 자격 진출은 우승 가능성의 정량 인증이 아니며 첫 라운드 탈락 경로에서도 이 출구의 미완성을 보여줄 수 있다. Chicago2025 우승·MVP, 2026 MIN Finals, LC1 및 원고 개방은 이 초기 포트의 선택 대상이 아니다.

## 공식 날짜·규칙과 가상 좌표

공식 시즌 발표의 종료/플레이인/PO 개시 날짜를 소비했다. [NBA 2024–25 공식 일정 발표](https://www.nba.com/news/2024-25-nba-regular-season-schedule)

2025 플레이인 일정은 7/8 경기 4월15일, 9/10 경기 4월16일, 마지막 시드 경기 4월18일이다. [NBA 2025 일정](https://www.nba.com/news/2025-nba-playoffs-schedule)

7/8 승자는 7번, 9/10 승자와 7/8 패자의 승자는 8번 시드다. [NBA 플레이인 방식](https://www.nba.com/news/nba-adopts-play-in-tournament-on-full-time-basis) 영구 채택은 [NBA 이사회 공식 발표](https://www.nba.com/news/nba-board-of-governors-approves-heightened-penalty-for-transition-take-foul)와 별도로 대조했다.

공식 본문은 웹 관측이다. 같은 네 URL의 직접 HTTP는 모두 403이어서 실패 bytes/상태/SHA를 임시 캐시에 보존했으며 본문 증거로 채택하지 않았다. 2025 실제 시드·승자·명단·득점은 가져오지 않는다. 아래 상대·시드·승패 조건·개별 시리즈 날짜는 전부 **미선택 가상 후보**이고 실제 NBA game_id는 null이다.

## 세 경로

| 경로 | 가상 자격/상대 | 날짜 | 새 FY24 상대 가족 | 비교 비용 |
|---|---|---|---|---|
| **A 권고** | CHI 정규6→직접 PO6, PHI3과 첫 라운드 | 자격4/13; 시리즈4/19·21·24·26, 필요시4/29·5/1·3 | PHI 1팀 | 한 상대의 계약/가용과 실제 벤치 비용에 집중 |
| B | CHI 정규7, ATL8에 승리→PO7, MIL2 | 플레이인4/15; 첫 라운드4/19부터 | ATL/MIL 2팀 | 단판 결과와 부하를 먼저 선택해야 함 |
| C | CHI 정규9, ORL10·ATL8에 연속승→PO8, MIL1 | 4/16·18; 첫 라운드4/19부터 | PHI/ORL/ATL/MIL 4팀 | PHI7의 ATL8 격파까지 선행; 짧은 회복·여러 상대 입력 |

세 안의 Chicago 정규 순위가 6/7/9로 달라 상호 배타적이다. A의 홈 순서는 PHI/PHI/CHI/CHI/PHI/CHI/PHI다. 해당 개별 날짜는 새로운 가상 일정 제안이며 실제 2025 첫 라운드 날짜를 상대만 바꿔 복사한 기록이 아니다. 아직 시리즈 승자도 선택하지 않았다.

A의 동부 전체순서 후보는 **MIL/BOS/PHI/NYK/CLE/CHI/MIA/ATL/ORL/TOR/IND/BKN/DET/WAS/CHA**(1–15)다. 모든 승패 수치는 null이며 해당 순서는 모델 승수에서 유도하지 않은 별도 가상 설정 후보다. PHI3/CHI6가 같은15팀 순서 안에 있어 placeholder두 개만인 구조를 피한다. 이 순서가 다른팀 당해 계약·경기·전체 시즌·2025 드래프트 권리/순번까지 인증하는 것은 아니다.

**A를 권고한다.** 이미 선택된 Chicago 성장 코어와 개발 B 계획을 보존하며, 준비된 PHI 역할 원형에 2022 선택 신인 Blake Wesley까지 들어 있어 동료·벤치 부담을 바로 비교할 수 있다. 준비된 NOP은 서부이므로 동부 Chicago의 첫 라운드 상대가 될 수 없다.

## A에 실제로 필요한 네 입력

1. **Q_SEED:** root가 A와 일관된 가상 자격 증인(CHI6/PHI3)을 선택한다. 전체 정규 결과를 계산했다고 주장한다면 결과/순위 입력을 붙여야 한다. 한정 설정상의 자격 참가를 명시적으로 채택하는 경로라면 정규82경기 실행은 false로 남길 수 있다. 자리표 두 개만으로 계산된 진출이라 인증하지 않는다. 역사 순위나 임의 ABC 동률해소를 쓰지 않는다.
2. **Q_PHI_SERVICE:** 아래 PHI 15명 각각의 당해 서비스·유효 옵션·같은 팀 새 UPC를 admitted lawful piecewise 가족으로 선택한다. 예전 명단은 소유/역할 원형이며 2025 원 UPC의 자동 존속 증거가 아니다. original Γ와 Hill 방출 채무를 보존한다.
3. **Q_DAY:** CHI·PHI 각각 13명 가용/active, 2명 inactive를 새 시리즈 날짜 구간에서 명시 선택한다. 임상 사실·과거 시즌 건강·GAME1 하루 가용성의 자동 연장이 아니다. 0분 reserve도 등록/가용을 갖춰야 한다.
4. **Q_OBSERVATION:** 서로 다른 시리즈 날짜의 두 8초 부담/수정 표본과 행위자 조건을 선택한다. 득점·승패·전체 시리즈 우승은 이 관측의 필수값이 아니다. 결과가 서사에 필요하면 기존 위임 범위의 별도 가상 결과 모델로 명시한다.

전역1230경기, 전체30팀 사적 원장, 모든 미래계약·17시즌을 이 네 입력의 선행 gate로 추가하지 않는다. 미입력 가격/보너스/잔여 비용을 0으로 채우지도 않는다.

## 명명 계약과 가용성

Chicago의 현행 선택 10 live + 5 새 minimum 가족, LaMelo/Jaquez 가격·원 Γ·R24·D24는 원본 전체로 보존했다. 각 `service_window_condition`이 제안한 4/19–5/3을 포함하는 admitted family인지 확인해야 하며 회계연도 끝을 원 사적 서비스 말단으로 읽지 않는다. LaVine·주인공의 2025 이후 계약/옵션을 이 구간 때문에 행사하지 않는다.

PHI 원 소유 15명은 Simmons/Green/Howard/Korkmaz/Joe/Springer/Embiid/Thybulle/Scott/Reed/Curry/Milton/Harris/Maxey/**Wesley**다. George Hill은 2022 zero-reserve clearance 원 Γ를 별도로 유지하고 등록에 다시 넣지 않는다. 실제2024 Paul George, 실제 Harden/Simmons 거래나 은퇴를 자동 이식하지 않는다.

Springer2021 RSC의 FY24 4년차와 Wesley2022 RSC의 FY24 3년차는 각각 적법한 2023 서명·개별 통지 조건을 붙인다. 제안 통지는 2023-10-01, 원 선택 Finals6/16 이후 창과10/31 기한 안이다. 실제 접수는 null이다. 나머지는 원 UPC/유효 옵션이 살아 있으면 원 Γ를 이월하고, 만료면 같은 팀의 적법한 2023 연속 계약과 별도2024 신규 계약을 순서대로 구성한다. Bird/Early/NonBird의 서비스 조건, 최소/최대/보호/bonus를 생략하지 않는다. 모르는 기간을 임의 연장하거나 팀 핵심의 minimum 수락을 시장 개연성 PASS로 삼지 않는다.

양팀 등록15STD/0TW, active/available13·court5/나머지8·inactive2 제안이다. PHI는 원 양수12명에 0분 Isaiah Joe를 더하고 Springer/Reed를 inactive로 둔다. 실제 임상 사실이나 다른 날의 nomination을 인증하지 않는다.

## 여섯 비용 범주·floor·trigger

PHI는 live 원/new Salary, waived/former 원 Γ(Hill 포함), camp/prior 명명 채무, unsigned rights/RT, FA/QO, unused exceptions/incomplete 여섯 범주를 각각 함수로 보존한다. 원 권리를 쓰는 새 합의 이후에만 적법한 cleanup을 제안하며 보호채무는 삭제하지 않는다. 미입력 D24normal/apron·camp·잔여액은 null/비음수 조건이며 합계 상단은 미인증이다.

기존 Game1 primary의 cap140,588,000/보도 표시 floor126,529,000을 보존하며, 이번 충분조건·gap에는 법식 floor126,529,200을 사용하고 2023 CBA VII2c의 MTS 별도 정의·statutory gap/payment를 직접 읽었다. ordinary FAhold나 unusedexception을 부풀려 floor를 충족했다고 하지 않는다. 충분 후보는 적법한 고정급여 함수로 opening MTS≥floor 및 당해 threshold 유지 조건을 만족하는 하위가족이다. 그 밖의 가족은 법정 추가 charge/payment/다음날 threshold복구 조건을 보존한다. 실제 지급액이나 사적 전체 예산은 미인증이다.

같은 팀 Bird/minimum/원RSC옵션만 쓰며 신규 S&T/NTMLE/BAE/assignment를 넣지 않는다. 실제 source가 지목하는 FY24 trigger H24는 해당 apron 제한과 함께 조건부로 남고, 이전 hardcap을 다른 capyear로 복사하지 않는다. 해당 범주 상단이 null인 사실을 신규 사적 장부 전수요구로 바꾸지도 않는다. 새 UPC는 법정 moratorium/기존 만료 이후이며 마지막 정규경기 시작 전 서명해야 하므로 시리즈 도중 계약을 붙이는 우회는 없다.

## 시계와 직접 비용

JSON은 선택된 Chicago B의 24블록과 이전 PHI 신인 개발 시계를 **새 FY24 후보**로 직접 조인했다. 각팀5포지션×2880초, 14,400 player-seconds=240분, 양수 선수 등록/active와10명 중복 없음까지 실제 정적 검산했다. 0OT는 선택 시 새 가상 정책이며 역사 OT 부재의 인증이 아니다. 승자/효율/신규2025 성장계수는 없다.

CHI: P34/Melo30/LV30/Mark30/Carter28/Jaquez20/Kessler14/Caruso20/Duarte10/Coby14/Young10. PHI: Simmons32/Curry30/Green24/Harris32/Embiid34/Wesley12/Thybulle16/Maxey16/Milton12/Howard14/Korkmaz14/Scott4.

CHI B의 Jaquez+16분은 A 대비 Duarte−4, Coby/Young/Kessler−2씩, LV/Melo/Mark−2씩의 같은240분 재분배다. PHI Wesley12분은 기존 Milton/Maxey 각6분의 국소 기회비용이다. 새 임금 삭제나 중복 계약비용이 아니다.

S3 새 표본은 G1(4/19)과 G2(4/21)의 같은 3Q1680–1688초로 제안한다. CHI Caruso/Coby/Duarte/P/Carter와 PHI Maxey/Milton/Thybulle/Simmons/Howard가 각각40 player-seconds를 갖는다. 첫 표본의 P 약한 쪽 지연→Duarte 추가 보완 노동, 수정 표본의 P 앞선 도움 **및 Duarte 자신의 읽기/같은 Thybulle 커터 조건**을 붙인다. P의 이동 하나만으로 동료 위치 유지·득점 저지를 보장하지 않는다. 두 관측은 미선택이고 GAME1의 두 창을 다시 세지 않는다.

## 검문·진척

13물리핀, PHI source indexed row/ID/소유, RSC 원등록, CHI/PHI 24개 동시 구간의 각48/240·등록15·active13, route6/7/9 구분 및 unknown/null 경계를 정적으로 확인했다. 생성기가 없는 두 파일 패킷이므로 constructor 음성/독립 검문을 지어내지 않았다. independent review=false, qualification/series observation executed=false다.

| 그룹 | 상태 |
|---|---|
| 1 | COMPLETE |
| 2 | COMPLETE |
| 3 | COMPLETE |
| 4 | INCOMPLETE |
| 5 | INCOMPLETE |
| 6 | INCOMPLETE |
| 7 | INCOMPLETE |

QUAL1이 선택돼도 Game1 첫 옵션 지위·효율과 영구 최우선 권한은 소급 증명되지 않는다. 전체A10 종료는 해당 주장 여부와 기존 local exact exit를 다시 대조할 포트로 남긴다. 우승·MVP·전체 시즌 결과를 이 관측의 새 필수조건으로 추가하지 않는다.

미완료4개 / 6번까지3개. v0.30 PARTIAL·CLOSED·Pack0·원고0. 첫 우승창의 자격·비용을 구체화할 권고이며 Chicago 우승/MVP·전체A10 완료를 선택하지 않았다.

## 법문 위치와 표시 정밀도 보정

일반 apron 조정은 2023 CBA VII2(e)(1), PDF210–211이다. VII6(n)(3), PDF273의 원팀 RSC 옵션 미행사 후 신규계약 성분 상한은 적용 가능한 별도 가지로 보존한다. 정규 마지막 경기 시작 후 신규 UPC 제한은 VII5(e)(2), PDF254다.

공식 보도 표시 floor 126,529,000은 보존한다. 충분조건과 차액 함수에는 VII2(a)(4)(i)의 90% × 140,588,000 = **126,529,200**이라는 DESIGN_CALCULATED 값을 쓴다. MTS current/opening이 각126,529,100이면 차액100이며, 표시값으로 계산한0을 채택하지 않는다. 기존 충분증인126,709,880은 두 값 모두 초과하여 결론이 변하지 않는다. 실제 사적 센트·가격·접수를 인증한 계산은 아니다.
