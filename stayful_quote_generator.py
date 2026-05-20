"""
Stayful Setup Quote Generator — Fixed header spacing
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.platypus import Image as RLImage

GREEN   = colors.HexColor('#5d8156')
DARK    = colors.HexColor('#2c2c2c')
MID_GREY= colors.HexColor('#666666')
LIGHT_G = colors.HexColor('#f0f7ee')
LIGHT_GR= colors.HexColor('#f7f5f1')
BORDER  = colors.HexColor('#e8e4de')

def S(name, **kw):
    return ParagraphStyle(name, **kw)

def generate_quote(config, output_path):
    quote_ref   = config['quote_ref']
    date_str    = config['date']
    lead_name   = config['lead_name']
    prop_addr   = config['property_address']
    bedrooms    = config['bedrooms']
    quote_type  = config['quote_type']   # 'furnished' or 'unfurnished'
    notes_text  = config.get('notes', '')
    logo_path   = config.get('logo_path', '/home/claude/stayful_logo.png')

    doc = SimpleDocTemplate(output_path, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm)

    W = A4[0] - 40*mm

    # ── Line items ──
    if quote_type == 'furnished':
        rooms = bedrooms + 1
        labour_qty = round(bedrooms / 2.5, 1)
        items = [
            ("Electrical pack",           1,           330),
            ("Kitchen pack",              1,           350),
            ("Soft furnishings per room", rooms,       300),
            ("Sofabed",                   1,           750),
            ("Double bed",                bedrooms,    350),
            ("Professional photography",  1,           250),
            ("Labour (2 people, 1 day)",  labour_qty,  750),
            ("TV & stand",                1,           350),
            ("Coffee table",              1,           200),
            ("Paint per room",            rooms,       100),
            ("Clothes rack",              bedrooms,     20),
            ("Side tables",               bedrooms*2,   20),
            ("Dining table & chairs",     1,           250),
            ("Keysafes",                  2,            15),
        ]
        travel_buffer = 350  # hidden in total
    else:
        rooms = bedrooms + 1
        labour_qty = round(bedrooms / 2.5, 1)
        items = [
            ("Soft furnishings per room",   rooms,      300),
            ("Professional photography",    1,          250),
            ("Labour — Mum (1 day)",        labour_qty, 200),
            ("Labour — Zac (1 day)",        labour_qty, 350),
            ("TV & stand",                  1,          350),
            ("Paint per room",              rooms,      100),
            ("Clothes rack",                bedrooms*2,  20),
            ("Keysafes",                    2,           15),
        ]
        travel_buffer = 0

    visible_total = sum(q * u for _, q, u in items)
    total = visible_total + travel_buffer

    story = []

    # ── HEADER: logo left, title block right ──
    logo_img = RLImage(logo_path, width=50*mm, height=22*mm, kind='proportional')

    # RIGHT BLOCK: separate rows with explicit heights so nothing overlaps
    right_block = Table(
        [
            [Paragraph("SETUP QUOTE",
                       S("qh", fontSize=22, fontName="Helvetica-Bold",
                         textColor=GREEN, alignment=TA_RIGHT, leading=28))],
            [Spacer(1, 3*mm)],
            [Paragraph(f"Ref: &nbsp;<b>{quote_ref}</b>",
                       S("qr", fontSize=10, textColor=MID_GREY,
                         alignment=TA_RIGHT, leading=16))],
            [Paragraph(f"Date: &nbsp;<b>{date_str}</b>",
                       S("qd", fontSize=10, textColor=MID_GREY,
                         alignment=TA_RIGHT, leading=16))],
        ],
        colWidths=[W * 0.52],
        rowHeights=[12*mm, 3*mm, 6*mm, 6*mm],
    )
    right_block.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("VALIGN",        (0,0), (-1,-1), "BOTTOM"),
    ]))

    header = Table([[logo_img, right_block]], colWidths=[W*0.44, W*0.56])
    header.setStyle(TableStyle([
        ("VALIGN",  (0,0), (-1,-1), "BOTTOM"),
        ("ALIGN",   (0,0), (0,0),   "LEFT"),
        ("ALIGN",   (1,0), (1,0),   "RIGHT"),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))
    story.append(header)
    story.append(HRFlowable(width="100%", thickness=2, color=GREEN, spaceAfter=10))

    # ── CLIENT INFO TABLE ──
    def TH(txt):
        return Paragraph(f"<b>{txt}</b>",
            S("th", fontName="Helvetica-Bold", fontSize=8, textColor=MID_GREY))
    def TV(txt):
        return Paragraph(f"<b>{txt}</b>",
            S("tv", fontName="Helvetica-Bold", fontSize=11, textColor=DARK))

    info = Table(
        [[TH("PREPARED FOR"), TH("PROPERTY"), TH("BEDROOMS"), TH("QUOTE TYPE")],
         [TV(lead_name), TV(prop_addr), TV(f"{bedrooms} bed"),
          TV("Full Setup — Furnished Property" if quote_type=="furnished" else "Soft Furnishing Refresh")]],
        colWidths=[38*mm, 60*mm, 28*mm, None],
    )
    info.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), LIGHT_GR),
        ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
        ("INNERGRID",     (0,0), (-1,-1), 0.5, BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(info)
    story.append(Spacer(1, 12))

    # ── LINE ITEMS ──
    story.append(Paragraph("Setup Items",
        S("sec", fontName="Helvetica-Bold", fontSize=11, textColor=DARK,
          spaceBefore=4, spaceAfter=6)))

    def col(txt, align=TA_LEFT, bold=False):
        fn = "Helvetica-Bold" if bold else "Helvetica"
        return Paragraph(txt, S("c", fontName=fn, fontSize=10,
                                textColor=DARK, alignment=align))

    rows = [[
        Paragraph("<b>DESCRIPTION</b>", S("thw", fontName="Helvetica-Bold",
            fontSize=9, textColor=colors.white)),
        Paragraph("<b>QTY</b>", S("thw2", fontName="Helvetica-Bold",
            fontSize=9, textColor=colors.white, alignment=TA_CENTER)),
        Paragraph("<b>UNIT COST</b>", S("thw3", fontName="Helvetica-Bold",
            fontSize=9, textColor=colors.white, alignment=TA_CENTER)),
        Paragraph("<b>TOTAL</b>", S("thw4", fontName="Helvetica-Bold",
            fontSize=9, textColor=colors.white, alignment=TA_RIGHT)),
    ]]
    for desc, qty, unit in items:
        qs = str(int(qty)) if qty == int(qty) else str(qty)
        rows.append([
            col(desc),
            col(qs, TA_CENTER),
            col(f"£{unit:,}", TA_CENTER),
            col(f"<b>£{int(qty*unit):,}</b>", TA_RIGHT, bold=True),
        ])

    tbl = Table(rows, colWidths=[90*mm, 25*mm, 32*mm, 28*mm])
    rstyles = [
        ("BACKGROUND",    (0,0), (-1,0), GREEN),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
        ("INNERGRID",     (0,0), (-1,-1), 0.5, BORDER),
    ]
    for i in range(2, len(rows), 2):
        rstyles.append(("BACKGROUND", (0,i), (-1,i), LIGHT_GR))
    tbl.setStyle(TableStyle(rstyles))
    story.append(tbl)

    # ── TOTAL ──
    tot = Table([[
        Paragraph("<b>ESTIMATED TOTAL</b>",
            S("tl", fontName="Helvetica-Bold", fontSize=11, textColor=colors.white)),
        Paragraph(f"<b>£{int(total):,}</b>",
            S("tv2", fontName="Helvetica-Bold", fontSize=20,
              textColor=colors.white, alignment=TA_RIGHT)),
    ]], colWidths=[None, 45*mm])
    tot.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), GREEN),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(tot)
    story.append(Spacer(1, 14))

    # ── PAYMENT / LINKS ──
    body = S("body", fontName="Helvetica", fontSize=9, textColor=DARK, leading=14)
    lbl  = S("lbl",  fontName="Helvetica-Bold", fontSize=10, textColor=DARK, spaceAfter=4)
    pay = Table([
        [Paragraph("<b>Payment Details</b>", lbl),
         Paragraph("<b>Useful Links</b>", lbl)],
        [Paragraph("Harrison R2RJV Ltd<br/>Sort Code: 04-00-03<br/>"
                   "Account No: 90529628<br/><b>Payment terms: 100% upfront</b>", body),
         Paragraph('Case studies &amp; photos:<br/>'
                   '<a href="https://www.stayful.co.uk/stayful-case-studies" color="blue">'
                   'stayful.co.uk/stayful-case-studies</a><br/><br/>'
                   "What's included in the pack:<br/>"
                   '<a href="https://www.stayful.co.uk/essential-item-checklist" color="blue">'
                   'stayful.co.uk/essential-item-checklist</a>', body)],
    ], colWidths=[85*mm, None])
    pay.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    story.append(pay)
    story.append(Spacer(1, 8))

    # ── NOTES ──
    if notes_text:
        story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6))
        story.append(Paragraph("<b>Notes</b>",
            S("nl", fontName="Helvetica-Bold", fontSize=9, textColor=DARK)))
        story.append(Paragraph(notes_text,
            S("nb", fontName="Helvetica", fontSize=9, textColor=DARK, leading=13)))
        story.append(Spacer(1, 8))

    # ── FOOTER ──
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6))
    story.append(Paragraph(
        f"Stayful — MWB Stays Ltd | 20 Wenlock Road, London, N1 7GU | "
        f"zac@stayful.co.uk | stayful.co.uk<br/>"
        f"Quote ref: {quote_ref} | Valid for 30 days from {date_str}",
        S("ft", fontName="Helvetica", fontSize=8,
          textColor=colors.grey, alignment=TA_CENTER)))

    doc.build(story)
    print(f"Quote saved: {output_path}  |  Total: £{int(total):,}")
