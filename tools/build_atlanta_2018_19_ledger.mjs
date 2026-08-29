import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputPath = process.argv[2] ?? "simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx";
const previewDir = process.argv[3] ?? "/tmp/atlanta_ledger_previews";

const games = [
  [1,"2018-10-17","A","New York Knicks","L",107,126,0],
  [2,"2018-10-19","A","Memphis Grizzlies","L",117,131,0],
  [3,"2018-10-21","A","Cleveland Cavaliers","W",133,111,0],
  [4,"2018-10-24","H","Dallas Mavericks","W",111,104,0],
  [5,"2018-10-27","H","Chicago Bulls","L",85,97,0],
  [6,"2018-10-29","A","Philadelphia 76ers","L",92,113,0],
  [7,"2018-10-30","A","Cleveland Cavaliers","L",114,136,0],
  [8,"2018-11-01","H","Sacramento Kings","L",115,146,0],
  [9,"2018-11-03","H","Miami Heat","W",123,118,0],
  [10,"2018-11-06","A","Charlotte Hornets","L",102,113,0],
  [11,"2018-11-07","H","New York Knicks","L",107,112,0],
  [12,"2018-11-09","H","Detroit Pistons","L",109,124,0],
  [13,"2018-11-11","A","Los Angeles Lakers","L",106,107,0],
  [14,"2018-11-13","A","Golden State Warriors","L",103,110,0],
  [15,"2018-11-15","A","Denver Nuggets","L",93,138,0],
  [16,"2018-11-17","A","Indiana Pacers","L",89,97,0],
  [17,"2018-11-19","H","Los Angeles Clippers","L",119,127,0],
  [18,"2018-11-21","H","Toronto Raptors","L",108,124,0],
  [19,"2018-11-23","H","Boston Celtics","L",96,114,0],
  [20,"2018-11-25","H","Charlotte Hornets","W",124,123,0],
  [21,"2018-11-27","A","Miami Heat","W",115,113,0],
  [22,"2018-11-28","A","Charlotte Hornets","L",94,108,0],
  [23,"2018-11-30","A","Oklahoma City Thunder","L",109,124,0],
  [24,"2018-12-03","H","Golden State Warriors","L",111,128,0],
  [25,"2018-12-05","H","Washington Wizards","L",117,131,0],
  [26,"2018-12-08","H","Denver Nuggets","W",106,98,0],
  [27,"2018-12-12","A","Dallas Mavericks","L",107,114,0],
  [28,"2018-12-14","A","Boston Celtics","L",108,129,0],
  [29,"2018-12-16","A","Brooklyn Nets","L",127,144,0],
  [30,"2018-12-18","H","Washington Wizards","W",118,110,0],
  [31,"2018-12-21","A","New York Knicks","W",114,107,0],
  [32,"2018-12-23","A","Detroit Pistons","W",98,95,0],
  [33,"2018-12-26","H","Indiana Pacers","L",121,129,0],
  [34,"2018-12-28","A","Minnesota Timberwolves","W",123,120,1],
  [35,"2018-12-29","H","Cleveland Cavaliers","W",111,108,0],
  [36,"2018-12-31","A","Indiana Pacers","L",108,116,0],
  [37,"2019-01-02","A","Washington Wizards","L",98,114,0],
  [38,"2019-01-04","A","Milwaukee Bucks","L",112,144,0],
  [39,"2019-01-06","H","Miami Heat","W",106,82,0],
  [40,"2019-01-08","A","Toronto Raptors","L",101,104,0],
  [41,"2019-01-09","A","Brooklyn Nets","L",100,116,0],
  [42,"2019-01-11","A","Philadelphia 76ers","W",123,121,0],
  [43,"2019-01-13","H","Milwaukee Bucks","L",114,133,0],
  [44,"2019-01-15","H","Oklahoma City Thunder","W",142,126,0],
  [45,"2019-01-19","H","Boston Celtics","L",105,113,0],
  [46,"2019-01-21","H","Orlando Magic","L",103,122,0],
  [47,"2019-01-23","A","Chicago Bulls","W",121,101,0],
  [48,"2019-01-26","A","Portland Trail Blazers","L",111,120,0],
  [49,"2019-01-28","A","Los Angeles Clippers","W",123,118,0],
  [50,"2019-01-30","A","Sacramento Kings","L",113,135,0],
  [51,"2019-02-01","A","Utah Jazz","L",112,128,0],
  [52,"2019-02-02","A","Phoenix Suns","W",118,112,0],
  [53,"2019-02-04","A","Washington Wizards","W",137,129,0],
  [54,"2019-02-07","H","Toronto Raptors","L",101,119,0],
  [55,"2019-02-09","H","Charlotte Hornets","L",120,129,0],
  [56,"2019-02-10","H","Orlando Magic","L",108,124,0],
  [57,"2019-02-12","H","Los Angeles Lakers","W",117,113,0],
  [58,"2019-02-14","H","New York Knicks","L",91,106,0],
  [59,"2019-02-22","H","Detroit Pistons","L",122,125,0],
  [60,"2019-02-23","H","Phoenix Suns","W",120,112,0],
  [61,"2019-02-25","A","Houston Rockets","L",111,119,0],
  [62,"2019-02-27","H","Minnesota Timberwolves","W",131,123,1],
  [63,"2019-03-01","H","Chicago Bulls","L",161,168,4],
  [64,"2019-03-03","A","Chicago Bulls","W",123,118,0],
  [65,"2019-03-04","A","Miami Heat","L",113,114,0],
  [66,"2019-03-06","H","San Antonio Spurs","L",104,111,0],
  [67,"2019-03-09","H","Brooklyn Nets","L",112,114,0],
  [68,"2019-03-10","H","New Orleans Pelicans","W",128,116,0],
  [69,"2019-03-13","H","Memphis Grizzlies","W",132,111,0],
  [70,"2019-03-16","A","Boston Celtics","L",120,129,0],
  [71,"2019-03-17","A","Orlando Magic","L",91,101,0],
  [72,"2019-03-19","H","Houston Rockets","L",105,121,0],
  [73,"2019-03-21","H","Utah Jazz","W",117,114,0],
  [74,"2019-03-23","H","Philadelphia 76ers","W",129,127,0],
  [75,"2019-03-26","A","New Orleans Pelicans","W",130,120,0],
  [76,"2019-03-29","H","Portland Trail Blazers","L",98,118,0],
  [77,"2019-03-31","H","Milwaukee Bucks","W",136,135,1],
  [78,"2019-04-02","A","San Antonio Spurs","L",111,117,0],
  [79,"2019-04-03","H","Philadelphia 76ers","W",130,122,0],
  [80,"2019-04-05","A","Orlando Magic","L",113,149,0],
  [81,"2019-04-07","A","Milwaukee Bucks","L",107,115,0],
  [82,"2019-04-10","H","Indiana Pacers","L",134,135,0],
];

// HoopsStats' published game log reports tenths of a minute and sums to the
// 805-minute public season total. The vector is a donor ledger, not a copy of
// Spellman's starts, injury, or production for the fictional protagonist.
const spellmanGameMinutes = new Map([
  ["2018-10-17",8.3],["2018-10-21",23.8],["2018-10-24",15.7],["2018-10-27",14.7],
  ["2018-10-29",23.3],["2018-10-30",20.4],["2018-11-01",20.5],["2018-11-03",20.2],
  ["2018-11-06",16.8],["2018-11-07",28.5],["2018-11-09",26.7],["2018-11-11",27.9],
  ["2018-11-13",14.2],["2018-11-15",26.7],["2018-11-17",12.4],["2018-11-19",14.1],
  ["2018-11-23",7.8],["2018-11-25",13.5],["2018-11-27",20.3],["2018-11-28",21.6],
  ["2018-11-30",15.2],["2018-12-03",7.7],["2018-12-26",7.4],["2019-01-06",2.7],
  ["2019-01-11",2.9],["2019-01-13",29.9],["2019-01-15",21.9],["2019-01-19",15.4],
  ["2019-01-21",16.7],["2019-01-23",19.6],["2019-01-26",15.1],["2019-01-28",10.5],
  ["2019-01-30",24.1],["2019-02-01",18.7],["2019-02-02",7.1],["2019-02-04",29.9],
  ["2019-02-07",15.3],["2019-02-09",11.9],["2019-02-10",26.3],["2019-02-12",13.7],
  ["2019-02-14",17.1],["2019-02-22",18.7],["2019-02-23",21.5],["2019-02-25",20.0],
  ["2019-02-27",19.4],["2019-03-01",18.9],
]);

const missedRotationDate = "2018-11-19";
const erieAssignmentStart = "2018-12-07";
const erieAssignmentEnd = "2018-12-22";
const erieGames = [
  [1,"2018-12-08","A","South Bay Lakers","24-30","S43"],
  [2,"2018-12-10","A","Stockton Kings","24-30","S43"],
  [3,"2018-12-13","A","Agua Caliente Clippers","24-30","S43"],
  [4,"2018-12-15","A","Santa Cruz Warriors","24-30","S43"],
  [5,"2018-12-19","H","Texas Legends","24-30","S43"],
  [6,"2018-12-21","A","Northern Arizona Suns","24-30","S43"],
];

function atlCounterfactualRow(game) {
  const date = game[1];
  const donor = spellmanGameMinutes.get(date) ?? 0;
  const eligible = donor >= 7;
  const planned = eligible ? Math.min(16, donor) : 0;
  const storySelected = date === missedRotationDate;
  const protagonistMinutes = storySelected ? 0 : planned;
  const reserveReceiver = Number((donor - protagonistMinutes).toFixed(1));
  const onAssignment = date >= erieAssignmentStart && date <= erieAssignmentEnd;
  const status = storySelected
    ? "MISSED_ROTATION"
    : protagonistMinutes > 0
      ? "ACTIVE"
      : onAssignment
        ? "ERIE_ASSIGNMENT"
        : donor > 0
          ? "LT_7_MIN_GATE"
          : "DNP";
  return {
    contact: protagonistMinutes > 0 ? "DIRECT" : "ROSTER",
    storySelected,
    status,
    protagonistMinutes,
    donor,
    reserveReceiver,
  };
}

const roster = [
  ["Trae Young","G",81,81,2503,"PROTECTED_CORE"],
  ["Kevin Huerter","G",75,59,2048,"PROTECTED_CORE"],
  ["DeAndre' Bembry","SF",82,15,1931,"PROTECTED_ROLE"],
  ["John Collins","F",61,59,1829,"PROTECTED_CORE"],
  ["Kent Bazemore","G",67,35,1643,"PROTECTED_ROLE"],
  ["Dewayne Dedmon","C",64,52,1609,"CENTER_POOL"],
  ["Taurean Prince","SF",55,47,1552,"PROTECTED_ROLE"],
  ["Alex Len","C",77,31,1544,"CENTER_POOL"],
  ["Vince Carter","F",76,9,1330,"PROTECTED_ROLE"],
  ["Jeremy Lin","G",51,1,1003,"GUARD_POOL"],
  ["Omari Spellman","F",46,11,805,"PRIMARY_REPLACED_SLOT"],
  ["Justin Anderson","SF",48,4,463,"FALLBACK_FORWARD"],
  ["Jaylen Adams","G",34,1,428,"GUARD_POOL"],
  ["Alex Poythress","F",21,1,305,"FALLBACK_FORWARD"],
  ["Tyler Dorsey","G",27,0,251,"GUARD_POOL"],
  ["Daniel Hamilton","G-F",19,3,204,"RESERVE"],
  ["Miles Plumlee","F-C",18,0,173,"CENTER_POOL"],
  ["Deyonta Davis","C",9,0,118,"CENTER_POOL"],
  ["Isaac Humphries","C",5,1,56,"CENTER_POOL"],
  ["B.J. Johnson","SF",6,0,43,"FALLBACK_FORWARD"],
  ["Tyler Zeller","F-C",2,0,11,"CENTER_POOL"],
  ["Jordan Sibert","SG",1,0,4,"RESERVE"],
];

const draftBoard = [
  [30,"Atlanta Hawks","Omari Spellman","Own pick","Atlanta Hawks","Fictional protagonist","CHANGED","Protagonist","The new player occupies Atlanta's actual #30 slot.","Atlanta roster/minutes rerun","S12/S13"],
  [31,"Phoenix Suns","Elie Okobo","Own pick","Phoenix Suns","Elie Okobo","UNCHANGED","None","Guard-development choice remains rational.","Actual path preserved","S13"],
  [32,"Memphis Grizzlies","Jevon Carter","Own pick","Memphis Grizzlies","Jevon Carter","UNCHANGED","None","Point-of-attack guard need remains distinct.","Actual path preserved","S13"],
  [33,"Dallas Mavericks","Jalen Brunson","Own pick","Dallas Mavericks","Jalen Brunson","UNCHANGED","None","Lead-guard depth remains the stronger fit.","Actual path preserved","S13"],
  [34,"Charlotte Hornets","Devonte' Graham","Rights from ATL for 2019 + 2023 seconds","Charlotte Hornets","Devonte' Graham","UNCHANGED","None","Charlotte paid two future seconds for a directed guard choice.","ATL asset trade preserved","S13"],
  [35,"Orlando Magic","Melvin Frazier","Own pick","Orlando Magic","Melvin Frazier","UNCHANGED","None","Wing-development lane remains distinct.","Actual path preserved","S13"],
  [36,"New York Knicks","Mitchell Robinson","Own pick","New York Knicks","Mitchell Robinson","UNCHANGED","None","Robinson's upside remains the board priority.","Actual path preserved","S13"],
  [37,"Portland Trail Blazers","Gary Trent Jr.","Rights from SAC","Portland Trail Blazers","Gary Trent Jr.","UNCHANGED","None","Perimeter shooting/development need remains.","Actual path preserved","S13"],
  [38,"Detroit Pistons","Khyri Thomas","Rights from PHI","Detroit Pistons","Khyri Thomas","UNCHANGED","None","Perimeter defense need remains distinct.","Actual path preserved","S13"],
  [39,"Los Angeles Lakers","Isaac Bonga","Rights from PHI","Los Angeles Lakers","Isaac Bonga","UNCHANGED","None","Lakers already used #25 on stretch big Moritz Wagner.","Actual path preserved","S13"],
  [40,"Brooklyn Nets","Rodions Kurucs","Own pick","Brooklyn Nets","Rodions Kurucs","UNCHANGED","None","Long-running Kurucs scouting interest remains decisive.","Actual path preserved","S17"],
  [41,"Denver Nuggets","Jarred Vanderbilt","Rights from ORL","Denver Nuggets","Jarred Vanderbilt","UNCHANGED","None","Vanderbilt upside remains the preferred development bet.","Actual path preserved","S13"],
  [42,"Detroit Pistons","Bruce Brown","Own pick","Detroit Pistons","Bruce Brown","UNCHANGED","None","Guard/wing role remains distinct.","Actual path preserved","S13"],
  [43,"Orlando Magic","Justin Jackson","Rights from DEN","Orlando Magic","Justin Jackson","UNCHANGED","None","Wing-development lane remains distinct.","Actual path preserved","S13"],
  [44,"Washington Wizards","Issuf Sanon","Own pick; overseas stash","Washington Wizards","Issuf Sanon","UNCHANGED","None","Roster/cap plan explicitly favored an overseas stash.","Actual path preserved","S16"],
  [45,"Oklahoma City Thunder","Hamidou Diallo","Rights via BKN/CHA","Oklahoma City Thunder","Hamidou Diallo","UNCHANGED","None","Athletic guard target remains distinct.","Actual path preserved","S13"],
  [46,"Houston Rockets","De'Anthony Melton","Own pick","Houston Rockets","De'Anthony Melton","UNCHANGED","None","Guard asset profile remains distinct.","Actual path preserved","S13"],
  [47,"Los Angeles Lakers","Svi Mykhailiuk","Own pick","Los Angeles Lakers","Svi Mykhailiuk","UNCHANGED","None","Shooting role remains distinct.","Actual path preserved","S13"],
  [48,"Minnesota Timberwolves","Keita Bates-Diop","Own pick","Minnesota Timberwolves","Keita Bates-Diop","UNCHANGED","None","Wing-forward choice does not require a cascade.","Actual path preserved","S13"],
  [49,"San Antonio Spurs","Chimezie Metu","Own pick","San Antonio Spurs","Omari Spellman","CHANGED","Spellman","Spellman worked out for San Antonio and fit its spacing/IQ profile.","Spurs baseline role PASS; outcomes HOLD","S14/S15/S22"],
  [50,"Indiana Pacers","Alize Johnson","Own pick","Indiana Pacers","Alize Johnson","UNCHANGED","None","Actual forward choice remains available.","Actual path preserved","S13"],
  [51,"New Orleans Pelicans","Tony Carr","Own pick","New Orleans Pelicans","Tony Carr","UNCHANGED","None","Guard-development choice remains distinct.","Actual path preserved","S13"],
  [52,"Houston Rockets","Vincent Edwards","Rights from UTA","Houston Rockets","Vincent Edwards","UNCHANGED","None","Wing-development choice remains distinct.","Actual path preserved","S13"],
  [53,"Oklahoma City Thunder","Devon Hall","Own pick","Oklahoma City Thunder","Devon Hall","UNCHANGED","None","Perimeter/stash route remains distinct.","Actual path preserved","S13"],
  [54,"Philadelphia 76ers","Shake Milton","Rights from DAL","Philadelphia 76ers","Shake Milton","UNCHANGED","None","Guard target and trade structure remain intact.","Actual path preserved","S13"],
  [55,"Charlotte Hornets","Arnoldas Kulboka","Own pick; overseas stash","Charlotte Hornets","Arnoldas Kulboka","UNCHANGED","None","Overseas-stash route remains distinct.","Actual path preserved","S13"],
  [56,"Dallas Mavericks","Ray Spalding","Rights from PHI","Dallas Mavericks","Chimezie Metu","CASCADE","Metu","Metu is the displaced #49 athletic big and remains above this slot.","Dallas contract layer PASS; outcomes HOLD","S13/S15/S28/S29/S30"],
  [57,"Oklahoma City Thunder","Kevin Hervey","Own pick","Oklahoma City Thunder","Kevin Hervey","UNCHANGED","None","Actual forward choice remains available.","Actual path preserved","S13"],
  [58,"Denver Nuggets","Thomas Welsh","Own pick","Denver Nuggets","Ray Spalding","CASCADE","Spalding","Spalding was graded in the drafted second-round big tier.","Denver contract layer PASS; Welsh market HOLD","S18/S31/S32/S33/S34"],
  [59,"Phoenix Suns","George King","Own pick","Phoenix Suns","George King","UNCHANGED","None","Actual wing choice remains available.","Actual path preserved","S13"],
  [60,"Dallas Mavericks","Kostas Antetokounmpo","Rights from PHI","Dallas Mavericks","Kostas Antetokounmpo","UNCHANGED","None","Second acquired pick and upside bet remain intact.","Actual path preserved","S13"],
];

const spursAssignmentWindows = [
  [1,"2018-10-25","2018-10-27",2,"Austin assignment","Recall","NBA contract retained","S22"],
  [2,"2018-11-05","2018-11-05",0,"Austin assignment","Same-day recall","NBA contract retained","S22"],
  [3,"2018-11-08","2018-11-08",0,"Austin assignment","Same-day recall","NBA contract retained","S22"],
  [4,"2018-11-20","2018-11-21",1,"Austin assignment","Recall","Second reported assignment","S22/S24"],
  [5,"2018-12-01","2018-12-02",1,"Austin assignment","Recall","NBA contract retained","S22"],
  [6,"2018-12-08","2018-12-09",1,"Austin assignment","Recall","NBA contract retained","S22"],
  [7,"2018-12-14","2018-12-23",9,"Austin assignment","Recall","Development window","S22"],
  [8,"2018-12-27","2019-01-03",7,"Austin assignment","Recall","Development window","S22"],
  [9,"2019-01-05","2019-01-05",0,"Austin assignment","Same-day recall","NBA contract retained","S22"],
  [10,"2019-01-07","2019-01-17",10,"Austin assignment","Recall","Development window","S22"],
  [11,"2019-01-19","2019-01-20",1,"Austin assignment","Recall","NBA contract retained","S22"],
  [12,"2019-01-25","2019-01-26",1,"Austin assignment","Recall","NBA contract retained","S22"],
  [13,"2019-02-01","2019-02-02",1,"Austin assignment","Recall","NBA contract retained","S22"],
  [14,"2019-02-10","2019-02-11",1,"Austin assignment","Recall","NBA contract retained","S22"],
  [15,"2019-02-28","2019-03-01",1,"Austin assignment","Recall","NBA contract retained","S22"],
  [16,"2019-03-07","2019-03-10",3,"Austin assignment","Recall","After Atlanta game","S22"],
  [17,"2019-03-13","2019-03-15",2,"Austin assignment","Recall","NBA contract retained","S22"],
  [18,"2019-03-19","2019-03-20",1,"Austin assignment","Recall","NBA contract retained","S22"],
  [19,"2019-03-21","2019-03-24",3,"Austin assignment","Recall","Final logged window","S22"],
];

const spursDirectGames = [
  ["2019-03-06","A","Atlanta Hawks","W",111,104,7,"NBA roster","DNP-CD / 0","NO_DIRECT_MINUTES","ATL-side execution HOLD","S25"],
  ["2019-04-02","H","Atlanta Hawks","W",117,111,6,"NBA roster","Inactive/0","NO_DIRECT_MINUTES","ATL-side execution HOLD","S26"],
];

const cascadeContracts = [
  ["Dallas","ACTUAL","Ray Spalding",56,"Standard NBA","Texas assignment",1,1,29,"Waived 2019-01-31","ACTUAL_REPLACED","Reference only","S28/S29/S30"],
  ["Dallas","CF","Chimezie Metu",56,"Standard NBA layer","Texas assignment baseline",1,1,29,"Jan. 31 waiver choice HOLD","CF_CHANGED_STANDARD",">1 NBA MIN or a different waiver opens Dallas player-game review","S28/S29/S30"],
  ["Denver","ACTUAL","Thomas Welsh",58,"Two-way","Capital City / Iowa",11,36,20,"Two-way ended 2019-07-30","ACTUAL_REPLACED","Reference only","S31/S34/S35"],
  ["Denver","CF","Ray Spalding",58,"Two-way (Welsh slot)","External G League assignment class",11,36,20,"Season role baseline","CF_CHANGED_TWO_WAY",">36 NBA MIN or different dates opens Denver player-game review","S31/S32/S33/S34"],
  ["Denver","CF","DeVaughn Akoon-Purcell",null,"Two-way","G League development",null,null,null,"Actual second slot preserved","CF_PROTECTED_TWO_WAY","Do not displace without a new transaction cause","S32/S33"],
  ["Denver","CF","Thomas Welsh",null,"No Denver slot","Undrafted free-agent market",0,0,0,"Destination unresolved","CF_OUT_NO_SLOT","Any NBA signing creates a new team-impact branch","S31/S32/S33/S35"],
];

const cascadeDirectGames = [
  ["Dallas","2018-10-24","A","L",104,111,-7,"Ray Spalding",0,"NO_DIRECT_MINUTES","ATL-side execution HOLD","S10/S29"],
  ["Dallas","2018-12-12","H","W",114,107,7,"Ray Spalding",0,"NO_DIRECT_MINUTES","ATL-side execution HOLD","S11/S29"],
  ["Denver","2018-11-15","H","W",138,93,45,"Thomas Welsh",0,"NO_DIRECT_MINUTES","ATL-side execution HOLD","S36/S37"],
  ["Denver","2018-12-08","A","L",98,106,-8,"Thomas Welsh",0,"NO_DIRECT_MINUTES","ATL-side execution HOLD","S38/S39"],
];

// Freeze the named receiver allocation before player production or outcomes.
// A receiver must be listed in the same-date ESPN Atlanta box score, including
// DNP-CD. Each cap is the player's actual 2018-19 single-game minute high.
const atlReceiverAllocations = [
  [1,3,"2018-10-21","Cleveland Cavaliers","401070718","PRE_ANDERSON","Alex Poythress","PLAY",24,26,2.0,"S44"],
  [2,3,"2018-10-21","Cleveland Cavaliers","401070718","PRE_ANDERSON","Miles Plumlee","DNP-CD",0,19,5.8,"S44"],
  [3,6,"2018-10-29","Philadelphia 76ers","401070769","PRE_ANDERSON","Miles Plumlee","PLAY",10,19,7.3,"S44"],
  [4,7,"2018-10-30","Cleveland Cavaliers","401070778","PRE_ANDERSON","Miles Plumlee","PLAY",1,19,4.4,"S44"],
  [5,8,"2018-11-01","Sacramento Kings","401070795","PRE_ANDERSON","Alex Poythress","PLAY",17,26,4.5,"S44"],
  [6,9,"2018-11-03","Miami Heat","401070809","PRE_ANDERSON","Alex Poythress","PLAY",10,26,4.2,"S44"],
  [7,10,"2018-11-06","Charlotte Hornets","401070830","PRE_ANDERSON","Alex Poythress","PLAY",17,26,0.8,"S44"],
  [8,11,"2018-11-07","New York Knicks","401070836","PRE_ANDERSON","Alex Poythress","PLAY",9,26,12.5,"S44"],
  [9,12,"2018-11-09","Detroit Pistons","401070850","PRE_ANDERSON","Alex Poythress","PLAY",11,26,10.7,"S44"],
  [10,13,"2018-11-11","Los Angeles Lakers","401070870","PRE_ANDERSON","Alex Poythress","PLAY",3,26,11.9,"S44"],
  [11,15,"2018-11-15","Denver Nuggets","401070895","PRE_ANDERSON","Alex Poythress","PLAY",24,26,2.0,"S44"],
  [12,15,"2018-11-15","Denver Nuggets","401070895","PRE_ANDERSON","Daniel Hamilton","PLAY",8,23,8.7,"S44"],
  [13,17,"2018-11-19","Los Angeles Clippers","401070924","ANDERSON_AVAILABLE","Justin Anderson","PLAY",3,31,14.1,"S44/S45"],
  [14,21,"2018-11-27","Miami Heat","401070983","ANDERSON_AVAILABLE","Justin Anderson","PLAY",2,31,4.3,"S44/S45"],
  [15,22,"2018-11-28","Charlotte Hornets","401070987","ANDERSON_AVAILABLE","Justin Anderson","PLAY",17,31,5.6,"S44/S45"],
  [16,39,"2019-01-06","Miami Heat","401071263","ANDERSON_AVAILABLE","Justin Anderson","PLAY",3,31,2.7,"S44/S45"],
  [17,42,"2019-01-11","Philadelphia 76ers","401071297","ANDERSON_AVAILABLE","Justin Anderson","PLAY",11,31,2.9,"S44/S45"],
  [18,43,"2019-01-13","Milwaukee Bucks","401071316","ANDERSON_AVAILABLE","Justin Anderson","PLAY",3,31,13.9,"S44/S45"],
  [19,44,"2019-01-15","Oklahoma City Thunder","401071329","ANDERSON_AVAILABLE","Justin Anderson","DNP-CD",0,31,5.9,"S44/S45"],
  [20,46,"2019-01-21","Orlando Magic","401071371","ANDERSON_AVAILABLE","Justin Anderson","DNP-CD",0,31,0.7,"S44/S45"],
  [21,47,"2019-01-23","Chicago Bulls","401071385","ANDERSON_AVAILABLE","Justin Anderson","PLAY",18,31,3.6,"S44/S45"],
  [22,50,"2019-01-30","Sacramento Kings","401071435","ANDERSON_AVAILABLE","Justin Anderson","PLAY",3,31,8.1,"S44/S45"],
  [23,51,"2019-02-01","Utah Jazz","401071446","ANDERSON_NOT_LISTED","Daniel Hamilton","PLAY",2,23,2.7,"S44"],
  [24,53,"2019-02-04","Washington Wizards","401071464","ANDERSON_AVAILABLE","Justin Anderson","DNP-CD",0,31,13.9,"S44/S45"],
  [25,56,"2019-02-10","Orlando Magic","401071510","ANDERSON_AVAILABLE","Justin Anderson","PLAY",9,31,10.3,"S44/S45"],
  [26,58,"2019-02-14","New York Knicks","401071538","ANDERSON_AVAILABLE","Justin Anderson","PLAY",5,31,1.1,"S44/S45"],
  [27,59,"2019-02-22","Detroit Pistons","401071550","ANDERSON_AVAILABLE","Justin Anderson","DNP-CD",0,31,2.7,"S44/S45"],
  [28,60,"2019-02-23","Phoenix Suns","401071556","ANDERSON_AVAILABLE","Justin Anderson","PLAY",6,31,5.5,"S44/S45"],
  [29,61,"2019-02-25","Houston Rockets","401071576","ANDERSON_AVAILABLE","Justin Anderson","PLAY",0,31,4.0,"S44/S45"],
  [30,62,"2019-02-27","Minnesota Timberwolves","401071585","ANDERSON_AVAILABLE","Justin Anderson","DNP-CD",0,31,3.4,"S44/S45"],
  [31,63,"2019-03-01","Chicago Bulls","401071601","ANDERSON_AVAILABLE","Justin Anderson","PLAY",5,31,2.9,"S44/S45"],
];

const atlReceiverSummaries = [
  ["Justin Anderson","SF",48,463,31,5,"S04/S44/S45"],
  ["Alex Poythress","F",21,305,26,0,"S04/S44/S46"],
  ["Daniel Hamilton","G-F",19,204,23,0,"S04/S44"],
  ["Miles Plumlee","F-C",18,173,19,1,"S04/S44"],
  ["B.J. Johnson","SF",6,43,19,0,"S04/S44"],
];

const sources = [
  ["S01","NBA Stats — Atlanta schedule","82-game official schedule baseline","https://www.nba.com/stats/team/1610612737/schedule?Season=2018-19"],
  ["S02","ESPN — Atlanta schedule","Scores/order cross-check; timezone dates not authoritative","https://www.espn.com/nba/team/schedule?name=ATL&season=2019&seasontype=2"],
  ["S03","Basketball-Reference — Atlanta schedule","29-53 and game-log cross-check","https://www.basketball-reference.com/teams/ATL/2019_games.html"],
  ["S04","NBA Stats — Atlanta player totals","Roster GP/GS/minutes baseline","https://www.nba.com/stats/players/traditional?Season=2018-19&SeasonType=Regular%20Season&TeamID=1610612737&PerMode=Totals"],
  ["S05","Hawks — Spellman injury update","March 1 high ankle sprain; not copied to protagonist","https://www.nba.com/hawks/news/omari-spellman-injury-update"],
  ["S06","NBA G League — Spellman","2018-19: 3 starts, 32.7 MPG","https://gleague.nba.com/player/1629016"],
  ["S07","Hawks — 2019 lottery odds explained","Atlanta/Dallas pick protection and odds baseline","https://www.nba.com/hawks/features/hawks-lottery-odds-explained"],
  ["S08","NBA Communications — 2019 tiebreakers","Lottery teams, inverse order, tied combinations","https://pr.nba.com/2019-nba-draft-tiebreakers/"],
  ["S09","NBA — 2019 lottery result","Actual draw baseline only","https://www.nba.com/news/pelicans-win-nba-draft-lottery"],
  ["S10","Hawks — Oct. 24 Dallas game","Atlanta 111-104 Dallas official game page","https://www.nba.com/hawks/game/0021800052-mavericks-vs-hawks-atlanta-ga-10-24-2018"],
  ["S11","Mavericks — Dec. 12 Atlanta game","Dallas 114-107 Atlanta official recap","https://www.nba.com/mavs/mavs-get-a-spark-from-carlisle-and-rallied-for-a-114-107-victory-over-the-hawks"],
  ["S12","NBA — 2018 Atlanta draft","Actual 30th pick was Spellman","https://www.nba.com/hawks/news/hawks-acquire-trae-young-select-kevin-huerter-omari-spellman-2018-nba-draft"],
  ["S13","NBA — 2018 Draft Trade Tracker","Actual picks, rights trades, and destination teams","https://www.nba.com/2018-draft-trade-tracker"],
  ["S14","San Antonio Express-News — Spurs workout target","Spellman worked out for Spurs; second workout interest","https://www.expressnews.com/spurs-nation/article/Spurs-target-Villanova-s-Spellman-others-for-12994749.php"],
  ["S15","Sports Illustrated — final 2018 mock","Spellman #44 range; Spurs fit; Metu second-round range","https://www.si.com/nba/2018/06/21/nba-mock-draft-2018-trade-rumors-final-picks-deandre-ayton-trae-young"],
  ["S16","Wizards — Issuf Sanon plan","Washington explicitly preferred an overseas stash","https://www.nba.com/wizards/wizards-plan-second-round-pick-issuf-sanon"],
  ["S17","Nets — Rodions Kurucs scouting history","Brooklyn's long-running Kurucs evaluation","https://www.nba.com/nets/news/feature/2018/12/28/brooklyn-nets-rookie-rodions-kurucs-had-a-breakout-month-in-december"],
  ["S18","NBA — 2018 big-board tiers","Spalding in drafted second-round tier; Welsh in the mix","https://www.nba.com/da-big-board-bigs-2018-draft"],
  ["S19","Nuggets — Thomas Welsh two-way","Actual Welsh occupied one Denver two-way slot","https://www.nba.com/nuggets/news/thomas-welsh-signs-two-way-contract-071918"],
  ["S20","Basketball-Reference — Chimezie Metu","2018-19 San Antonio: 29 games, 5.0 MPG (145 minutes)","https://www.basketball-reference.com/players/m/metuch01.html"],
  ["S21","Pounding the Rock — Metu season review","Most rookie NBA minutes came in garbage time; Austin was primary development venue","https://www.poundingtherock.com/2019/5/4/18523491/2018-2019-spurs-player-reviews-chimezie-metu"],
  ["S22","RealGM — Chimezie Metu profile","2018-19 NBA totals, Austin totals, and assignment/recall transaction log","https://basketball.realgm.com/player/Chimezie-Metu/Summary/76976"],
  ["S23","Spurs — Metu signing","Second-round pick signed to an NBA multi-year contract, not a two-way","https://www.nba.com/spurs/news/spurs-sign-2018-second-round-pick-chimezie-metu"],
  ["S24","Fox San Antonio — Nov. 20 assignment","Contemporary report identifies Metu's second Austin assignment and NBA baseline","https://foxsanantonio.com/sports/max-sports/spurs-assign-rookie-metu-to-g-league"],
  ["S25","ESPN — 2019-03-06 Spurs at Atlanta","Spurs 111-104; Metu DNP-Coach's Decision","https://www.espn.com/nba/boxscore/_/gameId/401071641"],
  ["S26","NBA Hawks — 2019-04-02 Atlanta at Spurs","Spurs 117-111; Metu recorded no minutes","https://www.nba.com/hawks/game/0021801162-hawks-vs-spurs-san-antonio-tx-04-02-2019"],
  ["S27","Spurs — 2019 Metu Austin recap","2018-19 Austin: 26 games, 14.0/7.4/2.3 in 27.3 MPG","https://www.nba.com/spurs/news/san-antonio-assigns-chimezie-metu-austin-spurs-8"],
  ["S28","Mavericks — Spalding signing","Dallas signed the actual #56 pick to a standard NBA contract","https://www.nba.com/mavs/mavericks-sign-forward-ray-spalding"],
  ["S29","Mavericks — Porzingis trade and Spalding waiver","Spalding appeared in one Dallas game and was waived in the Jan. 31 roster move","https://www.nba.com/mavs/mavericks-acquire-all-star-kristaps-porzingis-tim-hardaway-jr-courtney-lee-and-trey-burke-in-trade-with-knicks"],
  ["S30","NBA G League — Ray Spalding","2018-19 Texas: 29 games, 26 starts, 30.1 MPG","https://gleague.nba.com/player/1629034/ray-spalding"],
  ["S31","Nuggets — Thomas Welsh two-way","Denver signed the actual #58 pick to a two-way contract","https://www.nba.com/nuggets/news/thomas-welsh-signs-two-way-contract-071918"],
  ["S32","Nuggets — 2018-19 two-way preview","Welsh and Akoon-Purcell occupied Denver's two two-way positions","https://www.nba.com/nuggets/news/1819-player-previews-akoon-purcell-welsh-091918"],
  ["S33","NBA G League — 2018 two-way rule","2018-19 teams could carry two two-way players beyond the 15-man roster","https://windycity.gleague.nba.com/news/bulls-sign-brandon-sampson-to-two-way-contract"],
  ["S34","Nuggets — Welsh 2018-19 recap","Welsh played 11 NBA games and 36 minutes; G League was his primary venue","https://www.nba.com/nuggets/news/denver-nuggets-thomas-welsh-excited-for-nba-summer-league-070219c"],
  ["S35","RealGM — Thomas Welsh profile","Two-way transaction and 20-game G League allocation baseline","https://basketball.realgm.com/player/Thomas-Welsh/Summary/64323"],
  ["S36","NBA — 2018-11-15 Atlanta at Denver","Denver 138-93 official game baseline","https://www.nba.com/game/atl-vs-den-0021800214"],
  ["S37","Basketball-Reference — 2018-11-15 box score","Welsh did not play against Atlanta","https://www.basketball-reference.com/boxscores/201811150DEN.html"],
  ["S38","NBA Hawks — 2018-12-08 Denver at Atlanta","Atlanta 106-98 official game baseline","https://www.nba.com/hawks/game/0021800380"],
  ["S39","Basketball-Reference — 2018-12-08 box score","Welsh did not play against Atlanta","https://www.basketball-reference.com/boxscores/201812080ATL.html"],
  ["S40","HoopsStats — Omari Spellman 2018-19 game log","Exact 46 appearance dates and published tenths-of-a-minute donor vector; sums to 805.0","https://www.hoopsstats.com/basketball/fantasy/nba/atlanta-hawks/players/omari-spellman/gamelog/19/1/16"],
  ["S41","RealGM — Omari Spellman profile","46 games, 11 starts, 804.6 exact season minutes cross-check","https://basketball.realgm.com/player/Omari-Spellman/Summary/74078"],
  ["S42","Peachtree Hoops — Spellman assigned to Erie","Actual Dec. 30 assignment followed hip-injury absence and conditioning need; context only, not copied","https://www.peachtreehoops.com/2018/12/30/18161520/omari-spellman-alex-poythress-atlanta-hawks-g-league-erie-bayhawks-assignment-transfer-roster"],
  ["S43","Basketball-Reference — Erie 2018-19 schedule","Six real Erie games in the Dec. 7-22 development window","https://www.basketball-reference.com/gleague/schedules/HAW/2019.html"],
  ["S44","ESPN — Atlanta 2018-19 schedule and box scores","Same-date box-score listing, DNP-CD status, actual minutes, event IDs, and observed single-game maxima","https://www.espn.com/nba/team/schedule/_/name/atl/season/2019"],
  ["S45","Atlanta Hawks — Justin Anderson 2018-19 review","Anderson missed the first 16 games while rehabbing and returned for the Nov. 19 game","https://www.nba.com/hawks/features/five-things-know-about-justin-andersons-2018-19-season"],
  ["S46","Atlanta Hawks — Alex Poythress 2018-19 review","Poythress held a two-way development role with Atlanta and Erie","https://www.nba.com/hawks/five-things-know-about-alex-poythress-2018-19-season"],
];

const wb = Workbook.create();
const readme = wb.worksheets.add("README");
const ledger = wb.worksheets.add("Game Ledger");
const assignment = wb.worksheets.add("ATL Assignment");
const receivers = wb.worksheets.add("ATL Receivers");
const minutes = wb.worksheets.add("Season Minutes");
const draftBoardSheet = wb.worksheets.add("2018 Draft Board");
const spurs = wb.worksheets.add("Spurs Impact");
const cascade = wb.worksheets.add("Cascade Impact");
const draft = wb.worksheets.add("Draft Bridge");
const gates = wb.worksheets.add("Gate Audit");
const sourceSheet = wb.worksheets.add("Sources");

const navy = "#17223B";
const blue = "#2D5BFF";
const paleBlue = "#EAF0FF";
const paleGreen = "#E8F5E9";
const paleYellow = "#FFF4CE";
const paleRed = "#FDECEC";
const gray = "#667085";
const lightGray = "#F2F4F7";
const border = "#D0D5DD";

function title(sheet, range, text) {
  sheet.getRange(range).merge();
  const cell = sheet.getRange(range.split(":")[0]);
  cell.values = [[text]];
  cell.format.fill = navy;
  cell.format.font = { color: "#FFFFFF", bold: true, size: 18 };
  cell.format.rowHeight = 32;
  cell.format.verticalAlignment = "center";
}

function section(range) {
  range.format.fill = paleBlue;
  range.format.font = { color: navy, bold: true };
  range.format.borders = { preset: "all", style: "thin", color: border };
}

function header(range) {
  range.format.fill = blue;
  range.format.font = { color: "#FFFFFF", bold: true };
  range.format.borders = { preset: "all", style: "thin", color: border };
  range.format.verticalAlignment = "center";
  range.format.wrapText = true;
}

function body(range) {
  range.format.borders = { preset: "all", style: "thin", color: border };
  range.format.verticalAlignment = "center";
}

// README
readme.showGridLines = false;
title(readme, "A1:H2", "ATLANTA 2018-19 — CAUSALITY LEDGER / DRAFT BOARD v0.6");
readme.getRange("A4:H4").values = [["Status","ATL_RECEIVER_PASS / OUTCOME_HOLD","Canon","v0.24 PARTIAL","Manuscript","BLOCKED","Built","2026-08-29"]];
section(readme.getRange("A4:H4"));
readme.getRange("A6:H6").values = [["Verified baseline","Value","Expected","Check","Simulation guardrail","Low","High","Check"]];
header(readme.getRange("A6:H6"));
readme.getRange("A7:A12").values = [["Regular-season games"],["Actual wins"],["Actual losses"],["Atlanta points"],["Game capacity minutes"],["Published roster minutes"]];
readme.getRange("B7:B12").formulas = [["=COUNTA('Game Ledger'!$A$6:$A$87)"],["=COUNTIF('Game Ledger'!$E$6:$E$87,\"W\")"],["=COUNTIF('Game Ledger'!$E$6:$E$87,\"L\")"],["=SUM('Game Ledger'!$F$6:$F$87)"],["=SUM('Game Ledger'!$J$6:$J$87)"],["=SUM('Season Minutes'!$E$6:$E$27)"]];
readme.getRange("C7:C12").values = [[82],[29],[53],[9294],[19855],[19853]];
readme.getRange("D7:D12").formulas = [["=IF(B7=C7,\"PASS\",\"FAIL\")"],["=IF(B8=C8,\"PASS\",\"FAIL\")"],["=IF(B9=C9,\"PASS\",\"FAIL\")"],["=IF(B10=C10,\"PASS\",\"FAIL\")"],["=IF(B11=C11,\"PASS\",\"FAIL\")"],["=IF(ABS(B12-C12)<=2,\"PASS (rounding)\",\"FAIL\")"]];
readme.getRange("E7:E12").values = [["NBA games"],["NBA MPG"],["NBA total minutes"],["Spellman donor balance"],["Erie games"],["Named receiver balance"]];
readme.getRange("F7:F12").formulas = [["=COUNTIF('Game Ledger'!$O$6:$O$87,\"DIRECT\")"],["=SUM('Game Ledger'!$R$6:$R$87)/F7"],["=SUM('Game Ledger'!$R$6:$R$87)"],["=SUM('Game Ledger'!$S$6:$S$87)"],["=COUNTA('ATL Assignment'!$A$17:$A$22)"],["='ATL Receivers'!F4"]];
readme.getRange("G7:G12").values = [[43],[14.46],[621.9],[805],[6],[0]];
readme.getRange("H7:H12").formulas = [["=IF(F7=G7,\"PASS\",\"FAIL\")"],["=IF(ABS(F8-G8)<0.01,\"PASS\",\"FAIL\")"],["=IF(ABS(F9-G9)<0.01,\"PASS\",\"FAIL\")"],["=IF(ABS(F10-G10)<0.01,\"PASS\",\"FAIL\")"],["=IF(F11=G11,\"PASS\",\"FAIL\")"],["=IF(ABS(F12-G12)<0.01,\"PASS\",\"FAIL\")"]];
readme.getRange("F8:G8").setNumberFormat("0.00");
readme.getRange("F9:G10").setNumberFormat("0.0");
body(readme.getRange("A7:H12"));
readme.getRange("D7:D12").format.fill = paleGreen;
readme.getRange("H7:H12").format.fill = paleGreen;
readme.getRange("A14:H14").merge();
readme.getRange("A14").values = [["Decision boundary"]];
section(readme.getRange("A14:H14"));
readme.getRange("A15:H19").values = [
  ["1","All 82 games and the actual 29-53 record are immutable baseline data.",null,null,null,null,null,null],
  ["2","Every game has at least ROSTER contact because the #30 replacement removes Spellman from Atlanta, even when the protagonist is inactive.",null,null,null,null,null,null],
  ["3","Date-level rule is locked before outcomes: donor ≥7.0 minutes, cap at 16.0, except the Nov. 19 missed-rotation story cost.",null,null,null,null,null,null],
  ["4","The San Antonio, Dallas, and Denver replacement contract layers are closed. Each CF rookie starts inside the displaced player's team-specific role, not his old-team minutes.",null,null,null,null,null,null],
  ["5","The 183.1-minute bridge is fully assigned by same-date evidence: Anderson 105.6, Poythress 48.6, Plumlee 17.5, Hamilton 11.4. Production and outcomes remain HOLD.",null,null,null,null,null,null],
];
for (let r = 15; r <= 19; r++) readme.getRange(`B${r}:H${r}`).merge();
body(readme.getRange("A15:H19"));
readme.getRange("A21:H21").merge();
readme.getRange("A21").values = [["NEXT: preregister player production / pB / impact priors → fixed-hash outcome → opponent W/L → standings → lottery"]];
readme.getRange("A21").format.fill = paleYellow;
readme.getRange("A21").format.font = { color: navy, bold: true };
readme.getRange("A21").format.wrapText = true;
readme.getRange("A21").format.rowHeight = 34;
readme.getRange("A1:H21").format.font = { name: "Aptos" };
readme.getRange("A:H").format.columnWidth = 18;
readme.getRange("B:B").format.columnWidth = 44;
readme.getRange("E:E").format.columnWidth = 24;
readme.freezePanes.freezeRows(4);

// Game Ledger
ledger.showGridLines = false;
title(ledger, "A1:Y2", "82-GAME IMMUTABLE BASELINE + COUNTERFACTUAL CONTROL FIELDS");
ledger.getRange("A3:Y3").merge();
ledger.getRange("A3").values = [["Blue = official baseline · Yellow = future inputs · Gray = formula/control fields · All counterfactual outcomes remain HOLD"]];
ledger.getRange("A3").format.fill = lightGray;
ledger.getRange("A3").format.font = { color: gray, italic: true };
const gameHeaders = ["Game","Date","Site","Opponent","Actual","ATL Pts","Opp Pts","Margin","OT periods","Team min","Cum W","Cum L","Rest days","B2B","Contact","Story selected","Protagonist status","Protagonist min","Spellman donor","Named receiver pool","Minute check","Outcome status","CF result","Downstream","Source ID"];
ledger.getRange("A5:Y5").values = [gameHeaders];
header(ledger.getRange("A5:Y5"));
const gameRows = games.map((g) => {
  const cf = atlCounterfactualRow(g);
  return [g[0],new Date(`${g[1]}T12:00:00Z`),g[2],g[3],g[4],g[5],g[6],null,g[7],null,null,null,null,null,cf.contact,cf.storySelected,cf.status,cf.protagonistMinutes,cf.donor,cf.reserveReceiver,null,"HOLD","HOLD","PRODUCTION_PRIOR_PENDING","S01/S02/S03/S40/S44"];
});
ledger.getRange(`A6:Y${5+gameRows.length}`).values = gameRows;
ledger.getRange("H6:H87").formulasR1C1 = Array.from({length:82},()=>["=RC[-2]-RC[-1]"]);
ledger.getRange("J6:J87").formulasR1C1 = Array.from({length:82},()=>["=240+25*RC[-1]"]);
ledger.getRange("K6:K87").formulas = games.map((_,i)=>[i===0?'=IF(E6="W",1,0)':`=K${5+i}+IF(E${6+i}="W",1,0)`]);
ledger.getRange("L6:L87").formulas = games.map((_,i)=>[i===0?'=IF(E6="L",1,0)':`=L${5+i}+IF(E${6+i}="L",1,0)`]);
ledger.getRange("M6:M87").formulas = games.map((_,i)=>[i===0?'=""':`=B${6+i}-B${5+i}-1`]);
ledger.getRange("N6:N87").formulas = games.map((_,i)=>[i===0?'=FALSE':`=M${6+i}=0`]);
ledger.getRange("U6:U87").formulasR1C1 = Array.from({length:82},()=>["=RC[-2]-RC[-3]-RC[-1]"]);
ledger.getRange("B6:B87").setNumberFormat("yyyy-mm-dd");
ledger.getRange("M6:M87").setNumberFormat("0");
ledger.getRange("R6:U87").setNumberFormat("0.0");
ledger.getRange("A6:Y87").format.borders = { preset: "all", style: "thin", color: "#E4E7EC" };
ledger.getRange("A6:O87").format.fill = "#FFFFFF";
ledger.getRange("P6:T87").format.fill = paleYellow;
ledger.getRange("U6:Y87").format.fill = lightGray;
ledger.getRange("A5:Y87").format.font = { name: "Aptos", size: 9 };
ledger.getRange("D:D").format.columnWidth = 22;
ledger.getRange("B:B").format.columnWidth = 12;
ledger.getRange("O:O").format.columnWidth = 12;
ledger.getRange("Q:Q").format.columnWidth = 25;
ledger.getRange("V:W").format.columnWidth = 16;
ledger.getRange("X:X").format.columnWidth = 27;
ledger.getRange("Y:Y").format.columnWidth = 24;
ledger.getRange("A:A").format.columnWidth = 7;
ledger.getRange("C:C").format.columnWidth = 7;
ledger.getRange("E:N").format.columnWidth = 10;
ledger.getRange("P:U").format.columnWidth = 13;
ledger.freezePanes.freezeRows(5);
ledger.freezePanes.freezeColumns(4);
ledger.tables.add("A5:Y87", true, "GameLedgerTable");

// Atlanta availability and Erie assignment preregistration
assignment.showGridLines = false;
title(assignment, "A1:H2", "ATLANTA ROOKIE — AVAILABILITY & ASSIGNMENT PREREGISTRATION");
assignment.getRange("A4:H4").values = [["Metric","Value","Expected","Check","Rule","Value","Status","Source"]];
header(assignment.getRange("A4:H4"));
assignment.getRange("A5:A11").values = [["NBA GP"],["NBA minutes"],["NBA MPG"],["Spellman donor"],["ATL remainder pool"],["Minute balance"],["DIRECT / ROSTER"]];
assignment.getRange("B5:B11").formulas = [
  ["=COUNTIF('Game Ledger'!$O$6:$O$87,\"DIRECT\")"],
  ["=SUM('Game Ledger'!$R$6:$R$87)"],
  ["=B6/B5"],
  ["=SUM('Game Ledger'!$S$6:$S$87)"],
  ["=SUM('Game Ledger'!$T$6:$T$87)"],
  ["=ROUND(SUM('Game Ledger'!$U$6:$U$87),1)"],
  ["=COUNTIF('Game Ledger'!$O$6:$O$87,\"DIRECT\")&\" / \"&COUNTIF('Game Ledger'!$O$6:$O$87,\"ROSTER\")"],
];
assignment.getRange("C5:C11").values = [[43],[621.9],[14.46],[805],[183.1],[0],["43 / 39"]];
assignment.getRange("D5:D11").formulas = [
  ["=IF(B5=C5,\"PASS\",\"FAIL\")"],
  ["=IF(ABS(B6-C6)<0.01,\"PASS\",\"FAIL\")"],
  ["=IF(ABS(B7-C7)<0.01,\"PASS\",\"FAIL\")"],
  ["=IF(ABS(B8-C8)<0.01,\"PASS\",\"FAIL\")"],
  ["=IF(ABS(B9-C9)<0.01,\"PASS\",\"FAIL\")"],
  ["=IF(ABS(B10-C10)<0.01,\"PASS\",\"FAIL\")"],
  ["=IF(B11=C11,\"PASS\",\"FAIL\")"],
];
assignment.getRange("E5:H11").values = [
  ["Eligibility","Spellman donor ≥ 7.0", "LOCK","S40"],
  ["Game cap","MIN(16.0, donor)","LOCK","S40"],
  ["Story cost","2018-11-19; planned 14.1 → 0","LOCK","S01/S40"],
  ["Selection basis","First home game after multi-city road stretch","OUTCOME_BLIND","S01"],
  ["Assignment","2018-12-07 through 2018-12-22","LOCK","S43"],
  ["Assignment purpose","Six-game development block; not discipline","LOCK","S42/S43"],
  ["Injury firewall","Do not copy Spellman's hip/ankle injuries","LOCK","S05/S42"],
];
body(assignment.getRange("A5:H11"));
assignment.getRange("D5:D11").format.fill = paleGreen;
assignment.getRange("G5:G11").format.fill = paleGreen;
assignment.getRange("A13:H13").merge();
assignment.getRange("A13").values = [["Erie schedule inside the locked development window — exact fictional box-score minutes remain 24-30 MPG HOLD"]];
section(assignment.getRange("A13:H13"));
assignment.getRange("A16:H16").values = [["Erie game","Date","Site","Opponent","Minute band","NBA same date","NBA minutes","Source"]];
header(assignment.getRange("A16:H16"));
const erieRows = erieGames.map((g) => {
  const nba = games.find((game) => game[1] === g[1]);
  return [g[0],new Date(`${g[1]}T12:00:00Z`),g[2],g[3],g[4],nba ? `${nba[2]} ${nba[3]}` : "NONE",0,g[5]];
});
assignment.getRange("A17:H22").values = erieRows;
assignment.getRange("B17:B22").setNumberFormat("yyyy-mm-dd");
assignment.getRange("B6:C10").setNumberFormat("0.00");
body(assignment.getRange("A17:H22"));
assignment.getRange("A24:H24").merge();
assignment.getRange("A24").values = [["NO COLLISION: all six Erie dates carry 0 NBA minutes. Assignment follows the missed opportunity but is independently justified by development workload."]];
assignment.getRange("A24").format.fill = paleGreen;
assignment.getRange("A24").format.font = { color: navy, bold: true };
assignment.getRange("A24").format.wrapText = true;
assignment.getRange("A24").format.rowHeight = 34;
assignment.getRange("A1:H24").format.font = { name: "Aptos" };
assignment.getRange("A:H").format.columnWidth = 18;
assignment.getRange("D:D").format.columnWidth = 31;
assignment.getRange("E:E").format.columnWidth = 34;
assignment.getRange("F:F").format.columnWidth = 32;
assignment.getRange("H:H").format.columnWidth = 14;
assignment.getRange("A4:H24").format.wrapText = true;
assignment.freezePanes.freezeRows(4);

// Atlanta named reserve receivers
receivers.showGridLines = false;
title(receivers, "A1:R2", "ATLANTA 2018-19 — NAMED RESERVE RECEIVER ALLOCATION");
receivers.getRange("A4:R4").values = [["Pool",null,"Allocated",null,"Balance",null,"Dates",null,"Rows",null,"Receivers",null,"Uncovered",null,"Status",null,"Next","Production prior"]];
section(receivers.getRange("A4:R4"));
receivers.getRange("B4").formulas = [["=SUM('Game Ledger'!$T$6:$T$87)"]];
receivers.getRange("D4").formulas = [["=SUM(L7:L37)"]];
receivers.getRange("F4").formulas = [["=B4-D4"]];
receivers.getRange("H4").formulas = [["=COUNTIF('Game Ledger'!$T$6:$T$87,\">0\")"]];
receivers.getRange("J4").formulas = [["=COUNTA(A7:A37)"]];
receivers.getRange("L4").formulas = [["=COUNTIF(F43:F47,\">0\")"]];
receivers.getRange("N4").formulas = [["=COUNTIF(P7:P37,\">0.001\")"]];
receivers.getRange("P4").formulas = [["=IF(AND(ABS(F4)<0.01,H4=29,J4=31,L4=4,N4=0),\"PASS\",\"FAIL\")"]];
receivers.getRange("B4:F4").setNumberFormat("0.0");
receivers.getRange("P4").format.fill = paleGreen;

const receiverHeaders = ["Alloc","Game","Date","Opponent","Event ID","Phase","Receiver","Box status","Actual MIN","Observed max","Capacity","Allocated","Adjusted MIN","Date allocated","Game pool","Date balance","Source ID","Evidence URL"];
receivers.getRange("A6:R6").values = [receiverHeaders];
header(receivers.getRange("A6:R6"));
const receiverRows = atlReceiverAllocations.map((r) => [
  r[0],r[1],new Date(`${r[2]}T12:00:00Z`),r[3],r[4],r[5],r[6],r[7],r[8],r[9],null,r[10],null,null,null,null,r[11],`https://www.espn.com/nba/boxscore/_/gameId/${r[4]}`,
]);
receivers.getRange("A7:R37").values = receiverRows;
receivers.getRange("K7:K37").formulasR1C1 = Array.from({length:31},()=>["=RC[-1]-RC[-2]"]);
receivers.getRange("M7:M37").formulasR1C1 = Array.from({length:31},()=>["=RC[-4]+RC[-1]"]);
receivers.getRange("N7:N37").formulas = Array.from({length:31},(_,i)=>[`=SUMIF($C$7:$C$37,C${7+i},$L$7:$L$37)`]);
receivers.getRange("O7:O37").formulas = Array.from({length:31},(_,i)=>[`=SUMIF('Game Ledger'!$B$6:$B$87,C${7+i},'Game Ledger'!$T$6:$T$87)`]);
receivers.getRange("P7:P37").formulasR1C1 = Array.from({length:31},()=>["=RC[-1]-RC[-2]"]);
receivers.getRange("C7:C37").setNumberFormat("yyyy-mm-dd");
receivers.getRange("I7:P37").setNumberFormat("0.0");
body(receivers.getRange("A7:R37"));
receivers.getRange("F7:H37").format.fill = paleYellow;
receivers.getRange("K7:P37").format.fill = lightGray;

receivers.getRange("A40:J40").merge();
receivers.getRange("A40").values = [["SEASON RECEIVER SUMMARY — cap = actual 2018-19 observed single-game high; added GP counts DNP-CD dates converted to appearances"]];
section(receivers.getRange("A40:J40"));
receivers.getRange("A42:J42").values = [["Receiver","Pos","Actual GP","Actual MIN","Observed max","Allocated","Added GP","CF GP","CF MIN","Source ID"]];
header(receivers.getRange("A42:J42"));
receivers.getRange("A43:J47").values = atlReceiverSummaries.map((r)=>[...r.slice(0,5),null,r[5],null,null,r[6]]);
receivers.getRange("F43:F47").formulas = atlReceiverSummaries.map((r,idx)=>[`=SUMIF($G$7:$G$37,A${43+idx},$L$7:$L$37)`]);
receivers.getRange("H43:H47").formulasR1C1 = Array.from({length:5},()=>["=RC[-5]+RC[-1]"]);
receivers.getRange("I43:I47").formulasR1C1 = Array.from({length:5},()=>["=RC[-5]+RC[-3]"]);
receivers.getRange("D43:I47").setNumberFormat("0.0");
body(receivers.getRange("A43:J47"));
receivers.getRange("F43:I47").format.fill = lightGray;
receivers.getRange("A49:J49").values = [["TOTAL",null,null,null,null,null,null,null,null,"B.J. Johnson audited at zero: his only overlapping residual date (Mar. 1) already has Anderson available."]];
receivers.getRange("J49:R49").merge();
receivers.getRange("F49").formulas = [["=SUM(F43:F47)"]];
receivers.getRange("I49").formulas = [["=SUM(I43:I47)"]];
section(receivers.getRange("A49:J49"));
receivers.getRange("J49:R49").format.fill = paleBlue;
receivers.getRange("J49:R49").format.font = { color: navy, bold: true };
receivers.getRange("J49:R49").format.wrapText = true;
receivers.getRange("J49:R49").format.rowHeight = 32;
receivers.getRange("F49:I49").setNumberFormat("0.0");
receivers.getRange("A:R").format.columnWidth = 14;
receivers.getRange("C:C").format.columnWidth = 13;
receivers.getRange("D:D").format.columnWidth = 23;
receivers.getRange("F:G").format.columnWidth = 21;
receivers.getRange("H:H").format.columnWidth = 14;
receivers.getRange("Q:Q").format.columnWidth = 13;
receivers.getRange("R:R").format.columnWidth = 48;
receivers.getRange("A4:R49").format.wrapText = true;
receivers.getRange("A4:R49").format.font = { name: "Aptos", size: 9 };
receivers.freezePanes.freezeRows(6);
receivers.freezePanes.freezeColumns(4);
receivers.tables.add("A6:R37", true, "AtlReceiverAllocationTable");
receivers.tables.add("A42:J47", true, "AtlReceiverSummaryTable");

// Season Minutes
minutes.showGridLines = false;
title(minutes, "A1:L2", "ATLANTA 2018-19 — ROSTER MINUTES & REALLOCATION FIREWALL");
minutes.getRange("A3:L3").merge();
minutes.getRange("A3").values = [["Published integer player minutes sum two minutes below game capacity because of source rounding. Allow the two-minute audit delta; never spend it as new minutes."]];
minutes.getRange("A3").format.fill = paleYellow;
minutes.getRange("A3").format.wrapText = true;
const minuteHeaders = ["Player / bridge","Pos","Actual GP","Actual GS","Actual min","Actual MPG","Pool","Removed actual","Added CF","Post-CF min","Balance","Source ID"];
minutes.getRange("A5:L5").values = [minuteHeaders];
header(minutes.getRange("A5:L5"));
const rosterRows = roster.map((p)=>{
  const receiver = atlReceiverSummaries.find((candidate)=>candidate[0]===p[0]);
  return [...p.slice(0,5),null,p[5],p[0]==="Omari Spellman"?805:0,0,null,null,p[0]==="Omari Spellman"?"S04/S40":receiver?receiver[6]:"S04"];
});
rosterRows.push(["Fictional protagonist","F",0,0,0,null,"CF_INCOMING",0,null,null,null,"S40"]);
rosterRows.push(["ATL_REMAINDER_POOL","—",0,0,0,null,"RESOLVED_ACCOUNTING_BRIDGE",0,null,null,null,"S40/S44"]);
minutes.getRange(`A6:L${5+rosterRows.length}`).values = rosterRows;
minutes.getRange("F6:F29").formulasR1C1 = Array.from({length:24},()=>["=IF(RC[-3]=0,0,RC[-1]/RC[-3])"]);
for (let i = 0; i < roster.length; i++) {
  if (atlReceiverSummaries.some((receiver) => receiver[0] === roster[i][0])) {
    const row = 6 + i;
    minutes.getRange(`I${row}`).formulas = [[`=SUMIF('ATL Receivers'!$G$7:$G$37,A${row},'ATL Receivers'!$L$7:$L$37)`]];
  }
}
minutes.getRange("I28").formulas = [["=SUM('Game Ledger'!$R$6:$R$87)"]];
minutes.getRange("I29").formulas = [["=SUM('Game Ledger'!$T$6:$T$87)-SUM('ATL Receivers'!$L$7:$L$37)"]];
minutes.getRange("J6:J29").formulasR1C1 = Array.from({length:24},()=>["=RC[-5]-RC[-2]+RC[-1]"]);
minutes.getRange("K6:K29").formulasR1C1 = Array.from({length:24},()=>["=RC[-1]-(RC[-6]-RC[-3]+RC[-2])"]);
minutes.getRange("F6:F29").setNumberFormat("0.0");
minutes.getRange("H6:K29").setNumberFormat("0.0");
minutes.getRange("A6:L29").format.borders = { preset: "all", style: "thin", color: "#E4E7EC" };
minutes.getRange("H6:I29").format.fill = paleYellow;
minutes.getRange("J6:K29").format.fill = lightGray;
minutes.getRange("A31:L31").values = [["TOTAL",null,null,null,null,null,null,null,null,null,null,null]];
minutes.getRange("E31").formulas = [["=SUM(E6:E29)"]];
minutes.getRange("H31").formulas = [["=SUM(H6:H29)"]];
minutes.getRange("I31").formulas = [["=SUM(I6:I29)"]];
minutes.getRange("J31").formulas = [["=SUM(J6:J29)"]];
minutes.getRange("K31").formulas = [["=SUM(K6:K29)"]];
section(minutes.getRange("A31:L31"));
minutes.getRange("A33:L33").values = [["Primary rule","Donor ≥7.0; cap 16.0",null,"Exact NBA line","43 GP / 621.9 MIN / 14.46 MPG",null,null,"Named receivers","183.1 min / 4 players / 0 unresolved",null,null,null]];
minutes.getRange("B33:C33").merge();
minutes.getRange("E33:G33").merge();
minutes.getRange("I33:K33").merge();
section(minutes.getRange("A33:L33"));
minutes.getRange("A33:L33").format.wrapText = true;
minutes.getRange("A:L").format.columnWidth = 14;
minutes.getRange("A:A").format.columnWidth = 22;
minutes.getRange("G:G").format.columnWidth = 31;
minutes.getRange("L:L").format.columnWidth = 14;
minutes.freezePanes.freezeRows(5);
minutes.tables.add("A5:L29", true, "SeasonMinutesTable");

// 2018 Draft Board
draftBoardSheet.showGridLines = false;
title(draftBoardSheet, "A1:K2", "2018 PICKS 30-60 — COMPRESSED COUNTERFACTUAL BOARD");
draftBoardSheet.getRange("A4:H4").values = [["Scanned picks",null,"Changed/cascade",null,"Unchanged",null,"Next blocker","ATL production / outcome prior"]];
section(draftBoardSheet.getRange("A4:H4"));
draftBoardSheet.getRange("B4").formulas = [["=COUNTA(A7:A37)"]];
draftBoardSheet.getRange("D4").formulas = [["=COUNTIF(G7:G37,\"CHANGED\")+COUNTIF(G7:G37,\"CASCADE\")"]];
draftBoardSheet.getRange("F4").formulas = [["=COUNTIF(G7:G37,\"UNCHANGED\")"]];
const draftBoardHeaders = ["Pick","Actual destination","Actual player","Actual trade/path","CF destination","CF player","Status","Incoming displaced","Decision reason","Downstream","Source ID"];
draftBoardSheet.getRange("A6:K6").values = [draftBoardHeaders];
header(draftBoardSheet.getRange("A6:K6"));
draftBoardSheet.getRange("A7:K37").values = draftBoard;
body(draftBoardSheet.getRange("A7:K37"));
draftBoardSheet.getRange("A7:K37").format.wrapText = true;
draftBoardSheet.getRange("G7:G37").format.fill = lightGray;
for (let r = 7; r <= 37; r++) {
  const status = draftBoard[r - 7][6];
  if (status === "CHANGED" || status === "CASCADE") draftBoardSheet.getRange(`A${r}:K${r}`).format.fill = paleYellow;
}
draftBoardSheet.getRange("A:A").format.columnWidth = 16;
draftBoardSheet.getRange("B:B").format.columnWidth = 24;
draftBoardSheet.getRange("C:C").format.columnWidth = 22;
draftBoardSheet.getRange("D:D").format.columnWidth = 34;
draftBoardSheet.getRange("E:E").format.columnWidth = 24;
draftBoardSheet.getRange("F:F").format.columnWidth = 22;
draftBoardSheet.getRange("G:H").format.columnWidth = 17;
draftBoardSheet.getRange("I:I").format.columnWidth = 48;
draftBoardSheet.getRange("J:J").format.columnWidth = 28;
draftBoardSheet.getRange("K:K").format.columnWidth = 14;
draftBoardSheet.freezePanes.freezeRows(6);
draftBoardSheet.freezePanes.freezeColumns(2);
draftBoardSheet.tables.add("A6:K37", true, "DraftBoardTable");

// Spurs Impact
spurs.showGridLines = false;
title(spurs, "A1:L2", "SAN ANTONIO 2018-19 — SECOND-TEAM IMPACT FIREWALL");
spurs.getRange("A4:L4").values = [["Actual Spurs","48-34","Metu NBA","29 G / 145.4 MIN","Metu Austin","26 G / 710.4 MIN","CF base","29 G / 145.4 MIN","ATL series","2 G / 0 MIN","Status","BASELINE_ROLE_PASS"]];
section(spurs.getRange("A4:L4"));
spurs.getRange("A6:H6").values = [["Scenario","NBA GP","NBA MPG","NBA MIN","Starts","Austin GP","Result rule","Required evidence"]];
header(spurs.getRange("A6:H6"));
spurs.getRange("A7:H9").values = [
  ["LOW",24,4,120,0,28,"No automatic game changes","Stay inside Metu/deep-reserve slot"],
  ["BASE",29,5,145.4,0,26,"No automatic game changes","Metu actual role baseline"],
  ["HIGH",31,6,180,0,20,"GAME_REVIEW if competitive","Dated donor required above 145.4"],
];
body(spurs.getRange("A7:H9"));
spurs.getRange("A11:L11").values = [["Date","Site","Opponent","Actual","SAS Pts","ATL Pts","Margin","Metu roster","Metu status","Spurs-side CF contact","Outcome status","Source ID"]];
header(spurs.getRange("A11:L11"));
spurs.getRange("A12:L13").values = spursDirectGames.map((g)=>[new Date(`${g[0]}T12:00:00Z`),...g.slice(1)]);
spurs.getRange("A12:A13").setNumberFormat("yyyy-mm-dd");
body(spurs.getRange("A12:L13"));
spurs.getRange("A15:H15").values = [["Window","Assign date","Recall date","Calendar days","Entry","Exit","Contract/status","Source ID"]];
header(spurs.getRange("A15:H15"));
spurs.getRange(`A16:H${15+spursAssignmentWindows.length}`).values = spursAssignmentWindows.map((w)=>[w[0],new Date(`${w[1]}T12:00:00Z`),new Date(`${w[2]}T12:00:00Z`),...w.slice(3)]);
spurs.getRange(`B16:C${15+spursAssignmentWindows.length}`).setNumberFormat("yyyy-mm-dd");
body(spurs.getRange(`A16:H${15+spursAssignmentWindows.length}`));
spurs.getRange("J15:L15").values = [["Audit","Value","Check"]];
header(spurs.getRange("J15:L15"));
spurs.getRange("J16:J21").values = [["Assignment windows"],["Direct games"],["Direct Metu minutes"],["Base minutes"],["High-base excess"],["Outcome lock"]];
spurs.getRange("K16:K21").formulas = [
  ["=COUNTA(A16:A34)"],
  ["=COUNTA(A12:A13)"],
  ["=0"],
  ["=D8"],
  ["=D9-D8"],
  ["=IF(K18=0,\"SPURS-SIDE DIRECT PASS\",\"REVIEW\")"],
];
spurs.getRange("L16:L21").formulas = [
  ["=IF(K16=19,\"PASS\",\"FAIL\")"],
  ["=IF(K17=2,\"PASS\",\"FAIL\")"],
  ["=IF(K18=0,\"PASS\",\"FAIL\")"],
  ["=IF(ABS(K19-145.4)<0.01,\"PASS\",\"FAIL\")"],
  ["=IF(ABS(K20-34.6)<0.01,\"DONOR REQUIRED\",\"CHECK\")"],
  ["=IF(K21=\"SPURS-SIDE DIRECT PASS\",\"PASS\",\"HOLD\")"],
];
body(spurs.getRange("J16:L21"));
spurs.getRange("J23:L23").merge();
spurs.getRange("J23").values = [["48-34 remains BASELINE, not a locked counterfactual result. Atlanta-side player impact is still HOLD."]];
spurs.getRange("J23:L23").format.fill = paleYellow;
spurs.getRange("J23:L23").format.wrapText = true;
spurs.getRange("A:L").format.columnWidth = 16;
spurs.getRange("A:A").format.columnWidth = 13;
spurs.getRange("G:H").format.columnWidth = 27;
spurs.getRange("J:J").format.columnWidth = 24;
spurs.getRange("K:L").format.columnWidth = 22;
spurs.getRange("A4:L34").format.font = { name: "Aptos", size: 9 };
spurs.freezePanes.freezeRows(15);
spurs.tables.add("A15:H34", true, "SpursAssignmentTable");

// Dallas / Denver Cascade Impact
cascade.showGridLines = false;
title(cascade, "A1:M2", "DALLAS / DENVER 2018-19 — CASCADE CONTRACT FIREWALL");
cascade.getRange("A4:M4").values = [["Dallas base","1 G / 1 MIN",null,"Texas","29 G / 30.1 MPG",null,"Denver base","11 G / 36 MIN",null,"ATL series","4 G / 0 MIN","Status","CONTRACT_LAYER_PASS"]];
section(cascade.getRange("A4:M4"));
const cascadeContractHeaders = ["Team","World","Player","Pick","Contract layer","Development path","NBA GP","NBA MIN","G League GP","Transaction","Role status","Escalation trigger","Source ID"];
cascade.getRange("A6:M6").values = [cascadeContractHeaders];
header(cascade.getRange("A6:M6"));
cascade.getRange("A7:M12").values = cascadeContracts;
body(cascade.getRange("A7:M12"));
cascade.getRange("A7:M12").format.wrapText = true;
cascade.getRange("A15:L15").values = [["Team","Date","Site","Actual","Team pts","ATL pts","Margin","Replaced player","Replaced MIN","CF contact","Outcome status","Source ID"]];
header(cascade.getRange("A15:L15"));
cascade.getRange("A16:L19").values = cascadeDirectGames.map((g)=>[g[0],new Date(`${g[1]}T12:00:00Z`),...g.slice(2)]);
cascade.getRange("B16:B19").setNumberFormat("yyyy-mm-dd");
body(cascade.getRange("A16:L19"));
cascade.getRange("J21:L21").values = [["Audit","Value","Check"]];
header(cascade.getRange("J21:L21"));
cascade.getRange("J22:J27").values = [["Changed contract chains"],["Direct games"],["Direct replaced minutes"],["Denver CF two-way slots"],["Welsh duplicate blocked"],["Outcome lock"]];
cascade.getRange("K22:K27").formulas = [
  ["=COUNTIF(K7:K12,\"CF_CHANGED_STANDARD\")+COUNTIF(K7:K12,\"CF_CHANGED_TWO_WAY\")"],
  ["=COUNTA(A16:A19)"],
  ["=SUM(I16:I19)"],
  ["=COUNTIF(K7:K12,\"CF_CHANGED_TWO_WAY\")+COUNTIF(K7:K12,\"CF_PROTECTED_TWO_WAY\")"],
  ["=COUNTIF(K7:K12,\"CF_OUT_NO_SLOT\")"],
  ["=IF(AND(K24=0,K25=2,K26=1),\"CASCADE DIRECT PASS\",\"REVIEW\")"],
];
cascade.getRange("L22:L27").formulas = [
  ["=IF(K22=2,\"PASS\",\"FAIL\")"],
  ["=IF(K23=4,\"PASS\",\"FAIL\")"],
  ["=IF(K24=0,\"PASS\",\"REVIEW\")"],
  ["=IF(K25=2,\"PASS\",\"FAIL\")"],
  ["=IF(K26=1,\"PASS\",\"FAIL\")"],
  ["=IF(K27=\"CASCADE DIRECT PASS\",\"PASS\",\"HOLD\")"],
];
body(cascade.getRange("J22:L27"));
cascade.getRange("A21:H23").merge();
cascade.getRange("A21").values = [["Dallas: Metu begins inside Spalding's standard-contract / Texas assignment slot; a different Jan. 31 waiver choice remains HOLD. Denver: Spalding takes Welsh's two-way slot, Akoon-Purcell keeps the other, and Welsh moves to the undrafted free-agent market. Any minutes above the displaced-player base reopen player-game review."]];
cascade.getRange("A21:H23").format.fill = paleYellow;
cascade.getRange("A21:H23").format.wrapText = true;
cascade.getRange("A:M").format.columnWidth = 16;
cascade.getRange("A:A").format.columnWidth = 13;
cascade.getRange("C:C").format.columnWidth = 23;
cascade.getRange("E:F").format.columnWidth = 25;
cascade.getRange("J:J").format.columnWidth = 25;
cascade.getRange("K:K").format.columnWidth = 26;
cascade.getRange("L:L").format.columnWidth = 46;
cascade.getRange("M:M").format.columnWidth = 18;
cascade.getRange("A4:M27").format.font = { name: "Aptos", size: 9 };
cascade.freezePanes.freezeRows(6);
cascade.tables.add("A6:M12", true, "CascadeContractTable");
cascade.tables.add("A15:L19", true, "CascadeDirectGameTable");

// Draft Bridge
draft.showGridLines = false;
title(draft, "A1:J2", "2019 DRAFT BRIDGE — ACTUAL BASELINE, NOT A LOCKED OUTCOME");
draft.getRange("A4:J4").values = [["Team/Pick","Actual W","Actual L","Pre-lottery slot","No.1 odds","Top-4 odds","Actual draw","Protection","Actual disposition","Status"]];
header(draft.getRange("A4:J4"));
draft.getRange("A5:J6").values = [
  ["Atlanta own",29,53,5,0.105,0.4212,8,"None","Atlanta #8","BASELINE_ONLY"],
  ["Dallas → Atlanta",33,49,9,0.06,0.263,10,"2019 Top 5","Conveyed to Atlanta","BASELINE_ONLY"],
];
body(draft.getRange("A5:J6"));
draft.getRange("E5:F6").setNumberFormat("0.0%");
draft.getRange("A8:J8").merge();
draft.getRange("A8").values = [["SENSITIVITY EXAMPLE — flip only the 2018-12-12 Dallas 114-107 Atlanta game (not a canon result)"]];
section(draft.getRange("A8:J8"));
draft.getRange("A9:J10").values = [
  ["Atlanta",30,52,"still near 5th inverse","RECALCULATE","RECALCULATE","DO NOT COPY",null,null,"EXAMPLE"],
  ["Dallas",32,50,"ties Washington","RECALCULATE","RECALCULATE","DO NOT COPY","Top 5 remains","Convey/rollover unknown","EXAMPLE"],
];
body(draft.getRange("A9:J10"));
draft.getRange("A12:J12").merge();
draft.getRange("A12").values = [["REQUIRED ORDER: both teams' W/L for every changed game → 14 non-playoff teams → tied combinations/order → fixed-seed lottery → Dallas protection → trades and selections"]];
draft.getRange("A12").format.fill = paleYellow;
draft.getRange("A12").format.font = { bold: true, color: navy };
draft.getRange("A12").format.wrapText = true;
draft.getRange("A12").format.rowHeight = 36;
draft.getRange("A14:J14").merge();
draft.getRange("A14").values = [["FINAL BLOCKER: Atlanta's 82-game donor vector and 183.1 named receiver allocation are balanced. Preregister production and impact priors before standings/lottery."]];
draft.getRange("A14").format.fill = paleRed;
draft.getRange("A14").format.font = { bold: true, color: "#B42318" };
draft.getRange("A14").format.wrapText = true;
draft.getRange("A:J").format.columnWidth = 17;
draft.getRange("A:A").format.columnWidth = 22;
draft.getRange("H:I").format.columnWidth = 22;

// Gate Audit
gates.showGridLines = false;
title(gates, "A1:F2", "R09 AUDIT GATES");
gates.getRange("A4:F4").values = [["Gate","Requirement","Current evidence","Status","Blocks","Next action"]];
header(gates.getRange("A4:F4"));
const gateRows = [
  ["G0","Changed-pick contract and direct-game baselines","Spurs 145.4 min; Dallas 1 min; Denver 36 min; ATL series all 0","PASS","None","Preserve team-specific caps and triggers"],
  ["G1","82 unique + 29-53 + score/OT checksum","82 rows; 29-53; 9,294 pts; 19,855 game-min","PASS","None","Preserve immutable baseline"],
  ["G2","Rotation/assignment/impact priors before results","≥7 donor gate; 16 cap; Nov. 19 cost; Dec. 7-22 Erie","PASS","None","Preserve before outcome model"],
  ["G3","Every game minute-conserved; no NBA/Erie collision","621.9 protagonist + 183.1 named receivers = 805.0; 29 dates; zero balance","PASS","None","Preserve named receiver vector"],
  ["G4","All 82 games contact classified","43 DIRECT / 39 ROSTER","PASS","None","Upgrade CASCADE only with evidence"],
  ["G5","Pregame-only pB; fixed latent u; no manual flip","Method selected; inputs absent","HOLD","CF result","Calibrate and preregister"],
  ["G6","Chronological injury/fatigue/trade updates","Not executed","HOLD","CF result","Process in date order"],
  ["G7","No exact score invention; sensitivity isolated","No CF scores/results created","PASS","None","Keep results HOLD until model"],
  ["G8","Opponent W/L + league standings/tiebreaker","Not executed","HOLD","2019 lottery","Build league bridge"],
  ["G9","Raw baseline immutable; run/model/seed logged","Baseline + protagonist + named receiver date vectors recorded","PARTIAL","Reproduction","Add production/outcome run manifest"],
];
gates.getRange("A5:F14").values = gateRows;
body(gates.getRange("A5:F14"));
gates.getRange("D5:D14").format.fill = paleYellow;
gates.getRange("A16:F16").values = [["OVERALL","ATL_RECEIVER_ALLOCATION_PASS / OUTCOME_HOLD",null,null,null,"Preregister player production and game-impact priors before outcome execution"]];
section(gates.getRange("A16:F16"));
gates.getRange("A:F").format.columnWidth = 20;
gates.getRange("B:B").format.columnWidth = 34;
gates.getRange("C:C").format.columnWidth = 38;
gates.getRange("E:F").format.columnWidth = 26;
gates.getRange("A4:F16").format.wrapText = true;
gates.freezePanes.freezeRows(4);

// Sources
sourceSheet.showGridLines = false;
title(sourceSheet, "A1:D2", "SOURCE REGISTER");
sourceSheet.getRange("A4:D4").values = [["ID","Source","Use","URL"]];
header(sourceSheet.getRange("A4:D4"));
sourceSheet.getRange(`A5:D${4+sources.length}`).values = sources;
body(sourceSheet.getRange(`A5:D${4+sources.length}`));
sourceSheet.getRange("A:A").format.columnWidth = 9;
sourceSheet.getRange("B:B").format.columnWidth = 35;
sourceSheet.getRange("C:C").format.columnWidth = 48;
sourceSheet.getRange("D:D").format.columnWidth = 80;
sourceSheet.getRange(`A4:D${4+sources.length}`).format.wrapText = true;
sourceSheet.freezePanes.freezeRows(4);
sourceSheet.tables.add(`A4:D${4+sources.length}`, true, "SourceTable");

await fs.mkdir(path.dirname(outputPath), { recursive: true });
const blob = await SpreadsheetFile.exportXlsx(wb);
await blob.save(outputPath);

await fs.rm(previewDir, { recursive: true, force: true });
await fs.mkdir(previewDir, { recursive: true });
for (const sheetName of ["README","Game Ledger","ATL Assignment","ATL Receivers","Season Minutes","2018 Draft Board","Spurs Impact","Cascade Impact","Draft Bridge","Gate Audit","Sources"]) {
  const image = await wb.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  const bytes = new Uint8Array(await image.arrayBuffer());
  await fs.writeFile(path.join(previewDir, `${sheetName.replaceAll(" ", "_")}.png`), bytes);
}

// artifact-tool may emit a diagnostic sidecar while rendering a very large sheet.
// It is not part of the deliverable or the reproducibility record.
await fs.rm(`${outputPath}.inspect.ndjson`, { force: true });

console.log(`WROTE ${outputPath}`);
console.log(`PREVIEWS ${previewDir}`);
