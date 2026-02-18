import streamlit as st
import pandas as pd
import plotly.express as px
import os
import re
from datetime import datetime, date

# ---------------------------------------------------------
# CONFIG GÉNÉRALE
# ---------------------------------------------------------
st.set_page_config(
    page_title="CYBER SÉCURITÉ – Dashboard",
    layout="wide"
)

# ---------------------------------------------------------
# CSS GLOBAL (fond sombre technique, sans encart blanc) - Design cyber intemporel et technique
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap');
    
    body {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
        font-family: 'JetBrains Mono', monospace;
        color: #00d4ff;
    }
    .main {
        background: transparent;
        padding: 20px;
    }
    .cyber-title {
        text-align: center;
        color: #00ff88;
        font-size: 32px;
        font-weight: 600;
        letter-spacing: 2px;
        text-shadow: 0 0 10px #00ff88;
        margin-bottom: 8px;
    }
    .cyber-subtitle {
        text-align: center;
        color: #00d4ff;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .module-label {
        text-align: center;
        color: #ffffff;
        font-size: 16px;
        margin-top: 12px;
        margin-bottom: 8px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #00d4ff;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #00d4ff;
        font-weight: 600;
        font-size: 14px;
        padding: 10px 0;
        box-shadow: 0 0 10px rgba(0,212,255,0.5);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #16213e 0%, #0f0f23 100%);
        box-shadow: 0 0 20px rgba(0,212,255,0.8);
        transform: translateY(-2px);
    }
    .section-title {
        color: #00ff88;
        font-size: 24px;
        font-weight: 600;
        margin-top: 16px;
        text-shadow: 0 0 5px #00ff88;
    }
    .section-sub {
        color: #00d4ff;
        font-size: 14px;
        margin-bottom: 12px;
    }
    .terminal-style {
        background: rgba(0,0,0,0.8);
        border: 1px solid #00d4ff;
        border-radius: 8px;
        padding: 10px;
        font-family: 'JetBrains Mono', monospace;
        color: #00ff88;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# STATE NAVIGATION
# ---------------------------------------------------------
if "module" not in st.session_state:
    st.session_state.module = "vuln"  # par défaut

def set_module(name: str):
    st.session_state.module = name

# ---------------------------------------------------------
# HEADER : LOGO + TITRE + NAV (sans encart blanc, layout direct)
# ---------------------------------------------------------
col_logo, col_text = st.columns([1, 2])

with col_logo:
    if os.path.exists("interface_cyber.jpg"):
        st.image("interface_cyber.jpg", use_column_width=True)
    else:
        st.warning("⚠️ Placez le fichier 'interface_cyber.jpg' dans le même dossier que app.py")

with col_text:
    st.markdown('<div class="cyber-title">CYBER SÉCURITÉ – DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="cyber-subtitle">'
        'Vulnérabilités • Attaques • Mots de passe • Firewall • MFA'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="module-label">Choisissez un module pour continuer :</div>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("🌍 Vulnérabilités"):
            set_module("vuln")
    with c2:
        if st.button("🔒 Mots de passe"):
            set_module("pwd")
    with c3:
        if st.button("🛡️ Firewall"):
            set_module("fw")
    with c4:
        if st.button("🏠 Attaques"):
            set_module("attacks")
    with c5:
        if st.button("📝 Explications / MFA"):
            set_module("note")

st.write("")  # petit espace

# ---------------------------------------------------------
# DONNÉES VULN (COMMUNES) - Avec gestion d'erreurs
# ---------------------------------------------------------
CSV_FILE = "vulnerabilites.csv"

try:
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(
            columns=["Nom", "CVE", "Criticité", "Service", "Description", "Solution", "Date"]
        )
        df.to_csv(CSV_FILE, index=False)

    df = pd.read_csv(CSV_FILE)

    if "Date" not in df.columns:
        df["Date"] = datetime.now().date()
    else:
        try:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
        except Exception:
            df["Date"] = datetime.now().date()

    df.to_csv(CSV_FILE, index=False)
except Exception as e:
    st.error(f"Erreur lors du chargement du CSV : {e}")
    df = pd.DataFrame(columns=["Nom", "CVE", "Criticité", "Service", "Description", "Solution", "Date"])

# ---------------------------------------------------------
# MODULE : VULNÉRABILITÉS - Correction de append
# ---------------------------------------------------------
if st.session_state.module == "vuln":
    st.markdown('<div class="section-title">🌍 Vulnérabilités</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Ajoutez, visualisez et analysez les vulnérabilités détectées.</div>',
        unsafe_allow_html=True
    )

    with st.form("form_vuln"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom de la vulnérabilité")
            cve = st.text_input("CVE (ex: CVE-2021-1234)")
            criticite = st.selectbox("Criticité", ["Faible", "Moyenne", "Élevée", "Critique"])
        with col2:
            service = st.text_input("Service / Port")
            description = st.text_area("Description")
            solution = st.text_area("Solution / Remédiation")
        submit = st.form_submit_button("Ajouter")

    if submit:
        new_row = {
            "Nom": nom,
            "CVE": cve,
            "Criticité": criticite,
            "Service": service,
            "Description": description,
            "Solution": solution,
            "Date": datetime.now().date(),
        }
        # Correction : Utiliser pd.concat au lieu de append déprécié
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.success("✅ Vulnérabilité ajoutée.")

    st.subheader("📋 Tableau des vulnérabilités")
    st.dataframe(df, use_container_width=True)

    # suppression d'une ligne
    if not df.empty:
        st.markdown("### ❌ Supprimer une vulnérabilité")
        # propose une liste lisible avec index
        options = [f"{idx} - {row['Nom']} ({row.get('CVE','')})" for idx, row in df.iterrows()]
        choice = st.selectbox("Sélectionner la ligne à supprimer", options)
        if st.button("Supprimer la ligne sélectionnée"):
            try:
                idx_to_remove = int(choice.split(" - ")[0])
                df = df.drop(idx_to_remove).reset_index(drop=True)
                df.to_csv(CSV_FILE, index=False)
                st.success("✅ Ligne supprimée.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Erreur lors de la suppression : {e}")

        # génération de rapport
        st.markdown("### 📄 Générer un rapport technique")
        def make_txt_report(frame: pd.DataFrame) -> str:
            parts = ["Rapport de vulnérabilités\n", "Generated: " + str(datetime.now()) + "\n\n"]
            for i, r in frame.iterrows():
                parts.append(f"[{i}] Nom: {r['Nom']}\n")
                parts.append(f"    CVE: {r.get('CVE','')}\n")
                parts.append(f"    Criticité: {r.get('Criticité','')}\n")
                parts.append(f"    Service: {r.get('Service','')}\n")
                parts.append(f"    Description: {r.get('Description','')}\n")
                parts.append(f"    Solution: {r.get('Solution','')}\n")
                parts.append(f"    Date: {r.get('Date','')}\n\n")
            return "".join(parts)

        def make_pdf_report(frame: pd.DataFrame) -> bytes:
            try:
                from fpdf import FPDF
            except ImportError:
                st.error('Bibliothèque fpdf manquante ; ajoutez-la à requirements.txt et réinstallez.')
                return b""
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Rapport de vulnérabilités", ln=True, align="C")
            pdf.ln(4)
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 6, f"Generated: {datetime.now()}", ln=True)
            pdf.ln(4)
            for i, r in frame.iterrows():
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 6, f"[{i}] {r['Nom']}", ln=True)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 5, f"CVE: {r.get('CVE','')} | Criticité: {r.get('Criticité','')}")
                pdf.multi_cell(0, 5, f"Service: {r.get('Service','')} | Date: {r.get('Date','')}")
                pdf.multi_cell(0, 5, f"Description: {r.get('Description','')}")
                pdf.multi_cell(0, 5, f"Solution: {r.get('Solution','')}")
                pdf.ln(2)
            return pdf.output(dest='S').encode('latin-1')

        txt_report = make_txt_report(df)
        pdf_report = make_pdf_report(df)

        st.download_button(
            label="Télécharger le rapport (TXT)",
            data=txt_report,
            file_name="rapport_vulnerabilites.txt",
            mime="text/plain",
        )
        if pdf_report:
            st.download_button(
                label="Télécharger le rapport (PDF)",
                data=pdf_report,
                file_name="rapport_vulnerabilites.pdf",
                mime="application/pdf",
            )

    if not df.empty:
        col_a, col_b = st.columns(2)

        with col_a:
            attacks_per_day = df.groupby("Date").size().reset_index(name="Nombre")
            fig = px.line(
                attacks_per_day,
                x="Date",
                y="Nombre",
                markers=True,
                title="Évolution des vulnérabilités recensées",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            crit_counts = df["Criticité"].value_counts().reset_index()
            crit_counts.columns = ["Criticité", "Nombre"]
            fig2 = px.pie(
                crit_counts,
                names="Criticité",
                values="Nombre",
                title="Répartition par criticité",
            )
            st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------
# MODULE : MOTS DE PASSE
# ---------------------------------------------------------
if st.session_state.module == "pwd":
    st.markdown('<div class="section-title">🔒 Sécurité des mots de passe</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Testez la robustesse d’un mot de passe et sa présence dans rockyou.txt.</div>',
        unsafe_allow_html=True
    )

    pwd = st.text_input("Entrez un mot de passe à tester", type="password")

    def password_strength(p):
        score = 0
        criteria = []

        if len(p) >= 8:
            score += 1
            criteria.append("✔ Longueur suffisante (≥ 8)")
        else:
            criteria.append("✖ Trop court (< 8)")

        if re.search(r"[A-Z]", p):
            score += 1
            criteria.append("✔ Majuscules")
        else:
            criteria.append("✖ Pas de majuscules")

        if re.search(r"[a-z]", p):
            score += 1
            criteria.append("✔ Minuscules")
        else:
            criteria.append("✖ Pas de minuscules")

        if re.search(r"\d", p):
            score += 1
            criteria.append("✔ Chiffres")
        else:
            criteria.append("✖ Pas de chiffres")

        if re.search(r"[^A-Za-z0-9]", p):
            score += 1
            criteria.append("✔ Caractères spéciaux")
        else:
            criteria.append("✖ Pas de caractères spéciaux")

        return score, criteria

    def check_rockyou(password):
        if not os.path.exists("rockyou.txt"):
            return False, "⚠️ Fichier rockyou.txt introuvable dans le dossier."
        try:
            with open("rockyou.txt", "r", encoding="latin-1", errors="ignore") as f:
                for line in f:
                    if password == line.strip():
                        return True, "❌ Mot de passe présent dans rockyou.txt."
            return False, "✔ Mot de passe non présent dans rockyou.txt."
        except Exception as e:
            return False, f"Erreur lors de la lecture de rockyou.txt : {e}"

    if pwd:
        score, criteria = password_strength(pwd)
        found, msg = check_rockyou(pwd)

        st.write(f"### Score global : {score}/5")
        st.write(msg)
        st.write("### Détails :")
        for c in criteria:
            st.write("-", c)

# ---------------------------------------------------------
# MODULE : FIREWALL
# ---------------------------------------------------------
if st.session_state.module == "fw":
    st.markdown('<div class="section-title">🛡️ Firewall</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Rôle du pare-feu dans la réduction de la surface d’attaque.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
    <div class="terminal-style">
    - Filtre le trafic entrant et sortant pour bloquer les connexions malveillantes  
    - Réduit la surface d’attaque exposée à Internet  
    - Empêche certains scans de ports et tentatives d’exploitation  
    - Complète la sécurité des mots de passe et du MFA  
    </div>
    """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# MODULE : ATTAQUES
# ---------------------------------------------------------
if st.session_state.module == "attacks":
    st.markdown('<div class="section-title">🏠 Attaques</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Vue synthétique des attaques ou campagnes détectées.</div>',
        unsafe_allow_html=True
    )

    data = pd.DataFrame(
        {
            "Date": pd.date_range(end=date.today(), periods=10),
            "Attaques": [5, 12, 7, 15, 9, 4, 11, 6, 13, 8],
        }
    )

    col_t, col_g = st.columns([1, 2])

    with col_t:
        st.subheader("📅 Détail")
        st.dataframe(data, use_container_width=True)

    with col_g:
        st.subheader("📊 Volume d’attaques")
        fig = px.bar(data, x="Date", y="Attaques", title="Attaques par jour")
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# MODULE : EXPLICATIONS / MFA
# ---------------------------------------------------------
if st.session_state.module == "note":
    st.markdown('<div class="section-title">📝 Explications & MFA</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Rappels sur les bonnes pratiques de mots de passe et l’intérêt du MFA.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
    <div class="terminal-style">
    ### Risques des mots de passe faibles
    - Cassables en quelques secondes  
    - Très présents dans des dictionnaires comme rockyou.txt  
    - Souvent réutilisés sur plusieurs services  
    - Vulnérables aux attaques automatisées  

    ### Pourquoi activer le MFA
    - Protège même si le mot de passe est compromis  
    - Bloque une grande partie des attaques par phishing  
    - Ajoute une couche indépendante du mot de passe  
    - Indispensable pour les comptes sensibles (mail, banque, accès pro, etc.)  

    ### Bonnes pratiques
    - Utiliser un gestionnaire de mots de passe  
    - Générer des mots de passe longs (12+ caractères) et uniques  
    - Activer le MFA partout où c’est possible  
    - Ne jamais réutiliser le même mot de passe  
    </div>
    """,
        unsafe_allow_html=True
    )


