from collections import defaultdict

IMR = "imr"
SCREEN = "screen"
RPCA = "rpca"
Robust_PCA = RPCA
CDREC = "cdrec"
WindowRPCA = "wrpca"
SCREEN_GLOBAL = "screen_global"
SCREEN_l = "screen_5_95"
SCREEN_l2 = "screen_10_90"

ALGORITHM_TYPES = [IMR,SCREEN,RPCA,CDREC]#,SCREEN_l,SCREEN_l2]#,SCREEN_GLOBAL]

#black is used for the truth, and red for anomalies
ALGORITHM_COLORS = {IMR : "blue" , SCREEN : "purple" , RPCA : "green" , CDREC : "orange",}
ALGORITHM_COLORS = defaultdict(lambda: 'cyan', ALGORITHM_COLORS )




