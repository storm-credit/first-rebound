# O-15G15N — Orlando 2021–22 공통 계약 8명의 비용 입력

- 기준: `main` `e95b0d2` / PR #197의 [G15M](O15G15M_BACON_GUARANTEE_AND_ROOKIE_CAP_HOLD.md) 다음 조사. [G15L](O15G15L_ORLANDO_SUMMER_CONTRACT_EVENT_LEDGER.md)의 **조건부 공통 8명**을 선수별 계약 금액으로 연결한다.
- 상태: `HISTORICAL_CONTRACT_CHARGES_RECONCILED / ALTERNATE_TEAM_SALARY_HOLD`. 표의 금액은 원역사 계약 추적 자료의 2021–22 입력값이다. 대체 Orlando의 최종 명단·전체 팀 샐러리·캡 공간·새 사건을 확정하지 않는다.

## 1. 선수별 원역사 계약 charge

NBA의 [2021 드래프트 당시 Orlando 팀 프로필](https://www.nba.com/draft/2021/team-profiles/orlando-magic)은 아래 8명을 `Under Contract`에 넣었다. 이는 7월 무렵의 계약 분류이지 대체세계의 10월 등록 증명은 아니다. 금액은 각각 연결된 **비공식** SalarySwish 계약 이력의 해당 시즌 `Cap Hit`이며, 선수의 기본급·인센티브가 다른 경우 따로 썼다.

| G15L 공통 후보 | 2021–22 원역사 cap hit | 기본급 / 보장·인센티브 차이 | 대체 Orlando 사용 조건 |
|---|---:|---|---|
| [Gary Harris](https://www.salaryswish.com/players/gary-harris) | $20,482,143 | 기본급 동일; 별도 unlikely incentive $2,600,000은 이 charge에 **합산하지 않음** | Gordon 거래 A의 Harris 유입이 실제 실행되고 후속 이탈이 없을 때만. |
| [Jonathan Isaac](https://www.salaryswish.com/players/jonathan-isaac) | $17,400,000 | 기본급 동일; unlikely $2,600,000 별도 | 기존 연장계약과 보유가 유지될 때. |
| [Markelle Fultz](https://www.salaryswish.com/players/markelle-fultz) | $16,500,000 | 기본급 동일; unlikely $1,000,000 별도 | 기존 연장계약과 보유가 유지될 때. |
| [Terrence Ross](https://www.salaryswish.com/players/terrence-ross) | $12,500,000 | 기본급 동일; unlikely $1,000,000 별도 | 기존 계약과 보유가 유지될 때. |
| [Mo Bamba](https://www.salaryswish.com/players/mo-bamba) | $7,568,743 | 기본급 동일; 2021–22 팀 옵션 행사 원역사 추적 | 대체세계에서도 옵션 행사·보유가 유지될 때. |
| [Cole Anthony](https://www.salaryswish.com/players/cole-anthony) | $3,449,400 | 기본급/표시 보장액 $3,349,400 + likely incentive $100,000 | 기존 신인 계약·인센티브 취급이 유지될 때. |
| [Michael Carter-Williams](https://www.salaryswish.com/players/michael-carterwilliams) | $3,300,000 | 기본급·보장액 동일. 원역사 2022-02-10 방출은 이 2021 여름 비용 입력 이후 사건 | 기존 계약·보유가 유지될 때. 원역사 2022 방출 자동 이월 금지. |
| [Chuma Okeke](https://www.salaryswish.com/players/chuma-okeke) | $3,277,080 | 기본급/표시 보장액 $3,177,080 + likely incentive $100,000 | 기존 신인 계약·인센티브 취급이 유지될 때. |
| **8명 조건부 부분합** | **$84,477,366** | 기본급 열 단순합 **$84,277,366** + likely $200,000. Unlikely $7,200,000은 별도 표시이며 이 합계에 넣지 않음 | 위 8명 모두의 계약이 해당 날짜에 Orlando에 귀속된다는 동시 조건에서만. |

Harris의 $20,482,143은 [당시 Hoops Rumors의 팀별 최고 연봉표](https://www.hoopsrumors.com/2021/10/highest-paid-nba-players-by-team-4.html)와도 일치한다. 다른 집계에 보이는 $20,932,143은 여기서 사용하지 않는다. SalarySwish가 `Base Salary`, `Likely Inctv.`, `Unlikely Inctv.`를 분리하므로 세 열을 섞어 원역사 팀 샐러리인 것처럼 계산하지 않는다. 이 8명은 [G15L의 7월 선수 집합](O15G15L_ORLANDO_SUMMER_CONTRACT_EVENT_LEDGER.md)이지 G15E의 10월 공통 11명 전체가 아니다.

## 2. 기존 두 선수 및 #24 대체 신인과의 연결

[G15J](O15G15J_ORLANDO_2021_22_CONTRACT_INPUT_LEDGER.md)의 Vučević $24,000,000와 Aminu $10,183,800을 **둘 다 Orlando가 2021–22에 보유한다는 조건**에서만 위 8명에 더하면 `8계약 $84,477,366 + 추가 2계약 $34,183,800 = 10계약 $118,661,166`이다. 이것은 **10계약만의 가상 부분합**이며 Nnaji도 아직 없다. 원역사 [NBA 발표의 2021–22 cap $112,414,000](https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season)보다 크다는 산술만으로 불법 또는 사치세 여부를 판단할 수 없다. 이미 서명된 계약, 각종 예외, hold/방출 charge, 후속 이적과 날짜가 빠져 있다. T2 작가 승인은 Vučević의 **2020–21 잔여 시즌**에만 미친다.

[Gordon 대체 보드](../simulation/ORLANDO_DENVER_2021_GORDON_BOARD.md)의 Nnaji는 대체 2020 드래프트 **#24** 후보이며 원역사 Denver **#22** 신인 계약을 그대로 받을 수 없다. [RealGM의 2020 드래프트 신인 스케일](https://basketball.realgm.com/nba/info/rookie_scale/2021)은 #24의 2년차 2021–22 스케일을 **$1,919,200**으로 제시하고, 1라운드 서명 가능 범위를 스케일의 80~120%로 설명한다. **2020년 드래프트 뒤** 그 픽으로 Nnaji가 실제 서명해 **120%를 택했고 2021–22 계약이 계속 유효**하다는 별도 가정이면 2년차 후보 charge는 `1,919,200 × 1.2 = $2,303,040`이다. 이 금액은 위 8계약·10계약 부분합 **어디에도 포함하지 않았다**. [원역사 #24 RJ Hampton의 계약 추적표](https://www.salaryswish.com/players/rj-hampton)도 cap hit $2,303,040이지만, 이는 **금액 산술 대조**일 뿐 대체 Nnaji의 서명일·기본급·likely incentive·Orlando 소유를 증명하지 않는다. [원역사 #22 Nnaji의 $2,498,760](https://www.salaryswish.com/players/zeke-nnaji)을 Orlando 후보에 복사하면 **#24·120% 시험과 비교해 $195,720 과대** 계산한다. 실제 대체 계약액은 `HOLD`다.

[G15M](O15G15M_BACON_GUARANTEE_AND_ROOKIE_CAP_HOLD.md)의 Mobley3 미서명 1R hold 후보 $8,075,160은 위 8명, 두 선수 부분합 또는 Nnaji #24 산술 어디에도 포함하지 않았다. Bacon 보유/방출, Lopez·Moritz·Moore 영입, Herbert33 권리/계약, 다른 FA hold와 보장급여도 별도 사건이다. 따라서 이번 부분합을 10/16 전체 팀 샐러리, cap room, 거래 매칭 가능액으로 승격하지 않는다.

**사실:** NBA 원역사 드래프트 당시 분류와 리그 cap 발표, 비공식 선수별 계약표의 표시값. **추론:** 조건부 8명/10명 합산, #24를 120%로 서명할 때의 2년차 후보와 #22 대비 차이. **후보:** Harris 유입·Nnaji #24 서명·Vučević/Aminu 잔류 등 대체 사건. **작가확정:** 신규 0건.

## 3. 도구별 실행 범위

- **Antigravity CLI:** 로그인된 `agy.exe`로 NBA 공식 cap 발표 URL 직접 읽기를 요청했다. 35초 `print timeout`, 본문 0건이므로 이번 숫자의 Antigravity 증거는 `0`이다. CLI 버전 확인 `1.2.11`은 출처 판독 성공과 구분한다.
- **NotebookLM CLI:** 비정본 작업실에 Harris `160dc2f3-1dc9-4e1e-8667-db4365acb44f`, Cole `0428ccd7-e731-4e67-b2cf-330867211c49` 계약표 URL을 추가했다. 이 **두 소스만** 지정한 질의 `6bd7d46f-57a3-4731-9f03-0e4e1a3ef0b5`가 Harris 기본급/charge $20,482,143과 unlikely $2,600,000, Cole 기본급 $3,349,400 + likely $100,000 = charge $3,449,400을 분리했다. 동일 비공식 계약표 재분석이지 독립 원자료 2차 확인은 아니다.
- **Codex:** 8명 계약표와 당시 NBA 선수 분류·RealGM #24 스케일·원역사 #22/#24 계약을 교차하고 합산을 코드로 재계산했다. 승인 범위, 자리와 charge, 이미 서명한 계약과 새 계약/hold를 분리했다.
- **Claude CLI:** [제한 반증·결과 단독 검수](../reviews/R01_O15G15N_CLAUDE_LIMITED_AND_SOURCE_BLIND.md)의 좁은 산술 호출은 계산 오류가 없다고 했으나 원역사 #22가 대체 #24의 실제 의무라는 잘못된 전제를 제기해 기각했다. source-blind 편집 검수는 8+2 부분합과 #24 조건/제외 표시를 명료하게 하도록 지적했고 위 문장을 보강했다. 독립 계약 감사나 G16 PASS가 아니다.

## 4. 다음 인수

Lopez·Moritz·Moore의 원역사 계약과 Moritz의 자유계약선수 권리/hold, Herbert33의 required tender/서명 형식, Bacon 분기, Nnaji 실제 대체 서명 조건을 날짜별로 채운다. 그 뒤에만 G15L의 7/29→10/16 자리 원장과 Team Salary 입력을 동시에 재계산한다. G14 ORL4 `ROLE_HOLD`·DET4 `PRIOR_HOLD`, G16/G17 미완료, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, author/season/exact/manuscript false를 유지한다.
