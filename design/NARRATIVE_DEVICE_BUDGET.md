# Narrative Device Budget

- 상태: `FRAMEWORK_LOCKED / ASSIGNMENTS_BLOCKED_BY_NBA_LONG_RANGE_SELECTION`
- 중앙 기준: `novel-writing-skills/skills/writing/NARRATIVE_DEVICES.md`
- 과잉 검수: `novel-writing-skills/skills/writing/UNITY_REVIEW.md`

## 먼저 구분한다

- **Backwards Plotting**: 결말에서 원인을 역산하는 전체 설계법
- **Chekhov's Gun**: 강조한 설치를 실제 선택·위험·보상으로 회수하는 경제성 원칙
- **MacGuffin**: 여러 인물·조직을 움직이는 욕망 대상
- **Hoffman식 Unity**: 장치가 아니라 모든 재료가 중심 질문에 복무하는지 확인하는 삭제 게이트

## 전역 채택

| 항목 | 상태 | 우리 작품의 기능 |
|---|---|---|
| Backwards Plotting | REQUIRED | 파이널의 리바운드→패스에서 역산 |
| Plant-and-Payoff Relationship | PRIMARY | 마지막 패스를 받을 동료와 신뢰를 여러 단계로 축적 |
| Mirroring / Foil | PRIMARY | 주인공과 동료·라이벌의 ‘마지막 선택’ 대비 |
| Historical Dramatic Irony | SECONDARY | 독자가 아는 NBA 역사가 접촉 사건 때문에 달라질 수 있다는 긴장 |
| Callback / Echo | SECONDARY | 첫 리바운드와 마지막 리바운드의 의미 변화 |
| Chekhov Economy | REQUIRED_RULE | 강조한 기술·관계·물건만 회수 의무를 지님 |
| Hoffman Unity | REQUIRED_GATE | 중심 질문을 흐리는 장치·인물·실존 스타 출연 삭제 |

전역 PRIMARY는 2개를 넘기지 않는다. SECONDARY는 해당 Act 질문을 실제로 강화할 때만 활성화한다.

## 기본 비활성

| 장치 | 기본 상태 | 예외 조건 |
|---|---|---|
| MacGuffin | OFF_BY_DEFAULT | 장학 제안·스카우팅 자료·계약권처럼 여러 주체의 욕망과 관계를 실제로 움직일 때만 1개 |
| Red Herring | OFF | 미스터리 장르가 아니므로 원역사 기대만으로 충분 |
| Ticking Clock | LOCAL_ONLY | 등록·선언·트레이드·재활 기한처럼 실제 제도 기한 |
| False Victory | LIMITED | 전체 작품 2~3회 이하, 승리와 대가를 모두 보존 |
| Reversal | LOCAL_ONLY | 인과를 깨지 않고 Sub-Act 상태를 뒤집을 때 |
| Foreshadowing | LIGHT | 정답을 예고하지 않고 가능성과 비용만 심을 때 |
| Escalation | STRUCTURAL | 상대 이름보다 책임·비용·선택의 크기를 올림 |

## 예산

### 작품 전체

- 전역 중심 질문: 1개
- 전역 PRIMARY 장치: 최대 2개
- 전역 SECONDARY 장치: 최대 2개
- 장편 마스터 약속: 동시 활성 최대 5개
- 전 작품 MacGuffin: 기본 0개, 필요해도 1개

### Act

- 주 작법 1~2개
- Act 말에 회수하거나 넘길 장기 약속 1~3개
- 실존 스타 출연은 해당 Act 질문을 바꾸는 경우에만 허용

### Sub-Act

- 주 장치 1개
- 필요할 때만 보조 장치 1개
- `주보상 1 + 보조보상 1 + 장기 씨앗 1`
- 활성 장치가 3개 이상이면 자동 `OVER_BUDGET`

### Episode

장치 이름을 독자에게 설명하지 않는다. 현재 회차에서 활성인 설치·회수만 Context Pack에 싣는다. 장치 0개로 장면이 잘 작동하면 추가하지 않는다.

## 복선·약속 원장

복선은 단순 정보를 맞히는 퀴즈가 아니라 후반 선택의 비용을 바꾸어야 한다.

```yaml
promise_id:
type:
central_question_link:
plant_location:
reader_memory_reason:
reminder_or_variation:
payoff_location:
payoff_changes:
  choice:
  relationship:
  cost:
  reward:
status:
active_window:
source_links:
```

상태는 `PLANNED / PLANTED / REMINDED / VARIED / PAID_OFF / RETIRED / BROKEN`만 사용한다.

## 우리 작품의 마스터 약속 후보

아직 배치하지 않으며 E0·인물 정본 뒤 선택한다.

1. 첫 리바운드에서 공을 잡은 뒤 혼자 끝내려는 선택
2. 공 없는 움직임을 인정하지 않는 초기 믿음
3. 영어는 통하지만 농구의 권력 언어를 오해한 첫 실패
4. 결말 동료와 처음으로 공을 넘기지 못해 발생한 비용
5. 신체 성장으로 기존 슈팅·포지션 감각이 무너지는 사건
6. 독자가 아는 드래프트/시즌 결과가 주인공 접촉으로 처음 갈라지는 순간

여섯 개를 전부 채택하지 않는다. 전체 약속 최대 5개 안에서 중심 질문에 가장 직접적인 것만 선택한다.

## 삭제 질문 — Hoffman Unity

장치·인물·실존 경기마다 묻는다.

1. 현재 Act의 질문을 더 어렵거나 선명하게 만드는가?
2. 주인공의 선택·비용·관계 중 하나를 바꾸는가?
3. 없애면 이야기 기능이 실제로 약해지는가?
4. 유명하거나 멋있다는 이유만으로 전면에 올린 것은 아닌가?

1~3이 모두 아니면 백스테이지로 내리거나 삭제한다.
