import streamlit as st
import subprocess
import tempfile
import os
import black
import radon.complexity as radon_cc
import radon.metrics as radon_mi
import io
import sys

st.title("AI Code Reviewer")

st.markdown("Upload a Python file or paste code to analyze and improve quality using flake8, black, and radon.")

# Input
input_method = st.radio("Input Method", ("Paste Code", "Upload File"))

code = ""
if input_method == "Paste Code":
    code = st.text_area("Paste your Python code here:", height=300)
elif input_method == "Upload File":
    uploaded_file = st.file_uploader("Choose a Python file", type="py")
    if uploaded_file is not None:
        code = uploaded_file.read().decode("utf-8")

if code:
    st.subheader("Original Code")
    st.code(code, language="python")

    # Analyze with flake8
    st.subheader("Flake8 Style Check")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name
    try:
        result = subprocess.run(['flake8', temp_file], capture_output=True, text=True)
        flake8_output = result.stdout + result.stderr
        if flake8_output:
            st.text_area("Flake8 Issues:", flake8_output, height=150)
        else:
            st.success("No flake8 issues found.")
    except Exception as e:
        st.error(f"Error running flake8: {e}")
    finally:
        os.unlink(temp_file)

    # Complexity with radon
    st.subheader("Radon Complexity Analysis")
    try:
        cc_results = radon_cc.cc_visit(code)
        if cc_results:
            for result in cc_results:
                st.write(f"Function: {result.name}, Complexity: {result.complexity}")
        else:
            st.info("No functions found for complexity analysis.")
    except Exception as e:
        st.error(f"Error with radon complexity: {e}")

    st.subheader("Radon Maintainability Index")
    try:
        mi_result = radon_mi.mi_visit(code, multi=True)
        st.write(f"Maintainability Index: {mi_result}")
    except Exception as e:
        st.error(f"Error with radon MI: {e}")

    # Format with black
    st.subheader("Black Formatted Code")
    try:
        formatted_code = black.format_str(code, mode=black.FileMode())
        st.code(formatted_code, language="python")
        if formatted_code != code:
            st.info("Code was reformatted by black.")
        else:
            st.success("Code is already black-formatted.")
    except Exception as e:
        st.error(f"Error formatting with black: {e}")

    # Summary of improvements
    st.subheader("Summary of Improvements Needed")
    summary = ""
    if flake8_output:
        summary += "Style issues found by flake8. Fix them for better code quality.\n"
    else:
        summary += "No style issues.\n"
    if cc_results:
        high_complexity = [r for r in cc_results if r.complexity > 10]
        if high_complexity:
            summary += f"High complexity functions: {[r.name for r in high_complexity]}\n"
        else:
            summary += "Complexity is acceptable.\n"
    if mi_result < 20:
        summary += "Low maintainability index. Consider refactoring.\n"
    else:
        summary += "Maintainability is good.\n"
    st.text_area("Summary:", summary, height=100)

    # Export report
    report = f"Original Code:\n{code}\n\nFlake8 Output:\n{flake8_output}\n\nComplexity:\n{cc_results}\n\nMI: {mi_result}\n\nFormatted Code:\n{formatted_code}\n\nSummary:\n{summary}"
    st.download_button("Download Report", report, file_name="code_review_report.txt")
else:
    st.info("Please provide code to analyze.")
