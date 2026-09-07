import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_ISAIAH_STEWART_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_ISAIAH_STEWART_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_ISAIAH_STEWART_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['17', 'Oklahoma City Thunder', 'Aleksej Pokusevski', 'RETENTION_STRONG_LEAN'],
  ['18', 'Dallas Mavericks', 'Josh Green', 'RETENTION_LEAN'],
  ['19', 'Detroit Pistons', 'Isaiah Stewart', 'PRIMARY_LEAN_AUTHOR_GATE'],
];

if (primary.length !== expected.length) throw new Error(`expected 3 primary rows, got ${primary.length}`);
for (let index = 0; index < expected.length; index += 1) {
  const row = primary[index];
  const actual = [row.pick, row.team, row.rival_world_selection, row.status];
  if (actual.join('|') !== expected[index].join('|')) throw new Error(`primary pick ${index + 17} changed`);
}

const board = fs.readFileSync(boardPath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of [
  'KIRA_16_AUTHOR_LOCKED / PICKS_17_TO_19_AUTHOR_GATE',
  'Aleksej Pokuševski 17순위 `RETENTION_STRONG_LEAN`',
  'Josh Green 18순위 `RETENTION_LEAN`',
  'Isaiah Stewart 19순위 `PRIMARY_LEAN / AUTHOR_APPROVAL_REQUIRED`',
  '후대 NBA 성과·부상·계약은 사용하지 않는다',
  '픽 번호와 통제 구단을 분리한다',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('PICKS_17_TO_19_AUTHOR_GATE')) throw new Error('missing pick 17-19 author gate');
if (!review.includes('Green–Stewart 공개 head-to-head는 아니다')) throw new Error('missing Dallas evidence limit');
if (!review.includes('정확 17~19순위는 작가 승인 전 `HOLD`')) throw new Error('missing exact-pick hold');

console.log('PASS Isaiah Stewart relanding board');
console.log('Poku 17 / Green 18 retained as leans; Stewart 19 author-gated');
