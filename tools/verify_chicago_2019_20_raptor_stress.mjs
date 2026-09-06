import fs from 'node:fs';

const root = new URL('../', import.meta.url);
const parseCsv = (relative) => {
  const lines = fs.readFileSync(new URL(relative, root), 'utf8').trim().split(/\r?\n/);
  const header = lines.shift().split(',');
  return lines.map((line) => Object.fromEntries(header.map((key, index) => [key, line.split(',')[index]])));
};
const fail = (message) => { throw new Error(message); };

const cohort = parseCsv('simulation/CHICAGO_2019_20_SOPHOMORE_RAPTOR_COHORT.csv');
const values = cohort.map((row) => Number(row.raptor_total)).sort((a, b) => a - b);
if (cohort.length !== 9) fail(`cohort ${cohort.length}`);
if (Math.abs(values[2] - (-2.709159851)) > 1e-9) fail('Q1 anchor');
if (Math.abs(values[4] - (-1.803876459)) > 1e-9) fail('median anchor');
if (Math.abs(values[6] - (-0.952511110)) > 1e-9) fail('Q3 anchor');

const priors = parseCsv('simulation/CHICAGO_2019_20_RAPTOR_PRIORS.csv');
if (priors.map((row) => `${row.scenario}:${row.protagonist_rating}`).join('/') !== 'LOW:-2.7/BASE:-1.8/HIGH:-1.0') fail('RAPTOR priors');

const ledger = parseCsv('simulation/CHICAGO_2019_20_RAPTOR_OUTCOME_LEDGER.csv');
if (ledger.length !== 65 * 3 * 3) fail(`RAPTOR ledger ${ledger.length}`);
const expectedPrimary = {
  '0/LOW': 20, '0/BASE': 21, '0/HIGH': 22,
  '0.5/LOW': 20, '0.5/BASE': 21, '0.5/HIGH': 21,
  '1/LOW': 20, '1/BASE': 21, '1/HIGH': 21,
};
for (const [key, wins] of Object.entries(expectedPrimary)) {
  const [fatigue, scenario] = key.split('/');
  const rows = ledger.filter((row) => row.fatigue_penalty === fatigue && row.scenario === scenario);
  if (rows.length !== 65) fail(`${key} rows ${rows.length}`);
  if (rows.filter((row) => row.alt_wl === 'W').length !== wins) fail(`${key} wins`);
}
if (ledger.filter((row) => row.flip === '1').some((row) => Math.abs(Number(row.actual_margin)) > 2)) fail('RAPTOR flip beyond two-point game');

const sensitivity = parseCsv('simulation/CHICAGO_2019_20_REGULARIZER_SENSITIVITY.csv');
if (sensitivity.length !== 4 * 3 * 3) fail(`sensitivity ${sensitivity.length}`);
const winSet = [...new Set(sensitivity.map((row) => Number(row.wins)))].sort((a, b) => a - b);
if (winSet.join('/') !== '19/20/21/22') fail(`RAPTOR sensitivity wins ${winSet.join('/')}`);

const earlier = parseCsv('simulation/CHICAGO_2019_20_OUTCOME_LEDGER.csv');
const centralEarlier = earlier.filter((row) => row.scenario === 'BASE');
const centralWins = new Set();
for (const field of ['base_alt_wl', 'fatigue_05_alt_wl', 'fatigue_10_alt_wl']) {
  for (const proxy of ['BPM', 'NET_EB']) {
    centralWins.add(centralEarlier.filter((row) => row.proxy === proxy && row[field] === 'W').length);
  }
}
for (const fatigue of ['0', '0.5', '1']) {
  centralWins.add(ledger.filter((row) => row.scenario === 'BASE' && row.fatigue_penalty === fatigue && row.alt_wl === 'W').length);
}
if ([...centralWins].sort((a, b) => a - b).join('/') !== '21/22') fail('combined central set');

console.log('PASS Chicago 2019-20 RAPTOR crosscheck');
console.log('RAPTOR_EB-1000: 20/21/22 wins; regularizer stress: 19-22');
console.log('combined BASE families: 21-22 wins, lottery seed 7');
console.log('exact wins and lottery author choice remain HOLD');
