import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
import fs from "node:fs/promises";
import { createHash } from "node:crypto";

const inputPath = process.argv[2] ?? "simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx";
const blob = await FileBlob.load(inputPath);
const wb = await SpreadsheetFile.importXlsx(blob);

const checks = [
  ["README", "A4:H12"],
  ["Game Ledger", "A5:Z87"],
  ["ATL Assignment", "A4:H24"],
  ["ATL Receivers", "A4:R49"],
  ["ATL Priors", "A4:V44"],
  ["Season Minutes", "A5:L33"],
  ["2018 Draft Board", "A4:K37"],
  ["Spurs Impact", "A4:L34"],
  ["Cascade Impact", "A4:M27"],
  ["Draft Bridge", "A4:J14"],
  ["Gate Audit", "A4:F16"],
  ["Sources", "A4:D57"],
];

let errors = 0;
for (const [sheetName, rangeAddress] of checks) {
  const sheet = wb.worksheets.getItem(sheetName);
  const range = sheet.getRange(rangeAddress);
  const values = range.values;
  for (let r = 0; r < values.length; r++) {
    for (let c = 0; c < values[r].length; c++) {
      const value = values[r][c];
      if (typeof value === "string" && /^#(REF|DIV\/0|VALUE|NAME\?|N\/A|NUM|NULL)/.test(value)) {
        errors++;
        console.log(`FORMULA_ERROR ${sheetName}!${rangeAddress} r${r + 1}c${c + 1}: ${value}`);
      }
    }
  }
  console.log(`CHECKED ${sheetName}!${rangeAddress}: ${values.length} rows`);
}

const readme = wb.worksheets.getItem("README");
const summary = readme.getRange("B7:D12").values;
console.log("SUMMARY", JSON.stringify(summary));

const ledger = wb.worksheets.getItem("Game Ledger");
console.log("FINAL_RECORD", JSON.stringify(ledger.getRange("K87:L87").values));
console.log("TOTAL_GAME_MINUTES", JSON.stringify(readme.getRange("B11:D11").values));

const minutes = wb.worksheets.getItem("Season Minutes");
console.log("MINUTES_AUDIT", JSON.stringify(minutes.getRange("E31:K31").values));

const assignment = wb.worksheets.getItem("ATL Assignment");
const donorAudit = assignment.getRange("B5:D11").values;
console.log("ATL_DONOR_AUDIT", JSON.stringify(donorAudit));
for (const row of donorAudit) {
  if (row[2] !== "PASS") {
    errors++;
    console.log(`DONOR_AUDIT_FAIL ${JSON.stringify(row)}`);
  }
}

const receivers = wb.worksheets.getItem("ATL Receivers");
const receiverSummary = receivers.getRange("B4:P4").values[0];
console.log("ATL_RECEIVER_AUDIT", JSON.stringify(receiverSummary));
if (receiverSummary[14] !== "PASS") {
  errors++;
  console.log(`RECEIVER_SUMMARY_FAIL ${JSON.stringify(receiverSummary)}`);
}
const receiverRows = receivers.getRange("K7:P37").values;
for (let i = 0; i < receiverRows.length; i++) {
  const [capacity, allocated, adjusted, dateAllocated, gamePool, balance] = receiverRows[i].map(Number);
  if (allocated - capacity > 0.001 || Math.abs(gamePool - dateAllocated) > 0.001 || Math.abs(balance) > 0.001 || adjusted < 0) {
    errors++;
    console.log(`RECEIVER_ROW_FAIL row ${i + 7}: ${JSON.stringify(receiverRows[i])}`);
  }
}
const receiverTotals = receivers.getRange("A43:I47").values;
const expectedReceiverMinutes = new Map([
  ["Justin Anderson",105.6],
  ["Alex Poythress",48.6],
  ["Daniel Hamilton",11.4],
  ["Miles Plumlee",17.5],
  ["B.J. Johnson",0],
]);
for (const row of receiverTotals) {
  const expected = expectedReceiverMinutes.get(row[0]);
  if (expected === undefined || Math.abs(Number(row[5]) - expected) > 0.001) {
    errors++;
    console.log(`RECEIVER_TOTAL_FAIL ${JSON.stringify(row)}`);
  }
}

const priors = wb.worksheets.getItem("ATL Priors");
const priorAudit = priors.getRange("A37:D44").values;
console.log("ATL_PRIOR_AUDIT", JSON.stringify(priorAudit));
for (const row of priorAudit) {
  if (row[3] !== "PASS") {
    errors++;
    console.log(`PRIOR_AUDIT_FAIL ${JSON.stringify(row)}`);
  }
}
const priorRows = priors.getRange("A19:J24").values;
for (const row of priorRows) {
  const observedMinutes = Number(row[2]);
  const observedBpm = row[3] === "" || row[3] === null ? null : Number(row[3]);
  const mean = Number(row[4]);
  const weight = Number(row[5]);
  const low = Number(row[8]);
  const base = Number(row[6]);
  const band = Number(row[7]);
  const high = Number(row[9]);
  if (!(low <= base && base <= high && low >= -6 && high <= 2)) {
    errors++;
    console.log(`PRIOR_RANGE_FAIL ${JSON.stringify(row)}`);
  }
  const expectedWeight = observedBpm === null ? 0 : observedMinutes / (observedMinutes + 750);
  const expectedBase = observedBpm === null ? mean : expectedWeight * observedBpm + (1 - expectedWeight) * mean;
  const expectedBand = observedBpm === null ? 1.5 : 0.75 + 500 / (observedMinutes + 500);
  const expectedLow = Math.max(-6, expectedBase - expectedBand);
  const expectedHigh = Math.min(2, expectedBase + expectedBand);
  if ([weight - expectedWeight, base - expectedBase, band - expectedBand, low - expectedLow, high - expectedHigh].some((delta) => Math.abs(delta) > 0.00001)) {
    errors++;
    console.log(`PRIOR_FORMULA_RECALC_FAIL ${JSON.stringify(row)}`);
  }
}
const priorAssumptions = priors.getRange("B7:B13").values.flat().map(Number);
const outcomeAssumptions = priors.getRange("E7:F13").values;
const expectedPriorAssumptions = [-2.75,750,0.75,500,-6,2,1.5];
for (let i = 0; i < expectedPriorAssumptions.length; i++) {
  if (Math.abs(priorAssumptions[i] - expectedPriorAssumptions[i]) > 0.00001) {
    errors++;
    console.log(`PRIOR_ASSUMPTION_FAIL row ${i + 7}: ${priorAssumptions[i]}`);
  }
}
if (outcomeAssumptions[0][0] !== "HOLD" ||
    Number(outcomeAssumptions[1][0]) !== 0 ||
    Math.abs(Number(outcomeAssumptions[2][0]) - 0.85) > 0.00001 ||
    Math.abs(Number(outcomeAssumptions[3][0]) + 0.5) > 0.00001 ||
    Math.abs(Number(outcomeAssumptions[4][0]) - 0.0125) > 0.00001 ||
    Number(outcomeAssumptions[5][0]) !== 45 ||
    Math.abs(Number(outcomeAssumptions[5][1]) - 0.005) > 0.00001 ||
    Number(outcomeAssumptions[6][0]) !== 120 ||
    Math.abs(Number(outcomeAssumptions[6][1]) - 0.0025) > 0.00001) {
  errors++;
  console.log(`OUTCOME_ASSUMPTION_FAIL ${JSON.stringify(outcomeAssumptions)}`);
}
const seed = priors.getRange("E14:E15").values.flat();
const computedSeedSha = createHash("sha256").update(String(seed[0]), "utf8").digest("hex");
if (seed[0] !== "FIRST_REBOUND|R09|ATL_2018_19|PRIOR_v1" || seed[1] !== computedSeedSha || seed[1] !== "228aac4642a599e4545ed878efda7952bf04bf1b0ad73b20b217d44f5aa19cab") {
  errors++;
  console.log(`PRIOR_SEED_FAIL ${JSON.stringify(seed)}`);
}
const hashSpec = String(priors.getRange("E16").values[0][0]);
if (!hashSpec.includes("ATL_2018_19_G001..G082") || !hashSpec.includes("BE64") || !hashSpec.includes(">>11") || !hashSpec.includes("2^53")) {
  errors++;
  console.log(`HASH_SPEC_FAIL ${hashSpec}`);
}
const eventIds = Array.from({ length: 82 }, (_, index) => `ATL_2018_19_G${String(index + 1).padStart(3, "0")}`);
const latentHashes = eventIds.map((eventId) => createHash("sha256").update(`${seed[0]}|${eventId}`, "utf8").digest("hex"));
const ledgerEventIds = ledger.getRange("Z6:Z87").values.flat();
if (new Set(eventIds).size !== 82 || new Set(latentHashes).size !== 82 || JSON.stringify(ledgerEventIds) !== JSON.stringify(eventIds)) {
  errors++;
  console.log("EVENT_ID_HASH_UNIQUENESS_FAIL");
}
const firewallText = String(priors.getRange("F37").values[0][0]);
if (!firewallText.includes("LOW = new LOW - donor HIGH") || !firewallText.includes("HIGH = new HIGH - donor LOW") || !firewallText.includes("fixed-100-possession")) {
  errors++;
  console.log(`REPLACEMENT_UNCERTAINTY_SPEC_FAIL ${firewallText}`);
}

const outcomeColumns = ledger.getRange("V6:X87").values;
for (let i = 0; i < outcomeColumns.length; i++) {
  const [status, result, downstream] = outcomeColumns[i];
  if (status !== "HOLD" || result !== "HOLD" || downstream !== "OUTCOME_INPUTS_PENDING") {
    errors++;
    console.log(`OUTCOME_FIREWALL_FAIL row ${i + 6}: ${JSON.stringify(outcomeColumns[i])}`);
  }
}

const gameMinuteChecks = ledger.getRange("U6:U87").values;
for (let i = 0; i < gameMinuteChecks.length; i++) {
  if (Math.abs(Number(gameMinuteChecks[i][0])) > 0.001) {
    errors++;
    console.log(`GAME_MINUTE_BALANCE_FAIL row ${i + 6}: ${gameMinuteChecks[i][0]}`);
  }
}

const draftBoard = wb.worksheets.getItem("2018 Draft Board");
console.log("DRAFT_BOARD_AUDIT", JSON.stringify(draftBoard.getRange("A4:H4").values));

const spurs = wb.worksheets.getItem("Spurs Impact");
console.log("SPURS_IMPACT_AUDIT", JSON.stringify(spurs.getRange("J16:L21").values));

const cascade = wb.worksheets.getItem("Cascade Impact");
console.log("CASCADE_IMPACT_AUDIT", JSON.stringify(cascade.getRange("J22:L27").values));

const seasonTotals = minutes.getRange("E31:K31").values[0];
if (Math.abs(Number(seasonTotals[3]) - 805) > 0.001 || Math.abs(Number(seasonTotals[4]) - 805) > 0.001 || Math.abs(Number(seasonTotals[5]) - 19853) > 0.001 || Math.abs(Number(seasonTotals[6])) > 0.001) {
  errors++;
  console.log(`SEASON_REALLOCATION_FAIL ${JSON.stringify(seasonTotals)}`);
}

if (errors > 0) {
  await fs.rm(`${inputPath}.inspect.ndjson`, { force: true });
  console.error(`FAILED: ${errors} formula error(s)`);
  process.exit(1);
}
await fs.rm(`${inputPath}.inspect.ndjson`, { force: true });
console.log("PASS: no formula errors in audited ranges");
