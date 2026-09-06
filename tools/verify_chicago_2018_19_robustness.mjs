import fs from 'node:fs';
import crypto from 'node:crypto';

const readCsv = relative => {
  const [header, ...lines] = fs.readFileSync(new URL(relative, import.meta.url), 'utf8').trim().split('\n');
  const columns = header.split(',');
  return lines.map(line => Object.fromEntries(line.split(',').map((value, index) => [columns[index], value])));
};

const outcomeRows = readCsv('../simulation/CHICAGO_2018_19_OUTCOME_LEDGER.csv');
const robustRows = readCsv('../simulation/CHICAGO_2018_19_ROBUSTNESS_LEDGER.csv');
if (outcomeRows.length !== 82 || robustRows.length !== 82) throw new Error('expected 82 rows in both ledgers');

const outcomeById = new Map(outcomeRows.map(row => [row.event_id, row]));
for (const row of robustRows) {
  const source = outcomeById.get(row.event_id);
  if (!source || source.date !== row.date) throw new Error(`${row.event_id}: ledger join mismatch`);
  const chicagoAway = source.away === 'Chicago Bulls';
  const margin = chicagoAway
    ? Number(source.away_score) - Number(source.home_score)
    : Number(source.home_score) - Number(source.away_score);
  if (margin !== Number(row.actual_margin)) throw new Error(`${row.event_id}: actual margin mismatch`);
}

const seed = 'FIRST_REBOUND|R09|CHI_2018_19|PRIOR_v1';
const k = 6.841381133447518;
const logistic = value => 1 / (1 + Math.exp(-value));
const logit = probability => Math.log(probability / (1 - probability));
const hValue = eventId => {
  const digest = crypto.createHash('sha256').update(`${seed}|${eventId}`).digest();
  return Number(digest.readBigUInt64BE(0) >> 11n) / 2 ** 53;
};

const conditionalOutcome = (actual, probability, delta, eventId) => {
  const h = hValue(eventId);
  const u = actual === 'W' ? h * probability : probability + h * (1 - probability);
  const counterfactual = logistic(logit(probability) + delta / k);
  return u < counterfactual ? 'W' : 'L';
};

const summarize = outcomes => ({
  wins: outcomes.filter(value => value.outcome === 'W').length,
  flips: outcomes.filter(value => value.actual !== value.outcome).map(value => value.eventId),
});

const conditionalRun = (baseline, impact) => Object.fromEntries(['low', 'base', 'high'].map(scenario => {
  const outcomes = robustRows.map(row => {
    const source = outcomeById.get(row.event_id);
    const probability = baseline === 'odds' ? Number(source.pB) : Number(row.elo_pB);
    const delta = impact === 'bpm' ? Number(source[`delta_${scenario}`]) : Number(row[`ert_delta_${scenario}`]);
    return {
      eventId: row.event_id,
      actual: source.actual,
      outcome: conditionalOutcome(source.actual, probability, delta, row.event_id),
    };
  });
  return [scenario, summarize(outcomes)];
}));

const expectedConditional = {
  oddsBpm: {low: [21, ['CHI_2018_19_G033']], base: [22, []], high: [22, []]},
  eloBpm: {low: [21, ['CHI_2018_19_G033']], base: [22, []], high: [22, []]},
  oddsErt: {low: [22, []], base: [22, []], high: [23, ['CHI_2018_19_G027']]},
  eloErt: {low: [22, []], base: [22, []], high: [24, ['CHI_2018_19_G008', 'CHI_2018_19_G027']]},
};

for (const [key, baseline, impact] of [
  ['oddsBpm', 'odds', 'bpm'],
  ['eloBpm', 'elo', 'bpm'],
  ['oddsErt', 'odds', 'ert'],
  ['eloErt', 'elo', 'ert'],
]) {
  const result = conditionalRun(baseline, impact);
  for (const scenario of ['low', 'base', 'high']) {
    const [wins, flips] = expectedConditional[key][scenario];
    if (result[scenario].wins !== wins || JSON.stringify(result[scenario].flips) !== JSON.stringify(flips)) {
      throw new Error(`${key} ${scenario}: ${JSON.stringify(result[scenario])}`);
    }
  }
}

const b2b = new Set();
let previousPlayedDate = null;
for (const row of robustRows) {
  const source = outcomeById.get(row.event_id);
  const date = new Date(`${row.date}T00:00:00Z`);
  const played = Number(source.protagonist_minutes) > 0;
  if (played && previousPlayedDate && (date - previousPlayedDate) / 86400000 === 1) b2b.add(row.event_id);
  previousPlayedDate = played ? date : null;
}
if (b2b.size !== 11) throw new Error(`second-night count: ${b2b.size}`);

const marginRun = (impact, fatiguePenalty = 0) => Object.fromEntries(['low', 'base', 'high'].map(scenario => {
  const outcomes = robustRows.map(row => {
    const source = outcomeById.get(row.event_id);
    const rawDelta = impact === 'bpm' ? Number(source[`delta_${scenario}`]) : Number(row[`ert_delta_${scenario}`]);
    const fatigue = b2b.has(row.event_id) ? fatiguePenalty * Number(source.protagonist_minutes) / 48 : 0;
    const counterfactualMargin = Number(row.actual_margin) + rawDelta - fatigue;
    return {
      eventId: row.event_id,
      actual: Number(row.actual_margin) > 0 ? 'W' : 'L',
      outcome: counterfactualMargin > 0 ? 'W' : 'L',
    };
  });
  return [scenario, summarize(outcomes)];
}));

const expectedMargin = {
  bpm: {low: [22, []], base: [22, []], high: [23, ['CHI_2018_19_G008']]},
  ert: {low: [22, []], base: [23, ['CHI_2018_19_G008']], high: [24, ['CHI_2018_19_G008', 'CHI_2018_19_G021']]},
};

for (const impact of ['bpm', 'ert']) {
  for (const penalty of [0, 0.5, 1.0]) {
    const result = marginRun(impact, penalty);
    for (const scenario of ['low', 'base', 'high']) {
      const [wins, flips] = expectedMargin[impact][scenario];
      if (result[scenario].wins !== wins || JSON.stringify(result[scenario].flips) !== JSON.stringify(flips)) {
        throw new Error(`${impact} margin fatigue=${penalty} ${scenario}: ${JSON.stringify(result[scenario])}`);
      }
    }
  }
}

const g027 = robustRows.find(row => row.event_id === 'CHI_2018_19_G027');
if (Number(g027.actual_margin) !== -56) throw new Error('G027 margin changed');

console.log('PASS Chicago 2018-19 robustness audit');
console.log('independent baseline: Elo reproduces BPM conditional result 21/22/22');
console.log('structural blocker: Bernoulli runner can flip G027 despite actual margin -56');
console.log('margin-residual range: BPM 22/22/23, eRT 22/23/24');
console.log('fatigue stress: 11 second nights, -0.5/-1.0 per 48 changes no outcome');
