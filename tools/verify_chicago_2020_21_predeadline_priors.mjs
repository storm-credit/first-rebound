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
const median = (values) => {
  const sorted = [...values].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
};

const cohort = parseCsv('simulation/CHICAGO_2020_21_THIRD_YEAR_WING_COHORT.csv');
if (cohort.length !== 9) fail(`cohort size ${cohort.length}`);
const active = cohort.filter((row) => row.sample_status === 'ACTIVE');
if (active.length !== 8) fail(`active cohort size ${active.length}`);
const evans = cohort.find((row) => row.player === 'Jacob Evans');
if (!evans || evans.sample_status !== 'NO_NBA_MINUTES' || Number(evans.seconds) !== 0) fail('Jacob Evans attrition row');
const expectedMedians = {
  pts36: 11.3815, reb36: 7.2155, ast36: 2.2875, stl36: 1.4125, blk36: 0.7,
  tov36: 1.763, pf36: 3.5165, ts: 0.524666, three_pa36: 2.875, three_p: 0.304202,
};
for (const [field, expected] of Object.entries(expectedMedians)) {
  close(median(active.map((row) => Number(row[field]))), expected, 1e-9, `cohort median ${field}`);
}

const priors = parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_PRODUCTION_PRIORS.csv');
if (priors.length !== 6) fail(`prior rows ${priors.length}`);
const expectedMinutes = new Map([['Protagonist', 1219], ['LaMelo Ball', 1191]]);
for (const player of expectedMinutes.keys()) {
  const rows = priors.filter((row) => row.player === player);
  if (rows.map((row) => row.scenario).join('/') !== 'LOW/BASE/HIGH') fail(`${player}: scenario order`);
  for (const field of ['pts36', 'reb36', 'ast36', 'stl36', 'blk36', 'ts', 'three_pa36', 'three_p', 'usg']) {
    const values = rows.map((row) => Number(row[field]));
    if (!(values[0] <= values[1] && values[1] <= values[2])) fail(`${player}/${field}: range order`);
  }
  for (const field of ['tov36', 'pf36']) {
    const values = rows.map((row) => Number(row[field]));
    if (!(values[0] >= values[1] && values[1] >= values[2])) fail(`${player}/${field}: inverse range order`);
  }
  for (const row of rows) {
    const minutes = expectedMinutes.get(player);
    if (Number(row.minutes) !== minutes || Number(row.gp) !== 43) fail(`${player}/${row.scenario}: role minutes`);
    const totalFields = {pts36: 'total_pts', reb36: 'total_reb', ast36: 'total_ast', stl36: 'total_stl', blk36: 'total_blk', tov36: 'total_tov', pf36: 'total_pf'};
    for (const [rate, total] of Object.entries(totalFields)) {
      close(Number(row[total]), Number((Number(row[rate]) * minutes / 36).toFixed(2)), 1e-9, `${player}/${row.scenario}/${total}`);
    }
    if (row.impact_status !== 'HOLD') fail(`${player}/${row.scenario}: impact prematurely opened`);
  }
}
const lameloBase = priors.find((row) => row.player === 'LaMelo Ball' && row.scenario === 'BASE');
const charlottePreWrist = {pts36: 19.992334, reb36: 7.359141, ast36: 7.696435, stl36: 1.993101, ts: 0.561953, three_p: 0.375};
for (const [field, anchor] of Object.entries(charlottePreWrist)) {
  if (!(Number(lameloBase[field]) < anchor)) fail(`LaMelo BASE not shrunk below Charlotte ${field}`);
}

const playerBudget = new Map(parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_PLAYER_BUDGET.csv').map((row) => [row.player, row]));
const actualStats = new Map([
  ['Patrick Williams', {seconds: 71570, pts: 405, reb: 207, ast: 52, stl: 30, blk: 31, tov: 60, pf: 92, fga: 332, fta: 77, three_pa: 94}],
  ['Chandler Hutchison', {seconds: 3815, pts: 13, reb: 20, ast: 4, stl: 1, blk: 0, tov: 5, pf: 9, fga: 18, fta: 2, three_pa: 3}],
  ['Tomas Satoransky', {seconds: 43283, pts: 245, reb: 81, ast: 152, stl: 21, blk: 9, tov: 54, pf: 43, fga: 172, fta: 46, three_pa: 61}],
  ['Denzel Valentine', {seconds: 43168, pts: 282, reb: 150, ast: 65, stl: 25, blk: 1, tov: 22, pf: 42, fga: 287, fta: 9, three_pa: 169}],
  ['Ryan Arcidiacono', {seconds: 17766, pts: 86, reb: 42, ast: 33, stl: 7, blk: 0, tov: 6, pf: 30, fga: 78, fta: 14, three_pa: 47}],
  ['Coby White', {seconds: 81724, pts: 649, reb: 196, ast: 200, stl: 22, blk: 6, tov: 98, pf: 105, fga: 582, fta: 85, three_pa: 277}],
  ['Garrett Temple', {seconds: 58647, pts: 297, reb: 110, ast: 69, stl: 32, blk: 18, tov: 35, pf: 81, fga: 259, fta: 38, three_pa: 134}],
  ['Otto Porter Jr.', {seconds: 32419, pts: 247, reb: 138, ast: 50, stl: 12, blk: 4, tov: 25, pf: 37, fga: 202, fta: 37, three_pa: 95}],
]);
const transfer = parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_TRANSFER_PRODUCTION.csv');
if (transfer.length !== 8) fail(`transfer rows ${transfer.length}`);
if (transfer.reduce((sum, row) => sum + Number(row.net_debit_seconds), 0) !== 144600) fail('transfer seconds');
if (transfer.filter((row) => row.source_class === 'DIRECT_SLOT_REMOVED').reduce((sum, row) => sum + Number(row.net_debit_seconds), 0) !== 75385) fail('direct seconds');
if (transfer.filter((row) => row.source_class === 'SECONDARY_DONOR').reduce((sum, row) => sum + Number(row.net_debit_seconds), 0) !== 69215) fail('secondary seconds');
for (const row of transfer) {
  const stats = actualStats.get(row.player);
  const budget = playerBudget.get(row.player);
  if (!stats || !budget) fail(`${row.player}: missing source`);
  if (Number(row.actual_seconds) !== stats.seconds || Number(budget.actual_seconds) !== stats.seconds) fail(`${row.player}: actual seconds`);
  if (Number(row.net_debit_seconds) !== -Number(budget.delta_seconds)) fail(`${row.player}: budget debit`);
  const share = Number(row.net_debit_seconds) / stats.seconds;
  close(Number(row.share), share, 5e-10, `${row.player}/share`);
  for (const field of ['pts', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf', 'fga', 'fta', 'three_pa']) {
    close(Number(row[`${field}_removed`]), stats[field] * share, 0.0001, `${row.player}/${field}`);
  }
}

const minuteLedger = new Map(parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_MINUTE_LEDGER.csv').map((row) => [row.event_id, row]));
const donorVector = parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_DONOR_VECTOR.csv');
const inputs = parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_IMPACT_INPUTS.csv');
if (inputs.length !== 43 || new Set(inputs.map((row) => row.event_id)).size !== 43) fail('impact event count');
const protagonistBase = priors.find((row) => row.player === 'Protagonist' && row.scenario === 'BASE');
for (const row of inputs) {
  const minute = minuteLedger.get(row.event_id);
  if (!minute || row.game_id !== minute.game_id || row.date !== minute.date) fail(`${row.event_id}: minute join`);
  if (Number(row.protagonist_seconds) !== Number(minute.protagonist_seconds) || Number(row.lamelo_seconds) !== Number(minute.lamelo_seconds)) fail(`${row.event_id}: fictional seconds`);
  const eventDonors = donorVector.filter((item) => item.event_id === row.event_id && Number(item.delta_seconds) < 0 && item.player !== 'Thaddeus Young');
  for (const field of ['pts', 'reb', 'ast', 'stl', 'blk', 'tov']) {
    const added = Number(protagonistBase[`${field}36`]) * Number(row.protagonist_seconds) / 2160
      + Number(lameloBase[`${field}36`]) * Number(row.lamelo_seconds) / 2160;
    const removed = eventDonors.reduce((sum, item) => {
      const stats = actualStats.get(item.player);
      return sum + (-Number(item.delta_seconds)) * stats[field] / stats.seconds;
    }, 0);
    close(Number(row[`added_${field}_base`]), added, 0.0001, `${row.event_id}/added ${field}`);
    close(Number(row[`removed_${field}_linear`]), removed, 0.0001, `${row.event_id}/removed ${field}`);
    close(Number(row[`box_delta_${field}`]), added - removed, 0.0001, `${row.event_id}/delta ${field}`);
  }
  if (row.impact_status !== 'HOLD') fail(`${row.event_id}: impact prematurely opened`);
}

console.log('PASS Chicago 2020-21 pre-deadline production priors');
console.log('protagonist BASE: 14.5 / 9.8 / 3.2 per 36 over 1,219 minutes');
console.log('LaMelo BASE: 18.0 / 6.8 / 7.2 per 36 over 1,191 minutes');
console.log('transfer: 2,410:00; 43-game box inputs verified; impact remains HOLD');
