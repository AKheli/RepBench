from collections import defaultdict

IMR = "imr"
SCREEN = "screen"
RPCA = "rpca"
Robust_PCA = RPCA
CDREC = "cdrec"
WindowRPCA = "wrpca"
SCREEN_GLOBAL = "screenglobal"


ALGORITHM_TYPES = [IMR,SCREEN,RPCA,CDREC]#,WindowRPCA,SCREEN_GLOBAL]

#black is used for the truth, and red for anomalies
ALGORITHM_COLORS = {IMR : "blue" , SCREEN : "purple" , RPCA : "green" , CDREC : "orange",}
ALGORITHM_COLORS = defaultdict(lambda: 'cyan', ALGORITHM_COLORS )