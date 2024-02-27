from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def enforce_max_line_length(code, max_line_length=80):
    """
    Enforce a maximum line length for code and generate comments for lines that exceed the maximum length.
    
    Args:
        code (str): The input code.
        max_line_length (int): The maximum allowed line length.
        
    Returns:
        tuple: A tuple containing the corrected code and a list of comments.
    """
    corrected_code = []
    comments = []
    
    lines = code.split('\n')
    for i, line in enumerate(lines):
        if len(line) > max_line_length:
            comments.append(f"Line {i+1}: Exceeds maximum line length ({len(line)} characters)")
            # Truncate the line to meet the maximum length
            line = line[:max_line_length]
        corrected_code.append(line)

    corrected_code_str = '\n'.join(corrected_code)
    return corrected_code_str, comments

def custom_rules(code):
    """
    Apply custom rules to the provided code and generate comments for detected issues.
    
    Args:
        code (str): The input code.
        
    Returns:
        list: A list of comments for detected issues.
    """
    comments = []
    
    # List of regex patterns for custom rules
    custom_rules_patterns = [
        (r"'[^']*'|\"[^\"]*\"|\b\d+\b", "Hardcoded value detected"),
        (r'def\s+[a-z][a-zA-Z0-9_]*\s*\(.*?\)\s*:', "Improper function naming detected (use snake_case)"),
        (r'\bprint\s*\(', "Print statement detected"),
        (r'\b\d+(\.\d+)?\b', "Magic number detected")
    ]

    # Apply each regex pattern and generate comments for detected issues
    for i, line in enumerate(code.split('\n')):
        for pattern, comment in custom_rules_patterns:
            if re.search(pattern, line):
                comments.append(f"Line {i+1}: {comment}")
                break  # Stop searching for this pattern if a match is found

    return comments

@app.route('/analyze', methods=['POST'])
def analyze_code():
    """
    Analyze the submitted code, apply custom rules, and generate comments for detected issues.
    """
    data = request.get_json()
    code = data.get('code', '')

    # Apply custom rules
    custom_rule_comments = custom_rules(code)

    # Enforce maximum line length and generate comments
    corrected_code, length_comments = enforce_max_line_length(code)

    # Combine comments from custom rules and length enforcement
    all_comments = custom_rule_comments + length_comments

    return jsonify({'corrected_code': corrected_code, 'comments': all_comments})

if __name__ == '__main__':
    app.run(debug=True)
