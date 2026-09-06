import fs from 'node:fs';

const root = new URL('../', import.meta.url);
const ledgerPath = new URL('simulation/CHICAGO_2019_20_PLAYER_GAME_MINUTE_LEDGER.csv', root);
const vectorPath = new URL('simulation/CHICAGO_2019_20_PLAYER_GAME_DONOR_VECTOR.csv', root);

function parseCsv(path) {
  const lines = fs.readFileSync(path, 'utf8').trim().split(/\r?\n/);
  const header = lines.shift().split(',');
  return lines.map((line) => {
    const values = line.split(',');
    return Object.fromEntries(header.map((key, index) => [key, values[index]]));
  });
}

const ledger = parseCsv(ledgerPath);
const vector = parseCsv(vectorPath);
const fail = (message) => { throw new Error(message); };
const sum = (rows, field) => rows.reduce((total, row) => total + Number(row[field]), 0);

if (ledger.length !== 65) fail(`ledger rows ${ledger.length} != 65`);
if (new Set(ledger.map((row) => row.event_id)).size !== 65) fail('duplicate event_id');
if (new Set(ledger.map((row) => row.game_id)).size !== 65) fail('duplicate game_id');
if (sum(ledger, 'protagonist_seconds') !== 1395 * 60) fail('protagonist total mismatch');
if (sum(ledger, 'protagonist_start') !== 18) fail('protagonist starts mismatch');
if (Math.min(...ledger.map((row) => Number(row.protagonist_seconds))) !== 16 * 60) fail('minimum role mismatch');
if (Math.max(...ledger.map((row) => Number(row.protagonist_seconds))) !== 31 * 60) fail('maximum role mismatch');

const hutchStarts = ledger.filter((row) => row.start_source === 'Chandler Hutchison').length;
const harrisonStarts = ledger.filter((row) => row.start_source === 'Shaquille Harrison').length;
if (hutchStarts !== 10 || harrisonStarts !== 8) fail(`start sources ${hutchStarts}/${harrisonStarts}`);

const actualTeam = sum(ledger, 'actual_team_seconds');
const alternateTeam = sum(ledger, 'alternate_team_seconds');
if (actualTeam !== 940511 || alternateTeam !== actualTeam) fail('season team seconds mismatch');
for (const row of ledger) {
  if (row.actual_team_seconds !== row.alternate_team_seconds) fail(`${row.event_id}: team seconds mismatch`);
  const net = Number(row.real_player_debit_seconds) - Number(row.real_player_credit_seconds);
  if (net !== Number(row.protagonist_seconds)) fail(`${row.event_id}: game debit mismatch`);
}

const deltaByEvent = new Map();
const deltaByPlayer = new Map();
const grossByPlayer = new Map();
for (const row of vector) {
  const actual = Number(row.actual_seconds);
  const alternate = Number(row.alternate_seconds);
  const delta = Number(row.delta_seconds);
  if (alternate - actual !== delta) fail(`${row.event_id}/${row.player}: delta mismatch`);
  if (alternate < 0) fail(`${row.event_id}/${row.player}: negative minute`);
  deltaByEvent.set(row.event_id, (deltaByEvent.get(row.event_id) ?? 0) + delta);
  deltaByPlayer.set(row.player, (deltaByPlayer.get(row.player) ?? 0) + delta);
  const gross = grossByPlayer.get(row.player) ?? { debit: 0, credit: 0 };
  if (delta < 0) gross.debit -= delta;
  if (delta > 0) gross.credit += delta;
  grossByPlayer.set(row.player, gross);
}
for (const row of ledger) {
  if (deltaByEvent.get(row.event_id) !== -Number(row.protagonist_seconds)) {
    fail(`${row.event_id}: vector does not fund protagonist`);
  }
}

const expectedDebit = new Map([
  ['Chandler Hutchison', 31608], ['Denzel Valentine', 15600],
  ['Shaquille Harrison', 14400], ['Ryan Arcidiacono', 8400],
  ['Adam Mokoka', 5400], ['Max Strus', 374], ['Thaddeus Young', 7918],
]);
for (const [player, seconds] of expectedDebit) {
  if (deltaByPlayer.get(player) !== -seconds) fail(`${player}: season debit mismatch`);
}

const protectedPlayers = [
  'Zach LaVine', 'Tomas Satoransky', 'Coby White', 'Lauri Markkanen',
  'Kris Dunn', 'Wendell Carter Jr.', 'Otto Porter Jr.', 'Daniel Gafford',
  'Luke Kornet', 'Cristiano Felicio',
];
for (const player of protectedPlayers) {
  if ((deltaByPlayer.get(player) ?? 0) !== 0) fail(`${player}: protected net changed`);
}
for (const player of ['Wendell Carter Jr.', 'Daniel Gafford', 'Luke Kornet', 'Cristiano Felicio']) {
  if (grossByPlayer.has(player)) fail(`${player}: center game minute changed`);
}
for (const player of ['Zach LaVine', 'Tomas Satoransky', 'Coby White', 'Otto Porter Jr.']) {
  if (grossByPlayer.has(player)) fail(`${player}: protected game minute changed`);
}
const bridgeDebit = ['Lauri Markkanen', 'Kris Dunn']
  .reduce((total, player) => total + (grossByPlayer.get(player)?.debit ?? 0), 0);
const bridgeCredit = ['Lauri Markkanen', 'Kris Dunn']
  .reduce((total, player) => total + (grossByPlayer.get(player)?.credit ?? 0), 0);
if (bridgeDebit !== 19 * 60 + 34 || bridgeCredit !== bridgeDebit) fail('protected bridge mismatch');

console.log('PASS Chicago 2019-20 player-game ledger');
console.log('protagonist: 65 GP, 18 GS, 1395:00');
console.log(`start sources: Hutchison ${hutchStarts}, Harrison ${harrisonStarts}`);
console.log('team minutes: 15675:11 preserved across 65 games');
console.log('protected season net: 0; Markkanen/Dunn gross bridge: 19:34 each way');
