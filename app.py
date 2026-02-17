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
# CSS GLOBAL (fond, carte centrale, boutons) - Amélioré pour un design intemporel
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    body {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        font-family: 'Inter', sans-serif;
        color: #1e293b;
    }
    .main {
        background: transparent;
        padding: 20px;
    }
    .cyber-card {
        max-width: 1200px;
        margin: 20px auto 10px auto;
        padding: 32px 40px;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9));
        border: 1px solid rgba(148,163,184,0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: box-shadow 0.3s ease;
    }
    .cyber-card:hover {
        box-shadow: 0 12px 48px rgba(0,0,0,0.15);
    }
    .cyber-title {
        text-align: center;
        color: #0f172a;
        font-size: 32px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .cyber-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .module-label {
        text-align: center;
        color: #374151;
        font-size: 16px;
        margin-top: 12px;
        margin-bottom: 8px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid rgba(148,163,184,0.4);
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: #ffffff;
        font-weight: 600;
        font-size: 14px;
        padding: 10px 0;
        box-shadow: 0 4px 12px rgba(59,130,246,0.3);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 20px rgba(59,130,246,0.5);
        transform: translateY(-2px);
    }
    .section-title {
        color: #0f172a;
        font-size: 24px;
        font-weight: 700;
        margin-top: 16px;
    }
    .section-sub {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 12px;
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
# CARTE CENTRALE : LOGO + TITRE + NAV
# ---------------------------------------------------------
with st.container():
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)

    # Ligne logo + titre
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

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")  # petit espace sous la carte

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
    


