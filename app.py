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

    # --- 2. PÄIS ---
    header_height = 100
    c.setFillColor(COLOR_DARK)
    c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
    
    if logo_file is not None:
        try:
            logo = ImageReader(logo_file)
            iw, ih = logo.getSize()
            aspect = ih / float(iw)
            logo_width = 110
            logo_height = logo_width * aspect
            logo_y = height - header_height + (header_height - logo_height) / 2
            c.drawImage(logo, 40, logo_y, width=logo_width, height=logo_height, mask='auto')
        except:
            pass

    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 16)
    text_y_center = height - (header_height / 2) - 5
    c.drawRightString(width - 40, text_y_center + 8, "KOOSTÖÖ ALUSTAMISE PROTSESS")
    
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 40, text_y_center - 8, "Turundusjutud OÜ | Sinu partner kasumlikuks kasvuks")

    # --- 3. PROTSESSI SAMMUD ---

    # Edu mudeli andmed (Visuaalsete kaartide jaoks)
    pillars_data = [
        {"title": "TRACKING", "sub": "Analüütika", "color": COLOR_TEAL},
        {"title": "EESMÄRGID", "sub": "Unit Economics", "color": COLOR_DARK},
        {"title": "SIHTIMINE", "sub": "Audience Mix", "color": COLOR_ORANGE},
        {"title": "LOOVUS", "sub": "Creative Assets", "color": COLOR_TEAL},
        {"title": "TEEKOND", "sub": "CRO / UX", "color": COLOR_DARK},
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
            "has_visual_pillars": True, # Märge, et siia tuleb joonistada sambad
            "is_last": False
        },
        {
            "num": "4", "title": "START JA OPTIMEERIMINE",
            "subtitle": "Süsteemne haldus ja skaleerimine",
            "text": "Käivitame kampaaniad ja asume järjepidevale optimeerimisele. Koostöö on läbipaistev ning leping ülesöeldav 1-päevase etteteatamisega.",
            "is_last": True
        }
    ]

    current_y = height - 140
    line_x = 55
    box_width = 480 # Veidi laiem kast, et 5 sammast mahuks hästi ära

    # Vertikaalne ühendusjoon
    c.setStrokeColor(COLOR_TEAL)
    c.setLineWidth(1.2)
    c.line(line_x, current_y, line_x, 180)

    for step in steps:
        wrapper = textwrap.TextWrapper(width=90)
        wrapped_text = wrapper.wrap(step['text'])
        
        # Arvutame teksti kõrguse
        text_height = len(wrapped_text) * 14
        
        # Arvutame lisaruumi sammaste jaoks
        pillars_section_height = 0
        if step.get('has_visual_pillars'):
            pillars_section_height = 90 # Ruumi sammaste jaoks
            
        box_height = 60 + text_height + pillars_section_height

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
            
        # --- SAMMASTE JOONISTAMINE (kui on Step 3) ---
        if step.get('has_visual_pillars'):
            text_y -= 10 # Väike vahe teksti ja sammaste vahel
            
            # Arvutame sammaste mõõdud, et need mahuks kasti sisse
            # Kasti laius on box_width (480). Jätame äärtesse ruumi (nt 35px padding)
            available_width = box_width - 50 
            p_gap = 8
            p_width = (available_width - (4 * p_gap)) / 5
            p_height = 70
            
            p_start_x = line_x + 45 # Alguspunkt kasti sees
            
            for i, p in enumerate(pillars_data):
                px = p_start_x + (i * (p_width + p_gap))
                py = text_y - p_height
                
                # Samba taust (valge)
                c.setFillColor(COLOR_WHITE)
                c.setStrokeColor(p['color'])
                c.setLineWidth(1)
                c.roundRect(px, py, p_width, p_height, 4, fill=1, stroke=1)
                
                # Värviline päis
                c.setFillColor(p['color'])
                c.rect(px, py + p_height - 15, p_width, 15, fill=1, stroke=0)
                
                # Number päisesse
                c.setFillColor(COLOR_WHITE)
                c.setFont("Helvetica-Bold", 8)
                c.drawCentredString(px + p_width/2, py + p_height - 11, str(i + 1))
                
                # Pealkiri
                c.setFillColor(p['color'])
                c.setFont("Helvetica-Bold", 7)
                # Kui pealkiri on pikk, vähendame fonti
                if len(p['title']) > 8:
                     c.setFont("Helvetica-Bold", 6)
                c.drawCentredString(px + p_width/2, py + 35, p['title'])
                
                # Alampealkiri
                c.setFillColor(HexColor("#555555"))
                c.setFont("Helvetica", 6)
                c.drawCentredString(px + p_width/2, py + 20, p['sub'])
                
                # Ikoon/Sümbol (lihtsustatud ring)
                c.setStrokeColor(p['color'])
                c.setFillColor(COLOR_WHITE)
                c.circle(px + p_width/2, py + 10, 3, fill=1, stroke=1)

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
    
    c.linkURL("https://calendly.com/turundusjutud", (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), relative=0)
    
    c.setFont("Helvetica", 8)
    c.setFillColor(COLOR_WHITE)
    c.drawCentredString(width/2, 15, "reimo.arm@turundusjutud.ee  |  www.turundusjutud.ee")

    c.save()
    buffer.seek(0)
    return buffer

# --- STREAMLIT UI ---
st.title("📄 Turundusjutud Onboarding PDF")
st.write("Genereeri protsess, kus Edu Mudel on visuaalselt integreeritud tegevuskavasse.")

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
