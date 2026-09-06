import fs from 'node:fs';
import crypto from 'node:crypto';

const path = new URL('../simulation/CHICAGO_2018_19_OUTCOME_LEDGER.csv', import.meta.url);
const [header, ...lines] = fs.readFileSync(path, 'utf8').trim().split('\n');
const columns = header.split(',');
const rows = lines.map(line => Object.fromEntries(line.split(',').map((value, index) => [columns[index], value])));

if (rows.length !== 82) throw new Error(`expected 82 games, got ${rows.length}`);
if (new Set(rows.map(row => row.event_id)).size !== 82) throw new Error('duplicate event_id');

const expectedModeCounts = {HUTCH: 40, RETURN: 4, POST: 33, NONE: 5};
const modeCounts = Object.fromEntries(Object.keys(expectedModeCounts).map(mode => [mode, rows.filter(row => row.mode === mode).length]));
for (const [mode, expected] of Object.entries(expectedModeCounts)) {
  if (modeCounts[mode] !== expected) throw new Error(`${mode} count: ${modeCounts[mode]}`);
}

const implied = odds => odds < 0 ? -odds / (-odds + 100) : 100 / (odds + 100);
const logistic = value => 1 / (1 + Math.exp(-value));
const logit = probability => Math.log(probability / (1 - probability));
const k = 6.841381133447518;
const seed = 'FIRST_REBOUND|R09|CHI_2018_19|PRIOR_v1';
const seedSha = crypto.createHash('sha256').update(seed).digest('hex');
if (seedSha !== 'a327dfbb38ff2f8cfb25f1abc03a892cee1704613aa81053a8721806f04666e2') throw new Error('seed SHA mismatch');

for (const row of rows) {
  const awayImplied = implied(Number(row.away_ml));
  const homeImplied = implied(Number(row.home_ml));
  const awayFair = awayImplied / (awayImplied + homeImplied);
  const expectedPB = row.away === 'Chicago Bulls' ? awayFair : 1 - awayFair;
  if (Math.abs(Number(row.pB) - expectedPB) > 1e-8) throw new Error(`${row.event_id} pB mismatch`);

  const chicagoAway = row.away === 'Chicago Bulls';
  const actualW = chicagoAway ? Number(row.away_score) > Number(row.home_score) : Number(row.home_score) > Number(row.away_score);
  if ((actualW ? 'W' : 'L') !== row.actual) throw new Error(`${row.event_id} actual result mismatch`);

  const digest = crypto.createHash('sha256').update(`${seed}|${row.event_id}`).digest();
  const first64 = digest.readBigUInt64BE(0);
  const h = Number(first64 >> 11n) / 2 ** 53;
  if (Math.abs(Number(row.h) - h) > 1e-12) throw new Error(`${row.event_id} h mismatch`);
  const u = actualW ? h * expectedPB : expectedPB + h * (1 - expectedPB);
  if (Math.abs(Number(row.u) - u) > 1e-12) throw new Error(`${row.event_id} u mismatch`);

  for (const scenario of ['low', 'base', 'high']) {
    const pCF = logistic(logit(expectedPB) + Number(row[`delta_${scenario}`]) / k);
    if (Math.abs(Number(row[`pCF_${scenario}`]) - pCF) > 1e-8) throw new Error(`${row.event_id} ${scenario} pCF mismatch`);
    const outcome = u < pCF ? 'W' : 'L';
    if (outcome !== row[`cf_${scenario}`]) throw new Error(`${row.event_id} ${scenario} outcome mismatch`);
  }
}

const wins = Object.fromEntries(['low', 'base', 'high'].map(scenario => [scenario, rows.filter(row => row[`cf_${scenario}`] === 'W').length]));
if (wins.low !== 21 || wins.base !== 22 || wins.high !== 22) throw new Error(`wins mismatch: ${JSON.stringify(wins)}`);

const flipped = scenario => rows.filter(row => row.actual !== row[`cf_${scenario}`]).map(row => row.event_id);
if (JSON.stringify(flipped('low')) !== JSON.stringify(['CHI_2018_19_G033'])) throw new Error('LOW flip set mismatch');
if (flipped('base').length || flipped('high').length) throw new Error('unexpected BASE/HIGH flip');

const expectedDeltaSums = {low: -5.70354167, base: 26.145625, high: 57.99479167};
for (const [scenario, expected] of Object.entries(expectedDeltaSums)) {
  const actual = rows.reduce((sum, row) => sum + Number(row[`delta_${scenario}`]), 0);
  if (Math.abs(actual - expected) > 1e-7) throw new Error(`${scenario} delta sum: ${actual}`);
}

console.log('PASS Chicago 2018-19 outcome ledger');
console.log(`mode counts: ${JSON.stringify(modeCounts)}`);
console.log(`counterfactual wins: ${JSON.stringify(wins)}`);
console.log('sensitive event: CHI_2018_19_G033 LOW only');
