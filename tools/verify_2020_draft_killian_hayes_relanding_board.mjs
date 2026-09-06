import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_KILLIAN_HAYES_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_KILLIAN_HAYES_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_KILLIAN_HAYES_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['8', 'New York Knicks', 'Obi Toppin', 'AUTHOR_LOCKED'],
  ['9', 'Washington Wizards', 'Deni Avdija', 'AUTHOR_LOCKED'],
  ['10', 'Phoenix Suns', 'Jalen Smith', 'AUTHOR_LOCKED'],
  ['11', 'San Antonio Spurs', 'Devin Vassell', 'AUTHOR_LOCKED'],
  ['12', 'Sacramento Kings', 'Tyrese Haliburton', 'AUTHOR_LOCKED'],
  ['13', 'New Orleans Pelicans', 'Killian Hayes', 'AUTHOR_LOCKED'],
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
  'AUTHOR_APPROVED / PICKS_8_TO_13_LOCKED / HAYES_13_LOCKED',
  'Killian Hayes 13순위',
  'Kira Lewis를 Boston 14순위부터 재판정한다',
  '후대 NBA 성과와 계약은 사용하지 않는다',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('AUTHOR_RESOLVED')) throw new Error('missing author resolution');
if (!review.includes('공개되지 않은 Hayes–Lewis 내부 보드가 확인됐다는 뜻이 아니다')) throw new Error('missing evidence firewall');

console.log('PASS Killian Hayes relanding board');
console.log('actual picks 8-12 retained; Hayes 13 author-locked; Kira relanding open');
