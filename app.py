from flask import Flask, request, jsonify
import re
import pylint.lint

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

def run_pylint(code):
    """
    Run Pylint on the provided code and extract issues.
    
    Args:
        code (str): The input code.
        
    Returns:
        list: A list of tuples containing issue messages and line numbers.
    """
    pylint_output = Run(["--disable=all", "--enable=W", "--output-format=parseable", "--reports=n", "-"], do_exit=False, exit=False, stdout=None, stderr=None, script='').linter.check(code)
    issues = [(message.msg, message.line) for message in pylint_output]
    return issues
    
    


@app.route('/analyze', methods=['POST'])
def analyze_code():
    """
    Analyze the submitted code, apply custom rules, and generate comments for detected issues.
    """
    data = request.get_json()
    code = data.get('code', '')

    # Apply custom rules (enforce maximum line length)
    corrected_code, comments = enforce_max_line_length(code)

    # Run Pylint
    pylint_issues = run_pylint(code)
    for issue_message, line_number in pylint_issues:
        comments.append(f"Line {line_number}: {issue_message}")

    return jsonify({'corrected_code': corrected_code, 'comments': comments})

if __name__ == '__main__':
    app.run(debug=True)
