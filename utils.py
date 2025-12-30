import os
import re
import json


# -------------------------------------------------------------
# Basic JSON Extractor (Used for Billing + Report)
# -------------------------------------------------------------
def extract_json_object_or_array(text):
    """Extract ONLY the first valid JSON object {...} or array [...] from text."""
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Try arrays first
    arr_candidates = re.findall(r"\[.*?\]", text, flags=re.DOTALL)
    for candidate in arr_candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # Try objects
    obj_candidates = re.findall(r"\{.*?\}", text, flags=re.DOTALL)
    for candidate in obj_candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    raise ValueError("No valid JSON array or object found in model output.")


# -------------------------------------------------------------
# Billing Aggregation Utilities
# -------------------------------------------------------------
def aggregate_service_costs(billing):
    """Aggregate total costs and per-service costs from billing records."""
    total = 0
    svc_costs = {}

    for record in billing:
        cost = int(record.get("cost_inr", 0))
        service = record.get("service", "Unknown")

        svc_costs[service] = svc_costs.get(service, 0) + cost
        total += cost

    top_services = sorted(
        svc_costs.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    top_services = [svc for svc, _ in top_services]
    return total, svc_costs, top_services


# -------------------------------------------------------------
# Profile Parser Utilities
# -------------------------------------------------------------
def _strip_code_fences(text):
    """Remove Markdown code fences like ```json ... ```."""
    text = re.sub(r"```(?:json)?", "", text)
    return re.sub(r"```", "", text).strip()


def _clean_json_like(s):
    """Fix simple JSON mistakes like single quotes and trailing commas."""
    s = re.sub(r"(?<!\\)'", '"', s)
    s = re.sub(r",\s*([}\]])", r"\1", s)
    return s


def parse_json_response_for_profile(raw_text):
    """Parse JSON object from LLM output for profile extraction."""
    if not isinstance(raw_text, str):
        raise ValueError("Model output is not text")

    # Save raw output for debugging
    os.makedirs("samples", exist_ok=True)
    with open("samples/last_llm_raw.txt", "w", encoding="utf-8") as f:
        f.write(raw_text)

    txt = raw_text.strip()

    # 1) Direct parse
    try:
        obj = json.loads(txt)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    # 2) Regex fallback
    match = re.search(r"\{[\s\S]*\}", txt)
    if match:
        try:
            obj = json.loads(match.group(0))
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass

    raise ValueError("Unable to parse model output into JSON.")


def extract_json_object(text):
    """Extract ONLY the first valid JSON object {...} from text."""
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Direct parse
    try:
        obj = json.loads(text.strip())
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    # Regex fallback
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            obj = json.loads(match.group(0))
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass

    raise ValueError("Could not extract JSON object.")
