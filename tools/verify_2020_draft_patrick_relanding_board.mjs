import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_PATRICK_WILLIAMS_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_PATRICK_WILLIAMS_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_PATRICK_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['5', 'Cleveland Cavaliers', 'Isaac Okoro', 'RETENTION_STRONG_LEAN'],
  ['6', 'Atlanta Hawks', 'Onyeka Okongwu', 'RETENTION_LEAN'],
  ['7', 'Detroit Pistons', 'Patrick Williams', 'PRIMARY_LEAN_AUTHOR_GATE'],
];

if (primary.length !== expected.length) throw new Error(`expected 3 primary rows, got ${primary.length}`);
for (let index = 0; index < expected.length; index += 1) {
  const row = primary[index];
  const actual = [row.pick, row.team, row.rival_world_selection, row.status];
  if (actual.join('|') !== expected[index].join('|')) throw new Error(`primary pick ${index + 5} changed`);
}

const board = fs.readFileSync(boardPath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of [
  'PATRICK_7_PRIMARY_LEAN / AUTHOR_GATE',
  'Patrick Williams Detroit 7순위',
  'Hayes는 삭제하지 않고 New York 8순위부터 다시 보드에 넣는다',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('PICK6_BRANCH_OPEN')) throw new Error('missing Atlanta pick-six blocker');

console.log('PASS Patrick Williams relanding board');
console.log('Okoro 5 / Okongwu 6 / Patrick 7 primary; exact Patrick pick author-gated');
