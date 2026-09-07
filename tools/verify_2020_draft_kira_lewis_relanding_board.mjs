import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_KIRA_LEWIS_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_KIRA_LEWIS_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_KIRA_LEWIS_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['14', 'Boston Celtics', 'Aaron Nesmith', 'AUTHOR_LOCKED'],
  ['15', 'Orlando Magic', 'Cole Anthony', 'AUTHOR_LOCKED'],
  ['16', 'Detroit Pistons', 'Kira Lewis Jr.', 'PRIMARY_LEAN_AUTHOR_GATE'],
];

if (primary.length !== expected.length) throw new Error(`expected 3 primary rows, got ${primary.length}`);
for (let index = 0; index < expected.length; index += 1) {
  const row = primary[index];
  const actual = [row.pick, row.team, row.rival_world_selection, row.status];
  if (actual.join('|') !== expected[index].join('|')) throw new Error(`primary pick ${index + 14} changed`);
}

const board = fs.readFileSync(boardPath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of [
  'AUTHOR_APPROVED / PICKS_14_TO_15_LOCKED / DETROIT_16_AUTHOR_GATE',
  'Aaron Nesmith 14순위 `AUTHOR_APPROVED / LOCKED`',
  'Cole Anthony 15순위 유지 `AUTHOR_APPROVED / LOCKED`',
  'Kira Lewis Jr. 16순위 `PRIMARY_LEAN / AUTHOR_APPROVAL_REQUIRED`',
  '실제 세계에서 Kira가 13번에 이미 사라졌으므로',
  '후대 NBA 성과·부상·계약은 사용하지 않는다',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('AUTHOR_RESOLVED_TO_15')) throw new Error('missing author resolution');
if (!review.includes('PICK16_TEAM_BOARD_BLOCKER')) throw new Error('missing pick-16 blocker');
if (!review.includes('지명 뒤 발언')) throw new Error('missing post-draft evidence limit');

console.log('PASS Kira Lewis Jr. relanding board');
console.log('Nesmith 14 / Cole 15 author-locked; Detroit Kira/Stewart pick 16 author-gated');
