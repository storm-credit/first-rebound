import fs from 'node:fs';

const root = new URL('../', import.meta.url);
const parseCsv = (relative) => {
  const lines = fs.readFileSync(new URL(relative, root), 'utf8').trim().split(/\r?\n/);
  const header = lines.shift().split(',');
  return lines.map((line) => Object.fromEntries(header.map((key, index) => [key, line.split(',')[index]])));
};
const fail = (message) => { throw new Error(message); };
const close = (actual, expected, tolerance, label) => {
  if (Math.abs(actual - expected) > tolerance) fail(`${label}: ${actual} != ${expected}`);
};

const margins = parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_GAME_MARGIN_BASELINE.csv');
const minuteLedger = parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_MINUTE_LEDGER.csv');
if (margins.length !== 43 || new Set(margins.map((row) => row.event_id)).size !== 43) fail('margin event count');
if (margins.filter((row) => row.actual_wl === 'W').length !== 19) fail('actual wins');
if (margins.filter((row) => Number(row.actual_margin) > 0).length !== 19) fail('actual margin wins');
for (let index = 0; index < margins.length; index += 1) {
  for (const field of ['event_id', 'game_id', 'date', 'matchup', 'actual_wl']) {
    if (margins[index][field] !== minuteLedger[index][field]) fail(`${field} join ${index}`);
  }
  if (Number(margins[index].chicago_pts) - Number(margins[index].opponent_pts) !== Number(margins[index].actual_margin)) fail(`score margin ${margins[index].event_id}`);
}
const expectedB2b = ['CHI_2020_21_G003', 'CHI_2020_21_G006', 'CHI_2020_21_G009', 'CHI_2020_21_G014', 'CHI_2020_21_G016', 'CHI_2020_21_G022', 'CHI_2020_21_G029', 'CHI_2020_21_G036', 'CHI_2020_21_G039', 'CHI_2020_21_G042'];
if (margins.filter((row) => row.b2b_second_night === '1').map((row) => row.event_id).join('/') !== expectedB2b.join('/')) fail('b2b dates');

const cohort = parseCsv('simulation/CHICAGO_2020_21_THIRD_YEAR_WING_IMPACT_COHORT.csv');
if (cohort.length !== 9 || cohort.filter((row) => row.sample_status === 'ACTIVE').length !== 8) fail('impact cohort');
const active = cohort.filter((row) => row.sample_status === 'ACTIVE');
const median = (values) => {
  const sorted = [...values].sort((a, b) => a - b);
  return (sorted[3] + sorted[4]) / 2;
};
close(median(active.map((row) => Number(row.bpm))), -2.95, 1e-9, 'BPM median');
close(median(active.map((row) => Number(row.raptor_total))), -2.211622991, 1e-9, 'RAPTOR median');
close(median(active.map((row) => Number(row.e_net_to_2021_03_24))), -4.6, 1e-9, 'E_NET median');

const priors = parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_IMPACT_PRIORS.csv');
if (priors.length !== 9) fail('impact priors');
const expectedPriors = [
  'BPM/LOW/-3/-2.4', 'BPM/BASE/-1.2/-0.5', 'BPM/HIGH/0.3/1.8',
  'RAPTOR_EB/LOW/-2.2/-2.4', 'RAPTOR_EB/BASE/-0.8/-0.5', 'RAPTOR_EB/HIGH/0.6/0.3',
  'E_NET_EB/LOW/-4.6/-5.5', 'E_NET_EB/BASE/-2/-3.2', 'E_NET_EB/HIGH/0/0',
];
if (priors.map((row) => `${row.proxy}/${row.scenario}/${Number(row.protagonist_rating)}/${Number(row.lamelo_rating)}`).join('|') !== expectedPriors.join('|')) fail('prior values');

const outcomes = parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_OUTCOME_LEDGER.csv');
if (outcomes.length !== 43 * 9) fail(`outcome rows ${outcomes.length}`);
const expected = {
  'BPM/LOW': [19, 19, 19],
  'BPM/BASE': [21, 21, 21],
  'BPM/HIGH': [26, 26, 26],
  'RAPTOR_EB/LOW': [19, 19, 19],
  'RAPTOR_EB/BASE': [21, 20, 20],
  'RAPTOR_EB/HIGH': [23, 23, 23],
  'E_NET_EB/LOW': [14, 14, 14],
  'E_NET_EB/BASE': [19, 19, 19],
  'E_NET_EB/HIGH': [22, 21, 21],
};
const fields = ['base_alt_wl', 'fatigue_05_alt_wl', 'fatigue_10_alt_wl'];
for (const [key, wins] of Object.entries(expected)) {
  const [proxy, scenario] = key.split('/');
  const rows = outcomes.filter((row) => row.proxy === proxy && row.scenario === scenario);
  if (rows.length !== 43) fail(`${key} rows`);
  fields.forEach((field, index) => {
    if (rows.filter((row) => row[field] === 'W').length !== wins[index]) fail(`${key}/${field}`);
  });
}
if (outcomes.some((row) => row.base_alt_wl !== row.no_bridge_alt_wl)) fail('Young bridge changes an outcome');
for (const proxy of ['BPM', 'RAPTOR_EB', 'E_NET_EB']) {
  for (const scenario of ['LOW', 'BASE', 'HIGH']) {
    const sum = outcomes.filter((row) => row.proxy === proxy && row.scenario === scenario)
      .reduce((total, row) => total + Number(row.young_bridge_impact), 0);
    close(sum, 0, 1e-9, `${proxy}/${scenario} Young bridge net`);
  }
}
if (outcomes.filter((row) => row.base_flip === '1').some((row) => Math.abs(Number(row.actual_margin)) > 5)) fail('base flip beyond five-point game');

const centralBpm = outcomes.filter((row) => row.proxy === 'BPM' && row.scenario === 'BASE');
if (centralBpm.filter((row) => row.base_flip === '1').map((row) => row.event_id).join('/') !== 'CHI_2020_21_G003/CHI_2020_21_G018') fail('BPM BASE flips');
const centralRaptor = outcomes.filter((row) => row.proxy === 'RAPTOR_EB' && row.scenario === 'BASE');
if (centralRaptor.filter((row) => row.base_flip === '1').map((row) => row.event_id).join('/') !== 'CHI_2020_21_G003/CHI_2020_21_G018') fail('RAPTOR BASE base flips');
if (centralRaptor.filter((row) => row.fatigue_05_flip === '1').map((row) => row.event_id).join('/') !== 'CHI_2020_21_G018') fail('RAPTOR BASE fatigue flips');
const centralENet = outcomes.filter((row) => row.proxy === 'E_NET_EB' && row.scenario === 'BASE');
if (centralENet.some((row) => row.base_flip === '1' || row.fatigue_05_flip === '1' || row.fatigue_10_flip === '1')) fail('E_NET BASE flip');

const sensitivity = parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_RAPTOR_SENSITIVITY.csv');
if (sensitivity.length !== 4 * 3 * 3) fail('sensitivity rows');
const expectedSensitivity = {
  '500/LOW': [19, 19, 19], '500/BASE': [22, 22, 21], '500/HIGH': [24, 24, 24],
  '1000/LOW': [19, 19, 19], '1000/BASE': [21, 20, 20], '1000/HIGH': [23, 23, 23],
  '1500/LOW': [19, 19, 19], '1500/BASE': [19, 19, 19], '1500/HIGH': [23, 23, 22],
  '2000/LOW': [19, 19, 19], '2000/BASE': [19, 19, 19], '2000/HIGH': [23, 23, 22],
};
for (const [key, wins] of Object.entries(expectedSensitivity)) {
  const [regularizer, scenario] = key.split('/');
  const rows = sensitivity.filter((row) => row.regularizer_minutes === regularizer && row.scenario === scenario);
  if (rows.map((row) => Number(row.wins)).join('/') !== wins.join('/')) fail(`${key} sensitivity`);
}

const standings = parseCsv('simulation/CHICAGO_2020_21_2021_03_24_EAST_STANDINGS.csv');
if (standings.length !== 15) fail('East standings rows');
const chicago = standings.find((row) => row.team === 'Chicago Bulls');
if (!chicago || Number(chicago.wins) !== 19 || Number(chicago.losses) !== 24) fail('Chicago standings baseline');
const rankFor = (wins, losses) => {
  const pct = wins / (wins + losses);
  return 1 + standings.filter((row) => row.team !== 'Chicago Bulls' && Number(row.win_pct) > pct).length;
};
if (rankFor(19, 24) !== 10 || rankFor(20, 23) !== 9 || rankFor(21, 22) !== 8) fail('central East rank mapping');
const indiana = standings.find((row) => row.team === 'Indiana Pacers');
close(Number(indiana.win_pct), 20 / 43, 0.000001, 'Indiana tie boundary');

console.log('PASS Chicago 2020-21 pre-deadline outcome robustness');
console.log('43 games / actual 19-24 / 10 second nights / Young bridge outcome-neutral');
console.log('central BASE: 19-21 wins; primary envelope: 14-26; exact record remains HOLD');
console.log('central standing band: East 8-10; deadline trades remain HOLD');
