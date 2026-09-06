const names = ['Selden', 'Harrison', 'Blakeney', 'TLC', 'Alkins', 'Brandon', 'JaKarr'];

const rows = [
  ['2019-01-27', 12, [4, 3, 5, 0, 0, 0, 0], [38, 9, 12, 0, 0, 0, 0]],
  ['2019-01-29', 12, [6, 5, 1, 0, 0, 0, 0], [28, 25, 7, 0, 0, 0, 0]],
  ['2019-01-30', 12, [4, 3, 0, 0, 0, 5, 0], [35, 24, 4, 0, 0, 12, 0]],
  ['2019-02-02', 12, [4, 3, 0, 0, 0, 5, 0], [35, 17, 0, 0, 0, 13, 0]],
  ['2019-02-06', 12, [5, 4, 0, 3, 0, 0, 0], [20, 26, 0, 19, 0, 0, 0]],
  ['2019-02-08', 14, [6, 4, 0, 4, 0, 0, 0], [25, 10, 1, 14, 0, 1, 0]],
  ['2019-02-09', 14, [5, 5, 0, 4, 0, 0, 0], [25, 14, 0, 17, 0, 2, 0]],
  ['2019-02-11', 14, [6, 4, 0, 4, 0, 0, 0], [21, 10, 0, 16, 0, 0, 0]],
  ['2019-02-13', 14, [5, 5, 0, 4, 0, 0, 0], [20, 16, 2, 17, 2, 0, 0]],
  ['2019-02-22', 12, [6, 6, 0, 0, 0, 0, 0], [24, 14, 0, 5, 0, 0, 0]],
  ['2019-02-23', 14, [5, 5, 0, 4, 0, 0, 0], [26, 19, 0, 11, 0, 0, 0]],
  ['2019-02-25', 15, [4, 3, 5, 3, 0, 0, 0], [29, 20, 15, 28, 0, 0, 0]],
  ['2019-02-27', 14, [6, 6, 0, 2, 0, 0, 0], [19, 19, 0, 8, 0, 0, 0]],
  ['2019-03-01', 14, [5, 5, 0, 4, 0, 0, 0], [32, 15, 0, 14, 0, 0, 0]],
  ['2019-03-03', 15, [4, 3, 5, 3, 0, 0, 0], [24, 27, 20, 19, 0, 0, 0]],
  ['2019-03-05', 12, [6, 6, 0, 0, 0, 0, 0], [24, 14, 0, 5, 0, 0, 0]],
  ['2019-03-06', 14, [6, 4, 0, 4, 0, 0, 0], [23, 10, 0, 14, 0, 0, 0]],
  ['2019-03-08', 14, [5, 5, 0, 4, 0, 0, 0], [16, 13, 0, 10, 0, 0, 0]],
  ['2019-03-10', 15, [4, 3, 5, 3, 0, 0, 0], [28, 32, 14, 24, 0, 0, 0]],
  ['2019-03-12', 15, [4, 3, 5, 3, 0, 0, 0], [14, 25, 11, 12, 0, 2, 0]],
  ['2019-03-15', 14, [5, 5, 0, 4, 0, 0, 0], [23, 19, 6, 15, 0, 0, 0]],
  ['2019-03-17', 16, [4, 4, 5, 3, 0, 0, 0], [24, 20, 12, 22, 0, 0, 0]],
  ['2019-03-18', 16, [4, 4, 5, 3, 0, 0, 0], [20, 32, 17, 14, 0, 0, 0]],
  ['2019-03-20', 16, [4, 4, 5, 3, 0, 0, 0], [20, 39, 23, 26, 0, 0, 0]],
  ['2019-03-23', 16, [3, 3, 4, 2, 0, 4, 0], [23, 39, 27, 20, 0, 17, 0]],
  ['2019-03-26', 16, [3, 3, 4, 2, 0, 4, 0], [40, 33, 21, 28, 0, 23, 0]],
  ['2019-03-27', 16, [2, 2, 3, 1, 5, 3, 0], [34, 30, 32, 21, 16, 30, 0]],
  ['2019-03-30', 16, [2, 2, 3, 1, 5, 3, 0], [20, 32, 18, 32, 18, 22, 0]],
  ['2019-04-01', 16, [2, 2, 3, 1, 0, 2, 6], [34, 30, 17, 26, 2, 8, 30]],
  ['2019-04-03', 16, [2, 1, 0, 1, 4, 2, 6], [16, 34, 0, 26, 26, 13, 29]],
  ['2019-04-06', 16, [2, 1, 0, 1, 4, 2, 6], [13, 23, 0, 27, 20, 25, 35]],
  ['2019-04-09', 16, [2, 1, 0, 1, 4, 2, 6], [20, 28, 0, 25, 13, 23, 33]],
  ['2019-04-10', 16, [2, 2, 3, 1, 5, 3, 0], [28, 20, 14, 30, 19, 23, 0]],
];

const aggregate = Array(names.length).fill(0);
for (const [date, protagonist, debit, actual] of rows) {
  const rowDebit = debit.reduce((a, b) => a + b, 0);
  if (rowDebit !== protagonist) throw new Error(`${date}: ${rowDebit} != ${protagonist}`);
  debit.forEach((value, index) => {
    if (value > 6) throw new Error(`${date} ${names[index]}: debit above 6`);
    if (value > 0 && actual[index] - value < 6) {
      throw new Error(`${date} ${names[index]}: fewer than 6 actual minutes remain`);
    }
    aggregate[index] += value;
  });
}

const expected = [137, 119, 61, 73, 27, 35, 24];
if (aggregate.some((value, index) => value !== expected[index])) {
  throw new Error(`aggregate mismatch: ${aggregate}`);
}

const postInjury = rows.reduce((sum, row) => sum + row[1], 0);
const missedAndAssignmentSeconds = 96 * 60 + 35;
const hutchisonSeconds = 894 * 60 + 37;
const protagonistSeconds = hutchisonSeconds - missedAndAssignmentSeconds + postInjury * 60;
const realPlayerNetDebit = postInjury * 60 - missedAndAssignmentSeconds;

if (postInjury !== 476) throw new Error(`post-injury total: ${postInjury}`);
if (protagonistSeconds !== 1274 * 60 + 2) throw new Error('protagonist total mismatch');
if (realPlayerNetDebit !== 379 * 60 + 25) throw new Error('net debit mismatch');

console.log('PASS Chicago 2018-19 ledger');
console.log(`33-game debit: ${postInjury}:00`);
console.log(`aggregate: ${names.map((name, i) => `${name} ${aggregate[i]}`).join(', ')}`);
console.log('protagonist: 73 GP, 11 GS, 1274:02');
console.log('real-player net debit: 379:25');
