"""
Alveolar-Capillary Gas Diffusion (DLCO) & Membrane Conductance Engine.
Provides deterministic, zero-dependency modeling of carbon monoxide diffusing capacity (DLCO),
hemoglobin normalization, alveolar volume (VA) ratio, and pulmonary diffusion resilience.
"""

from typing import Dict, Any, List, Optional


class AlveolarCapillaryDiffusionClient:
    """
    Deterministic client for calculating DLCO lung diffusing capacity and hemoglobin adjustments.
    Pure Python standard library implementation based on ATS/ERS Pulmonary Function Standards.
    """

    def __init__(self):
        pass

    def evaluate_dlco_diffusion(
        self,
        measured_dlco_ml_min_mmhg: float,
        predicted_dlco_ml_min_mmhg: float,
        hemoglobin_g_dl: float = 14.5,
        is_female: bool = False,
        alveolar_volume_liters: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Evaluates DLCO pulmonary diffusing capacity:
        - Adjusts for circulating hemoglobin concentration using standard ATS/ERS formulas.
        - Calculates % predicted DLCO.
        - Computes KCO (Transfer coefficient = DLCO / VA) if VA provided.
        - Scores Pulmonary Diffusion Resilience Score (PDRS, 0-100).
        """
        if measured_dlco_ml_min_mmhg <= 0 or predicted_dlco_ml_min_mmhg <= 0 or hemoglobin_g_dl <= 3.0:
            return {"error": "Invalid physiological values: DLCO and hemoglobin must be positive"}

        # Dinakara / Cotes hemoglobin correction factor:
        # Men: Factor = (10.22 + Hb) / (1.7 * Hb)
        # Women: Factor = (9.38 + Hb) / (1.7 * Hb)
        if is_female:
            hb_factor = (9.38 + hemoglobin_g_dl) / (1.7 * hemoglobin_g_dl)
        else:
            hb_factor = (10.22 + hemoglobin_g_dl) / (1.7 * hemoglobin_g_dl)

        adjusted_dlco = round(measured_dlco_ml_min_mmhg * hb_factor, 2)
        pct_predicted = round((adjusted_dlco / predicted_dlco_ml_min_mmhg) * 100.0, 1)

        # Transfer coefficient KCO (DLCO / VA in mL/min/mmHg/L)
        kco = round(adjusted_dlco / alveolar_volume_liters, 2) if alveolar_volume_liters and alveolar_volume_liters > 0 else None

        # Pulmonary Diffusion Resilience Score (PDRS, 0 - 100):
        # 100% predicted -> ~85-95 score. >= 80% is clinically normal.
        if pct_predicted >= 80.0:
            pdrs = min(100.0, 75.0 + ((pct_predicted - 80.0) / 20.0) * 20.0)
        elif pct_predicted >= 60.0:
            pdrs = 50.0 + ((pct_predicted - 60.0) / 20.0) * 25.0
        elif pct_predicted >= 40.0:
            pdrs = 25.0 + ((pct_predicted - 40.0) / 20.0) * 25.0
        else:
            pdrs = max(5.0, (pct_predicted / 40.0) * 25.0)

        pdrs_score = round(pdrs, 1)

        if pct_predicted >= 80.0:
            severity = "NORMAL_PULMONARY_DIFFUSION"
            interpretation = f"Normal alveolar-capillary membrane gas exchange ({pct_predicted}% of predicted); erythrocyte transit time is well matched to diffusion capacity."
            guidance = "Gas exchange reserve is optimal. Full capacity for high-altitude aerobic exertion."
        elif pct_predicted >= 60.0:
            severity = "MILD_DIFFUSION_LIMITATION"
            interpretation = f"Mildly reduced DLCO ({pct_predicted}% of predicted); subtle alveolar membrane thickening or minor capillary volume loss."
            guidance = "Monitor during maximal aerobic exertion; ensure adequate warm-up and avoid air pollution / smoke exposure."
        elif pct_predicted >= 40.0:
            severity = "MODERATE_DIFFUSION_IMPAIRMENT"
            interpretation = f"Moderate reduction in gas diffusion ({pct_predicted}% of predicted); potential interstitial or pulmonary vascular involvement."
            guidance = "Exercise-induced desaturation likely at high intensities. Formal clinical spirometry review indicated."
        else:
            severity = "SEVERE_GAS_TRANSFER_DEFICIT"
            interpretation = f"Critically impaired alveolar gas exchange ({pct_predicted}% of predicted); high risk of resting or exertional hypoxemia."
            guidance = "Urgent pulmonary medicine evaluation recommended; limit strenuous physical strain."

        return {
            "measured_dlco_ml_min_mmhg": measured_dlco_ml_min_mmhg,
            "predicted_dlco_ml_min_mmhg": predicted_dlco_ml_min_mmhg,
            "hemoglobin_g_dl": hemoglobin_g_dl,
            "hb_correction_factor": round(hb_factor, 3),
            "adjusted_dlco_ml_min_mmhg": adjusted_dlco,
            "pct_predicted_dlco": pct_predicted,
            "transfer_coefficient_kco": kco,
            "pulmonary_diffusion_score": pdrs_score,
            "clinical_severity": severity,
            "physiological_interpretation": interpretation,
            "actionable_guidance": guidance
        }
