import streamlit as st
import google.generativeai as genai
import PyPDF2
import json
import time
import streamlit.components.v1 as components
from datetime import datetime

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Connected Global Intelligence Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. SIDEBAR SETUP ---
st.sidebar.title("🚀 Intelligence Engine")
st.sidebar.markdown("---")

# API Key Input (Secure)
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# Simulation Inputs
st.sidebar.subheader("Simulation Setup")
opp_id_input = st.sidebar.text_input("Opportunity ID", value="SGS-PERTH-001")
user_name_input = st.sidebar.text_input("User Name", value="Armand")

# File Uploader
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Upload Context (PDF)", type=['pdf'])

# --- 2. AGENT FUNCTIONS (Your Core Logic) ---

def agent_document_parser(uploaded_file):
    """Extracts text from the uploaded PDF stream."""
    if not uploaded_file: return "", []
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return f"\n--- CONTENT FROM {uploaded_file.name} ---\n{text}", [uploaded_file.name]
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return "", []

def agent_salesforce_mimic():
    """Simulates the Salesforce connection."""
    with st.spinner("🔌 Connecting to Salesforce API..."):
        time.sleep(1.5) # Fake delay for realism
    return {
        "Name": "SGS - Perth - Consolidation",
        "Account": {"Name": "SGS"},
        "Amount": 20000000,
        "CloseDate": "2026-09-30",
        "StageName": "4. Qualified",
        "Owner": {"Name": "Sam Henderson"},
        "Description": "TIC Labs Sector. Mixed refurbishment and fit-out. Client meeting on 4.12.24. Key driver: 35.0% GP%.",
        "CustomFields": {
            "Decision_Date__c": "2026-04-04",
            "Handover_Date__c": "2026-03-05",
            "Delta_Score__c": 30,
            "GP_Amount__c": 7000000,
            "Office__c": "Perth"
        },
        "Contacts": [
            {"Name": "Bruce Larsen", "Role": "Procurement", "Title": "National Procurement Manager"},
            {"Name": "Luke Menezies", "Role": "Influencer", "Title": "Director (CBRE)"},
            {"Name": "Johan O'Connell", "Role": "Decision Maker", "Title": "MD, ANZ"},
            {"Name": "Barry O'Donoghue", "Role": "Finance", "Title": "CFO + GM Finance"},
            {"Name": "Gavin Grace", "Role": "CR Lead", "Title": "Connected Contact"}
        ],
        "Tasks": [
            {"Subject": "Meeting with SGS Perth", "Status": "Event", "ActivityDate": "2026-02-02", "Owner": {"Name": "Mia Baker"}},
            {"Subject": "Confirm mtg with Bruce & ops team", "Status": "Update", "ActivityDate": "2026-01-21", "Owner": {"Name": "Sam Henderson"}}
        ]
    }

def agent_strategy_brain(sf_data, file_context, key):
    """The AI Core."""
    # Fallback Data if no API Key provided
    fallback_data = {
        "summary": "Demo Mode: SGS is consolidating 6 labs into one 8,000m² facility. Critical requirement is reuse of existing services.",
        "swot": {
            "strengths": ["TIC Sector Proven Track Record", "Connection with Sydney Ops team"],
            "weaknesses": ["Lack of connection with Exec level", "Low budget expectations"],
            "opportunities": ["Connection with CBRE (Luke Menzies)", "Global Portfolio Leverage"],
            "threats": ["CBRE PM focused on Warehousing", "Perceived Conflict of Interest (ALS)"]
        },
        "win_thesis": "We win by proving our sector expertise allows us to de-risk the complex 'reuse of services' better than general builders.",
        "lose_thesis": "We lose if the 'Conflict of Interest' with ALS becomes a blocker at the Geneva Executive level.",
        "stakeholder_intel": "Bruce Larsen focuses on cost/risk. Luke Menzies (CBRE) is the gatekeeper.",
        "win_probability": 45,
        "stakeholder_scores": [
            {"name": "Bruce Larsen", "influence": 8, "support": 5},
            {"name": "Luke Menzies", "influence": 9, "support": 6},
            {"name": "Johan O'Connell", "influence": 10, "support": 4},
            {"name": "Barry O'Donoghue", "influence": 7, "support": 5}
        ]
    }

    if not key:
        return fallback_data

    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        full_context = f"""
        PROJECT: {sf_data['Name']}
        CLIENT: {sf_data['Account']['Name']}
        CRM NOTES: {sf_data['Description']}
        DELTA SCORE: {sf_data['CustomFields']['Delta_Score__c']} (Low score indicates risk)
        UPLOADED FILE CONTENT:
        {file_context}
        """
        
        prompt = f"""
        Act as a Strategic Bid Director. Perform a deep analysis on this Opportunity.
        DATA: {full_context}
        TASK: Output JSON only.
        OUTPUT JSON:
        {{
            "summary": "Strategic context summary...",
            "swot": {{ "strengths": [], "weaknesses": [], "opportunities": [], "threats": [] }},
            "win_thesis": "One sentence on why we win...",
            "lose_thesis": "One sentence on why we lose...",
            "stakeholder_intel": "Inferred motivations...",
            "win_probability": 45,
            "stakeholder_scores": [
                {{"name": "Name 1", "influence": 8, "support": 5}}
            ]
        }}
        """
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '')
        return json.loads(text)
    except Exception as e:
        st.error(f"AI Error: {e}")
        return fallback_data

def generate_html_report(sf_data, ai_data, uploaded_filenames, user_name):
    """Generates the exact HTML you loved in the demo."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    fmt_amount = f"${sf_data['Amount']:,.0f}" if sf_data['Amount'] else "N/A"
    
    # HTML Construction
    stakeholders_html = ""
    for c in sf_data.get('Contacts', []):
        name = c.get('Name')
        role = c.get('Role', 'Stakeholder')
        title = c.get('Title', '')
        stakeholders_html += f'<div style="margin-bottom:15px;"><strong style="display:block; color:white;">{name}</strong><span style="display:block; font-size:0.8rem; color:var(--c-stone);">{title}</span><span style="font-size:0.7rem; color:var(--c-tech-green);">{role}</span></div>'

    actions_html = ""
    for t in sf_data.get('Tasks', []):
        actions_html += f"<tr><td>{t['Subject']}</td><td>{t['Owner']['Name']}</td><td>{t['ActivityDate']}</td><td>{t['Status']}</td></tr>"

    chart_labels = [s['name'] for s in ai_data.get('stakeholder_scores', [])]
    chart_influence = [s['influence'] for s in ai_data.get('stakeholder_scores', [])]
    chart_support = [s['support'] for s in ai_data.get('stakeholder_scores', [])]
    
    win_prob = ai_data.get('win_probability', 30)
    delta_score = sf_data['CustomFields']['Delta_Score__c']

    # Your CSS from the demo
    css = """
    :root { --c-deep-blue: #0B2430; --c-tech-blue: #B7E1E1; --c-stone: #949088; --c-tech-green: #CBE7AC; --c-alert: #ff8b8b; --c-ai-purple: #C084FC; --glass-bg: rgba(255, 255, 255, 0.03); --glass-border: 1px solid rgba(183, 225, 225, 0.15); font-family: 'Inter', sans-serif; background-color: var(--c-deep-blue); color: #fff; line-height: 1.5; }
    body { margin: 0; padding: 20px; }
    .grid-header { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px; }
    .grid-main { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; }
    h1 { font-weight: 300; font-size: 2.0rem; margin: 0 0 5px 0; }
    .card { background: var(--glass-bg); border: var(--glass-border); padding: 20px; border-radius: 6px; margin-bottom: 30px; }
    .metric-box { background: rgba(183, 225, 225, 0.05); border: 1px solid rgba(183, 225, 225, 0.2); padding: 10px; border-radius: 4px; text-align: center; }
    .metric-label { font-family: 'Roboto Mono', monospace; font-size: 0.7rem; color: var(--c-tech-blue); text-transform: uppercase; display: block; margin-bottom: 5px; }
    .metric-value { font-size: 1.2rem; font-weight: 600; color: #fff; }
    .ai-field { border-left: 2px solid #C084FC; padding-left: 15px; background: linear-gradient(90deg, rgba(192, 132, 252, 0.05) 0%, transparent 100%); margin-bottom: 10px; }
    .swot-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
    .swot-box { padding: 10px; border-radius: 4px; font-size: 0.85rem; }
    .swot-s { background: rgba(203, 231, 172, 0.1); border-left: 3px solid var(--c-tech-green); }
    .swot-w { background: rgba(255, 139, 139, 0.1); border-left: 3px solid var(--c-alert); }
    .swot-o { background: rgba(183, 225, 225, 0.1); border-left: 3px solid var(--c-tech-blue); }
    .swot-t { background: rgba(255, 139, 139, 0.1); border-left: 3px solid var(--c-alert); }
    table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
    th { text-align: left; color: var(--c-tech-blue); border-bottom: 1px solid rgba(255,255,255,0.2); padding: 8px; }
    td { border-bottom: 1px solid rgba(255,255,255,0.05); padding: 8px; color: rgba(255,255,255,0.8); }
    .visual-container { height: 200px; position: relative; margin-bottom: 20px; }
    .gauge-wrapper { width: 100%; height: 50px; background: rgba(0,0,0,0.2); border-radius: 50px; position: relative; overflow: hidden; margin-top: 10px; }
    .gauge-fill { height: 100%; background: linear-gradient(90deg, #ff8b8b 0%, #CBE7AC 100%); width: """ + str(win_prob) + """%; }
    .gauge-val { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: bold; font-size: 1.0rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5); }
    """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>{css}</style>
        <script>
            window.onload = function() {{
                const ctx = document.getElementById('stakeholderChart').getContext('2d');
                new Chart(ctx, {{
                    type: 'radar',
                    data: {{
                        labels: {json.dumps(chart_labels)},
                        datasets: [
                            {{
                                label: 'Influence',
                                data: {json.dumps(chart_influence)},
                                backgroundColor: 'rgba(183, 225, 225, 0.2)',
                                borderColor: '#B7E1E1',
                                pointBackgroundColor: '#B7E1E1',
                            }},
                            {{
                                label: 'Support',
                                data: {json.dumps(chart_support)},
                                backgroundColor: 'rgba(203, 231, 172, 0.2)',
                                borderColor: '#CBE7AC',
                                pointBackgroundColor: '#CBE7AC',
                            }}
                        ]
                    }},
                    options: {{
                        scales: {{
                            r: {{
                                angleLines: {{ color: 'rgba(255, 255, 255, 0.1)' }},
                                grid: {{ color: 'rgba(255, 255, 255, 0.1)' }},
                                pointLabels: {{ color: '#fff', font: {{ size: 10 }} }},
                                ticks: {{ display: false, max: 10 }}
                            }}
                        }},
                        plugins: {{ legend: {{ labels: {{ color: '#fff' }} }} }}
                    }}
                }});
            }};
        </script>
    </head>
    <body>
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom: 20px;">
            <div>
                <h1>{sf_data['Name']}</h1>
                <span style="color: var(--c-stone); font-family: 'Roboto Mono';">Account: {sf_data['Account']['Name']}</span>
            </div>
            <div style="text-align:right;">
                 <span style="display:block; font-size:0.75rem; color:var(--c-stone);">Opportunity Owner</span>
                 <strong style="color:var(--c-tech-blue);">{sf_data['Owner']['Name']}</strong>
            </div>
        </div>

        <div class="grid-header">
            <div class="metric-box"><span class="metric-label">Stage</span><span style="color:var(--c-tech-green); font-weight:600;">{sf_data['StageName']}</span></div>
            <div class="metric-box"><span class="metric-label">Close Date</span><span class="metric-value">{sf_data['CloseDate']}</span></div>
            <div class="metric-box"><span class="metric-label">Amount</span><span class="metric-value">{fmt_amount}</span></div>
            <div class="metric-box"><span class="metric-label">Delta Score</span><span class="metric-value" style="color:var(--c-alert);">{delta_score}</span></div>
        </div>

        <div class="grid-main">
            <div>
                <div class="card">
                    <h2 style="color:var(--c-tech-blue); text-transform:uppercase; font-size:1.1rem; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px;">Strategic Context</h2>
                    <div class="ai-field">
                        <strong style="color:#C084FC; font-size:0.75rem; text-transform:uppercase; display:block; margin-bottom:5px;">AI Extracted Insight</strong>
                        <p style="color: rgba(255,255,255,0.9);">{ai_data['summary']}</p>
                    </div>
                    <div style="margin-top:15px; border-top:1px solid rgba(255,255,255,0.1); padding-top:10px;">
                        <strong style="color:#C084FC; font-size:0.75rem; text-transform:uppercase; display:block;">Stakeholder Intel (AI Profiling)</strong>
                        <p style="color: rgba(255,255,255,0.8); font-size:0.85rem;">{ai_data['stakeholder_intel']}</p>
                    </div>
                </div>
                
                <div class="card">
                    <h2 style="color:var(--c-tech-blue); text-transform:uppercase; font-size:1.1rem; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px;">Win Probability</h2>
                    <div class="gauge-wrapper">
                        <div class="gauge-fill"></div>
                        <div class="gauge-val">{win_prob}% AI Confidence</div>
                    </div>
                </div>

                <div class="card">
                    <h2 style="color:var(--c-tech-blue); text-transform:uppercase; font-size:1.1rem; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px;">SWOT Analysis</h2>
                    <div class="ai-field">
                        <div class="swot-grid">
                            <div class="swot-box swot-s"><strong style="color:var(--c-tech-green)">STRENGTHS</strong><ul>{''.join([f"<li>{s}</li>" for s in ai_data['swot']['strengths']])}</ul></div>
                            <div class="swot-box swot-w"><strong style="color:var(--c-alert)">WEAKNESSES</strong><ul>{''.join([f"<li>{s}</li>" for s in ai_data['swot']['weaknesses']])}</ul></div>
                            <div class="swot-box swot-o"><strong style="color:var(--c-tech-blue)">OPPORTUNITIES</strong><ul>{''.join([f"<li>{s}</li>" for s in ai_data['swot']['opportunities']])}</ul></div>
                            <div class="swot-box swot-t"><strong style="color:var(--c-alert)">THREATS</strong><ul>{''.join([f"<li>{s}</li>" for s in ai_data['swot']['threats']])}</ul></div>
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <div class="card">
                    <h2 style="color:var(--c-tech-blue); text-transform:uppercase; font-size:1.1rem; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px;">Stakeholder Influence Map</h2>
                    <div class="visual-container">
                        <canvas id="stakeholderChart"></canvas>
                    </div>
                    <div style="margin-top:20px;">
                        {stakeholders_html}
                    </div>
                </div>
                
                <div class="card"><h2 style="color:var(--c-tech-blue); text-transform:uppercase; font-size:1.1rem; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px;">Action Plan</h2><table><thead><tr><th>Task</th><th>Owner</th><th>Date</th><th>Status</th></tr></thead><tbody>{actions_html}</tbody></table></div>
                
                <div class="card">
                    <h2 style="color:var(--c-tech-blue); text-transform:uppercase; font-size:1.1rem; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px;">Win Thesis</h2>
                    <div class="ai-field">
                        <div style="margin-bottom: 20px;"><strong style="color:var(--c-tech-green); font-size:0.85rem;">WHY WE WIN</strong><p style="font-size:0.85rem; color:rgba(255,255,255,0.8); margin-top:5px;">{ai_data['win_thesis']}</p></div>
                        <div><strong style="color:var(--c-alert); font-size:0.85rem;">WHY WE LOSE</strong><p style="font-size:0.85rem; color:rgba(255,255,255,0.8); margin-top:5px;">{ai_data['lose_thesis']}</p></div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top:20px; color:#555; font-size:0.7rem;">Generated by Connected Intelligence Engine | User: {user_name} | {timestamp}</div>
    </body>
    </html>
    """
    return html

# --- 3. EXECUTION ---

st.title("Connected Global Intelligence Engine")
st.markdown("Upload the SGS file to begin the Deep Research simulation.")

if uploaded_file:
    # RUN BUTTON
    if st.button("🚀 Run Deep Analysis"):
        sf_data = agent_salesforce_mimic()
        
        with st.spinner("🧠 AI Agent Reading Documents..."):
            file_text, file_names = agent_document_parser(uploaded_file)
        
        with st.spinner("💡 Formulating Strategy..."):
            ai_data = agent_strategy_brain(sf_data, file_text, api_key)
            
        st.success("Analysis Complete")
        
        # Generate HTML
        html_report = generate_html_report(sf_data, ai_data, file_names, user_name_input)
        
        # Display HTML in Streamlit
        components.html(html_report, height=1200, scrolling=True)
        
        # Download Button
        st.download_button(
            label="Download PDF Report (HTML)",
            data=html_report,
            file_name=f"{sf_data['Name']}_Win_Map.html",
            mime="text/html"
        )
else:
    st.info("👈 Please upload the 'SGS - Perth.pdf' in the sidebar to start.")