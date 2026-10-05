# Denver 2020 예외 사용 — 원보도와 실제 서명 연결

기준 main `9391fab`. [근거 원장](DEN_2020_EXCEPTION_EXECUTION_EVIDENCE_2026_10_05.json). 판정은 **원보도 본문 회수 완료 / 실제 적용 예외·전체 비용 HOLD**다.

이 문서는 **초기 계획 보도·서명 연결 조사**다. 아래 null은 해당 단계의 판정이다. 이후 [역사 상한 증인](DEN_HARDCAP_POST_SIGNING_REPORT_2026_10_05.json)에서 후속 보고와 별도 숫자·법규 근거를 연결해 역사 상한138,928,000을 확보했다. 대체 비용 전체 HOLD는 유지한다. NotebookLM 입력은 이 후속 연결 이전 사본이다.

## 직접 확인한 것

- **당시 원보도:** Mike Singer의 [Denver Post 2020-11-21 기사](https://www.denverpost.com/2020/11/21/nuggets-free-agency-jerami-grant-paul-millsap/) 본문 9번째 문단은 익명 리그 소식통을 근거로 Green의 MLE, Campazzo의 BAE 사용 **계획**을 보도한다. 미래형이며 구단의 실행 확인은 아니다. Python HTTP200으로 원본문을 회수했고 web 도구의 robots 차단과 구별했다. 기사 전체는 저장소에 복제하지 않고 본문 위치·지문을 원장에 기록했다.
- **NBA 공식 기록:** [Player Movement](https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json)의 고정 사본 9,927행 중 Green·Campazzo의 2020-11-30 서명 2행을 대조했다. 계약 서명은 확인되지만 적용 예외명은 없다. 현재 제공되는 데이터의 과거 날짜 기록이며 당시 리그 접수증은 아니다.
- **2017 조문:** [NBA 공식 CBA](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf) PDF227/228/231/240쪽을 직접 읽었다. BAE·NTMLE 사용 이후 해당 cap year의 apron 의무, TaxMLE 재분류 조건, apron의 성과 보너스 산입을 구분했다. 2020 개정 적용까지 인증한 것은 아니다.

## 비용 증명에 연결하는 범위

당시 BAE 계획과 후속 서명의 일치는 실행 경로를 지지하는 **추론**이다. 원계약 모든 센트가 없더라도, 실제 적용 예외와 해당 시즌 규칙을 확인하면 원역사 전체 apron 비용 상한을 법적 의무에서 도출할 수 있다. 이 경로는 [F5 비교식](DEN_F5_COST_COMPARATOR_2026_10_05.md)의 `HIST_UPPER`를 채울 수 있다.

현재 `138,928,000`은 그 경로의 **조건부 상한**이며 인증된 상한은 `null`이다. Gordon/Clark의 당해 연도 배분 보너스 차이와 `DELTA_OTHER` 전체 차액 구간도 남는다. 이 자료만으로 `DEN_COMPLETE_COST`나 `DEN_F5_COMPLETE_COST`를 PASS로 올리지 않는다.

Green의 알려진 첫해 급여가 TaxMLE보다 크다는 사실만으로 취득 경로를 확정하지 않는다. 계약 당시 cap-room과 다른 합법 경로·시간을 함께 검토해야 한다. Bol의 낮은 첫해 급여도 단독 하드캡 증인이 아니다. Campazzo의 당시 보도 약 $6m와 기존 상세 입력은 별개이며 보도 반올림으로 연간 비용을 다시 쓰지 않는다.

## 다음 종료 증인

1. 실제 사용 예외와 2020 규칙 적용을 공개 근거로 연결한다. 비공개 원계약 자체를 새 필수 조건으로 추가하지 않는다.
2. 같은 날짜·동일 apron 정의의 원역사 상한에 **전체 비공통 차액 상단**을 합쳐 제한 이하임을 증명한다. 동일 선수라는 이유로 미확인 보너스·잔여 비용을 자동 0으로 두지 않는다.

새 작가확정0·법적 추가PASS0·전체 비용 HOLD·freeze v0.30 PARTIAL·설계/원고 CLOSED·원고0.
