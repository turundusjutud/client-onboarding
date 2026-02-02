import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import io
import textwrap

# --- LEHE SEADISTUSED ---
st.set_page_config(page_title="PDF Generaator", page_icon="📄")

# --- BRÄNDI VÄRVID ---
COLOR_TEAL = HexColor("#1A776F")
COLOR_DARK = HexColor("#052623")
COLOR_ORANGE = HexColor("#FF7F40")
COLOR_YELLOW = HexColor("#FFC876")
COLOR_BG = HexColor("#FAFAFA")
COLOR_WHITE = HexColor("#FFFFFF")

# --- PDF GENEREERIMISE FUNKTSIOON ---
def create_onboarding_pdf(logo_file):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Taust
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, width, height, fill=1)

    # --- 1. PÄIS (HEADER) ---
    header_height = 120
    c.setFillColor(COLOR_DARK)
    c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
    
    # Logo
    if logo_file is not None:
        try:
            logo = ImageReader(logo_file)
            # Arvutame logo kuvasuhte, et see ei veniks välja
            iw, ih = logo.getSize()
            aspect = ih / float(iw)
            logo_width = 150
            logo_height = logo_width * aspect
            # Paigutame logo üles keskele
            c.drawImage(logo, (width - logo_width)/2, height - 85, width=logo_width, height=logo_height, mask='auto')
        except:
            # Kui pilti pole, kirjutame teksti
            c.setFillColor(COLOR_WHITE)
            c.setFont("Helvetica-Bold", 30)
            c.drawCentredString(width/2, height - 60, "TURUNDUSJUTUD")

    # Pealkiri
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height - header_height + 40, "Sinu teekond kasumlike kampaaniateni")
    
    # Alampealkiri
    c.setFillColor(COLOR_YELLOW)
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - header_height + 20, "Läbipaistev 5-etapiline protsess ideest tulemusteni")

    # --- 2. AJATELG (TIMELINE) ---
    
    # Andmed sammude kohta
    steps = [
        {
            "title": "1. Tutvustus ja Eesmärgid (Päev 1)",
            "text": "Me ei müü kotti pähe. Kaardistame sinu äri hetkeseisu ja eesmärgid. Hindame, kas Google Ads on sulle praegu tulus lahendus. Tulemuseks on selgus potentsiaalis.",
            "highlight": False
        },
        {
            "title": "2. Pakkumine ja Kokkulepe (Päev 2)",
            "text": "Saadame personaalse tegevuskava. Meie hinnastus on läbipaistev: eraldi ühekordne seadistustasu ja igakuine haldus. Sõlmime NDA ja lepingu.",
            "highlight": False
        },
        {
            "title": "3. AUDIT JA SEADISTUS (Päevad 3-5)",
            "text": "See on TASULINE DIAGNOOS. Me ei tee tasuta 'müügiauditit'. Siseneme kontole, kontrollime kooditasandil trackingut (GA4), puhastame märksõnad ja loome tehnilise vundamendi.",
            "highlight": True # See samm saab erilise disaini
        },
        {
            "title": "4. Strateegia ja Ülevaatus (Päev 6)",
            "text": "Tutvustame auditi leide ja 90 päeva strateegiat. Sina näed ja kinnitad reklaamtekste ning eelarveid enne, kui need eetrisse lähevad.",
            "highlight": False
        },
        {
            "title": "5. Start ja Optimeerimine (Päev 7+)",
            "text": "Kampaaniad on aktiivsed. Algab õppimisperiood, kus algoritm kogub andmeid. Meie optimeerime iganädalaselt, sina saad raporti kord kuus.",
            "highlight": False
        }
    ]

    start_y = height - header_height - 60
    line_x = 60 # Joone asukoht vasakult
    
    # Joonista vertikaalne joon
    c.setStrokeColor(COLOR_TEAL)
    c.setLineWidth(2)
    c.line(line_x, start_y, line_x, 150)

    current_y = start_y

    for step in steps:
        # Arvuta kasti kõrgus teksti põhjal
        text_width = 400
        wrapper = textwrap.TextWrapper(width=75) # Umbes tähemärkide arv real
        wrapped_text = wrapper.wrap(step['text'])
        block_height = 40 + (len(wrapped_text) * 15)
        
        # Kui on highlight (Audit), joonista taustakast
        if step['highlight']:
            c.setFillColor(HexColor("#FFF3E0")) # Väga hele oranž taust
            c.setStrokeColor(COLOR_ORANGE)
            c.setLineWidth(1)
            # x, y, width, height (ReportLab koordinaadid on alt üles)
            c.roundRect(line_x + 20, current_y - block_height + 10, 480, block_height, 10, fill=1, stroke=1)
            
            # Lisa "PAID STEP" silt
            c.setFillColor(COLOR_ORANGE)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(line_x + 400, current_y - 15, "DIAGNOSTIKA FAAS")

        # Pallikene joone peal
        c.setFillColor(COLOR_ORANGE if step['highlight'] else COLOR_TEAL)
        c.setStrokeColor(COLOR_WHITE)
        c.setLineWidth(2)
        c.circle(line_x, current_y - 10, 8, fill=1, stroke=1)

        # Pealkiri
        c.setFillColor(COLOR_TEAL if not step['highlight'] else COLOR_ORANGE)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(line_x + 35, current_y - 15, step['title'])

        # Sisu tekst
        c.setFillColor(COLOR_DARK)
        c.setFont("Helvetica", 11)
        text_y = current_y - 35
        for line in wrapped_text:
            c.drawString(line_x + 35, text_y, line)
            text_y -= 15

        current_y -= (block_height + 25) # Liigu allapoole järgmise sammu jaoks

    # --- 3. JALUS (FOOTER) ---
    footer_height = 80
    c.setFillColor(COLOR_TEAL)
    c.rect(0, 0, width, footer_height, fill=1, stroke=0)
    
    # Muster (Dekoratiivsed elemendid)
    c.setStrokeColor(COLOR_YELLOW)
    c.setLineWidth(1)
    c.circle(50, 40, 10, stroke=1, fill=0)
    c.circle(width-50, 40, 10, stroke=1, fill=0)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, 45, "Kas oled valmis kasvuks?")
    
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, 25, "Kirjuta: info@turundusjutud.ee  |  Helista: +372 5555 5555")

    c.save()
    buffer.seek(0)
    return buffer

# --- STREAMLIT UI ---
st.title("📄 Onboarding PDF Generaator")
st.markdown("Lae üles oma logo ja lae alla valmis PDF, mida kliendile saata.")

uploaded_logo = st.file_uploader("Lae üles logo (PNG formaat, soovitavalt läbipaistva taustaga)", type=['png'])

if st.button("Genereeri PDF"):
    pdf_bytes = create_onboarding_pdf(uploaded_logo)
    
    st.success("PDF valmis! Lae alla siit:")
    
    st.download_button(
        label="⬇️ Lae alla Onboarding_Teekaart.pdf",
        data=pdf_bytes,
        file_name="Turundusjutud_Teekaart.pdf",
        mime="application/pdf"
    )

# Eelvaate pilt (valikuline, et näidata, milline see välja näeb)
st.markdown("---")
st.caption("See tööriist loob A4 formaadis PDF faili, mis on optimeeritud meiliga saatmiseks.")
