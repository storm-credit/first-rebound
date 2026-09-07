import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_RJ_HAMPTON_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_RJ_HAMPTON_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_RJ_HAMPTON_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['25', 'New York Knicks', 'Immanuel Quickley', 'RETENTION_STRONG_LEAN'],
  ['26', 'Boston Celtics', 'Payton Pritchard', 'RETENTION_LEAN'],
  ['27', 'Utah Jazz', 'Udoka Azubuike', 'RETENTION_STRONG_LEAN'],
  ['28', 'Minnesota Timberwolves', 'Jaden McDaniels', 'RETENTION_STRONG_LEAN'],
  ['29', 'Toronto Raptors', 'Malachi Flynn', 'RETENTION_STRONG_LEAN'],
  ['30', 'Memphis Grizzlies', 'Desmond Bane', 'RETENTION_STRONG_LEAN'],
  ['31', 'Dallas Mavericks', 'R.J. Hampton', 'PRIMARY_LEAN_AUTHOR_GATE'],
];

if (primary.length !== expected.length) throw new Error(`expected 7 primary rows, got ${primary.length}`);
for (let index = 0; index < expected.length; index += 1) {
  const row = primary[index];
  const actual = [row.pick, row.team, row.rival_world_selection, row.status];
  if (actual.join('|') !== expected[index].join('|')) throw new Error(`primary pick ${index + 25} changed`);
}

const board = fs.readFileSync(boardPath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of [
  'PICKS_1_TO_24_AUTHOR_LOCKED / PICKS_25_TO_31_AUTHOR_GATE',
  'R.J. Hampton 31순위 `PRIMARY_LEAN / AUTHOR_APPROVAL_REQUIRED`',
  '선수 선택과 픽 거래의 경제는 분리',
  '후대 NBA 성과·부상·계약은 사용하지 않는다',
  'Quickley 25 → Pritchard 26 → Azubuike 27 → McDaniels 28 → Flynn 29 → Bane 30 유지 → Hampton 31',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('PICKS_25_TO_31_AUTHOR_GATE')) throw new Error('missing pick 25-31 author gate');
if (!review.includes('Dallas가 Hampton과 인터뷰했다는 사실은 Terry보다 높게 평가했다는 뜻이 아니다')) throw new Error('missing Dallas evidence limit');
if (!review.includes('정확 25~31순위는 작가 승인 전 `HOLD`')) throw new Error('missing exact-pick hold');

console.log('PASS R.J. Hampton relanding board');
console.log('Picks 25-30 retained; Hampton 31 author-gated');
