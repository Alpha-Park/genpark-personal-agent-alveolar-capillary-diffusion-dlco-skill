---
name: genpark-personal-agent-alveolar-capillary-diffusion-dlco-skill
description: Deterministic evaluation of diffusing capacity of the lung for carbon monoxide (DLCO), hemoglobin adjustment, transfer coefficient (KCO), and alveolar gas exchange.
version: 1.0.0
author: GenPark Autonomous Agents Ecosystem
license: MIT
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
---

# Alveolar-Capillary Gas Diffusion (DLCO) Skill

## Overview
The `genpark-personal-agent-alveolar-capillary-diffusion-dlco-skill` brings clinical pulmonary gas exchange analytics to sovereign personal agents. The diffusing capacity of the lung for carbon monoxide (DLCO / $T_LCO$) measures the rate at which gas molecules cross from alveolar air spaces across the thin alveolar-capillary membrane into red blood cells to bind with hemoglobin. Factoring in circulating hemoglobin concentration and alveolar volume ($V_A$), this skill computes percentage of predicted transfer, transfer coefficient ($KCO$), and pulmonary diffusion resilience.

## Physiological Model & Mathematics
1. **Dinakara / Cotes Hemoglobin Normalization**:
   $$\text{Factor}_{\text{male}} = \frac{10.22 + Hb}{1.7 \cdot Hb}, \quad \text{Factor}_{\text{female}} = \frac{9.38 + Hb}{1.7 \cdot Hb}$$
   $$DLCO_{\text{adj}} = DLCO_{\text{measured}} \times \text{Factor}$$
2. **Percentage of Predicted DLCO**:
   $$\%DLCO_{\text{pred}} = \frac{DLCO_{\text{adj}}}{DLCO_{\text{predicted}}} \times 100\%$$
   - **Normal Gas Diffusion**: $\ge 80\%$.
   - **Mild Reduction**: $60 - 79\%$.
   - **Moderate Impairment**: $40 - 59\%$.
   - **Severe Transfer Deficit**: $< 40\%$.
3. **Transfer Coefficient ($KCO$)**:
   $$KCO = \frac{DLCO_{\text{adj}}}{V_A} \quad (\text{mL/min/mmHg/L})$$
4. **Pulmonary Diffusion Resilience Score ($PDRS$)**:
   Standardized 0 to 100 score mapping respiratory gas exchange reserve.

## Tools & Endpoints
- `evaluate_dlco_diffusion`: Calculates hemoglobin-adjusted DLCO, % of predicted, transfer coefficient $KCO$, and diffusion resilience score.
