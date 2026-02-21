import ast


def detect_syntax_error(code):
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        return f"Syntax Error: {e}"


def analyze_code(code):
    bugs = []

    syntax_issue = detect_syntax_error(code)
    if syntax_issue:
        bugs.append(syntax_issue)
        return bugs

    if "def " in code and "return" not in code:
        bugs.append("Warning: Function may be missing a return statement.")

    if "=" in code and "print" not in code:
        bugs.append("Warning: Variable assigned but may be unused.")

    return bugs
