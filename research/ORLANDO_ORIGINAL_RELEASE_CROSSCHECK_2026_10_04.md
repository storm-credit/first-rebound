# Orlando 원래 계약 발표 대조 — 2026-10-04

기준 main `20020bd`. [근거·지문 JSON](ORLANDO_ORIGINAL_RELEASE_CROSSCHECK_2026_10_04.json), [재현기](../tools/build_orlando_release_crosscheck.py), [검수](../reviews/ORLANDO_ORIGINAL_RELEASE_REVIEW_2026_10_04.md).

## 원역사 사실: 앞선 자료 차이 4건 해소

앞선 [NBA 거래 데이터 대조](NBA_MOVEMENT_WINDOW_EVIDENCE_2026_10_04.md)의 가이드만 존재하던 해제 3건을 **당시 구단 발표 본문**에서 직접 확인했다. 검색 도구가 iframe만 반환했던 URL도 일반 HTTP 응답의 공개 `__NEXT_DATA__`에서 기사 본문을 회수할 수 있었다. 각 기사의 id·게시/수정일·전체 응답/본문 지문을 저장했다.

| 사건 | 당시 구단 발표 | 이번 확인 |
|---|---|---|
| 4/13 Cannady 일반계약 해제 | [Hall 영입 발표](https://www.nba.com/magic/orlando-magic-sign-donta-hall-ten-day-contract-20210413), 첫 문단 | 10일 계약에서 해제했다고 명시 |
| 4/27 Franks 해제 | [Wagner 영입 발표](https://www.nba.com/magic/orlando-magic-sign-moe-wagner-free-agent-center-20210427), 첫 문단 | 10일 계약에서 해제했다고 명시 |
| 5/2 Hall 해제 | [Brazdeikis 영입 발표](https://www.nba.com/magic/orlando-magic-sign-ignas-brazdeikis-10-day-contract-20210502), 첫 문단 | 10일 계약에서 해제했다고 명시 |
| 5/9 Hall 계약 종류 | [Hall 재영입 발표](https://www.nba.com/magic/orlando-magic-sign-donta-hall-remainder-season-20210509), 첫 문단 | 잔여 정규시즌 계약과 당시 NBA hardship 승인 명시 |

5/9 계약 종류는 당시 발표와 구단 가이드가 일치한다. 원역사 라벨의 우선 근거는 이 두 자료로 삼고, 집계 feed의 10일 표시는 원행과 함께 보존한다. feed의 11일치/3해제 누락/1라벨 차이라는 과거 대조 결과를 사후 수정하지 않는다. 집계 자료가 왜 다르게 기재했는지는 확인되지 않았다.

## 적용과 권한

- **FACT:** 위 해제 3건과 5/9 계약·hardship에 관한 당시 구단의 명시적 발표를 회수했다. 기사는 계약 금액을 비공개로 한다. 발표 시각은 리그 접수 시각이 아니다.
- **추론:** 앞선 자료 차이의 원역사 사건·공개 라벨은 당시 발표로 좁힐 수 있다. hardship의 전체 승인 요건이나 잔여 급여는 따로 검증해야 한다.
- **후보:** 대체세계 등록·비용 계산에 이 원역사 자료를 연결할 수 있지만, 실제 실행 인증은 아니다.
- **작가확정:** 새 선택 0. 기존 Hall 5/9 계약 생략과 4월 의무 보존을 따른다. 이 선택의 권위는 작가 결정이며 구단의 원역사 발표가 아니다.

5/9 원역사 hardship을 4월 계약이나 선택 세계에 복사하지 않는다. 4월 기사에서 hardship을 찾지 못했다는 이유로 일반 계약을 법적으로 인증하지도 않는다. 해제는 계약의 미지급 의무 0을 뜻하지 않는다. 기존 53일 명단과 35일 후반 원행은 수정하지 않았다.

이번 4문서는 모두 같은 구단의 발표다. 문서 4개와 독립 발행 주체 4개를 혼동하지 않는다. 전체 등록·Team Salary·적용 규칙은 HOLD, 법적 완료 수 증가 0이다.
