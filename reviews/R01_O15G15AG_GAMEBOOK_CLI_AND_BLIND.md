# R01 — G15AG 개막 공식 경기 기록 제한 검수

- 시작 권위 `main` `885deb9`, 대상 [G15AG](../research/O15G15AG_DETROIT_2021_OPENING_GAMEBOOK_WITNESS.md). G16/G17 통과가 아니다.
- **Codex 직접 자료:** [NBA 공식 10/20 CHI@DET 경기 기록 PDF 첫 페이지](https://statsdmz.nba.com/pdfs/20211020/20211020_CHIDET_book.pdf)를 직접 받아 `FINAL BOX`의 Detroit 선발5·교체5·DNP4·inactive3 = 고유17명을 읽었다. [Detroit 10/5 Smith 투웨이](https://www.nba.com/pistons/preseason-primer-cunninghams-ankle-likely-hold-him-out-pistons-opener-casey-says), [10/13 Pickett 투웨이](https://www.nba.com/pistons/features/minus-3-starters-pistons-go-cold-2nd-half-and-come-short-new-york)를 따로 대조했다. PDF 자체는 계약 유형을 표시하지 않는다.
- **Antigravity CLI 1.2.11:** 같은 공식 PDF URL에 읽기 전용 `read_url_content`/`view_file` 요청을 보냈지만 `print timeout after 45s`, 결과 `response:""`·`num_turns=1`; 저장 본문·최종 답변 모두 없음. `status:SUCCESS`만으로 읽기 성공으로 세지 않는다. 이번 AG 직접 PDF 증거 **0건**.
- **NotebookLM CLI:** 공식 PDF를 기존 작업실 `303ffd55-e019-476a-9ae3-8dc0e32fe11f`에 파일 소스 `b72843bd-c88e-442a-a472-b5ad4d4202ff`로 추가했다. **그 소스 하나만** 지정한 질의에서 17명과 5/5/4/3 분류를 반환하고, PDF에는 계약 유형이 없다고 답했다. Codex가 읽은 **동일 PDF**의 분석이며 독립 원자료 한 건을 추가한 것이 아니다.
- **Claude CLI source-blind:** 문서 초안만 본 무도구 검토는 9/29 투웨이 상태를 10/20로 자동 연장할 위험을 유효하게 지적했다. 10/5 Smith·10/13 Pickett 구단 자료를 추가하고 `17−2=15`를 교차 출처 **추론**으로 명시했다. DNP/inactive 자체가 계약 종류를 증명하지 않는다는 지적도 반영했다. Cade/Livers 부상 사유가 PDF에 없다는 의심은 공식 inactive 행에 직접 표기되어 기각했다. Claude는 PDF나 구단 사이트를 직접 읽지 않았다.
- **기계 검산:** `python tools/check_o15g15ag_detroit_gamebook.py`는 경기 기록 이름 17개가 중복 없고, 구단 출처상 투웨이 두 이름을 빼면 G15AF 원역사 이름 집합 15개와 일치하는지 확인한다. 계약 유형·급여·대체세계 실행을 기계가 독립 인증하지 않는다.

**맹점:** 10/20 당일 공식 계약 원장 원본은 여전히 없다. 이름 일치가 P0-B Plumlee/Olynyk 동시 보유나 G14 분·승패를 증명하지 않는다. 같은 PDF를 Codex·NotebookLM이 읽었다고 독립 출처 2건으로 세지 않는다. 신규 작가확정 0건, 설계/원고 `CLOSED`.
