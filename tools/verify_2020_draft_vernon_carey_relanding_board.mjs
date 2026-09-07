import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_VERNON_CAREY_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_VERNON_CAREY_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_VERNON_CAREY_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['33', 'LA Clippers', 'Daniel Oturu', 'AUTHOR_LOCKED'],
  ['34', 'Oklahoma City Thunder', 'Theo Maledon', 'AUTHOR_LOCKED'],
  ['35', 'Memphis Grizzlies', 'Xavier Tillman Sr.', 'AUTHOR_LOCKED'],
  ['36', 'Dallas Mavericks', 'Tyler Bey', 'AUTHOR_LOCKED'],
  ['37', 'Oklahoma City Thunder', 'Vit Krejci', 'AUTHOR_LOCKED'],
  ['38', 'Detroit Pistons', 'Saben Lee', 'AUTHOR_LOCKED'],
  ['39', 'Utah Jazz', 'Elijah Hughes', 'AUTHOR_LOCKED'],
  ['40', 'Sacramento Kings', 'Robert Woodard II', 'AUTHOR_LOCKED'],
  ['41', 'San Antonio Spurs', 'Tre Jones', 'AUTHOR_LOCKED'],
  ['42', 'Charlotte Hornets', 'Vernon Carey Jr.', 'AUTHOR_LOCKED'],
];

if (primary.length !== expected.length) throw new Error(`expected 10 primary rows, got ${primary.length}`);
for (let index = 0; index < expected.length; index += 1) {
  const row = primary[index];
  const actual = [row.pick, row.team, row.rival_world_selection, row.status];
  if (actual.join('|') !== expected[index].join('|')) throw new Error(`primary pick ${index + 33} changed`);
}

const board = fs.readFileSync(boardPath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of [
  'PICKS_1_TO_42_AUTHOR_LOCKED / RICHARDS_RELANDING_OPEN',
  '선수 선택과 거래 경제는 분리',
  '후대 NBA 성과·부상·계약은 사용하지 않으며',
  '실제 33~41 유지 → Charlotte Vernon Carey Jr. 42',
  'Nick Richards를 Sacramento 43순위부터 재판정',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('PICKS_33_TO_42_AUTHOR_LOCKED')) throw new Error('missing picks 33-42 author lock');
if (!review.includes('공개 내부 보드가 확인된 것으로 과장하지 않으며')) throw new Error('missing evidence limit');
if (!review.includes('Richards는 43순위부터 재판정')) throw new Error('missing Richards relanding boundary');

console.log('PASS Vernon Carey Jr. relanding board');
console.log('Picks 33-41 retained and Carey 42 author-locked; Richards relanding open');
