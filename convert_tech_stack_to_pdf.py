"""
Convert TECHNICAL_STACK_AND_ARCHITECTURE.md to PDF
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
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
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Title'],
        fontSize=14,
        textColor=colors.HexColor('#555555'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=10,
        spaceBefore=20,
        borderWidth=2,
        borderColor=colors.HexColor('#3498db'),
        borderPadding=8,
        backColor=colors.HexColor('#ecf0f1'),
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
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=6,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=7,
        textColor=colors.HexColor('#2c3e50'),
        backColor=colors.HexColor('#f8f8f8'),
        borderWidth=1,
        borderColor=colors.HexColor('#ddd'),
        borderPadding=6,
        leftIndent=15,
        fontName='Courier',
        leading=10
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        alignment=TA_LEFT
    )
    
    # Story
    story = []
    lines = content.split('\n')
    
    in_code_block = False
    code_block = []
    is_first_title = True
    
    for line in lines:
        # Handle code blocks
        if in_code_block:
            if line.strip().startswith('```'):
                if code_block:
                    code_text = '\n'.join(code_block)
                    # Limit code block size
                    if len(code_text) > 3000:
                        code_text = code_text[:3000] + '\n... (content truncated for PDF)'
                    pre = Preformatted(code_text, code_style)
                    story.append(pre)
                    story.append(Spacer(1, 0.15*inch))
                code_block = []
                in_code_block = False
                continue
            else:
                code_block.append(line)
                continue
        
        if line.strip().startswith('```'):
            in_code_block = True
            continue
        
        # Title (# )
        if line.startswith('# ') and not line.startswith('## '):
            text = line[2:].strip()
            if is_first_title:
                story.append(Paragraph(text, title_style))
                is_first_title = False
            else:
                story.append(PageBreak())
                story.append(Paragraph(text, heading1_style))
            story.append(Spacer(1, 0.2*inch))
        
        # Heading 1 (## )
        elif line.startswith('## ') and not line.startswith('### '):
            text = line[3:].strip()
            # Remove emojis
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            if not is_first_title:
                story.append(PageBreak())
            story.append(Paragraph(text, heading1_style))
            story.append(Spacer(1, 0.15*inch))
        
        # Heading 2 (### )
        elif line.startswith('### ') and not line.startswith('#### '):
            text = line[4:].strip()
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            story.append(Paragraph(text, heading2_style))
            story.append(Spacer(1, 0.1*inch))
        
        # Heading 3 (#### )
        elif line.startswith('#### '):
            text = line[5:].strip()
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            story.append(Paragraph(text, heading3_style))
            story.append(Spacer(1, 0.08*inch))
        
        # Horizontal rule
        elif line.strip() in ['---', '***', '___']:
            story.append(Spacer(1, 0.15*inch))
        
        # Bold text
        elif '**' in line:
            text = line.strip()
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'`(.+?)`', r'<font color="#c7254e" face="Courier"><i>\1</i></font>', text)
            if text:
                story.append(Paragraph(text, normal_style))
                story.append(Spacer(1, 0.05*inch))
        
        # Bullet points
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip()[2:]
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            text = re.sub(r'`(.+?)`', r'<font color="#c7254e" face="Courier"><i>\1</i></font>', text)
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            bullet_style = ParagraphStyle('Bullet', parent=normal_style, leftIndent=25, bulletIndent=10)
            story.append(Paragraph(f'• {text}', bullet_style))
            story.append(Spacer(1, 0.02*inch))
        
        # Regular paragraph
        elif line.strip():
            text = line.strip()
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            text = re.sub(r'`(.+?)`', r'<font color="#c7254e" face="Courier"><i>\1</i></font>', text)
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            if text and not text.startswith('```'):
                story.append(Paragraph(text, normal_style))
                story.append(Spacer(1, 0.04*inch))
    
    try:
        doc.build(story)
        print(f"✅ PDF created successfully: {pdf_file}")
        return True
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    md_file = "TECHNICAL_STACK_AND_ARCHITECTURE.md"
    pdf_file = "TECHNICAL_STACK_AND_ARCHITECTURE.pdf"
    
    if not os.path.exists(md_file):
        print(f"❌ Error: {md_file} not found!")
    else:
        print(f"📄 Converting {md_file} to PDF...")
        if parse_markdown_to_pdf(md_file, pdf_file):
            print(f"\n✅ PDF file created: {os.path.abspath(pdf_file)}")
            print(f"📍 Location: {os.path.dirname(os.path.abspath(pdf_file))}")
        else:
            print("\n❌ Failed to create PDF")
