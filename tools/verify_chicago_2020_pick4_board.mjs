import fs from 'node:fs';

const csvPath = new URL('../simulation/CHICAGO_2020_PICK4_CONDITIONAL_BOARD.csv', import.meta.url);
const docPath = new URL('../simulation/CHICAGO_2020_PICK4_TEAM_BOARD.md', import.meta.url);

const csv = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = csv.shift().split(',');
const rows = csv.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const expected = ['Tyrese Haliburton', 'Deni Avdija', 'Patrick Williams', 'Devin Vassell', 'Isaac Okoro'];

if (rows.length !== 5) throw new Error(`expected 5 candidates, got ${rows.length}`);
if (rows.map((row) => row.candidate).join('|') !== expected.join('|')) {
  throw new Error('conditional board order or candidate set changed');
}
if (new Set(rows.map((row) => row.board_order)).size !== 5) throw new Error('duplicate board order');

const doc = fs.readFileSync(docPath, 'utf8');
for (const marker of [
  'UPSTREAM_RIVAL_BLOCKER',
  'EXACT_PICK_HOLD',
  '실제 상위 3명이 그대로 지명된 경우',
  '후대 NBA 성과가 아니라',
  '전체 4순위: `AUTHOR_APPROVED / LOCKED`',
]) {
  if (!doc.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}

console.log('PASS Chicago 2020 pick 4 conditional board');
console.log('5 candidates / upstream rival blocker / exact pick HOLD');
