import fs from 'node:fs';

const csvPath = new URL('../simulation/CHICAGO_2021_VUCEVIC_TRADE_BOARD.csv', import.meta.url);
const text = fs.readFileSync(csvPath, 'utf8').trim();
const [headerLine, ...lines] = text.split(/\r?\n/);
const headers = headerLine.split(',');
const rows = lines.map((line) => {
  const values = line.split(',');
  return Object.fromEntries(headers.map((header, index) => [header, values[index]]));
});

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

assert(rows.length === 3, `expected 3 options, got ${rows.length}`);
assert(new Set(rows.map((row) => row.option_id)).size === 3, 'option ids must be unique');

const byId = Object.fromEntries(rows.map((row) => [row.option_id, row]));
assert(byId.A.option_name === 'HISTORICAL_VUCEVIC_PACKAGE', 'A must be historical Vucevic package');
assert(byId.A.first_rounders_spent === '2', 'A must spend two first-rounders');
assert(byId.A.carter_retained === '0', 'A must send Carter');
assert(byId.B.first_rounders_spent === '0', 'B cannot spend a first-rounder');
assert(byId.B.carter_retained === '1', 'B must retain Carter at this board stage');
assert(byId.B.board_status === 'AUTHOR_APPROVED_DIRECTION_LOCK', 'B direction must be author approved');
assert(byId.B.exact_transaction_status === 'A_PLAYER_ROUTE_APPROVED_EXECUTION_DETAILS_HOLD', 'B exact target must remain open');
assert(byId.A.board_status === 'REJECTED_HISTORICAL_CONTINGENCY', 'A must remain historical contingency');
assert(byId.C.board_status === 'FAILURE_CONTINGENCY', 'C must remain target-failure contingency');
assert(rows.every((row) => row.exact_transaction_status !== 'LOCKED'), 'exact transaction must remain open');

console.log('PASS Chicago 2021 Vucevic board: B direction author-locked, A player route approved; execution details HOLD');
