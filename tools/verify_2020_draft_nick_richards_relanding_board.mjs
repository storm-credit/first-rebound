import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_NICK_RICHARDS_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_NICK_RICHARDS_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_NICK_RICHARDS_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['43', 'Sacramento Kings', 'Jahmius Ramsey', 'RETENTION_LEAN'],
  ['44', 'Chicago Bulls', 'Marko Simonovic', 'RETENTION_STRONG_LEAN'],
  ['45', 'Milwaukee Bucks', 'Jordan Nwora', 'RETENTION_LEAN'],
  ['46', 'Portland Trail Blazers', 'CJ Elleby', 'RETENTION_LEAN'],
  ['47', 'Boston Celtics', 'Yam Madar', 'RETENTION_LEAN'],
  ['48', 'Golden State Warriors', 'Nico Mannion', 'RETENTION_LEAN'],
  ['49', 'Philadelphia 76ers', 'Isaiah Joe', 'RETENTION_STRONG_LEAN'],
  ['50', 'Atlanta Hawks', 'Skylar Mays', 'RETENTION_LEAN'],
  ['51', 'Golden State Warriors', 'Justinian Jessup', 'RETENTION_LEAN'],
  ['52', 'Houston Rockets', 'Kenyon Martin Jr.', 'RETENTION_STRONG_LEAN'],
  ['53', 'Washington Wizards', 'Cassius Winston', 'RETENTION_LEAN'],
  ['54', 'Indiana Pacers', 'Cassius Stanley', 'RETENTION_LEAN'],
  ['55', 'LA Clippers', 'Jay Scrubb', 'RETENTION_STRONG_LEAN'],
  ['56', 'Charlotte Hornets', 'Nick Richards', 'PRIMARY_LEAN_AUTHOR_GATE'],
];

if (primary.length !== expected.length) throw new Error(`expected 14 primary rows, got ${primary.length}`);
for (let index = 0; index < expected.length; index += 1) {
  const row = primary[index];
  const actual = [row.pick, row.team, row.rival_world_selection, row.status];
  if (actual.join('|') !== expected[index].join('|')) throw new Error(`primary pick ${index + 43} changed`);
}

const board = fs.readFileSync(boardPath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of [
  'PICKS_1_TO_42_AUTHOR_LOCKED / PICKS_43_TO_55_RETENTION_LEAN / PICK_56_AUTHOR_GATE',
  '후대 NBA 성과·부상·계약은 사용하지 않으며',
  '실제 43~55 유지 → Charlotte Nick Richards 56',
  'Grant Riller를 Brooklyn 통제 57순위부터 재판정',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('PICK_56_AUTHOR_GATE')) throw new Error('missing pick 56 author gate');
if (!review.includes('공개 Richards–Riller 내부 head-to-head는 아니다')) throw new Error('missing evidence limit');
if (!review.includes('정확 43~56순위는 작가 승인 전 `HOLD`')) throw new Error('missing exact-pick hold');

console.log('PASS Nick Richards relanding board');
console.log('Picks 43-55 retention lean; Richards 56 author-gated; Riller relanding conditional');
