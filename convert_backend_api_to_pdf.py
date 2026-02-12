"""
Convert backend/API_ENDPOINTS.md to PDF
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import re

def parse_markdown_to_pdf(md_file, pdf_file):
    """Convert markdown to PDF with formatting"""
    
    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.75*inch,
        bottomMargin=0.5*inch
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=20,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#3498db'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#2980b9'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=8,
        textColor=colors.HexColor('#2c3e50'),
        backColor=colors.HexColor('#f4f4f4'),
        borderWidth=1,
        borderColor=colors.HexColor('#ddd'),
        borderPadding=8,
        leftIndent=10,
        fontName='Courier'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    # Story
    story = []
    lines = content.split('\n')
    
    in_code_block = False
    code_block = []
    
    for line in lines:
        if in_code_block:
            if line.strip().startswith('```'):
                if code_block:
                    code_text = '\n'.join(code_block)
                    if len(code_text) > 2000:
                        code_text = code_text[:2000] + '\n... (truncated)'
                    pre = Preformatted(code_text, code_style)
                    story.append(pre)
                    story.append(Spacer(1, 0.2*inch))
                code_block = []
                in_code_block = False
                continue
            else:
                code_block.append(line)
                continue
        
        if line.strip().startswith('```'):
            in_code_block = True
            continue
        
        if line.startswith('# ') and not line.startswith('## '):
            text = line[2:].strip()
            story.append(Paragraph(text, title_style))
            story.append(Spacer(1, 0.3*inch))
        
        elif line.startswith('## ') and not line.startswith('### '):
            text = line[3:].strip()
            story.append(PageBreak())
            story.append(Paragraph(text, heading1_style))
            story.append(Spacer(1, 0.15*inch))
        
        elif line.startswith('### '):
            text = line[4:].strip()
            story.append(Paragraph(text, heading2_style))
            story.append(Spacer(1, 0.1*inch))
        
        elif line.strip() in ['---', '***', '___']:
            story.append(Spacer(1, 0.2*inch))
        
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip()[2:]
            text = re.sub(r'`(.+?)`', r'<font color="#2c3e50"><i>\1</i></font>', text)
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            bullet_style = ParagraphStyle('Bullet', parent=normal_style, leftIndent=20, bulletIndent=10)
            story.append(Paragraph(f'• {text}', bullet_style))
        
        elif line.strip():
            text = line.strip()
            text = re.sub(r'`(.+?)`', r'<font color="#2c3e50"><i>\1</i></font>', text)
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            if text and not text.startswith('```'):
                story.append(Paragraph(text, normal_style))
                story.append(Spacer(1, 0.05*inch))
    
    try:
        doc.build(story)
        print(f"✅ PDF created successfully: {pdf_file}")
        return True
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return False

if __name__ == "__main__":
    md_file = "backend/API_ENDPOINTS.md"
    pdf_file = "Backend_API_ENDPOINTS.pdf"
    
    if not os.path.exists(md_file):
        print(f"❌ Error: {md_file} not found!")
    else:
        print(f"📄 Converting {md_file} to PDF...")
        if parse_markdown_to_pdf(md_file, pdf_file):
            print(f"\n✅ PDF file created: {os.path.abspath(pdf_file)}")
        else:
            print("\n❌ Failed to create PDF")
