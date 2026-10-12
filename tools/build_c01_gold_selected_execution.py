"""Build the authorized finite fictional gold/duty execution, not real certificates."""
import argparse, copy, hashlib, json
from datetime import date, timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT='canon/C01_GOLD_USED_CALENDAR_SELECTED_EXECUTION_2026_10_12.json'
AUTHOR='canon/C01_PUBLIC_ROUTE_AND_CODEX_REVIEW_AUTHOR_SELECTION_2026_10_12.json'
CAL='research/THREEPEAT_C01_PUBLIC_AND_DUTY_USED_CALENDAR_PREPARATION_2026_10_09.json'
R09='research/LC1_R09_TOURNAMENT_AND_NM1_AUTHOR_OPTIONS_2026_10_08.json'
CHI='simulation/THREEPEAT_2024_25_CHI_SERVICE_AND_ROLE_JOIN_2026_10_09.json'
MIN='simulation/THREEPEAT_2025_MIN_NAMED15_AND_USED_ROTATION_2026_10_09.json'
MIN_SERVICE='simulation/MINNESOTA_2025_26_A11_SELECTED_NAMED15_SERVICE_2026_10_08.json'
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256((ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').encode()).hexdigest()
def ref(p,pointer=''): return {'path':p,'source_sha256':sha(p),'json_pointer':pointer}
def absence_blocks(blocks, removed, targets, allowed):
 """Construct a synthetic legal-time witness; not actual substitution timestamps."""
 holes=[(i,pos) for i,b in enumerate(blocks) for pos,n in b['positions'].items() if n==removed]
 demands={n:int(minutes*60) for n,minutes in targets.items()}
 chosen={}
 def solve(k):
  if k==len(holes): return not any(demands.values())
  i,pos=holes[k];b=blocks[i];span=b['end_second']-b['start_second']
  for n in sorted(demands,key=lambda n:-demands[n]):
   if demands[n]>=span and n not in b['positions'].values() and pos in allowed[n]:
    demands[n]-=span;chosen[i]=n
    if solve(k+1):return True
    demands[n]+=span;chosen.pop(i)
  return False
 assert solve(0),'No legal nonduplicate role replacement witness'
 result=copy.deepcopy(blocks)
 for i,pos in holes: result[i]['positions'][pos]=chosen[i]
 seconds={}
 for b in result:
  assert len(set(b['positions'].values()))==5 and set(b['positions'])=={'PG','SG','SF','PF','C'}
  for n in b['positions'].values(): seconds[n]=seconds.get(n,0)+b['end_second']-b['start_second']
 assert sum(seconds.values())==14400 and removed not in seconds and max(seconds.values())<=2880
 return {'classification':'SYNTHETIC_REGULATION_ROLE_FEASIBILITY_NOT_ACTUAL_SUBSTITUTION_CLOCK',
         'ordered_blocks':result,'player_seconds':seconds,'player_minutes':{n:s/60 for n,s in seconds.items()},
         'total_player_seconds':14400,'total_minutes':240,'removed_actor_minutes':0}
def build():
 author=load(AUTHOR);cal=load(CAL);r09=load(R09)
 assert author['selection']['medal']=='GOLD' and author['independent_Codex_review_authorization']['agent_creation_allowed']
 gold=copy.deepcopy(cal['gold_with_duties_candidate'])
 profiles=copy.deepcopy(r09['candidate_shared_clock_profiles'])
 by_profile={p['id']:p for p in profiles}
 for p in profiles:
  p['classification']='SELECTED_FICTIONAL_SHARED_CLOCK_ROLE_WITNESS_NOT_ACTUAL_BOX'
  assert sum(p['player_minutes'].values())==200
  observed={n:0 for n in p['roster']}
  for b in p['blocks']:
   assert len(b['players'])==len(set(b['players']))==5
   assert b['primary_ball_handler'] in b['players'] and b['center'] in b['players']
   for n in b['players']: observed[n]+=b['elapsed_end_seconds']-b['elapsed_start_seconds']
  assert observed=={n:v*60 for n,v in p['player_minutes'].items()}
 routes=copy.deepcopy(r09['author_options'][0]['route'])
 causes=[
  ('INA','허훈의 운반·이우석의 수비 교대·하윤기의 림 주행을 유지하며 두NBA선수는 낮은 부하 역할을 나누어 수행한다.'),
  ('QAT','주인공의 페인트 진입을 무조건 마무리하지 않고 외곽 반환과 라건아의 내부 마무리로 나눈다. 슛 성공과 전체 승리는 별도의 가상 결과 선택이다.'),
  ('JPN','Imamura/Terashima/Saito의 외곽 운반·슈팅을 위협으로 두고 라이벌의 첫윙 부담과 이우석·문정현의 교대를 선택한다. 상대를 NBA명성으로 무력화하지 않는다.'),
  ('TPE','LinTingChien/LiuCheng의 운반과Artino/TsengWenTing의 내부 역할 앞에서 허훈의 운반, 김종규의 스크린, 이승현의 전환 인계를 나눈다.'),
  ('JOR','Jefferson의 창조와AlDwairi/Mustafa의 내부 분업을 남기며 두윙의 공 운반·박스아웃과 라건아의 마무리를 분리한다. 상대 실패를 고의나 무능으로 만들지 않는다.'),
  ('PHI','Brownlee/Newsome/Thompson의 운반·외곽과Fajardo/Kouame의 내부 선택 앞에서 주인공·라이벌의 다른 윙 부담, 허훈의 반환, 하윤기·라건아의 공 확보를 함께 사용한다.')]
 for row,(opp,cause) in zip(routes,causes):
  assert row['opponent']==opp
  row.update(classification='AUTHOR_SELECTED_FICTIONAL_RESULT_NOT_REAL_HISTORY',selected_winner='KOR',
             result='W',score=None,OT=0,causal_role_model=cause,
             outcome_authority='Human gold-route selection with bounded delegated game implementation; minute legality does not predict victory.')
  row['selected_shared_clock_profile']=row.pop('minutes_profile')
  row.pop('result_candidate',None)
 education=copy.deepcopy(gold['education_slots'])
 for e in education:
  e['selected_start_KST']=e['candidate_start_KST'];e['selected_end_KST']=e['candidate_end_KST']
  e['selected_days']=e['candidate_days'];e['status']='SELECTED_FICTIONAL_REQUIRED_COURSE_MODEL'
  e['actual_order_or_attendance']=None
  e['institutional_resolution']='Separate fictional competent-agency notice and attendance/order model; duration is not a recovered historical course or statutory minimum.'
 sessions=copy.deepcopy(gold['candidate_volunteer_sessions'])
 for s in sessions:
  s['status']='SELECTED_FICTIONAL_APPROVED_PLAN_NOT_PERFORMED_REAL_HOURS'
  s['selected_plan_hours']=s['candidate_instruction_hours']
  s['selected_host_type']='Separately MCST-designated eligible domestic/foreign institution in fictional administration; no named real host approval asserted.'
  s['NBA_availability_resolution']='Unpaid activity is not NBAtraining/service. Club release and local travel/preparation reserved; any incompatible ordinary game/practice shifts activity through approved same-quarter amendment. Exact dated pool remains plan, not completed attendance.'
 assert len(sessions)==68 and sum(s['selected_plan_hours'] for s in sessions)==544
 assert sum(s['selected_plan_hours'] for s in sessions if s['venue_jurisdiction']=='KOREA_DOMESTIC')==272
 windows=[
 {'year':2023,'team':'CHI','actor':'CHI protagonist','NBA_unavailable_local_dates':['2023-11-09','2023-11-25'],
  'known_game_dates':['2023-11-12','2023-11-13','2023-11-15','2023-11-17','2023-11-18','2023-11-20','2023-11-22','2023-11-24'],
  'minutes_removed':34,'replacement_added_minutes':{'Jaquez':12,'Duarte':10,'Caruso':6,'Green':6}},
 {'year':2023,'team':'MIN','actor':'MIN rival','NBA_unavailable_local_dates':['2023-11-09','2023-11-25'],
  'known_game_dates':['2023-11-10','2023-11-12','2023-11-14','2023-11-15','2023-11-18','2023-11-20','2023-11-22','2023-11-24'],
  'minutes_removed':34,'replacement_added_minutes':{'Beasley':14,'Okogie':10,'Nowell':10}},
 {'year':2024,'team':'CHI','actor':'CHI protagonist','NBA_unavailable_local_dates':['2024-11-14','2024-11-25'],
  'known_game_dates':['2024-11-15','2024-11-17','2024-11-18','2024-11-20','2024-11-22','2024-11-23'],
  'minutes_removed':34,'replacement_added_minutes':{'Jaquez':12,'Duarte':10,'Caruso':6,'Green':6}},
 {'year':2024,'team':'MIN','actor':'MIN rival','NBA_unavailable_local_dates':['2024-11-14','2024-11-25'],
  'known_game_dates':['2024-11-15','2024-11-17','2024-11-21','2024-11-24'],
  'minutes_removed':34,'replacement_added_minutes':{'Beasley':14,'Okogie':10,'Nowell':10}}]
 for w in windows:
  assert sum(w['replacement_added_minutes'].values())==w['minutes_removed']
  w['status']='SELECTED_FICTIONAL_ABSENCE_ROLE_COST'
  w['real_calendar_anchor_not_real_result']=True
  w['P_or_Rival_NBA_minutes_in_absence']=0
  w['source_ref']=ref(CHI,'/role_windows') if w['team']=='CHI' else ref(MIN,'/rotation')
  w['scope']='Explicit local absence and replacement burden; no invented exact substitutions, scores, clinical cause or all82 attendance. Regular season results unused here; selected seed/title endpoints remain existing bounded model.'
  if w['team']=='CHI':
   base=load(CHI)['role_windows'][0 if w['year']==2023 else 1]['ordered_blocks']
   full={'Jaime Jaquez Jr.':12,'Chris Duarte':10,'Alex Caruso':6,'Javonte Green':6}
   w['role_witness']=absence_blocks(base,'Protagonist',full,
     {'Jaime Jaquez Jr.':{'SF','PF'},'Chris Duarte':{'SF'},'Alex Caruso':{'SF'},'Javonte Green':{'SF','PF'}})
   w['registration']='Chosenfictionalcoachactive12 swaps Protagonist out and existingSTD JavonteGreen in; noinjury/suspension/newUPC. FY23capacity nowchosenforthisabsenceonly.'
   w['service_source']=ref(CHI,'/season_service_rows/'+str(w['year']))
  else:
   full={'Malik Beasley':14,'Josh Okogie':10,'Jaylen Nowell':10}
   base=load(MIN)['rotation']['blocks']
   w['role_witness']=absence_blocks(base,'Fictional Rival',full,{n:{'SG','SF'} for n in full})
   service=load(MIN_SERVICE)['named15_service_rows']
   for n in full:
    row=next(x for x in service if x['player']==n)
    covered=any(int(u['first_Season'][:4])<=w['year']<int(u['first_Season'][:4])+u['service_Seasons'] for u in row['selected_new_UPC_chain'])
    original_end=row.get('original_source',{}).get('last_service_Season','0000')
    assert covered or int(original_end[:4])>=w['year'],n
   w['service_source']=ref(MIN_SERVICE,'/named15_service_rows')
   w['registration']='Existingstandard13rotationactors: Rivalinactive; Nowelladdedtoactive12, existingCulverinactive. No2025game/service claim importedfromundatedgrammar.'
 institutional=[
 {'date':'2023-07-15','actors':'KBA/KOC→OCAentry','act':'Existing12roster timely accepted in fictional public route; replaces private-only bridge, no second roster choice.'},
 {'date':'2023-09-14','actors':'NBA/FIBA/NBPA; CHI and MIN separately','act':'SelectedwrittenAG2023-onlyaccord expressly coversSep26–Oct6publicgames andMIN Sep29/CHI Oct3campSeasonoverlap/UPCexcusedabsence. Clubconsents andsatisfactorydisabilitycoverage separatefictionacts. ArticleXXIII3(c)off-seasonexamplesalone donotwaivecampSeasonboundary; no2018exception copied.'},
 {'date':'2023-09-25','actors':'technicaldelegate/teamrepresentatives','act':'Before14:00CST meeting, public entry/eligibility complete; no late roster insertion.'},
 {'date':'2023-10-09','actors':'two clubs/player/agent','act':'Separate club return and limitedpracticefromOct10; lostcamp/media/preseason opportunities remain.'},
 {'date':'2023-10-20','actors':'MCST recommendation→regionalMMA admission, eachactorseparate','act':'Fictional sports-service admission; no34monthblanketexemption or automatic544hours.'}]
 return {'id':'C01_GOLD_USED_CALENDAR_SELECTED_EXECUTION_2026_10_12',
  'choice_id':'C01_CALENDAR','kind':'CALENDAR_AVAILABILITY','selected':True,
  'status':'SELECTED_FICTIONAL_USED_RESOLUTION','authority_class':'AUTHOR_SELECTED','producer_id':'root_codex',
  'resolution':'승인된2023항저우 금메달/NM1과 별도 체육요원 편입을 작품 경로로 사용한다. 각자34개월·교육·544시간의무·국외허가를 한정 가상 기관/달력과NBA부재/동료비용으로 실행하고,2035사용3일의 적법한 의무·여행 상태를 별도 가상 모델로 연결한다. 실제2023금메달·정부증서·실적 인증은 아니다.',
  'used_calendar_status':'SELECTED_RESOLVED','covered_exit_port_ids':['FC031','FC032','FC040'],
  'unresolved_used_dependencies':[],
  'authority_basis':ref(AUTHOR),
  'source_sha256':{p:sha(p) for p in [AUTHOR,CAL,R09,CHI,MIN,MIN_SERVICE]},
  'selected_public_institutional_acts':institutional,'selected_games':routes,'shared_clock_profiles':profiles,
  'original_butterfly_cost_ref':ref(R09,'/existing_author_design_preserved/displaced_opportunities'),
  'medal_butterfly':'KOR7→gold;JPND1bye/TPEsemifinal andPHIgoldopportunity change, no actualplayersprivateintent fabricated.',
  'selected_admission_date':'2023-10-20','selected_nominal_service_end':'2026-08-19',
  'service_end_formula':gold['completion_formula'],'selected_education':education,
  'selected_domestic_trips':gold['domestic_trip_capacity'],'selected_volunteer_plan':sessions,
  'per_actor_planned_hours':544,'per_actor_domestic_hours':272,'per_actor_foreign_hours':272,
  'pooled_actor_hours':False,'actual_completed_hours':None,'actual_recognized_hours':None,
  'administrative_deadlines_by_actor':cal['administrative_deadlines_by_actor'],
  'selected_initial_foreign_stay_permits':[
   {'actor':actor,'start_KST':'2023-10-20','end_KST':'2023-11-10',
    'countries':['USA','Canada'],'return_by_KST':'2023-11-10',
    'institutional_order':'MCSTrecommendation→regionalMMAadmissionandseparateforeignstaydecisioneffectiveatadmissioninthesamefictionaladministrativebundle. No preadmissionartsqualification or uncoveredUSstay assumed.',
    'purpose':'AlreadyabroadNBAfieldserviceuntilNov9USdeparture/Nov10Koreareturn',
    'classification':'SELECTED_FICTIONAL_INITIAL_STAY_PERMISSION_NOT_REAL_CERTIFICATE'}
   for actor in ['CHI protagonist','MIN rival']],
  'selected_foreign_permission_windows':[
   {'actor':actor,'id':trip['id']+':'+actor,
    'issued_fictionally_before_KST':(date.fromisoformat(trip['candidate_Korea_to_US_departure_KST'])-timedelta(days=2)).isoformat(),
    'start_KST':trip['candidate_Korea_to_US_departure_KST'],'end_KST':'2026-08-19',
    'countries':['USA','Canada'],'purpose':'registeredNBAfieldserviceandseparatelyapprovedunpaidpublicservice',
    'classification':'SEPARATE_SELECTED_FICTIONAL_MCST_RECOMMENDATION_REGIONAL_MMA_PERMIT_NOT_REAL_CERTIFICATE',
    'conditions':'Norevocation/excludedextensioninselectedfamily; completion endsartspermit. Koreaexit aftercompetentagencyissue. Anyothercountryseparatetravelpermit, noautomaticworldwideNBApermission.'}
   for actor in ['CHI protagonist','MIN rival'] for trip in gold['domestic_trip_capacity']],
  'NBA_absence_windows':windows,
  '2026_Korea_remote_UPC_access':{
   'Protagonist':{'signature_ET':'2026-07-07T12:04:00-04:00','same_instant_KST':'2026-07-08T01:04:00+09:00',
    'location':'KOREA','selected_method':'PreviouslyselectedUPC signedthroughlawfulremoteplayer/agent/clubchannelwithindependentpartyassent; agentrelayssignedreceipt. NoChicago physicalpresenceclaimed.',
    'next_job_education_KST':'2026-07-08T09:00:00+09:00','window_hours_before_course':7.933333333333334},
   'Rival':'AnyalreadyusedsameJuly7MINUPC assentisreceivedseparatelyinKorea throughlawfulremotechannelbeforeJuly8course; noPsignaturecoversRival.',
   'price_or_terms_changed':False,'travel_permit_is_UPC_assent':False},
  'club_contract_and_service_resolution':{
   'classification':'SELECTED_FICTIONAL_CBA_CONFORMING_CLUB_AUTHORIZED_ABSENCE_NOT_REAL_SIDELETTER',
   'contract_and_cap':'ExistingselectedUPCterms/capcharge retained; noextraUPC/salaryprice/guarantee change, noinjury suspension invented.',
   'pay':'Selectedfictionalclub/leagueconformingexcusedauthorizedleave retains existingUPCbasepay andcapcharge, withclubconsentandrequiredCBAchannels; noattendancefine/suspension ornewprice. Thisisexpressfictionagreement, notArticleVautomaticmilitarypayentitlement. NoNBAcourt/practice/service performedinsideeducation/trips.',
   'registration_and_YOS':'Existingregisteredcontractcontinuity andusedoutsideabsenceNBAgames preserveapplicableYOS; absenceisnotautomaticfreeagency/noseparate82gameclaim.',
   'return':'Foreignpermit+travel/rest+clubre-admission andlimitedpractice modeledseparately before usedlaterNBArole, notinstantgamefitness.'},
  'positive_costs':{'travel_lodging_meals':'actor/eligiblelawfulsupport, noautomaticgovernmentfullreimbursement',
   'materials_host_logistics':'publicserviceplanfunds/actoraslegallyallowed, noNBAwagecredit',
   'public_competition_disability_insurance':'separateCHI/MINsatisfactorypositiveGammafamily;priceunknownpreserved',
   'NBA_opportunity':'missedcamp/mediapreseason and0actorNBAminutesinabsence withnamedcoactorburden',
   'no_double_credit':'Necessaryexpenses countedonce;NBAwages/sponsorshipnotvolunteerhours orpaidcliniccredit'},
  'future_completion_and_2035_used_state':{
   'classification':'AUTHOR_MODELED_FUTURE_ADMINISTRATION_NOT_CURRENT_LAW_FORECAST_OR_REAL_RECORD',
   'selected_completion_disposition':'Eachactorselectedfuturefictionledger: finalplannedactivityJuly14_2026→allfinalproofbyJuly24→competentrecognition544hoursandcoursecompletioncheckedJuly25→Aug1dispositionnoticeeffectiveAug19_2026. Exclusions/extensions0 inselectedmodel. Thisseparatechosenfutureperformed/recognizedcheckpoint, nottheplannedpoolorrealcertificate, establishesretirementbackstory.',
   'no_real_completed_hours_claim':True,
   'selected_current_usepoint_guard':'Selectedfuturelaw-continuityfiction: owncompetentagencyJune10_2035acceptsoverseasUSstayandlawfuldeferralofapplicableannualtrainingtoSep15_2035; resultingnoticeknownbeforeJune18. NoobligationduringJune18–20. Successorlawconformityisexplicitfictionassumption, notrecovered2035law. No34monthpermitextendedto2035.',
   'service_guest_retirement':'NBAserviceJun18_23ET→separatelypermittedguestJun19_10ET→publicretirementJun20_10ET; guestnotstaffemployment.',
   'all_middle_year_games_or_private_certificates_required':False},
  'verification_boundary':'Selectedfinitefictionimplementation subjecttoreviewerchecks; noactualpubliccertificate orallcareer/fullregularseasonmedicalverification.',
  'independent_review_completed':False,
  'gates':{'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--refresh-owned',action='store_true');p.add_argument('--expected-hash');a=p.parse_args()
 raw=json.dumps(build(),ensure_ascii=False,indent=2)+'\n';out=ROOT/OUT
 if a.check:
  assert out.read_text(encoding='utf-8-sig').replace('\r\n','\n')==raw
 elif out.exists():
  exact_hashes={sha(OUT),hashlib.sha256(out.read_bytes()).hexdigest()}
  assert a.refresh_owned and a.expected_hash in exact_hashes,'Refusing overwrite without exactowned raw or normalized hash'
  backup=ROOT/'Temp/c01_owned_before_repair.json';backup.write_bytes(out.read_bytes());out.write_text(raw,encoding='utf-8')
 else: out.write_text(raw,encoding='utf-8')
 print(json.dumps({'selected_route':True,'fiction_only':True,'six_games':6,'planned_hours_each':544,'independent_review_completed':False},ensure_ascii=False))
if __name__=='__main__':main()
