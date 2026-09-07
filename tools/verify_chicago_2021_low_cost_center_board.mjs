import fs from 'node:fs';

const boardPath = new URL('../simulation/CHICAGO_2021_LOW_COST_CENTER_BOARD.csv', import.meta.url);
const ledgerPath = new URL('../simulation/CHICAGO_2021_THEIS_GREEN_TRANSACTION_LEDGER.csv', import.meta.url);

function readCsv(path) {
  const text = fs.readFileSync(path, 'utf8').trim();
  const [headerLine, ...lines] = text.split(/\r?\n/);
  const headers = headerLine.split(',');
  return lines.map((line) => {
    const values = line.split(',');
    return Object.fromEntries(headers.map((header, index) => [header, values[index]]));
  });
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const board = readCsv(boardPath);
const ledger = readCsv(ledgerPath);

assert(board.length === 3, `expected 3 board options, got ${board.length}`);
assert(new Set(board.map((row) => row.option_id)).size === 3, 'board option ids must be unique');

const byId = Object.fromEntries(board.map((row) => [row.option_id, row]));
assert(byId.A.option_name === 'THEIS_GREEN_FIVE_PLAYER', 'A must be the Theis-Green five-player structure');
assert(byId.A.players_moved === '5', 'A must identify five unique moved players');
assert(byId.A.teams_involved === '3', 'A must involve three teams');
assert(byId.A.first_rounders_spent === '0', 'A cannot spend a first-rounder');
assert(byId.A.carter_retained === '1' && byId.A.porter_retained === '1', 'A must retain Carter and Porter');
assert(byId.A.board_status === 'PRIMARY_LEAN', 'A must be the primary lean');
assert(byId.A.event_status === 'AUTHOR_GATE', 'A exact event must remain at the author gate');
assert(byId.B.board_status === 'SECONDARY_MARKET', 'B must remain the secondary market');
assert(byId.C.board_status === 'FAILURE_CONTINGENCY', 'C must remain the failure contingency');
assert(board.every((row) => row.first_rounders_spent === '0'), 'no O-15F5 option may spend a first-rounder');
assert(board.every((row) => row.carter_retained === '1' && row.porter_retained === '1'), 'all options must retain Carter and Porter');
assert(board.every((row) => row.event_status === 'AUTHOR_GATE'), 'no exact O-15F5 outcome may be auto-locked');

assert(ledger.length === 3, `expected 3 team ledger rows, got ${ledger.length}`);
const byTeam = Object.fromEntries(ledger.map((row) => [row.team, row]));
assert(new Set(ledger.map((row) => row.team)).size === 3, 'team ledger rows must be unique');

const expected = {
  CHI: { outgoing: 3767981, incoming: 6517981, allowed: 6693967, margin: 175986 },
  WAS: { outgoing: 2161920, incoming: 1517981, allowed: 3883360, margin: 2365379 },
  BOS: { outgoing: 6517981, incoming: 4411920, allowed: 8247476, margin: 3835556 },
};

for (const [team, values] of Object.entries(expected)) {
  const row = byTeam[team];
  assert(row, `missing ${team} ledger row`);
  assert(Number(row.outgoing_salary) === values.outgoing, `${team} outgoing salary mismatch`);
  assert(Number(row.incoming_salary) === values.incoming, `${team} incoming salary mismatch`);
  assert(Number(row.allowed_incoming) === values.allowed, `${team} allowed incoming mismatch`);
  assert(Number(row.margin) === values.margin, `${team} margin mismatch`);
  assert(Number(row.incoming_salary) <= Number(row.allowed_incoming), `${team} salary matching failed`);
  assert(row.cap_status === 'PASS', `${team} cap status must pass`);
  assert(row.outgoing_players.split('|').length === row.incoming_players.split('|').length, `${team} roster count must remain flat`);
}

const movedPlayers = new Set();
for (const row of ledger) {
  for (const field of ['outgoing_players', 'incoming_players']) {
    for (const player of row[field].split('|')) movedPlayers.add(player);
  }
}

assert(movedPlayers.size === 5, `expected five unique moved players, got ${movedPlayers.size}`);
assert([...movedPlayers].sort().join('|') === ['GAFFORD', 'GREEN', 'KORNET', 'THEIS', 'WAGNER'].sort().join('|'), 'moved-player set mismatch');

for (const player of movedPlayers) {
  const outgoingCount = ledger.filter((row) => row.outgoing_players.split('|').includes(player)).length;
  const incomingCount = ledger.filter((row) => row.incoming_players.split('|').includes(player)).length;
  assert(outgoingCount === 1 && incomingCount === 1, `${player} must appear once outgoing and once incoming`);
}

console.log('PASS Chicago 2021 low-cost center board: 3 teams, 5 players, cap/roster structure valid, A primary lean, exact event AUTHOR_GATE');
