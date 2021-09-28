from injection.agots.multivariate_generators.multivariate_variance_outlier_generator import \
    MultivariateVarianceOutlierGenerator

import pandas as pd
import numpy as np
gen = MultivariateVarianceOutlierGenerator([(3,90)])

ser = pd.Series(np.arange(100)+10)

x = gen.add_outliers(ser)