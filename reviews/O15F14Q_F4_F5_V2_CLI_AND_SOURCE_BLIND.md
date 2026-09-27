# O-15F14-Q — F4/F5 선택 경로의 도구별 검증 기록

- 기준: `main` `b258ad8` 이후 F4/F5 선택 브랜치. [결정](../canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json)과 [국소 계산](../simulation/CHICAGO_2020_21_F4_F5_SELECTED_BRIDGE.md)은 정본의 일부가 아니라 D1 재검증 입력이다.
- Anti-Gravity CLI 절대 경로 `C:\Users\Storm Credit\AppData\Local\agy\bin\agy.exe`와 NotebookLM CLI `nlm`, Claude CLI를 실제 호출했다. 도구 실행 횟수를 독립 원자료 건수로 세지 않는다.

| 단계 | 실행·입력 | 결과·판정 |
|---|---|---|
| Anti-Gravity 원자료 | Cavaliers 2020-11-23 [McGee 취득 구단 공지](https://www.nba.com/cavaliers/releases/mcgee-trade-201123)를 읽기 전용 `read_url_content→view_file`로 요청. stream-json에서 두 호출 DONE 확인 | 저장 본문은 26,566바이트 HTML 셸로 선수·픽 기사 본문을 추출하지 못했다. 60초 print 제한에서 최종 응답 빈 문자열. `RUN / NO_ARTICLE_BODY`, Evidence Pack 증가 **0건**. 원역사 사건은 Codex가 같은 공식 링크를 별도 직접 확인한 범위에서만 사용. |
| NotebookLM 출처 연결 | [작업실](https://notebooklm.google.com/notebook/a3f30584-3a9d-4a8b-8960-b661615d98e9)에 NBA 공식 URL 3건 추가 시도 실패. 저장소 작성 F4/F5 결정·브리지의 **한 줄 요약만** 출처 `564bacb7-ec07-45c0-81d3-94796a2b5379`로 추가하고, `nlm content source`로 820자 수록을 확인한 뒤 해당 출처만 질의 | 3/25 미거래→4/13~5/1 Hall 기존 계약→5/2~8 공백→5/9 미재계약의 연표 반환. 5/9에 이미 떠난 Hall을 다시 `remove`한다고 읽힐 수 있는 문구를 지적했다. **표현 수용**: 계산은 5/9 원안 재계약 행 삭제이며 새 5/2 해제 사건이 아님을 브리지에 명시. NBA 출처 검증 `NOT_RUN`이고 이 작업실은 Codex 입력 하나의 재독이다. |
| Codex 저장소·산술 | 5+25 국소 경기, 두 방법 60개 승자 방향, ORL 15+2, CLE 14경기 조건부 5인조·DEN 11경기 역할, 급여 공개값 차액과 출처 해시 | 국소 재현 PASS. 전체 건강·등록/급여·플레이오프·F1~F3는 HOLD. |
| Claude 반증 | 결과 문서만 `haiku --tools '' --max-turns 1`로 검토 | [R01 처분](R01_O15F14Q_F4_F5_SELECTED_BRIDGE_BLIND.md)에 표현 보강·HOLD를 기록. 원자료 접속 없는 문서 단독 검토. |
| Source-blind | 위 Claude의 결과 문서 단독 검토는 이전 긴 연구·추천 논리를 입력하지 않은 제한형 검수 | Hall 계약 시점과 K1 불변의 전제를 의심했다. 독립 원자료나 G16 심사로 세지 않는다. |

F4/F5의 **방향만 작가 선택**이다. F1~F5 전체 PASS `0/5`, A1~A3 최종 채택 `0/3`, 네 K 종료 `0/4`. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, `manuscript_allowed=false`.
