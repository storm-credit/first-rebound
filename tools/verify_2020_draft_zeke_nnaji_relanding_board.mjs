import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_ZEKE_NNAJI_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_ZEKE_NNAJI_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_ZEKE_NNAJI_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['23', 'Minnesota Timberwolves', 'Leandro Bolmaro', 'RETENTION_STRONG_LEAN'],
  ['24', 'Denver Nuggets', 'Zeke Nnaji', 'PRIMARY_LEAN_AUTHOR_GATE'],
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
  'BEY_22_AUTHOR_LOCKED / PICKS_23_TO_24_AUTHOR_GATE',
  'Leandro Bolmaro 23순위 `RETENTION_STRONG_LEAN`',
  'Zeke Nnaji 24순위 `PRIMARY_LEAN / AUTHOR_APPROVAL_REQUIRED`',
  '선수 선택과 픽 거래의 경제는 분리',
  '후대 NBA 성과·부상·계약은 사용하지 않는다',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('PICKS_23_TO_24_AUTHOR_GATE')) throw new Error('missing pick 23-24 author gate');
if (!review.includes('공개된 Nnaji–Hampton 내부 head-to-head 보드는 아니다')) throw new Error('missing Denver evidence limit');
if (!review.includes('정확 23~24순위는 작가 승인 전 `HOLD`')) throw new Error('missing exact-pick hold');

console.log('PASS Zeke Nnaji relanding board');
console.log('Bolmaro 23 retained as strong lean; Nnaji 24 author-gated');
