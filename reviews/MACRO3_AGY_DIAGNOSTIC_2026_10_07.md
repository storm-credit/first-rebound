# Antigravity 단일호출·MCP startup 한정 진단 — 2026-10-07

범위는 **현재 help와 보존 timeout helper의 실독**입니다. 새 NBA본문 수집·MCP 실통신·전체 G16 인증이 아닙니다. 프로젝트 진행을 CLI 복구에 종속시키지 않습니다.

## 확인한 것

- 절대 경로 `C:/Users/Storm Credit/AppData/Local/agy/bin/agy.exe --help`: **exit0, 0.358초**. `--print`, `--print-timeout`, `--output-format json/stream-json`, `--json-schema`, `--mode plan`이 현재 광고된 옵션입니다.
- `agy.exe help mcp`: **exit0**. 노출된 하위명령은 add/remove/list/enable/disable입니다. 한 번의 print호출에서만 MCP를 빼는 옵션은 이 help에 없습니다. `--sandbox`는 terminal 제한이고 `--disable-slash-commands`는 slash/skill 확장을 막는 옵션이므로 MCP 격리로 해석하지 않습니다. 미공개 방법이 없다는 전역 주장도 하지 않습니다.
- [기존 macro3 호출](MACRO3_AGY_RULE_COLLECTION_2026_10_07.json)과 그 보존 helper를 직접 읽었습니다. 공식URL **3개**, 모델 명시 없음, `plan/json/schema`, 내부35초·외부45초였습니다. **45.076초 PROCESS_TIMEOUT, 응답null** 기록은 그대로 유지합니다.
- helper의 timeout branch는 부분stdout/stderr를 버리고 상태·시간만 저장합니다. 따라서 기존 자료로 **MCP startup→Codex/NotebookLM 호출**, 웹 열람, 모델 처리, plan수명주기, 종료 대기 중 어디에서 지연됐는지 판별할 수 없습니다. 프롬프트의 “external MCP를 쓰지 마라”는 문장만으로 MCP startup 차단을 인증할 수 없습니다.

현재 help에 인자가 존재한다는 사실은 옛 프로세스가 인자를 끝까지 성공적으로 해석했다는 별도 증명이 아닙니다. **인자 오류를 관측한 근거0, MCP startup 원인 확정0**입니다. 원인을 추측해 로그인이나 설정을 바꾸지 않습니다.

## 새1URL 시험을 실행하지 않은 이유

이번 지시는 **공식 단일호출 no-MCP 옵션이 확인되면** temp cwd에서 공식2022cap URL 하나를35초 한 번 실행하는 조건이었습니다. 현재 help는 그 조건을 충족하지 않아 **NOT_RUN**입니다. 새본문 성공0/새독립출처0이며 timeout을 성공으로 재계수하지 않습니다.

후보 URL은 [NBA2022 cap 원발표](https://pr.nba.com/nba-salary-cap-2022-23-season/)입니다. 이 URL은 별도 Codex core비용 자료에서 이미 회수했으며, 그것을 이번 Antigravity의 성공으로 표시하지 않습니다.

전역MCP끄기·프로필수정·재로그인·새설치·다른프로젝트세션 변경·미광고flag 추측·옛3URL반복을 실행하지 않았습니다. 계정/key/token/auth 및 세션private로그는 열람/출력/보존하지 않았습니다. 도움말과 task helper 코드·이미 sanitization된 저장소 기록만 읽었습니다.

## 동작과 수집 성공의 구분

[앞선 운송 진단](ANTIGRAVITY_RECOVERY_DIAGNOSIS_2026_10_07.json)의 모델목록/1.3.0/25.72초 `AGY_OK`는 **당시** 모델·응답 운송이 가능했다는 기록입니다. 이번에 모델목록이나 인증을 다시 시험하지 않았습니다. help 실행 성공·앞선 모델목록 성공·본문 수집 성공·MCP 실통신은 별개입니다. 지금 단정할 수 있는 내용은 실행파일/help 동작과 옛 timeout의 계측 한계입니다.

원천2개 LF정규화SHA와 helper rawSHA는 [JSON](MACRO3_AGY_DIAGNOSTIC_2026_10_07.json)에 있습니다. 기존 source/parser/helper 수정0, 중앙/원장/Git변경0.

## 전체7행

[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)의 진행을 보존합니다.

|번호|작업|상태|
|---|---|---|
|1|2020드래프트연쇄|완료|
|2|Chicago2020–21|S2완료|
|3|2021–23 거래·계약|draft60 후보·2022core 입력 독립검문 완료; 전체미완료|
|4|장기커리어|후속설계|
|5|결말·전체구조|국소기능 누적; 전체미완료|
|6|집필규격·Context Pack|후속기능 진행·실제Pack0|
|7|통합·독립·작가승인|최종게이트 CLOSED|

미완료 큰 묶음 **5**. `v0.30 PARTIAL`·설계/원고 `CLOSED`·원고0. CLI 진단을 마쳤으며 승인된 프로젝트 작업은 계속합니다.
