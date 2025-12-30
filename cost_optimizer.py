import os
import json
from dotenv import load_dotenv

load_dotenv()

# Project imports
from llm_client import call_hf_chat
from prompts import PROFILE_PROMPT_EXAMPLE, BILLING_PROMPT, REPORT_PROMPT
from utils import (
    extract_json_object_or_array,
    aggregate_service_costs,
    parse_json_response_for_profile,
    extract_json_object,
)
from validators import validate_json

# Path Setup
ROOT = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(ROOT, "samples")
SCHEMAS_DIR = os.path.join(ROOT, "schemas")

os.makedirs(SAMPLES_DIR, exist_ok=True)

PROFILE_PATH = os.path.join(SAMPLES_DIR, "project_profile.json")
BILLING_PATH = os.path.join(SAMPLES_DIR, "mock_billing.json")
REPORT_PATH = os.path.join(SAMPLES_DIR, "cost_optimization_report.json")
DESC_PATH = os.path.join(SAMPLES_DIR, "project_description.txt")
RAW_LLM_PATH = os.path.join(SAMPLES_DIR, "last_llm_raw.txt")



# Helpers
def save_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    print(f"Saved: {path}")


def save_raw_output(text):
    with open(RAW_LLM_PATH, "w", encoding="utf-8") as f:
        f.write(text)


def clear_samples_folder():
    """Delete all generated outputs when starting a new project."""
    if not os.path.exists(SAMPLES_DIR):
        return

    for fname in os.listdir(SAMPLES_DIR):
        path = os.path.join(SAMPLES_DIR, fname)
        if os.path.isfile(path):
            os.remove(path)


def load_description(force_new=False):
    """Load or prompt for project description."""
    if not force_new and os.path.exists(DESC_PATH):
        with open(DESC_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content

    print("Enter project description (end with an empty line):")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)

    desc = "\n".join(lines).strip()
    if desc:
        os.makedirs(os.path.dirname(DESC_PATH), exist_ok=True)
        with open(DESC_PATH, "w", encoding="utf-8") as f:
            f.write(desc)

    return desc


# LLM Pipeline Stages
def run_profile_extraction(description, retries=2):
    prompt = PROFILE_PROMPT_EXAMPLE.replace("{description}", description)
    last_exc = None

    for attempt in range(1, retries + 2):
        raw = call_hf_chat(prompt, max_tokens=400, temperature=0.0)
        save_raw_output(raw)

        try:
            profile = parse_json_response_for_profile(raw)
            ok, err = validate_json(profile, os.path.join(SCHEMAS_DIR, "profile_schema.json"))
            if not ok:
                raise ValueError(err)

            save_json(PROFILE_PATH, profile)
            return profile

        except Exception as e:
            last_exc = e
            print(f"\nProfile extraction attempt {attempt} failed:", e)
            if attempt <= retries:
                prompt += "\nIMPORTANT: Return ONLY a strict JSON object."

    raise RuntimeError(f"Profile extraction failed: {last_exc}")


def run_billing_generation(profile, retries=1):
    prompt = BILLING_PROMPT.replace("{profile_json}", json.dumps(profile))
    last_exc = None

    for attempt in range(1, retries + 2):
        raw = call_hf_chat(prompt, max_tokens=3000, temperature=0.0)
        save_raw_output(raw)

        try:
            billing = extract_json_object_or_array(raw)
            if not isinstance(billing, list):
                raise ValueError("Billing must be a JSON array")

            ok, err = validate_json(billing, os.path.join(SCHEMAS_DIR, "billing_schema.json"))
            if not ok:
                raise ValueError(err)

            save_json(BILLING_PATH, billing)
            return billing

        except Exception as e:
            last_exc = e
            print(f"\nBilling generation attempt {attempt} failed:", e)

    raise RuntimeError(f"Billing generation failed: {last_exc}")


def run_report_generation(profile, billing, retries=1):
    prompt = (
        REPORT_PROMPT
        .replace("{profile_json}", json.dumps(profile))
        .replace("{billing_json}", json.dumps(billing))
    )
    last_exc = None

    for attempt in range(1, retries + 2):
        raw = call_hf_chat(prompt, max_tokens=3000, temperature=0.0)
        save_raw_output(raw)

        try:
            report = extract_json_object(raw)
            ok, err = validate_json(report, os.path.join(SCHEMAS_DIR, "report_schema.json"))
            if not ok:
                print("WARNING:", err)

            save_json(REPORT_PATH, report)
            return report

        except Exception as e:
            last_exc = e
            print(f"\nReport generation attempt {attempt} failed:", e)

    raise RuntimeError(f"Report generation failed: {last_exc}")


# Orchestration
def run_full_pipeline():
    desc = load_description()
    if not desc:
        print("Missing description.")
        return

    print("\nRunning profile extraction...")
    profile = run_profile_extraction(desc)

    print("\nRunning billing generation...")
    billing = run_billing_generation(profile)

    print("\nRunning report generation...")
    run_report_generation(profile, billing)

    total, svc_costs, top_services = aggregate_service_costs(billing)

    print("\n=== BILLING SUMMARY ===")
    print("Total (INR):", total)
    print("Service costs:", svc_costs)
    print("Top cost drivers:", top_services)
    print("=======================")


def view_report():
    if os.path.exists(REPORT_PATH):
        print(open(REPORT_PATH, "r", encoding="utf-8").read())
    else:
        print("Report not found.")


def export_report():
    if not os.path.exists(REPORT_PATH):
        print("No report to export.")
        return

    path = input("Enter export file path (e.g. report.json): ").strip()
    if not path:
        print("Invalid path.")
        return

    with open(REPORT_PATH, "r", encoding="utf-8") as src:
        with open(path, "w", encoding="utf-8") as dst:
            dst.write(src.read())

    print(f"Report exported to {path}")


# CLI
def menu():
    while True:
        print("\n1. Enter new project description")
        print("2. Run Complete Cost Analysis")
        print("3. View Recommendations")
        print("4. Export Report")
        print("5. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            clear_samples_folder()
            desc = load_description(force_new=True)
            print("New project initialized.") if desc else print("No description entered.")

        elif choice == "2":
            try:
                run_full_pipeline()
            except Exception as e:
                print("Pipeline failed:", e)

        elif choice == "3":
            view_report()

        elif choice == "4":
            export_report()

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    print("AI-Powered Cloud Cost Optimizer")
    menu()
