import fs from 'node:fs';

const root = new URL('../', import.meta.url);
const parseCsv = (relative) => {
  const lines = fs.readFileSync(new URL(relative, root), 'utf8').trim().split(/\r?\n/);
  const header = lines.shift().split(',');
  return lines.map((line) => Object.fromEntries(header.map((key, index) => [key, line.split(',')[index]])));
};
const fail = (message) => { throw new Error(message); };

const games = parseCsv('simulation/CHICAGO_2019_20_GAME_MARGIN_BASELINE.csv');
const minuteLedger = parseCsv('simulation/CHICAGO_2019_20_PLAYER_GAME_MINUTE_LEDGER.csv');
const outcomes = parseCsv('simulation/CHICAGO_2019_20_OUTCOME_LEDGER.csv');
const priors = parseCsv('simulation/CHICAGO_2019_20_IMPACT_PRIORS.csv');
const impactInputs = parseCsv('simulation/CHICAGO_2019_20_IMPACT_INPUTS.csv');

if (games.length !== 65) fail(`margin games ${games.length}`);
if (new Set(games.map((row) => row.event_id)).size !== 65) fail('duplicate margin event');
if (games.filter((row) => row.actual_wl === 'W').length !== 22) fail('actual wins not 22');
if (games.filter((row) => Number(row.actual_margin) > 0).length !== 22) fail('actual margin wins not 22');
for (let index = 0; index < games.length; index += 1) {
  for (const field of ['event_id', 'game_id', 'date', 'matchup', 'actual_wl']) {
    if (games[index][field] !== minuteLedger[index][field]) fail(`${field} join mismatch at ${index}`);
  }
}

if (priors.length !== 6) fail(`prior rows ${priors.length}`);
if (impactInputs.length !== 9) fail(`impact input rows ${impactInputs.length}`);
if (outcomes.length !== 65 * 6) fail(`outcome rows ${outcomes.length}`);

const expected = {
  'BPM/LOW': [21, 21, 21],
  'BPM/BASE': [22, 21, 21],
  'BPM/HIGH': [22, 22, 22],
  'NET_EB/LOW': [22, 21, 21],
  'NET_EB/BASE': [22, 22, 22],
  'NET_EB/HIGH': [24, 24, 24],
};
const fields = ['base_alt_wl', 'fatigue_05_alt_wl', 'fatigue_10_alt_wl'];
for (const [key, counts] of Object.entries(expected)) {
  const [proxy, scenario] = key.split('/');
  const subset = outcomes.filter((row) => row.proxy === proxy && row.scenario === scenario);
  if (subset.length !== 65) fail(`${key} rows ${subset.length}`);
  fields.forEach((field, index) => {
    const actual = subset.filter((row) => row[field] === 'W').length;
    if (actual !== counts[index]) fail(`${key}/${field} ${actual} != ${counts[index]}`);
  });
}

const b2b = [...new Set(outcomes.filter((row) => row.b2b_second_night === '1').map((row) => row.event_id))];
const expectedB2b = ['CHI_2019_20_G003', 'CHI_2019_20_G009', 'CHI_2019_20_G017', 'CHI_2019_20_G025', 'CHI_2019_20_G028', 'CHI_2019_20_G040', 'CHI_2019_20_G044', 'CHI_2019_20_G048', 'CHI_2019_20_G058'];
if (b2b.join('/') !== expectedB2b.join('/')) fail(`b2b mismatch ${b2b.join('/')}`);

const baseFlips = outcomes.filter((row) => row.base_flip === '1');
const flipKeys = baseFlips.map((row) => `${row.proxy}/${row.scenario}/${row.event_id}`).sort();
const expectedFlips = [
  'BPM/LOW/CHI_2019_20_G017',
  'NET_EB/HIGH/CHI_2019_20_G001',
  'NET_EB/HIGH/CHI_2019_20_G025',
];
if (flipKeys.join('/') !== expectedFlips.join('/')) fail(`base flips ${flipKeys.join('/')}`);
if (baseFlips.some((row) => Math.abs(Number(row.actual_margin)) > 1)) fail('base flip beyond one-point game');

const seedFor = (wins) => {
  const losses = 65 - wins;
  const pct = wins / (wins + losses);
  const worse = [15 / 65, 19 / 65, 19 / 64, 20 / 67, 20 / 66, 21 / 66]
    .filter((otherPct) => otherPct < pct).length;
  const charlottePct = wins === 24 ? 22 / 65 : wins === 21 ? 24 / 65 : 23 / 65;
  return 1 + worse + (charlottePct < pct ? 1 : 0);
};
if (seedFor(21) !== 7 || seedFor(22) !== 7 || seedFor(24) !== 8) fail('lottery seed mapping');
if (!(24 / 65 < 24 / 64)) fail('Washington boundary');

console.log('PASS Chicago 2019-20 outcome robustness');
console.log('65 games / 390 proxy-scenario rows / 9 second nights');
console.log('attainable wins: 21, 22, 24; lottery seeds: 7, 8');
console.log('exact record, fixed draw, and Patrick Williams remain HOLD');
