"""Finite post-M1/A/T1 ownership effects of three omitted historical Bulls trades."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_chicago_2021_three_original_trades_downstream.py"
OUT = "research/CHICAGO_2021_THREE_ORIGINAL_TRADES_DOWNSTREAM_2026_10_07.json"
MD = OUT.replace(".json", ".md")
PINS = {
    "canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json": "9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce",
    "canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json": "253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088",
    "simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json": "f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306",
    "simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json": "11140e49baa665f18e267fa6419efa238302250b724fa51cfd3262b010b4a312",
    "simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json": "3e35fd2abfeb32e2bc5b66b7796f843ca117359be1a419d037844d29177a26d8",
    "research/O15G8G_M1_2021_23_DEPENDENCY_CHAIN.md": "df5476deaeab6c067323b355ee526b572b6b3a471e35439ad0615baf00b180ae",
}
RAW_DIR = Path("C:/Users/Storm Credit/AppData/Local/Temp/fr-bulls-three-departures-20261007")
ORIGINAL = {
    "VUCEVIC": ("https://www.nba.com/bulls/news/bulls-acquire-all-star-nikola-vucevic-and-al-farouq-aminu-trade-magic", "78d75cab45c05afa369842921e9c3f742473c2e2e99792a0f729f99abfac7753"),
    "LONZO": ("https://www.nba.com/bulls/news/bulls-acquire-lonzo-ball", "9f7eb171ea1878d8b018a08abfbcd0a3c53f39617bfd306508035c5c605336d3"),
    "DEROZAN": ("https://www.nba.com/bulls/news/bulls-acquire-demar-derozan", "caa57a5024bb4f0bbb0f9232f1c155049fd28b93066abe22e0b9b4b8234e4329"),
    "SANCTION": ("https://pr.nba.com/bulls-heat-penalties-free-agency/", "82b5313e5ea4dbd06e9462fbbaa49d3a3f798f6868019a37f341fb94a41b6b19"),
}


def require(value: bool, why: str):
    if not value:
        raise ValueError(why)


def normalized_sha(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").encode()).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


class ScriptText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_ld, self.parts, self.ld, self.text = False, [], [], []

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("type") == "application/ld+json":
            self.in_ld, self.parts = True, []

    def handle_data(self, data):
        self.text.append(data)
        if self.in_ld:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.in_ld:
            self.ld.append(json.loads("".join(self.parts)))
            self.in_ld = False


def parse_official(path: Path):
    parser = ScriptText()
    parser.feed(path.read_bytes().decode("utf-8", errors="replace"))
    return parser


def source_inputs(root: Path):
    data = {}
    for relative, expected in PINS.items():
        path = root / relative
        require(normalized_sha(path) == expected, "Pinned selected source changed: " + relative)
        if relative.endswith(".json"):
            loaded = load_json(path)
            require(loaded == json.loads(path.read_bytes().decode("utf-8-sig")), "Selected JSON loader differs from physical source: " + relative)
            data[relative] = loaded
    facts = {}
    for name, (url, expected) in ORIGINAL.items():
        path = RAW_DIR / (name + ".html")
        raw = path.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == expected, "Official raw body changed: " + name)
        loaded = parse_official(path)
        physical = ScriptText()
        physical.feed(raw.decode("utf-8", errors="replace"))
        require((loaded.ld, loaded.text) == (physical.ld, physical.text), "Official body loader differs from physical source: " + name)
        if name == "SANCTION":
            text = " ".join(" ".join(loaded.text).split())
            require("next available second-round draft pick be forfeited" in text and "Lonzo Ball" in text, "Original sanction facts changed")
            facts[name] = {"body_locator": "official release text", "original_2021_penalty_reason": "Lonzo Ball early free-agency discussions", "original_next_available_2R_forfeited": True}
        else:
            require(len(loaded.ld) == 1, "Official NBA announcement JSON-LD missing: " + name)
            facts[name] = {"description": loaded.ld[0]["description"], "published_utc": loaded.ld[0]["datePublished"], "body_locator": "script[type=application/ld+json].description"}
        facts[name]["source_url"] = url
        facts[name]["raw_path"] = str(path)
        facts[name]["raw_sha256"] = expected
    return data, facts


def build(root: Path = ROOT):
    data, facts = source_inputs(root)
    a = data["canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json"]
    m = data["canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json"]
    t1 = data["simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json"]
    sq = data["simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json"]
    s2 = data["simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json"]
    require(a["selected"]["route"] == "G1A_PLUS_M1" and a["selected"]["event_direction"] == "Chicago pursues the growth-core 2021 offseason: Markkanen M1 stays, Green re-signing and Caruso acquisition are the chosen pursuit, Young and Satoransky remain on their contract-year path, and Theis leaves through free agency.", "Approved Chicago direction changed")
    require(set(a["mutually_exclusive_routes_not_selected"]) == {"G1C_PLUS_M1_LONZO", "G1D_PLUS_M1_DEROZAN"}, "Original Lonzo/DeRozan omission changed")
    require(m["selected"]["route"] == "M1" and m["selected"]["event"].startswith("Markkanen chooses a Chicago four-year guaranteed offer"), "M1 Chicago retention changed")
    require(t1["summary"]["working_draft_choices"] == 60 and t1["summary"]["prior_CHI_choices_preserved"] == 2, "T1 draft 60 changed")
    ownership = {(x["asset"], x["owner"]) for x in t1["final_asset_ownership"] if x["kind"] == "UNSIGNED_DRAFT_RIGHTS"}
    require({("CHI_2021_10:Chris Duarte", "CHI"), ("CHI_2021_39:Joe Wieskamp", "CHI")} <= ownership, "Chicago T1 picks changed")
    s2_rows = s2["pick_control_snapshot"]["rows"]
    require(any(x["origin"] == "CHI" and x["pick"] == 10 and x["control_holder"] == "CHI" for x in s2_rows), "S2 CHI 10 changed")
    require(any(x["origin"] == "CHI" and x["pick"] == 39 and x["control_holder"] == "CHI" for x in s2_rows), "S2 CHI 39 changed")
    roster = {x["player"] for x in sq["standard_roster_working"]}
    require(len(roster) == 15 and len(sq["two_way_working"]) == 2, "Chicago A 15+2 working slots changed")
    require({"Carter", "Young", "Satoransky", "LaMelo_pick4", "LaVine", "Markkanen", "Caruso"} <= roster, "Approved Chicago core or retained consideration absent")
    require(roster.isdisjoint({"Vučević", "Vucevic", "Aminu", "Lonzo Ball", "DeRozan", "Garrett Temple", "Otto Porter Jr."}), "Omitted transaction player appears in Chicago roster")
    desc = {key: value["description"] for key, value in facts.items() if "description" in value}
    require(all(term in desc["VUCEVIC"] for term in ("Nikola", "Al-Farouq Aminu", "Otto Porter Jr.", "Wendell Carter Jr.", "two first-round picks")), "Original Orlando exchange meaning changed")
    require(all(term in desc["LONZO"] for term in ("Lonzo Ball", "Garrett Temple", "Tomas Satoransky", "2024 second-round Draft pick", "cash considerations")), "Original Lonzo exchange meaning changed")
    require(all(term in desc["DEROZAN"] for term in ("DeMar DeRozan", "Thaddeus Young", "Al-Farouq Aminu", "protected first-round Draft pick", "two second-round draft picks")), "Original DeRozan exchange meaning changed")
    transactions = [
        {"id": "ORL_CHI_VUCEVIC_AMINU_2021_03", "historical_report": "ORL sends Vučević/Aminu; CHI sends Porter/Carter/protected firsts x2", "selected_original_transaction_executed": False, "selected_CHI_effect": ["Carter remains in approved 2021 A 15", "2021 CHI original-control pick #10 and #39 remain through selected T1; no Orlando transfer edge", "Porter not assumed on August 2021 roster without a new contract"], "counterparty_effect": "Orlando pre-trade Vučević/Aminu control continues in fictional March window; later Orlando contract/roster path must be dated separately", "asset_nontransfer": ["CHI_to_ORL_2021_protected_1R", "CHI_to_ORL_later_protected_1R"], "later_exact_pick_owner_certified": False, "other_NBA_transaction_or_contract_selected": False},
        {"id": "NOP_CHI_LONZO_2021_08", "historical_report": "CHI sends Temple via S&T, Satoransky, 2024 second and cash to NOP for Lonzo via S&T", "selected_original_transaction_executed": False, "selected_CHI_effect": ["Satoransky remains in approved A 15", "No Lonzo in approved A 15", "Temple absent from A 15; no new retained Temple contract is inferred"], "counterparty_effect": "No original Chicago→NOP package; Lonzo's alternate RFA/signing route remains typed", "asset_nontransfer": ["CHI_to_NOP_2024_2R_in_original_deal", "CHI_to_NOP_cash_in_original_deal"], "later_exact_pick_owner_certified": False, "historical_tampering_penalty_carried_into_fiction": False, "alternate_2023_2R_free_of_any_sanction_or_transfer_certified": False},
        {"id": "SAS_CHI_DEROZAN_2021_08", "historical_report": "CHI sends Young/Aminu/protected first/two seconds to SAS for DeRozan via S&T", "selected_original_transaction_executed": False, "selected_CHI_effect": ["Young remains in approved A 15", "No Aminu or DeRozan in approved A 15", "No original protected first/two seconds transferred by this deal"], "counterparty_effect": "San Antonio cannot use Young acquired through this omitted Chicago deal for the original 2022 Toronto Young exchange; DeRozan's alternate free-agent path is typed", "asset_nontransfer": ["CHI_to_SAS_protected_1R_in_original_deal", "CHI_to_SAS_two_2R_in_original_deal"], "later_exact_pick_owner_certified": False, "original_SAS_to_TOR_Young_trade_automatically_copied": False},
    ]
    return {"schema": "CHI_2021_M1A_THREE_OMITTED_ORIGINAL_TRADES_DOWNSTREAM_V1", "status": "THREE_OMITTED_ORIGINAL_TRADES_SOURCE_BOUND_ASSET_AND_ROLE_EFFECTS_SELECTED", "source_sha256": dict(PINS), "source_hash_method": "UTF8_LF_SHA256", "self_sha256": normalized_sha(root / SELF), "official_historical_reports": facts, "selected_predecessors": {"M1_G1A_direction": True, "S2_control_CHI_10_39": True, "T1_60_working_draft": True, "Chicago_A_working_standard": 15, "Chicago_A_working_two_way": 2}, "transaction_effects": transactions, "Chicago_approved_working_roster_relevant": sorted(roster & {"Carter", "Young", "Satoransky", "Markkanen", "Caruso", "LaMelo_pick4", "LaVine"}), "named_descendant_boundary": {"Young_to_SAS_then_TOR_original_chain": "NOT_COPIED_WITHOUT_SAS_OWNERSHIP", "Markkanen_to_CLE_then_Mitchell_original_consideration": "NOT_COPIED_M1_RETAINS_MARKKANEN_CHI", "Lonzo_early_talk_sanction": "ORIGINAL_FACT_ONLY_ALTERNATE_INVESTIGATION_AND_PICK_OWNER_UNSELECTED", "2023_or_later_exact_pick_rights": "TYPED_AFTER_OTHER_MOVES_AND_SANCTIONS"}, "finite_remaining": ["Orlando later Vučević/Aminu roster and contract interval from no March Chicago transfer, including own-draft #3/#33 working T1 rights; do not invent their destination or re-signing.", "New Orleans Lonzo alternate RFA/signing/roster route and original 2024 second/cash nontransfer; the original tampering cause is absent but the alternate 2023 second-round asset requires its own ownership/sanction ledger.", "San Antonio DeRozan alternate UFA route and Young absence for original 2022 Toronto exchange/#20 consideration; Chicago retained Young/Satoransky contract-year expiry must be dated independently.", "2021–23 league results, player minutes and later pick dispositions are outside this three-transaction asset/role packet."], "limits": {"original_Mitchell_consideration_imported": False, "three_original_transactions_selected": False, "new_author_lock": False, "whole_macro3_complete": False, "BOS_OKC_HOU_or_29_team_book_complete": False, "actual_private_acceptance_or_receipt_certified": False, "manuscript_allowed": False}, "design_gate": "CLOSED", "freeze": "v0.30 PARTIAL"}


def validate(packet, root: Path = ROOT):
    require(packet == build(root), "Saved downstream packet differs from physical-source reconstruction")
    return []


def render(p):
    lines = ["# M1/A/T1 뒤 Chicago 세 원거래의 자산·역할 인계", "", "원역사 Chicago의 Vučević·Lonzo·DeRozan 거래를 선택된 세계에 자동 복사하지 않는다. M1/A와 S2 #10/#39, T1 60명 보드, A 작업명단 15+2를 대조했다.", "", "| 원거래 | 선택세계 Chicago | 상대·후속 |", "|---|---|---|"]
    for x in p["transaction_effects"]:
        lines.append(f"| {x['id']} 생략 | {'; '.join(x['selected_CHI_effect'])} | {x['counterparty_effect']} |")
    lines += ["", "Chicago의 Carter·Young·Satoransky는 A 작업명단에 남는다. Porter·Temple을 2021 여름 계약 만료 뒤 자동 잔류시키지 않는다. 원거래로 이전될 픽·현금은 해당 거래에서 **이동하지 않지만**, 후속 전체 소유권과 제재 부재까지 보증하지는 않는다.", "", "Lonzo 조기 접촉에 따른 실제 NBA 2R 박탈은 원역사 사실이다. Chicago가 이 경로에서 원 Lonzo 거래를 하지 않는다는 이유로 가상의 특정 2023 2R을 자동 복원하지 않는다. 원 Young을 이용한 Spurs→Toronto 거래와 Markkanen이 필요한 Cleveland→Utah Mitchell 원형 대가도 자동 실행하지 않는다.", "", "## 남은 유한 후손", "", *[f"{i}. {x}" for i, x in enumerate(p["finite_remaining"], 1)], "", "새 계약·픽/현금 수령·실존 당사자 수락·29팀 전체 원장·시즌 결과·원고를 인증하지 않는다. v0.30 PARTIAL, 설계/원고 CLOSED.", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    packet = build()
    if args.write:
        (ROOT / OUT).write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (ROOT / MD).write_text(render(packet), encoding="utf-8")
    if args.check:
        validate(load_json(ROOT / OUT))
        require((ROOT / MD).read_text(encoding="utf-8") == render(packet), "MD differs from JSON")
    if args.self_test:
        wrong = json.loads(json.dumps(packet))
        wrong["transaction_effects"][1]["selected_original_transaction_executed"] = True
        try:
            validate(wrong)
        except ValueError:
            pass
        else:
            raise AssertionError("Lonzo original trade falsely accepted")
    print("PASS", len(packet["transaction_effects"]), "original trades omitted; CHI retained", packet["Chicago_approved_working_roster_relevant"])


if __name__ == "__main__":
    main()
