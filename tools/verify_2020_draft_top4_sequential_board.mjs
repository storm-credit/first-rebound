import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_TOP4_SEQUENTIAL_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_TOP4_SEQUENTIAL_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_TOP4_SEQUENTIAL_BOARD_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));

const primary = rows.filter((row) => row.branch === 'PRIMARY');
if (primary.length !== 4) throw new Error(`expected 4 primary picks, got ${primary.length}`);

const expected = [
  ['1', 'Minnesota Timberwolves', 'Fictional Rival', 'AUTHOR_LOCKED'],
  ['2', 'Golden State Warriors', 'James Wiseman', 'AUTHOR_LOCKED'],
  ['3', 'Charlotte Hornets', 'Anthony Edwards', 'AUTHOR_LOCKED'],
  ['4', 'Chicago Bulls', 'LaMelo Ball', 'AUTHOR_LOCKED'],
];

for (let index = 0; index < expected.length; index += 1) {
  const row = primary[index];
  const actual = [row.pick, row.team, row.rival_world_selection, row.status];
  if (actual.join('|') !== expected[index].join('|')) throw new Error(`primary pick ${index + 1} changed`);
}

const board = fs.readFileSync(boardPath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of [
  'TOP4_AUTHOR_APPROVED / LOCKED',
  'Wiseman 2 → Edwards 3 → LaMelo 4',
  '정확 top four는 `가상 라이벌 → Wiseman → Edwards → LaMelo`',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('AUTHOR_RESOLVED')) throw new Error('missing author resolution');
if (!review.includes('공개 내부 head-to-head')) throw new Error('missing Charlotte evidence limit');

console.log('PASS 2020 Draft top-four sequential board');
console.log('2020 top four author-locked');
