# Alveolar-Capillary Gas Diffusion (DLCO) Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](https://github.com/alphaparkinc/genpark-personal-agent-alveolar-capillary-diffusion-dlco-skill)
[![OpenClaw Ready](https://img.shields.io/badge/OpenClaw-Compatible-purple.svg)](https://github.com/alphaparkinc/genpark-personal-agent-alveolar-capillary-diffusion-dlco-skill)
[![MCP Protocol](https://img.shields.io/badge/MCP-Standard-orange.svg)](https://modelcontextprotocol.io/)

A sovereign personal agent capability for computational pulmonary physiology, evaluating single-breath diffusing capacity of the lung for carbon monoxide (DLCO), hemoglobin normalization, and transfer coefficient (KCO).

## Architecture

```mermaid
flowchart TD
    DiffusionInputs["DLCO Measured (mL/min/mmHg), Predicted DLCO, Hemoglobin (g/dL)"] --> HbCorrection["Dinakara/Cotes Hemoglobin Normalization Factor"]
    HbCorrection --> AdjustedDLCO["Hemoglobin-Adjusted DLCO (mL/min/mmHg)"]
    AdjustedDLCO --> PredictedPercent["Percentage of Predicted DLCO (% Predicted)"]
    AdjustedDLCO --> KCOEngine["Transfer Coefficient KCO = Adjusted DLCO / Alveolar Volume (VA)"]
    PredictedPercent & KCOEngine --> PDRS["Pulmonary Diffusion Resilience Score (0 - 100)"]
    PDRS --> Directives["OpenClaw / Hermes Altitude & Cardiorespiratory Directives"]
```

## Quickstart

```python
from client import AlveolarCapillaryDiffusionClient

client = AlveolarCapillaryDiffusionClient()

# Assess DLCO pulmonary gas exchange
res = client.evaluate_dlco_diffusion(
    measured_dlco_ml_min_mmhg=28.2,
    predicted_dlco_ml_min_mmhg=30.0,
    hemoglobin_g_dl=15.0,
    is_female=False,
    alveolar_volume_liters=6.2
)

print("Adjusted DLCO:", res["adjusted_dlco_ml_min_mmhg"], "mL/min/mmHg")
print("% Predicted:", res["pct_predicted_dlco"], "%")
print("Diffusion Score:", res["pulmonary_diffusion_score"], "/ 100")
print("Severity:", res["clinical_severity"])
```

## MCP Server Integration

Add to your `claude_desktop_config.json` or OpenClaw tool registry:

```json
{
  "mcpServers": {
    "alveolar-capillary-diffusion": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-alveolar-capillary-diffusion-dlco-skill/mcp_server.py"]
    }
  }
}
```

## License
MIT License.
