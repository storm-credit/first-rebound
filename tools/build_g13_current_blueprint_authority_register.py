"""Reference-only current verification-Blueprint authority register.
Local peer qualification does not rewrite parent pending flags or open G13/Packs.
"""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
OUT = "control/G13_CURRENT_BLUEPRINT_AUTHORITY_REGISTER_2026_10_08.json"
REG = "control/G13_A14_FUNCTION_EXECUTION_REGISTER_2026_10_08.json"
REG_KEYS = ["id","path","record_pointer","order","planned_slot","act","subact","exact_entry","exact_exit"]
REVIEWS = ['reviews/A01_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json', 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json', 'reviews/A06_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json', 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json', 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json']
BUNDLES = ['design/A01_REMAINING_VERIFIED_BLUEPRINT_BUNDLE_2026_10_08.json', 'design/A06_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json', 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json', 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json']
PINS = {'reviews/A01_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json': 'e22158cc3859c7e16f302f4b7df8cd7dbe3c3bd35be01b1fbab9737f8bed4bb3',
 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json': '5489540b09a2959452b2e677406cef3e9b10e6c66ce2f3f58d2d8766dc2b05c9',
 'reviews/A06_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json': 'c32ae5e1921a872caf240498d131647f19690fe7d0edfe059edd054548e49cbf',
 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json': 'bd19a355d55b4a1f3669f3f0c948469a989e4dd194c1be71fe388cdb361d6fc6',
 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json': '7a2c4b3c47f8eed4439eb83f35cc0cf44b9ab1b7c7a83fb185892feb1edca1f1',
 'design/A01_REMAINING_VERIFIED_BLUEPRINT_BUNDLE_2026_10_08.json': '36b48ef73b91a477d5caf547f010c1c4ada7ac7deac6b5f9de9abc498f90c439',
 'design/A06_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json': '80ae9cd6dccdac4fbd820f08fd89863018d444548f5eac861d2fe6bc92894a53',
 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json': '3f9df0820e40c927c69b840a05c5163162c214b59558a915b0da0051513cfba8',
 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json': 'eb06cd19e9f30d4b5927f65251b9c9ef2398a7417c657dd19706400e94c9071b',
 'tools/build_a01_remaining_verified_blueprint_bundle.py': '9f7a46f219542a27aa45c5e41e0638a179102cb33ee2a45994114fef1e608170',
 'design/A01_REMAINING_VERIFIED_BLUEPRINT_BUNDLE_2026_10_08.md': 'a2d9051550731d3559f0488ff49b1623da6cf22ece5e1215c1bd92aedae405be',
 'tools/build_a06_local_blueprint_bundle.py': '28d7e13f05e41753b3e4ecb69a750114965174f49db44deb8a91fc80b5bc8a2d',
 'design/A06_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.md': '72da6e4f8c13c0fc5e852db8b9e4846d42fcdd050ae2212acc126180f783d491',
 'design/G13_VERIFIED_BLUEPRINT_FINITE_BUILD_QUEUE_2026_10_08.json': '2a318281c77158687ced14a5cf6ad5c07243079189b2631a3f5db048279af84d',
 'design/G13_VERIFIED_BLUEPRINT_FINITE_BUILD_QUEUE_2026_10_08.md': '041146239750eed90a8b85e069fcb99f6e34a6e60ea271c89d449d8039e62369',
 'tools/build_a06_a09_remaining_blueprint_bundle.py': '8fee93ceb8e6f7eaafb1d6dd66d13adaaefc7f3f7da2d41f0d00e98a49cd58a8',
 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.md': '008db4849c373280cd12f9f1d3a9e0ab927cec9b682086328fe8d25e130c4991',
 'tools/build_a10_a14_local_blueprint_bundle.py': '5b2147524832c0fe95ce23406c65f62fd66718f8defd6aeabaebd4379087d94f',
 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.md': 'fd84a8f871d09a0777138e25e20db7bd363066f44ec57eef989e380ba79e35ef'}
LOCATORS = {'A01-EF-001': {'blueprint_path': 'design/A01_OPENING_BLUEPRINT.json',
                'pointer': '/',
                'review': 'reviews/A01_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/checks',
                'kind': 'EXISTING_BLUEPRINT_REFERENCE'},
 'A01-EF-002': {'blueprint_path': 'design/A01_FIRST_TRIAL_BLUEPRINT.json',
                'pointer': '/',
                'review': 'reviews/A01_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/checks',
                'kind': 'EXISTING_BLUEPRINT_REFERENCE'},
 'A01-EF-003': {'blueprint_path': 'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json',
                'pointer': '/',
                'review': 'reviews/A01_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/checks',
                'kind': 'EXISTING_BLUEPRINT_REFERENCE'},
 'A01-EF-004': {'blueprint_path': 'design/A01_E4_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A01_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/checks',
                'kind': 'EXISTING_BLUEPRINT_REFERENCE'},
 'A01-EF-005': {'blueprint_path': 'design/A01_E5_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A01_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/checks',
                'kind': 'EXISTING_BLUEPRINT_REFERENCE'},
 'A01-EF-006': {'blueprint_path': 'design/A01_E6_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A01_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/checks',
                'kind': 'EXISTING_BLUEPRINT_REFERENCE'},
 'A01-EF-007': {'blueprint_path': 'design/A01_E7_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A01_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/checks',
                'kind': 'EXISTING_BLUEPRINT_REFERENCE'},
 'A01-EF-008': {'blueprint_path': 'design/A01_E8_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A01_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/checks',
                'kind': 'EXISTING_BLUEPRINT_REFERENCE'},
 'A01-EF-009': {'blueprint_path': 'design/A01_E9_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A01_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/checks',
                'kind': 'EXISTING_BLUEPRINT_REFERENCE'},
 'A02-EF-001': {'blueprint_path': 'design/A02_E1_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/0',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A02-EF-002': {'blueprint_path': 'design/A02_E2_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/1',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A02-EF-003': {'blueprint_path': 'design/A02_E3_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/2',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A02-EF-004': {'blueprint_path': 'design/A02_E4_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/3',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A02-EF-005': {'blueprint_path': 'design/A02_E5_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/4',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A02-EF-006': {'blueprint_path': 'design/A02_E6_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/5',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A02-EF-007': {'blueprint_path': 'design/A02_E7_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/6',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A02-EF-008': {'blueprint_path': 'design/A02_E8_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/7',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A02-EF-009': {'blueprint_path': 'design/A02_E9_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/8',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A02-EF-010': {'blueprint_path': 'design/A02_E10_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/9',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A03-EF-001': {'blueprint_path': 'design/A03_E1_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/10',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A03-EF-002': {'blueprint_path': 'design/A03_E2_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/11',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A03-EF-003': {'blueprint_path': 'design/A03_E3_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/12',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A04-EF-001': {'blueprint_path': 'design/A04_E1_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/13',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A04-EF-002': {'blueprint_path': 'design/A04_E2_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/14',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A04-EF-003': {'blueprint_path': 'design/A04_E3_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/15',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A04-EF-004': {'blueprint_path': 'design/A04_E4_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/16',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A04-EF-005': {'blueprint_path': 'design/A04_E5_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/17',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A05-EF-001': {'blueprint_path': 'design/A05_E1_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/18',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A05-EF-002': {'blueprint_path': 'design/A05_E2_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/19',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A05-EF-003': {'blueprint_path': 'design/A05_E3_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/20',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A05-EF-004': {'blueprint_path': 'design/A05_E4_FINAL_EPISODE_FUNCTION.json',
                'pointer': '/local_blueprint',
                'review': 'reviews/A02_A05_EMBEDDED_BLUEPRINT_CURRENT_CORE_CHI_REVIEW_2026_10_08.json',
                'review_pointer': '/function_reviews/21',
                'kind': 'EXISTING_EMBEDDED_REFERENCE'},
 'A06-EF-001': {'blueprint_path': 'design/A06_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/',
                'review': 'reviews/A06_BLUEPRINT_BUNDLE_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/checks',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A06-EF-002': {'blueprint_path': 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/0',
                'review': 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/0',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A06-EF-003': {'blueprint_path': 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/1',
                'review': 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/1',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A06-EF-004': {'blueprint_path': 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/2',
                'review': 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/2',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A06-EF-005': {'blueprint_path': 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/3',
                'review': 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/3',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A07-EF-001': {'blueprint_path': 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/4',
                'review': 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/4',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A07-EF-002': {'blueprint_path': 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/5',
                'review': 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/5',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A07-EF-003': {'blueprint_path': 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/6',
                'review': 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/6',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A08-EF-001': {'blueprint_path': 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/7',
                'review': 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/7',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A08-EF-002': {'blueprint_path': 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/8',
                'review': 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/8',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A08-EF-003': {'blueprint_path': 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/9',
                'review': 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/9',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A09-EF-001': {'blueprint_path': 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/10',
                'review': 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/10',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A09-EF-002': {'blueprint_path': 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/11',
                'review': 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/11',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A09-EF-003': {'blueprint_path': 'design/A06_A09_REMAINING_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/12',
                'review': 'reviews/A06_A09_REMAINING_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/12',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A10-EF-001': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/0',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/0',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A10-EF-002': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/1',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/1',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A10-EF-003': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/2',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/2',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A11-EF-001': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/3',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/3',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A11-EF-002': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/4',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/4',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A11-EF-003': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/5',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/5',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A12-EF-001': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/6',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/6',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A12-EF-002': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/7',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/7',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A12-EF-003': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/8',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/8',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A13-EF-001': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/9',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/9',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A13-EF-002': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/10',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/10',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A13-EF-003': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/11',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/11',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A14-EF-001': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/12',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/12',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A14-EF-002': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/13',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/13',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'},
 'A14-EF-003': {'blueprint_path': 'design/A10_A14_LOCAL_BLUEPRINT_BUNDLE_2026_10_08.json',
                'pointer': '/records/14',
                'review': 'reviews/A10_A14_LOCAL_BLUEPRINT_ROOT_INDEPENDENT_REVIEW_2026_10_08.json',
                'review_pointer': '/verified_source_records/14',
                'kind': 'NEW_LOCAL_BLUEPRINT_REFERENCE'}}
REGISTER_CORE_SHA = 'd6bbe165a376f081471aceec76f44a0df930a38eab5cfc4435f6c6b508d1412c'

REGISTER_LOCATOR_SNAPSHOT = {'commit': '1953b41782dd4ae7367746011a2f803e67c9dee2',
 'sha256': 'a3ad1c502d0112b07a9b34579b78afa25641305ea660de0af22f5a5ae5d0b990',
 'historical_lines': {'A01-EF-001': 133,
                      'A01-EF-002': 143,
                      'A01-EF-003': 153,
                      'A01-EF-004': 163,
                      'A01-EF-005': 173,
                      'A01-EF-006': 183,
                      'A01-EF-007': 193,
                      'A01-EF-008': 203,
                      'A01-EF-009': 213,
                      'A02-EF-001': 223,
                      'A02-EF-002': 233,
                      'A02-EF-003': 243,
                      'A02-EF-004': 253,
                      'A02-EF-005': 263,
                      'A02-EF-006': 273,
                      'A02-EF-007': 283,
                      'A02-EF-008': 293,
                      'A02-EF-009': 303,
                      'A02-EF-010': 313,
                      'A03-EF-001': 323,
                      'A03-EF-002': 333,
                      'A03-EF-003': 343,
                      'A04-EF-001': 353,
                      'A04-EF-002': 363,
                      'A04-EF-003': 373,
                      'A04-EF-004': 383,
                      'A04-EF-005': 393,
                      'A05-EF-001': 403,
                      'A05-EF-002': 413,
                      'A05-EF-003': 423,
                      'A05-EF-004': 433,
                      'A06-EF-001': 443,
                      'A06-EF-002': 454,
                      'A06-EF-003': 465,
                      'A06-EF-004': 476,
                      'A06-EF-005': 487,
                      'A07-EF-001': 498,
                      'A07-EF-002': 509,
                      'A07-EF-003': 520,
                      'A08-EF-001': 531,
                      'A08-EF-002': 542,
                      'A08-EF-003': 553,
                      'A09-EF-001': 564,
                      'A09-EF-002': 574,
                      'A09-EF-003': 586,
                      'A10-EF-001': 598,
                      'A10-EF-002': 610,
                      'A10-EF-003': 622,
                      'A11-EF-001': 634,
                      'A11-EF-002': 645,
                      'A11-EF-003': 659,
                      'A12-EF-001': 673,
                      'A12-EF-002': 687,
                      'A12-EF-003': 701,
                      'A13-EF-001': 715,
                      'A13-EF-002': 729,
                      'A13-EF-003': 743,
                      'A14-EF-001': 757,
                      'A14-EF-002': 771,
                      'A14-EF-003': 785},
 'line_numbers_are_snapshot_locators_not_currentness_gates': True}

def text(p):
    return (ROOT / p).read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
def sha(p):
    return hashlib.sha256(text(p).encode()).hexdigest()
def meaning(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
def read(p):
    return json.loads(text(p))
def at(v, ptr):
    if ptr in ("", "/"): return v
    for k in ptr.strip("/").split("/"):
        k=k.replace("~1","/").replace("~0","~")
        v=v[int(k)] if isinstance(v,list) else v[k]
    return v
def core(reg):
    return [{k:r.get(k) for k in REG_KEYS} for r in reg["functions"]]
def module(name):
    name="authority_upstream_"+name
    file=ROOT/"tools"/(name.removeprefix("authority_upstream_")+".py")
    spec=importlib.util.spec_from_file_location(name,file)
    m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m)
    return m

def sources():
    for p,h in PINS.items(): assert sha(p)==h, "Accepted evidence physical source changed: "+p
    s={p:read(p) for p in PINS if p.endswith(".json")}
    s[REG]=read(REG)
    return s

def check_embedded_review(rv, reg):
    assert rv["status"]=="INDEPENDENT_CURRENT_CORE_MATCH_EXISTING_22_EMBEDDED_BLUEPRINTS"
    assert rv["summary"]["current_core_conflicts"]==0
    scoped=[r for r in reg["functions"] if r["act"] in ["A02","A03","A04","A05"]]
    assert meaning(scoped)==rv["register"]["current_A02_A05_projection_sha256"]
    for f in rv["source_fingerprints"]:
        if f["complete_fingerprint_unchanged"]:
            assert sha(f["path"])==f["current_complete_sha256"], "Embedded source changed: "+f["path"]
    for p,snap in rv["historical_full_file_vs_current_core"].items():
        old=subprocess.check_output(["git","show",snap["historical_commit"]+":"+p],cwd=ROOT).decode("utf-8-sig").replace("\r\n","\n").replace("\r","\n")
        assert hashlib.sha256(old.encode()).hexdigest()==snap["historical_full_file_sha256"]
        def sections(t):
            hs=list(re.finditer(r"^## .+$",t,re.M))
            return {m.group():t[m.start():hs[i+1].start() if i+1<len(hs) else len(t)].strip() for i,m in enumerate(hs)}
        a,b=sections(old),sections(text(p))
        for k,h in snap["current_consumed_anchors_sha256"].items():
            assert meaning(a[k])==h==meaning(b[k]), "Current consumed Canon anchor changed: "+p+"/"+k
    for r in rv["function_reviews"]:
        assert sha(r["function_path"])==r["current_function_sha256"]
        d=read(r["function_path"]);assert meaning(d["local_blueprint"])==r["current_blueprint_semantic_sha256"]
        assert all(r["checks"].values()) and r["original_blueprint_status"]=="ACTUAL_VERIFIED"
        for cl in r["claims"]:
            assert sha(cl["source_path"])==cl["current_source_sha256"]
            for ptr,h in cl["current_source_anchors_sha256"].items():
                assert meaning(at(read(cl["source_path"]),ptr))==h

def check_sources(s):
    historical=subprocess.check_output(["git","show",REGISTER_LOCATOR_SNAPSHOT["commit"]+":"+REG],cwd=ROOT).decode("utf-8-sig").replace("\r\n","\n").replace("\r","\n")
    assert hashlib.sha256(historical.encode()).hexdigest()==REGISTER_LOCATOR_SNAPSHOT["sha256"]
    for p,v in s.items(): assert v==read(p), "In-memory source differs from physical evidence: "+p
    reg=s[REG];assert meaning(core(reg))==REGISTER_CORE_SHA, "Current named 60-function core changed"
    assert len(reg["functions"])==60 and {r["order"] for r in reg["functions"]}==set(range(1,61))
    assert len({r["subact"] for r in reg["functions"]})==42
    assert {r["id"] for r in reg["functions"]}==set(LOCATORS)
    for p in [REVIEWS[0],REVIEWS[2],REVIEWS[3],REVIEWS[4]]:
        rv=s[p];assert rv["independent_review_completed"] is True
        assert rv["qualified_blueprint_status"]=="ACTUAL_VERIFIED"
        for sp,h in rv["source_sha256"].items(): assert sha(sp)==h
    check_embedded_review(s[REVIEWS[1]],reg)
    # Source-specific scopes and committed snapshots, not central progress whole-hash repins.
    m=module("build_a01_remaining_verified_blueprint_bundle");assert not m.validate(s[BUNDLES[0]])
    m=module("build_a06_local_blueprint_bundle");assert not m.validate(s[BUNDLES[1]],read(m.QUEUE))
    m=module("build_a06_a09_remaining_blueprint_bundle")
    assert m.build(m.load_sources(),s[BUNDLES[2]]["revision"]["historical_full_file_snapshot"])==s[BUNDLES[2]]
    m=module("build_a10_a14_local_blueprint_bundle")
    assert m.build(m.sources(),s[BUNDLES[3]]["information_and_revision"]["historical_full_file_snapshot"])==s[BUNDLES[3]]
    return True

def provenance(s,r):
    lc=LOCATORS[r["id"]];bp=s.get(lc["blueprint_path"]) or read(lc["blueprint_path"])
    v=at(bp,lc["pointer"]);rv=s[lc["review"]]
    return lc,bp,v,rv

def generation(bp,v):
    return {"parent_status":bp.get("status"),"record_status":v.get("status"),
        "parent_independent_review_completed":bp.get("independent_review_completed"),
        "parent_this_blueprint_independent_review_completed":bp.get("this_blueprint_independent_review_completed"),
        "record_ACTUAL_VERIFIED_promoted_by_writer":v.get("ACTUAL_VERIFIED_promoted_by_writer")}

def register_line(fid):
    return REGISTER_LOCATOR_SNAPSHOT["historical_lines"][fid]

def construct(s):
    rows=[]
    for i,r in enumerate(s[REG]["functions"]):
        lc,bp,v,rv=provenance(s,r)
        rows.append({"function_id":r["id"],"order":r["order"],"subact":r["subact"],
            "current_register":{"path":REG,"json_pointer":"/functions/"+str(i),"line_at_read_snapshot":register_line(r["id"]),"relevant_core_sha256":meaning({k:r.get(k) for k in REG_KEYS})},
            "selected_function":{"path":r["path"],"json_pointer":r.get("record_pointer") or "/","current_source_sha256":sha(r["path"])},
            "blueprint":{"path":lc["blueprint_path"],"json_pointer":lc["pointer"],"current_source_sha256":sha(lc["blueprint_path"]),"record_semantic_sha256":meaning(v),"reference_kind":lc["kind"]},
            "qualified_status":"ACTUAL_VERIFIED",
            "qualification":{"review_path":lc["review"],"json_pointer":lc["review_pointer"],"current_review_sha256":PINS[lc["review"]],"scope":rv.get("qualified_scope",rv["scope"] if "scope" in rv else "CURRENT_EXISTING_EMBEDDED_CANON_CORE_AND_INFORMATION_ACCESS")},
            "original_generation_flags_preserved":generation(bp,v),
            "individual_scene_pov_verified":False,"scope":"CURRENT_SOURCE_PATH_REVISION_CORE_AND_INFORMATION_ACCESS_FOR_EXISTING_LOCAL_FUNCTION_ONLY",
            "Blueprint_source_referenceable_under_scope":True,"actual_Pack_compilation_authorized":False})
    add=s[BUNDLES[0]]["remaining_blueprints"][0]
    return {"schema":"G13_CURRENT_BLUEPRINT_AUTHORITY_REGISTER_V1","status":"CURRENT_60_LOCAL_BLUEPRINT_AUTHORITIES_REFERENCE_ONLY_PENDING_REGISTER_PEER",
        "source_sha256":{**PINS,"tools/build_g13_current_blueprint_authority_register.py":sha("tools/build_g13_current_blueprint_authority_register.py")},
        "current_function_register_scope_sha256":REGISTER_CORE_SHA,"historical_register_line_snapshot":REGISTER_LOCATOR_SNAPSHOT,"function_authorities":rows,
        "same_trial_W_supplement":{"function_id":"A01-EF-002","blueprint_path":BUNDLES[0],"json_pointer":"/remaining_blueprints/0","semantic_sha256":meaning(add),"qualified_status":"ACTUAL_VERIFIED","qualifying_review":REVIEWS[0],"review_sha256":PINS[REVIEWS[0]],"original_generation_status_preserved":add["status"],"new_function_or_event":False},
        "counts":{"qualified_functions":len(rows),"function_orders":60,"covered_subacts":42,"existing_blueprint_references":31,"new_local_blueprint_references":29,"same_trial_supplements":1,"blueprint_bodies_copied":0,"new_events_functions_or_dialogue":0},
        "exception_report":[],"currentness_policy":"Immutable evidence/review pins plus each producer's relevant current Canon/register projection. Historical complete SHA/commits remain in the referenced accepted sources. Unrelated central progress appends are not new currentness gates.",
        "scope_limits":{"register_independent_review_completed":False,"parent_pending_flags_rewritten":False,"individual_scene_POV_lock_certified":False,"whole_Act_history_or_G13_complete":False,"final_published_allocation_locked":False,"whole_g14_complete":False,"actual_context_packs":0,"manuscript_allowed":False,"new_author_lock":False,"design_gate":"CLOSED","freeze":"v0.30 PARTIAL"},
        "next_dependency":"Whole Act/historical exits and final publication allocation remain prerequisites to actual Context Pack compilation; local Blueprint qualification alone does not open them."}

def assert_output(o,s):
    assert o["source_sha256"]=={**PINS,"tools/build_g13_current_blueprint_authority_register.py":sha("tools/build_g13_current_blueprint_authority_register.py")}
    assert o["current_function_register_scope_sha256"]==REGISTER_CORE_SHA
    assert o["historical_register_line_snapshot"]==REGISTER_LOCATOR_SNAPSHOT
    assert o["status"]=="CURRENT_60_LOCAL_BLUEPRINT_AUTHORITIES_REFERENCE_ONLY_PENDING_REGISTER_PEER"
    assert o["counts"]=={"qualified_functions":60,"function_orders":60,"covered_subacts":42,"existing_blueprint_references":31,"new_local_blueprint_references":29,"same_trial_supplements":1,"blueprint_bodies_copied":0,"new_events_functions_or_dialogue":0}
    assert o["exception_report"]==[]
    assert len(o["function_authorities"])==60
    for i,(x,r) in enumerate(zip(o["function_authorities"],s[REG]["functions"])):
        lc,bp,v,rv=provenance(s,r)
        assert x["function_id"]==r["id"] and x["order"]==r["order"] and x["subact"]==r["subact"]
        assert x["current_register"]=={"path":REG,"json_pointer":"/functions/"+str(i),"line_at_read_snapshot":register_line(r["id"]),"relevant_core_sha256":meaning({k:r.get(k) for k in REG_KEYS})}
        assert x["selected_function"]=={"path":r["path"],"json_pointer":r.get("record_pointer") or "/","current_source_sha256":sha(r["path"])}
        assert x["blueprint"]=={"path":lc["blueprint_path"],"json_pointer":lc["pointer"],"current_source_sha256":sha(lc["blueprint_path"]),"record_semantic_sha256":meaning(v),"reference_kind":lc["kind"]}, "Blueprint locator or meaning does not match physical evidence"
        expected_scope=rv.get("qualified_scope",rv.get("scope","CURRENT_EXISTING_EMBEDDED_CANON_CORE_AND_INFORMATION_ACCESS"))
        assert x["qualification"]=={"review_path":lc["review"],"json_pointer":lc["review_pointer"],"current_review_sha256":PINS[lc["review"]],"scope":expected_scope}
        assert x["qualified_status"]=="ACTUAL_VERIFIED" and x["original_generation_flags_preserved"]==generation(bp,v)
        assert x["individual_scene_pov_verified"] is False and x["actual_Pack_compilation_authorized"] is False
        assert x["Blueprint_source_referenceable_under_scope"] is True
        assert x["scope"]=="CURRENT_SOURCE_PATH_REVISION_CORE_AND_INFORMATION_ACCESS_FOR_EXISTING_LOCAL_FUNCTION_ONLY"
    add=o["same_trial_W_supplement"];w=s[BUNDLES[0]]["remaining_blueprints"][0]
    assert add=={"function_id":"A01-EF-002","blueprint_path":BUNDLES[0],"json_pointer":"/remaining_blueprints/0","semantic_sha256":meaning(w),"qualified_status":"ACTUAL_VERIFIED","qualifying_review":REVIEWS[0],"review_sha256":PINS[REVIEWS[0]],"original_generation_status_preserved":w["status"],"new_function_or_event":False}
    assert o["scope_limits"]=={"register_independent_review_completed":False,"parent_pending_flags_rewritten":False,"individual_scene_POV_lock_certified":False,"whole_Act_history_or_G13_complete":False,"final_published_allocation_locked":False,"whole_g14_complete":False,"actual_context_packs":0,"manuscript_allowed":False,"new_author_lock":False,"design_gate":"CLOSED","freeze":"v0.30 PARTIAL"}

def build():
    s=sources();check_sources(s);o=construct(s);check_sources(s)
    fresh=sources();check_sources(fresh);assert_output(o,fresh)
    return o

def validate(o):
    try:
        s=sources();check_sources(s);assert_output(o,s)
        assert o==build(), "Saved authority register differs from current source-bound reconstruction"
        return []
    except (AssertionError,KeyError,ValueError,TypeError) as e:return [str(e) or type(e).__name__]

def render(o):
    lines=["# G13 현재 국소 Blueprint 권위 등록", "", "독립 검문이 수용한 60함수/42소막의 Blueprint 참조만 연결한다. 기존31·새29와 같은 체험 W 보충1의 본문은 복제하지 않는다.", "", "`ACTUAL_VERIFIED`는 해당 국소 설계의 현재 정본·경로·핵심 상태·정보 접근 정합에 한정한다. 원 생성물 pending/false는 이력 그대로이며, 개별 씬 POV와 전체 역사·막 출구·최종 출판 배치는 인증하지 않는다.", "", "| 순서 | 함수 / 소막 | Blueprint 포인터 | 독립 검문 |", "|---:|---|---|---|"]
    for x in o["function_authorities"]:
        b=x["blueprint"];q=x["qualification"]
        lines.append(f"|{x['order']}|{x['function_id']} / {x['subact']}|{b['path']} `{b['json_pointer']}`|{q['review_path']} `{q['json_pointer']}`|")
    lines += ["", "A01-EF002의 같은 체험 W는 `/remaining_blueprints/0`에서 별도로 참조한다. 원 T1/W/T2 순서를 보존하며 새 사건·회차를 만들지 않는다.", "", "현재성은 수용된 immutable 원천 지문과 관련 Canon/등록기 의미 투영으로 검문한다. 역사 전체 SHA/commit은 원 번들·리뷰에 보존한다. 후행 중앙 진척 메모만 바뀌었다고 현재 Blueprint를 STALE로 만들지 않는다.", "", "## 다음 선행조건", "", "실제 Pack 컴파일은 아직 허가되지 않았다. 전체 Act·역사 출구와 최종 회차 배치/G13·G14 선행조건을 계속 충족해야 한다. Pack0·원고0·v0.30 PARTIAL·CLOSED를 유지한다.", "", "| 단계 | 상태 |", "|---|---|", "|1 드래프트|완료|", "|2 S2 유한 시즌|완료|", "|3 원 유한 계약가족|완료|", "|4 장기 커리어|진행|", "|5 결말·전체 구조|미완료|", "|6 집필 규격·Context Pack|국소 Blueprint60 검문 연결·Pack0·미완료|", "|7 통합·독립·최종승인|미완료·CLOSED|", "", "미완료4 / 6번까지3. 새 원고·일정·승인 질문0.", ""]
    return "\n".join(lines)

def selftest():
    good=build();passed=[]
    cases=[("wrong_blueprint_pointer",lambda o:o["function_authorities"][32]["blueprint"].update(json_pointer="/records/12")),
      ("unearned_private_POV",lambda o:o["function_authorities"][0].update(individual_scene_pov_verified=True)),
      ("pending_flag_rewrite",lambda o:o["function_authorities"][31]["original_generation_flags_preserved"].update(parent_this_blueprint_independent_review_completed=True)),
      ("Pack_authority_promotion",lambda o:o["function_authorities"][0].update(actual_Pack_compilation_authorized=True)),
      ("whole_G13_promotion",lambda o:o["scope_limits"].update(whole_Act_history_or_G13_complete=True))]
    for name,fn in cases:
        bad=copy.deepcopy(good);fn(bad)
        try:
            with patch(__name__+".construct",return_value=bad):build()
        except AssertionError:passed.append(name)
        else:raise AssertionError("FALSE PASS "+name)
    original=construct
    def alias(s):
        o=original(s);s[REVIEWS[0]]["qualified_blueprint_status"]="UNVERIFIED";return o
    try:
        with patch(__name__+".construct",side_effect=alias):build()
    except AssertionError:passed.append("source_return_alias_authority_mutation")
    else:raise AssertionError("FALSE PASS source alias")
    return passed

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--write",action="store_true");ap.add_argument("--check",action="store_true");ap.add_argument("--self-test",action="store_true");a=ap.parse_args()
    o=build()
    if a.write:
        (ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
        (ROOT/OUT.replace(".json",".md")).write_text(render(o),encoding="utf-8",newline="\n")
    if a.check:
        assert read(OUT)==o;assert text(OUT.replace(".json",".md"))==render(o);assert not validate(o)
    tests=selftest() if a.self_test else []
    print(json.dumps({"current":True,"functions":60,"subacts":42,"existing":31,"new_local":29,"W":1,"exception_report":[],"writer_controls":tests,"packs":0},ensure_ascii=False))
if __name__=="__main__":main()
