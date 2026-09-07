import fs from 'node:fs';

const root = new URL('../', import.meta.url);
const parseCsv = (relative) => {
  const lines = fs.readFileSync(new URL(relative, root), 'utf8').trim().split(/\r?\n/);
  const header = lines.shift().split(',');
  return lines.map((line) => Object.fromEntries(header.map((key, index) => [key, line.split(',')[index]])));
};
const csv = (rows, fields) => `${fields.join(',')}\n${rows.map((row) => fields.map((field) => row[field]).join(',')).join('\n')}\n`;
const number = (value) => Number(value);
const fixed = (value) => Number(value).toFixed(6);
const wl = (margin) => margin > 0 ? 'W' : 'L';

const margins = parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_GAME_MARGIN_BASELINE.csv');
const minutes = new Map(parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_MINUTE_LEDGER.csv').map((row) => [row.event_id, row]));
const donors = parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_DONOR_VECTOR.csv');
const inputs = new Map(parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_PLAYER_IMPACT_INPUTS.csv').map((row) => [row.player, row]));
const priors = parseCsv('simulation/CHICAGO_2020_21_PREDEADLINE_IMPACT_PRIORS.csv');

const ratingMap = (proxy, regularizer = 1000) => new Map([...inputs].map(([player, row]) => {
  if (proxy === 'BPM') return [player, number(row.bpm)];
  if (proxy === 'E_NET_EB') {
    const playerMinutes = number(row.predeadline_seconds) / 60;
    const chicagoPrior = -0.6;
    return [player, (number(row.e_net_to_2021_03_24) * playerMinutes + chicagoPrior * regularizer) / (playerMinutes + regularizer)];
  }
  const raw = number(row.raptor_total);
  const playerMinutes = number(row.raptor_minutes);
  return [player, raw * playerMinutes / (playerMinutes + regularizer)];
}));

const calculate = ({proxy, scenario, protagonistRating, lameloRating, regularizer = 1000, fatiguePenalty = 0}) => {
  const ratings = ratingMap(proxy, regularizer);
  return margins.map((game) => {
    const role = minutes.get(game.event_id);
    const eventDonors = donors.filter((row) => row.event_id === game.event_id);
    const protagonistImpact = number(role.protagonist_seconds) / 60 * protagonistRating / 48;
    const lameloImpact = number(role.lamelo_seconds) / 60 * lameloRating / 48;
    const coreDonorImpact = eventDonors.filter((row) => row.player !== 'Thaddeus Young')
      .reduce((sum, row) => sum + number(row.delta_seconds) / 60 * ratings.get(row.player) / 48, 0);
    const youngBridgeImpact = eventDonors.filter((row) => row.player === 'Thaddeus Young')
      .reduce((sum, row) => sum + number(row.delta_seconds) / 60 * ratings.get(row.player) / 48, 0);
    const baseImpact = protagonistImpact + lameloImpact + coreDonorImpact + youngBridgeImpact;
    const fatigueImpact = number(game.b2b_second_night)
      ? -fatiguePenalty * (number(role.protagonist_seconds) + number(role.lamelo_seconds)) / 60 / 48
      : 0;
    const alternateMargin = number(game.actual_margin) + baseImpact + fatigueImpact;
    return {
      ...game,
      proxy,
      scenario,
      protagonist_rating: protagonistRating,
      lamelo_rating: lameloRating,
      protagonist_impact: fixed(protagonistImpact),
      lamelo_impact: fixed(lameloImpact),
      core_donor_impact: fixed(coreDonorImpact),
      young_bridge_impact: fixed(youngBridgeImpact),
      base_impact: fixed(baseImpact),
      fatigue_impact: fixed(fatigueImpact),
      alternate_margin: fixed(alternateMargin),
      alternate_wl: wl(alternateMargin),
      no_bridge_margin: fixed(number(game.actual_margin) + baseImpact - youngBridgeImpact + fatigueImpact),
      no_bridge_wl: wl(number(game.actual_margin) + baseImpact - youngBridgeImpact + fatigueImpact),
      flip: wl(number(game.actual_margin)) === wl(alternateMargin) ? '0' : '1',
      fatigue_penalty: fatiguePenalty,
      regularizer,
    };
  });
};

const primary = [];
for (const prior of priors) {
  const rowsByFatigue = [0, 0.5, 1].map((fatiguePenalty) => calculate({
    proxy: prior.proxy,
    scenario: prior.scenario,
    protagonistRating: number(prior.protagonist_rating),
    lameloRating: number(prior.lamelo_rating),
    fatiguePenalty,
  }));
  for (let index = 0; index < margins.length; index += 1) {
    const [base, fatigue05, fatigue10] = rowsByFatigue.map((rows) => rows[index]);
    primary.push({
      event_id: base.event_id,
      game_id: base.game_id,
      date: base.date,
      matchup: base.matchup,
      actual_wl: base.actual_wl,
      actual_margin: base.actual_margin,
      b2b_second_night: base.b2b_second_night,
      proxy: base.proxy,
      scenario: base.scenario,
      protagonist_rating: base.protagonist_rating,
      lamelo_rating: base.lamelo_rating,
      protagonist_impact: base.protagonist_impact,
      lamelo_impact: base.lamelo_impact,
      core_donor_impact: base.core_donor_impact,
      young_bridge_impact: base.young_bridge_impact,
      base_impact: base.base_impact,
      base_alt_margin: base.alternate_margin,
      base_alt_wl: base.alternate_wl,
      base_flip: base.flip,
      fatigue_05_impact: fatigue05.fatigue_impact,
      fatigue_05_alt_margin: fatigue05.alternate_margin,
      fatigue_05_alt_wl: fatigue05.alternate_wl,
      fatigue_05_flip: fatigue05.flip,
      fatigue_10_impact: fatigue10.fatigue_impact,
      fatigue_10_alt_margin: fatigue10.alternate_margin,
      fatigue_10_alt_wl: fatigue10.alternate_wl,
      fatigue_10_flip: fatigue10.flip,
      no_bridge_alt_margin: base.no_bridge_margin,
      no_bridge_alt_wl: base.no_bridge_wl,
    });
  }
}

const sensitivity = [];
const raptorPriors = priors.filter((row) => row.proxy === 'RAPTOR_EB');
for (const regularizer of [500, 1000, 1500, 2000]) {
  for (const prior of raptorPriors) {
    for (const fatiguePenalty of [0, 0.5, 1]) {
      const rows = calculate({
        proxy: 'RAPTOR_EB',
        scenario: prior.scenario,
        protagonistRating: number(prior.protagonist_rating),
        lameloRating: number(prior.lamelo_rating),
        regularizer,
        fatiguePenalty,
      });
      sensitivity.push({
        regularizer_minutes: regularizer,
        scenario: prior.scenario,
        fatigue_penalty: fatiguePenalty,
        wins: rows.filter((row) => row.alternate_wl === 'W').length,
        losses: rows.filter((row) => row.alternate_wl === 'L').length,
        cumulative_impact: fixed(rows.reduce((sum, row) => sum + number(row.base_impact) + number(row.fatigue_impact), 0)),
        flips: rows.filter((row) => row.flip === '1').map((row) => row.event_id).join('|') || 'NONE',
      });
    }
  }
}

const primaryFields = [
  'event_id', 'game_id', 'date', 'matchup', 'actual_wl', 'actual_margin', 'b2b_second_night', 'proxy', 'scenario',
  'protagonist_rating', 'lamelo_rating', 'protagonist_impact', 'lamelo_impact', 'core_donor_impact', 'young_bridge_impact',
  'base_impact', 'base_alt_margin', 'base_alt_wl', 'base_flip', 'fatigue_05_impact', 'fatigue_05_alt_margin',
  'fatigue_05_alt_wl', 'fatigue_05_flip', 'fatigue_10_impact', 'fatigue_10_alt_margin', 'fatigue_10_alt_wl',
  'fatigue_10_flip', 'no_bridge_alt_margin', 'no_bridge_alt_wl',
];
const sensitivityFields = ['regularizer_minutes', 'scenario', 'fatigue_penalty', 'wins', 'losses', 'cumulative_impact', 'flips'];

if (process.argv.includes('--write')) {
  fs.writeFileSync(new URL('simulation/CHICAGO_2020_21_PREDEADLINE_OUTCOME_LEDGER.csv', root), csv(primary, primaryFields));
  fs.writeFileSync(new URL('simulation/CHICAGO_2020_21_PREDEADLINE_RAPTOR_SENSITIVITY.csv', root), csv(sensitivity, sensitivityFields));
}

const summary = priors.map((prior) => {
  const rows = primary.filter((row) => row.proxy === prior.proxy && row.scenario === prior.scenario);
  return `${prior.proxy}/${prior.scenario}: ${['base_alt_wl', 'fatigue_05_alt_wl', 'fatigue_10_alt_wl'].map((field) => rows.filter((row) => row[field] === 'W').length).join('/')}`;
});
console.log(summary.join('\n'));
