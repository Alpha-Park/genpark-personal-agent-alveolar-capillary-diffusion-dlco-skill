"""
MCP Server for Alveolar-Capillary Gas Diffusion (DLCO) & Membrane Conductance.
Exposes JSON-RPC endpoints for evaluating DLCO gas exchange and hemoglobin adjustments.
"""

import json
import sys
from client import AlveolarCapillaryDiffusionClient

client = AlveolarCapillaryDiffusionClient()


def handle_request(request: dict) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_dlco_diffusion",
                        "description": "Calculates hemoglobin-adjusted diffusing capacity of the lung for carbon monoxide (DLCO), % of predicted, transfer coefficient (KCO), and pulmonary diffusion resilience score.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "measured_dlco_ml_min_mmhg": {"type": "number", "description": "Unadjusted measured DLCO in mL/min/mmHg (e.g. 26.5)"},
                                "predicted_dlco_ml_min_mmhg": {"type": "number", "description": "Demographically predicted normal DLCO in mL/min/mmHg (e.g. 29.0)"},
                                "hemoglobin_g_dl": {"type": "number", "default": 14.5, "description": "Circulating hemoglobin in g/dL"},
                                "is_female": {"type": "boolean", "default": False, "description": "True for female reference formula"},
                                "alveolar_volume_liters": {"type": "number", "description": "Optional single-breath alveolar volume (VA) in Liters"}
                            },
                            "required": ["measured_dlco_ml_min_mmhg", "predicted_dlco_ml_min_mmhg"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "evaluate_dlco_diffusion":
            res = client.evaluate_dlco_diffusion(
                measured_dlco_ml_min_mmhg=args.get("measured_dlco_ml_min_mmhg", 26.5),
                predicted_dlco_ml_min_mmhg=args.get("predicted_dlco_ml_min_mmhg", 29.0),
                hemoglobin_g_dl=args.get("hemoglobin_g_dl", 14.5),
                is_female=args.get("is_female", False),
                alveolar_volume_liters=args.get("alveolar_volume_liters")
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {tool_name} not found"}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": "Invalid Request"}
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
