import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_RJ_HAMPTON_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_RJ_HAMPTON_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_RJ_HAMPTON_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['25', 'New York Knicks', 'Immanuel Quickley', 'AUTHOR_LOCKED'],
  ['26', 'Boston Celtics', 'Payton Pritchard', 'AUTHOR_LOCKED'],
  ['27', 'Utah Jazz', 'Udoka Azubuike', 'AUTHOR_LOCKED'],
  ['28', 'Minnesota Timberwolves', 'Jaden McDaniels', 'AUTHOR_LOCKED'],
  ['29', 'Toronto Raptors', 'Malachi Flynn', 'AUTHOR_LOCKED'],
  ['30', 'Memphis Grizzlies', 'Desmond Bane', 'AUTHOR_LOCKED'],
  ['31', 'Dallas Mavericks', 'R.J. Hampton', 'AUTHOR_LOCKED'],
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
  'PICKS_25_TO_31_AUTHOR_LOCKED / TERRY_RELANDING_OPEN',
  'R.J. Hampton 31순위 `AUTHOR_APPROVED / LOCKED`',
  '선수 선택과 픽 거래의 경제는 분리',
  '후대 NBA 성과·부상·계약은 사용하지 않는다',
  'Quickley 25 → Pritchard 26 → Azubuike 27 → McDaniels 28 → Flynn 29 → Bane 30 유지 → Hampton 31',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('PICKS_25_TO_31_AUTHOR_LOCKED')) throw new Error('missing pick 25-31 author lock');
if (!review.includes('공개 내부 보드가 새로 확인된 것은 아니다')) throw new Error('missing Dallas evidence limit');
if (!review.includes('정확 1~31순위가 정본화됐다')) throw new Error('missing exact-pick lock');

console.log('PASS R.J. Hampton relanding board');
console.log('Picks 25-30 retained and Hampton 31 author-locked; Terry relanding open');
