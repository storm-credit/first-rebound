import fs from 'node:fs';

const root = new URL('../', import.meta.url);
const parseCsv = (relative) => {
  const lines = fs.readFileSync(new URL(relative, root), 'utf8').trim().split(/\r?\n/);
  const header = lines.shift().split(',');
  return lines.map((line) => Object.fromEntries(header.map((key, index) => [key, line.split(',')[index]])));
};
const fail = (message) => { throw new Error(message); };
const median = (values) => {
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[(sorted.length - 1) / 2];
};

const cohort = parseCsv('simulation/CHICAGO_2019_20_SOPHOMORE_WING_COHORT.csv');
if (cohort.length !== 9) fail(`cohort size ${cohort.length}`);
const expectedMedians = {
  pts36: 12.8, reb36: 6.2, ast36: 2.7, stl36: 1.4, blk36: 0.5,
  tov36: 2.0, pf36: 3.2, ts: 0.524, three_pa36: 3.6,
  three_p: 0.333, usg: 0.165, net_rating: -4.7,
};
for (const [field, expected] of Object.entries(expectedMedians)) {
  const actual = median(cohort.map((row) => Number(row[field])));
  if (actual !== expected) fail(`${field} median ${actual} != ${expected}`);
}

const priors = parseCsv('simulation/CHICAGO_2019_20_PRODUCTION_PRIORS.csv');
if (priors.map((row) => row.scenario).join('/') !== 'LOW/BASE/HIGH') fail('scenario order');
for (const field of ['pts36', 'reb36', 'ast36', 'stl36', 'blk36', 'ts', 'three_pa36', 'three_p', 'usg']) {
  const values = priors.map((row) => Number(row[field]));
  if (!(values[0] <= values[1] && values[1] <= values[2])) fail(`${field} range order`);
}
for (const field of ['tov36', 'pf36']) {
  const values = priors.map((row) => Number(row[field]));
  if (!(values[0] >= values[1] && values[1] >= values[2])) fail(`${field} inverse range order`);
}
const minutes = 1395;
const games = 65;
const totalFields = {pts36: 'season_pts', reb36: 'season_reb', ast36: 'season_ast', stl36: 'season_stl', blk36: 'season_blk'};
const gameFields = {pts36: 'ppg', reb36: 'rpg', ast36: 'apg', stl36: 'spg', blk36: 'bpg'};
for (const row of priors) {
  for (const [rate, total] of Object.entries(totalFields)) {
    const expected = Number((Number(row[rate]) * minutes / 36).toFixed(2));
    if (Number(row[total]) !== expected) fail(`${row.scenario}/${total}`);
  }
  for (const [rate, perGame] of Object.entries(gameFields)) {
    const expected = Number((Number(row[rate]) * minutes / 36 / games).toFixed(2));
    if (Number(row[perGame]) !== expected) fail(`${row.scenario}/${perGame}`);
  }
  if (row.impact_status !== 'HOLD') fail(`${row.scenario}: impact prematurely opened`);
}

const roster = parseCsv('simulation/CHICAGO_2019_20_ROSTER_BASELINE.csv');
const rosterByPlayer = new Map(roster.map((row) => [row.player, row]));
const transfer = parseCsv('simulation/CHICAGO_2019_20_TRANSFER_PRODUCTION.csv');
const expectedDebits = new Map([
  ['Chandler Hutchison', 31608], ['Denzel Valentine', 15600],
  ['Shaquille Harrison', 14400], ['Ryan Arcidiacono', 8400],
  ['Adam Mokoka', 5400], ['Max Strus', 374], ['Thaddeus Young', 7918],
]);
if (transfer.reduce((total, row) => total + Number(row.net_debit_seconds), 0) !== 1395 * 60) fail('transfer total');
for (const row of transfer) {
  const base = rosterByPlayer.get(row.player);
  if (!base) fail(`${row.player}: absent from roster`);
  if (Number(row.net_debit_seconds) !== expectedDebits.get(row.player)) fail(`${row.player}: debit mismatch`);
  const share = Number(row.net_debit_seconds) / Number(base.seconds);
  if (Math.abs(Number(row.share) - share) > 5e-10) fail(`${row.player}: share mismatch`);
  for (const stat of ['pts', 'reb', 'ast', 'stl', 'blk']) {
    const expected = Number(base[stat]) * share;
    if (Math.abs(Number(row[`${stat}_removed`]) - expected) > 0.0001) fail(`${row.player}/${stat}`);
  }
}

console.log('PASS Chicago 2019-20 production priors');
console.log('longitudinal sophomore wing cohort: 9');
console.log('protagonist: LOW/BASE/HIGH over 65 GP and 1395:00');
console.log('transfer production: 1395:00 verified; impact remains HOLD');
