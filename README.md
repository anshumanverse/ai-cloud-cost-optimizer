# AI-Powered Cloud Cost Optimizer (CLI)

##  Description

The **AI-Powered Cloud Cost Optimizer** is a command-line tool designed to analyze cloud project requirements and provide cost optimization insights.
It takes a **plain-text project description** from the user, converts it into a **structured project profile**, generates **realistic mock cloud billing data**, and produces a **cost optimization report** with actionable recommendations.

---

## File Descriptions

* **`cost_optimizer.py`**
  Main CLI entry point that orchestrates the full pipeline, manages user input, and handles report generation and export.

* **`llm_client.py`**
  Wrapper around the HuggingFace LLM API with retry logic and response normalization.

* **`prompts.py`**
  Contains strict JSON-only prompt templates for profile extraction, billing generation, and cost analysis.

* **`utils.py`**
  Utility functions for JSON extraction, cost aggregation, and safe parsing of LLM outputs.

* **`validators.py`**
  JSON Schema validation utilities to ensure correctness of generated data at each stage.

* **`schemas/`**
  JSON schema definitions for validating project profiles, billing records, and reports.

* **`samples/`**
  Stores generated outputs such as profiles, billing data, and reports (ignored by Git).

---

##  Complete Setup & Usage Instructions


---

## 1. Clone the Repository

### Using Git (Command Line)

```bash
git clone https://github.com/anshumanverse/ai-cloud-cost-optimizer.git
cd ai-cloud-cost-optimizer
```

### Using Visual Studio Code

1. Open **VS Code**
2. Press **Ctrl + Shift + P**
3. Select **Git: Clone**
4. Paste the repository URL:

   ```
   https://github.com/anshumanverse/ai-cloud-cost-optimizer.git
   ```
5. Choose a local folder and open the repository

---

## 2. Prerequisites

Ensure the following are installed:

* Python **3.8+**
* Git
* Internet connection (for LLM API calls)

---

##  3. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate    # Windows
```

After activation, your terminal should show:

```
(venv)
```

---

##  4. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required libraries for the project.

---

## 5. Configure Environment Variables

Create a file named **`.env`** in the project root and add:

```env
HF_API_KEY=your_huggingface_api_key_here
```

This API key is required to access the HuggingFace LLM.
Do **not** commit this file to GitHub.

---

## 6. Run the Application

```bash
python cost_optimizer.py
```

You will see the CLI menu:

```
AI-Powered Cloud Cost Optimizer

1. Enter new project description
2. Run Complete Cost Analysis
3. View Recommendations
4. Export Report
5. Exit
```

---

## 7. Typical Usage Flow

### Step 1: Enter Project Description

Choose **Option 1** and enter a plain-text description.

* Old outputs are automatically cleared
* Description is saved locally

---

### Step 2: Run Complete Cost Analysis

Choose **Option 2** to:

* Generate a structured project profile
* Generate mock cloud billing data
* Generate a cost optimization report

All outputs are stored in the `samples/` folder.

---

### Step 3: View Recommendations

Choose **Option 3** to display the generated cost optimization report directly in the terminal.

---

### Step 4: Export Report

Choose **Option 4** to export `cost_optimization_report.json` to a location of your choice.

---

## 8. Output Files

Generated outputs include:

* `project_description.txt`
* `project_profile.json`
* `mock_billing.json`
* `cost_optimization_report.json`

These files are created inside the **`samples/`** directory and are ignored by Git.

---

## Example Usage Flow

### Sample Project Description

```
We are building a web-based task management application for a startup.
The expected cloud budget is around 2500 INR per month.
Frontend is built using React and backend uses Python with FastAPI.
PostgreSQL is used as the database.
The application requires basic monitoring and scalability.
```

Saved as:

```
samples/project_description.txt
```

---

### Generated `project_profile.json`

```json
{
  "name": "Task Management Application",
  "description": "Web-based task management application for a startup team.",
  "budget_inr_per_month": 2500,
  "tech_stack": {
    "frontend": "React",
    "backend": "Python (FastAPI)",
    "database": "PostgreSQL",
    "storage": null,
    "proxy": null,
    "hosting": "Cloud VM",
    "monitoring": "Basic monitoring",
    "analytics": null
  },
  "non_functional_requirements": ["scalability"]
}
```

---

### Generated `mock_billing.json` (shortened)

```json
[
  {
    "month": "2024-01",
    "service": "Compute",
    "resource_id": "i-123456",
    "region": "ap-south-1",
    "usage_type": "OnDemand",
    "usage_quantity": 10,
    "unit": "hours",
    "cost_inr": 1500,
    "desc": "Virtual machine instance"
  }
]
```

---

### Generated `cost_optimization_report.json`

```json
{
  "project_name": "Task Management Application",
  "analysis": {
    "total_monthly_cost": 17180,
    "budget": 2500,
    "budget_variance": 14680,
    "is_over_budget": true
  }
}
```

---

## Tools Used

* **ChatGPT (OpenAI)**
  Used for assistance with prompt refinement, code review, and documentation.

* **Visual Studio Code**  
  Used as the development environment.

---


