import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_NICK_RICHARDS_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_NICK_RICHARDS_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_NICK_RICHARDS_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['43', 'Sacramento Kings', 'Jahmius Ramsey', 'AUTHOR_LOCKED'],
  ['44', 'Chicago Bulls', 'Marko Simonovic', 'AUTHOR_LOCKED'],
  ['45', 'Milwaukee Bucks', 'Jordan Nwora', 'AUTHOR_LOCKED'],
  ['46', 'Portland Trail Blazers', 'CJ Elleby', 'AUTHOR_LOCKED'],
  ['47', 'Boston Celtics', 'Yam Madar', 'AUTHOR_LOCKED'],
  ['48', 'Golden State Warriors', 'Nico Mannion', 'AUTHOR_LOCKED'],
  ['49', 'Philadelphia 76ers', 'Isaiah Joe', 'AUTHOR_LOCKED'],
  ['50', 'Atlanta Hawks', 'Skylar Mays', 'AUTHOR_LOCKED'],
  ['51', 'Golden State Warriors', 'Justinian Jessup', 'AUTHOR_LOCKED'],
  ['52', 'Houston Rockets', 'Kenyon Martin Jr.', 'AUTHOR_LOCKED'],
  ['53', 'Washington Wizards', 'Cassius Winston', 'AUTHOR_LOCKED'],
  ['54', 'Indiana Pacers', 'Cassius Stanley', 'AUTHOR_LOCKED'],
  ['55', 'LA Clippers', 'Jay Scrubb', 'AUTHOR_LOCKED'],
  ['56', 'Charlotte Hornets', 'Nick Richards', 'AUTHOR_LOCKED'],
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
  'PICKS_1_TO_56_AUTHOR_LOCKED / RILLER_RELANDING_OPEN',
  '후대 NBA 성과·부상·계약은 사용하지 않으며',
  '실제 43~55 유지 → Charlotte Nick Richards 56',
  'Grant Riller를 Brooklyn 통제 57순위부터 재판정',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('PICKS_43_TO_56_AUTHOR_LOCKED')) throw new Error('missing picks 43-56 author lock');
if (!review.includes('공개 Richards–Riller 내부 head-to-head는 아니다')) throw new Error('missing evidence limit');
if (!review.includes('Riller는 57순위부터 재판정')) throw new Error('missing Riller relanding boundary');

console.log('PASS Nick Richards relanding board');
console.log('Picks 43-55 retained and Richards 56 author-locked; Riller relanding open');
