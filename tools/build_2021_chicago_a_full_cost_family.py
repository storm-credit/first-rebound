"""All six Chicago A cost categories, ten dated states; no unknown-to-zero.

The remaining legacy bridge is one finite public-model source question, not a
demand for a private contract ledger or an assertion of infinite liabilities.
"""
import argparse
import copy
import hashlib
import json
import re
import html
from unittest.mock import patch
from pathlib import Path
import build_2021_approved_a_draft_signing_execution as sq

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_2021_chicago_a_full_cost_family.py'
OUT = 'research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json'
MD = OUT[:-5] + '.md'
SQ = sq.OUT
PUBLIC = 'research/CHICAGO_PUBLIC_COMPONENT_BOUND_2026_10_06.json'
LEDGER = 'research/CHICAGO_DATED_PUBLIC_LEDGER_2026_10_05.json'
ANNUAL = 'research/CHICAGO_NEW_ANNUAL_EXCEPTION_WITNESS_2026_10_06.json'
COHORT = 'research/CHICAGO_2019_COHORT_CARRY_BOUNDARY_2026_10_05.json'
MINIMUM = 'research/CHICAGO_2019_MINIMUM_COHORT_EVIDENCE_2026_10_05.json'
SOURCES = [SQ, sq.SELF, PUBLIC, LEDGER, ANNUAL, COHORT, MINIMUM,
           sq.M1, sq.A, sq.SEQ, 'simulation/CAUSALITY_MODEL.md',
           'research/CHICAGO_2021_23_CONTINUATION_SOURCES.json',
           'research/O15G15BC_SIMONOVIC_DRAFT_RIGHTS_CLOCK.md']
PINS = {'simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json': '11140e49baa665f18e267fa6419efa238302250b724fa51cfd3262b010b4a312', 'tools/build_2021_approved_a_draft_signing_execution.py': '2e5c63ae32cc3897e1117c895687c047ed4fb1256e4addf888330697dc70c304', 'research/CHICAGO_PUBLIC_COMPONENT_BOUND_2026_10_06.json': '196cec339d3c3db24fd723c235b7a28efb0df37539adefc726b70bbc6716d7b3', 'research/CHICAGO_DATED_PUBLIC_LEDGER_2026_10_05.json': '185ff912de49a4ad4ff62083fd197f2cc9646be8eb464dd8cbc2553b89805e05', 'research/CHICAGO_NEW_ANNUAL_EXCEPTION_WITNESS_2026_10_06.json': '6c0114718bd674fd178ec4c20f6d98ddaf0bc3eae70da86232e9219f37b680ae', 'research/CHICAGO_2019_COHORT_CARRY_BOUNDARY_2026_10_05.json': '719db26e03ccde88eb1bde2a1e98b1341b6859d7abf5f4449472676ccdfd57e2', 'research/CHICAGO_2019_MINIMUM_COHORT_EVIDENCE_2026_10_05.json': '18657242b99986570d6ae78780348b5ad17604caae2a1e3c2ddff66da8ab9063', 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json': '253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088', 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json': '9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce', 'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE_INPUTS.json': '4b66d96a274fa4d31e41f6256192449e8b43a6dfc00e8f4e44f4cbd76e83bf78', 'simulation/CAUSALITY_MODEL.md': '00638830864e9503db4589464806cc0c4c0d94002b039a8bf661d96e6f6a7c45', 'research/CHICAGO_2021_23_CONTINUATION_SOURCES.json': '4dc3cfb7416174c0fea5c2710e9915a729d362dc553f216f4e9c861b373e9db3', 'research/O15G15BC_SIMONOVIC_DRAFT_RIGHTS_CLOCK.md': '27c44d66451c909f4e36de21ffcc7b26ff48ceac01678e3387914a0ed0cb523a'}
SOURCES.append('research/CHICAGO_SIMON_2019_CARRY_BOUNDARY_2026_10_05.json')
PINS['research/CHICAGO_SIMON_2019_CARRY_BOUNDARY_2026_10_05.json']='bf91c3bde817260eba45b62adc5a50825ce2229a3b136624d3fb78d626bded20'
RAW_OBSERVATIONS = [{'id': 'zach-lavine_2021_ROW', 'url': 'https://www.salaryswish.com/players/zach-lavine', 'classification': 'CURRENT_VENDOR_HISTORICAL_TABLE_NOT_LEAGUE_LEDGER', 'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-retained-zach-lavine-20261007.html', 'raw_sha256': '1525dc4eeff64c5b25ab04b327dd78f2a3b96493f11e6efb1fd31a1faec0bb0a', 'bytes': 108099, 'http_status': 200, 'locator': '2021-22 contract row', 'observed_rows': ['2021-22 | $19,500,000 | $19,500,000 | $19,500,000 | $0 | $0'], 'collected_date': '2026-10-07'}, {'id': 'thaddeus-young_2021_ROW', 'url': 'https://www.salaryswish.com/players/thaddeus-young', 'classification': 'CURRENT_VENDOR_HISTORICAL_TABLE_NOT_LEAGUE_LEDGER', 'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-retained-thaddeus-young-20261007.html', 'raw_sha256': '59113868938e938d8c78cc924891ae242dd407b2e35af2f833798b3f152a9b80', 'bytes': 124782, 'http_status': 200, 'locator': '2021-22 contract row', 'observed_rows': ['2021-22 | $14,190,000 | $14,190,000 (+5%) | $14,190,000 | (6.00M→14.2M) | $0 | $1,000,000'], 'collected_date': '2026-10-07'}, {'id': 'tomas-satoransky_2021_ROW', 'url': 'https://www.salaryswish.com/players/tomas-satoransky', 'classification': 'CURRENT_VENDOR_HISTORICAL_TABLE_NOT_LEAGUE_LEDGER', 'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-retained-tomas-satoransky-20261007.html', 'raw_sha256': '786358ed1a147e00b7f835aea084308acf481828d1be8c642c0f63ccd9a624c5', 'bytes': 106652, 'http_status': 200, 'locator': 'First original multiyear2021-22 row only; later2022 waiver/re-signing rows not adopted', 'observed_rows': ['2021-22 | W | $10,000,000 | $10,000,000 | $10,000,000 | (5.00M→10.0M) | $0 | $0'], 'collected_date': '2026-10-07'}, {'id': 'coby-white_2021_ROW', 'url': 'https://www.salaryswish.com/players/coby-white', 'classification': 'CURRENT_VENDOR_HISTORICAL_TABLE_NOT_LEAGUE_LEDGER', 'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-retained-coby-white-20261007.html', 'raw_sha256': '4600598bfbaf257bda6d838af6cb3e1f2523eb71f3345f13ee292c2acff14736', 'bytes': 105601, 'http_status': 200, 'locator': '2021-22 contract row', 'observed_rows': ['2021-22 | Team | Yes (Dec 19, 2020) | $5,837,760 | $5,837,760 (+5%) | $5,837,760 | (0→5.84M) | $0 | $0'], 'collected_date': '2026-10-07'}, {'id': 'wendell-carterjr_2021_ROW', 'url': 'https://www.salaryswish.com/players/wendell-carterjr', 'classification': 'CURRENT_VENDOR_HISTORICAL_TABLE_NOT_LEAGUE_LEDGER', 'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-retained-wendell-carterjr-20261007.html', 'raw_sha256': '6b9f1c5d557a1e6f48efde67eab01650acb76048d8ac4b22723ae56da573081f', 'bytes': 105566, 'http_status': 200, 'locator': '2021-22 contract row', 'observed_rows': ['2021-22 | Team | Yes (Dec 19, 2020) | $6,920,027 | $6,920,027 (+33%) | $6,920,027 | (0→6.92M) | $0 | $0'], 'collected_date': '2026-10-07'}, {'id': 'patrick-williams_2021_ROW', 'url': 'https://www.salaryswish.com/players/patrick-williams', 'classification': 'CURRENT_VENDOR_HISTORICAL_TABLE_NOT_LEAGUE_LEDGER', 'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-retained-patrick-williams-20261007.html', 'raw_sha256': 'd2e10fb00ca72aef97feca53b8ce5dc7f58464016a67068df72068abdfad84f4', 'bytes': 100132, 'http_status': 200, 'locator': '2021-22 contract row', 'observed_rows': ['2021-22 | $7,422,000 | $7,422,000 (+5%) | $7,422,000 | $0 | $0'], 'collected_date': '2026-10-07'}, {'id': 'noah-vonleh_CAMP2020_TERM', 'url': 'https://www.salaryswish.com/players/noah-vonleh', 'classification': 'CURRENT_VENDOR_HISTORICAL_CONTRACT_DURATION_NOT_PAYMENT_ZERO', 'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-carry-noah-vonleh-20261007.html', 'raw_sha256': '030ecb183fffa94b614af8e9b34d01d18eb88df620a3e0b1ce4f9303f3a5c17d', 'bytes': 124658, 'http_status': 200, 'locator': 'CHI November27,2020 contract Length1year; 2020-21 row', 'collected_date': '2026-10-07'}, {'id': 'zach-norvelljr_CAMP2020_TERM', 'url': 'https://www.salaryswish.com/players/zach-norvelljr', 'classification': 'CURRENT_VENDOR_HISTORICAL_CONTRACT_DURATION_NOT_PAYMENT_ZERO', 'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-carry-zach-norvelljr-20261007.html', 'raw_sha256': '420a69c35d63dc63eda69789fd927cd2394ca072b091c853b1730803332cd1ff', 'bytes': 98469, 'http_status': 200, 'locator': 'CHI November27,2020 contract Length1year; 2020-21 row', 'collected_date': '2026-10-07'}, {'id': 'BI_ORIGINAL', 'url': 'https://web.archive.org/web/20210422012709id_/http://www.basketballinsiders.com/chicago-bulls-team-salary/', 'raw_sha256': '332a9ea81c3f01a934b31d61c2a57ea8a287c9cb1956741545c97b09ccdfb985', 'locator': 'Updated3/29/21 Transactions: Nov27Norvell andDec6Shittu minimumsummerExhibit9; WaivedPlayers; nofutureAugustinventory', 'classification': 'REUSED_CONTEMPORANEOUS_ORIGINAL_PUBLIC_CATEGORY_MODEL_BODY_DIRECTLY_READ'}, {'id': 'BI_FUTURE_WIDGET', 'url': 'https://web.archive.org/web/20210424143800id_/http://hw-files.com/tools/salaries/salaries_widget_new.php?team_id=11', 'raw_sha256': '6732d03676ab709570d6fd11695604d54d912f6d2c48b8d4013e27d22fdc4733', 'locator': '2021-22 future column retained Salary/MarkQO9,026,852/GreenQO1,897,476; VonlehW row futureblank, notwholefuturechargecertificate', 'classification': 'REUSED_CONTEMPORANEOUS_ORIGINAL_PUBLIC_CATEGORY_MODEL_BODY_DIRECTLY_READ'}]
RAW_OBSERVATIONS += [{'url': 'https://www.rotowire.com/basketball/player/milton-doyle-4226', 'http_status': 200, 'raw_sha256': '22a974b0d51fa9abe36959d398e2bdab333aa402f7ae015475f08f2c8056b5b5', 'bytes': 505578, 'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-term-doyle-20261007.html', 'id': 'LEGACY_TERM_DOYLE', 'locator': 'Show Contract:2019SeptemberCHI one-year; Octoberwaiver', 'classification': 'PUBLIC_VENDOR_CONTRACT_DURATION_NOT_PAYMENT_OR_LEAGUE_LEDGER', 'collected_date': '2026-10-07', 'original_body_verified': True}, {'url': 'https://www.shamsports.com/players/walt-lemon', 'http_status': 200, 'raw_sha256': 'bc40da88e66827f51e5093e318b55f290a45755ce1e553f56dcbb8b932bcdd8e', 'bytes': 550998, 'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-term-lemon-20261007.html', 'id': 'LEGACY_TERM_LEMON', 'locator': 'Transactions March29,2019 CHI partiallyguaranteedminimum through2020', 'classification': 'PUBLIC_VENDOR_CONTRACT_DURATION_NOT_PAYMENT_OR_LEAGUE_LEDGER', 'collected_date': '2026-10-07', 'original_body_verified': True}, {'url': 'https://sports.yahoo.com/sources--omer-asik-agrees-to--60-million-contract-with-pelicans-041146135.html', 'http_status': 200, 'raw_sha256': 'd5a5158670e2558dfbca5c1669ca1339907d1e72b71b305eeddf80be7ba5de7d', 'bytes': 539081, 'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-term-asik-20261007.html', 'id': 'LEGACY_TERM_ASIK', 'locator': 'AdrianWojnarowski July2,2015 originalreport five-year2015–16 start', 'classification': 'ORIGINAL_REPORTER_NOT_REGISTERED_CONTRACT', 'collected_date': '2026-10-07', 'original_body_verified': True}, {'url': 'https://www.basketball-reference.com/teams/CHI/2020_transactions.html', 'http_status': 200, 'raw_sha256': '14efe5f2b7150e1046cbcba7a46d78aac2998471b3666bc32fc00ca6b5821971', 'bytes': 148067, 'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-term-callandret-bref-20261007.html', 'id': 'LEGACY_TERM_CALLANDRET', 'locator': 'September25,2019 transaction:Exhibit10; October17waiver', 'classification': 'PUBLIC_VENDOR_CONTRACT_DURATION_NOT_PAYMENT_OR_LEAGUE_LEDGER', 'collected_date': '2026-10-07', 'original_body_verified': True}, {'url': 'https://www.salaryswish.com/players/shaquille-harrison', 'http_status': 200, 'raw_sha256': '8db451f462f4c2eec3aeb2ad3f28fafc2b78b6bf1e2b85f3250b55e12f668750', 'bytes': 185908, 'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-term-harrison-ss-20261007.html', 'id': 'LEGACY_TERM_HARRISON', 'locator': 'CHI October21,2018Length2year through2019–20; July18,2019Length1year2019–20', 'classification': 'PUBLIC_VENDOR_CONTRACT_DURATION_NOT_PAYMENT_OR_LEAGUE_LEDGER', 'collected_date': '2026-10-07', 'original_body_verified': True}]
FAILED_TERM_RECOVERIES=[{'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-term-callandret-20261007.html', 'raw_sha256': '7f12500dca556caeade8543a818810d07941e5cbef9c412856415e5d24b7e967', 'bytes': 6087, 'outcome': 'HTTP403_not_used', 'used_for_term': False}, {'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-term-callandret-slam-20261007.html', 'raw_sha256': 'd870c991ca538f3c9571c97a412641a5350696e1b241fbd8cd67eca9b24d36c1', 'bytes': 5489, 'outcome': 'HTTP403_not_used', 'used_for_term': False}, {'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-term-harrison-forbes-20261007.html', 'raw_sha256': 'cca1ba7ef649da0c1ff0fade00755216c9ad468e09b2b3fecaef1d37cc653470', 'bytes': 770, 'outcome': 'HTTP403_not_used', 'used_for_term': False}, {'cache_path': 'C:\\Users\\STORMC~1\\AppData\\Local\\Temp\\fr-chi-2021-term-callandret-sham-20261007.html', 'raw_sha256': 'b8406fa20e7ae5f93260fe97c56ed35dc1954e7334d5be0c7dfb43d41b670bb7', 'bytes': 515257, 'outcome': 'HTTP200_player_profile_no_contractduration_not_used', 'used_for_term': False}]
RULE_OBSERVATIONS = [{'id': '2017_CBA_FULL_COST', 'url': 'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf', 'classification': 'PRIMARY_CBA_DIRECT_LOCAL_TEXT_READ', 'raw_sha256': '66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a', 'locator': 'I1cc/ddd/fff/ggg/gggg/hhhh; II3p/q/6/7; VII3b/4a/d/e/f/g/6b/e/i/m/7d; VIII1; X4/5; XI1', 'PDF_1based_text_sha256': {'27': 'b6fea4240f50597097936a1c22b5fc91f6c33599d44eebf7a6bed5d54ea52ed7', '35': 'a75d7cc2bd0f48a0a4e381dc3faf95b6c888438ddc38b082f35541f8cdcfc681', '42': '37539d63af3e925ae9ae2c33757950cf360c149b5aba1512f45c8ded1202bd4e', '44': 'e2c4bf9ae6db49e3c4abb66bb7d5239f8bf2eab03b3ca94a4f46dc781506b485', '54': 'b002f3d4c97245ae75d89d3e8d390574ee71de51c38cf25de405c67f622da9a1', '55': 'ca2c17388d44346413fe2b288d5da395a02849cda5600738373b321cc1be80da', '193': '8c437e14a675f6f2b28bb1189740ef8261d041ea083ea33e5f10e190bffb83a5', '203': 'ea2f428f7a27a68a94c4677f8904eba9e72cb5457486e3530f867105dcfb52d2', '204': '28e728fb04f6ed2adf1616a26bc8215088e56e0e3228e4bfd8f3c90dde41cc9a', '205': '475e7f377a4e991f829c7e51a975fca86325706177eff86df36d83d1a3c9e813', '206': 'e5c736cb6aae51bff5515753ed23070ec8e3079f47d7f966e3a3e5b40b54fb62', '208': '6233d594134459740d61511b7f3ee62f00a60ae2388c387957bf26736af406c3', '209': '3a47b881e3d34ff50f7ad32a38792702ac43e77a9aa9383b5433ceba6bc84859', '210': '6f155805eebeb105501cc90b1f27ff41e222d3413033bd952f010e9b4daa3c3a', '211': '46763c8e87cdec7f91f16a94c91342403a137bdfcf10a6397ea5e3c8dfc61c1e', '212': 'fef14022ff9875a4a6a9b609792ea7b005bedfaca3a4bc489925b0e0ea87a82a', '213': '6ef8b2bb13c92f6112753e380f98c48c4472b5a8d8db9695f8fc5cd73a9cbf44', '218': 'f79ff7838664c65a9a960fc9a05537aca47b7acb38e92c969f31e766f55af50a', '221': '95381a108bbe074058aacd9f91595bd3516016356cd0b38d6c8f6bfd34fe80c2', '223': '1036fb9ce58b602830b3dbd04ef902a09de8922f94671a2ba98a01e451919f3b', '228': '29dbab5b2ece11f0ab356048dddec4eb3004cd670669a248b530340a9ecaba96', '229': '9730d33141c80d8cfdc81e91e7bafe26b38f1a403591affd3ccc9c3e1b2dacbe', '233': '236194df68b0f343933e4b25e48bef4c80d2bbfba11006a87e9585687aae7ba3', '239': '8cbbebad974fe1b8e78cca0ec11c99b04d22dc0ef34a7282dac2b81721bc5918', '240': '894e9af9d73b50ed7208a6188c8fa7990be625dfe863b85945ff20c57ae85a65', '241': '43236045b17a96dc3b0a2fc34452c83b383a4b6aacc623d961ec8cdb7ebb6f60', '248': 'c722bdea14fa56c16772c7f070c15a40313f9afa91cf7f998176c7c93bd737c9', '249': '8c960b7a0da244e0efa39669c6e79ff5929ceabb8240c920cc9ede5cfa1ad468', '250': '73349e6eeedc8c0687d0df8258e5b4fc3affaabf3586f5fedbda1a618d1fb399', '289': '6718e4e058c39515f6c0a8d40b7ce86caf7c168c3c511eb01e1d2c22b6e54b4f', '295': '759d7300ca1b2e3539c96c7119b40eae99c77e6d7f4d23582fa890f9f3f2b3c0', '303': '4495fa6281a8f9f34fa3241fc8e4cdf540a62109090d0bbc324ffe7bdd0f677b', '304': 'fbc88aa3499f45d41bb440f5636d862a7aa2d49b34e3fcb76a5f8283d4f3a5aa', '313': '54e8c9a7575c279e4dd2c829c433ccfa4288ccb134fe77d8488563fb4477e3b6', '314': '00bed2e48a3c10dcce6f1db6dbac242567f56871c932915d12918c9df6ad9bd3', '30': '9cf0f5b23523777c69220fc109f59a6b42dc1550c90082e39b48748f53a03338', '31': 'd157a3547a4a9b336ce312fe2159e06efe4f46c61050cdb1d324082b4c6a8ecd', '56': 'f25d2afa78d77cf1b6141a08c5afe08318c20e33c00bd3005544e89cff7b6b44', '57': 'a7aad971c53c9aeba55c6a8d5957bae0c64010395a433063c3cf44a303bc133b', '292': 'd151202c5842be9171b84af9abf62aa6c5f2e0621c9ecc1091fa4312d984fbed', '293': 'c40ae37ee2223a2b35e626a7ec0b5c5f9b7ed10f70f6980e8c446c89d9df41df', '294': '0bf07b526efa465a4be3c22a10b85dcf364b763628c9cf73420f0a859c9b9f8b'}}, {'id': 'NBA2021_CAP', 'url': 'https://pr.nba.com/nba-salary-cap-for-2021-22-season-set-at-112-414-million/', 'classification': 'PRIMARY_NBA_RELEASE_BODY_DIRECT_READ', 'date': '2021-08-02', 'locator': 'cap112414000;tax136606000;NTMLE9536000;newcapyearAugust3'}, {'id': 'NBA2021_FA', 'url': 'https://www.nba.com/news/nba-announces-start-date-for-2021-free-agency', 'classification': 'PRIMARY_NBA_RELEASE_BODY_DIRECT_READ', 'date': '2021-04-19', 'locator': 'August6 12:01ET signing start'}, {'id': 'NBA2021_ROSTER_TW', 'url': 'https://pr.nba.com/nba-board-of-governors-play-in-roster-rules-2021-22-season/', 'classification': 'PRIMARY_NBA_RELEASE_BODY_DIRECT_READ', 'date': '2021-07-27', 'locator': 'STD15+TW2;flat50%0YOS;regularactive50'}]

CAP, APRON, NTMLE, BAE, MIN0 = 112414000, 143002000, 9536000, 3732000, 925258
CAMP_RESERVE = 4372601
STRETCH_SCREEN = 16371000  # .15 * highest named prior waiver-year cap,109140000.
CATEGORIES = [
    'preservedcontract_currentSalary/allperformance/assignmentcarry2021mapping',
    'newproposal_signing/performancebonuses_and_NTMLEaggregate',
    'legacy_dead_salary_or_resolved_grievancecarry',
    'other_named_FA/unsigned_draftrights_charge_before_renounce',
    'requiredtenders_and_Green/MarkQO_firstrefusalstates',
    'DPE/TPE/BAE_history_normalcharge_and_explicitunusedrightsclosure']


def text(p):
    return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')


def sha(p): return hashlib.sha256(text(p).encode()).hexdigest()
def load(p): return json.loads(text(p))


def fixed_inputs(reader=load, hasher=sha):
    assert set(PINS) == set(SOURCES)
    for p in SOURCES:
        assert hasher(p) == PINS[p], 'Unreviewed source change: '+p
    prior = reader(SQ)
    assert not sq.validate(prior), 'SQ1 producer reconstruction failed'
    assert prior['cost_boundary']['uncovered_finite_categories'] == CATEGORIES
    assert prior['summary']['working_signing_state_count'] == 10
    assert prior['summary']['named_cost_cases'] == 60
    public = reader(PUBLIC)
    assert public['whole_cost_pass'] and public['as_of'] == '2021-03-25 AFTER_ATOMIC_F1'
    assert public['arithmetic']['upper_usd'] == 132367326.15
    ledger = reader(LEDGER)
    assert ledger['body_reported_none_fields'] == ['TradeKickers','Expired10DayContracts',
        'QualifyingOffers','FreeAgentsWithCapHolds','UnsignedFirstRounders','NextCutDownNonGuaranteedSalaries']
    return prior, public, ledger


def implementation():
    return {
      'classification':'AUTHOR_MODELED_ROUTINE_LAWFUL_TERMS_WITHIN_ALREADY_SELECTED_M1_A',
      'new_contracts':{
        'Markkanen':{'first_year_regular_salary':17000000,'years':4,'annual_raise':1360000,
          'signing_performance_trade_promotional_loan_or_buyout_additions':0},
        'Caruso':{'first_year_Salary_plus_Unlikely':8600000,'years':4,
          'aggregate_NTMLE_limit':NTMLE,'proposed_regular_schedule':[8600000,9030000,9460000,9890000],'annual_raise':430000,'signing_performance_trade_promotional_loan_or_buyout_additions':0},
        **{n:{'first_year_minimum':v,'years':2,'all_bonuses':0,
              'later_minimum':'II6 applicable signing-year scale/credited YOS; automatic statutory adjustment'}
           for n,v in {'Green':1669178,'Joe Wieskamp':925258,'Tony Bradley':1789256,
                       'Stanley Johnson':2089448,'Denzel Valentine':1939350}.items()},
        'Chris Duarte':{'rookie_Salary_plus_Unlikely_ceiling':4373040,'new_bonus_additions':0}},
      'Ryan_Arcidiacono':'AUTHOR_MODELED_OPTION_NOT_EXERCISED_AND_NO_NEW_QO_BEFORE_NEW_CAP_YEAR; no waived future salary; Bird FA upper1.9*3m remains until renounce',
      'Dotson_Mokoka':'AUTHOR_MODELED_NO_NEW_QO_ISSUED; completed TW FA amounts kept until August11 renounce',
      'FirstRefusalExerciseNotices':'No new notice/offer-sheet transaction is selected in this implementation; actual private notices null',
      'Mark_Green_QO':'Preserve admissible QO uncertainty until each new contract; accepting QO is not selected',
      'new_chicago_trade_DPE_application_renegotiation_or_grievance_settlement':False,
      'actual_agreement_cents_receipt_consents':None,
      'new_exact_author_lock':False}


# Frozen at module load, before any constructor mutation. The separate legal
# guards below bind monetary inputs actually used by the prior600-state ledger.
FIXED_ROUTINE_POLICY=copy.deepcopy(implementation())


def checked_implementation():
    p=implementation()
    assert p==FIXED_ROUTINE_POLICY, 'Routine source policy differs from fixed selected public implementation'
    contracts=p['new_contracts']
    m,c=contracts['Markkanen'],contracts['Caruso']
    assert m['first_year_regular_salary']==17000000 and m['years']==4
    assert m['annual_raise']==1360000 and m['annual_raise']<=m['first_year_regular_salary']*.08
    assert m['signing_performance_trade_promotional_loan_or_buyout_additions']==0
    assert c['first_year_Salary_plus_Unlikely']==8600000 and c['years']==4
    assert c['aggregate_NTMLE_limit']==NTMLE and c['first_year_Salary_plus_Unlikely']<=NTMLE
    assert c['annual_raise']==430000 and c['annual_raise']<=c['first_year_Salary_plus_Unlikely']*.05
    assert c['proposed_regular_schedule']==[8600000,9030000,9460000,9890000]
    assert c['signing_performance_trade_promotional_loan_or_buyout_additions']==0
    for n,v in {'Green':1669178,'Joe Wieskamp':925258,'Tony Bradley':1789256,
                'Stanley Johnson':2089448,'Denzel Valentine':1939350}.items():
        x=contracts[n];assert x['first_year_minimum']==v and x['years']==2 and x['all_bonuses']==0
        assert x['later_minimum']=='II6 applicable signing-year scale/credited YOS; automatic statutory adjustment'
    assert contracts['Chris Duarte']=={'rookie_Salary_plus_Unlikely_ceiling':4373040,'new_bonus_additions':0}
    return p


def states_for(case, events, policy):
    assert policy == checked_implementation(), 'Routine finance/rights semantics changed'
    assert len(case['states']) == len(events) == 10
    rows=[]
    for i,(s,e) in enumerate(zip(case['states'],events)):
        assert s['event_id']==e['id'] and s['date']==e['date']
        signed=set(s['contract_players'])
        # Upper envelope: every reported Young performance dollar is reserved,
        # irrespective of the prior likely/unlikely sensitivity branch.
        young_delta=1000000-case['Young_existing_bonus_reference']
        assert young_delta in [0,1000000]
        # These expired named contracts were left outside the older partial sum.
        # VII4d5 caps Porter's FA amount; Arc option decline doesn't waive debt.
        extra_fa={} if i>=5 else {
           'Otto Porter Jr.':39344900,'Cristiano Felicio':14305138,
           'Garrett Temple':5720400,'Ryan Arcidiacono':5700000,
           'Adam Mokoka':MIN0,'Devon Dotson':MIN0}
        # Green's potential starter QO/FR amount cannot matter after early signing.
        # Before then use even the first-year 0-6YOS maximum as a broad hold bound.
        green_unsign=28103500 if 'Green' not in signed else 0
        old_holds=dict(s['retained_named_FA'])
        all_normal_holds={**old_holds,**extra_fa}
        if green_unsign: all_normal_holds['Green']=green_unsign
        unsigned=dict(s['unsigned_first_reference'])
        # Incomplete cap holds are recomputed using all counted FA identities.
        empty=max(0,12-len(signed)-len(all_normal_holds)-len(unsigned))
        exception_nominal=s['unused_NTMLE_nominal']+(BAE if i<5 else 0)
        normal_without_legacy=(s['known_normal_terms_including_incomplete']
            -s['incomplete_roster_usd']+young_delta+sum(extra_fa.values())
            +green_unsign+empty*MIN0+exception_nominal)
        tender_apron=4373040 if 'Chris Duarte' not in signed else 0
        green_apron=green_unsign  # safe even where QO/FA hold distinction narrows it
        apron_without_legacy=s['known_apron_reference_terms']+young_delta+tender_apron+green_apron
        # Exact source inventories are not a cash-zero certificate. Reserve all
        # named current-year camp cash, and screen future stretched totals broadly.
        reserved_legacy=CAMP_RESERVE+STRETCH_SCREEN
        screened_apron=apron_without_legacy+reserved_legacy
        allowance=APRON-screened_apron if s['hard_cap_triggered_in_working_family'] else None
        assert allowance is None or allowance>=0
        rows.append({'id':e['id'],'date':e['date'],'within_model_order':i,
          'standard_contract_count':len(signed),'signed_players':sorted(signed),
          'normal_FA_upper_by_player':all_normal_holds,'unsigned_first_upper':unsigned,
          'counted_incomplete_roster':empty,'incomplete_roster_usd':empty*MIN0,
          'normal_exception_nominal_upper':exception_nominal,
          'annual_unused_exception_upper_is_actual_charge':False,
          'reported_performance_added_to_prior_branch':young_delta,
          'required_first_round_tender_apron_upper':tender_apron,
          'second_round_rights_without_signed_UPC_apron_charge':0,
          'second_round_rights_retention_certified':False,
          'normal_upper_excluding_unresolved_legacy':normal_without_legacy,
          'apron_upper_excluding_unresolved_legacy':apron_without_legacy,
          'conservative_named_camp_and_future_stretch_screen':reserved_legacy,
          'screened_apron_before_additional_legacy':screened_apron,
          'hard_cap_triggered':s['hard_cap_triggered_in_working_family'],
          'additional_legacy_upper_required_for_apron':allowance,
          'normal_complete_upper':normal_without_legacy+reserved_legacy,'apron_complete_upper':screened_apron,
          'actual_private_salary_or_waiver':None,'whole_cost_pass':True})
    return rows


def legacy_bridge():
    # Source-correct contract-year endpoints, not waiver => payment zero.
    rows = [
      {'player':'Antonio Blakeney','start':'2018-19','last_ordinary_year':'2019-20','length_years':2,'source':COHORT},
      {'player':'Luol Deng','start':'2019-20','last_ordinary_year':'2019-20','term':'one-day Chicago retirement','source':COHORT},
      {'player':'Simisola Shittu','start':'2019-20','last_ordinary_year':'2019-20','length_years':1,'source':COHORT},
      {'player':'Justin Simon','start':'2019-20','last_ordinary_year':'2019-20','term':'Exhibit10/II3q one-season','source':'research/CHICAGO_SIMON_2019_CARRY_BOUNDARY_2026_10_05.json'},
      {'player':'Perrion Callandret','start':'2019-20','last_ordinary_year':'2019-20','term':'Exhibit10/II3q one-season','source':'LEGACY_TERM_CALLANDRET'},
      {'player':'Milton Doyle','start':'2019-20','last_ordinary_year':'2019-20','length_years':1,'source':'LEGACY_TERM_DOYLE'},
      {'player':'Shaquille Harrison oldCHI','start':'2018-19','last_ordinary_year':'2019-20','length_years':2,'source':MINIMUM},
      {'player':'Shaquille Harrison newCHI','start':'2019-20','last_ordinary_year':'2019-20','length_years':1,'source':'LEGACY_TERM_HARRISON'},
      {'player':'Walt Lemon Jr.','start':'2018-19','last_ordinary_year':'2019-20','length_years':2,'source':'LEGACY_TERM_LEMON'},
      {'player':'Omer Asik','start':'2015-16','last_ordinary_year':'2019-20','length_years':5,'source':'LEGACY_TERM_ASIK'},
      {'player':'Noah Vonleh','start':'2020-21','last_ordinary_year':'2020-21','length_years':1,'source':'noah-vonleh_CAMP2020_TERM'},
      {'player':'Zach Norvell Jr.','start':'2020-21','last_ordinary_year':'2020-21','term':'Exhibit9/II3p one-season','source':'BI_ORIGINAL'},
      {'player':'Simisola Shittu secondCHI','start':'2020-21','last_ordinary_year':'2020-21','term':'Exhibit9/II3p one-season','source':'BI_ORIGINAL'}]
    assert len(rows)==13 and len({r['player'] for r in rows})==13
    for r in rows:
        assert int(r['last_ordinary_year'][:4]) < 2021
        if 'length_years' in r:
            assert int(r['start'][:4])+r['length_years']-1==int(r['last_ordinary_year'][:4])
    return {'status':'SOURCE_SUPPORTED_NAMED_ENDPOINT_AND_PRESERVED_PUBLIC_CATEGORY_BRIDGE',
      'ordinary_contracts':rows,'ordinary_2021_future_component_upper':0,
      'ordinary_zero_is_actual_payment_zero':False,
      'preserved_inventory_source':PUBLIC,
      'positive_inventory':'Accepted fullMarch25 publiccategory model; originalBI WaivedPlayers three2020camp names and2021futurecolumn; named2019duration endpoints add yearmapping, not a raw13-salary partialsum',
      'all_named_camp_cash_and_resolution_reserved':CAMP_RESERVE,
      'all_valid_prior_future_stretch_annual_upper':STRETCH_SCREEN,
      'stretch_definition':'VII7d6 futurewaived/formerplayerSalary aggregate in anyfutureseason <=15% salarycap of stretch-waiver year; maximum namedpriorcap109140000',
      'new_settlement_or_grievance_resolution_selected':False,
      'arbitrary_unreported_new_future_resolution_required':False,
      'reported_prior_adjustments_kept_in_currentSalary':True,
      'actual_private_payments_settlements_and_hidden_clause_absence_certified':False,
      'new_identified_preserved_cost_or_changed_contract_reopens_family':True,
      'not_an_all_historical_private_ledger_certificate':True}


def checked_legacy_bridge():
    b=legacy_bridge()
    expected={
      'Antonio Blakeney':('2018-19','2019-20',COHORT),
      'Luol Deng':('2019-20','2019-20',COHORT),
      'Simisola Shittu':('2019-20','2019-20',COHORT),
      'Justin Simon':('2019-20','2019-20','research/CHICAGO_SIMON_2019_CARRY_BOUNDARY_2026_10_05.json'),
      'Perrion Callandret':('2019-20','2019-20','LEGACY_TERM_CALLANDRET'),
      'Milton Doyle':('2019-20','2019-20','LEGACY_TERM_DOYLE'),
      'Shaquille Harrison oldCHI':('2018-19','2019-20',MINIMUM),
      'Shaquille Harrison newCHI':('2019-20','2019-20','LEGACY_TERM_HARRISON'),
      'Walt Lemon Jr.':('2018-19','2019-20','LEGACY_TERM_LEMON'),
      'Omer Asik':('2015-16','2019-20','LEGACY_TERM_ASIK'),
      'Noah Vonleh':('2020-21','2020-21','noah-vonleh_CAMP2020_TERM'),
      'Zach Norvell Jr.':('2020-21','2020-21','BI_ORIGINAL'),
      'Simisola Shittu secondCHI':('2020-21','2020-21','BI_ORIGINAL')}
    rows=b['ordinary_contracts']
    assert len(rows)==13 and {r['player'] for r in rows}==set(expected)
    assert {r['player']:(r['start'],r['last_ordinary_year'],r['source']) for r in rows}==expected, 'Named legacy source endpoint changed'
    assert b['ordinary_2021_future_component_upper']==0 and not b['ordinary_zero_is_actual_payment_zero']
    assert b['all_named_camp_cash_and_resolution_reserved']==CAMP_RESERVE
    assert b['all_valid_prior_future_stretch_annual_upper']==STRETCH_SCREEN
    assert not b['new_settlement_or_grievance_resolution_selected']
    assert not b['actual_private_payments_settlements_and_hidden_clause_absence_certified']
    # Independent raw caches are optional for portable reproduction. Whenever
    # present their actual bytes and positive duration/classification are checked.
    phrases={
      'LEGACY_TERM_DOYLE':['Signed a one-year, $1.45 million contract with the Bulls in September of 2019'],
      'LEGACY_TERM_CALLANDRET':['Signed Perrion Callandret to an Exhibit 10 contract.'],
      'LEGACY_TERM_LEMON':['through 2020 with Chicago Bulls'],
      'LEGACY_TERM_ASIK':['five-year, $60 million contract with the New Orleans Pelicans'],
      'LEGACY_TERM_HARRISON':['Length : 1 year','Signing Date : July 18, 2019','2019-20']}
    obs={x['id']:x for x in RAW_OBSERVATIONS}
    for k,tokens in phrases.items():
        x=obs[k];assert x['http_status']==200 and x['original_body_verified']
        q=Path(x['cache_path'])
        if q.exists():
            raw=q.read_bytes();assert hashlib.sha256(raw).hexdigest()==x['raw_sha256']
            body=' '.join(html.unescape(re.sub('<[^>]+>',' ',raw.decode('utf8',errors='replace'))).split())
            for token in tokens: assert token in body, 'Positive term body not present: '+k
    return b


def category_map():
    return [
      {'id':CATEGORIES[0],'status':'SOURCE_SUPPORTED_PRESERVED_PUBLIC_CURRENT_SALARY_FAMILY',
       'basis':'six positive2021 contract Salary rows; currentSalary includes allocated signing/assignment bonus per VII3b/4a1; prior acquisition preserved, no new August assignment',
       'performance':'Full Young1m regardless likely/unlikely classification; rookies full120% Salary+Unlikely envelope; other preserved reported performance0',
       'historical_exact_financial_certified':False},
      {'id':CATEGORIES[1],'status':'CONSTRUCTED_ROUTINE_LEGAL_IMPLEMENTATION',
       'basis':'Minimum new contracts explicitly choose no bonus; II6f permits trade/Ex10 exceptions, not a universal all-bonus ban; Caruso total8.6m≤NTMLE9.536m; M1 guaranteed regular schedule/no added bonuses; new ordinary FA contracts separate from old six-month restriction'},
      {'id':CATEGORIES[2],'status':'INDEPENDENTLY_REVIEWED_SOURCE_SUPPORTED_FINITE_LEGACY_CATEGORY_BRIDGE',
       'ordinary2020camp_future_salary_upper':0,
       'ordinary_zero_basis':'Thirteen namedcontractyear endpoints below2021; no guarantee0 inference',
       'camp_cash_resolution_overreserve':CAMP_RESERVE,
       'prior_stretch_only_screen':STRETCH_SCREEN,
       'legacy_total_upper':CAMP_RESERVE+STRETCH_SCREEN,
       'stretch_screen_is_complete_legacy_bound':False,
       'unresolved_id':None,'source_scope':'Accepted publiccategory family with positive namedduration endpoint mapping and no new resolutionevent selected; actual hiddenledger not certified',
       'source_bridge':checked_legacy_bridge()},
      {'id':CATEGORIES[3],'status':'CLOSED_NAMED_PUBLIC_FAMILY_ALL_TEN_STATES',
       'expired':'Porter/Felicio/Temple/Arc/Mark/Theis/Valentine/Green plus completed Dotson/Mokoka TW',
       'rule':'VII4d5 FA maximum; VII4f counted players; VII4g renounce August11; no cap-room claim from high normal TeamSalary',
       'firsts':'Positive prior None inventory plus only workingCHI10 unsigned first; second round oldrights not firsts'},
      {'id':CATEGORIES[4],'status':'CONSTRUCTED_FINITE_QO_TENDER_AND_NOTICE_PATH',
       'Mark_QO_upper':9026952,'Green_pre_signing_broad_maximum':28103500,
       'Duarte_required_tender_upper':4373040,
       'basis':'Old QOs terminate upon direct contracts; new no FRNotice action; no new TW QO; unsigned first tender reserved before Duarte signing',
       'Simonovic_rights_window_closed':False,'actual_tender_or_notice_received':None},
      {'id':CATEGORIES[5],'status':'FULL_NOMINAL_NORMAL_EXCEPTION_ENVELOPE_AND_EXPLICIT_RENOUNCE',
       'normal_upper_before_use':NTMLE+BAE,'after_Caruso':936000+BAE,'after_Aug11':0,
       'basis':'VII6d4/e4 oldannual expiry; source-supported prior remaining TPE/DPE inventory preserved/no new grant/trade selected; VII6m2 explicit all-unused renounce August11',
       'apron_deemed_exception_charge':0,'apron_basis':'VII6m3F exclusion, not balance absence',
       'historical_TPE_DPE_never_existed':False}]


def build(reader=load,hasher=sha):
    prior,public,ledger=fixed_inputs(reader,hasher)
    policy=checked_implementation()
    cases=[{'protagonist_existing_family':c['protagonist_existing_model'],
            'prior_Young_sensitivity':c['Young_existing_bonus_reference'],
            'states':states_for(c,prior['working_events'],policy)}
           for c in prior['named_cost_family_cases']]
    remaining=min(r['additional_legacy_upper_required_for_apron'] for c in cases
                  for r in c['states'] if r['hard_cap_triggered'])
    assert remaining==14087225
    assert len(cases)==60 and sum(len(c['states']) for c in cases)==600
    return {'id':'CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07',
      'status':'SIX_CATEGORIES_SOURCE_SUPPORTED_PUBLIC_COST_EXECUTION_INDEPENDENTLY_REVIEWED_PASS',
      'source_sha256':{p:hasher(p) for p in SOURCES+[SELF]},
      'hash_convention':'UTF8_BOM_STRIPPED_CRLF_CR_NORMALIZED_LF',
      'raw_body_observations':RAW_OBSERVATIONS,'primary_rule_observations':RULE_OBSERVATIONS,
      'failed_term_recovery_attempts':FAILED_TERM_RECOVERIES,
      'quantifier':{'external_preserved_public_contract_inputs':'all admitted original contract/rate/bonus families',
        'routine_new_implementation':'exists proposed lawful terms/order/renounce path',
        'all_arbitrary_hidden_private_contract_clauses_required':False,
        'actual_cash_receipts_agreements_certified':False},
      'routine_implementation':policy,'categories':category_map(),'cases':cases,
      'summary':{'categories':6,'bounded_or_constructed_categories':6,
        'unresolved_source_categories':0,'dated_states':10,'cases':60,'case_states':600,
        'named_final_annual_upper':108171174,
        'camp_full_cash_reservation':CAMP_RESERVE,'prior_stretch_only_screen':STRETCH_SCREEN,
        'conditional_final_upper_before_additional_legacy':128914775,
        'additional_legacy_upper_needed_usd':None,'remaining_apron_margin_usd':remaining,
        'complete_normal_upper':max(r['normal_complete_upper'] for c in cases for r in c['states']),
        'complete_apron_upper':max(r['apron_complete_upper'] for c in cases for r in c['states'] if r['hard_cap_triggered']),'whole_cost_pass_count':600},
      'legacy_remaining':{'id':None,'aggregate_upper_usd':CAMP_RESERVE+STRETCH_SCREEN,
        'additional_ordinary_future_upper_usd':0,'unknown_selected_zero':False,
        'named_endpoint_bridge':checked_legacy_bridge(),'not_an_infinite_private_ledger_requirement':True,
        'actual_legacy_payment_is_zero_certified':False},
      'six_month_boundary':prior['six_month_descendant_boundary'],
      'full60_draft_execution_closed':False,'Simonovic_rights_window_closed':False,
      'whole_source_supported_cost_family_pass':True,
      'macro3_complete':False,'new_REGISTER_promotion':False,
      'independent_review_completed':True,'season_selected':False,
      'independent_review_scope':{'reviewer':'/root/den_pick_full_branch',
        'actual_case_state_recalculations':600,'repo_source_pins_checked':14,
        'new_HTML_bodies_read':13,'reused_BI_bodies_read':2,
        'original_policy_constructor_defects_rejected_after_repair':['Green added bonus','Caruso future schedule reversal'],
        'root_CBA_raw_and_PDF249_250_read':True,
        'actual_private_or_macro3_certification':False},
      'design_gate':'CLOSED','manuscript_allowed':False}


def validate(d):
    try: return [] if d==build() else ['Output differs from exact source reconstruction']
    except (AssertionError,KeyError,ValueError) as e: return [str(e)]


def markdown(d):
    rows=['# Chicago 2021 A — 6범주·10단계 전체 비용 family',
      '',d['status'],'',
      '승인된 M1/A 아래의 가상 합법 루틴 구현이다. 실제 계약·수락·접수 인증은 아니다. 60개 기존 급여 family × 10단계 = 600개를 계산하고 원문·의미·별도 산술 검문 뒤 공개 보존 family 전체 비용 PASS600으로 수용했다.',
      '', '| 범주 | 판정 |','|---|---|']
    rows += [f'| {c["id"]} | {c["status"]} |' for c in d['categories']]
    rows += ['', '## 비용과 남은 단일 범주','',
      '최종 명명 계약·전 performance 상단 $108,171,174. 2020 캠프 현금 전액 $4,372,601 및 유효 과거 stretch 전체 연간 상한 $16,371,000을 더한 공개 보존 family 상단은 $128,914,775, apron 여유 $14,087,225이다. 명명된 13계약의 ordinary 연도 끝점을 2021 이전으로 연결했다. 실제 미공표 지급·합의 0의 인증은 아니며 신규 발견 보존 비용/새 사건은 family를 다시 검문한다. 별도 담당의 600상태 재계산·원문 직접 대조와 정책 변조 반례 수리 뒤 이 한정 가족의 전체 비용을 수용했다.',
      '', 'Norvell/Shittu의 원 BI Exhibit9 계약은 II3(p)에 따라 한 시즌이며 Vonleh는 새 직접 계약표의 1년 행을 확인했다. 보장 0이나 방출 자체로 비용 0을 추론하지 않는다. 과거 미공표 장부 전체나 실제 리그 접수는 새 필수조건이 아니다. 허용된 공개 경제 family의 연도별 category mapping을 아래 끝점으로 구성했다.',
      '', '## 상태 경계','',
      '7개 계속 계약의 CurrentSalary는 공개 Salary 입력점으로 연결한다. 기존 취득의 할당 보너스는 같은 CurrentSalary에 두 번 더하지 않는다. Young $1m 전 performance는 likely/unlikely에 관계없이 예약한다. 새 M1/Caruso는 추가 보너스·대여·매입 없는 루틴 제안, Caruso $8.6m≤NTMLE $9.536m; 최소계약은 이번 제안에서 보너스 없이 구성했다. II6(f)는 trade/Exhibit10 예외를 허용하므로 모든 최소계약의 법적 보너스 금지로 일반화하지 않는다.',
      '', '이전 부분합에서 빠졌던 Porter/Felicio/Temple/Arc 및 완료된 TW 두 명의 FA 보류액도 넣었다. Green은 조기 서명 전 넓은 최대급여 화면을 쓰고 이후 QO/보류를 제거한다. 모든 unsigned first/tender·미달 차지 및 nominal NTMLE/BAE를 서로 다른 normal/apron 정의로 계산했다. 모든 미사용 예외와 불필요 권리는 8/11 명시 포기한다. 높은 normal TeamSalary를 불법 지출로 오인하지 않는다.',
      '', 'Wieskamp는 독점 지명권을 가진 Draft Rookie여서 I1(cc)의 Free Agent와 다르다. 0YOS FA의 apron floor를 자동 이식하지 않는다. Simonović의 무서명 2R 권리는 Salary가 아니지만 2021 권리 존속 자체는 이 비용 파일에서 완료하지 않는다.',
      '', '8/12 뒤 새 거래·새 분쟁·추가 명단 계약은 이 10단계 family에 포함되지 않는다. 기존 F1 면제 후 원 계약 연장·재협상은 max(9/25,원래 가능일) 이후이며, 만료 뒤 새 FA 계약은 원 계약 연장과 자동 등치하지 않는다.',
      '', '## 계약 기간 끝점','', '| 계약 | 시작 | 마지막 ordinary 연도 | 근거 |', '|---|---|---|---|']
    rows += [f'| {r["player"]} | {r["start"]} | {r["last_ordinary_year"]} | {r["source"]} |' for r in checked_legacy_bridge()['ordinary_contracts']]
    rows += ['', '새 미보고2021분쟁/해결은 선택되지 않았다. 기존 공개 inventory의 보고된 조정은 CurrentSalary에 보존한다. 이 가족은 임의 미래 소송·합의를 무한 추가한 모든 현실 장부의 가족이 아니다. ordinary 연도 종료와 stretch 연간 상단, 캠프 전액 예약은 서로 다른 증명이다.', '', '## 출처·검문','']
    rows += [f'- [{x["id"]}]({x["url"]}): {x["locator"]}; {x.get("classification","PRIMARY_CBA")}' for x in d['raw_body_observations']+d['primary_rule_observations']]
    rows += ['', '원문은 실제 읽은 범위만 기록한다. 최신 vendor 계약표는 역사 원장/작가 확정이 아니며, March25 공개 wholecost는 그 날짜 증인으로 보존한다. 새 연도 법적 입력 family의 상한 후보만 구성하며 실제 리그 원장은 인증하지 않는다. 전체 macro3·시즌·원고·REGISTER 승격 false.']
    return '\n'.join(rows)+'\n'


def self_test():
    d=build(); n=0
    changes=[lambda x:x['summary'].__setitem__('complete_apron_upper',128914774),
      lambda x:x.__setitem__('macro3_complete',True),
      lambda x:x['legacy_remaining'].__setitem__('aggregate_upper_usd',0),
      lambda x:x['categories'][2].__setitem__('stretch_screen_is_complete_legacy_bound',True),
      lambda x:x['cases'][0]['states'][0]['normal_FA_upper_by_player'].pop('Otto Porter Jr.'),
      lambda x:x['cases'][0]['states'][3].__setitem__('normal_exception_nominal_upper',0),
      lambda x:x['routine_implementation']['new_contracts']['Green'].__setitem__('all_bonuses',1),
      lambda x:x.__setitem__('Simonovic_rights_window_closed',True)]
    for change in changes:
        x=copy.deepcopy(d);change(x);assert validate(x);n+=1
    p=implementation();p['new_contracts']['Caruso']['first_year_Salary_plus_Unlikely']=9536001
    try: states_for(load(SQ)['named_cost_family_cases'][0],load(SQ)['working_events'],p)
    except AssertionError: n+=1
    else: raise AssertionError('NTMLE illegal routine accepted')
    for mutate in [lambda x:x['ordinary_contracts'][4].__setitem__('last_ordinary_year','2021-22'),
                   lambda x:x['ordinary_contracts'].pop(5)]:
        x=legacy_bridge();mutate(x)
        with patch(__name__+'.legacy_bridge',return_value=x):
            try: build()
            except AssertionError: n+=1
            else: raise AssertionError('Invalid named legacy endpoint accepted')
    for mutate in [lambda x:x['new_contracts']['Green'].__setitem__('all_bonuses',100000),
                   lambda x:x['new_contracts']['Caruso'].__setitem__('proposed_regular_schedule',[8600000,100000000,100000000,100000000])]:
        x=implementation();mutate(x)
        with patch(__name__+'.implementation',return_value=x):
            try: build()
            except AssertionError: n+=1
            else: raise AssertionError('Routine financial constructor mutation accepted')
    return n


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args()
    d=build();md=markdown(d)
    if a.write:
        (ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(md,encoding='utf8')
    current=(ROOT/OUT).exists() and load(OUT)==d and text(MD)==md
    if a.check: assert current,'Saved source/output stale'
    print(json.dumps({'current':current,'categories':6,'bounded_or_constructed':6,'legacy_gap':0,
        'case_states':600,'remaining_apron_margin':d['summary']['remaining_apron_margin_usd'],
        'whole_source_supported_cost_family_pass':d['whole_source_supported_cost_family_pass'],
        'macro3_complete':d['macro3_complete'],'negative_controls':self_test() if a.self_test else None}))


if __name__=='__main__': main()
