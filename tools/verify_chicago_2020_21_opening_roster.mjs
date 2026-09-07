import fs from 'node:fs';

const rosterPath = new URL('../simulation/CHICAGO_2020_21_ROSTER_MINUTE_BASELINE.csv', import.meta.url);
const priorPath = new URL('../simulation/CHICAGO_2020_21_ROLE_MINUTE_PRIOR.csv', import.meta.url);
const baselinePath = new URL('../research/CHICAGO_2020_21_OPENING_ROSTER_BASELINE.md', import.meta.url);
const rolePath = new URL('../simulation/CHICAGO_2020_21_ROLE_ARCHITECTURE.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_CHICAGO_2020_21_OPENING_ROSTER_REVIEW.md', import.meta.url);

function parseCsv(path) {
  const lines = fs.readFileSync(path, 'utf8').trim().split(/\r?\n/);
  const header = lines.shift().split(',');
  return lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
}

const rows = parseCsv(rosterPath);
const opening = rows.filter((row) => row.phase === 'OPENING');
const midseason = rows.filter((row) => row.phase === 'MIDSEASON');
const actualStandard = opening.filter((row) => row.actual_contract_class === 'STANDARD');
const actualTwoWay = opening.filter((row) => row.actual_contract_class === 'TWO_WAY');
const rivalStandard = opening.filter((row) => row.rival_world_contract_class === 'STANDARD');
const rivalTwoWay = opening.filter((row) => row.rival_world_contract_class === 'TWO_WAY');

if (opening.length !== 17) throw new Error(`expected 17 opening players, got ${opening.length}`);
if (actualStandard.length !== 15 || actualTwoWay.length !== 2) throw new Error('actual opening roster is not 15+2');
if (rivalStandard.length !== 15 || rivalTwoWay.length !== 2) throw new Error('rival-world opening roster is not 15+2');
if (midseason.length !== 5) throw new Error(`expected five actual midseason additions, got ${midseason.length}`);

const hutchison = opening.find((row) => row.actual_player === 'Chandler Hutchison');
const patrick = opening.find((row) => row.actual_player === 'Patrick Williams');
if (hutchison?.rival_world_player !== 'Protagonist' || hutchison?.rival_world_disposition !== 'DIRECT_2018_SLOT_REPLACEMENT') throw new Error('Hutchison replacement changed');
if (patrick?.rival_world_player !== 'LaMelo Ball' || patrick?.rival_world_disposition !== 'DIRECT_PICK4_REPLACEMENT') throw new Error('Patrick replacement changed');

const minutes = rows.reduce((sum, row) => sum + Number(row.actual_minutes), 0);
const starts = rows.reduce((sum, row) => sum + Number(row.actual_gs), 0);
if (minutes !== 17380) throw new Error(`actual team minutes changed: ${minutes}`);
if (starts !== 360) throw new Error(`actual starts changed: ${starts}`);

const priors = parseCsv(priorPath);
const protagonist = priors.find((row) => row.player === 'Protagonist');
const lamelo = priors.find((row) => row.player === 'LaMelo Ball');
const baseCombined = Number(protagonist.total_minutes_base) + Number(lamelo.total_minutes_base);
const directRemoved = Number(hutchison.actual_minutes) + Number(patrick.actual_minutes);
if (baseCombined !== 3698) throw new Error(`base combined minutes changed: ${baseCombined}`);
if (directRemoved !== 2047) throw new Error(`direct removed pool changed: ${directRemoved}`);
if (baseCombined - directRemoved !== 1651) throw new Error('secondary donor requirement changed');

const baseline = fs.readFileSync(baselinePath, 'utf8');
const role = fs.readFileSync(rolePath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of [
  'EVIDENCE_BASELINE_PASS / 15_PLUS_2_STRUCTURE_PASS / DEADLINE_EVENTS_HOLD',
  '표준계약 15명 + 투웨이 2명',
  '3,698 - 2,047 = 1,651분',
  'INJURY_EVENT_HOLD',
  '원형 그대로 법적으로 발생할 수 없다',
]) {
  if (!baseline.includes(marker)) throw new Error(`missing baseline firewall: ${marker}`);
}
if (!role.includes('STAGED_STARTING_SEQUENCE_PROVISIONAL_BASE')) throw new Error('missing staged role status');
if (!role.includes('다음은 작가 선택이 아니라 계산 단계')) throw new Error('missing calculation-only next gate');
if (!review.includes('PLAYER_GAME_BLOCKER')) throw new Error('missing player-game blocker');
if (!review.includes('exact 승수와 두 마감일 거래는 계속 `HOLD`')) throw new Error('missing deadline hold');

console.log('PASS Chicago 2020-21 opening roster baseline');
console.log('actual and rival-world opening roster: 15 standard + 2 two-way');
console.log('actual totals: 17,380 minutes / 360 starts');
console.log('provisional BASE: 3,698 minutes; secondary donor requirement: 1,651');
