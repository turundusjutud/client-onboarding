import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import io
import textwrap
import random

# --- BRÄNDI VÄRVID ---
COLOR_TEAL = HexColor("#1A776F")
COLOR_DARK = HexColor("#052623")
COLOR_ORANGE = HexColor("#FF7F40")
COLOR_YELLOW = HexColor("#FFC876")
COLOR_BG = HexColor("#FAFAFA")
COLOR_WHITE = HexColor("#FFFFFF")
COLOR_TEXT = HexColor("#2E3A39")

BRAND_COLORS = [COLOR_TEAL, COLOR_ORANGE, COLOR_YELLOW]

# --- ABIFUNKTSIOONID DEKOORI JAOKS ---
def draw_brand_elements(c, width, height):
    """Joonistab taustale brändi sümboleid (ristid, ringid, kolmnurgad)."""
    random.seed(42) 
    for _ in range(18): # Veidi tihedam muster tühja ruumi täitmiseks
        x = random.randint(30, int(width) - 30)
        y = random.randint(120, int(height) - 150)
        size = random.randint(6, 12)
        color = random.choice(BRAND_COLORS)
        shape = random.choice(['cross', 'circle', 'triangle'])
        
        c.setStrokeColor(color)
        c.setLineWidth(1.2)
        c.setDash([]) # PARANDUS: Tühi list tähistab pidevat joont
        
        if shape == 'cross':
            c.line(x - size/2, y, x + size/2, y)
            c.line(x, y - size/2, x, y + size/2)
        elif shape == 'circle':
            c.circle(x, y, size/2, stroke=1, fill=0)
        elif shape == 'triangle':
            path = c.beginPath()
            path.moveTo(x, y + size/2)
            path.lineTo(x - size/2, y - size/2)
            path.lineTo(x + size/2, y - size/2)
            path.close()
            c.drawPath(path, stroke=1, fill=0)

def create_onboarding_pdf(logo_file):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # 1. Põhitaust
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, width, height, fill=1)
    
    # Lisa dekoratiivsed elemendid
    draw_brand_elements(c, width, height)

    # --- 2. PÄIS (HEADER) ---
    header_height = 140
    c.setFillColor(COLOR_DARK)
    c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
    
    # Logo paigutus (parandatud, et ei lõikaks poolt ära)
    if logo_file is not None:
        try:
            logo = ImageReader(logo_file)
            iw, ih = logo.getSize()
            aspect = ih / float(iw)
            logo_width = 160
            logo_height = logo_width * aspect
            # Tõstsime logo positsiooni veidi kõrgemale
            c.drawImage(logo, (width - logo_width)/2, height - 85, width=logo_width, height=logo_height, mask='auto')
        except:
            pass

    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 105, "STRATEEGILINE KOOSTÖÖMUDEL")
    
    c.setFillColor(COLOR_YELLOW)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 122, "Süsteemne teekond juhuslikest kampaaniatest kasumliku kasvumootorini.")

    # --- 3. PROTSESSI SAMMUD ---
    steps = [
        {
            "num": "1",
            "title": "TUTVUMISKÕNE",
            "subtitle": "Lähtepunkti ja eesmärkide kaardistamine",
            "text": "30-minutiline vestlus, kus kaardistame seni tehtud turundustegevused, saavutatud tulemused ja konkreetsed ärieesmärgid, kuhu soovitakse jõuda.",
            "highlight": False
        },
        {
            "num": "2",
            "title": "DIAGNOSTIKA JA LEPINGUD",
            "subtitle": "Kasvuvõimaluste süvaanalüüs",
            "text": "Enne töö algust allkirjastame konfidentsiaalsuslepingu (NDA) ja teenuslepingu. Teostame reklaamkontode ja andmete auditi, et tuvastada ebaefektiivsed kulud ja kasvupotentsiaal.",
            "highlight": True
        },
        {
            "num": "3",
            "title": "STRATEEGILINE PLAAN",
            "subtitle": "Elluviidav tegevuskava kolmes vaates",
            "text": "Koostame plaani, mis koosneb kolmest sambast: 1. Analüütika ja tracking (mõõdikute korrastamine); 2. Kampaaniate tehniline seadistus ja struktuur; 3. Loominguliste varade strateegia.",
            "highlight": False
        },
        {
            "num": "4",
            "title": "START JA OPTIMEERIMINE",
            "subtitle": "Süsteemne haldus ja tulemuste skaleerimine",
            "text": "Käivitame kampaaniad ja asume järjepidevale optimeerimisele. Koostöö on läbipaistev ja suunatud objektiivsele tulule. Leping on ülesöeldav 1-päevase etteteatamisega.",
            "highlight": False
        }
    ]

    current_y = height - 190
    line_x = 75

    # Vertikaalne joon
    c.setStrokeColor(COLOR_TEAL)
    c.setLineWidth(1.2)
    c.setDash([]) 
    c.line(line_x, current_y, line_x, 190)

    for step in steps:
        if step['highlight']:
            c.setFillColor(HexColor("#F2F7F6"))
            c.setStrokeColor(COLOR_ORANGE)
            c.setLineWidth(0.5)
            c.roundRect(line_x + 25, current_y - 85, 440, 100, 8, fill=1, stroke=1)
            c.setFillColor(COLOR_ORANGE)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(line_x + 365, current_y + 3, "DIAGNOSTIKA FAAS")

        c.setFillColor(COLOR_ORANGE if step['highlight'] else COLOR_TEAL)
        c.circle(line_x, current_y, 14, fill=1, stroke=0)
        c.setFillColor(COLOR_WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(line_x, current_y - 4, step['num'])

        c.setFillColor(COLOR_TEAL if not step['highlight'] else COLOR_ORANGE)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(line_x + 35, current_y + 3, step['title'])
        
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(line_x + 35, current_y - 14, step['subtitle'])

        c.setFont("Helvetica", 10)
        wrapper = textwrap.TextWrapper(width=72)
        text_y = current_y - 28
        for line in wrapper.wrap(step['text']):
            c.drawString(line_x + 35, text_y, line)
            text_y -= 14
        
        current_y -= 115

    # --- 4. JALUS (FOOTER) ---
    footer_y = 100
    c.setFillColor(COLOR_DARK)
    c.rect(0, 0, width, footer_y, fill=1, stroke=0)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, 65, "Alustame koostööd strateegilise kõnega")
    
    # Calendly link kollase ja rasvasena
    c.setFillColor(COLOR_YELLOW)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(width/2, 45, "BRONEERI KÕNE: calendly.com/turundusjutud")
    
    c.setFont("Helvetica", 9)
    c.setFillColor(COLOR_WHITE)
    c.drawCentredString(width/2, 25, "reimo.arm@turundusjutud.ee  |  www.turundusjutud.ee  |  Turundusjutud OÜ")

    c.save()
    buffer.seek(0)
    return buffer

# --- STREAMLIT UI ---
st.title("📄 Turundusjutud PDF Generaator")
st.write("Genereeri visuaalne 4-etapiline teekond koos brändielementidega.")

logo = st.file_uploader("Lae üles logo (PNG)", type=['png'])

if st.button("Loo PDF"):
    pdf_bytes = create_onboarding_pdf(logo)
    st.success("Dokument on valmis!")
    st.download_button(
        label="⬇️ Lae alla: Turundusjutud_Onboarding.pdf",
        data=pdf_bytes,
        file_name="Turundusjutud_Onboarding.pdf",
        mime="application/pdf"
    )
