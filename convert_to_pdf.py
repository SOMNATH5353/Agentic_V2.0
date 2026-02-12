"""
Convert API_ENDPOINTS.md to PDF using markdown and reportlab
"""
import os
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
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
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#3498db'),
        spaceAfter=12,
        spaceBefore=20,
        borderWidth=1,
        borderColor=colors.HexColor('#3498db'),
        borderPadding=5
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2980b9'),
        spaceAfter=10,
        spaceBefore=15
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=12
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        textColor=colors.HexColor('#c7254e'),
        backColor=colors.HexColor('#f9f2f4'),
        borderWidth=1,
        borderColor=colors.HexColor('#e1e1e8'),
        borderPadding=5,
        leftIndent=10
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    # Story (content container)
    story = []
    
    # Split content into lines
    lines = content.split('\n')
    
    in_code_block = False
    code_block = []
    
    for line in lines:
        # Skip empty lines in code blocks
        if in_code_block:
            if line.strip().startswith('```'):
                # End code block
                if code_block:
                    code_text = '\n'.join(code_block)
                    pre = Preformatted(code_text, code_style)
                    story.append(pre)
                    story.append(Spacer(1, 0.2*inch))
                code_block = []
                in_code_block = False
                continue
            else:
                code_block.append(line)
                continue
        
        # Start code block
        if line.strip().startswith('```'):
            in_code_block = True
            continue
        
        # Skip markdown link definitions
        if line.strip().startswith('[') and ']:' in line:
            continue
        
        # Title (# )
        if line.startswith('# ') and not line.startswith('## '):
            text = line[2:].strip()
            story.append(Paragraph(text, title_style))
            story.append(Spacer(1, 0.3*inch))
        
        # Heading 1 (## )
        elif line.startswith('## ') and not line.startswith('### '):
            text = line[3:].strip()
            story.append(Paragraph(text, heading1_style))
            story.append(Spacer(1, 0.15*inch))
        
        # Heading 2 (### )
        elif line.startswith('### ') and not line.startswith('#### '):
            text = line[4:].strip()
            story.append(Paragraph(text, heading2_style))
            story.append(Spacer(1, 0.1*inch))
        
        # Heading 3 (#### )
        elif line.startswith('#### '):
            text = line[5:].strip()
            story.append(Paragraph(text, heading3_style))
            story.append(Spacer(1, 0.1*inch))
        
        # Horizontal rule
        elif line.strip() in ['---', '***', '___']:
            story.append(Spacer(1, 0.1*inch))
            story.append(PageBreak())
        
        # Bold text (**text**)
        elif '**' in line or '__' in line:
            text = line.strip()
            # Convert markdown bold to HTML bold
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
            # Convert inline code
            text = re.sub(r'`(.+?)`', r'<font color="#c7254e" backColor="#f9f2f4">\1</font>', text)
            story.append(Paragraph(text, normal_style))
            story.append(Spacer(1, 0.1*inch))
        
        # Bullet points
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip()[2:]
            # Convert inline code
            text = re.sub(r'`(.+?)`', r'<font color="#c7254e">\1</font>', text)
            bullet_style = ParagraphStyle('Bullet', parent=normal_style, leftIndent=20, bulletIndent=10)
            story.append(Paragraph(f'• {text}', bullet_style))
        
        # Numbered list
        elif re.match(r'^\d+\.\s', line.strip()):
            text = re.sub(r'^\d+\.\s', '', line.strip())
            # Convert inline code
            text = re.sub(r'`(.+?)`', r'<font color="#c7254e">\1</font>', text)
            bullet_style = ParagraphStyle('Numbered', parent=normal_style, leftIndent=20)
            story.append(Paragraph(text, bullet_style))
        
        # Table rows (basic detection)
        elif '|' in line and line.strip().startswith('|'):
            # Skip table separators
            if '---' in line:
                continue
            # Simple table rendering (just as text)
            story.append(Paragraph(line.replace('|', ' | '), code_style))
        
        # Regular paragraph
        elif line.strip():
            text = line.strip()
            # Convert inline code
            text = re.sub(r'`(.+?)`', r'<font color="#c7254e" backColor="#f9f2f4">\1</font>', text)
            story.append(Paragraph(text, normal_style))
            story.append(Spacer(1, 0.05*inch))
    
    # Build PDF
    doc.build(story)
    print(f"✅ PDF created successfully: {pdf_file}")

if __name__ == "__main__":
    md_file = "API_ENDPOINTS.md"
    pdf_file = "API_ENDPOINTS.pdf"
    
    if not os.path.exists(md_file):
        print(f"❌ Error: {md_file} not found!")
    else:
        parse_markdown_to_pdf(md_file, pdf_file)
        print(f"\n📄 PDF file location: {os.path.abspath(pdf_file)}")
