import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
import fs from "node:fs/promises";

const inputPath = process.argv[2] ?? "simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx";
const blob = await FileBlob.load(inputPath);
const wb = await SpreadsheetFile.importXlsx(blob);

const checks = [
  ["README", "A4:H12"],
  ["Game Ledger", "A5:Y87"],
  ["ATL Assignment", "A4:H24"],
  ["Season Minutes", "A5:L33"],
  ["2018 Draft Board", "A4:K37"],
  ["Spurs Impact", "A4:L34"],
  ["Cascade Impact", "A4:M27"],
  ["Draft Bridge", "A4:J14"],
  ["Gate Audit", "A4:F16"],
  ["Sources", "A4:D47"],
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

if (errors > 0) {
  await fs.rm(`${inputPath}.inspect.ndjson`, { force: true });
  console.error(`FAILED: ${errors} formula error(s)`);
  process.exit(1);
}
await fs.rm(`${inputPath}.inspect.ndjson`, { force: true });
console.log("PASS: no formula errors in audited ranges");
