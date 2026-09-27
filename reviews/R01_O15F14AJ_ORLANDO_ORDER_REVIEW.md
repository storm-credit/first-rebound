# R01 — Orlando 거래일 순서 화면 반증 수렴

- 2026-09-28, Claude CLI `-p --allowedTools Read`로 AJ 문서·JSON·빌더와 상류 장부를 읽는 **문서 한정 반증**을 실행했다. 파일 수정 권한은 주지 않았다. 별도 source-blind 입력에는 결론·검토 이력·파일을 주지 않고 시나리오와 두 수치열만 제공했다. 첫 PowerShell 호출은 `$`가 변수 확장되어 금액 앞자리가 빠졌으므로 **무효로 제외**했고, 숫자를 달러 기호 없이 다시 전달한 두 번째 결과만 사용한다. 전체 G16 독립 검수와 별개다.
- Codex는 두 급여 열의 산술과 [2017 CBA VII §6(j)(1)(iii), §6(m)(3)(A)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)을 직접 다시 대조했다. 두 도구의 같은 문서 재독은 새 원자료 2건이 아니다.

| Claude 지적 | 판정·처리 |
|---|---|
| 처음 표가 unlikely 보너스를 넣은 apron 부담을 일반 세금선에도 대조 | **수용.** 일반 급여는 기본급+likely, apron 시험은 공개 unlikely 전액 포함으로 분리했다. 기존 `Gordon 먼저 일반 급여가 세금선 초과` 문장을 철회. CBA §6(j)의 post-assignment Team Salary와 §6(m)(3)의 조정 Team Salary는 같은 숫자가 아니다. |
| unlikely 보너스를 apron에도 빼야 하므로 `$76,411` 사례가 사라진다 | **기각.** CBA VII §6(m)(3)(A)은 일반 Salary에서 빠진 성과 보너스를 해당 apron 계산에 **포함**한다. SalarySwish의 `reported_cap_hit` 열은 일반 급여 대조에 사용하되 apron 정의를 대체하지 않는다. |
| Mozgov 분산분 누락 | **부분 수용.** 기존 L 원장에는 2019 리그 제외 승인 **보도**가 있으며 동일 경로 유지 조건에서는 기계적 재가산하지 않는다. 새 문서에 이 전제와 대체 세계 인증 부재를 명시했다. Mozgov가 반드시 추가 부채라는 주장은 근거 부족. |
| `$76,411` 음수는 Birch `$413,964` 보수화 하나보다 작다 | **수용.** 음수 사례를 실재 위반이나 의미 있는 안전 한도로 사용하지 않고 민감도 예시로 낮췄다. 0보장 캠프 4명의 연간 전액도 실제 charge가 아니다. |
| Teague의 4월/방출 후 비용을 3/25 취득 charge와 같다고 확정 | **수용.** 동일 값 재사용의 잠정 성격을 명시하고 실제 3/25 incoming charge는 null로 둔다. |
| 기존 4월 JSON과의 일치를 독립 검증으로 읽을 수 있음 | **수용.** 같은 소스의 내부 일관성 검사로 재표기했다. |
| Fournier 먼저의 낮은 중간 금액은 급여 차이의 산술 필연 | **수용.** 우월한 역사 근거나 작가확정으로 쓰지 않는다. |
| Gordon/Clark/Fournier 입력 드리프트와 Windows 경로 | **수용.** 세 outgoing 입력의 예상값 guard를 추가하고 JSON 출처 경로를 POSIX 형태로 고정했다. |

재현 스크립트와 JSON 검산 후 실제 F2는 계속 `HOLD`. 후속 검증 대상은 정확 리그 Team Salary·apron 정의에 따른 모든 조정·hard-cap 발생·실제 거래 승인 순서·당일 Teague 차지다. 이 제한 검토는 F1~F5 `0/5`, A `0/3`, K `0/4`, freeze/CLOSED를 바꾸지 않는다.

## 결론 비제공 source-blind 검문

두 번째 Claude 출력은 (1) Teague의 동일한 일반/조정 비용에 깔린 보너스 부재 가정, (2) Fournier 순액의 선수·픽 분해 및 두 거래의 독립성, (3) hard-cap 발동, (4) 거래 전 구성과 대체 Nnaji 급여의 지명 순번 의존을 질문했다. **수용:** Teague 보너스 부재를 인증으로 쓰지 않도록 AJ에 명시했고, hard-cap/당일 charge·거래 순서는 기존 정확 필드에 남겼다. **이미 표기됨:** AJ는 Fournier `$17.45m`→Teague 잠정 `$1.620564m`, 별도 Gordon 거래, Vučević/Aminu를 포함한 11명+Birch, 대체 24순위·120% Nnaji를 조건부 입력으로 밝힌다. 두 2R 권리는 선수 계약 급여를 뜻하지 않으나 픽 가용성은 F2 HOLD다. **기각:** source-blind 출력의 apron용 조정 급여 `$134,863,784`를 일반 세금선과 직접 비교한 문장은 CBA 정의를 섞는다. 이를 새로운 발견이나 위반 근거로 쓰지 않는다.
