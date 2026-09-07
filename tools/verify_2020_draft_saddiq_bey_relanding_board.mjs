import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_SADDIQ_BEY_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_SADDIQ_BEY_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_SADDIQ_BEY_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['20', 'Miami Heat', 'Precious Achiuwa', 'RETENTION_STRONG_LEAN'],
  ['21', 'Philadelphia 76ers', 'Tyrese Maxey', 'RETENTION_STRONG_LEAN'],
  ['22', 'Denver Nuggets', 'Saddiq Bey', 'PRIMARY_LEAN_AUTHOR_GATE'],
];

if (primary.length !== expected.length) throw new Error(`expected 3 primary rows, got ${primary.length}`);
for (let index = 0; index < expected.length; index += 1) {
  const row = primary[index];
  const actual = [row.pick, row.team, row.rival_world_selection, row.status];
  if (actual.join('|') !== expected[index].join('|')) throw new Error(`primary pick ${index + 20} changed`);
}

const board = fs.readFileSync(boardPath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of [
  'STEWART_19_AUTHOR_LOCKED / PICKS_20_TO_22_AUTHOR_GATE',
  'Precious Achiuwa 20순위 `RETENTION_STRONG_LEAN`',
  'Tyrese Maxey 21순위 `RETENTION_STRONG_LEAN`',
  'Saddiq Bey 22순위 `PRIMARY_LEAN / AUTHOR_APPROVAL_REQUIRED`',
  '후대 NBA 성과·부상·계약은 사용하지 않는다',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('PICKS_20_TO_22_AUTHOR_GATE')) throw new Error('missing pick 20-22 author gate');
if (!review.includes('head-to-head 증거는 아니다')) throw new Error('missing Denver evidence limit');
if (!review.includes('정확 20~22순위는 작가 승인 전 `HOLD`')) throw new Error('missing exact-pick hold');

console.log('PASS Saddiq Bey relanding board');
console.log('Achiuwa 20 / Maxey 21 retained as strong leans; Bey 22 author-gated');
