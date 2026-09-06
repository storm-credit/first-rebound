import fs from 'node:fs';

const csvPath = new URL('../simulation/RIVAL_2020_WEST_TEAM_CANDIDATES.csv', import.meta.url);
const packetPath = new URL('../design/RIVAL_2020_WEST_TEAM_DECISION_PACKET.md', import.meta.url);
const lines = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
const header = lines.shift().split(',');
const rows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [header[index], value])));

const expected = [
  ['A', 'Minnesota Timberwolves', 'direct_pick', '1'],
  ['B', 'Golden State Warriors', 'direct_pick', '2'],
  ['C', 'San Antonio Spurs', 'trade_up_to_2', '11'],
  ['D', 'Oklahoma City Thunder', 'trade_up_to_2', '25'],
];

if (rows.length !== expected.length) throw new Error(`expected 4 options, got ${rows.length}`);
for (let index = 0; index < expected.length; index += 1) {
  const actual = [rows[index].option, rows[index].team, rows[index].entry_path, rows[index].actual_pick];
  if (actual.join('|') !== expected[index].join('|')) throw new Error(`option ${index + 1} changed`);
}

const packet = fs.readFileSync(packetPath, 'utf8');
for (const marker of [
  'AUTHOR_SELECTED_A / MINNESOTA_1_LOCKED',
  '작가 선택 / LOCKED',
  '한 명씩 자동으로 아래 순번으로 미는 방식은 금지',
  'Minnesota가 전체 1순위로 지명',
]) {
  if (!packet.includes(marker)) throw new Error(`missing firewall: ${marker}`);
}

console.log('PASS rival 2020 western team decision packet');
console.log('Minnesota #1 author lock / 3 historical contingencies preserved');
