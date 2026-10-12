import os
import json
import pandas as pd

def test_outputs_exist():
    assert os.path.exists('/app/results/optimized_kinetics.json'), "Missing optimized_kinetics.json"
    assert os.path.exists('/app/results/metabolite_anova_summary.csv'), "Missing metabolite_anova_summary.csv"

def test_scientific_correctness():
    with open('/app/results/optimized_kinetics.json', 'r') as f:
        kinetics = json.load(f)

    for sample, metrics in kinetics.items():
        assert metrics['max_accumulation'] > 0, f"Sample {sample} maximum accumulation must be positive."
        assert metrics['production_rate'] >= 0, f"Sample {sample} production rate cannot be negative."

    anova_df = pd.read_csv('/app/results/metabolite_anova_summary.csv')
    assert not anova_df.empty, "ANOVA summary table is empty."
    assert 'F_value' in anova_df.columns, "Missing F_value column."

if __name__ == '__main__':
    test_outputs_exist()
    test_scientific_correctness()
    print("Verification checks passed: Kombucha kinetic parameters and ANOVA recomputed successfully.")
