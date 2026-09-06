const minutes = 1274 + 2 / 60;
const cohort = {
  PTS: [12.2, 11.7, 9.2, 7.1, 14.9, 7.9, 13.0, 10.9, 10.8],
  TRB: [7.2, 4.5, 7.4, 4.4, 6.8, 4.6, 6.6, 2.9, 5.9],
  AST: [3.9, 1.9, 1.4, 4.1, 1.4, 2.3, 1.2, 3.0, 1.2],
  STL: [1.0, 1.8, 0.9, 0.9, 1.1, 1.0, 1.4, 1.1, 1.3],
  BLK: [0.2, 0.7, 0.2, 0.5, 0.7, 0.9, 0.7, 0.1, 1.0],
  TS: [.487, .492, .507, .374, .545, .469, .497, .447, .489],
  threePA: [3.4, 4.4, 2.0, 2.6, 5.1, 2.3, 1.6, 7.3, 3.7],
  threeP: [.319, .279, .280, .267, .315, .258, .167, .326, .250],
  BPM: [-2.7, -3.1, -3.9, -8.2, -2.6, -3.3, -4.2, -5.0, -3.4],
};

const median = values => {
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[(sorted.length - 1) / 2];
};

const expectedMedians = {PTS: 10.9, TRB: 5.9, AST: 1.9, STL: 1.1, BLK: .7, TS: .489, threePA: 3.4, threeP: .279, BPM: -3.4};
for (const [key, expected] of Object.entries(expectedMedians)) {
  if (median(cohort[key]) !== expected) throw new Error(`${key} median mismatch`);
}

const prior = {
  PTS: [8.0, 9.5, 11.0], TRB: [7.5, 8.5, 9.5], AST: [1.2, 1.7, 2.2],
  STL: [1.0, 1.3, 1.6], BLK: [.5, .8, 1.1], TOV: [2.2, 1.8, 1.4],
  PF: [4.2, 3.6, 3.0], TS: [.470, .500, .530], threePA: [1.5, 2.3, 3.1],
  threeP: [.240, .280, .320], BPM: [-4.2, -3.0, -1.8],
};

for (const key of ['PTS', 'TRB', 'AST', 'STL', 'BLK', 'TS', 'threePA', 'threeP', 'BPM']) {
  if (!(prior[key][0] <= prior[key][1] && prior[key][1] <= prior[key][2])) throw new Error(`${key} range order`);
}
for (const key of ['TOV', 'PF']) {
  if (!(prior[key][0] >= prior[key][1] && prior[key][1] >= prior[key][2])) throw new Error(`${key} inverse range order`);
}

const totals = value => Math.round(value * minutes / 36);
const expectedTotals = {PTS: [283, 336, 389], TRB: [265, 301, 336], AST: [42, 60, 78], STL: [35, 46, 57], BLK: [18, 28, 39]};
for (const [key, expected] of Object.entries(expectedTotals)) {
  const actual = prior[key].map(totals);
  if (actual.some((value, i) => value !== expected[i])) throw new Error(`${key} total mismatch: ${actual}`);
}

const debitMinutes = [137, 119, 61, 73, 27, 35, 24].reduce((a, b) => a + b, 0);
const returnSeconds = [22 * 60, 27 * 60, 15 * 60, 15 * 60 + 44, 16 * 60 + 51].reduce((a, b) => a + b, 0);
if (debitMinutes !== 476) throw new Error('debit minutes mismatch');
if (returnSeconds !== 96 * 60 + 35) throw new Error('return clock mismatch');

console.log('PASS Chicago 2018-19 production priors');
console.log('cohort medians verified');
console.log('protagonist ranges and 1,274:02 conversions verified');
console.log('476:00 debit and 96:35 return clocks verified');
