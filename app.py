import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import io
import textwrap

# --- BRÄNDI VÄRVID ---
COLOR_TEAL = HexColor("#1A776F")   # 1, 4
COLOR_DARK = HexColor("#052623")   # 2, 5
COLOR_ORANGE = HexColor("#FF7F40") # 3
COLOR_BG = HexColor("#FAFAFA")
COLOR_WHITE = HexColor("#FFFFFF")
COLOR_TEXT = HexColor("#2E3A39")

# --- JOONISTAMISE ABIFUNKTSIOONID ---

def draw_rounded_header_rect(c, x, y, w, h, radius, color):
    """
    Joonistab kasti, millel on ainult ülemised nurgad ümarad.
    Parandatud versioon: kasutab 'kattuvuse' tehnikat, et vältida ZeroDivisionErrorit.
    """
    c.setFillColor(color)
    c.setStrokeColor(color) # Ääris sama värvi, et vältida triipe
    
    # 1. Joonista täielikult ümarate nurkadega kast
    c.roundRect(x, y, w, h, radius, fill=1, stroke=0)
    
    # 2. Joonista alumisse poolde kandiline kast, et "sirgendada" alumised nurgad
    # See kast katab ümara kasti alumise osa kinni
    rect_height = radius  # Piisab, kui katame nurgaraadiuse jagu
    c.rect(x, y, w, rect_height, fill=1, stroke=0)

def draw_vector_icon(c, x, y, type, color):
    """Joonistab lihtsa vektorsümboli (et vältida emoji probleeme)"""
    c.setStrokeColor(color)
    c.setLineWidth(1.5)
    c.setFillColor(color)
    
    cx, cy = x, y + 5 # Tsentreerimise nihe
    
    if type == "chart": # Tracking
        c.rect(cx - 6, cy - 4, 3, 6, fill=1, stroke=0)
        c.rect(cx - 1, cy - 4, 3, 10, fill=1, stroke=0)
        c.rect(cx + 4, cy - 4, 3, 8, fill=1, stroke=0)
        
    elif type == "pie": # Eesmärgid
        c.circle(cx, cy, 6, fill=0, stroke=1)
        c.line(cx, cy, cx, cy + 6) # Joon üles
        c.line(cx, cy, cx + 4, cy - 4) # Joon diagonaali
        
    elif type == "target": # Sihtimine
        c.circle(cx, cy, 7, fill=0, stroke=1)
        c.circle(cx, cy, 4, fill=0, stroke=1)
        c.circle(cx, cy, 1, fill=1, stroke=1)
        
    elif type == "bulb": # Loovus
        p = c.beginPath()
        p.moveTo(cx, cy + 7)
        p.lineTo(cx + 6, cy)
        p.lineTo(cx, cy - 7)
        p.lineTo(cx - 6, cy)
        p.close()
        c.drawPath(p, fill=0, stroke=1)
        
    elif type == "arrow": # Teekond
        c.circle(cx, cy, 7, fill=0, stroke=1)
        # Lihtne nool paremale
        c.line(cx - 3, cy, cx + 3, cy)
        c.line(cx + 3, cy, cx + 1, cy + 2)
        c.line(cx + 3, cy, cx + 1, cy - 2)

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
    
    # Logo
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

    # Pealkiri
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 16)
    text_y_center = height - (header_height / 2) - 5
    c.drawRightString(width - 40, text_y_center + 8, "KOOSTÖÖ ALUSTAMISE PROTSESS")
    
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 40, text_y_center - 8, "Turundusjutud OÜ | Sinu partner kasumlikuks kasvuks")

    # --- 3. PROTSESSI SAMMUD ---

    # Edu mudeli andmed
    pillars_data = [
        {"title": "TRACKING", "sub": "Analüütika", "icon": "chart", "color": COLOR_TEAL},
        {"title": "EESMÄRGID", "sub": "Unit Economics", "icon": "pie", "color": COLOR_DARK},
        {"title": "SIHTIMINE", "sub": "Audience Mix", "icon": "target", "color": COLOR_ORANGE},
        {"title": "LOOVUS", "sub": "Creative Assets", "icon": "bulb", "color": COLOR_TEAL},
        {"title": "TEEKOND", "sub": "CRO / UX", "icon": "arrow", "color": COLOR_DARK},
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
            "has_visual_pillars": True,
            "is_last": False
        },
        {
            "num": "4", "title": "START JA OPTIMEERIMINE",
            "subtitle": "Süsteemne haldus ja skaleerimine",
            "text": "Käivitame kampaaniad ja asume järjepidevale optimeerimisele. Koostöö on läbipaistev ning leping ülesöeldav 1-päevase etteteatamisega.",
            "is_last": True
        }
    ]

    # --- EELARVUTUS ---
    layout_data = []
    current_y_cursor = height - 140
    line_x = 55
    box_width = 480
    
    for step in steps:
        wrapper = textwrap.TextWrapper(width=90)
        wrapped_text = wrapper.wrap(step['text'])
        text_height = len(wrapped_text) * 14
        
        pillars_section_height = 0
        if step.get('has_visual_pillars'):
            pillars_section_height = 100 
            
        box_height = 60 + text_height + pillars_section_height
        box_top = current_y_cursor
        
        # Numbrite asukoht: Joondatud kasti ülemise äärega (offset 20px)
        circle_offset = 20 
        circle_y = box_top - circle_offset
        
        layout_data.append({
            "step": step,
            "box_top": box_top,
            "box_height": box_height,
            "circle_y": circle_y,
            "text_lines": wrapped_text
        })
        current_y_cursor -= (box_height + 30)

    # --- JOONISTAMINE ---

    # 1. Joonista ühendav joon
    start_line_y = layout_data[0]['circle_y']
    last_box_bottom = layout_data[-1]['box_top'] - layout_data[-1]['box_height']
    
    infinity_center_y = last_box_bottom - 20
    infinity_radius = 5
    
    end_line_y = infinity_center_y + infinity_radius + 5
    
    c.setStrokeColor(COLOR_TEAL)
    c.setLineWidth(2)
    c.line(line_x, start_line_y, line_x, end_line_y)
    
    # Lõpmatuse sümbol
    c.setLineWidth(1.5)
    c.circle(line_x - 5, infinity_center_y, 5, stroke=1, fill=0)
    c.circle(line_x + 5, infinity_center_y, 5, stroke=1, fill=0)


    # 2. Joonista kastid ja sisu
    for item in layout_data:
        step = item['step']
        box_top = item['box_top']
        box_height = item['box_height']
        circle_y = item['circle_y']
        
        # Kasti värvid
        if step['is_last']:
            bg_color = HexColor("#FFF7F2")
            stroke_color = COLOR_ORANGE
            main_color = COLOR_ORANGE
        else:
            bg_color = HexColor("#F7F9F9")
            stroke_color = COLOR_TEAL
            main_color = COLOR_TEAL
        
        # Kasti joonistamine
        c.setFillColor(bg_color)
        c.setStrokeColor(stroke_color)
        c.setLineWidth(1)
        c.roundRect(line_x + 25, box_top - box_height, box_width, box_height, 10, fill=1, stroke=1)

        # Ring ja Number (Vasakul joonel)
        c.setFillColor(main_color)
        c.setStrokeColor(COLOR_BG) 
        c.circle(line_x, circle_y, 14, fill=1, stroke=1)
        
        c.setFillColor(COLOR_WHITE)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(line_x, circle_y - 4, step['num'])

        # Sisu alguspunkt
        content_start_y = box_top - 25

        # Pealkirjad
        c.setFillColor(main_color)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(line_x + 45, content_start_y, step['title'])
        
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(line_x + 45, content_start_y - 14, step['subtitle'])

        # Põhitekst
        c.setFont("Helvetica", 10)
        text_y = content_start_y - 32
        for line in item['text_lines']:
            c.drawString(line_x + 45, text_y, line)
            text_y -= 14
            
        # --- SAMMASTE JOONISTAMINE (Step 3) ---
        if step.get('has_visual_pillars'):
            pillars_y = text_y - 15 
            
            available_width = box_width - 60 
            p_gap = 8
            p_width = (available_width - (4 * p_gap)) / 5
            p_height = 80
            
            p_start_x = line_x + 55 
            
            for i, p in enumerate(pillars_data):
                px = p_start_x + (i * (p_width + p_gap))
                py = pillars_y - p_height
                
                # Võta värv vastavalt andmetele
                pillar_color = p['color']
                pillar_radius = 8
                
                # 1. Kasti taust (Valge, värvilise äärega)
                c.setFillColor(COLOR_WHITE)
                c.setStrokeColor(pillar_color)
                c.setLineWidth(1)
                c.roundRect(px, py, p_width, p_height, pillar_radius, fill=1, stroke=1)
                
                # 2. Värviline päis (KASUTAME UUT FUNKTSIOONI)
                header_height = 25
                draw_rounded_header_rect(c, px, py + p_height - header_height, p_width, header_height, pillar_radius, pillar_color)
                
                # 3. Number päises
                c.setFillColor(COLOR_WHITE)
                c.setFont("Helvetica-Bold", 11)
                c.drawCentredString(px + p_width/2, py + p_height - 18, str(i + 1))
                
                # 4. Pealkiri
                c.setFillColor(pillar_color)
                c.setFont("Helvetica-Bold", 7)
                if len(p['title']) > 8:
                     c.setFont("Helvetica-Bold", 6)
                c.drawCentredString(px + p_width/2, py + p_height - 38, p['title'])
                
                # 5. Alampealkiri
                c.setFillColor(HexColor("#555555"))
                c.setFont("Helvetica", 6)
                c.drawCentredString(px + p_width/2, py + p_height - 48, p['sub'])
                
                # 6. Sümbol (Vektorikoon)
                icon_center_x = px + p_width/2
                icon_center_y = py + 12
                draw_vector_icon(c, icon_center_x, icon_center_y, p['icon'], pillar_color)


    # --- 4. JALUS JA NUPP ---
    footer_height = 100
    c.setFillColor(COLOR_DARK)
    c.rect(0, 0, width, footer_height, fill=1, stroke=0)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(width/2, 75, "Alustame koostööd tutvumiskõnega")
    
    # Nupp
    btn_w, btn_h = 160, 30
    btn_x = (width - btn_w) / 2
    btn_y = 35
    
    c.setFillColor(COLOR_ORANGE)
    c.roundRect(btn_x, btn_y, btn_w, btn_h, 15, fill=1, stroke=0)
    
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
st.write("Genereeri ametlik protsessijoonis (Sümbolitega, ilma emojideta).")

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
