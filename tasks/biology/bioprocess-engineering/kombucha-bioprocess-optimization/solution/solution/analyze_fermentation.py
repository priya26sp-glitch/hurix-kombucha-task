import json
import os
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import statsmodels.api as sm
from statsmodels.formula.api import ols

# 1. Load data from absolute path
df = pd.read_csv('/app/data/fermentation_time_course.csv')

# 2. Clean data & handle missing points
cleaned_df = df.dropna(subset=['day', 'sample_type', 'ph', 'acetic_acid', 'dpph_antioxidant']).copy()

# 3. Kinetic modeling for acetic acid accumulation kinetics
results_dict = {}
for stype, group in cleaned_df.groupby('sample_type'):
    days = group['day'].values
    acid = group['acetic_acid'].values

    try:
        def acid_model(t, max_val, rate):
            return max_val / (1 + np.exp(-rate * (t - 3.0)))

        popt, _ = curve_fit(acid_model, days, acid, p0=[4.5, 0.5], maxfev=5000)
        results_dict[stype] = {
            "max_accumulation": float(popt[0]),
            "production_rate": float(popt[1])
        }
    except Exception:
        results_dict[stype] = {
            "max_accumulation": float(acid.max()),
            "production_rate": 0.0
        }

# 4. ANOVA analysis for antioxidant activity across days and sample types
anova_model = ols('dpph_antioxidant ~ C(sample_type) + C(day)', data=cleaned_df).fit()
anova_table = sm.stats.anova_lm(anova_model, typ=2)

# 5. Save outputs to required absolute paths
os.makedirs('/app/results', exist_ok=True)
with open('/app/results/optimized_kinetics.json', 'w') as f:
    json.dump(results_dict, f, indent=4)

anova_summary = pd.DataFrame({
    'factor': anova_table.index,
    'F_value': anova_table['F'].values,
    'PR_('>F')': anova_table['PR(>F)'].values
})
anova_summary.to_csv('/app/results/metabolite_anova_summary.csv', index=False)

print("Kombucha bioprocess analysis complete.")
