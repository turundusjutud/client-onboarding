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
    
    # Logo paigaldus
    if logo_file is not None:
        try:
            logo = ImageReader(logo_file)
            iw, ih = logo.getSize()
            aspect = ih / float(iw)
            logo_width = 140
            c.drawImage(logo, (width - logo_width)/2, height - 75, width=logo_width, height=logo_width * aspect, mask='auto')
        except:
            pass

    # Pealkirjad veebilehe stiilis
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 95, "KLIENDI TEEKOND: STRATEEGILINE KASVUMOOTOR")
    
    c.setFillColor(COLOR_YELLOW)
    c.setFont("Helvetica", 11)
    c.drawCentredString(width/2, height - 115, "Reklaamiraha põletamise asemel kasvatame süsteemselt sinu kasumit.")

    # --- 2. PROTSESSI SAMMUD ---
    steps = [
        {
            "num": "1",
            "title": "TUTVUMISKÕNE",
            "subtitle": "Sobivuse ja hetkeolukorra kaardistamine",
            "text": "30-minutiline vestlus, et näha, kas saame olla strateegiliseks partneriks. Me ei ole agentuur algajatele – keskendume ärimudelitele, mis on valmis järgmiseks suureks hüppeks.",
            "highlight": False
        },
        {
            "num": "2",
            "title": "DIAGNOSTIKA",
            "subtitle": "Suurimate kasutamata võimaluste leidmine",
            "text": "Süvaanalüüs (NDA alusel). Viime turundusnumbrid vastavusse pangakontol toimuvaga. Kontrollime andmete usaldusväärsust ja leiame kohad, kus sinu eelarve hetkel ebaefektiivselt põleb.",
            "highlight": True # See on tasuline diagnostika faas
        },
        {
            "num": "3",
            "title": "STRATEEGILINE PLAAN",
            "subtitle": "Süsteemne tegevuskava kasumlikuks kasvuks",
            "text": "Loome selgete eesmärkidega plaani. Asendame juhuslikud kampaaniad andmetel põhineva süsteemiga, mis parandab tulemusi nädalast nädalasse, mitte ei piirdu vaid klikkide lugemisega.",
            "highlight": False
        },
        {
            "num": "4",
            "title": "START JA SKALEERIMINE",
            "subtitle": "Kohene tööle asumine ja pidev optimeerimine",
            "text": "Asume koheselt tööle. Meie koostöö on läbipaistev ja paindlik – kui me ei sobi, saab lepingu üles öelda 1-päevase etteteatamisega. Toome sinu ärisse Bolti-tasemel digiturunduse kogemuse.",
            "highlight": False
        }
    ]

    current_y = height - 180
    line_x = 70

    # Vertikaalne joon
    c.setStrokeColor(COLOR_TEAL)
    c.setLineWidth(1.5)
    c.line(line_x, current_y, line_x, 180)

    for step in steps:
        # Highlight kast Diagnostika jaoks
        if step['highlight']:
            c.setFillColor(HexColor("#F0F7F6"))
            c.setStrokeColor(COLOR_ORANGE)
            c.roundRect(line_x + 25, current_y - 95, 450, 110, 8, fill=1, stroke=1)
            c.setFillColor(COLOR_ORANGE)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(line_x + 360, current_y + 2, "TASULINE DIAGNOSTIKA")

        # Ring ja number
        c.setFillColor(COLOR_ORANGE if step['highlight'] else COLOR_TEAL)
        c.circle(line_x, current_y, 15, fill=1, stroke=0)
        c.setFillColor(COLOR_WHITE)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(line_x, current_y - 4, step['num'])

        # Tekstiblokk
        c.setFillColor(COLOR_TEAL if not step['highlight'] else COLOR_ORANGE)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(line_x + 35, current_y + 2, step['title'])
        
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(line_x + 35, current_y - 15, step['subtitle'])

        c.setFont("Helvetica", 10)
        wrapper = textwrap.TextWrapper(width=70)
        wrapped_text = wrapper.wrap(step['text'])
        text_y = current_y - 32
        for line in wrapped_text:
            c.drawString(line_x + 35, text_y, line)
            text_y -= 14
        
        current_y -= 135

    # --- 3. JALUS (FOOTER) ---
    c.setFillColor(COLOR_DARK)
    c.rect(0, 0, width, 100, fill=1, stroke=0)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, 65, "Sinu ambitsioonid on vaid ühe strateegilise otsuse kaugusel.")
    
    c.setFillColor(COLOR_YELLOW)
    c.setFont("Helvetica", 9)
    c.drawCentredString(width/2, 45, "Turundusjutud OÜ  |  www.turundusjutud.ee  |  info@turundusjutud.ee")
    
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(COLOR_WHITE)
    c.drawCentredString(width/2, 25, "6 aastat globaalset kogemust Boltist – nüüd sinu ettevõtte teenistuses.")

    c.save()
    buffer.seek(0)
    return buffer

# --- STREAMLIT UI ---
st.title("📄 Turundusjutud Onboarding PDF")
st.write("Genereeri ametlik 4-etapiline teekond, mis peegeldab veebilehe sõnumeid.")

logo = st.file_uploader("Vali logo (läbipaistev PNG on parim)", type=['png'])

if st.button("Loo Onboarding PDF"):
    pdf = create_onboarding_pdf(logo)
    st.success("Dokument on valmis!")
    st.download_button(
        label="⬇️ Lae alla: Turundusjutud_Onboarding.pdf",
        data=pdf,
        file_name="Turundusjutud_Onboarding.pdf",
        mime="application/pdf"
    )
