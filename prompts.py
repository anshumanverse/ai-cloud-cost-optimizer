
# PROFILE PROMPT (JSON OBJECT ONLY)

PROFILE_PROMPT_EXAMPLE = """
You MUST output ONLY a single valid JSON object and nothing else.
Do NOT include explanations, markdown, or code fences.

The JSON MUST match exactly this structure:

{
  "name": "string",
  "description": "string",
  "budget_inr_per_month": integer,
  "tech_stack": {
    "frontend": string|null,
    "backend": string|null,
    "database": string|null,
    "storage": string|null,
    "proxy": string|null,
    "hosting": string|null,
    "monitoring": string|null,
    "analytics": string|null
  },
  "non_functional_requirements": ["string", ...]
}

Rules:
- Use null if information is missing.
- Use [] if there are no non-functional requirements.

Example input:
\"\"\"
We are building an e-commerce analytics tool. 
Budget 3000 INR per month. 
Frontend: React. 
Backend: Node.js. 
Database: MongoDB. 
Non-functional: scalability.
\"\"\"

Correct output:
{
  "name": "Ecommerce Market Analysis Tool",
  "description": "We are building an e-commerce analytics tool.",
  "budget_inr_per_month": 3000,
  "tech_stack": {
    "frontend": "React",
    "backend": "Node.js",
    "database": "MongoDB",
    "storage": null,
    "proxy": null,
    "hosting": null,
    "monitoring": null,
    "analytics": null
  },
  "non_functional_requirements": ["scalability"]
}

Now process the user input below and output ONLY the JSON object:

User input:
\"\"\"{description}\"\"\"
"""


# BILLING PROMPT (JSON ARRAY ONLY)

BILLING_PROMPT = """
You must output ONLY a JSON array (nothing else).

Input project profile:
{profile_json}

Produce 12–20 billing objects. Each object must contain:

- month               (string, YYYY-MM)
- service             (string)
- resource_id         (string)
- region              (string)
- usage_type          (string)
- usage_quantity      (number)
- unit                (string)
- cost_inr            (integer)
- desc                (string)

Rules:
- Costs must be realistic and loosely aligned with the given budget.
- Use a mix of compute, storage, database, networking, monitoring, CDN.
- No narration. No markdown. Output only the JSON array.
"""


# REPORT PROMPT (JSON OBJECT ONLY)

REPORT_PROMPT = """
You must output ONLY a JSON object (nothing else).

Inputs:
PROJECT PROFILE:
{profile_json}

MOCK BILLING:
{billing_json}

Produce a JSON object with this structure:

{
  "project_name": "string",
  "analysis": {
    "total_monthly_cost": integer,
    "budget": integer,
    "budget_variance": integer,
    "is_over_budget": boolean,
    "service_costs": { service_name: cost_integer },
    "high_cost_services": ["string", ...]
  },
  "recommendations": [
    {
      "title": "string",
      "service": "string",
      "current_cost": integer,
      "potential_savings": integer,
      "recommendation_type": "string",
      "description": "string",
      "implementation_effort": "low"|"medium"|"high",
      "risk_level": "low"|"medium"|"high",
      "steps": ["string", ...],
      "cloud_providers": ["AWS", "GCP", "Azure", ...]
    }
  ],
  "summary": {
    "total_potential_savings": integer,
    "savings_percentage": number,
    "recommendations_count": integer,
    "high_impact_recommendations": integer
  }
}

Rules:
- Produce 6–10 recommendations.
- Produce realistic numeric ranges.
- potential_savings must sum correctly to the summary.
- Output ONLY the JSON object.
"""
