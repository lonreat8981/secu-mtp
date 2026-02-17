import streamlit as st
import pandas as pd
import plotly.express as px
import os
import re
from datetime import datetime, date
from PIL import Image

# ---------------------------------------------------------
# CONFIG GÉNÉRALE
# ---------------------------------------------------------
st.set_page_config(
    page_title="CYBER SÉCURITÉ – Dashboard",
    layout="wide"
)

px.defaults.template = "plotly_dark"

# ---------------------------------------------------------
# CSS GLOBAL (fond, carte centrale, boutons)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    body {
        background: radial-gradient(circle at top, #0f172a 0, #020617 45%, #000000 100%);
    }
    .main {
        background: transparent;
    }
    .cyber-card {
        max-width: 1100px;
        margin: 20px auto 10px auto;
        padding: 24px 28px;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(15,23,42,0.85));
        border: 1px solid rgba(56,189,248,0.5);
        box-shadow: 0 0 35px rgba(15,23,42,0.9);
    }
    .cyber-title {
        text-align: center;
        color: #e5f4ff;
        font-size: 30px;
        font-weight: 800;
        letter-spacing: 3px;
        margin-bottom: 4px;
    }
    .cyber-subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 13px;
        margin-bottom: 16px;
    }
    .module-label {
        text-align: center;
        color: #e5e7eb;
        font-size: 14px;
        margin-top: 10px;
        margin-bottom: 6px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 999px;
        border: 1px solid rgba(148,163,184,0.6);
        background: radial-gradient(circle at top left, #0ea5e9 0, #020617 55%);
        color: #e5f4ff;
        font-weight: 600;
        font-size: 13px;
        padding: 8px 0;
        box-shadow: 0 0 12px rgba(56,189,248,0.4);
        transition: all 0.15s ease-in-out;
    }
    .stButton>button:hover {
        border-color: #38bdf8;
        box-shadow: 0 0 18px rgba(56,189,248,0.8);
        transform: translateY(-1px);
    }
    .section-title {
        color: #e5f4ff;
        font-size: 20px;
        font-weight: 700;
        margin-top: 10px;
    }
    .section-sub {
        color: #9ca3af;
        font-size: 13px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# IMAGE + CARDS + GRAPHIQUE
# ---------------------------------------------------------
image = Image.open("interface_cyber.jpg")
st.image(image, use_column_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Vulnérabilités critiques", 12)
col2.metric("Vulnérabilités hautes", 27)
col3.metric("Vulnérabilités moyennes", 41)

st.markdown("---")

df_stats = pd.DataFrame({
    "Type": ["Critique", "Haute", "Moyenne"],
    "Nombre": [12, 27, 41]
})

fig_stats = px.bar(df_stats, x="Type", y="Nombre", title="Répartition des vulnérabilités")
st.plotly_chart(fig_stats, use_container_width=True)

# ---------------------------------------------------------
# STATE NAVIGATION
# ---------------------------------------------------------
if "module" not in st.session_state:
    st.session_state.module = "vuln"

def set_module(name: str):
    st.session_state.module = name

# ---------------------------------------------------------
# CARTE CENTRALE : LOGO + TITRE + NAV
# ---------------------------------------------------------
with st.container():
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)

    col_logo, col_text = st.columns([1, 2])

    with col_logo:
        if os.path.exists("interface_cyber.jpg"):
            st.image("interface_cyber.jpg", use_column_width=True)
        else:
            st.error("⚠️ Place ton fichier 'interface_cyber.jpg' dans le même dossier que app.py")

    with col_text:
        st.markdown('<div class="cyber-title">CYBER SÉCURITÉ – DASHBOARD</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="cyber-subtitle">'
            'Vulnérabilités • Attaques • Mots de passe • Firewall • MFA'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="module-label">Choisis un module pour continuer :</div>', unsafe_allow_html=True)

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

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------------
# DONNÉES VULN
# ---------------------------------------------------------
CSV_FILE = "vulnerabilites.csv"

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

# ---------------------------------------------------------
# MODULE : VULNÉRABILITÉS
# ---------------------------------------------------------
if st.session_state.module == "vuln":
    st.markdown('<div class="section-title">🌍 Vulnérabilités</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Ajoute, visualise et analyse les vulnérabilités détectées.</div>',
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
        df = df._append(new_row, ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.success("✅ Vulnérabilité ajoutée.")

    st.subheader("📋 Tableau des vulnérabilités")
    st.dataframe(df, use_container_width=True)

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
        '<div class="section-sub">Teste la robustesse d’un mot de passe et sa présence dans rockyou.txt.</div>',
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
        with open("rockyou.txt", "r", encoding="latin-1", errors="ignore") as f:
            for line in f:
                if password == line.strip():
                    return True, "❌ Mot de passe présent dans rockyou.txt."
        return False, "✔ Mot de passe non présent dans rockyou.txt."

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
- Filtre le trafic entrant et sortant pour bloquer les connexions malveillantes  
- Réduit la surface d’attaque exposée à Internet  
- Empêche certains scans de ports et tentatives d’exploitation  
- Complète la sécurité des mots de passe et du MFA  
"""
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
"""
    )



