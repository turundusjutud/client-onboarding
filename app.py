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
# COLOR_YELLOW on eemaldatud tekstist parema kontrasti huvides
COLOR_BG = HexColor("#FAFAFA")
COLOR_WHITE = HexColor("#FFFFFF")
COLOR_TEXT = HexColor("#2E3A39")

def create_onboarding_pdf(logo_file):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # 1. Taust
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, width, height, fill=1)

    # --- 2. PÄIS (LOGO JA PEALKIRI JOONDATUD) ---
    header_height = 100
    c.setFillColor(COLOR_DARK)
    c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
    
    # Logo vasakul (Vertikaalselt tsentreeritud päises)
    if logo_file is not None:
        try:
            logo = ImageReader(logo_file)
            iw, ih = logo.getSize()
            aspect = ih / float(iw)
            logo_width = 110
            logo_height = logo_width * aspect
            # Arvutame y-positsiooni, et oleks päise keskel
            logo_y = height - header_height + (header_height - logo_height) / 2
            c.drawImage(logo, 40, logo_y, width=logo_width, height=logo_height, mask='auto')
        except:
            pass

    # Pealkiri paremal (Samal joonel logoga)
    # Kasutame VALGET värvi (mitte kollast) parema kontrasti jaoks
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 16)
    # Teksti y-positsioon on sätitud logo keskkohaga kohakuti
    text_y_center = height - (header_height / 2) - 5
    c.drawRightString(width - 40, text_y_center + 8, "KOOSTÖÖ ALUSTAMISE PROTSESS")
    
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 40, text_y_center - 8, "Turundusjutud OÜ | Sinu partner kasumlikuks kasvuks")

    # --- 3. PROTSESSI SAMMUD ---
    
    # Defineerime Edu Mudeli punktid, mis lähevad 3. sammu sisse
    success_pillars = [
        "• Analüütika ja andmete usaldusväärsus (Tracking)",
        "• Ärilised eesmärgid ja kasumlikkus (Unit Economics)",
        "• Sihtimine ja kanalite valik (Audience & Mix)",
        "• Loovstrateegia ja sõnumid (Creative Assets)",
        "• Kasutajateekonna optimeerimine (CRO)"
    ]

    steps = [
        {
            "num": "1", "title": "TUTVUMISKÕNE",
            "subtitle": "Lähtepunkti kaardistamine",
            "text": "30-minutiline vestlus, kus klient annab ülevaate seni tehtud turundustegevustest, tulemustest ja konkreetsetest ärieesmärkidest.",
            "is_last": False
        },
        {
            "num": "2", "title": "DIAGNOSTIKA JA LEPINGUD",
            "subtitle": "Andmete audit ja juriidiline põhi",
            "text": "Allkirjastame konfidentsiaalsuslepingu (NDA) ja teenuslepingu. Teostame reklaamkontode süvaanalüüsi, et tuvastada ebaefektiivsed kulud.",
            "is_last": False
        },
        {
            "num": "3", "title": "STRATEEGILINE PLAAN",
            "subtitle": "Tegevuskava kinnitamine",
            "text": "Loome tegevuskava koos selgete eesmärkide ja lahendustega. Lähtume plaanis järgmisest 5-osalisest edu mudelist:",
            "pillars": success_pillars, # Siin on uued alampunktid
            "is_last": False
        },
        {
            "num": "4", "title": "START JA OPTIMEERIMINE",
            "subtitle": "Süsteemne haldus ja skaleerimine",
            "text": "Käivitame kampaaniad ja asume järjepidevale optimeerimisele. Koostöö on läbipaistev ning leping ülesöeldav 1-päevase etteteatamisega.",
            "is_last": True
        }
    ]

    current_y = height - 150
    line_x = 65
    box_width = 460

    # Vertikaalne ühendusjoon
    c.setStrokeColor(COLOR_TEAL)
    c.setLineWidth(1.2)
    # Joonistame joone algusest kuni peaaegu lõpuni (arvestuslikult)
    c.line(line_x, current_y, line_x, 180)

    for step in steps:
        wrapper = textwrap.TextWrapper(width=80)
        wrapped_text = wrapper.wrap(step['text'])
        
        # Arvutame kasti kõrguse
        text_height = len(wrapped_text) * 14
        pillars_height = 0
        
        # Kui on sammaste (pillars) nimekiri, lisame sellele ruumi
        if "pillars" in step:
            pillars_height = (len(step['pillars']) * 14) + 10 # +10 vahe
            
        box_height = 60 + text_height + pillars_height

        # Kasti joonistamine
        if step['is_last']:
            c.setFillColor(HexColor("#FFF7F2"))
            c.setStrokeColor(COLOR_ORANGE)
        else:
            c.setFillColor(HexColor("#F7F9F9"))
            c.setStrokeColor(COLOR_TEAL)
            
        c.roundRect(line_x + 20, current_y - box_height + 15, box_width, box_height, 8, fill=1, stroke=1)

        # Pallikene ja Number
        c.setFillColor(COLOR_ORANGE if step['is_last'] else COLOR_TEAL)
        c.circle(line_x, current_y, 12, fill=1, stroke=0)
        c.setFillColor(COLOR_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(line_x, current_y - 3, step['num'])

        # Pealkirjad kasti sees
        c.setFillColor(COLOR_ORANGE if step['is_last'] else COLOR_TEAL)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(line_x + 35, current_y - 12, step['title'])
        
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(line_x + 35, current_y - 26, step['subtitle'])

        # Põhitekst
        c.setFont("Helvetica", 10)
        text_y = current_y - 42
        for line in wrapped_text:
            c.drawString(line_x + 35, text_y, line)
            text_y -= 14
            
        # Kui on alampunktid (Edu mudel), joonistame need
        if "pillars" in step:
            text_y -= 5 # Väike vahe
            c.setFont("Helvetica-Oblique", 9) # Kursiivis alampunktid
            c.setFillColor(COLOR_TEAL)
            for pillar in step['pillars']:
                c.drawString(line_x + 50, text_y, pillar) # Treppimine paremale
                text_y -= 14

        current_y -= (box_height + 20)

    # --- 4. JALUS JA NUPP ---
    footer_height = 100
    c.setFillColor(COLOR_DARK)
    c.rect(0, 0, width, footer_height, fill=1, stroke=0)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(width/2, 75, "Alustame koostööd tutvumiskõnega")
    
    # "BRONEERI KÕNE" NUPP
    btn_w, btn_h = 160, 30
    btn_x = (width - btn_w) / 2
    btn_y = 35
    
    c.setFillColor(COLOR_ORANGE)
    c.roundRect(btn_x, btn_y, btn_w, btn_h, 6, fill=1, stroke=0)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, btn_y + 10, "BRONEERI KÕNE")
    
    # Klikitav link nupu peale
    c.linkURL("https://calendly.com/turundusjutud", (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), relative=0)
    
    c.setFont("Helvetica", 8)
    c.setFillColor(COLOR_WHITE)
    c.drawCentredString(width/2, 15, "reimo.arm@turundusjutud.ee  |  www.turundusjutud.ee")

    c.save()
    buffer.seek(0)
    return buffer

# --- STREAMLIT UI ---
st.title("📄 Turundusjutud Onboarding PDF")
st.write("Genereeri ametlik koostöö alustamise protsess (Lõplik versioon).")

logo = st.file_uploader("Vali logo (PNG)", type=['png'])

if st.button("Loo PDF"):
    pdf = create_onboarding_pdf(logo)
    st.success("PDF on valmis!")
    st.download_button(
        label="⬇️ Lae alla: Turundusjutud_Onboarding.pdf",
        data=pdf,
        file_name="Turundusjutud_Onboarding.pdf",
        mime="application/pdf"
    )
