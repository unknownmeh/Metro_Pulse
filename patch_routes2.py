import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def patch_route_stops(text, route_code, new_stops_list):
    new_stops_str = ',\n          '.join(f'"{s}"' for s in new_stops_list)
    pattern = r'("' + re.escape(route_code) + r'":\s*\{[^}]*?"stops":\s*\[)(.*?)(\])'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        # Only patch if it hasn't already been patched (check for waypoints)
        current = m.group(2)
        if 'wp_' in current:
            return text, False  # already patched
        text = text[:m.start(2)] + '\n          ' + new_stops_str + '\n        ' + text[m.end(2):]
        return text, True
    return text, False

route_patches2 = {
    # ── Routes sharing PCR→IGMC→Benz→Patamata→Autonagar corridor ────────────
    '10C': [
        'railwaystn', 'wp_pcr_igmc_2', 'wp_pcr_igmc_1',
        'pcr', 'wp_pcr_igmc_1', 'wp_pcr_igmc_2',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_auto_kan_1', 'wp_auto_kan_2',
        'kanuru', 'wp_kan_por_1',
        'poranki', 'chodavaram'
    ],
    '121': [
        'railwaystn', 'wp_pcr_igmc_2', 'wp_pcr_igmc_1',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_auto_kam_1',
        'kamayyathopu', 'wp_kam_por_1', 'wp_kam_por_2',
        'poranki', 'vanukuru'
    ],
    '122': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pcr_igmc_2', 'wp_pcr_igmc_1',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_auto_kam_1',
        'kamayyathopu', 'wp_kam_por_1', 'wp_kam_por_2',
        'poranki', 'vanukuru'
    ],
    '123': [
        'shabad',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_auto_kam_1',
        'kamayyathopu', 'wp_kam_por_1', 'wp_kam_por_2',
        'poranki', 'wp_por_pen_1', 'wp_por_pen_2',
        'penamaluru', 'kankipadu'
    ],
    '31': [
        'milkproject', 'wp_milk_krm_1', 'wp_milk_krm_2',
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'governorpet', 'wp_gov_pcr_1',
        'pcr', 'wp_pcr_igmc_1', 'wp_pcr_igmc_2',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar'
    ],
    '31A': [
        'milkproject', 'wp_milk_krm_1', 'wp_milk_krm_2',
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'governorpet', 'wp_gov_pcr_1',
        'pcr', 'wp_pcr_igmc_1', 'wp_pcr_igmc_2',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_auto_kam_1',
        'kamayyathopu', 'thadigadapa'
    ],
    '31H': [
        'hbcolony',
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'governorpet', 'wp_gov_pcr_1',
        'pcr', 'wp_pcr_igmc_1', 'wp_pcr_igmc_2',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar'
    ],
    '55': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'pcr', 'wp_pcr_benz_1', 'wp_pcr_benz_2', 'wp_pcr_benz_3', 'wp_pcr_benz_4',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_auto_kam_1',
        'kamayyathopu', 'wp_auto_kan_1', 'wp_auto_kan_2',
        'kanuru'
    ],
    '55S': [
        'railwaystn', 'wp_pnbs_rly_2', 'wp_pnbs_rly_1',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'pcr', 'wp_pcr_benz_1', 'wp_pcr_benz_2', 'wp_pcr_benz_3', 'wp_pcr_benz_4',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_auto_kam_1',
        'kamayyathopu', 'wp_auto_kan_1', 'wp_auto_kan_2',
        'kanuru'
    ],
    '49': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'governorpet', 'wp_gov_pcr_1',
        'pcr', 'wp_pcr_igmc_1', 'wp_pcr_igmc_2',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'kamayyathopu', 'yanamalakuduru'
    ],
    '5': [
        'kabela', 'wp_kabe_krm_1', 'wp_kabe_krm_2', 'wp_kabe_krm_3', 'wp_kabe_krm_4',
        'krmarket', 'wp_krm_tum_1',
        'tummalapalli', 'wp_tum_pnbs_1', 'wp_tum_pnbs_2',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'governorpet', 'nakkal_road', 'besant_road', 'pushpa_hotel',
        'ramesh_hospital', 'wp_igmc_benz_2', 'wp_igmc_benz_1',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar'
    ],
    '5G': [
        'krmarket', 'wp_krm_tum_1',
        'tummalapalli', 'wp_tum_pnbs_1', 'wp_tum_pnbs_2',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'governorpet', 'nakkal_road', 'besant_road', 'pushpa_hotel',
        'ramesh_hospital', 'gurunanak',
        'wp_benz_pat_1', 'wp_benz_pat_2',
        'autonagar'
    ],
    '5SG': [
        'railwaystn', 'wp_pnbs_rly_2', 'wp_pnbs_rly_1',
        'governorpet', 'nakkal_road', 'besant_road', 'pushpa_hotel',
        'ramesh_hospital', 'gurunanak',
        'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar'
    ],
    '141': [
        'krmarket', 'wp_krm_pnbs_2', 'wp_krm_pnbs_1',
        'railwaystn', 'wp_pnbs_rly_1', 'wp_pnbs_rly_2', 'wp_pnbs_rly_3',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'pcr', 'wp_pcr_gang_1', 'wp_pcr_gang_2',
        'ganguru', 'wp_gang_uppu_1', 'wp_gang_uppu_2', 'wp_gang_uppu_3', 'wp_gang_uppu_4', 'wp_gang_uppu_5',
        'uppuluru'
    ],
    '150': [
        'kondapalli', 'wp_kond_pnbs_1', 'wp_kond_pnbs_2', 'wp_kond_pnbs_3', 'wp_kond_pnbs_4',
        'pnbs', 'wp_pcr_igmc_2', 'wp_pcr_igmc_1',
        'pcr', 'wp_pcr_benz_1', 'wp_pcr_benz_2', 'wp_pcr_benz_3', 'wp_pcr_benz_4',
        'benzcircle', 'wp_benz_gang_1', 'wp_benz_gang_2', 'wp_benz_gang_3',
        'ganguru', 'wp_gang_uppu_1', 'wp_gang_uppu_2', 'wp_gang_uppu_3', 'wp_gang_uppu_4', 'wp_gang_uppu_5',
        'kankipadu'
    ],
    # ── Eluru Road / Machavaram corridor routes ───────────────────────────────
    '77': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_rly_1', 'wp_pnbs_rly_2', 'wp_pnbs_rly_3',
        'railwaystn', 'wp_rly_sit_1', 'wp_rly_sit_2',
        'eluru_road', 'wp_eluru_gun_1', 'wp_eluru_gun_2',
        'pushpa_hotel',
        'machavaram', 'wp_mach_gun_1', 'wp_mach_gun_2',
        'gunadala', 'wp_gun_ramv_1', 'wp_gun_ramv_2', 'wp_gun_ramv_3',
        'esi_hospital',
        'ramavarappadu'
    ],
    '77S': [
        'railwaystn', 'wp_rly_sit_1', 'wp_rly_sit_2',
        'eluru_road', 'wp_eluru_gun_1', 'wp_eluru_gun_2', 'wp_eluru_gun_3', 'wp_eluru_gun_4', 'wp_eluru_gun_5',
        'ramavarappadu'
    ],
    '79E': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_rly_1', 'wp_pnbs_rly_2', 'wp_pnbs_rly_3',
        'railwaystn', 'wp_rly_sit_1', 'wp_rly_sit_2',
        'eluru_road', 'wp_eluru_gun_1', 'wp_eluru_gun_2',
        'machavaram', 'wp_mach_gun_1', 'wp_mach_gun_2',
        'gunadala', 'wp_gun_ramv_1', 'wp_gun_ramv_2', 'wp_gun_ramv_3',
        'ramavarappadu', 'wp_ramv_enik_1', 'wp_ramv_enik_2', 'wp_ramv_enik_3',
        'srk_college',
        'nidamanuru'
    ],
    '201C': [
        'peddaoutpalli', 'gannavaram',
        'wp_airp_gann_3', 'wp_airp_gann_2', 'wp_airp_gann_1',
        'gudavalli', 'wp_nida_guda_2', 'wp_nida_guda_1',
        'nidamanuru', 'wp_enik_nida_1',
        'ramavarappadu', 'wp_gun_ramv_3', 'wp_gun_ramv_2', 'wp_gun_ramv_1',
        'gunadala', 'wp_eluru_gun_2', 'wp_eluru_gun_1',
        'eluru_road', 'wp_leni_elur_1',
        'challapalli_bungalow', 'wp_pnbs_chap_1',
        'pnbs', 'wp_krm_pnbs_3', 'wp_krm_pnbs_2', 'wp_krm_pnbs_1',
        'krmarket'
    ],
    '201T': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_leni_elur_1',
        'eluru_road', 'wp_eluru_gun_1', 'wp_eluru_gun_2', 'wp_eluru_gun_3', 'wp_eluru_gun_4', 'wp_eluru_gun_5',
        'gunadala', 'wp_gun_ramv_1', 'wp_gun_ramv_2', 'wp_gun_ramv_3',
        'ramavarappadu', 'wp_ramv_enik_1', 'wp_ramv_enik_2', 'wp_ramv_enik_3',
        'enikepadu', 'wp_enik_nida_1',
        'gannavaram', 'telaprolu'
    ],
    '203C': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_leni_elur_1',
        'eluru_road', 'wp_eluru_gun_1', 'wp_eluru_gun_2', 'wp_eluru_gun_3', 'wp_eluru_gun_4', 'wp_eluru_gun_5',
        'gunadala', 'wp_gun_ramv_1', 'wp_gun_ramv_2', 'wp_gun_ramv_3',
        'ramavarappadu', 'wp_ramv_enik_1', 'wp_ramv_enik_2', 'wp_ramv_enik_3',
        'enikepadu', 'wp_enik_nida_1',
        'gannavaram', 'prodduturu'
    ],
    '203T': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_leni_elur_1',
        'eluru_road', 'wp_eluru_gun_1', 'wp_eluru_gun_2', 'wp_eluru_gun_3', 'wp_eluru_gun_4', 'wp_eluru_gun_5',
        'gunadala', 'wp_gun_ramv_1', 'wp_gun_ramv_2', 'wp_gun_ramv_3',
        'ramavarappadu', 'wp_ramv_enik_1', 'wp_ramv_enik_2', 'wp_ramv_enik_3',
        'enikepadu', 'wp_enik_nida_1',
        'nidamanuru', 'wp_nida_guda_1', 'wp_nida_guda_2',
        'gudavalli', 'manthena', 'tenneru'
    ],
    '208': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_buda_paip_1',
        'ajit_singh_nagar',
        'paipula_road', 'wp_paip_payk_1', 'wp_paip_payk_2',
        'nunna', 'wp_nunn_nrih_1', 'wp_nunn_nrih_2',
        'surampalli', 'wp_agir_ravi_1',
        'agiripalli'
    ],
    '209': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pcr_benz_3', 'wp_pcr_benz_4',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_benz_gang_1', 'wp_benz_gang_2', 'wp_benz_gang_3',
        'ganguru', 'thadigadapa',
        'poranki', 'wp_por_pen_1', 'wp_por_pen_2',
        'penamaluru', 'gosala',
        'kankipadu', 'chinapulipaka', 'prodduturu', 'vallurupalem'
    ],
    '222': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'pcr', 'wp_pcr_benz_1', 'wp_pcr_benz_2', 'wp_pcr_benz_3', 'wp_pcr_benz_4',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_auto_kam_1',
        'kamayyathopu', 'wp_kam_por_1', 'wp_kam_por_2',
        'poranki', 'gosala', 'kankipadu', 'aakunuru', 'vuyyuru'
    ],
    '333': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_chap_1',
        'challapalli_bungalow', 'siddhartha_college',
        'ramesh_hospital', 'wp_igmc_benz_2', 'wp_igmc_benz_1',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'autonagar', 'wp_kam_por_1', 'wp_kam_por_2',
        'poranki', 'wp_por_pen_1', 'wp_por_pen_2',
        'penamaluru', 'kankipadu', 'vuyyuru', 'pamarru'
    ],
    # ── 116K: KR Market → Kankipadu ──────────────────────────────────────────
    '116K': [
        'krmarket', 'wp_krm_pnbs_2', 'wp_krm_pnbs_1',
        'railwaystn', 'wp_pcr_igmc_2', 'wp_pcr_igmc_1',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_auto_kam_1',
        'kamayyathopu', 'thadigadapa', 'wp_kan_por_1',
        'poranki', 'kankipadu'
    ],
    # ── 1G: Gollapudi → Kankipadu ─────────────────────────────────────────────
    '1G': [
        'gollapudi', 'wp_bhav_goll_2', 'wp_bhav_goll_1',
        'kummaripalem', 'wp_krm_bhav_3', 'wp_krm_bhav_2', 'wp_krm_bhav_1',
        'bhavanipuram', 'wp_pnbs_rly_3', 'wp_pnbs_rly_2', 'wp_pnbs_rly_1',
        'railwaystn', 'wp_pcr_igmc_2', 'wp_pcr_igmc_1',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_auto_kan_1', 'wp_auto_kan_2',
        'kanuru', 'wp_kan_por_1',
        'poranki', 'kankipadu'
    ],
    # ── Route 2 long: KR Market → Ramavarappadu ───────────────────────────────
    '2': [
        'krmarket', 'wp_krm_tum_1',
        'tummalapalli', 'wp_tum_pnbs_1', 'wp_tum_pnbs_2',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'governorpet', 'wp_gov_pcr_1',
        'challapalli_bungalow', 'wp_chap_buda_1',
        'wp_leni_elur_1',
        'besant_road', 'rama_mandiram', 'vijaya_talkies', 'kotha_vantena',
        'sitarampuram', 'wp_sit_mach_1', 'wp_sit_mach_2',
        'chuttugunta', 'maruthi_nagar',
        'srr_college', 'anjaneya_temple',
        'machavaram', 'wp_mach_gun_1', 'wp_mach_gun_2',
        'padavala_revu', 'gunadala_church',
        'gunadala', 'wp_gun_ramv_1', 'wp_gun_ramv_2', 'wp_gun_ramv_3',
        'gunadala_vantena', 'esi_hospital', 'power_office',
        'ramavarappadu'
    ],
    # ── Route 350: PNBS → Mailavaram ──────────────────────────────────────────
    '350': [
        'pnbs', 'wp_krm_bhav_1', 'wp_krm_bhav_2', 'wp_krm_bhav_3',
        'bhavanipuram', 'wp_bhav_goll_1', 'wp_bhav_goll_2',
        'guntupalli', 'wp_goll_ibra_1', 'wp_goll_ibra_2', 'wp_goll_ibra_3',
        'ibrahimpatnam', 'kondapalli',
        'jupudi', 'cheruvu_madhavaram', 'konduru', 'pulluru', 'mailavaram'
    ],
    # ── Route 154 / 7A: KR Market → PCR → ... ────────────────────────────────
    '154': [
        'krmarket', 'wp_krm_pcr_1', 'wp_krm_pcr_2', 'wp_krm_pcr_3',
        'pcr', 'wp_pcr_gang_1', 'wp_pcr_gang_2',
        'kankipadu'
    ],
    '7A': [
        'krmarket', 'wp_krm_pcr_1', 'wp_krm_pcr_2', 'wp_krm_pcr_3',
        'pcr', 'wp_pcr_igmc_1', 'wp_pcr_igmc_2',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'peddapulipaka'
    ],
    '7R': [
        'milkproject', 'wp_milk_krm_1', 'wp_milk_krm_2',
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'governorpet', 'wp_gov_pcr_1',
        'pcr', 'wp_pcr_igmc_1', 'wp_pcr_igmc_2',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'yanamalakuduru'
    ],
    '7ST': [
        'railwaystn', 'wp_pcr_igmc_2', 'wp_pcr_igmc_1',
        'pcr', 'wp_pcr_igmc_1', 'wp_pcr_igmc_2',
        'igmc_stadium', 'wp_igmc_benz_1', 'wp_igmc_benz_2',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'thadigadapa'
    ],
    '79B': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'pcr', 'wp_pat_auto_2', 'wp_pat_auto_1',
        'autonagar', 'thadigadapa',
        'poranki'
    ],
    # ── Route 99: Railwaystn → Kankipadu ─────────────────────────────────────
    '99': [
        'railwaystn', 'satyanarayanapuram', 'govpress',
        'ramavarappadu', 'wp_gun_ramv_3', 'wp_gun_ramv_2', 'wp_gun_ramv_1',
        'wp_igmc_benz_2', 'wp_igmc_benz_1',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'wp_kam_por_1', 'wp_kam_por_2',
        'poranki', 'wp_por_pen_1', 'wp_por_pen_2',
        'penamaluru', 'edupugallu', 'gosala', 'kankipadu'
    ],
    # ── Route 48K/48N/48V: Autonagar ↔ Kundavari (Eluru Road) ────────────────
    '48K': [
        'kundavari', 'paipula_road', 'wp_buda_paip_2', 'wp_buda_paip_1',
        'daba_kotlu', 'wp_elur_buda_1',
        'ajit_singh_nagar', 'eluru_locks', 'wp_leni_elur_1',
        'challapalli_bungalow', 'wp_pnbs_chap_1',
        'raghavaiah_park',
        'pcr', 'wp_pcr_benz_1', 'wp_pcr_benz_2', 'wp_pcr_benz_3', 'wp_pcr_benz_4',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar'
    ],
    '48N': [
        'autonagar', 'wp_pat_auto_2', 'wp_pat_auto_1',
        'patamata', 'wp_benz_pat_2', 'wp_benz_pat_1',
        'benzcircle', 'wp_pcr_benz_4', 'wp_pcr_benz_3', 'wp_pcr_benz_2', 'wp_pcr_benz_1',
        'pcr', 'raghavaiah_park', 'wp_pnbs_chap_1',
        'challapalli_bungalow', 'wp_leni_elur_1',
        'eluru_locks', 'ajit_singh_nagar', 'wp_elur_buda_1',
        'wp_buda_paip_1', 'wp_buda_paip_2',
        'paipula_road', 'nunna'
    ],
    '48V': [
        'autonagar', 'wp_pat_auto_2', 'wp_pat_auto_1',
        'patamata', 'wp_benz_pat_2', 'wp_benz_pat_1',
        'benzcircle', 'wp_pcr_benz_4', 'wp_pcr_benz_3', 'wp_pcr_benz_2', 'wp_pcr_benz_1',
        'pcr', 'raghavaiah_park', 'wp_pnbs_chap_1',
        'challapalli_bungalow', 'wp_leni_elur_1',
        'eluru_locks', 'ajit_singh_nagar', 'wp_elur_buda_1',
        'wp_buda_paip_1', 'wp_buda_paip_2',
        'paipula_road', 'vombaycolony'
    ],
    '49M': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_gov_1', 'wp_pnbs_gov_2', 'wp_pnbs_gov_3',
        'governorpet', 'wp_leni_elur_1',
        'eluru_locks', 'ajit_singh_nagar', 'wp_buda_paip_1', 'wp_buda_paip_2',
        'paipula_road', 'wp_paip_payk_1', 'wp_paip_payk_2',
        'nunna', 'managalapuram'
    ],
    '2K': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'raghavaiah_park',
        'igmc_stadium', 'pvp_square', 'kanthaari',
        'benzcircle', 'wp_benz_pat_1', 'wp_benz_pat_2',
        'ntr_circle', 'patamata', 'wp_pat_auto_1', 'wp_pat_auto_2',
        'autonagar', 'wp_auto_kan_1', 'wp_auto_kan_2',
        'kanuru'
    ],
    '112A': [
        'krmarket', 'wp_krm_pnbs_1', 'wp_krm_pnbs_2', 'wp_krm_pnbs_3',
        'pnbs', 'wp_pnbs_rly_1', 'wp_pnbs_rly_2', 'wp_pnbs_rly_3',
        'railwaystn', 'wp_rly_sit_1', 'wp_rly_sit_2',
        'eluru_locks', 'wp_buda_paip_1',
        'ajit_singh_nagar', 'wp_paip_payk_1', 'wp_paip_payk_2',
        'nunna', 'musthabadh'
    ],
}

patched_count = 0
for code, stops in route_patches2.items():
    text, ok = patch_route_stops(text, code, stops)
    if ok:
        patched_count += 1
        print(f"  ✓ Route {code} patched ({len(stops)} stops)")
    else:
        print(f"  - Route {code} skipped (already patched or not found)")

print(f"\n✓ {patched_count} additional routes patched")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print(f"Done. File size: {len(text)} bytes")
