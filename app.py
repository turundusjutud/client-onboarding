import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import io
import textwrap

# --- BRÄNDI VÄRVID ---
COLOR_TEAL = HexColor("#1A776F")
COLOR_DARK = HexColor("#052623")
COLOR_ORANGE = HexColor("#FF7F40")
COLOR_YELLOW = HexColor("#FFC876")
COLOR_BG = HexColor("#FAFAFA")
COLOR_WHITE = HexColor("#FFFFFF")
COLOR_TEXT = HexColor("#2E3A39")

def create_onboarding_pdf(logo_file):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Taust
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, width, height, fill=1)

    # --- 1. PÄIS (HEADER) ---
    header_height = 140
    c.setFillColor(COLOR_DARK)
    c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
    
    if logo_file is not None:
        try:
            logo = ImageReader(logo_file)
            iw, ih = logo.getSize()
            aspect = ih / float(iw)
            logo_width = 160
            logo_height = logo_width * aspect
            c.drawImage(logo, (width - logo_width)/2, height - 80, width=logo_width, height=logo_height, mask='auto')
        except:
            pass

    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 100, "STRATEEGILINE KOOSTÖÖMUDEL")
    
    c.setFillColor(COLOR_YELLOW)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 118, "Süsteemne teekond juhuslikest kampaaniatest kasumliku kasvumootorini.")

    # --- 2. PROTSESSI SAMMUD ---
    steps = [
        {
            "num": "1",
            "title": "TUTVUMISKÕNE",
            "subtitle": "Lähtepunkti ja eesmärkide kaardistamine",
            "text": "30-minutiline vestlus, kus klient annab detailse ülevaate seni tehtud turundustegevustest, saavutatud tulemustest ja konkreetsetest ärieesmärkidest, kuhu soovitakse jõuda.",
            "highlight": False
        },
        {
            "num": "2",
            "title": "DIAGNOSTIKA JA LEPINGUD",
            "subtitle": "Kasvuvõimaluste süvaanalüüs",
            "text": "Allkirjastame konfidentsiaalsuslepingu ja teenuslepingu enne tööga alustamist. Teostame reklaamkontode ja andmete seadistuse auditi, et tuvastada ebaefektiivsed kulud ja kasutamata potentsiaal.",
            "highlight": True
        },
        {
            "num": "3",
            "title": "STRATEEGILINE PLAAN",
            "subtitle": "Elluviidav tegevuskava kolmes vaates",
            "text": "Koostame ja kinnitame plaani, mis koosneb: 1. Analüütika ja mõõdikute korrastamine; 2. Kampaaniate tehniline struktureerimine; 3. Loovlahenduste ja visuaalide strateegia.",
            "highlight": False
        },
        {
            "num": "4",
            "title": "START JA OPTIMEERIMINE",
            "subtitle": "Süsteemne haldus ja tulemuste skaleerimine",
            "text": "Käivitame kampaaniad ja asume järjepidevale optimeerimisele. Koostöö on läbipaistev ja objektiivsetele tulemustele suunatud. Paindlik leping on ülesöeldav 1-päevase etteteatamisega.",
            "highlight": False
        }
    ]

    current_y = height - 185
    line_x = 75

    # Vertikaalne joon
    c.setStrokeColor(COLOR_TEAL)
    c.setLineWidth(1.2)
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
        for line in wrapper.wrap(step['text']):
            current_y -= 14
            c.drawString(line_x + 35, current_y - 15, line)
        
        current_y -= 105

    # --- 3. JALUS (FOOTER) ---
    footer_y = 100
    c.setFillColor(COLOR_DARK)
    c.rect(0, 0, width, footer_y, fill=1, stroke=0)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, 65, "Alustame koostööd strateegilise kõnega")
    
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
st.write("Genereeri veebilehe stiilis 4-etapiline teekond.")

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
