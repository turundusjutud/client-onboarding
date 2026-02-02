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

    # Edu mudeli andmed (Visuaalsete kaartide jaoks) - Uuendatud sümbolitega
    pillars_data = [
        {"title": "TRACKING", "sub": "Analüütika", "symbol": "📊"}, # Tulpdiagramm
        {"title": "EESMÄRGID", "sub": "Unit Economics", "symbol": "💼"}, # Portfell
        {"title": "SIHTIMINE", "sub": "Audience Mix", "symbol": "🎯"}, # Märklaud
        {"title": "LOOVUS", "sub": "Creative Assets", "symbol": "💡"}, # Lambipirn
        {"title": "TEEKOND", "sub": "CRO / UX", "symbol": "🔄"}, # Nooled ringis (optimeerimine)
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
            pillars_section_height = 100 # Ruumi sammaste jaoks
            
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
    
    infinity_y = last_box_bottom - 15
    end_line_y = infinity_y + 12 
    
    c.setStrokeColor(COLOR_TEAL)
    c.setLineWidth(2)
    c.line(line_x, start_line_y, line_x, end_line_y)
    
    # Lõpmatuse sümbol
    c.setFont("Helvetica", 24)
    c.setFillColor(COLOR_TEAL)
    c.drawCentredString(line_x, infinity_y - 8, "∞")


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
            p_height = 75 # Optimeeritud kõrgus
            
            p_start_x = line_x + 55 
            
            for i, p in enumerate(pillars_data):
                px = p_start_x + (i * (p_width + p_gap))
                py = pillars_y - p_height
                
                pillar_color = COLOR_TEAL # Kõik ühte värvi
                pillar_radius = 8
                
                # --- 1. Joonista kasti taust ja piirjoon ---
                c.setFillColor(COLOR_WHITE)
                c.setStrokeColor(pillar_color)
                c.setLineWidth(1)
                c.roundRect(px, py, p_width, p_height, pillar_radius, fill=1, stroke=1)
                
                # --- 2. Joonista värviline päis (Clippinguga) ---
                c.saveState()
                
                # Loome maski, mis on sama kujuga nagu sammas
                path = c.beginPath()
                path.roundRect(px, py, p_width, p_height, pillar_radius)
                c.clipPath(path, stroke=0, fill=0)
                
                # Joonistame päise kasti
                c.setFillColor(pillar_color)
                c.rect(px, py + p_height - 22, p_width, 22, fill=1, stroke=0)
                
                c.restoreState()
                
                # --- 3. Taasta piirjoon päise ümber (puhtuse mõttes) ---
                c.setStrokeColor(pillar_color)
                c.setLineWidth(1)
                c.roundRect(px, py, p_width, p_height, pillar_radius, fill=0, stroke=1)

                # --- 4. Sisu ---
                
                # Number päises
                c.setFillColor(COLOR_WHITE)
                c.setFont("Helvetica-Bold", 11)
                c.drawCentredString(px + p_width/2, py + p_height - 16, str(i + 1))
                
                # Pealkiri
                c.setFillColor(pillar_color)
                c.setFont("Helvetica-Bold", 7)
                if len(p['title']) > 8:
                     c.setFont("Helvetica-Bold", 6)
                c.drawCentredString(px + p_width/2, py + p_height - 35, p['title'])
                
                # Alampealkiri
                c.setFillColor(HexColor("#555555"))
                c.setFont("Helvetica", 6)
                c.drawCentredString(px + p_width/2, py + p_height - 45, p['sub'])
                
                # --- SÜMBOL/EMOJI ---
                # Asendame kirjelduse ja ringi sümboliga
                c.setFillColor(pillar_color)
                symbol = p.get('symbol', '')
                # Kasutame suuremat fonti sümboli jaoks
                c.setFont("Helvetica", 16) 
                # Paigutame sümboli kasti alumisse ossa
                c.drawCentredString(px + p_width/2, py + 12, symbol)

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
st.write("Genereeri ametlik protsessijoonis (Viimistletud Edu mudeliga).")

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
