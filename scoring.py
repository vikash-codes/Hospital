import re

def generate_performance_summary(response_analysis):
    match = re.search(r"Score:\s*(\d+)/10", response_analysis)
    score = int(match.group(1)) if match else "N/A"
    feedback = f"Performance Summary:\n- Score: {score}/10\n- Analysis: {response_analysis}"
    return feedback
