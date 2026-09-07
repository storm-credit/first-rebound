import fs from 'node:fs';

const root = new URL('../', import.meta.url);
const ledgerPath = new URL('simulation/CHICAGO_2020_21_PREDEADLINE_MINUTE_LEDGER.csv', root);
const vectorPath = new URL('simulation/CHICAGO_2020_21_PREDEADLINE_DONOR_VECTOR.csv', root);
const budgetPath = new URL('simulation/CHICAGO_2020_21_PREDEADLINE_PLAYER_BUDGET.csv', root);
const designPath = new URL('simulation/CHICAGO_2020_21_PREDEADLINE_PLAYER_GAME.md', root);
const reviewPath = new URL('reviews/R01_CHICAGO_2020_21_PREDEADLINE_PLAYER_GAME_REVIEW.md', root);

function parseCsv(path) {
  const lines = fs.readFileSync(path, 'utf8').trim().split(/\r?\n/);
  const header = lines.shift().split(',');
  return lines.map((line) => {
    const values = line.split(',');
    return Object.fromEntries(header.map((key, index) => [key, values[index]]));
  });
}

const fail = (message) => { throw new Error(message); };
const sum = (rows, field) => rows.reduce((total, row) => total + Number(row[field]), 0);
const ledger = parseCsv(ledgerPath);
const vector = parseCsv(vectorPath);
const budget = parseCsv(budgetPath);

if (ledger.length !== 43) fail(`ledger rows ${ledger.length} != 43`);
if (new Set(ledger.map((row) => row.event_id)).size !== 43) fail('duplicate event_id');
if (new Set(ledger.map((row) => row.game_id)).size !== 43) fail('duplicate game_id');
if (ledger[0].date !== '2020-12-23' || ledger.at(-1).date !== '2021-03-24') fail('pre-deadline date boundary changed');
if (ledger.filter((row) => row.actual_wl === 'W').length !== 19 || ledger.filter((row) => row.actual_wl === 'L').length !== 24) fail('actual 19-24 baseline changed');

if (sum(ledger, 'protagonist_seconds') !== 73_140) fail('protagonist 1,219-minute target changed');
if (sum(ledger, 'lamelo_seconds') !== 71_460) fail('LaMelo 1,191-minute target changed');
if (sum(ledger, 'protagonist_start') !== 43) fail('protagonist starts changed');
if (sum(ledger, 'lamelo_start') !== 25) fail('LaMelo starts changed');
if (ledger.filter((row) => row.protagonist_start_source === 'Patrick Williams').length !== 42) fail('Patrick start-source count changed');
if (ledger.filter((row) => row.protagonist_start_source === 'Garrett Temple').length !== 1) fail('Temple start-source count changed');
if (ledger.filter((row) => row.lamelo_start_source === 'Coby White').length !== 18) fail('Coby start-source count changed');
if (ledger.filter((row) => row.lamelo_start_source === 'Tomas Satoransky').length !== 7) fail('Satoransky start-source count changed');

const actualTeam = sum(ledger, 'actual_team_seconds');
const alternateTeam = sum(ledger, 'alternate_team_seconds');
if (actualTeam !== 625_202 || alternateTeam !== actualTeam) fail('43-game team seconds changed');
for (const row of ledger) {
  if (row.actual_team_seconds !== row.alternate_team_seconds) fail(`${row.event_id}: team seconds mismatch`);
  const net = Number(row.real_player_debit_seconds) - Number(row.real_player_credit_seconds);
  if (net !== Number(row.protagonist_seconds) + Number(row.lamelo_seconds)) fail(`${row.event_id}: ledger funding mismatch`);
}

const deltaByEvent = new Map();
const startDeltaByEvent = new Map();
const deltaByPlayer = new Map();
const grossByPlayer = new Map();
for (const row of vector) {
  const actual = Number(row.actual_seconds);
  const alternate = Number(row.alternate_seconds);
  const delta = Number(row.delta_seconds);
  if (alternate - actual !== delta) fail(`${row.event_id}/${row.player}: delta mismatch`);
  if (alternate < 0) fail(`${row.event_id}/${row.player}: negative alternate minute`);
  deltaByEvent.set(row.event_id, (deltaByEvent.get(row.event_id) ?? 0) + delta);
  startDeltaByEvent.set(row.event_id, (startDeltaByEvent.get(row.event_id) ?? 0) + Number(row.alternate_start) - Number(row.actual_start));
  deltaByPlayer.set(row.player, (deltaByPlayer.get(row.player) ?? 0) + delta);
  const gross = grossByPlayer.get(row.player) ?? { debit: 0, credit: 0 };
  if (delta < 0) gross.debit -= delta;
  if (delta > 0) gross.credit += delta;
  grossByPlayer.set(row.player, gross);
  const floors = new Map([
    ['Tomas Satoransky', 600], ['Denzel Valentine', 360], ['Ryan Arcidiacono', 0],
    ['Coby White', 1200], ['Garrett Temple', 960], ['Otto Porter Jr.', 720],
  ]);
  if (delta < 0 && floors.has(row.player) && alternate < floors.get(row.player)) fail(`${row.event_id}/${row.player}: donor floor violated`);
}
for (const row of ledger) {
  const fiction = Number(row.protagonist_seconds) + Number(row.lamelo_seconds);
  if (deltaByEvent.get(row.event_id) !== -fiction) fail(`${row.event_id}: vector does not fund fictional players`);
  const newStarts = Number(row.protagonist_start) + Number(row.lamelo_start);
  if (startDeltaByEvent.get(row.event_id) !== -newStarts) fail(`${row.event_id}: five-start conservation failed`);
}

const expectedDelta = new Map([
  ['Patrick Williams', -71_570], ['Chandler Hutchison', -3_815],
  ['Tomas Satoransky', -19_800], ['Denzel Valentine', -21_600],
  ['Ryan Arcidiacono', -8_362], ['Coby White', -13_200],
  ['Garrett Temple', -4_838], ['Otto Porter Jr.', -1_415],
  ['Thaddeus Young', 0],
]);
for (const [player, delta] of expectedDelta) {
  if (deltaByPlayer.get(player) !== delta) fail(`${player}: season delta changed`);
}
if (grossByPlayer.get('Thaddeus Young')?.debit !== 38 || grossByPlayer.get('Thaddeus Young')?.credit !== 38) fail('Young net-zero bridge changed');
for (const player of ['Wendell Carter Jr.', 'Daniel Gafford', 'Luke Kornet', 'Cristiano Felicio']) {
  if (grossByPlayer.has(player)) fail(`${player}: center minute changed`);
}

const byBudgetPlayer = new Map(budget.map((row) => [row.player, row]));
if (sum(budget.filter((row) => !['Protagonist', 'LaMelo Ball'].includes(row.player)), 'actual_seconds') !== actualTeam) fail('budget actual seconds mismatch');
if (sum(budget, 'alternate_seconds') !== actualTeam) fail('budget alternate seconds mismatch');
if (sum(budget.filter((row) => !['Protagonist', 'LaMelo Ball'].includes(row.player)), 'actual_gs') !== 215) fail('actual starts != 215');
if (sum(budget, 'alternate_gs') !== 215) fail('alternate starts != 215');
if (byBudgetPlayer.get('Protagonist')?.alternate_gp !== '43' || byBudgetPlayer.get('Protagonist')?.alternate_gs !== '43') fail('protagonist budget role changed');
if (byBudgetPlayer.get('LaMelo Ball')?.alternate_gp !== '43' || byBudgetPlayer.get('LaMelo Ball')?.alternate_gs !== '25') fail('LaMelo budget role changed');
if (byBudgetPlayer.get('Coby White')?.alternate_seconds !== '68524') fail('Coby retained-minute floor changed');
if (byBudgetPlayer.get('Thaddeus Young')?.actual_gp !== byBudgetPlayer.get('Thaddeus Young')?.alternate_gp) fail('Young bridge created a new appearance');

const design = fs.readFileSync(designPath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of ['PLAYER_GAME_CONSERVATION_PASS', '43경기·43선발·1,219분', '43경기·25선발·1,191분', '1,153분 35초']) {
  if (!design.includes(marker)) fail(`missing design marker: ${marker}`);
}
if (!review.includes('PASS_FOR_PREDEADLINE_ROLE_PROVISIONAL_LOCK')) fail('missing review disposition');
if (!review.includes('생산성·승패·거래 발생은 계속 `HOLD`')) fail('missing downstream hold');

console.log('PASS Chicago 2020-21 pre-deadline player-game ledger');
console.log('actual baseline: 43 games / 19-24 / 10,420:02 / 215 starts');
console.log('protagonist: 43 GP / 43 GS / 1,219:00');
console.log('LaMelo: 43 GP / 25 GS / 1,191:00');
console.log('secondary donor net: 1,153:35; Young gross bridge: 0:38 each way');
