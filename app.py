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
    
    # 1. Taust
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, width, height, fill=1)

    # --- 2. PÄIS (LOGO VASAKUL, PEALKIRI PAREMAL) ---
    header_height = 110
    c.setFillColor(COLOR_DARK)
    c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
    
    # Logo vasakul
    if logo_file is not None:
        try:
            logo = ImageReader(logo_file)
            iw, ih = logo.getSize()
            aspect = ih / float(iw)
            logo_width = 100
            logo_height = logo_width * aspect
            c.drawImage(logo, 40, height - 85, width=logo_width, height=logo_height, mask='auto')
        except:
            pass

    # Pealkiri paremal
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawRightString(width - 40, height - 65, "KOOSTÖÖ ALUSTAMISE PROTSESS")
    
    c.setFillColor(COLOR_YELLOW)
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 40, height - 80, "Turundusjutud OÜ | Sinu partner kasumlikuks kasvuks")

    # --- 3. TAKTIKALISED SAMBAD (VISUALISEERITUD) ---
    # See sektsioon joonistab nüüd 5 kõrvuti asetsevat "kaarti"
    
    pillars_y_start = height - 150
    c.setFillColor(COLOR_TEAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, pillars_y_start, "EDU MUDEL: 5 TAKTIKALIST SAMMAST")
    
    # Sammaste andmed
    pillars_data = [
        {"title": "EESMÄRGID", "sub": "Unit Economics", "desc": "Kasumlikkuse ja KPI-de paika panemine.", "color": COLOR_TEAL},
        {"title": "SIHTIMINE", "sub": "Audience & Mix", "desc": "Õige sõnum õigele inimesele õiges kanalis.", "color": COLOR_DARK},
        {"title": "LOOVUS", "sub": "Creative Assets", "desc": "Kõrge mõjuga visuaalid ja tekstid.", "color": COLOR_ORANGE},
        {"title": "TEEKOND", "sub": "Post-Click / CRO", "desc": "Maandumislehe ja ostukogemuse audit.", "color": COLOR_TEAL},
        {"title": "KASV", "sub": "Scale & Volume", "desc": "Eelarve skaleerimine ja efektiivsus.", "color": COLOR_DARK},
    ]

    p_width = 95  # Ühe samba laius
    p_gap = 10    # Vahe sammaste vahel
    p_height = 110 # Samba kõrgus
    p_start_x = 40
    p_start_y = pillars_y_start - 20 - p_height

    for i, p in enumerate(pillars_data):
        x = p_start_x + (i * (p_width + p_gap))
        y = p_start_y
        
        # Joonista samba taust (hele kast)
        c.setFillColor(HexColor("#FFFFFF"))
        c.setStrokeColor(p['color'])
        c.setLineWidth(1)
        c.roundRect(x, y, p_width, p_height, 6, fill=1, stroke=1)
        
        # Joonista värviline päis ("Header bar")
        c.setFillColor(p['color'])
        # (x, y, width, height) - joonistame väikese kasti üles
        c.rect(x, y + p_height - 5, p_width, 5, fill=1, stroke=0) 
        # Et ülemised nurgad oleks ümarad, joonistame ülemise osa uuesti roundRectina ja katame alumise osa kinni, 
        # aga lihtsuse mõttes teeme lihtsalt värvilise riba üles.
        
        # Ikooni asendaja (Ring numbri jaoks)
        c.setFillColor(p['color'])
        c.circle(x + p_width/2, y + p_height - 25, 12, fill=1, stroke=0)
        c.setFillColor(COLOR_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + p_width/2, y + p_height - 28, str(i + 1))
        
        # Pealkiri
        c.setFillColor(p['color'])
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + p_width/2, y + p_height - 50, p['title'])
        
        # Alampealkiri (hallikas)
        c.setFillColor(HexColor("#666666"))
        c.setFont("Helvetica-Oblique", 7)
        c.drawCentredString(x + p_width/2, y + p_height - 62, p['sub'])
        
        # Kirjeldus
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica", 7)
        
        # Teksti murdmine
        wrapper = textwrap.TextWrapper(width=18)
        text_lines = wrapper.wrap(p['desc'])
        text_y = y + p_height - 78
        for line in text_lines:
            c.drawCentredString(x + p_width/2, text_y, line)
            text_y -= 9

    # --- 4. PROTSESSI SAMMUD ---
    steps_y_start = p_start_y - 40
    
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
            "text": "Kinnitame plaani: 1. Analüütika ja tracking; 2. Kampaaniate tehniline seadistus; 3. Loominguliste varade (creative assets) strateegia.",
            "is_last": False
        },
        {
            "num": "4", "title": "START JA OPTIMEERIMINE",
            "subtitle": "Süsteemne haldus ja skaleerimine",
            "text": "Käivitame kampaaniad ja asume järjepidevale optimeerimisele. Koostöö on läbipaistev ning leping ülesöeldav 1-päevase etteteatamisega.",
            "is_last": True
        }
    ]

    current_y = steps_y_start
    line_x = 65
    box_width = 460

    for step in steps:
        wrapper = textwrap.TextWrapper(width=85)
        wrapped_text = wrapper.wrap(step['text'])
        box_height = 50 + (len(wrapped_text) * 12)

        # Kasti joonistamine
        if step['is_last']:
            c.setFillColor(HexColor("#FFF7F2"))
            c.setStrokeColor(COLOR_ORANGE)
        else:
            c.setFillColor(HexColor("#F7F9F9"))
            c.setStrokeColor(COLOR_TEAL)
            
        c.roundRect(line_x + 20, current_y - box_height + 10, box_width, box_height, 8, fill=1, stroke=1)

        # Pallikene ja Number
        c.setFillColor(COLOR_ORANGE if step['is_last'] else COLOR_TEAL)
        c.circle(line_x, current_y, 12, fill=1, stroke=0)
        c.setFillColor(COLOR_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(line_x, current_y - 3, step['num'])

        # Pealkirjad kasti sees
        c.setFillColor(COLOR_ORANGE if step['is_last'] else COLOR_TEAL)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(line_x + 35, current_y - 10, step['title'])
        
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(line_x + 35, current_y - 22, step['subtitle'])

        c.setFont("Helvetica", 9)
        text_y = current_y - 36
        for line in wrapped_text:
            c.drawString(line_x + 35, text_y, line)
            text_y -= 12
        
        current_y -= (box_height + 12)

    # --- 5. JALUS JA NUPP ---
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
st.write("Genereeri ametlik koostöö alustamise protsess (Visualiseeritud sammastega).")

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
