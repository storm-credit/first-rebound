# LaVine 2026 선수 옵션: 두 법적 후보

**후보 / 미선택.** 기존 Chicago 계약의 Year5 **$48,967,380**을 행사하는 A안을 권고한다. 실제 선수의 시장 판단·사적 통지·접수·지급을 인증하지 않는다.

## 원계약과 기한

- 원2022 선택 계약은 4개 stated Seasons(2022–2025) + 2026 Player Option 하나다. Year4 $45,999,660 → Year5 $48,967,380, 증가 $2,967,720. stated4 합 $166,192,320, 유효 행사 시 5년 base 합 $215,159,700. 새6년차·새UPC가 아니다.
- 실제 pointer: `simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json#/contract_terms/LaVine`, 원후보 `#/terms_candidate`, FY25 named15 `#/named15/4`, FY26 rollover `#/rows/4`. 원후보 false는 생성 당시 이력이며 현재 원계약 선택을 부정하지 않는다. 옵션 자체는 아직 선택하지 않았다.
- 2017 XII2(a)/3/4/5 PDF334–336의 원계약 법적형식과 [2023 CBA](https://imgix.cosmicjs.com/25da5eb0-15eb-11ee-b5b3-fbd321202bdf-Final-2023-NBA-Collective-Bargaining-Agreement-6-28-23.pdf) XII2–5 PDF360–362의 현재 행사 규칙을 분리했다. **2026-06-29 월요일 17:00 ET**까지 행사. 원계약도 June29이며 veteran UFA인 이 가족에는 RFA June25 예외가 적용되지 않는다.
- 후보는 **June29 16:00 ET 선수 서명 이메일 → 구단의 적법 수신16:05 → NBA 전달16:10**. 이메일 단독이 원UPC 지정 채널에서 유효하다는 조건 또는 같은 기한의 적법 서면 전달을 명시한다. XII5는 Team→NBA→NBPA 전달 사본을 정하며, 선수 이메일의 자동 deemed-sent 법칙을 정하지 않는다. XI의 offer-sheet 이메일 규칙을 가져오지 않는다. NBA 수신 후 NBPA 사본은 2영업일 이내; 이 달력 예시에서 July1이며 실제 접수는 null이다.
- A형 보호를 선택했다. 행사 전 구단 해지에도 행사한 것과 같은 보호가 남는다. B형에만 붙는 '구단 마지막 경기 다음 날부터 행사' 제한을 A형에 넣지 않는다. 허용된 원계약 행사구간 안의 통지라는 조건은 보존한다.
- fiscal June30, 원NBASeason 마지막 Finals 경기, 계약상 서비스 완료는 서로 다르다. 여기서 Finals 날짜·우승자·건강 또는 서비스 실제완료를 선택하지 않는다.

## 상호배타적 비교

| 후보 | FY26 LaVine claim | 등록·권리 | 경계 |
|---|---|---|---|
| A 행사, 권고 | 기존 Year5 base $48,967,380 + 적용 원Γ, 한 번 산입 | 기존1UPC/STD증분0/TW0, 같은 선수 FA hold 없음 | 실제행사·가격예측0, 다른 STD≤14일 때 합≤15인 국소조건 |
| B 불행사→UFA | 이 UPC의 option base0; 원부채0 아님 | 서비스 완료 조건의 ordinary UFA hold, 새UPC/가격/팀 null | 동일 hold는 새계약·타팀서명·적법renounce 때 한 번 교체, 원A형 해지 보호 유지 |

B의 normal FA amount는 VII4(d)(1)(i)/(5)/(8): prior Salary P25가 prior Estimated Average 이상이면150%, 미만이면190%, 적용 최소/최대 범위로 clip한다. P25에는 regular·signing allocation·실제 earned incentive가 포함된다. rookie250/300%가 아니다. VII2(e)(1)(iv)의 apron 계산은 고립된 ordinary FA amount를 제외하며, 다른 부채나 현재 apron-trigger를0으로 만들지 않는다. 신규 Bird가격·기간 또는 이적은 별도 미선택 포트다.

## 원보호·비용 보존

원100% skill/injury 보호, 표준조건, bonus0, Ex4율0..15%/실제율null을 유지한다. 옵션행사는 거래를 선택하지 않는다. 기존 live / waived·stretch·resolution / FA·QO / unsigned·RT / exception·current-apron / incomplete·floor 여섯 범주를 JSON의 명명 함수로 보존했다. 2021 hardcap을 2026에 이월하지 않으며, 새해 유효 transaction restriction은 그대로 조건이다. wholeFY26 비용·전체15명·사적장부 인증은 하지 않는다.

## 검문과 다음 연결

4개 LF source pin·4개 실제 pointer·원CBA 두 PDF와2026 cap 원raw SHA를 검문했고 원표 산술을 재계산했다. 정적 패킷이므로 constructor시험0/조상재실행0, 독립검문 미완료. 다음은 root/peer가 A/B를 검문한 뒤 실제 가상 선택·적법 통지를 신규 소비자에 기록하는 단계다.

프로젝트: 1 완료 / 2 완료 / 3 완료 / 4 미완료 / 5 미완료 / 6 미완료 / 7 미완료. 미완료 전체4, 6번까지3. design CLOSED / Pack0 / 원고0.
