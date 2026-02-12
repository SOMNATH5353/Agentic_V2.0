"""
Convert ALL_APIS_REFERENCE.md to PDF
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
        fontSize=22,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
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
        borderPadding=5,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2980b9'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
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
    
    # Story (content container)
    story = []
    
    # Split content into lines
    lines = content.split('\n')
    
    in_code_block = False
    code_block = []
    in_table = False
    table_data = []
    
    for line in lines:
        # Handle code blocks
        if in_code_block:
            if line.strip().startswith('```'):
                # End code block
                if code_block:
                    code_text = '\n'.join(code_block)
                    # Limit code block length to prevent overflow
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
            # Remove emojis for PDF
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            story.append(Paragraph(text, title_style))
            story.append(Spacer(1, 0.3*inch))
        
        # Heading 1 (## )
        elif line.startswith('## ') and not line.startswith('### '):
            text = line[3:].strip()
            # Remove emojis
            text = re.sub(r'[^\x00-\x7F]+', '', text)
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
            story.append(Spacer(1, 0.1*inch))
        
        # Horizontal rule
        elif line.strip() in ['---', '***', '___']:
            story.append(Spacer(1, 0.2*inch))
        
        # Table detection
        elif '|' in line and line.strip().startswith('|'):
            # Skip table separators
            if '---' in line or '===' in line:
                continue
            
            # Parse table row
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if cells:
                if not in_table:
                    in_table = True
                    table_data = []
                table_data.append(cells)
        
        # End of table
        elif in_table and not line.strip().startswith('|'):
            # Create table
            if table_data:
                # Create table with styling
                t = Table(table_data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                story.append(t)
                story.append(Spacer(1, 0.2*inch))
            in_table = False
            table_data = []
        
        # Bold text (**text**)
        elif '**' in line or '__' in line:
            text = line.strip()
            # Remove emojis
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            # Convert markdown bold to HTML bold
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
            # Convert inline code
            text = re.sub(r'`(.+?)`', r'<font color="#c7254e" backColor="#f9f2f4"><i>\1</i></font>', text)
            if text:
                story.append(Paragraph(text, normal_style))
                story.append(Spacer(1, 0.1*inch))
        
        # Bullet points
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip()[2:]
            # Remove emojis
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            # Convert inline code
            text = re.sub(r'`(.+?)`', r'<font color="#2c3e50"><i>\1</i></font>', text)
            # Handle bold
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            bullet_style = ParagraphStyle('Bullet', parent=normal_style, leftIndent=20, bulletIndent=10)
            story.append(Paragraph(f'• {text}', bullet_style))
        
        # Numbered list
        elif re.match(r'^\d+\.\s', line.strip()):
            text = re.sub(r'^\d+\.\s', '', line.strip())
            # Remove emojis
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            # Convert inline code
            text = re.sub(r'`(.+?)`', r'<font color="#2c3e50"><i>\1</i></font>', text)
            # Handle bold
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            bullet_style = ParagraphStyle('Numbered', parent=normal_style, leftIndent=20)
            story.append(Paragraph(text, bullet_style))
        
        # Regular paragraph
        elif line.strip():
            text = line.strip()
            # Remove emojis
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            # Convert inline code
            text = re.sub(r'`(.+?)`', r'<font color="#2c3e50"><i>\1</i></font>', text)
            # Handle bold
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            if text and not text.startswith('```'):
                story.append(Paragraph(text, normal_style))
                story.append(Spacer(1, 0.05*inch))
    
    # Build PDF
    try:
        doc.build(story)
        print(f"✅ PDF created successfully: {pdf_file}")
        return True
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return False

if __name__ == "__main__":
    # Convert ALL_APIS_REFERENCE.md to PDF
    md_file = "ALL_APIS_REFERENCE.md"
    pdf_file = "ALL_APIS_REFERENCE.pdf"
    
    if not os.path.exists(md_file):
        print(f"❌ Error: {md_file} not found!")
    else:
        print(f"📄 Converting {md_file} to PDF...")
        if parse_markdown_to_pdf(md_file, pdf_file):
            print(f"\n✅ PDF file created: {os.path.abspath(pdf_file)}")
            print(f"\n📍 Location: {os.path.dirname(os.path.abspath(pdf_file))}")
        else:
            print("\n❌ Failed to create PDF")
