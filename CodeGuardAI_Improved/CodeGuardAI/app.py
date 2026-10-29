import pandas as pd
import streamlit as st
from analyzer import analyze_code
from ai_reviewer import review_with_ai_stream

st.set_page_config(page_title="CodeGuard AI", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap');
:root { --cg-bg:#080d19; --cg-panel:#10192b; --cg-border:#25334d; --cg-text:#eef4ff; --cg-muted:#94a3b8; --cg-blue:#60a5fa; --cg-purple:#a78bfa; }
.stApp { background: radial-gradient(ellipse at 8% 0%, #172449 0%, #0b1120 38%, #080d19 78%); color:var(--cg-text); font-family:'Inter',sans-serif; }
[data-testid="stSidebar"] { background:rgba(10,16,31,.96); border-right:1px solid var(--cg-border); }
.block-container { max-width:1450px; padding-top:1.8rem; padding-bottom:3rem; }
[data-testid="stHeader"] { background:transparent; }
.cg-hero { position:relative; overflow:hidden; padding:1.8rem 2rem; border:1px solid #344568; border-radius:22px; background:linear-gradient(115deg,rgba(21,37,69,.97),rgba(35,23,65,.94)); margin-bottom:1.35rem; box-shadow:0 18px 50px rgba(0,0,0,.22); }
.cg-hero:after { content:' '; position:absolute; width:220px; height:220px; right:-65px; top:-95px; border:1px solid rgba(167,139,250,.32); border-radius:50%; box-shadow:0 0 0 22px rgba(96,165,250,.04),0 0 0 46px rgba(167,139,250,.035); }
.cg-kicker { color:#93c5fd; font-family:'DM Mono',monospace; font-size:.76rem; letter-spacing:.16em; text-transform:uppercase; }
.cg-title { color:#f8fbff; font-size:2.25rem; font-weight:800; letter-spacing:-.045em; margin:.35rem 0 .45rem; }
.cg-subtitle { color:#b9c6e0; font-size:1rem; max-width:760px; margin:0; }
.cg-section { font-size:1.08rem; font-weight:750; color:#f0f6ff; margin:.4rem 0 .75rem; }
.cg-card { border:1px solid var(--cg-border); background:linear-gradient(145deg,rgba(17,27,47,.94),rgba(12,19,34,.96)); padding:1rem 1.1rem; border-radius:16px; min-height:100px; }
.cg-card-label { color:var(--cg-muted); font-size:.78rem; font-weight:600; letter-spacing:.03em; }
.cg-card-value { color:#f8fbff; font-size:1.85rem; font-weight:800; margin-top:.3rem; }
.cg-muted { color:var(--cg-muted); font-size:.86rem; }
div.stButton > button, div.stDownloadButton > button { border-radius:11px; border:1px solid #4255a3; font-weight:700; min-height:2.8rem; transition:all .15s ease; }
div.stButton > button[kind="primary"] { background:linear-gradient(100deg,#4f67ed,#7957e8); color:white; border:0; }
div.stButton > button[kind="secondary"] { background:#111b30; color:#e4edff; }
div.stButton > button:hover, div.stDownloadButton > button:hover { border-color:#9b8cff; color:white; }
[data-testid="stTextArea"] textarea { background:#080e1c; color:#dbeafe; border:1px solid #293956; border-radius:13px; font-family:'DM Mono',monospace; font-size:.88rem; line-height:1.55; }
[data-testid="stFileUploader"] { border:1px dashed #344568; border-radius:13px; padding:.55rem; background:rgba(16,25,43,.5); }
[data-testid="stDataFrame"] { border:1px solid #263550; border-radius:13px; overflow:hidden; }
.stTabs [data-baseweb="tab-list"] { gap:.45rem; border-bottom:1px solid var(--cg-border); }
.stTabs [data-baseweb="tab"] { border-radius:10px 10px 0 0; padding:.65rem 1rem; color:#aab8d0; }
.stTabs [aria-selected="true"] { color:#f8fbff !important; background:#182542; }
hr { border-color:#25334d; }
[data-testid="stAlert"] { border-radius:12px; }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div class='cg-kicker'>CODEGUARD / WORKSPACE</div>", unsafe_allow_html=True)
    st.markdown("## 🛡️ CodeGuard AI")
    st.caption("Python security and quality review")
    st.divider()
    st.markdown("**Scan configuration**")
    run_security = st.toggle("Security checks · Bandit", value=True)
    run_quality = st.toggle("Quality checks · Ruff", value=True)
    st.divider()
    st.markdown("**Review workflow**")
    st.markdown("<span class='cg-muted'>01</span>  Paste or upload code", unsafe_allow_html=True)
    st.markdown("<span class='cg-muted'>02</span>  Run a local scan", unsafe_allow_html=True)
    st.markdown("<span class='cg-muted'>03</span>  Request AI explanations", unsafe_allow_html=True)
    st.divider()
    st.caption("Privacy note: AI review sends the submitted code to Google Gemini. Remove secrets and private credentials before reviewing.")

st.markdown("""
<div class="cg-hero">
  <div class="cg-kicker">DEVELOPER SECURITY TOOLKIT</div>
  <div class="cg-title">CodeGuard <span style="color:#a78bfa">AI</span></div>
  <p class="cg-subtitle">Catch risky patterns, understand code quality issues, and get practical review suggestions in one focused workspace.</p>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader("Upload a Python file", type=["py"], help="Choose a .py file to load into the editor.")
if uploaded is not None:
    uploaded_code = uploaded.getvalue().decode("utf-8", errors="replace")
    if st.session_state.get("loaded_file_name") != uploaded.name:
        st.session_state["code_input"] = uploaded_code
        st.session_state["loaded_file_name"] = uploaded.name

default_code = "import os\n\ndef run_command(user_input):\n    result = eval(user_input)\n    os.system(\"echo \" + user_input)\n    return result\n"
if "code_input" not in st.session_state:
    st.session_state["code_input"] = default_code

st.markdown("<div class='cg-section'>01 / Code workspace</div>", unsafe_allow_html=True)
code = st.text_area("Python source code", key="code_input", height=300, label_visibility="collapsed", placeholder="Paste Python code here...")

scan_col, ai_col, note_col = st.columns([1, 1, 2])
with scan_col:
    scan_clicked = st.button("🔎  Run static scan", type="secondary", use_container_width=True)
with ai_col:
    ai_clicked = st.button("✦  Review with Gemini", type="primary", use_container_width=True)
with note_col:
    st.markdown("<div class='cg-muted' style='padding:.75rem .2rem'>Static checks run locally. AI review may take longer because it calls the Gemini API.</div>", unsafe_allow_html=True)

if scan_clicked:
    with st.spinner("Scanning for security and quality issues..."):
        st.session_state["scan_result"] = analyze_code(code, run_security, run_quality)

if ai_clicked:
    if not code.strip():
        st.warning("Add Python code before requesting a review.")
    else:
        st.session_state.pop("ai_review", None)
        try:
            with st.status("Gemini is reviewing your code…", expanded=True) as status:
                st.write("Checking for likely bugs, security risks, and maintainability issues.")
                review_text = st.write_stream(review_with_ai_stream(code))
                status.update(label="AI review complete", state="complete", expanded=False)
            st.session_state["ai_review"] = review_text
        except Exception as exc:
            st.error(f"AI review failed: {exc}")

scan_tab, ai_tab, about_tab = st.tabs(["📊  Scan results", "✦  AI review", "ⓘ  About"])
with scan_tab:
    st.markdown("<div class='cg-section'>02 / Findings overview</div>", unsafe_allow_html=True)
    if "scan_result" not in st.session_state:
        st.info("Run a static scan to see findings, severity counts, and downloadable results.")
    else:
        result = st.session_state["scan_result"]
        findings = result["findings"]
        high_count = sum(x["severity"] == "High" for x in findings)
        medium_count = sum(x["severity"] == "Medium" for x in findings)
        low_count = sum(x["severity"] == "Low" for x in findings)
        metric_cols = st.columns(4)
        for col, label, value in zip(metric_cols, ["Total findings", "High severity", "Medium severity", "Low severity"], [len(findings), high_count, medium_count, low_count]):
            col.markdown(f"<div class='cg-card'><div class='cg-card-label'>{label}</div><div class='cg-card-value'>{value}</div></div>", unsafe_allow_html=True)
        st.write("")
        if findings:
            frame = pd.DataFrame(findings)
            filters = st.columns([1, 1, 2])
            with filters[0]:
                severity_filter = st.selectbox("Severity", ["All", "High", "Medium", "Low", "Info"])
            with filters[1]:
                source_filter = st.selectbox("Source", ["All"] + sorted(frame["source"].dropna().unique().tolist()))
            filtered = frame.copy()
            if severity_filter != "All":
                filtered = filtered[filtered["severity"] == severity_filter]
            if source_filter != "All":
                filtered = filtered[filtered["source"] == source_filter]
            visible = [c for c in ["severity", "source", "line", "rule", "message", "recommendation"] if c in filtered.columns]
            st.dataframe(filtered[visible], use_container_width=True, hide_index=True, column_config={"severity": st.column_config.TextColumn("Severity", help="Estimated severity, not a proof of exploitability."), "line": st.column_config.NumberColumn("Line", format="%d")})
            st.download_button("⬇ Download filtered findings · CSV", filtered.to_csv(index=False).encode("utf-8"), "codeguard_findings.csv", "text/csv")
        else:
            st.success("No findings were reported by the enabled checks. This does not guarantee that the code is secure.")
        with st.expander("Technical tool output"):
            for name, output in result["tool_output"].items():
                st.markdown(f"**{name}**")
                st.code(output or "No output", language="text")

with ai_tab:
    st.markdown("<div class='cg-section'>03 / AI code review</div>", unsafe_allow_html=True)
    if "ai_review" in st.session_state:
        st.markdown(st.session_state["ai_review"])
    else:
        st.markdown("<div class='cg-card'><div class='cg-card-label'>GEMINI REVIEW ENGINE</div><div style='font-size:1.05rem;font-weight:700;margin:.4rem 0'>Ready when you are.</div><div class='cg-muted'>Click “Review with Gemini” to generate a focused review. The response will appear here as it streams in.</div></div>", unsafe_allow_html=True)

with about_tab:
    st.markdown("<div class='cg-section'>About CodeGuard AI</div>", unsafe_allow_html=True)
    st.write("CodeGuard AI combines local static-analysis tools with optional Gemini-powered explanations.")
    st.markdown("- **Bandit:** Python security checks\n- **Ruff:** Python linting and code-quality rules\n- **CodeGuard rules:** selected risky patterns\n- **Gemini:** explanations and recommended fixes")
    st.warning("This tool is a developer aid, not a guarantee of security. Review findings manually, and test any suggested fixes before using them.")

st.divider()
st.markdown("<div class='cg-muted'>CODEGUARD AI · LOCAL SCANS + GEMINI REVIEW · Treat all automated findings as guidance that requires human verification.</div>", unsafe_allow_html=True)
