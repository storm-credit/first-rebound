import fs from 'node:fs';
import path from 'node:path';

const root = new URL('../simulation/', import.meta.url);
const parse = text => {
  const lines = text.trim().split(/\r?\n/);
  const split = line => [...line.matchAll(/(?:^|,)("(?:[^"]|"")*"|[^,]*)/g)].map(m => m[1].replace(/^"|"$/g, '').replaceAll('""', '"'));
  const headers = split(lines.shift());
  return lines.map(line => Object.fromEntries(split(line).map((v,i) => [headers[i],v])));
};
const write = (name, rows) => {
  const headers = Object.keys(rows[0]);
  const cell = v => /[,"\n]/.test(String(v)) ? '"'+String(v).replaceAll('"','""')+'"' : String(v);
  fs.writeFileSync(new URL(name,root), [headers.join(','), ...rows.map(r => headers.map(k=>cell(r[k])).join(','))].join('\n')+'\n');
};
const sum = (rs,k) => rs.reduce((n,r)=>n+Number(r[k]),0);
const source = 'CHICAGO_2020_21_POSTDEADLINE_ACTUAL.csv';
if (process.argv[2]) {
  const raw = parse(fs.readFileSync(path.resolve(process.argv[2]),'utf8')).filter(r=>r.season_year==='2020-21' && r.teamTricode==='CHI');
  const seconds = r => r.minutes ? r.minutes.split(':').reduce((a,b)=>a*60+Number(b),0) : 0;
  const pre = raw.filter(r=>r.game_date<='2021-03-24');
  if (pre.reduce((n,r)=>n+seconds(r),0)!==625202 || new Set(pre.map(r=>r.gameId)).size!==43) throw Error('raw source fails existing 43-game reconciliation');
  write(source, raw.filter(r=>r.game_date>'2021-03-24').sort((a,b)=>a.game_date.localeCompare(b.game_date)||a.personName.localeCompare(b.personName)).map(r=>({game_id:r.gameId.padStart(10,'0'),date:r.game_date,matchup:r.matchup,player:r.personName,actual_seconds:seconds(r),actual_start:r.position?1:0,points:Number(r.points),plus_minus:Number(r.plusMinusPoints),comment:r.comment,source_url:'https://www.nba.com/game/'+r.gameId.padStart(10,'0')+'/box-score'})));
}
const actual = parse(fs.readFileSync(new URL(source,root),'utf8'));
const dates = [...new Set(actual.map(r=>r.date))].sort();
if (dates.length!==29) throw Error('29 dates required');
const removed = ['Patrick Williams','Nikola Vucevic','Al-Farouq Aminu','Troy Brown Jr.'];
const additions = ['Protagonist','LaMelo Ball','Wendell Carter Jr.','Otto Porter Jr.'];
const floors = [['Tomas Satoransky',600],['Denzel Valentine',360],['Ryan Arcidiacono',0],['Coby White',1200],['Garrett Temple',960]];
const vector=[],games=[];
for (const scenario of ['PORTER_ZERO','PORTER_12_STRESS','PORTER_CAPPED']) {
  for (const [i,date] of dates.entries()) {
    const rs=actual.filter(r=>r.date===date), map=new Map(rs.map(r=>[r.player,{...r,alternate_seconds:Number(r.actual_seconds),alternate_start:Number(r.actual_start),treatment:'OBSERVED_BASELINE_RETAINED'}]));
    for (const p of removed) if(map.has(p)) Object.assign(map.get(p),{alternate_seconds:0,alternate_start:0,treatment:'NOT_ON_ALTERNATE_ROSTER'});
    for (const p of additions) map.set(p,{player:p,actual_seconds:0,actual_start:0,alternate_seconds:0,alternate_start:0,treatment:'CONDITIONAL_AVAILABILITY'});
    map.get('Protagonist').alternate_seconds=1800;
    map.get('LaMelo Ball').alternate_seconds=1680;
    map.get('Wendell Carter Jr.').alternate_seconds=1560;
    map.get('Otto Porter Jr.').alternate_seconds=scenario==='PORTER_ZERO'?0:720;
    const theis=map.get('Daniel Theis');
    if(theis) theis.alternate_seconds=Math.min(theis.alternate_seconds,1440);
    let excess=sum([...map.values()],'alternate_seconds')-sum(rs,'actual_seconds');
    for (const [p,floor] of floors) {
      const r=map.get(p);if(!r || excess<=0)continue;
      const take=Math.min(excess,Math.max(0,r.alternate_seconds-floor));
      r.alternate_seconds-=take;excess-=take;if(take)r.treatment='SAME_DATE_DONOR';
    }
    if(excess>0 && scenario==='PORTER_CAPPED') {
      const r=map.get('Otto Porter Jr.'), take=Math.min(excess,r.alternate_seconds);
      r.alternate_seconds-=take;excess-=take;r.treatment='CONDITIONAL_PORTER_ROLE_CAP';
    }
    if(excess<0) {
      // Return unused minutes to existing rotation players, within the game clock.
      for(const p of ['Wendell Carter Jr.','Thaddeus Young','Daniel Theis','Garrett Temple']) {
        const r=map.get(p);if(!r || r.alternate_seconds===0)continue;
        const cap=p==='Wendell Carter Jr.'?1800:Math.max(Number(r.actual_seconds),1800);
        const credit=Math.min(-excess,Math.max(0,cap-r.alternate_seconds));
        r.alternate_seconds+=credit;excess+=credit;if(!excess)break;
      }
    }
    // Three new starters replace Patrick, the historical PG and the historical starting center.
    map.get('Protagonist').alternate_start=1;
    const pg=['Coby White','Tomas Satoransky'].find(p=>map.get(p)?.alternate_start===1);
    if(!pg)throw Error('missing historical PG '+date);
    map.get(pg).alternate_start=0;map.get('LaMelo Ball').alternate_start=1;
    if(!rs.some(r=>r.player==='Nikola Vucevic' && Number(r.actual_start))) {
      const center=['Daniel Theis','Thaddeus Young','Lauri Markkanen'].find(p=>map.get(p)?.alternate_start===1);
      if(!center)throw Error('missing starting center '+date);
      map.get(center).alternate_start=0;
    }
    map.get('Wendell Carter Jr.').alternate_start=1;
    const event_id='CHI_2020_21_G'+String(i+44).padStart(3,'0');
    const margin=sum(rs,'plus_minus')/5;
    games.push({scenario,event_id,game_id:rs[0].game_id,date,matchup:rs[0].matchup,actual_wl:margin>0?'W':'L',actual_points:sum(rs,'points'),actual_margin:margin,actual_team_seconds:sum(rs,'actual_seconds'),alternate_team_seconds:sum([...map.values()],'alternate_seconds'),unfunded_seconds:excess,alternate_starts:sum([...map.values()],'alternate_start'),status:excess===0?'CAPACITY_PASS_AVAILABILITY_HOLD':'CAPACITY_BLOCKED'});
    for(const r of map.values()) vector.push({scenario,event_id,date,player:r.player,actual_seconds:Number(r.actual_seconds),alternate_seconds:r.alternate_seconds,delta_seconds:r.alternate_seconds-Number(r.actual_seconds),actual_start:Number(r.actual_start),alternate_start:r.alternate_start,treatment:r.treatment});
  }
}
write('CHICAGO_2020_21_POSTDEADLINE_CAPACITY_GAMES.csv',games);
write('CHICAGO_2020_21_POSTDEADLINE_CAPACITY_VECTOR.csv',vector);
const budget=[];
for(const scenario of [...new Set(vector.map(r=>r.scenario))])for(const player of [...new Set(vector.map(r=>r.player))].sort()) {
 const rs=vector.filter(r=>r.scenario===scenario&&r.player===player);
 budget.push({scenario,player,actual_seconds:sum(rs,'actual_seconds'),alternate_seconds:sum(rs,'alternate_seconds'),delta_seconds:sum(rs,'delta_seconds'),alternate_gp:rs.filter(r=>r.alternate_seconds>0).length,alternate_gs:sum(rs,'alternate_start'),status:'CONDITIONAL_CAPACITY_NOT_CANON'});
}
write('CHICAGO_2020_21_POSTDEADLINE_CAPACITY_BUDGET.csv',budget);
console.log(JSON.stringify({dates:dates.length,actualSeconds:sum(actual,'actual_seconds'),blocked:games.filter(r=>r.unfunded_seconds!==0).map(r=>({date:r.date,scenario:r.scenario,seconds:r.unfunded_seconds})),budgets:budget.filter(r=>additions.includes(r.player))},null,2));
