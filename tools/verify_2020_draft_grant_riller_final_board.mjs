import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_GRANT_RILLER_FINAL_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_GRANT_RILLER_FINAL_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_GRANT_RILLER_FINAL_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [
  ['57', 'Brooklyn Nets', 'Reggie Perry', 'RETENTION_STRONG_LEAN'],
  ['58', 'Philadelphia 76ers', 'Paul Reed', 'RETENTION_STRONG_LEAN'],
  ['59', 'Toronto Raptors', 'Jalen Harris', 'RETENTION_STRONG_LEAN'],
  ['60', 'Milwaukee Bucks', 'Sam Merrill', 'RETENTION_STRONG_LEAN'],
  ['UDFA', 'Free-agent market', 'Grant Riller', 'PRIMARY_LEAN_AUTHOR_GATE'],
];

if (primary.length !== expected.length) throw new Error(`expected 5 primary rows, got ${primary.length}`);
for (let index = 0; index < expected.length; index += 1) {
  const row = primary[index];
  const actual = [row.pick, row.team, row.rival_world_selection, row.status];
  if (actual.join('|') !== expected[index].join('|')) throw new Error(`primary row ${index + 1} changed`);
}

const board = fs.readFileSync(boardPath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of [
  'PICKS_1_TO_56_AUTHOR_LOCKED / PICKS_57_TO_60_RETENTION_LEAN / UNDRAFTED_AUTHOR_GATE',
  '후대 NBA 성과·징계·계약은 사용하지 않으며',
  '실제 57~60 유지 → Grant Riller 미지명 자유계약 시장',
  '정확 자유계약 팀·계약 종류는 `HOLD`',
  'World Bible 남은 매크로 게이트 2인 Chicago 2020-21 시즌 원장',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('UNDRAFTED_AUTHOR_GATE')) throw new Error('missing undrafted author gate');
if (!review.includes('Riller와의 공개 head-to-head는 아니다')) throw new Error('missing Toronto evidence limit');
if (!review.includes('정확 팀·계약은 Chicago 2020-21 opening roster 원장과 분리해 `HOLD`')) throw new Error('missing contract hold');

console.log('PASS Grant Riller final board');
console.log('Picks 57-60 retention lean; Riller undrafted-market author gate');
