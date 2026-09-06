#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");

function readCsv(relativePath) {
  const text = fs.readFileSync(path.join(root, relativePath), "utf8").trim();
  const [headerLine, ...lines] = text.split(/\r?\n/);
  const headers = headerLine.split(",");
  return lines.map((line) => {
    const values = line.split(",");
    return Object.fromEntries(headers.map((header, index) => [header, values[index]]));
  });
}

function assertEqual(actual, expected, label) {
  if (actual !== expected) {
    throw new Error(`${label}: expected ${expected}, got ${actual}`);
  }
}

const roster = readCsv("simulation/CHICAGO_2019_20_ROSTER_BASELINE.csv");
const budget = readCsv("simulation/CHICAGO_2019_20_PROTAGONIST_MINUTE_BUDGET.csv");

assertEqual(roster.length, 17, "actual player count");
assertEqual(roster.reduce((sum, row) => sum + Number(row.seconds), 0), 940511, "actual team seconds");
assertEqual(roster.reduce((sum, row) => sum + Number(row.gs), 0), 325, "actual starts");

const byPlayer = new Map(roster.map((row) => [row.player, row]));
for (const row of budget) {
  const source = byPlayer.get(row.donor);
  if (!source) throw new Error(`unknown donor: ${row.donor}`);
  assertEqual(Number(row.available_seconds), Number(source.seconds), `${row.donor} available seconds`);
  assertEqual(
    Number(row.available_seconds) - Number(row.base_transfer_seconds),
    Number(row.remaining_seconds),
    `${row.donor} remaining seconds`,
  );
  if (Number(row.remaining_seconds) < 0) throw new Error(`negative remaining seconds: ${row.donor}`);
}

const totalTransfer = budget.reduce((sum, row) => sum + Number(row.base_transfer_seconds), 0);
assertEqual(totalTransfer, 83700, "BASE protagonist seconds");
assertEqual(totalTransfer / 60, 1395, "BASE protagonist minutes");

const direct = budget.find((row) => row.donor === "Chandler Hutchison");
assertEqual(Number(direct.base_transfer_seconds), 31608, "direct Hutchison transfer");
assertEqual(totalTransfer - Number(direct.base_transfer_seconds), 52092, "secondary transfer seconds");

const protectedPlayers = roster.filter((row) => row.donor_class === "PROTECTED_ZERO").map((row) => row.player);
for (const player of protectedPlayers) {
  if (budget.some((row) => row.donor === player && Number(row.base_transfer_seconds) !== 0)) {
    throw new Error(`protected player used as donor: ${player}`);
  }
}

console.log("PASS Chicago 2019-20 baseline");
console.log(`actual_players=${roster.length}`);
console.log("actual_team_minutes=15675:11");
console.log("actual_starts=325");
console.log("base_protagonist=1395:00");
console.log("direct_hutchison=526:48");
console.log("secondary_transfer=868:12");
