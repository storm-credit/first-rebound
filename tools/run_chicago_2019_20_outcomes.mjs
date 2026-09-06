import fs from 'node:fs';

const root = new URL('../', import.meta.url);
const parseCsv = (relative) => {
  const lines = fs.readFileSync(new URL(relative, root), 'utf8').trim().split(/\r?\n/);
  const header = lines.shift().split(',');
  return lines.map((line) => Object.fromEntries(header.map((key, index) => [key, line.split(',')[index]])));
};
const round = (value, places = 6) => Number(value.toFixed(places));
const isoDay = 86_400_000;

const ledger = parseCsv('simulation/CHICAGO_2019_20_PLAYER_GAME_MINUTE_LEDGER.csv');
const donorVector = parseCsv('simulation/CHICAGO_2019_20_PLAYER_GAME_DONOR_VECTOR.csv');
const margins = parseCsv('simulation/CHICAGO_2019_20_GAME_MARGIN_BASELINE.csv');
const roster = parseCsv('simulation/CHICAGO_2019_20_ROSTER_BASELINE.csv');
const impactInputs = parseCsv('simulation/CHICAGO_2019_20_IMPACT_INPUTS.csv');
const priors = parseCsv('simulation/CHICAGO_2019_20_IMPACT_PRIORS.csv');

const marginsByEvent = new Map(margins.map((row) => [row.event_id, row]));
const rosterMinutes = new Map(roster.map((row) => [row.player, Number(row.seconds) / 60]));
const inputsByPlayer = new Map(impactInputs.map((row) => [row.player, row]));
const donorByEvent = new Map();
for (const row of donorVector) {
  if (!donorByEvent.has(row.event_id)) donorByEvent.set(row.event_id, []);
  donorByEvent.get(row.event_id).push(row);
}

const teamNetPrior = -3.1;
const netPriorMinutes = 1000;
const ratingFor = (player, proxy) => {
  const input = inputsByPlayer.get(player);
  if (!input) throw new Error(`missing impact input for ${player}`);
  if (proxy === 'BPM') return Number(input.bpm);
  const minutes = rosterMinutes.get(player);
  if (minutes === undefined) throw new Error(`missing roster minutes for ${player}`);
  return (minutes * Number(input.nba_net_rating) + netPriorMinutes * teamNetPrior) /
    (minutes + netPriorMinutes);
};

const header = [
  'event_id', 'game_id', 'date', 'matchup', 'actual_wl', 'actual_margin',
  'proxy', 'scenario', 'protagonist_rating', 'protagonist_minutes',
  'protagonist_impact_points', 'real_player_impact_points', 'base_impact_points',
  'base_alt_margin', 'base_alt_wl', 'base_flip', 'b2b_second_night',
  'fatigue_05_alt_margin', 'fatigue_05_alt_wl', 'fatigue_05_flip',
  'fatigue_10_alt_margin', 'fatigue_10_alt_wl', 'fatigue_10_flip',
];
const output = [header.join(',')];

let previousDate = null;
for (const game of ledger) {
  const baseline = marginsByEvent.get(game.event_id);
  if (!baseline) throw new Error(`missing margin for ${game.event_id}`);
  const currentDate = Date.parse(`${game.date}T00:00:00Z`);
  const secondNight = previousDate !== null && currentDate - previousDate === isoDay;
  previousDate = currentDate;
  const protagonistMinutes = Number(game.protagonist_seconds) / 60;

  for (const prior of priors) {
    const protagonistRating = Number(prior.protagonist_rating);
    const protagonistImpact = protagonistMinutes * protagonistRating / 48;
    const realPlayerImpact = (donorByEvent.get(game.event_id) ?? []).reduce(
      (total, row) => total + Number(row.delta_seconds) / 60 * ratingFor(row.player, prior.proxy) / 48,
      0,
    );
    const baseImpact = protagonistImpact + realPlayerImpact;
    const actualMargin = Number(baseline.actual_margin);
    const actualWin = actualMargin > 0;
    const resultFor = (fatiguePenalty) => {
      const fatigueImpact = secondNight ? protagonistMinutes * fatiguePenalty / 48 : 0;
      const altMargin = actualMargin + baseImpact - fatigueImpact;
      const altWin = altMargin > 0;
      return {altMargin, altWl: altWin ? 'W' : 'L', flip: altWin !== actualWin ? 1 : 0};
    };
    const base = resultFor(0);
    const fatigue05 = resultFor(0.5);
    const fatigue10 = resultFor(1.0);
    output.push([
      game.event_id, game.game_id, game.date, game.matchup, baseline.actual_wl, actualMargin,
      prior.proxy, prior.scenario, protagonistRating, round(protagonistMinutes, 4),
      round(protagonistImpact), round(realPlayerImpact), round(baseImpact),
      round(base.altMargin), base.altWl, base.flip, secondNight ? 1 : 0,
      round(fatigue05.altMargin), fatigue05.altWl, fatigue05.flip,
      round(fatigue10.altMargin), fatigue10.altWl, fatigue10.flip,
    ].join(','));
  }
}

fs.writeFileSync(new URL('simulation/CHICAGO_2019_20_OUTCOME_LEDGER.csv', root), `${output.join('\n')}\n`);

const rows = output.slice(1).map((line) => {
  const values = line.split(',');
  return Object.fromEntries(header.map((key, index) => [key, values[index]]));
});
for (const proxy of ['BPM', 'NET_EB']) {
  for (const scenario of ['LOW', 'BASE', 'HIGH']) {
    const subset = rows.filter((row) => row.proxy === proxy && row.scenario === scenario);
    const wins = (field) => subset.filter((row) => row[field] === 'W').length;
    console.log(`${proxy}/${scenario}: base ${wins('base_alt_wl')}, fatigue-0.5 ${wins('fatigue_05_alt_wl')}, fatigue-1.0 ${wins('fatigue_10_alt_wl')}`);
  }
}
