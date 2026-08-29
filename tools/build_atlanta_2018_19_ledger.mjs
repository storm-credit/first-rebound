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
  [49,"San Antonio Spurs","Chimezie Metu","Own pick","San Antonio Spurs","Omari Spellman","CHANGED","Spellman","Spellman worked out for San Antonio and fit its spacing/IQ profile.","Spurs 2018-19 impact HOLD","S14/S15"],
  [50,"Indiana Pacers","Alize Johnson","Own pick","Indiana Pacers","Alize Johnson","UNCHANGED","None","Actual forward choice remains available.","Actual path preserved","S13"],
  [51,"New Orleans Pelicans","Tony Carr","Own pick","New Orleans Pelicans","Tony Carr","UNCHANGED","None","Guard-development choice remains distinct.","Actual path preserved","S13"],
  [52,"Houston Rockets","Vincent Edwards","Rights from UTA","Houston Rockets","Vincent Edwards","UNCHANGED","None","Wing-development choice remains distinct.","Actual path preserved","S13"],
  [53,"Oklahoma City Thunder","Devon Hall","Own pick","Oklahoma City Thunder","Devon Hall","UNCHANGED","None","Perimeter/stash route remains distinct.","Actual path preserved","S13"],
  [54,"Philadelphia 76ers","Shake Milton","Rights from DAL","Philadelphia 76ers","Shake Milton","UNCHANGED","None","Guard target and trade structure remain intact.","Actual path preserved","S13"],
  [55,"Charlotte Hornets","Arnoldas Kulboka","Own pick; overseas stash","Charlotte Hornets","Arnoldas Kulboka","UNCHANGED","None","Overseas-stash route remains distinct.","Actual path preserved","S13"],
  [56,"Dallas Mavericks","Ray Spalding","Rights from PHI","Dallas Mavericks","Chimezie Metu","CASCADE","Metu","Metu is the displaced #49 athletic big and remains above this slot.","Dallas role/minutes HOLD","S13/S15"],
  [57,"Oklahoma City Thunder","Kevin Hervey","Own pick","Oklahoma City Thunder","Kevin Hervey","UNCHANGED","None","Actual forward choice remains available.","Actual path preserved","S13"],
  [58,"Denver Nuggets","Thomas Welsh","Own pick","Denver Nuggets","Ray Spalding","CASCADE","Spalding","Spalding was graded in the drafted second-round big tier.","Denver role/two-way HOLD","S18"],
  [59,"Phoenix Suns","George King","Own pick","Phoenix Suns","George King","UNCHANGED","None","Actual wing choice remains available.","Actual path preserved","S13"],
  [60,"Dallas Mavericks","Kostas Antetokounmpo","Rights from PHI","Dallas Mavericks","Kostas Antetokounmpo","UNCHANGED","None","Second acquired pick and upside bet remain intact.","Actual path preserved","S13"],
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
  ["S19","Nuggets — Thomas Welsh two-way","Actual Welsh two-way destination used as role-preservation baseline","https://www.nba.com/nuggets/news/thomas-welsh-signs-two-way-contract-071918"],
  ["S20","Basketball-Reference — Chimezie Metu","2018-19 San Antonio: 29 games, 5.0 MPG (145 minutes)","https://www.basketball-reference.com/players/m/metuch01.html"],
  ["S21","Pounding the Rock — Metu season review","Most rookie NBA minutes came in garbage time; Austin was primary development venue","https://www.poundingtherock.com/2019/5/4/18523491/2018-2019-spurs-player-reviews-chimezie-metu"],
];

const wb = Workbook.create();
const readme = wb.worksheets.add("README");
const ledger = wb.worksheets.add("Game Ledger");
const minutes = wb.worksheets.add("Season Minutes");
const draftBoardSheet = wb.worksheets.add("2018 Draft Board");
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
title(readme, "A1:H2", "ATLANTA 2018-19 — CAUSALITY LEDGER / DRAFT BOARD v0.2");
readme.getRange("A4:H4").values = [["Status","BASELINE_PASS / SECOND_TEAM_IMPACT_HOLD","Canon","PROVISIONAL","Manuscript","BLOCKED","Built","2026-08-29"]];
section(readme.getRange("A4:H4"));
readme.getRange("A6:H6").values = [["Verified baseline","Value","Expected","Check","Simulation guardrail","Low","High","Check"]];
header(readme.getRange("A6:H6"));
readme.getRange("A7:A12").values = [["Regular-season games"],["Actual wins"],["Actual losses"],["Atlanta points"],["Game capacity minutes"],["Published roster minutes"]];
readme.getRange("B7:B12").formulas = [["=COUNTA('Game Ledger'!$A$6:$A$87)"],["=COUNTIF('Game Ledger'!$E$6:$E$87,\"W\")"],["=COUNTIF('Game Ledger'!$E$6:$E$87,\"L\")"],["=SUM('Game Ledger'!$F$6:$F$87)"],["=SUM('Game Ledger'!$J$6:$J$87)"],["=SUM('Season Minutes'!$E$6:$E$27)"]];
readme.getRange("C7:C12").values = [[82],[29],[53],[9294],[19855],[19853]];
readme.getRange("D7:D12").formulas = [["=IF(B7=C7,\"PASS\",\"FAIL\")"],["=IF(B8=C8,\"PASS\",\"FAIL\")"],["=IF(B9=C9,\"PASS\",\"FAIL\")"],["=IF(B10=C10,\"PASS\",\"FAIL\")"],["=IF(B11=C11,\"PASS\",\"FAIL\")"],["=IF(ABS(B12-C12)<=2,\"PASS (rounding)\",\"FAIL\")"]];
readme.getRange("E7:E12").values = [["NBA games"],["NBA MPG"],["NBA total minutes"],["Spellman slot cap"],["Erie games"],["Protected core"]];
readme.getRange("F7:F12").values = [[42],[14,],[588],[0],[4],["Young/Huerter/Collins"]];
readme.getRange("G7:G12").values = [[46],[16],[736],[805],[10],["Same"]];
readme.getRange("H7:H12").formulas = [["=IF(AND(F7>=38,G7<=50),\"PASS\",\"FAIL\")"],["=IF(AND(F8>=10,G8<=16),\"PASS\",\"FAIL\")"],["=IF(G9<=G10,\"PASS\",\"FAIL\")"],["=IF(G10=805,\"CAP\",\"CHECK\")"],["=IF(AND(F11>=4,G11<=10),\"PASS\",\"FAIL\")"],["=\"LOCK\""]];
body(readme.getRange("A7:H12"));
readme.getRange("D7:D12").format.fill = paleGreen;
readme.getRange("H7:H12").format.fill = paleGreen;
readme.getRange("A14:H14").merge();
readme.getRange("A14").values = [["Decision boundary"]];
section(readme.getRange("A14:H14"));
readme.getRange("A15:H19").values = [
  ["1","All 82 games and the actual 29-53 record are immutable baseline data.",null,null,null,null,null,null],
  ["2","Every game has at least ROSTER contact because the #30 replacement removes Spellman from Atlanta, even when the protagonist is inactive.",null,null,null,null,null,null],
  ["3","Allocate protagonist minutes inside Spellman's 805-minute cap first. Do not auto-allocate before date-specific availability is verified.",null,null,null,null,null,null],
  ["4","Spellman's destination is resolved at San Antonio #49. The 2019 standings/lottery cannot be FINAL until the Spurs' 2018-19 impact is closed.",null,null,null,null,null,null],
  ["5","No counterfactual scores or results have been generated. Manual flips and close-game cherry-picking are prohibited.",null,null,null,null,null,null],
];
for (let r = 15; r <= 19; r++) readme.getRange(`B${r}:H${r}`).merge();
body(readme.getRange("A15:H19"));
readme.getRange("A21:H21").merge();
readme.getRange("A21").values = [["NEXT: game-level availability → donor vector → preregistered pB/impact → fixed-hash outcome → opponent W/L → standings → lottery"]];
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
const gameHeaders = ["Game","Date","Site","Opponent","Actual","ATL Pts","Opp Pts","Margin","OT periods","Team min","Cum W","Cum L","Rest days","B2B","Contact","Story selected","Protagonist status","Protagonist min","Spellman donor","Other donor","Minute check","Outcome status","CF result","Downstream","Source ID"];
ledger.getRange("A5:Y5").values = [gameHeaders];
header(ledger.getRange("A5:Y5"));
const gameRows = games.map((g) => [g[0],new Date(`${g[1]}T12:00:00Z`),g[2],g[3],g[4],g[5],g[6],null,g[7],null,null,null,null,null,"ROSTER",false,"HOLD",0,0,0,null,"HOLD","HOLD","PENDING","S01/S02/S03"]);
ledger.getRange(`A6:Y${5+gameRows.length}`).values = gameRows;
ledger.getRange("H6:H87").formulasR1C1 = Array.from({length:82},()=>["=RC[-2]-RC[-1]"]);
ledger.getRange("J6:J87").formulasR1C1 = Array.from({length:82},()=>["=240+25*RC[-1]"]);
ledger.getRange("K6:K87").formulas = games.map((_,i)=>[i===0?'=IF(E6="W",1,0)':`=K${5+i}+IF(E${6+i}="W",1,0)`]);
ledger.getRange("L6:L87").formulas = games.map((_,i)=>[i===0?'=IF(E6="L",1,0)':`=L${5+i}+IF(E${6+i}="L",1,0)`]);
ledger.getRange("M6:M87").formulas = games.map((_,i)=>[i===0?'=""':`=B${6+i}-B${5+i}-1`]);
ledger.getRange("N6:N87").formulas = games.map((_,i)=>[i===0?'=FALSE':`=M${6+i}=0`]);
ledger.getRange("U6:U87").formulasR1C1 = Array.from({length:82},()=>["=RC[-3]-RC[-2]-RC[-1]"]);
ledger.getRange("B6:B87").setNumberFormat("yyyy-mm-dd");
ledger.getRange("M6:M87").setNumberFormat("0");
ledger.getRange("A6:Y87").format.borders = { preset: "all", style: "thin", color: "#E4E7EC" };
ledger.getRange("A6:O87").format.fill = "#FFFFFF";
ledger.getRange("P6:T87").format.fill = paleYellow;
ledger.getRange("U6:Y87").format.fill = lightGray;
ledger.getRange("A5:Y87").format.font = { name: "Aptos", size: 9 };
ledger.getRange("D:D").format.columnWidth = 22;
ledger.getRange("B:B").format.columnWidth = 12;
ledger.getRange("O:O").format.columnWidth = 12;
ledger.getRange("Q:Q").format.columnWidth = 18;
ledger.getRange("V:Y").format.columnWidth = 16;
ledger.getRange("A:A").format.columnWidth = 7;
ledger.getRange("C:C").format.columnWidth = 7;
ledger.getRange("E:N").format.columnWidth = 10;
ledger.getRange("P:U").format.columnWidth = 13;
ledger.freezePanes.freezeRows(5);
ledger.freezePanes.freezeColumns(4);
ledger.tables.add("A5:Y87", true, "GameLedgerTable");

// Season Minutes
minutes.showGridLines = false;
title(minutes, "A1:L2", "ATLANTA 2018-19 — ROSTER MINUTES & REALLOCATION FIREWALL");
minutes.getRange("A3:L3").merge();
minutes.getRange("A3").values = [["Published integer player minutes sum two minutes below game capacity because of source rounding. Allow the two-minute audit delta; never spend it as new minutes."]];
minutes.getRange("A3").format.fill = paleYellow;
minutes.getRange("A3").format.wrapText = true;
const minuteHeaders = ["Player","Pos","GP","GS","Minutes","MPG","Pool","Max removable","Allocated to protagonist","Post-CF minutes","Delta check","Source ID"];
minutes.getRange("A5:L5").values = [minuteHeaders];
header(minutes.getRange("A5:L5"));
const rosterRows = roster.map((p)=>[...p.slice(0,5),null,p[5],p[0]==="Omari Spellman"?805:(p[5]==="FALLBACK_FORWARD"?p[4]:0),0,null,null,"S04"]);
minutes.getRange(`A6:L${5+rosterRows.length}`).values = rosterRows;
minutes.getRange("F6:F27").formulasR1C1 = Array.from({length:22},()=>["=IF(RC[-3]=0,0,RC[-1]/RC[-3])"]);
minutes.getRange("J6:J27").formulasR1C1 = Array.from({length:22},()=>["=RC[-5]-RC[-1]"]);
minutes.getRange("K6:K27").formulasR1C1 = Array.from({length:22},()=>["=RC[-1]+RC[-2]-RC[-6]"]);
minutes.getRange("F6:F27").setNumberFormat("0.0");
minutes.getRange("A6:L27").format.borders = { preset: "all", style: "thin", color: "#E4E7EC" };
minutes.getRange("H6:I27").format.fill = paleYellow;
minutes.getRange("J6:K27").format.fill = lightGray;
minutes.getRange("A29:L29").values = [["TOTAL",null,null,null,null,null,null,null,null,null,null,null]];
minutes.getRange("E29").formulas = [["=SUM(E6:E27)"]];
minutes.getRange("H29").formulas = [["=SUM(H6:H27)"]];
minutes.getRange("I29").formulas = [["=SUM(I6:I27)"]];
minutes.getRange("J29").formulas = [["=SUM(J6:J27)"]];
minutes.getRange("K29").formulas = [["=SUM(K6:K27)"]];
section(minutes.getRange("A29:L29"));
minutes.getRange("A31:L31").values = [["Primary rule","Protagonist total ≤ 805",null,"Fallback rule","Use Anderson/Poythress/B.J. Johnson only with date-specific availability proof",null,null,"Protected","Young/Huerter/Collins",null,null,null]];
minutes.getRange("B31:C31").merge();
minutes.getRange("E31:G31").merge();
section(minutes.getRange("A31:L31"));
minutes.getRange("A31:L31").format.wrapText = true;
minutes.getRange("A:L").format.columnWidth = 14;
minutes.getRange("A:A").format.columnWidth = 22;
minutes.getRange("G:G").format.columnWidth = 24;
minutes.getRange("L:L").format.columnWidth = 14;
minutes.freezePanes.freezeRows(5);
minutes.tables.add("A5:L27", true, "SeasonMinutesTable");

// 2018 Draft Board
draftBoardSheet.showGridLines = false;
title(draftBoardSheet, "A1:K2", "2018 PICKS 30-60 — COMPRESSED COUNTERFACTUAL BOARD");
draftBoardSheet.getRange("A4:H4").values = [["Scanned picks",null,"Changed/cascade",null,"Unchanged",null,"Next blocker","Spurs 2018-19 impact"]];
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
draft.getRange("A14").values = [["FINAL BLOCKER: Spellman is resolved to San Antonio #49; close the Spurs' 2018-19 rotation and game impact before standings/lottery."]];
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
  ["G0","Spellman destination + second-team impact","Spellman → Spurs #49; Spurs impact not executed","PARTIAL","FINAL standings/lottery","Model Spurs 2018-19"],
  ["G1","82 unique + 29-53 + score/OT checksum","82 rows; 29-53; 9,294 pts; 19,855 game-min","PASS","None","Preserve immutable baseline"],
  ["G2","Rotation/assignment/impact priors before results","Only season range locked","HOLD","CF execution","Build date-specific availability"],
  ["G3","Every game minute-conserved; no NBA/Erie collision","Season cap proven; player-game not built","HOLD","CF execution","Create player-game donor vectors"],
  ["G4","All 82 games contact classified","82/82 ROSTER","PASS","None","Upgrade DIRECT/CASCADE as needed"],
  ["G5","Pregame-only pB; fixed latent u; no manual flip","Method selected; inputs absent","HOLD","CF result","Calibrate and preregister"],
  ["G6","Chronological injury/fatigue/trade updates","Not executed","HOLD","CF result","Process in date order"],
  ["G7","No exact score invention; sensitivity isolated","No CF scores/results created","PASS","None","Keep results HOLD until model"],
  ["G8","Opponent W/L + league standings/tiebreaker","Not executed","HOLD","2019 lottery","Build league bridge"],
  ["G9","Raw baseline immutable; run/model/seed logged","Workbook baseline created","PARTIAL","Reproduction","Add run manifest after preregistration"],
];
gates.getRange("A5:F14").values = gateRows;
body(gates.getRange("A5:F14"));
gates.getRange("D5:D14").format.fill = paleYellow;
gates.getRange("A16:F16").values = [["OVERALL","BASELINE_PASS / SECOND_TEAM_IMPACT_HOLD",null,null,null,"Draft path closed; Spurs season bridge remains"]];
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
for (const sheetName of ["README","Game Ledger","Season Minutes","2018 Draft Board","Draft Bridge","Gate Audit","Sources"]) {
  const image = await wb.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  const bytes = new Uint8Array(await image.arrayBuffer());
  await fs.writeFile(path.join(previewDir, `${sheetName.replaceAll(" ", "_")}.png`), bytes);
}

// artifact-tool may emit a diagnostic sidecar while rendering a very large sheet.
// It is not part of the deliverable or the reproducibility record.
await fs.rm(`${outputPath}.inspect.ndjson`, { force: true });

console.log(`WROTE ${outputPath}`);
console.log(`PREVIEWS ${previewDir}`);
