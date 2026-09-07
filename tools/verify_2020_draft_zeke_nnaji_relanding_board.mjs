import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_ZEKE_NNAJI_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_ZEKE_NNAJI_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_ZEKE_NNAJI_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['23', 'Minnesota Timberwolves', 'Leandro Bolmaro', 'AUTHOR_LOCKED'],
  ['24', 'Denver Nuggets', 'Zeke Nnaji', 'AUTHOR_LOCKED'],
];

if (primary.length !== expected.length) throw new Error(`expected 2 primary rows, got ${primary.length}`);
for (let index = 0; index < expected.length; index += 1) {
  const row = primary[index];
  const actual = [row.pick, row.team, row.rival_world_selection, row.status];
  if (actual.join('|') !== expected[index].join('|')) throw new Error(`primary pick ${index + 23} changed`);
}

const board = fs.readFileSync(boardPath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of [
  'PICKS_23_TO_24_AUTHOR_LOCKED / HAMPTON_RELANDING_OPEN',
  'Leandro Bolmaro 23순위 `AUTHOR_APPROVED / LOCKED`',
  'Zeke Nnaji 24순위 `AUTHOR_APPROVED / LOCKED`',
  '선수 선택과 픽 거래의 경제는 분리',
  '후대 NBA 성과·부상·계약은 사용하지 않는다',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('PICKS_23_TO_24_AUTHOR_LOCKED')) throw new Error('missing pick 23-24 author lock');
if (!review.includes('공개된 Nnaji–Hampton 내부 head-to-head 보드는 아니다')) throw new Error('missing Denver evidence limit');
if (!review.includes('정확 1~24순위가 정본화됐다')) throw new Error('missing exact-pick lock');

console.log('PASS Zeke Nnaji relanding board');
console.log('Bolmaro 23 and Nnaji 24 author-locked; Hampton relanding open');
