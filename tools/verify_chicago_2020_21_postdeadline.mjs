import fs from 'node:fs';
import assert from 'node:assert/strict';
const read = name => {
 const lines=fs.readFileSync(new URL('../simulation/'+name,import.meta.url),'utf8').trim().split(/\r?\n/);
 const split=l=>[...l.matchAll(/(?:^|,)("(?:[^"]|"")*"|[^,]*)/g)].map(m=>m[1].replace(/^"|"$/g,'').replaceAll('""','"'));
 const keys=split(lines.shift());return lines.map(l=>Object.fromEntries(split(l).map((v,i)=>[keys[i],v])));
};
const a=read('CHICAGO_2020_21_POSTDEADLINE_ACTUAL.csv'),g=read('CHICAGO_2020_21_POSTDEADLINE_CAPACITY_GAMES.csv'),v=read('CHICAGO_2020_21_POSTDEADLINE_CAPACITY_VECTOR.csv'),b=read('CHICAGO_2020_21_POSTDEADLINE_CAPACITY_BUDGET.csv');
const sum=(rs,k)=>rs.reduce((n,r)=>n+Number(r[k]),0);
const roster=read('CHICAGO_2021_POSTDEADLINE_ROSTER.csv');
assert.equal(roster.length,17);assert.equal(new Set(roster.map(r=>r.player)).size,17);
assert.equal(roster.filter(r=>r.contract_class==='STANDARD').length,15);
assert.equal(roster.filter(r=>r.contract_class==='TWO_WAY').length,2);
for(const r of v)if(Number(r.alternate_seconds)>0)assert(roster.some(p=>p.player===r.player));
assert.equal(new Set(a.map(r=>r.game_id)).size,29);
assert.equal(new Set(a.map(r=>r.game_id+'|'+r.player)).size,a.length);
assert.equal(sum(a,'actual_seconds'),417603);
assert.equal(sum(a,'actual_start'),145);
assert.equal(a[0].date,'2021-03-27');assert.equal(a.at(-1).date,'2021-05-16');
assert.equal(g.length,87);assert.equal(new Set(g.map(r=>r.scenario+'|'+r.event_id)).size,87);
assert.equal(new Set(v.map(r=>r.scenario+'|'+r.event_id+'|'+r.player)).size,v.length);
for(const row of g){
 const actual=a.filter(r=>r.game_id===row.game_id), vector=v.filter(r=>r.scenario===row.scenario&&r.event_id===row.event_id);
 assert.equal(sum(actual,'actual_seconds'),Number(row.actual_team_seconds));
 assert.equal(sum(actual,'plus_minus')/5,Number(row.actual_margin));
 assert.equal(sum(actual,'points'),Number(row.actual_points));
 assert.equal(Number(row.alternate_starts),5);
 assert.equal(sum(vector,'alternate_start'),5);
 assert.equal(sum(vector,'actual_seconds'),Number(row.actual_team_seconds));
 assert.equal(sum(vector,'alternate_seconds'),Number(row.alternate_team_seconds));
 assert.equal(sum(vector,'delta_seconds'),Number(row.unfunded_seconds));
 if(row.scenario!=='PORTER_12_STRESS')assert.equal(Number(row.unfunded_seconds),0);
 for(const r of vector){
  assert(Number(r.alternate_seconds)>=0 && Number(r.alternate_seconds)<=2880);
  assert.equal(Number(r.alternate_seconds)-Number(r.actual_seconds),Number(r.delta_seconds));
  if(Number(r.alternate_start))assert(Number(r.alternate_seconds)>0);
  if(['Patrick Williams','Nikola Vucevic','Al-Farouq Aminu','Troy Brown Jr.'].includes(r.player))assert.equal(Number(r.alternate_seconds),0);
  if(['Zach LaVine','Lauri Markkanen','Javonte Green','Adam Mokoka','Devon Dotson','Cristiano Felicio'].includes(r.player))assert.equal(Number(r.delta_seconds),0);
 }
}
for(const row of b){
 const rs=v.filter(r=>r.scenario===row.scenario&&r.player===row.player);
 for(const k of ['actual_seconds','alternate_seconds','delta_seconds'])assert.equal(sum(rs,k),Number(row[k]));
 assert.equal(rs.filter(r=>Number(r.alternate_seconds)>0).length,Number(row.alternate_gp));
 assert.equal(sum(rs,'alternate_start'),Number(row.alternate_gs));
 assert.equal(row.status,'CONDITIONAL_CAPACITY_NOT_CANON');
}
const stress=g.filter(r=>r.scenario==='PORTER_12_STRESS'&&Number(r.unfunded_seconds)>0);
assert.equal(stress.length,5);assert.equal(sum(stress,'unfunded_seconds'),1724);
assert.deepEqual(stress.map(r=>r.date),['2021-05-06','2021-05-07','2021-05-11','2021-05-13','2021-05-16']);
const baseline=g.filter(r=>r.scenario==='PORTER_ZERO');
assert.equal(baseline.filter(r=>r.actual_wl==='W').length,12);
assert.equal(baseline.filter(r=>r.actual_wl==='L').length,17);
console.log('PASS O-15F6: actual 29 games / 12-17 / 6,960:03 / 145 starts');
console.log('Capacity: PORTER_ZERO and PORTER_CAPPED 29/29 conserved; fixed Porter 12-minute stress fails 5 games by 28:44');
console.log('Availability, five-player lineup feasibility, production and alternate outcomes remain HOLD');
