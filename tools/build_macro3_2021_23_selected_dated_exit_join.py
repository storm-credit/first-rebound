"""Finite dated macro3 source consumer; no ancestor producer invocation."""
from __future__ import annotations
import argparse, copy, hashlib, json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SELF="tools/build_macro3_2021_23_selected_dated_exit_join.py"
OUTPUT="simulation/MACRO3_2021_23_SELECTED_DATED_EXIT_JOIN.json"
MARKDOWN="simulation/MACRO3_2021_23_SELECTED_DATED_EXIT_JOIN.md"
PATHS={'AUDIT': 'research/MACRO3_2021_23_FINITE_EXIT_AUDIT_2026_10_08.json', 'M1': 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json', 'A': 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json', 'ORL': 'simulation/CHICAGO_ORLANDO_2021_22_SELECTED_KEEPER_RESULTS.json', 'SAS': 'simulation/CHICAGO_SAN_ANTONIO_2021_22_SELECTED_KEEPER_RESULTS.json', 'NOP': 'simulation/CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT.json', 'PORT': 'simulation/NBA_2022_23_NPC_CONTRACT_PORTFOLIO.json', 'NPC': 'canon/DELEGATED_2022_23_NPC_CORE_CONTRACT_EXECUTION_2026_10_08.json', 'T1': 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json', 'SQ1': 'simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json', 'C21': 'research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json', 'CORE': 'simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json', 'R22': 'simulation/CHICAGO_2022_ROOKIE_SELECTED_EXECUTION.json', 'G21': 'simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json', 'G22': 'simulation/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS.json', 'PO22': 'simulation/NBA_2022_SELECTED_FULL_POSTSEASON.json', 'PO23': 'simulation/NBA_2023_SELECTED_FULL_POSTSEASON.json', 'ROUTINE': 'simulation/CHICAGO_2023_SELECTED_ROUTINE_EXECUTION.json', 'DOMAIN': 'simulation/CHICAGO_2023_ROUTINE_COST_DOMAIN.json', 'RPEER': 'reviews/CHI_2023_SELECTED_ROUTINE_EXECUTION_G11_INDEPENDENT_REVIEW_2026_10_08.json', 'DPEER': 'reviews/CHICAGO_2023_ROUTINE_COST_DOMAIN_G11_INDEPENDENT_REVIEW_2026_10_08.json', 'LM': 'simulation/LAMELO_2023_SELECTED_EXTENSION.json', 'LPEER': 'reviews/LAMELO_2023_SELECTED_EXTENSION_G11_INDEPENDENT_REVIEW_2026_10_08.json', 'CLAIMS': 'research/CHICAGO_2023_NAMED_DRAFT_CLAIMS_AND_COST_PORTS_2026_10_08.json', 'DRAW': 'canon/DELEGATED_2023_DRAFT_ORIGIN_DRAW_DECISION_2026_10_08.json', 'J16': 'simulation/CHICAGO_2023_SELECTED_ROOKIE_EXECUTION.json', 'JPEER': 'reviews/CHI_2023_SELECTED_ROOKIE_EXECUTION_G11_INDEPENDENT_REVIEW_2026_10_08.json', 'JEXTERNAL': 'reviews/CHI_2023_J16_EXTERNAL_DISPOSITION_2026_10_08.json'}
PINS={'research/MACRO3_2021_23_FINITE_EXIT_AUDIT_2026_10_08.json': '40e01b77d63773d04f27202ae1d0197ccb5a733cf65a4f48f73abd2877e2c3ed', 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json': '253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088', 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json': '9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce', 'simulation/CHICAGO_ORLANDO_2021_22_SELECTED_KEEPER_RESULTS.json': '0b028cd28271954dc78c547475f128457cc9194d08797787e7fcd4ebf619c147', 'simulation/CHICAGO_SAN_ANTONIO_2021_22_SELECTED_KEEPER_RESULTS.json': '8a855d70fb97195e77caaca8062e093b7de2c9d2217c79c701fb4de1fd4fd14f', 'simulation/CHICAGO_NEW_ORLEANS_2021_SELECTED_KEEPER_RESULT.json': 'd1975077c8879807d63763d77d58a2d89f8b481ec6c2964f0a6a9bf7a96138fd', 'simulation/NBA_2022_23_NPC_CONTRACT_PORTFOLIO.json': '123d07df572ac4350e9528b3f0b913b3013ad4d51584c88a94e78051b9c7af19', 'canon/DELEGATED_2022_23_NPC_CORE_CONTRACT_EXECUTION_2026_10_08.json': '0b03b3c9afa279b9537af21da44f70565407a284832dce71aeeb333489433da5', 'simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json': 'f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306', 'simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json': '11140e49baa665f18e267fa6419efa238302250b724fa51cfd3262b010b4a312', 'research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json': '7244beff7a120c5ca246a04e72b61586f3cfbe245487d5fc6479f5245fd78d9f', 'simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json': 'e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7', 'simulation/CHICAGO_2022_ROOKIE_SELECTED_EXECUTION.json': '3c06967cf8c7171f815819efd3b4a71fb88ac77db3ae8798b34afeeeae93ce1c', 'simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json': '93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8', 'simulation/NBA_2022_23_GLOBAL_SELECTED_REGULAR_RESULTS.json': '8e2a778fe646de3c6070be7dd3acc64199fe2a7c813e780916e380b099fa3889', 'simulation/NBA_2022_SELECTED_FULL_POSTSEASON.json': 'b571c7645e006df1d63ead19e46343b4234034f10a9883539f52e0f9f7c7ff10', 'simulation/NBA_2023_SELECTED_FULL_POSTSEASON.json': 'ecc876c91d1008285b944fd9b7e7213a1c3e54b94d0a2fea84cd82b2f7cb0407', 'simulation/CHICAGO_2023_SELECTED_ROUTINE_EXECUTION.json': '9a4f6db21d6ad50e2c6d6897f1c2dedbdf440cee89bae47019f4bd131f341790', 'simulation/CHICAGO_2023_ROUTINE_COST_DOMAIN.json': '13448f381896ee9da4da16e9716b98f7bb511ecd42b527dcba26802a64ba1f8d', 'reviews/CHI_2023_SELECTED_ROUTINE_EXECUTION_G11_INDEPENDENT_REVIEW_2026_10_08.json': 'e9bfc3699dd2da3c4cfd6871e05f1b729748674018e617f098f3e5138065f169', 'reviews/CHICAGO_2023_ROUTINE_COST_DOMAIN_G11_INDEPENDENT_REVIEW_2026_10_08.json': 'a05b70a2234dd9efd4f3243f2f6a0e03cc7402f91ec477b12b3864ff626a3fb7', 'simulation/LAMELO_2023_SELECTED_EXTENSION.json': '98f03115f8a71a7f2e0ac3f9376aae5f94647d62c8ce6d942b63881af629483d', 'reviews/LAMELO_2023_SELECTED_EXTENSION_G11_INDEPENDENT_REVIEW_2026_10_08.json': 'abea927ebaac99d389a07d128b47d016adb0a387cc709e23a5e58b21597627d3', 'research/CHICAGO_2023_NAMED_DRAFT_CLAIMS_AND_COST_PORTS_2026_10_08.json': 'b139af4af09a48dd1c9e345d17d05fc8e38f4cb021193f32bc3a09ed537f49e3', 'canon/DELEGATED_2023_DRAFT_ORIGIN_DRAW_DECISION_2026_10_08.json': '6df7f62328263c0b3864e2d4a05cb4a5b56edbd332d5d31556627c6b421d9292', 'simulation/CHICAGO_2023_SELECTED_ROOKIE_EXECUTION.json': '61979a4edc201e314cf7e523393fbe3131f8d3eec547b530ede260729a791511', 'reviews/CHI_2023_SELECTED_ROOKIE_EXECUTION_G11_INDEPENDENT_REVIEW_2026_10_08.json': '2cec63e86be97c86429667a1907312c59833e6d374b5cfc4617491abe337ee6c', 'reviews/CHI_2023_J16_EXTERNAL_DISPOSITION_2026_10_08.json': 'e6ee358b1d845ce383a6e98def0849d9d508442a2bae7b7746fdebb94a187abc'}

def text(root,p): return (root/p).read_text(encoding="utf-8-sig").replace("\r\n","\n").replace("\r","\n")
def sha(root,p): return hashlib.sha256(text(root,p).encode()).hexdigest()
def direct(root,p): return json.loads(text(root,p))
def sources(root):
    for p,h in PINS.items():
        assert sha(root,p)==h, f"Stale source {p}"
    return {k:direct(root,p) for k,p in PATHS.items()}
def physical(root):
    # Independent caller parse; never call the replaceable sources/direct loader.
    return {k:json.loads((root/p).read_text(encoding="utf-8-sig")) for k,p in PATHS.items()}
def one(rows,player):
    a=[x for x in rows if x.get("player")==player]
    assert len(a)==1, f"Named contract identity {player}"
    return copy.deepcopy(a[0])

def actors(s):
    rows=[]
    for k,player,owner in [("ORL","Nikola Vucevic","ORL"),("SAS","DeMar DeRozan","SAS"),("NOP","Lonzo Ball","NOP")]:
        prior=one(s[k]["lawful_contract_family"],player)
        carry=one(s["PORT"]["NPC_contract_rows"],player)
        assert carry["candidate_owner"]==owner and carry["original_all_Gamma_reserved"]
        row={"player":player,"selected_owner":owner,"Chicago_acquisition":False,
             "original_Chicago_trade_or_SandT_imported":False,"2021_contract_family":prior,
             "FY22_same_owner_admitted_function":carry["execution_policy"],
             "original_Gamma_reserved":True,"actual_price_or_receipt_certified":False}
        if player=="Lonzo Ball":
            row["FY22_price_function_superseding_generation_minimum"]=one(s["NPC"]["selected_core_execution"],player)
        rows.append(row)
    rows.extend([
      {"player":"Alex Caruso","selected_owner":"CHI","2021_selected_SQ1_events":[copy.deepcopy(x) for x in s["SQ1"]["working_events"] if "CARUSO" in x["id"]],"original_Gamma_reserved":True},
      {"player":"Lauri Markkanen","selected_owner":"CHI","2021_author_selected_terms":copy.deepcopy(s["M1"]["selected"]),"original_Gamma_reserved":True},
      {"player":"Zach LaVine","selected_owner":"CHI","2022_selected_contract":copy.deepcopy(s["CORE"]["contract_terms"]["LaVine"]),"original_Gamma_reserved":True},
      {"player":"Protagonist","selected_owner":"CHI","2022_selected_contract":copy.deepcopy(s["CORE"]["contract_terms"]["Protagonist"]),"original_Gamma_reserved":True}])
    return rows

def costs(s):
    c21=s["C21"]; c22=s["R22"]["working_execution"]; d=s["DOMAIN"]; j=s["J16"]
    states=[x for c in c21["cases"] for x in c["states"]]
    assert len(c21["categories"])==6 and len(states)==600
    assert all(x["whole_cost_pass"] and x["apron_complete_upper"]<=143002000 for x in states)
    return {
      "2021": {"six_categories":copy.deepcopy(c21["categories"]),"dated_state_count":10,"source_case_count":60,
        "checked_source_case_states":600,"maximum_apron_over_all_source_states":max(x["apron_complete_upper"] for x in states),
        "final_apron_upper":c21["summary"]["complete_apron_upper"],"apron":143002000,
        "final_margin":143002000-c21["summary"]["complete_apron_upper"],
        "full_source_domain_pass":True,"source_has_selected_2021_hardcap":any(x["hard_cap_triggered"] for x in states)},
      "2022": {"pre_rookie_July7":copy.deepcopy(s["CORE"]["cost_on_2022_07_07"]),
        "Kessler_Stanley_refinement":copy.deepcopy(c22["cost"]),"retained_waived_Gamma":copy.deepcopy(c22["dead_protection_reservation"]),
        "registration":copy.deepcopy(c22["registration_summary"]),"normal":162976941,"apron":164614941,
        "2021_hardcap_carried_into_2022":False,"new_hardcap_trigger":False,
        "negative_apron_screen_is_illegality":False},
      "2023": {"six_categories":copy.deepcopy(d["six_categories"]),"domains":copy.deepcopy(d["domains"]),
        "legal_checks":copy.deepcopy(d["symbolic_legal_checks"]),"pre_RSC_forms":copy.deepcopy(d["cost_forms"]),
        "hold_lifecycle":copy.deepcopy(d["hold_lifecycle_through_FY23"]),"selected_J16_cost":copy.deepcopy(j["cost_join"]),
        "normal_signed_outer":"157912834 + R23 + 6/5*S23(16,1)",
        "apron_signed_outer":"157912834 + R23 + 6/5*S23(16,1), conservative annual QO reservation; actual date charge follows lifecycle",
        "R23":[0,16371000],"new_hardcap_trigger":False,"tax_is_same_as_apron":False,
        "M_S_are_lawfully_prepared_functions_not_arbitrary_positive_inputs":True,
        "J16_price_domain":["S4=S3*767/500","M4<=6/5*S3*767/500","each_y M_y<=6/5*S_y","max(4/5,max_y M_y/S_y)<=alpha_RT<=6/5"],
        "normal_unsigned_hold_replaced_once":True,"normal_unsigned_to_RSC_delta":0,
        "apron_RT_to_RSC_delta":"(6/5-alpha_RT)*S1 >=0; not generally zero",
        "exact_prepared_rounding_or_private_totals_certified":False}}

def dated(s):
    return [
      {"period":"2021-07-28/29","scope":"T1 atomic AP1/SG16 and 60 sequential rights; contracts separate", "source":PATHS["T1"],"events":copy.deepcopy(s["T1"]["event_trace"]),"CHI_rows":[copy.deepcopy(x) for x in s["T1"]["selected_rows"] if x["pick"] in (10,39)]},
      {"period":"2021-08-03..12","scope":"M1/A/SQ1 selected legal implementation; ten same-date ordered transitions", "source":PATHS["SQ1"],"events":copy.deepcopy(s["SQ1"]["working_events"]),"STD":15,"TW":2},
      {"period":"2021-10-01..2022-07-07","scope":"Original options/CX1, ordinary P QO, expiries and six new UPCs; hold replaced once", "source":PATHS["CORE"],"events":copy.deepcopy(s["CORE"]["event_trace"])},
      {"period":"2022-selected-rookie-transition","scope":"Kessler UPC after Stanley nonassignment waiver with full current liability; Ellis rights-only", "source":PATHS["R22"],"events":copy.deepcopy(s["R22"]["working_execution"]["fictional_process"]),"STD":15,"TW":2},
      {"period":"2023-06-28..2023-10-01","scope":"June28 live9 is FY23 forward projection, not June28 actual registration; four routine states then J16 overlay", "source":PATHS["ROUTINE"],"events":copy.deepcopy(s["ROUTINE"]["dated_states"])},
      {"period":"2023-06-22/2023-07-07","scope":"June22 rights delta0/registration unknown; July7 valid tender then 15STD0TW", "source":PATHS["J16"],"events":copy.deepcopy(s["J16"]["dated_events"]),"STD_after_UPC":15,"TW_after_UPC":0},
      {"period":"2023-07-07T12:01ET","scope":"LM1 adds only 2024..2028 obligations, no FY23 new salary/slot", "source":PATHS["LM"],"terms":copy.deepcopy(s["LM"]["selected_terms"])},
      {"period":"2023-10-01/after2023-10-02..2024-06-30","scope":"Selected FY24 option notices add no FY23 salary; expired standard QO -> normal FA holds/ROFR, no new UPC", "source":PATHS["DOMAIN"],"option_notices":copy.deepcopy(s["ROUTINE"]["selected_FY24_option_notices"]),"lifecycle":copy.deepcopy(s["DOMAIN"]["hold_lifecycle_through_FY23"])}]

def compose(s):
    return {"named_seven_actor_rows":actors(s),"dated_groups":dated(s),"cost_family_join":costs(s),
      "selected_contract_carry_bank":{"2021_M1_A_authority":copy.deepcopy(s["A"]),"2022_selected_rows":copy.deepcopy(s["CORE"]["selected_contracts"]),"2022_all_terms":copy.deepcopy(s["CORE"]["contract_terms"]),"2023_named_contracts_and_rights":copy.deepcopy(s["ROUTINE"]["named_contracts_and_rights"])},
      "Chicago_pick_claims":copy.deepcopy(s["CLAIMS"]["named_claims"]),
      "selected_J16_contract":copy.deepcopy(s["J16"]["selected_contract"]),
      "post_J16_named_standard":copy.deepcopy(s["J16"]["post_signature_named_STD"]),
      "future_salary_and_option_ports":{"Carter_CX1":copy.deepcopy(s["CORE"]["contract_terms"]["Carter"]),
        "E2":copy.deepcopy(s["CORE"]["contract_terms"]["Protagonist"]),
        "LaVine":copy.deepcopy(s["CORE"]["contract_terms"]["LaVine"]),
        "Markkanen":copy.deepcopy(s["M1"]["selected"]),
        "LM1":copy.deepcopy(s["LM"]["future_salary_branches"]),
        "J16":copy.deepcopy(s["J16"]["selected_contract"]),
        "FY24_existing_option_notices":copy.deepcopy(s["ROUTINE"]["selected_FY24_option_notices"])},
      "selected_season_dependencies":[{"capyear":2021,"regular_summary":copy.deepcopy(s["G21"]["summary"]),"postseason_summary":copy.deepcopy(s["PO22"]["summary"])},
        {"capyear":2022,"regular_summary":copy.deepcopy(s["G22"]["summary"]),"postseason_summary":copy.deepcopy(s["PO23"]["summary"])}],
      "reviewed_new_consumers":{k:{"path":PATHS[k],"independent_review_completed":s[k]["independent_review_completed"]} for k in ("RPEER","DPEER","LPEER","JPEER")},
      "finite_original_macro3_dependency_join_complete":True,
      "scope":"Original seven actors' selected Chicago/non-Chicago paths, source-supported cost families and selected dated rights/contract implementation through 2023 transitions; future contracted salary functions preserved without inventing successor season results",
      "remaining_original_macro3_named_inputs":[],
      "successor_only_ports":copy.deepcopy(s["AUDIT"]["successor_only_ports"]),
      "certification":{"independent_review_of_this_new_join_completed":False,"root_macro3_central_promotion":False,
        "actual_private_salary_payment_receipt_foreign_law_or_medical_certificate":False,
        "all_2023_draft_UPCs_or_all_30_FY23_team_ledgers_required":False,
        "2023_24_season_results_chosen":False,"new_MVP_franchise_titlecount_or_ending_choice":False,
        "whole_macro3_central_state_changed":False,"manuscript_allowed":False}}

def guard(root,s,o):
    fresh=physical(root)
    assert s==fresh,"Returned consumed source differs from independent physical source"
    # Independent source projection caller checks; do not recall compose/actors/dated/costs.
    rows=o["named_seven_actor_rows"]
    assert [(x["player"],x["selected_owner"]) for x in rows]==[("Nikola Vucevic","ORL"),("DeMar DeRozan","SAS"),("Lonzo Ball","NOP"),("Alex Caruso","CHI"),("Lauri Markkanen","CHI"),("Zach LaVine","CHI"),("Protagonist","CHI")]
    assert all(x["original_Gamma_reserved"] for x in rows),"Original Gamma erased"
    for row,k in zip(rows[:3],("ORL","SAS","NOP")):
        assert row["2021_contract_family"]==one(fresh[k]["lawful_contract_family"],row["player"])
        assert row["FY22_same_owner_admitted_function"]==one(fresh["PORT"]["NPC_contract_rows"],row["player"])["execution_policy"]
        assert not row["Chicago_acquisition"] and not row["original_Chicago_trade_or_SandT_imported"]
    assert rows[2]["FY22_price_function_superseding_generation_minimum"]==one(fresh["NPC"]["selected_core_execution"],"Lonzo Ball")
    assert rows[3]["2021_selected_SQ1_events"]==[x for x in fresh["SQ1"]["working_events"] if "CARUSO" in x["id"]]
    assert rows[4]["2021_author_selected_terms"]==fresh["M1"]["selected"]
    for row,key in [(rows[5],"LaVine"),(rows[6],"Protagonist")]: assert row["2022_selected_contract"]==fresh["CORE"]["contract_terms"][key]
    g=o["dated_groups"]
    assert len(g)==8
    for i,k,field in [(0,"T1","event_trace"),(1,"SQ1","working_events"),(2,"CORE","event_trace"),(4,"ROUTINE","dated_states"),(5,"J16","dated_events")]:
        assert g[i]["events"]==fresh[k][field],"Dated event source identity changed"
    assert g[3]["events"]==fresh["R22"]["working_execution"]["fictional_process"]
    assert g[6]["terms"]==fresh["LM"]["selected_terms"]
    assert g[7]["lifecycle"]==fresh["DOMAIN"]["hold_lifecycle_through_FY23"] and g[7]["option_notices"]==fresh["ROUTINE"]["selected_FY24_option_notices"]
    assert g[0]["CHI_rows"]==[x for x in fresh["T1"]["selected_rows"] if x["pick"] in (10,39)]
    assert [x["player"] for x in g[0]["CHI_rows"]]==["Chris Duarte","Joe Wieskamp"]
    c=o["cost_family_join"]
    assert c["2021"]["six_categories"]==fresh["C21"]["categories"]
    states=[x for a in fresh["C21"]["cases"] for x in a["states"]]
    assert c["2021"]["maximum_apron_over_all_source_states"]==max(x["apron_complete_upper"] for x in states)
    assert (c["2021"]["final_apron_upper"],c["2021"]["final_margin"],c["2021"]["checked_source_case_states"])==(128914775,14087225,600)
    assert c["2022"]["Kessler_Stanley_refinement"]==fresh["R22"]["working_execution"]["cost"]
    assert c["2022"]["retained_waived_Gamma"]==fresh["R22"]["working_execution"]["dead_protection_reservation"]
    assert c["2022"]["registration"]==fresh["R22"]["working_execution"]["registration_summary"]
    assert c["2022"]["pre_rookie_July7"]==fresh["CORE"]["cost_on_2022_07_07"]
    assert c["2022"]["normal"]==144569941+16371000+2036000 and c["2022"]["apron"]==144569941+16371000+3674000
    assert not c["2022"]["2021_hardcap_carried_into_2022"] and not c["2022"]["negative_apron_screen_is_illegality"]
    for key,field in [("six_categories","six_categories"),("domains","domains"),("legal_checks","symbolic_legal_checks"),("pre_RSC_forms","cost_forms"),("hold_lifecycle","hold_lifecycle_through_FY23")]:
        assert c["2023"][key]==fresh["DOMAIN"][field],"2023 source cost function altered"
    assert c["2023"]["selected_J16_cost"]==fresh["J16"]["cost_join"]
    assert c["2023"]["normal_signed_outer"]=="157912834 + R23 + 6/5*S23(16,1)" and c["2023"]["apron_signed_outer"]=="157912834 + R23 + 6/5*S23(16,1), conservative annual QO reservation; actual date charge follows lifecycle", "Returned signed salary outer differs from preserved source budget and RSC"
    assert fresh["J16"]["cost_join"]["conditional_nonrookie_base_upper"]==157912834 and fresh["J16"]["cost_join"]["signed_normal_apron_annual_outer"]=="157912834+R23+6/5*S23(16,1)"
    assert c["2023"]["apron_RT_to_RSC_delta"]=="(6/5-alpha_RT)*S1 >=0; not generally zero", "Returned RT transition is not the source-defined salary difference"
    assert c["2023"]["M_S_are_lawfully_prepared_functions_not_arbitrary_positive_inputs"] is True
    assert c["2023"]["R23"]==[0,16371000] and c["2023"]["normal_unsigned_to_RSC_delta"]==0 and c["2023"]["normal_unsigned_hold_replaced_once"]
    assert c["2023"]["J16_price_domain"]==["S4=S3*767/500","M4<=6/5*S3*767/500","each_y M_y<=6/5*S_y","max(4/5,max_y M_y/S_y)<=alpha_RT<=6/5"]
    assert not c["2023"]["new_hardcap_trigger"] and not c["2023"]["tax_is_same_as_apron"] and not c["2023"]["exact_prepared_rounding_or_private_totals_certified"]
    assert o["selected_contract_carry_bank"]=={"2021_M1_A_authority":fresh["A"],"2022_selected_rows":fresh["CORE"]["selected_contracts"],"2022_all_terms":fresh["CORE"]["contract_terms"],"2023_named_contracts_and_rights":fresh["ROUTINE"]["named_contracts_and_rights"]},"Named original/current contract carry altered"
    assert o["Chicago_pick_claims"]==fresh["CLAIMS"]["named_claims"]
    assert [(x["origin"],x["round"],x.get("selected_holder",x.get("selected_CHI_receipt"))) for x in o["Chicago_pick_claims"]]==[("CHI",1,"CHI"),("CHI",2,"WAS"),("DEN",2,False)]
    assert o["selected_J16_contract"]==fresh["J16"]["selected_contract"] and o["post_J16_named_standard"]==fresh["J16"]["post_signature_named_STD"]
    assert len(set(o["post_J16_named_standard"]))==15 and "Jaime Jaquez Jr." in o["post_J16_named_standard"]
    assert all(s[k]["independent_review_completed"] for k in ("RPEER","DPEER","LPEER","JPEER"))
    for k in ("RPEER","DPEER","LPEER","JPEER"): assert o["reviewed_new_consumers"][k]=={"path":PATHS[k],"independent_review_completed":True}
    for key,source,field in [("Carter_CX1","CORE","Carter"),("E2","CORE","Protagonist"),("LaVine","CORE","LaVine")]:
        assert o["future_salary_and_option_ports"][key]==fresh[source]["contract_terms"][field]
    for key,value in [("Markkanen",fresh["M1"]["selected"]),("LM1",fresh["LM"]["future_salary_branches"]),("J16",fresh["J16"]["selected_contract"]),("FY24_existing_option_notices",fresh["ROUTINE"]["selected_FY24_option_notices"])]:
        assert o["future_salary_and_option_ports"][key]==value,"Future contracted obligation altered"
    for row,gkey,pkey in zip(o["selected_season_dependencies"],("G21","G22"),("PO22","PO23")):
        assert row["regular_summary"]==fresh[gkey]["summary"] and row["postseason_summary"]==fresh[pkey]["summary"]
        assert row["regular_summary"]["league_games"]==1230
    assert o["successor_only_ports"]==fresh["AUDIT"]["successor_only_ports"]
    assert o["finite_original_macro3_dependency_join_complete"] and o["remaining_original_macro3_named_inputs"]==[]
    assert all(v is False for v in o["certification"].values()),"New join authority or actual certification promoted"

def build(root=ROOT):
    s=sources(root); o=compose(s); guard(root,s,o)
    o.update({"id":"MACRO3_2021_23_SELECTED_DATED_EXIT_JOIN","status":"FINITE_ORIGINAL_SCOPE_DATED_JOIN_COMPLETE_PENDING_NEW_INDEPENDENT_REVIEW",
      "baseline_main":"4d1855333e7de3387d5af0c5f811ed014c2591d2",
      "original_rule_snapshot":copy.deepcopy(s["AUDIT"]["central_rule_snapshot"]),
      "source_sha256":{**PINS,SELF:sha(root,SELF)},"hash_convention":"UTF8 BOM stripped; CRLF/CR to LF; SHA256",
      "ancestor_producer_calls":0,"new_external_collection":0,"design_gate":"CLOSED","Pack_count":0,"manuscript_allowed":False})
    return o

def validate(d,root=ROOT):
    try:
        assert d==build(root),"Saved output differs from current source-bound join"
        return []
    except (AssertionError,KeyError,ValueError) as e: return [str(e)]

def render(d):
    return "\n".join(["# 2021–23 Chicago 원조건 선택 경로 최종 날짜 연결", "",
      "상태: 원 매크로3의 유한 의존성 연결 완료 · 이 신규 소비기 독립 검문 대기. 중앙 완료 승격은 root 소유.", "",
      "## 일곱 경로", "", "| 선수 | 선택 소유 | 연결 |", "|---|---|---|",
      *[f"| {x['player']} | {x['selected_owner']} | 원계약·Gamma 보존, 기존 Chicago 성장 방향 유지 |" for x in d['named_seven_actor_rows']], "",
      "## 비용과 시간", "",
      "- 2021: M1/A/SQ1의 10상태·60가족·600상태를 소비. 기존 NTMLE hardcap을 유지하며 최종 apron 상단 128,914,775 / 143,002,000, 여유 14,087,225.",
      "- 2022: E2 22/23.76/25.52/27.28m, CX1 50m, LaVine 직접 Bird 5년 및 Young/Sato·TW가족. Kessler RSC로 기존 한 예약을 대체하고 Stanley 원 2,351,532 전액을 별도 보존. normal 162,976,941 / apron 164,614,941. 새 hardcap이 없으므로 음수 apron screen을 불법이라고 판정하지 않는다.",
      "- 2023: Coby 12m×3와 법정 최소 4계약, 원 live9, R23 [0,16,371,000], 완전한 FA/QO 및 미사용 예외 정리를 소비. M/S는 법정 prepared 함수이며 임의 양수가 아니다. July7 J16 RSC 후 conservative annual normal/apron 상단은 `157912834+R23+6/5*S23(16,1)`.",
      "- June22는 지명권 선택·UPC 등록 변화0이며 당시 STD/TW는 미인증. July7 유효 RT 뒤 RSC가 14→15STD/0TW를 만든다. normal unsigned hold는 같은 120% 급여로 한 번 대체한다. apron RT 차액은 `(6/5-alpha_RT)*S1`이며 일반적으로 0이 아니다.",
      "- J16 Year4 reference는 `S3*767/500`. 모든 연도 최소 급여 제약 및 `M4<=6/5*S3*767/500`, `max(4/5,max_y M_y/S_y)<=alpha_RT<=6/5`를 유지한다. 정확 prepared cents 반올림 인증은 하지 않는다.",
      "- Dotson/Cook standard QO는 Oct2까지 outstanding. 미수락 만료 후에도 normal FA Amount와 ROFR을 보존하며 apron의 expired QO만 제거한다. 새 UPC/현금 지급은 발생하지 않는다.",
      "- LM1 July7 12:01 연장은 당해 급여·등록 Δ0. 2024–28 C24의 25%/법정 자격을 만족하는 30%와 고정 초년 기준 8% 함수다. MVP/수상은 선택하지 않았다. Duarte/Kessler Oct1 notice는 FY24 급여만 추가한다.", "",
      "## 입력과 검문 범위", "",
      "원칙의 역사 스냅샷, 원7명 계약 경로, 현행 2021/2022/2023 가족, LM1·J16 및 비용 독립 검문을 물리 SHA와 내용으로 연결한다. 반환 객체를 원디스크 독립 파싱과 비교하고 alias 오염을 거부한다. 조상 생산기는 재실행하지 않는다.",
      "이 출력은 admitted lawful fictional implementation의 유한 연결이다. 실제 사적 금액·접수·지급·임상·외국법 전체 인증이나 원래 모든 역사 사건을 확정하는 증인이 아니다.", "",
      "## 원조건 잔여와 후손", "",
      "원 매크로3의 명명 입력 잔여는 0. 신규 소비기의 root/G11 독립 검문과 중앙 승격이 남는다. 다른 59신인 UPC, 전30팀 2023–24 시즌, 미보고 미래 계약을 새 선행 gate로 추가하지 않는다. 새 실제 선택이나 의무가 생기면 해당 비용·권리 포트만 재개한다.", "",
      "## 프로젝트 진행", "", "| 묶음 | 상태 |", "|---|---|", "| 1 기반 | 완료 |", "| 2 첫 시즌 | 완료 |", "| 3 2021–23 Chicago | 유한 날짜 연결 완료·신규 검문 대기 |", "| 4 장기 커리어 | 미완료 |", "| 5 설계 전체 | 미완료 |", "| 6 Context Pack | 미완료 |", "| 7 최종 승인 | 미완료 |", "",
      "중앙 기준 미완료 큰 묶음 5개 / 6번까지 4개. v0.30 PARTIAL · CLOSED · Pack0 · 원고0.", "", "## 고정 원천", "",
      *[f"- `{p}` — `{h}`" for p,h in d['source_sha256'].items()], ""])

def self_test(root=ROOT):
    from unittest.mock import patch
    good=build(root); count=0
    faults=[("typed_normal_outer_zero",lambda o:o["cost_family_join"]["2023"].update(normal_signed_outer="0")),("actor_Gamma",lambda o:o["named_seven_actor_rows"][6].update(original_Gamma_reserved=False)),
      ("held_CHI_R2",lambda o:o["Chicago_pick_claims"][1].update(selected_holder="CHI")),
      ("J16_June22_future_registration",lambda o:o["dated_groups"][5]["events"][0].update(STD=14)),
      ("2022_dead_Gamma",lambda o:o["cost_family_join"]["2022"]["retained_waived_Gamma"].update(full_original_family_upper=0)),
      ("LM1_FY23_addition",lambda o:o["dated_groups"][6]["terms"].update(FY23_new_salary=1000000))]
    original=compose
    for name,f in faults:
        def bad(s,f=f):
            o=original(s);f(o);return o
        with patch(__name__+".compose",bad):
            try: build(root)
            except AssertionError: count+=1
            else: raise AssertionError("FALSE_PASS "+name)
    original_sources=sources
    def bad_source(r):
        s=original_sources(r); s["J16"]["selected_contract"]["team"]="LAL";return s
    with patch(__name__+".sources",bad_source):
        try: build(root)
        except AssertionError:count+=1
        else:raise AssertionError("FALSE_PASS returned source alias")
    assert validate(good,root)==[]
    return count

def main():
    p=argparse.ArgumentParser();p.add_argument("--write",action="store_true");p.add_argument("--check",action="store_true");p.add_argument("--self-test",action="store_true");a=p.parse_args()
    d=build()
    if a.write:
        (ROOT/OUTPUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        (ROOT/MARKDOWN).write_text(render(d),encoding="utf-8")
    if a.check:
        errors=validate(direct(ROOT,OUTPUT));assert not errors,errors
        assert text(ROOT,MARKDOWN)==render(d),"Markdown stale"
    n=self_test() if a.self_test else None
    print(json.dumps({"current":True,"seven_actor_rows":len(d["named_seven_actor_rows"]),"dated_groups":len(d["dated_groups"]),"remaining_original_named_inputs":0,"new_join_independent_review":False,"writer_negative_controls":n},ensure_ascii=False))
if __name__=="__main__":main()
