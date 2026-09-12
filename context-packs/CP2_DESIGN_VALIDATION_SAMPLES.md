# CP2 설계 검증 샘플

- [파생 JSON](CP2_DESIGN_VALIDATION_SAMPLES.json): A06-S3(2021 잠정 결산 연결), A13-S3(결말 기능과 선행 신뢰).
- 상태: `DESIGN_VALIDATION_ONLY_NOT_EPISODE_PACK`. 실제 회차 팩0개·원고0개. [Context Pack 규약](README.md)의 CLOSED 상태 샘플 허용 범위다.
- 기반 커밋은 PR #167의 `8bd0cc8a9aefeda72e4683a35bceba646f3a50a2`. 새 설계 파일까지 해당 기반 커밋에 들어 있었다는 뜻은 아니다. 같은 변경 묶음의 실제 내용을 `source_content_sha256`로 고정한다. 따라서 기반 커밋+개별 내용 해시가 생성 버전이다.
- 먼저 `python tools/build_cp2_design_packets.py --check`로 검사한다. 정본/설계가 바뀌면 `STALE` 오류가 나며, 근거 검토 없이 builder를 돌려 오류를 숨기지 않는다. 검토된 변경만 기본 builder로 새 해시를 생성한다.

| 샘플 | 검증할 기능 | 원고에 넘기지 않을 HOLD |
|---|---|---|
| CP2-A06-S3 | K1/L2/M 결과의 조건부 연결과 실제 사실 분리 | 건강·등록·charge, 전체 소유권/선수 지명 |
| CP2-A13-S3 | 승인된 결말 기능, RC1 선행 상호 비용과 활성 약속 | 2028 대진·시간·점수·잔류·의학·패스 각도 |

이 샘플이 통과해도 사건의 전술적 성공이나 사실 인증이 되는 것은 아니다. 소설 문장·대사·집필 지시를 넣지 않는다. Pack과 정본이 충돌하면 정본이 우선한다.
