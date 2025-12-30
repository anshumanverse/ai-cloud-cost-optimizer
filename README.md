**DESCRIPTION**:
The AI-Powered Cloud Cost Optimizer is a command-line tool designed to analyze cloud project requirements and provide cost optimization insights.
It takes a plain-text project description from the user, converts it into a structured project profile, generates realistic mock cloud billing data, and produces a cost optimization report with actionable recommendations.

**File Descriptions**
cost_optimizer.py
Main CLI entry point that orchestrates the full pipeline, manages user input, and handles report generation and export.

llm_client.py
Wrapper around the HuggingFace LLM API with retry logic and response normalization.

prompts.py
Contains strict JSON-only prompt templates for profile extraction, billing generation, and cost analysis.

utils.py
Utility functions for JSON extraction, cost aggregation, and safe parsing of LLM outputs.

validators.py
JSON Schema validation utilities to ensure correctness of generated data at each stage.

schemas/
JSON schema definitions for validating project profiles, billing records, and reports.

samples/
Stores generated outputs such as profiles, billing data, and reports (ignored by Git).
