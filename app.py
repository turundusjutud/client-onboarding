import streamlit as st
from PIL import Image
import os

# --- LEHE SEADISTUSED ---
st.set_page_config(
    page_title="Turundusjutud | Onboarding",
    page_icon="📣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- BRÄNDI VÄRVID JA STIIL (CSS) ---
# Kasutame sinu brändi värve: 
# Teal: #1A776F, Dark: #052623, Orange: #FF7F40, Yellow: #FFC876, Bg: #FAFAFA
def local_css():
    st.markdown("""
    <style>
        /* Põhitaust */
        .stApp {
            background-color: #FAFAFA;
            color: #2E3A39;
            font-family: 'Helvetica', 'Arial', sans-serif; /* Aftika asendus */
        }
        
        /* Sidebar taust */
        [data-testid="stSidebar"] {
            background-color: #052623;
        }
        [data-testid="stSidebar"] * {
            color: #FAFAFA !important;
        }

        /* Pealkirjad */
        h1, h2, h3 {
            color: #1A776F !important;
            font-weight: 700;
        }
        
        /* Sektsiooni eraldajad */
        hr {
            border-color: #FFC876;
        }

        /* Nupud (Orange) */
        .stButton>button {
            background-color: #FF7F40;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #e66b2e;
            color: white;
            border: none;
        }

        /* Info kastid */
        .info-box {
            padding: 20px;
            border-radius: 10px;
            background-color: #ffffff;
            border-left: 5px solid #1A776F;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        /* Protsessi sammud */
        .step-header {
            font-size: 24px;
            color: #052623;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- FUNKTSIOONID LEHTEDE JAOKS ---

def show_intro():
    st.title("Tere tulemast Turundusjuttudesse! 👋")
    st.markdown("### Sinu teejuht edukate Google Ads kampaaniateni")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Olen väga rõõmus, et tunned huvi koostöö vastu. Minu eesmärk ei ole lihtsalt reklaame üles panna, 
        vaid ehitada süsteem, mis toob sulle reaalselt kasumit.
        
        Selleks, et meie koostöö oleks sujuv ja läbipaistev, olen loonud selle **5-etapilise protsessi**.
        Vasakult menüüst saad liikuda läbi etappide, et näha täpselt, mis meid ees ootab.
        """)
        
        st.info("💡 **Miks see protsess hea on?** Sest see välistab üllatused. Sina tead täpselt, mille eest maksad, ja mina saan keskenduda tulemustele.")

    with col2:
        # Siia võiksid panna brändielemendi pildi
        st.markdown(
            """
            <div style="background-color:#1A776F; padding:20px; border-radius:15px; text-align:center;">
                <h1 style="color:white !important; font-size: 50px;">🚀</h1>
                <p style="color:white;">Valmis stardiks?</p>
            </div>
            """, unsafe_allow_html=True
        )

def show_step1():
    st.header("1. Samm: Tutvustav kõne (Intro)")
    st.markdown("##### Eesmärk: Sobivuse ja potentsiaali hindamine")
    
    st.markdown("""
    <div class="info-box">
    Selles faasis me ei sukellu veel tehnilistesse detailidesse. Meie eesmärk on aru saada, kas Google Ads on sinu ärile praegu õige tööriist.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("✅ **Mida me arutame:**")
        st.markdown("""
        * Sinu äri hetkeseis ja eesmärgid.
        * Sinu ideaalne klient.
        * Varasemad kogemused reklaamiga.
        * Eelarve raamid.
        """)
    with col2:
        st.markdown("❌ **Mida me EI tee:**")
        st.markdown("""
        * Ma ei logi veel sinu kontole sisse.
        * Ma ei tee tasuta auditit (selgitame 4. sammus miks).
        * Me ei sea üles kampaaniaid.
        """)

def show_step2():
    st.header("2. Samm: Hinnapakkumine ja Strateegia")
    st.markdown("##### Eesmärk: Fikseerida töömaht ja investeering")
    
    st.write("Pärast meie kõne koostan ma personaalse pakkumise. Minu hinnastus on läbipaistev ja koosneb kahest osast:")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
        ### 1. Ühekordne Häälestustasu
        **Sisaldab:**
        * 🔍 Konto süva-audit (Paid Diagnostic)
        * 🛠 Tehniline seadistus (GA4, GTM)
        * 🎯 Märksõnade uuring ja strateegia
        * 🚫 Negatiivsete märksõnade listid
        """)
        
    with c2:
        st.markdown("""
        ### 2. Igakuine Haldustasu
        **Sisaldab:**
        * 📈 Iganädalane optimeerimine
        * 🧪 A/B testimine
        * 📊 Raporteerimine
        * 📞 Jooksev suhtlus
        """)

    st.warning("⚠️ **NB!** Audit on eraldi tasustatud teenus, sest see on põhjalik diagnostika, mille tulemused (raport) jäävad sulle.")

def show_step3():
    st.header("3. Samm: Leping ja Turvalisus")
    st.markdown("##### Eesmärk: Juriidiline korrektsus ja andmekaitse")
    
    st.markdown("""
    <div class="info-box">
    Enne töö alustamist vormistame kõik korrektselt. See kaitseb nii sind kui mind.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **Selles etapis toimub:**
    1. **NDA (Konfidentsiaalsusleping):** Sinu ärisaladused on kaitstud.
    2. **Teenusleping:** Fikseerime kohustused ja tähtajad.
    3. **Ettemaks:** Auditi ja seadistuse arve tasumine.
    """)
    
    st.error("🛑 Ma ei küsi ligipääsu sinu kontodele enne, kui paberid on korras. See on sinu andmete turvalisuse huvides.")

def show_step4():
    st.header("4. Samm: Ligipääs ja Tasuline Audit 🕵️‍♂️")
    st.markdown("##### Eesmärk: Diagnoos ja 'Musta kasti' avamine")
    
    st.markdown("See on faas, mille eest sa maksid ühekordse tasu. Nüüd algab päris töö.")
    
    with st.expander("Miks audit on tasuline?", expanded=True):
        st.write("""
        Paljud agentuurid teevad tasuta "auditeid", mis on tegelikult müügitrikid. 
        Minu audit on **meditsiiniline läbivaatus**. Ma lähen koodi tasandile, kontrollin, kas sinu veebileht
        üldse saadab Google'ile õigeid andmeid, ja analüüsin, kuhu raha kaob.
        """)
    
    st.subheader("Mida ma kontrollin:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 🎯 Tracking")
        st.caption("Kas ostud/päringud tegelikult mõõdetakse? Kas GA4 ja Google Ads räägivad ühte keelt?")
    with col2:
        st.markdown("#### 💸 Kulutused")
        st.caption("Search Terms reporti analüüs – kui palju raha kulub ebaolulistele märksõnadele?")
    with col3:
        st.markdown("#### ⚙️ Struktuur")
        st.caption("Kas kampaaniad on loogiliselt üles ehitatud või on kõik 'segasummasuvila'?")

    st.success("Tulemus: Põhjalik PDF raport vigadest ja parendusettepanekutest.")

def show_step5():
    st.header("5. Samm: Strateegia ja Käivitamine 🚀")
    st.markdown("##### Eesmärk: Tulemuste toomine")
    
    st.write("Kui audit on tehtud, esitlen sulle tulemusi ja 90-päeva plaani.")
    
    timeline = {
        "Nädal 1": "Kampaaniate ehitus ja reklaamtekstide kinnitamine",
        "Nädal 2-4": "Õppimisperiood (Learning Phase) - algoritm kogub andmeid",
        "Kuu 2": "Optimeerimine ja CPA (Cost Per Acquisition) alandamine",
        "Kuu 3": "Skaleerimine - tõstame eelarvet seal, mis töötab"
    }
    
    for time, activity in timeline.items():
        st.markdown(f"**{time}:** {activity}")
        st.progress(100 if time == "Nädal 1" else (70 if "2-4" in time else (40 if "Kuu 2" in time else 10)))

# --- SIDEBAR NAVIGATSIOON ---

with st.sidebar:
    # Proovi laadida logo, kui fail puudub, kuva tekst
    if os.path.exists("logo.png"):
        image = Image.open("logo.png")
        st.image(image, width=200)
    else:
        st.markdown("# TURUNDUSJUTUD")
    
    st.markdown("---")
    
    # Raadionupud on stiliseeritud CSS-iga
    selected_step = st.radio(
        "Sinu teekond:",
        ["Avaleht", "1. Tutvustus", "2. Pakkumine", "3. Leping", "4. Audit & Setup", "5. Strateegia"]
    )
    
    st.markdown("---")
    st.markdown("#### Võta ühendust")
    st.markdown("📧 info@turundusjutud.ee")
    st.markdown("📞 +372 5555 5555")

# --- LEHE SISU KUVAMINE ---

if selected_step == "Avaleht":
    show_intro()
elif selected_step == "1. Tutvustus":
    show_step1()
elif selected_step == "2. Pakkumine":
    show_step2()
elif selected_step == "3. Leping":
    show_step3()
elif selected_step == "4. Audit & Setup":
    show_step4()
elif selected_step == "5. Strateegia":
    show_step5()

# --- JALUS ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>© 2024 Turundusjutud. Sinu strateegiline kasvu partner.</div>", 
    unsafe_allow_html=True
)
