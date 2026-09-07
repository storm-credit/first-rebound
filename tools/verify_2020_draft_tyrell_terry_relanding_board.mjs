import fs from 'node:fs';

const csvPath = new URL('../simulation/2020_DRAFT_TYRELL_TERRY_RELANDING_BOARD.csv', import.meta.url);
const boardPath = new URL('../simulation/2020_DRAFT_TYRELL_TERRY_RELANDING_BOARD.md', import.meta.url);
const reviewPath = new URL('../reviews/R01_2020_DRAFT_TYRELL_TERRY_RELANDING_REVIEW.md', import.meta.url);

const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));
const primary = rows.filter((row) => row.branch === 'PRIMARY');

const expected = [['32', 'Charlotte Hornets', 'Tyrell Terry', 'AUTHOR_LOCKED']];
if (primary.length !== expected.length) throw new Error(`expected 1 primary row, got ${primary.length}`);
const actual = [primary[0].pick, primary[0].team, primary[0].rival_world_selection, primary[0].status];
if (actual.join('|') !== expected[0].join('|')) throw new Error('primary pick 32 changed');

const board = fs.readFileSync(boardPath, 'utf8');
const review = fs.readFileSync(reviewPath, 'utf8');
for (const marker of [
  'PICKS_1_TO_32_AUTHOR_LOCKED / CAREY_RELANDING_OPEN',
  'Tyrell Terry 32**를 `AUTHOR_APPROVED / LOCKED`',
  '공개된 Terry–Carey 내부 head-to-head는 확인되지 않았다',
  '후대 NBA 성과·부상·계약은 사용하지 않는다',
  'Carey를 LA Clippers 통제 33순위부터 재판정',
]) {
  if (!board.includes(marker)) throw new Error(`missing board firewall: ${marker}`);
}
if (!review.includes('PICK_32_AUTHOR_LOCKED')) throw new Error('missing pick 32 author lock');
if (!review.includes('Graham·Rozier를 보존한다')) throw new Error('missing Charlotte roster firewall');
if (!review.includes('공개 내부 보드가 새로 확인된 것은 아니다')) throw new Error('missing evidence limit');

console.log('PASS Tyrell Terry relanding board');
console.log('Terry 32 author-locked; Carey relanding open');
