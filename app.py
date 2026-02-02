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
    
    # 1. Põhitaust (puhas, ilma mustriteta)
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, width, height, fill=1)

    # --- 2. PÄIS (HEADER) ---
    header_height = 160 # Tõstsime päise kõrgust
    c.setFillColor(COLOR_DARK)
    c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
    
    # Logo paigutus - nihutatud allapoole, et vältida lõikamist
    if logo_file is not None:
        try:
            logo = ImageReader(logo_file)
            iw, ih = logo.getSize()
            aspect = ih / float(iw)
            logo_width = 120
            logo_height = logo_width * aspect
            # y-koordinaat on nüüd madalamal (height - 115)
            c.drawImage(logo, (width - logo_width)/2, height - 115, width=logo_width, height=logo_height, mask='auto')
        except:
            pass

    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 130, "STRATEEGILINE KOOSTÖÖMUDEL")
    
    c.setFillColor(COLOR_YELLOW)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 145, "Süsteemne teekond juhuslikest kampaaniatest kasumliku kasvumootorini.")

    # --- 3. PROTSESSI SAMMUD ---
    steps = [
        {
            "num": "1",
            "title": "TUTVUMISKÕNE",
            "subtitle": "Lähtepunkti ja eesmärkide kaardistamine",
            "text": "30-minutiline vestlus, kus klient annab detailse ülevaate seni tehtud turundustegevustest, tulemustest ja konkreetsetest ärieesmärkidest, kuhu soovitakse jõuda.",
            "is_last": False
        },
        {
            "num": "2",
            "title": "DIAGNOSTIKA JA LEPINGUD",
            "subtitle": "Kasvuvõimaluste süvaanalüüs",
            "text": "Allkirjastame konfidentsiaalsuslepingu ja teenuslepingu enne tööga alustamist. Teostame reklaamkontode ja andmete seadistuse auditi, et tuvastada ebaefektiivsed kulud.",
            "is_last": False
        },
        {
            "num": "3",
            "title": "STRATEEGILINE PLAAN",
            "subtitle": "Elluviidav tegevuskava kolmes vaates",
            "text": "Koostame plaani, mis koosneb kolmest sambast: 1. Analüütika ja tracking (mõõdikute korrastamine); 2. Kampaaniate tehniline seadistus; 3. Loominguliste varade strateegia.",
            "is_last": False
        },
        {
            "num": "4",
            "title": "START JA OPTIMEERIMINE",
            "subtitle": "Süsteemne haldus ja skaleerimine",
            "text": "Käivitame kampaaniad ja asume järjepidevale optimeerimisele. Koostöö on läbipaistev ja suunatud objektiivsele tulule. Leping on ülesöeldav 1-päevase etteteatamisega.",
            "is_last": True
        }
    ]

    current_y = height - 200
    line_x = 75
    box_width = 440
    box_padding_top = 15
    box_padding_bottom = 20

    # Vertikaalne joon
    c.setStrokeColor(COLOR_TEAL)
    c.setLineWidth(1.2)
    c.setDash([]) 
    c.line(line_x, current_y, line_x, 150)

    for step in steps:
        # Teksti mähkimine kõrguse arvutamiseks
        wrapper = textwrap.TextWrapper(width=70)
        wrapped_text = wrapper.wrap(step['text'])
        # Arvutame kasti kõrguse dünaamiliselt
        line_count = len(wrapped_text)
        box_height = 65 + (line_count * 14) 

        # KASTI JOONISTAMINE
        # Kui on viimane punkt, siis oranž, muidu teal/valge
        if step['is_last']:
            c.setFillColor(HexColor("#FFF7F2")) # Hele oranž taust
            c.setStrokeColor(COLOR_ORANGE)
        else:
            c.setFillColor(HexColor("#F7F9F9")) # Hele teal taust
            c.setStrokeColor(COLOR_TEAL)
            
        c.setLineWidth(1)
        # Joonistame kasti (suurema ümarusega nurgad = 12)
        c.roundRect(line_x + 25, current_y - box_height + 10, box_width, box_height, 12, fill=1, stroke=1)

        # Number ja Pallikene
        c.setFillColor(COLOR_ORANGE if step['is_last'] else COLOR_TEAL)
        c.circle(line_x, current_y, 14, fill=1, stroke=0)
        c.setFillColor(COLOR_WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(line_x, current_y - 4, step['num'])

        # Pealkiri
        c.setFillColor(COLOR_ORANGE if step['is_last'] else COLOR_TEAL)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(line_x + 45, current_y - box_padding_top, step['title'])
        
        # Alampealkiri
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(line_x + 45, current_y - box_padding_top - 16, step['subtitle'])

        # Sisu tekst (rohkem ruumi/paddingut)
        c.setFont("Helvetica", 10)
        text_start_y = current_y - box_padding_top - 34
        for line in wrapped_text:
            c.drawString(line_x + 45, text_start_y, line)
            text_start_y -= 14
        
        # Liigume järgmise sammu juurde (lisame kasti kõrguse + vahe)
        current_y -= (box_height + 25)

    # --- 4. JALUS (FOOTER) ---
    footer_height = 100
    c.setFillColor(COLOR_DARK)
    c.rect(0, 0, width, footer_height, fill=1, stroke=0)
    
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
st.write("Genereeri puhas ja professionaalne 4-etapiline koostöömudel.")

logo = st.file_uploader("Lae üles logo (ruudukujuline PNG)", type=['png'])

if st.button("Loo PDF"):
    pdf_bytes = create_onboarding_pdf(logo)
    st.success("Dokument on valmis!")
    st.download_button(
        label="⬇️ Lae alla: Turundusjutud_Onboarding.pdf",
        data=pdf_bytes,
        file_name="Turundusjutud_Onboarding.pdf",
        mime="application/pdf"
    )
