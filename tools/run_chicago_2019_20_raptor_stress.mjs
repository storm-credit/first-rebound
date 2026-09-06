import fs from 'node:fs';

const root = new URL('../', import.meta.url);
const parseCsv = (relative) => {
  const lines = fs.readFileSync(new URL(relative, root), 'utf8').trim().split(/\r?\n/);
  const header = lines.shift().split(',');
  return lines.map((line) => Object.fromEntries(header.map((key, index) => [key, line.split(',')[index]])));
};
const round = (value, places = 6) => Number(value.toFixed(places));
const isoDay = 86_400_000;

const games = parseCsv('simulation/CHICAGO_2019_20_PLAYER_GAME_MINUTE_LEDGER.csv');
const margins = new Map(parseCsv('simulation/CHICAGO_2019_20_GAME_MARGIN_BASELINE.csv').map((row) => [row.event_id, row]));
const donorVector = parseCsv('simulation/CHICAGO_2019_20_PLAYER_GAME_DONOR_VECTOR.csv');
const rosterMinutes = new Map(parseCsv('simulation/CHICAGO_2019_20_ROSTER_BASELINE.csv').map((row) => [row.player, Number(row.seconds) / 60]));
const raptorInputs = new Map(parseCsv('simulation/CHICAGO_2019_20_RAPTOR_INPUTS.csv').map((row) => [row.player, row]));
const priors = parseCsv('simulation/CHICAGO_2019_20_RAPTOR_PRIORS.csv');

const donorByEvent = new Map();
for (const row of donorVector) {
  if (!donorByEvent.has(row.event_id)) donorByEvent.set(row.event_id, []);
  donorByEvent.get(row.event_id).push(row);
}

const secondNights = new Map();
let previousDate = null;
for (const game of games) {
  const currentDate = Date.parse(`${game.date}T00:00:00Z`);
  secondNights.set(game.event_id, previousDate !== null && currentDate - previousDate === isoDay);
  previousDate = currentDate;
}

const ratingFor = (player, regularizerMinutes) => {
  const input = raptorInputs.get(player);
  const minutes = rosterMinutes.get(player);
  if (!input || minutes === undefined) throw new Error(`missing RAPTOR input for ${player}`);
  return minutes * Number(input.raptor_total) / (minutes + regularizerMinutes);
};

const run = (regularizerMinutes, fatiguePenalty, includeRows = false) => {
  const rows = [];
  const summary = [];
  for (const prior of priors) {
    let wins = 0;
    let totalImpact = 0;
    for (const game of games) {
      const protagonistMinutes = Number(game.protagonist_seconds) / 60;
      const secondNight = secondNights.get(game.event_id);
      const protagonistRating = Number(prior.protagonist_rating) - (secondNight ? fatiguePenalty : 0);
      const protagonistImpact = protagonistMinutes * protagonistRating / 48;
      const realPlayerImpact = (donorByEvent.get(game.event_id) ?? []).reduce(
        (total, row) => total + Number(row.delta_seconds) / 60 * ratingFor(row.player, regularizerMinutes) / 48,
        0,
      );
      const impact = protagonistImpact + realPlayerImpact;
      const actualMargin = Number(margins.get(game.event_id).actual_margin);
      const altMargin = actualMargin + impact;
      const altWin = altMargin > 0;
      wins += altWin;
      totalImpact += impact;
      if (includeRows) {
        rows.push({
          event_id: game.event_id,
          game_id: game.game_id,
          date: game.date,
          matchup: game.matchup,
          actual_wl: game.actual_wl,
          actual_margin: actualMargin,
          scenario: prior.scenario,
          protagonist_rating: Number(prior.protagonist_rating),
          protagonist_minutes: round(protagonistMinutes, 4),
          b2b_second_night: secondNight ? 1 : 0,
          fatigue_penalty: fatiguePenalty,
          real_player_impact_points: round(realPlayerImpact),
          total_impact_points: round(impact),
          alt_margin: round(altMargin),
          alt_wl: altWin ? 'W' : 'L',
          flip: altWin !== (actualMargin > 0) ? 1 : 0,
        });
      }
    }
    summary.push({regularizer_minutes: regularizerMinutes, fatigue_penalty: fatiguePenalty, scenario: prior.scenario, wins, losses: 65 - wins, total_impact_points: round(totalImpact)});
  }
  return {rows, summary};
};

const primaryHeader = ['event_id', 'game_id', 'date', 'matchup', 'actual_wl', 'actual_margin', 'scenario', 'protagonist_rating', 'protagonist_minutes', 'b2b_second_night', 'fatigue_penalty', 'real_player_impact_points', 'total_impact_points', 'alt_margin', 'alt_wl', 'flip'];
const primaryRows = [];
for (const fatigue of [0, 0.5, 1.0]) primaryRows.push(...run(1000, fatigue, true).rows);
const encode = (header, rows) => `${header.join(',')}\n${rows.map((row) => header.map((field) => row[field]).join(',')).join('\n')}\n`;
fs.writeFileSync(new URL('simulation/CHICAGO_2019_20_RAPTOR_OUTCOME_LEDGER.csv', root), encode(primaryHeader, primaryRows));

const sensitivityHeader = ['regularizer_minutes', 'fatigue_penalty', 'scenario', 'wins', 'losses', 'total_impact_points'];
const sensitivityRows = [];
for (const regularizer of [500, 1000, 1500, 2000]) {
  for (const fatigue of [0, 0.5, 1.0]) sensitivityRows.push(...run(regularizer, fatigue).summary);
}
fs.writeFileSync(new URL('simulation/CHICAGO_2019_20_REGULARIZER_SENSITIVITY.csv', root), encode(sensitivityHeader, sensitivityRows));

for (const row of sensitivityRows) {
  if (row.regularizer_minutes === 1000) console.log(`RAPTOR_EB/${row.scenario}/fatigue-${row.fatigue_penalty}: ${row.wins}-${row.losses}`);
}
