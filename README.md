# Elevatelab_Ai_code_Reviewer

# AI Code Reviewer

An interactive AI-powered Python Code Reviewer built using Streamlit.  
This application helps developers analyze and improve Python code quality using:

- Flake8 → Style & syntax checking
- Black → Automatic code formatting
- Radon → Complexity & maintainability analysis

---

## Features

### 1. Upload or Paste Python Code
Users can:
- Paste Python code directly into the app
- Upload `.py` files for analysis

### 2. Flake8 Style Analysis
Checks:
- PEP8 violations
- Unused imports
- Syntax issues
- Formatting problems

### 3. Radon Complexity Analysis
Measures:
- Cyclomatic Complexity of functions
- Helps identify overly complex functions

### 4. Maintainability Index
Calculates maintainability score using Radon:
- High score = easier to maintain
- Low score = code needs refactoring

### 5. Automatic Code Formatting
Uses Black formatter to:
- Reformat Python code
- Improve consistency and readability

### 6. Improvement Summary
Generates a summary including:
- Style issues
- Complexity problems
- Maintainability feedback

### 7. Downloadable Report
Users can export the full analysis report as a `.txt` file.

---

# Technologies Used

- Python
- Streamlit
- Flake8
- Black
- Radon

---

# Project Structure

```bash
AI-Code-Reviewer/
│
├── app.py
├── README.md
└── requirements.txt
