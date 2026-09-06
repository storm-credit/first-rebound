import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_KILLIAN_HAYES_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_KILLIAN_HAYES_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_KILLIAN_HAYES_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['8', 'New York Knicks', 'Obi Toppin', 'RETENTION_STRONG_LEAN'],
  ['9', 'Washington Wizards', 'Deni Avdija', 'RETENTION_STRONG_LEAN'],
  ['10', 'Phoenix Suns', 'Jalen Smith', 'RETENTION_LEAN'],
  ['11', 'San Antonio Spurs', 'Devin Vassell', 'RETENTION_LEAN'],
  ['12', 'Sacramento Kings', 'Tyrese Haliburton', 'RETENTION_STRONG_LEAN'],
  ['13', 'New Orleans Pelicans', 'Killian Hayes', 'PRIMARY_LEAN_AUTHOR_GATE'],
];

if (primary.length !== expected.length) throw new Error(`expected 6 primary rows, got ${primary.length}`);
for (let index = 0; index < expected.length; index += 1) {
  const row = primary[index];
  const actual = [row.pick, row.team, row.rival_world_selection, row.status];
  if (actual.join('|') !== expected[index].join('|')) throw new Error(`primary pick ${index + 8} changed`);
}

const board = fs.readFileSync(boardPath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of [
  'HAYES_13_PRIMARY_LEAN / AUTHOR_GATE',
  'Killian Hayes 13순위',
  'Kira Lewis를 Boston 14순위부터',
  '후대 NBA 성과와 계약은 사용하지 않는다',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('PICK13_INTERNAL_BOARD_BLOCKER')) throw new Error('missing pick-13 blocker');

console.log('PASS Killian Hayes relanding board');
console.log('actual picks 8-12 retained; Hayes 13 primary; exact pick author-gated');
