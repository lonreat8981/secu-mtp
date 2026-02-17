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
# CSS GLOBAL + IMAGE DE FOND
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    body {
        background-image: url('interface_cyber.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main {
        background: rgba(0,0,0,0.55);
        padding: 20px;
        border-radius: 15px;
    }
    .icon-btn {
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        background: rgba(15,23,42,0.75);
        border: 1px solid rgba(56,189,248,0.5);
        color: #e5f4ff;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: 0.2s;
    }
    .icon-btn:hover {
        background: rgba(56,189,248,0.3);
        transform: scale(1.05);
    }
    .section-title {
        color: #e5f4ff;
        font-size: 26px;
        font-weight: 800;
        margin-top: 10px;
    }
    .section-sub {
        color: #cbd5e1;
        font-size: 15px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# STATE NAVIGATION
# ---------------------------------------------------------
if "module" not in st.session_state:
    st.session_state.module = "home"

def set_module(name: str):
    st.session_state.module = name

# ---------------------------------------------------------
# PAGE D’ACCUEIL AVEC ICÔNES INTERACTIVES
# ---------------------------------------------------------
if st.session_state.module == "home":

    st.markdown("<h1 style='text-align:center;color:white;'>CYBER SÉCURITÉ – DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#cbd5e1;'>Choisis un module pour continuer</p>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("🌍\nVulnérabilités"):
            set_module("vuln")

    with col2:
        if st.button("🔒\nMots de passe"):
            set_module("pwd")

    with col3:
        if st.button("🛡️\nFirewall"):
            set_module("fw")

    with col4:
        if st.button("🏠\nAttaques"):
            set_module("attacks")

    with col5:
        if st.button("📝\nExplications / MFA"):
            set_module("note")

    st.stop()

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
    st.markdown('<div class="section-sub">Ajoute, visualise et analyse les vulnérabilités détectées.</div>', unsafe_allow_html=True)

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
            fig = px.line(attacks_per_day, x="Date", y="Nombre", markers=True, title="Évolution des vulnérabilités")
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            crit_counts = df["Criticité"].value_counts().reset_index()
            crit_counts.columns = ["Criticité", "Nombre"]
            fig2 = px.pie(crit_counts, names="Criticité", values="Nombre", title="Répartition par criticité")
            st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------
# MODULE : MOTS DE PASSE
# ---------------------------------------------------------
if st.session_state.module == "pwd":
    st.markdown('<div class="section-title">🔒 Sécurité des mots de passe</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Teste la robustesse d’un mot de passe et sa présence dans rockyou.txt.</div>', unsafe_allow_html=True)

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
            return False, "⚠️ Fichier rockyou.txt introuvable."
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
    st.markdown('<div class="section-sub">Rôle du pare-feu dans la réduction de la surface d’attaque.</div>', unsafe_allow_html=True)

    st.markdown(
        """
- Filtre le trafic entrant et sortant  
- Réduit la surface d’attaque exposée  
- Empêche scans de ports et exploits  
- Complète mots de passe + MFA  
"""
    )

# ---------------------------------------------------------
# MODULE : ATTAQUES
# ---------------------------------------------------------
if st.session_state.module == "attacks":
    st.markdown('<div class="section-title">🏠 Attaques</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Vue synthétique des attaques détectées.</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="section-sub">Rappels sur les bonnes pratiques et l’intérêt du MFA.</div>', unsafe_allow_html=True)

    st.markdown(
        """
### Risques des mots de passe faibles
- Cassables en quelques secondes  
- Très présents dans rockyou.txt  
- Réutilisés sur plusieurs services  
- Vulnérables aux attaques automatisées  

### Pourquoi activer le MFA
- Protège même si le mot de passe fuit  
- Bloque une grande partie du phishing  
- Ajoute une couche indépendante  
- Indispensable pour les comptes sensibles  

### Bonnes pratiques
- Utiliser un gestionnaire  
- Générer des mots de passe longs  
- Activer le MFA partout  
- Ne jamais réutiliser un mot de passe  
"""
    )


     
