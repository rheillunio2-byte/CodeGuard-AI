import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

MAX_CODE_CHARS = 100_000
PATTERNS = [
    (r"\beval\s*\(", "CG001", "High", "Use of eval() can execute arbitrary Python expressions.", "Avoid eval(). Parse expected input with safer methods such as json.loads(), int(), or a dedicated parser."),
    (r"\bexec\s*\(", "CG002", "High", "Use of exec() can execute dynamically supplied Python code.", "Avoid exec() where possible. Replace dynamic execution with explicit functions or a restricted parser."),
    (r"\bos\.system\s*\(", "CG003", "High", "os.system() runs a command through the system shell.", "Prefer subprocess.run() with a list of arguments and shell=False. Validate all untrusted input."),
    (r"\bshell\s*=\s*True\b", "CG004", "High", "subprocess is configured to use a shell.", "Use shell=False and pass command arguments as a list unless shell features are truly required."),
    (r"(?i)(api[_-]?key|secret|password|token)\s*=\s*['\"][^'\"]{5,}['\"]", "CG005", "High", "A value resembling a hardcoded secret was found.", "Load secrets from environment variables or a secret manager. Rotate the value if it is real."),
    (r"\.execute\s*\(\s*f['\"]", "CG006", "High", "An f-string appears to be passed directly to execute(), which may create SQL injection risk.", "Use parameterized SQL queries instead of building SQL statements with string interpolation."),
    (r"\bpickle\.loads?\s*\(", "CG007", "High", "Pickle can execute code during deserialization when input is untrusted.", "Do not unpickle untrusted data. Use a safer format such as JSON for simple data."),
    (r"\bassert\s+", "CG008", "Low", "An assert statement was found.", "Do not use assert for validation that must remain active in production; Python can disable assertions."),
]

def _run_tool(command, path):
    try:
        result = subprocess.run(command + [str(path)], capture_output=True, text=True, timeout=20, check=False)
        output = result.stdout.strip()
        if result.stderr.strip():
            output = (output + "\n" + result.stderr.strip()).strip()
        return output, result.returncode
    except subprocess.TimeoutExpired:
        return "Tool timed out.", 124
    except OSError as exc:
        return str(exc), 127

def analyze_code(code, run_security=True, run_quality=True):
    if not isinstance(code, str):
        raise TypeError("Code must be text.")
    if not code.strip():
        return {"findings": [], "tools_run": [], "tool_output": {"CodeGuard": "No code was supplied."}}
    if len(code) > MAX_CODE_CHARS:
        raise ValueError(f"Code is too large. Limit is {MAX_CODE_CHARS} characters.")
    findings, tool_output, tools_run = [], {}, []
    for line_number, line in enumerate(code.splitlines(), 1):
        for pattern, rule, severity, message, recommendation in PATTERNS:
            if re.search(pattern, line):
                findings.append({"severity": severity, "source": "CodeGuard", "line": line_number, "rule": rule, "message": message, "recommendation": recommendation})
    with tempfile.TemporaryDirectory(prefix="codeguard_") as folder:
        path = Path(folder) / "review_target.py"
        path.write_text(code, encoding="utf-8")
        if run_security:
            if shutil.which("bandit"):
                output, _ = _run_tool(["bandit", "-f", "json", "-q"], path)
                tool_output["Bandit"] = output
                tools_run.append("Bandit")
                try:
                    for item in json.loads(output or "{}").get("results", []):
                        findings.append({"severity": item.get("issue_severity", "Medium").title(), "source": "Bandit", "line": item.get("line_number", 0), "rule": item.get("test_id", "Bandit"), "message": item.get("issue_text", "Security issue reported."), "recommendation": item.get("more_info", "Review this finding and determine whether it applies.")})
                except json.JSONDecodeError:
                    pass
            else:
                tool_output["Bandit"] = "Bandit is not installed. Install requirements to enable it."
        if run_quality:
            if shutil.which("ruff"):
                output, _ = _run_tool(["ruff", "check", "--output-format", "json"], path)
                tool_output["Ruff"] = output
                tools_run.append("Ruff")
                try:
                    for item in json.loads(output or "[]"):
                        loc = item.get("location", {})
                        findings.append({"severity": "Low", "source": "Ruff", "line": loc.get("row", 0), "rule": item.get("code", "Ruff"), "message": item.get("message", "Code quality issue reported."), "recommendation": item.get("fix", {}).get("message", "Review the reported lint rule and update code if appropriate.")})
                except json.JSONDecodeError:
                    pass
            else:
                tool_output["Ruff"] = "Ruff is not installed. Install requirements to enable it."
    rank = {"High": 0, "Medium": 1, "Low": 2, "Info": 3}
    unique = {(x["source"], x["rule"], x["line"], x["message"]): x for x in findings}
    findings = sorted(unique.values(), key=lambda x: (rank.get(x["severity"], 4), x["line"], x["source"]))
    if not tools_run:
        tools_run.append("CodeGuard")
    return {"findings": findings, "tools_run": tools_run, "tool_output": tool_output}
