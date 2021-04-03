edge_4 = {
    'TFL_1' : ['gneE8', 'gneE10', 'gneE12', 'gneE14']
}
nextEdge_4 = {
    'TFL_1' : ['-gneE14_1','-gneE12_0','-gneE8_1','-gneE14_0','-gneE10_1','-gneE8_0','-gneE12_1','-gneE10_0']
}
maxWT_4 = 90
satFR_16 = 1500

edge_16 = {
    'TFL_1' : ['InB_WN_2', 'InB_NW_2', 'Mid_N_2', 'Mid_W_1'],
    'TFL_2' : ['Mid_N_1', 'InB_NE_2', 'InB_EN_2', 'Mid_E_1'],
    'TFL_3' : ['Mid_S_1', 'Mid_E_2', 'InB_ES_2', 'InB_SE_2'],
    'TFL_4' : ['InB_WS_2', 'Mid_W_2', 'Mid_S_2', 'InB_SW_2']
}
nextEdge_16 = {
    'TFL_1' : ['Mid_W_2_1','Mid_N_1_0','OutB_WN_2_1','Mid_W_2_0','OutB_NW_2_1','OutB_WN_2_0','Mid_N_1_1','OutB_NW_2_0'],
    'TFL_2' : ['Mid_E_2_1','OutB_EN_2_0','Mid_N_2_1','Mid_E_2_0','OutB_NE_2_1','Mid_N_2_0','OutB_EN_2_1','OutB_NE_2_0'],
    'TFL_3' : ['OutB_SE_2_1','OutB_ES_2_0','Mid_S_2_1','OutB_SE_2_0','Mid_E_1_1','Mid_S_2_0','OutB_ES_2_1','Mid_E_1_0'],
    'TFL_4' : ['OutB_SW_2_1','Mid_S_1_0','OutB_WS_2_1','OutB_SW_2_0','Mid_W_1_1','OutB_WS_2_0','Mid_S_1_1','Mid_W_1_0']   
}

maxWT_16 = 90 # peak WT fix rou1
satFR_16 = 4000 # peak FR fix rou1

edge_36 = {
    'TFL_1' : ['InB_WN_2', 'InB_NW_2', 'Mid_NW_2', 'Mid_WN_1'],
    'TFL_2' : ['Mid_NW_1', 'InB_NM_2', 'Mid_NE_2', 'Mid_N_1'],
    'TFL_3' : ['Mid_NE_1', 'InB_NE_2', 'InB_EN_2', 'Mid_EN_1'],
    'TFL_4' : ['InB_WM_2', 'Mid_WN_2', 'Mid_W_2', 'Mid_WS_1'],
    'TFL_5' : ['Mid_W_1', 'Mid_N_2', 'Mid_E_2', 'Mid_S_1'],
    'TFL_6' : ['Mid_E_1', 'Mid_EN_2', 'InB_EM_2', 'Mid_ES_1'],
    'TFL_7' : ['InB_WS_2', 'Mid_WS_2', 'Mid_SW_2', 'InB_SW_2'],
    'TFL_8' : ['Mid_SW_1', 'Mid_S_2', 'Mid_SE_2', 'InB_SM_2'],
    'TFL_9' : ['Mid_SE_1', 'Mid_ES_2', 'InB_ES_2', 'InB_SE_2']
}

nextEdge_36 = {
    'TFL_1' : ['Mid_NW_1_1','Mid_NW_1_0','Mid_WN_2_1','Mid_WN_2_0','OutB_WN_2_1','OutB_WN_2_0','OutB_NW_2_1','OutB_NW_2_0'],
    'TFL_2' : ['Mid_NE_1_1','Mid_NE_1_0','Mid_N_2_1','Mid_N_2_0','Mid_NW_2_1','Mid_NW_2_0','OutB_NM_2_1','OutB_NM_2_0'],
    'TFL_3' : ['OutB_EN_2_1','OutB_EN_2_0','Mid_EN_2_1','Mid_EN_2_0','Mid_NE_2_1','Mid_NE_2_0','OutB_NE_2_1','OutB_NE_2_0'],
    'TFL_4' : ['Mid_W_1_1','Mid_W_1_0','Mid_WS_2_1','Mid_WS_2_0','OutB_WM_2_1','OutB_WM_2_0','Mid_WN_1_1','Mid_WN_1_0'],
    'TFL_5' : ['Mid_E_1_1', 'Mid_E_1_0', 'Mid_S_2_1', 'Mid_S_2_0','Mid_W_2_1','Mid_W_2_0','Mid_N_1_1','Mid_N_1_0'],
    'TFL_6' : ['OutB_EM_2_1', 'OutB_EM_2_0', 'Mid_ES_2_1', 'Mid_ES_2_0','Mid_E_2_1','Mid_E_2_0','Mid_EN_1_1','Mid_EN_1_0'],
    'TFL_7' : ['Mid_SW_1_1', 'Mid_SW_1_0', 'OutB_SW_2_1', 'OutB_SW_2_0','OutB_WS_2_1','OutB_WS_2_0','Mid_WS_1_1','Mid_WS_1_0'],
    'TFL_8' : ['MID_SE_1_1', 'MID_SE_1_0', 'OutB_SM_2_1', 'OutB_SM_2_0','Mid_SW_2_1','Mid_SW_2_0','Mid_S_1_1','Mid_S_1_0'],
    'TFL_9' : ['OutB_ES_2_1', 'OutB_ES_2_0', 'OutB_SE_2_1', 'OutB_SE_2_0','MID_SE_2_1','MID_SE_2_0','Mid_ES_1_1','Mid_ES_1_0'] 
}

maxWT_36 = 180
avgSPD_36 = 31.03
avgDEN_36 = 14.7
