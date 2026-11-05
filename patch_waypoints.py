import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# =============================================================================
# INTERMEDIATE ROAD WAYPOINTS
# These hidden waypoints follow actual road curves between major stops.
# They are prefixed with "wp_" to distinguish from real bus stops.
# Coordinates are traced from OSM road geometry for Vijayawada city area.
# =============================================================================

NEW_WAYPOINTS = '''
  /* ── Hidden Road-Curve Waypoints (not shown as stops in UI) ── */
  "wp_krm_pnbs_1":       { "id":"wp_krm_pnbs_1",       "name":"", "teName":"", "lat":16.5125, "lng":80.6285, "hidden":true },
  "wp_krm_pnbs_2":       { "id":"wp_krm_pnbs_2",       "name":"", "teName":"", "lat":16.5100, "lng":80.6240, "hidden":true },
  "wp_krm_pnbs_3":       { "id":"wp_krm_pnbs_3",       "name":"", "teName":"", "lat":16.5085, "lng":80.6215, "hidden":true },

  "wp_pnbs_rly_1":       { "id":"wp_pnbs_rly_1",       "name":"", "teName":"", "lat":16.5100, "lng":80.6205, "hidden":true },
  "wp_pnbs_rly_2":       { "id":"wp_pnbs_rly_2",       "name":"", "teName":"", "lat":16.5140, "lng":80.6210, "hidden":true },
  "wp_pnbs_rly_3":       { "id":"wp_pnbs_rly_3",       "name":"", "teName":"", "lat":16.5165, "lng":80.6218, "hidden":true },

  "wp_pnbs_gov_1":       { "id":"wp_pnbs_gov_1",       "name":"", "teName":"", "lat":16.5092, "lng":80.6232, "hidden":true },
  "wp_pnbs_gov_2":       { "id":"wp_pnbs_gov_2",       "name":"", "teName":"", "lat":16.5100, "lng":80.6270, "hidden":true },
  "wp_pnbs_gov_3":       { "id":"wp_pnbs_gov_3",       "name":"", "teName":"", "lat":16.5108, "lng":80.6305, "hidden":true },

  "wp_gov_pcr_1":        { "id":"wp_gov_pcr_1",        "name":"", "teName":"", "lat":16.5112, "lng":80.6315, "hidden":true },

  "wp_pcr_igmc_1":       { "id":"wp_pcr_igmc_1",       "name":"", "teName":"", "lat":16.5072, "lng":80.6285, "hidden":true },
  "wp_pcr_igmc_2":       { "id":"wp_pcr_igmc_2",       "name":"", "teName":"", "lat":16.5052, "lng":80.6318, "hidden":true },

  "wp_igmc_benz_1":      { "id":"wp_igmc_benz_1",      "name":"", "teName":"", "lat":16.5028, "lng":80.6368, "hidden":true },
  "wp_igmc_benz_2":      { "id":"wp_igmc_benz_2",      "name":"", "teName":"", "lat":16.5015, "lng":80.6425, "hidden":true },

  "wp_benz_pat_1":       { "id":"wp_benz_pat_1",       "name":"", "teName":"", "lat":16.5005, "lng":80.6528, "hidden":true },
  "wp_benz_pat_2":       { "id":"wp_benz_pat_2",       "name":"", "teName":"", "lat":16.4992, "lng":80.6562, "hidden":true },

  "wp_pat_auto_1":       { "id":"wp_pat_auto_1",       "name":"", "teName":"", "lat":16.4975, "lng":80.6590, "hidden":true },
  "wp_pat_auto_2":       { "id":"wp_pat_auto_2",       "name":"", "teName":"", "lat":16.4962, "lng":80.6622, "hidden":true },

  "wp_auto_kam_1":       { "id":"wp_auto_kam_1",       "name":"", "teName":"", "lat":16.4938, "lng":80.6700, "hidden":true },
  "wp_auto_kan_1":       { "id":"wp_auto_kan_1",       "name":"", "teName":"", "lat":16.4912, "lng":80.6728, "hidden":true },
  "wp_auto_kan_2":       { "id":"wp_auto_kan_2",       "name":"", "teName":"", "lat":16.4892, "lng":80.6762, "hidden":true },

  "wp_kam_por_1":        { "id":"wp_kam_por_1",        "name":"", "teName":"", "lat":16.4892, "lng":80.6870, "hidden":true },
  "wp_kam_por_2":        { "id":"wp_kam_por_2",        "name":"", "teName":"", "lat":16.4862, "lng":80.6952, "hidden":true },
  "wp_kan_por_1":        { "id":"wp_kan_por_1",        "name":"", "teName":"", "lat":16.4862, "lng":80.6952, "hidden":true },

  "wp_por_pen_1":        { "id":"wp_por_pen_1",        "name":"", "teName":"", "lat":16.4795, "lng":80.7108, "hidden":true },
  "wp_por_pen_2":        { "id":"wp_por_pen_2",        "name":"", "teName":"", "lat":16.4768, "lng":80.7162, "hidden":true },

  /* Machavaram / Gunadala corridor (Eluru Road east branch) */
  "wp_sit_mach_1":       { "id":"wp_sit_mach_1",       "name":"", "teName":"", "lat":16.5182, "lng":80.6402, "hidden":true },
  "wp_sit_mach_2":       { "id":"wp_sit_mach_2",       "name":"", "teName":"", "lat":16.5190, "lng":80.6448, "hidden":true },
  "wp_mach_gun_1":       { "id":"wp_mach_gun_1",       "name":"", "teName":"", "lat":16.5228, "lng":80.6535, "hidden":true },
  "wp_mach_gun_2":       { "id":"wp_mach_gun_2",       "name":"", "teName":"", "lat":16.5248, "lng":80.6572, "hidden":true },
  "wp_gun_ramv_1":       { "id":"wp_gun_ramv_1",       "name":"", "teName":"", "lat":16.5272, "lng":80.6618, "hidden":true },
  "wp_gun_ramv_2":       { "id":"wp_gun_ramv_2",       "name":"", "teName":"", "lat":16.5295, "lng":80.6658, "hidden":true },
  "wp_gun_ramv_3":       { "id":"wp_gun_ramv_3",       "name":"", "teName":"", "lat":16.5312, "lng":80.6690, "hidden":true },

  /* Ramavarappadu → NH16 → Gannavaram corridor */
  "wp_ramv_enik_1":      { "id":"wp_ramv_enik_1",      "name":"", "teName":"", "lat":16.5322, "lng":80.6815, "hidden":true },
  "wp_ramv_enik_2":      { "id":"wp_ramv_enik_2",      "name":"", "teName":"", "lat":16.5312, "lng":80.6912, "hidden":true },
  "wp_ramv_enik_3":      { "id":"wp_ramv_enik_3",      "name":"", "teName":"", "lat":16.5308, "lng":80.6985, "hidden":true },
  "wp_enik_nida_1":      { "id":"wp_enik_nida_1",      "name":"", "teName":"", "lat":16.5308, "lng":80.7048, "hidden":true },
  "wp_nida_guda_1":      { "id":"wp_nida_guda_1",      "name":"", "teName":"", "lat":16.5322, "lng":80.7188, "hidden":true },
  "wp_nida_guda_2":      { "id":"wp_nida_guda_2",      "name":"", "teName":"", "lat":16.5348, "lng":80.7268, "hidden":true },
  "wp_guda_kesr_1":      { "id":"wp_guda_kesr_1",      "name":"", "teName":"", "lat":16.5388, "lng":80.7358, "hidden":true },
  "wp_guda_kesr_2":      { "id":"wp_guda_kesr_2",      "name":"", "teName":"", "lat":16.5402, "lng":80.7432, "hidden":true },
  "wp_kesr_airp_1":      { "id":"wp_kesr_airp_1",      "name":"", "teName":"", "lat":16.5388, "lng":80.7518, "hidden":true },
  "wp_kesr_airp_2":      { "id":"wp_kesr_airp_2",      "name":"", "teName":"", "lat":16.5385, "lng":80.7598, "hidden":true },
  "wp_airp_gann_1":      { "id":"wp_airp_gann_1",      "name":"", "teName":"", "lat":16.5378, "lng":80.7688, "hidden":true },
  "wp_airp_gann_2":      { "id":"wp_airp_gann_2",      "name":"", "teName":"", "lat":16.5352, "lng":80.7762, "hidden":true },
  "wp_airp_gann_3":      { "id":"wp_airp_gann_3",      "name":"", "teName":"", "lat":16.5328, "lng":80.7812, "hidden":true },

  /* Varadhi Bridge → Tadepalli → Mangalagiri */
  "wp_pnbs_vara_1":      { "id":"wp_pnbs_vara_1",      "name":"", "teName":"", "lat":16.5065, "lng":80.6178, "hidden":true },
  "wp_pnbs_vara_2":      { "id":"wp_pnbs_vara_2",      "name":"", "teName":"", "lat":16.5048, "lng":80.6162, "hidden":true },
  "wp_vara_tade_1":      { "id":"wp_vara_tade_1",      "name":"", "teName":"", "lat":16.5008, "lng":80.6148, "hidden":true },
  "wp_vara_tade_2":      { "id":"wp_vara_tade_2",      "name":"", "teName":"", "lat":16.4968, "lng":80.6138, "hidden":true },
  "wp_vara_tade_3":      { "id":"wp_vara_tade_3",      "name":"", "teName":"", "lat":16.4920, "lng":80.6132, "hidden":true },
  "wp_tade_mang_1":      { "id":"wp_tade_mang_1",      "name":"", "teName":"", "lat":16.4788, "lng":80.6118, "hidden":true },
  "wp_tade_mang_2":      { "id":"wp_tade_mang_2",      "name":"", "teName":"", "lat":16.4682, "lng":80.6110, "hidden":true },
  "wp_tade_mang_3":      { "id":"wp_tade_mang_3",      "name":"", "teName":"", "lat":16.4562, "lng":80.6105, "hidden":true },
  "wp_mang_nula_1":      { "id":"wp_mang_nula_1",      "name":"", "teName":"", "lat":16.4718, "lng":80.6112, "hidden":true },

  /* NH65 West → Bhavanipuram → Ibrahimpatnam */
  "wp_krm_bhav_1":       { "id":"wp_krm_bhav_1",       "name":"", "teName":"", "lat":16.5272, "lng":80.6202, "hidden":true },
  "wp_krm_bhav_2":       { "id":"wp_krm_bhav_2",       "name":"", "teName":"", "lat":16.5298, "lng":80.6155, "hidden":true },
  "wp_krm_bhav_3":       { "id":"wp_krm_bhav_3",       "name":"", "teName":"", "lat":16.5322, "lng":80.6072, "hidden":true },
  "wp_bhav_goll_1":      { "id":"wp_bhav_goll_1",      "name":"", "teName":"", "lat":16.5345, "lng":80.5968, "hidden":true },
  "wp_bhav_goll_2":      { "id":"wp_bhav_goll_2",      "name":"", "teName":"", "lat":16.5382, "lng":80.5875, "hidden":true },
  "wp_goll_ibra_1":      { "id":"wp_goll_ibra_1",      "name":"", "teName":"", "lat":16.5548, "lng":80.5642, "hidden":true },
  "wp_goll_ibra_2":      { "id":"wp_goll_ibra_2",      "name":"", "teName":"", "lat":16.5648, "lng":80.5512, "hidden":true },
  "wp_goll_ibra_3":      { "id":"wp_goll_ibra_3",      "name":"", "teName":"", "lat":16.5748, "lng":80.5388, "hidden":true },

  /* Eluru Road / Route 308 → Nuzvid */
  "wp_pnbs_chap_1":      { "id":"wp_pnbs_chap_1",      "name":"", "teName":"", "lat":16.5102, "lng":80.6238, "hidden":true },
  "wp_chap_buda_1":      { "id":"wp_chap_buda_1",      "name":"", "teName":"", "lat":16.5158, "lng":80.6268, "hidden":true },
  "wp_buda_paip_1":      { "id":"wp_buda_paip_1",      "name":"", "teName":"", "lat":16.5252, "lng":80.6318, "hidden":true },
  "wp_buda_paip_2":      { "id":"wp_buda_paip_2",      "name":"", "teName":"", "lat":16.5308, "lng":80.6332, "hidden":true },
  "wp_paip_payk_1":      { "id":"wp_paip_payk_1",      "name":"", "teName":"", "lat":16.5395, "lng":80.6468, "hidden":true },
  "wp_paip_payk_2":      { "id":"wp_paip_payk_2",      "name":"", "teName":"", "lat":16.5412, "lng":80.6568, "hidden":true },
  "wp_payk_nunn_1":      { "id":"wp_payk_nunn_1",      "name":"", "teName":"", "lat":16.5468, "lng":80.6728, "hidden":true },
  "wp_payk_nunn_2":      { "id":"wp_payk_nunn_2",      "name":"", "teName":"", "lat":16.5512, "lng":80.6842, "hidden":true },
  "wp_nunn_nrih_1":      { "id":"wp_nunn_nrih_1",      "name":"", "teName":"", "lat":16.5588, "lng":80.6988, "hidden":true },
  "wp_nunn_nrih_2":      { "id":"wp_nunn_nrih_2",      "name":"", "teName":"", "lat":16.5912, "lng":80.7268, "hidden":true },
  "wp_nunn_nrih_3":      { "id":"wp_nunn_nrih_3",      "name":"", "teName":"", "lat":16.6152, "lng":80.7425, "hidden":true },
  "wp_agir_ravi_1":      { "id":"wp_agir_ravi_1",      "name":"", "teName":"", "lat":16.6758, "lng":80.7858, "hidden":true },
  "wp_ravi_nuzv_1":      { "id":"wp_ravi_nuzv_1",      "name":"", "teName":"", "lat":16.7388, "lng":80.8168, "hidden":true },
  "wp_ravi_nuzv_2":      { "id":"wp_ravi_nuzv_2",      "name":"", "teName":"", "lat":16.7688, "lng":80.8342, "hidden":true },
  "wp_nuzv_viss_1":      { "id":"wp_nuzv_viss_1",      "name":"", "teName":"", "lat":16.8188, "lng":80.8468, "hidden":true },
  "wp_nuzv_viss_2":      { "id":"wp_nuzv_viss_2",      "name":"", "teName":"", "lat":16.8552, "lng":80.8542, "hidden":true },

  /* Route 16R → Kandrika area */
  "wp_leni_elur_1":      { "id":"wp_leni_elur_1",      "name":"", "teName":"", "lat":16.5158, "lng":80.6262, "hidden":true },
  "wp_elur_buda_1":      { "id":"wp_elur_buda_1",      "name":"", "teName":"", "lat":16.5192, "lng":80.6282, "hidden":true },
  "wp_buda_daba_1":      { "id":"wp_buda_daba_1",      "name":"", "teName":"", "lat":16.5238, "lng":80.6308, "hidden":true },
  "wp_daba_newrr_1":     { "id":"wp_daba_newrr_1",     "name":"", "teName":"", "lat":16.5268, "lng":80.6318, "hidden":true },

  /* Kondapalli → PNBS (NH65 east side) */
  "wp_kond_pnbs_1":      { "id":"wp_kond_pnbs_1",      "name":"", "teName":"", "lat":16.5885, "lng":80.5488, "hidden":true },
  "wp_kond_pnbs_2":      { "id":"wp_kond_pnbs_2",      "name":"", "teName":"", "lat":16.5652, "lng":80.5648, "hidden":true },
  "wp_kond_pnbs_3":      { "id":"wp_kond_pnbs_3",      "name":"", "teName":"", "lat":16.5488, "lng":80.5792, "hidden":true },
  "wp_kond_pnbs_4":      { "id":"wp_kond_pnbs_4",      "name":"", "teName":"", "lat":16.5312, "lng":80.6012, "hidden":true },

  /* Kabela → KR Market */
  "wp_kabe_krm_1":       { "id":"wp_kabe_krm_1",       "name":"", "teName":"", "lat":16.5298, "lng":80.6108, "hidden":true },
  "wp_kabe_krm_2":       { "id":"wp_kabe_krm_2",       "name":"", "teName":"", "lat":16.5248, "lng":80.6168, "hidden":true },
  "wp_kabe_krm_3":       { "id":"wp_kabe_krm_3",       "name":"", "teName":"", "lat":16.5198, "lng":80.6228, "hidden":true },
  "wp_kabe_krm_4":       { "id":"wp_kabe_krm_4",       "name":"", "teName":"", "lat":16.5168, "lng":80.6278, "hidden":true },

  /* Gannavaram → Hanuman Junction NH16 */
  "wp_gann_hanu_1":      { "id":"wp_gann_hanu_1",      "name":"", "teName":"", "lat":16.5428, "lng":80.8112, "hidden":true },
  "wp_gann_hanu_2":      { "id":"wp_gann_hanu_2",      "name":"", "teName":"", "lat":16.5658, "lng":80.8548, "hidden":true },
  "wp_gann_hanu_3":      { "id":"wp_gann_hanu_3",      "name":"", "teName":"", "lat":16.5938, "lng":80.8988, "hidden":true },
  "wp_gann_hanu_4":      { "id":"wp_gann_hanu_4",      "name":"", "teName":"", "lat":16.6148, "lng":80.9312, "hidden":true },

  /* Milkproject → KR Market loop */
  "wp_milk_krm_1":       { "id":"wp_milk_krm_1",       "name":"", "teName":"", "lat":16.5248, "lng":80.6258, "hidden":true },
  "wp_milk_krm_2":       { "id":"wp_milk_krm_2",       "name":"", "teName":"", "lat":16.5202, "lng":80.6292, "hidden":true },

  /* KR Market → Tummalapalli → PNBS */
  "wp_krm_tum_1":        { "id":"wp_krm_tum_1",        "name":"", "teName":"", "lat":16.5138, "lng":80.6278, "hidden":true },
  "wp_tum_pnbs_1":       { "id":"wp_tum_pnbs_1",       "name":"", "teName":"", "lat":16.5105, "lng":80.6238, "hidden":true },
  "wp_tum_pnbs_2":       { "id":"wp_tum_pnbs_2",       "name":"", "teName":"", "lat":16.5088, "lng":80.6218, "hidden":true },

  /* Railwaystn → Sitarampuram → Machavaram */
  "wp_rly_sit_1":        { "id":"wp_rly_sit_1",        "name":"", "teName":"", "lat":16.5188, "lng":80.6278, "hidden":true },
  "wp_rly_sit_2":        { "id":"wp_rly_sit_2",        "name":"", "teName":"", "lat":16.5185, "lng":80.6338, "hidden":true },

  /* Eluru Road Junction - various connections */
  "wp_eluru_gun_1":      { "id":"wp_eluru_gun_1",      "name":"", "teName":"", "lat":16.5175, "lng":80.6355, "hidden":true },
  "wp_eluru_gun_2":      { "id":"wp_eluru_gun_2",      "name":"", "teName":"", "lat":16.5192, "lng":80.6415, "hidden":true },
  "wp_eluru_gun_3":      { "id":"wp_eluru_gun_3",      "name":"", "teName":"", "lat":16.5208, "lng":80.6488, "hidden":true },
  "wp_eluru_gun_4":      { "id":"wp_eluru_gun_4",      "name":"", "teName":"", "lat":16.5228, "lng":80.6548, "hidden":true },
  "wp_eluru_gun_5":      { "id":"wp_eluru_gun_5",      "name":"", "teName":"", "lat":16.5252, "lng":80.6618, "hidden":true },

  /* PCR → Benz Circle direct */
  "wp_pcr_benz_1":       { "id":"wp_pcr_benz_1",       "name":"", "teName":"", "lat":16.5072, "lng":80.6345, "hidden":true },
  "wp_pcr_benz_2":       { "id":"wp_pcr_benz_2",       "name":"", "teName":"", "lat":16.5042, "lng":80.6398, "hidden":true },
  "wp_pcr_benz_3":       { "id":"wp_pcr_benz_3",       "name":"", "teName":"", "lat":16.5018, "lng":80.6448, "hidden":true },
  "wp_pcr_benz_4":       { "id":"wp_pcr_benz_4",       "name":"", "teName":"", "lat":16.5008, "lng":80.6492, "hidden":true },

  /* KR Market → PCR */
  "wp_krm_pcr_1":        { "id":"wp_krm_pcr_1",        "name":"", "teName":"", "lat":16.5138, "lng":80.6312, "hidden":true },
  "wp_krm_pcr_2":        { "id":"wp_krm_pcr_2",        "name":"", "teName":"", "lat":16.5122, "lng":80.6298, "hidden":true },
  "wp_krm_pcr_3":        { "id":"wp_krm_pcr_3",        "name":"", "teName":"", "lat":16.5112, "lng":80.6278, "hidden":true },

  /* PCR → Ganguru → Uppuluru / Kankipadu */
  "wp_pcr_gang_1":       { "id":"wp_pcr_gang_1",       "name":"", "teName":"", "lat":16.5062, "lng":80.6318, "hidden":true },
  "wp_pcr_gang_2":       { "id":"wp_pcr_gang_2",       "name":"", "teName":"", "lat":16.4985, "lng":80.6458, "hidden":true },
  "wp_gang_uppu_1":      { "id":"wp_gang_uppu_1",      "name":"", "teName":"", "lat":16.4792, "lng":80.6618, "hidden":true },
  "wp_gang_uppu_2":      { "id":"wp_gang_uppu_2",      "name":"", "teName":"", "lat":16.4712, "lng":80.6818, "hidden":true },
  "wp_gang_uppu_3":      { "id":"wp_gang_uppu_3",      "name":"", "teName":"", "lat":16.4658, "lng":80.7052, "hidden":true },
  "wp_gang_uppu_4":      { "id":"wp_gang_uppu_4",      "name":"", "teName":"", "lat":16.4622, "lng":80.7248, "hidden":true },
  "wp_gang_uppu_5":      { "id":"wp_gang_uppu_5",      "name":"", "teName":"", "lat":16.4602, "lng":80.7388, "hidden":true },

  /* Benz Circle → Ganguru (via bypass) */
  "wp_benz_gang_1":      { "id":"wp_benz_gang_1",      "name":"", "teName":"", "lat":16.4998, "lng":80.6568, "hidden":true },
  "wp_benz_gang_2":      { "id":"wp_benz_gang_2",      "name":"", "teName":"", "lat":16.4942, "lng":80.6648, "hidden":true },
  "wp_benz_gang_3":      { "id":"wp_benz_gang_3",      "name":"", "teName":"", "lat":16.4862, "lng":80.6778, "hidden":true },

  /* Mangalagiri → Guntur */
  "wp_mang_gun_1":       { "id":"wp_mang_gun_1",       "name":"", "teName":"", "lat":16.4188, "lng":80.5318, "hidden":true },
  "wp_mang_gun_2":       { "id":"wp_mang_gun_2",       "name":"", "teName":"", "lat":16.3888, "lng":80.5012, "hidden":true },
  "wp_mang_gun_3":       { "id":"wp_mang_gun_3",       "name":"", "teName":"", "lat":16.3508, "lng":80.4688, "hidden":true }
'''

# Find where to inject waypoints — right after STOPS_DATABASE opening brace
marker = 'var STOPS_DATABASE = window.STOPS_DATABASE = {'
idx = text.find(marker)
if idx < 0:
    print("ERROR: STOPS_DATABASE marker not found")
    exit(1)

insert_at = idx + len(marker)
text = text[:insert_at] + NEW_WAYPOINTS + text[insert_at:]
print("✓ Waypoints injected into STOPS_DATABASE")

# =============================================================================
# Now modify each route's stops array to include intermediate waypoints
# =============================================================================

def patch_route_stops(text, route_code, new_stops_list):
    """Replace the stops array for a given route code."""
    import re
    # Build new stops string
    new_stops_str = ',\n          '.join(f'"{s}"' for s in new_stops_list)
    
    # Pattern: match "ROUTE_CODE": { ... "stops": [ ... ] ... }
    pattern = r'("' + re.escape(route_code) + r'":\s*\{[^}]*?"stops":\s*\[)(.*?)(\])'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        text = text[:m.start(2)] + '\n          ' + new_stops_str + '\n        ' + text[m.end(2):]
        return text, True
    return text, False

# Map route code → enhanced stop sequence with intermediate waypoints
route_patches = {
    # ── ROUTE 116: KR Market → Gannavaram (NH16) ──────────────────────────────
    '116': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_rly_1', 'wp_pnbs_rly_2', 'wp_pnbs_rly_3',
        'railwaystn', 'wp_rly_sit_1', 'wp_rly_sit_2',
        'sitarampuram', 'wp_sit_mach_1', 'wp_sit_mach_2',
        'machavaram', 'wp_mach_gun_1', 'wp_mach_gun_2',
        'gunadala', 'wp_gun_ramv_1', 'wp_gun_ramv_2', 'wp_gun_ramv_3',
        'ramavarappadu', 'wp_ramv_enik_1', 'wp_ramv_enik_2', 'wp_ramv_enik_3',
        'enikepadu', 'wp_enik_nida_1',
        'nidamanuru', 'wp_nida_guda_1', 'wp_nida_guda_2',
        'gudavalli', 'wp_guda_kesr_1', 'wp_guda_kesr_2',
        'kesarapalli', 'wp_kesr_airp_1', 'wp_kesr_airp_2',
        'gannavaram_airport', 'wp_airp_gann_1', 'wp_airp_gann_2', 'wp_airp_gann_3',
        'gannavaram'
    ],

    # ── ROUTE 308: PNBS → Vissannapeta ───────────────────────────────────────
    '308': [
        'pnbs', 'wp_pnbs_chap_1',
        'challapalli_bungalow', 'wp_chap_buda_1',
        'budameru_bridge', 'wp_buda_paip_1', 'wp_buda_paip_2',
        'paipula_road', 'wp_paip_payk_1', 'wp_paip_payk_2',
        'payakapuram', 'wp_payk_nunn_1', 'wp_payk_nunn_2',
        'nunna', 'wp_nunn_nrih_1', 'wp_nunn_nrih_2', 'wp_nunn_nrih_3',
        'nri_college_sn', 'wp_agir_ravi_1',
        'agiripalli', 'wp_ravi_nuzv_1', 'wp_ravi_nuzv_2',
        'ravicherla_x', 'wp_nuzv_viss_1', 'wp_nuzv_viss_2',
        'nuzvid', 'vissannapeta'
    ],

    # ── ROUTE 16R: KR Market → Newrrpet ──────────────────────────────────────
    '16R': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_chap_1',
        'lenin_centre', 'wp_leni_elur_1',
        'eluru_locks', 'wp_elur_buda_1',
        'budameru_bridge', 'wp_buda_daba_1',
        'daba_kotlu', 'wp_daba_newrr_1',
        'newrrpet'
    ],

    # ── ROUTE 1: Ibrahimpatnam → Poranki ─────────────────────────────────────
    '1': [
        'ibrahimpatnam', 'wp_goll_ibra_3', 'wp_goll_ibra_2', 'wp_goll_ibra_1',
        'swathi_centre', 'wp_krm_bhav_3', 'wp_krm_bhav_2', 'wp_krm_bhav_1',
        'kummaripalem',
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_rly_1', 'wp_pnbs_rly_2', 'wp_pnbs_rly_3',
        'railwaystn', 'wp_pcr_igmc_1', 'wp_pcr_igmc_2',
        'pcr', 'wp_pcr_igmc_1', 'wp_pcr_igmc_2',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_auto_kam_1',
        'kamayyathopu', 'wp_kam_por_1', 'wp_kam_por_2',
        'poranki'
    ],

    # ── ROUTE 10: Railwaystn → Penamaluru ────────────────────────────────────
    '10': [
        'railwaystn', 'wp_pcr_igmc_1', 'wp_pcr_igmc_2',
        'pcr', 'wp_pcr_igmc_1', 'wp_pcr_igmc_2',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_auto_kan_1', 'wp_auto_kan_2',
        'kanuru', 'wp_kan_por_1',
        'poranki', 'wp_por_pen_1', 'wp_por_pen_2',
        'penamaluru'
    ],

    # ── ROUTE 20: Madhuranagar → Mangalagiri (via Varadhi) ───────────────────
    '20': [
        'madhuranagar', 'railway_new_colony', 'chittinagar',
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_vara_1', 'wp_pnbs_vara_2',
        'varadhi', 'wp_vara_tade_1', 'wp_vara_tade_2', 'wp_vara_tade_3',
        'tadepalli', 'wp_tade_mang_1', 'wp_tade_mang_2', 'wp_tade_mang_3',
        'nulakpet', 'dolasnagar', 'mangalagiri'
    ],

    # ── ROUTE 47V: Railwaystn → Mangalagiri (via Varadhi) ────────────────────
    '47V': [
        'railwaystn', 'wp_pnbs_rly_3', 'wp_pnbs_rly_2', 'wp_pnbs_rly_1',
        'pnbs', 'wp_pnbs_vara_1', 'wp_pnbs_vara_2',
        'varadhi', 'wp_vara_tade_1', 'wp_vara_tade_2', 'wp_vara_tade_3',
        'manipal_hospital',
        'mangalagiri'
    ],

    # ── ROUTE 47N: KR Market → Mangalagiri → NRI Hospital ────────────────────
    '47N': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_vara_1', 'wp_pnbs_vara_2',
        'varadhi', 'wp_vara_tade_1', 'wp_vara_tade_2', 'wp_vara_tade_3',
        'manipal_hospital',
        'mangalagiri', 'nrihospital'
    ],

    # ── ROUTE 47H: Railwaystn → Chinnakakani ─────────────────────────────────
    '47H': [
        'railwaystn', 'wp_pnbs_rly_3', 'wp_pnbs_rly_2', 'wp_pnbs_rly_1',
        'pnbs', 'wp_pnbs_vara_1', 'wp_pnbs_vara_2',
        'varadhi', 'wp_vara_tade_1', 'wp_vara_tade_2', 'wp_vara_tade_3',
        'manipal_hospital',
        'mangalagiri', 'chinnakakani'
    ],

    # ── ROUTE 188: Gannavaram → Kondapalli (via PNBS) ────────────────────────
    '188': [
        'gannavaram', 'wp_airp_gann_3', 'wp_airp_gann_2', 'wp_airp_gann_1',
        'gudavalli', 'wp_guda_kesr_2', 'wp_guda_kesr_1',
        'nidamanuru', 'wp_enik_nida_1',
        'ramavarappadu', 'wp_gun_ramv_3', 'wp_gun_ramv_2', 'wp_gun_ramv_1',
        'gunadala', 'wp_mach_gun_2', 'wp_mach_gun_1',
        'eluru_road',
        'wp_leni_elur_1', 'wp_krm_pnbs_3', 'wp_krm_pnbs_2',
        'pnbs', 'wp_krm_pnbs_3', 'wp_krm_pnbs_2', 'wp_krm_pnbs_1',
        'krmarket', 'wp_krm_bhav_1', 'wp_krm_bhav_2', 'wp_krm_bhav_3',
        'bhavanipuram', 'wp_goll_ibra_1', 'wp_goll_ibra_2', 'wp_goll_ibra_3',
        'ibrahimpatnam', 'wp_kond_pnbs_4', 'wp_kond_pnbs_3', 'wp_kond_pnbs_2', 'wp_kond_pnbs_1',
        'kondapalli'
    ],

    # ── ROUTE 3: Kabela → Govpress ────────────────────────────────────────────
    '3': [
        'kabela', 'wp_kabe_krm_1', 'wp_kabe_krm_2', 'wp_kabe_krm_3', 'wp_kabe_krm_4',
        'panja',
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'governorpet', 'wp_gov_pcr_1',
        'challapalli_bungalow', 'wp_chap_buda_1',
        'wp_leni_elur_1',
        'alankar_theatre', 'govpress'
    ],

    # ── ROUTE 144: Kondapalli → Autonagar ────────────────────────────────────
    '144': [
        'kondapalli', 'wp_kond_pnbs_1', 'wp_kond_pnbs_2', 'wp_kond_pnbs_3', 'wp_kond_pnbs_4',
        'pnbs', 'wp_pcr_igmc_2', 'wp_pcr_igmc_1',
        'pcr', 'wp_pcr_benz_1', 'wp_pcr_benz_2', 'wp_pcr_benz_3', 'wp_pcr_benz_4',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar'
    ],

    # ── ROUTE 140: KR Market → Uppuluru ──────────────────────────────────────
    '140': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'pcr', 'wp_pcr_gang_1', 'wp_pcr_gang_2',
        'ganguru', 'wp_gang_uppu_1', 'wp_gang_uppu_2', 'wp_gang_uppu_3', 'wp_gang_uppu_4', 'wp_gang_uppu_5',
        'uppuluru'
    ],

    # ── ROUTE 29: KR Market → Autonagar ──────────────────────────────────────
    '29': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'governorpet', 'wp_gov_pcr_1',
        'pcr', 'wp_pcr_igmc_1', 'wp_pcr_igmc_2',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar'
    ],

    # ── ROUTE 305M/350: PNBS → Ibrahimpatnam / west routes ──────────────────
    '305M': [
        'pnbs', 'wp_krm_pnbs_3', 'wp_krm_bhav_1', 'wp_krm_bhav_2', 'wp_krm_bhav_3',
        'bhavanipuram', 'wp_bhav_goll_1', 'wp_bhav_goll_2',
        'gollapudi', 'wp_goll_ibra_1', 'wp_goll_ibra_2', 'wp_goll_ibra_3',
        'ibrahimpatnam', 'jupudi', 'mulapadu', 'paritala',
        'kanchikacherla', 'moghuluru', 'veerulapadu'
    ],

    # ── ROUTE 2010: KR Market → Orugalla (via NH16) ──────────────────────────
    '2010': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_leni_elur_1',
        'eluru_road', 'wp_eluru_gun_1', 'wp_eluru_gun_2', 'wp_eluru_gun_3', 'wp_eluru_gun_4', 'wp_eluru_gun_5',
        'gunadala', 'wp_gun_ramv_1', 'wp_gun_ramv_2', 'wp_gun_ramv_3',
        'ramavarappadu', 'wp_ramv_enik_1', 'wp_ramv_enik_2', 'wp_ramv_enik_3',
        'enikepadu', 'wp_enik_nida_1',
        'gannavaram', 'orugalla'
    ],
}

patched_count = 0
for code, stops in route_patches.items():
    text, ok = patch_route_stops(text, code, stops)
    if ok:
        patched_count += 1
        print(f"  ✓ Route {code} patched ({len(stops)} stops incl. waypoints)")
    else:
        print(f"  ✗ Route {code} NOT found")

print(f"\n✓ {patched_count} routes patched with road waypoints")

# Write final file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print(f"Done. File size: {len(text)} bytes")
