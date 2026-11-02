"""
Example usage for Alveolar-Capillary Gas Diffusion (DLCO) Skill.
Demonstrates analyzing single-breath carbon monoxide diffusing capacity.
"""

from client import AlveolarCapillaryDiffusionClient


def main():
    client = AlveolarCapillaryDiffusionClient()

    print("=== 1. Evaluating DLCO Gas Transfer (Male Athlete, Hb = 15.0 g/dL) ===")
    res = client.evaluate_dlco_diffusion(
        measured_dlco_ml_min_mmhg=28.2,
        predicted_dlco_ml_min_mmhg=30.0,
        hemoglobin_g_dl=15.0,
        is_female=False,
        alveolar_volume_liters=6.2
    )

    print(f"Measured DLCO: {res['measured_dlco_ml_min_mmhg']} mL/min/mmHg")
    print(f"Hb Correction Factor: {res['hb_correction_factor']}x")
    print(f"Adjusted DLCO: {res['adjusted_dlco_ml_min_mmhg']} mL/min/mmHg")
    print(f"% Predicted DLCO: {res['pct_predicted_dlco']} % (Normative: >= 80%)")
    print(f"Transfer Coefficient KCO: {res['transfer_coefficient_kco']} mL/min/mmHg/L")
    print(f"Pulmonary Diffusion Score: {res['pulmonary_diffusion_score']} / 100")
    print(f"Severity: {res['clinical_severity']}")
    print(f"Interpretation: {res['physiological_interpretation']}")
    print(f"Guidance: {res['actionable_guidance']}")


if __name__ == "__main__":
    main()
