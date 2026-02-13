"""
Master PDF Report Generator
Generates comprehensive PDF reports with all candidate analytics
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from datetime import datetime
import json

class MasterReportGenerator:
    """Generate comprehensive PDF reports for candidates"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        self.title_style = ParagraphStyle(
            'ReportTitle',
            parent=self.styles['Title'],
            fontSize=22,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.heading1_style = ParagraphStyle(
            'ReportHeading1',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=20,
            borderWidth=2,
            borderColor=colors.HexColor('#3498db'),
            borderPadding=8,
            backColor=colors.HexColor('#ecf0f1'),
            fontName='Helvetica-Bold'
        )
        
        self.heading2_style = ParagraphStyle(
            'ReportHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2980b9'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        self.heading3_style = ParagraphStyle(
            'ReportHeading3',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        self.normal_style = ParagraphStyle(
            'ReportNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=14
        )
        
        self.small_style = ParagraphStyle(
            'ReportSmall',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=12
        )
    
    def generate_master_report(self, candidates_data, output_path=None):
        """
        Generate comprehensive master PDF report
        
        Args:
            candidates_data: List of candidate dictionaries with all analytics
            output_path: File path or BytesIO object
            
        Returns:
            BytesIO object with PDF data
        """
        if output_path is None:
            output_path = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.75*inch,
            bottomMargin=0.5*inch
        )
        
        story = []
        
        # Add title page
        story.extend(self._create_title_page(len(candidates_data)))
        
        # Add executive summary
        story.extend(self._create_executive_summary(candidates_data))
        
        story.append(PageBreak())
        
        # Add each candidate's detailed report
        for idx, candidate in enumerate(candidates_data, 1):
            story.extend(self._create_candidate_report(candidate, idx))
            if idx < len(candidates_data):
                story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
        
        if isinstance(output_path, BytesIO):
            output_path.seek(0)
        
        return output_path
    
    def _create_title_page(self, total_candidates):
        """Create title page"""
        elements = []
        
        # Title
        elements.append(Paragraph("MASTER CANDIDATE ANALYTICS REPORT", self.title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Subtitle
        subtitle = ParagraphStyle('Subtitle', parent=self.normal_style, 
                                 fontSize=14, alignment=TA_CENTER,
                                 textColor=colors.HexColor('#555555'))
        elements.append(Paragraph("Comprehensive AI-Powered Candidate Evaluation", subtitle))
        elements.append(Spacer(1, 0.5*inch))
        
        # Report info
        info_data = [
            ['Report Date:', datetime.now().strftime('%B %d, %Y %I:%M %p')],
            ['Total Candidates:', str(total_candidates)],
            ['Report Type:', 'Master Analytics Report'],
            ['Generated By:', 'Agentic AI Hiring Platform v2.0']
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(info_table)
        elements.append(PageBreak())
        
        return elements
    
    def _create_executive_summary(self, candidates_data):
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.heading1_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Calculate statistics
        total_apps = sum(c['application_summary']['total_applications'] for c in candidates_data)
        total_selected = sum(c['application_summary']['selected'] for c in candidates_data)
        total_rejected = sum(c['application_summary']['rejected'] for c in candidates_data)
        total_pending = sum(c['application_summary']['pending'] for c in candidates_data)
        
        # Calculate average scores
        avg_scores = [c['application_summary']['average_composite_score'] 
                     for c in candidates_data 
                     if c['application_summary']['average_composite_score']]
        overall_avg = np.mean(avg_scores) if avg_scores else 0
        
        # Summary table
        summary_data = [
            ['Metric', 'Value'],
            ['Total Candidates', str(len(candidates_data))],
            ['Total Applications', str(total_apps)],
            ['Selected', f"{total_selected} ({total_selected*100//total_apps if total_apps else 0}%)"],
            ['Rejected', f"{total_rejected} ({total_rejected*100//total_apps if total_apps else 0}%)"],
            ['Pending Review', f"{total_pending} ({total_pending*100//total_apps if total_apps else 0}%)"],
            ['Average Score', f"{overall_avg:.2f}"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Top performers
        elements.append(Paragraph("TOP 5 PERFORMERS", self.heading2_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Sort by best application score
        sorted_candidates = sorted(
            candidates_data,
            key=lambda x: x['application_summary']['best_application']['composite_score'] 
                         if x['application_summary']['best_application'] else 0,
            reverse=True
        )[:5]
        
        top_performers_data = [['Rank', 'Name', 'Best Score', 'Job Role', 'Status']]
        for idx, candidate in enumerate(sorted_candidates, 1):
            best_app = candidate['application_summary']['best_application']
            if best_app:
                top_performers_data.append([
                    str(idx),
                    candidate['candidate_profile']['name'][:20],
                    f"{best_app['composite_score']:.2f}",
                    best_app['job_role'][:25],
                    best_app['decision']
                ])
        
        if len(top_performers_data) > 1:
            top_table = Table(top_performers_data, colWidths=[0.6*inch, 1.8*inch, 1*inch, 2*inch, 1*inch])
            top_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ]))
            elements.append(top_table)
        
        return elements
    
    def _create_candidate_report(self, candidate, candidate_number):
        """Create detailed report for a single candidate"""
        elements = []
        
        profile = candidate['candidate_profile']
        summary = candidate['application_summary']
        applications = candidate['applications']
        
        # Candidate header
        header_text = f"CANDIDATE #{candidate_number}: {profile['name']}"
        elements.append(Paragraph(header_text, self.heading1_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Profile section
        elements.append(Paragraph("PROFILE INFORMATION", self.heading2_style))
        profile_data = [
            ['Email:', profile['email']],
            ['Mobile:', profile.get('mobile', 'N/A')],
            ['LinkedIn:', profile.get('linkedin', 'N/A')[:50]],
            ['GitHub:', profile.get('github', 'N/A')[:50]],
            ['Experience:', f"{profile['years_of_experience']} years"],
            ['Profile Created:', profile.get('profile_created_at', 'N/A')[:10]],
        ]
        
        profile_table = Table(profile_data, colWidths=[1.5*inch, 5*inch])
        profile_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(profile_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # Skills
        skills = profile.get('skills', [])
        if skills:
            elements.append(Paragraph("KEY SKILLS", self.heading3_style))
            skills_text = ', '.join(skills[:15])
            if len(skills) > 15:
                skills_text += f" ... (+{len(skills)-15} more)"
            elements.append(Paragraph(skills_text, self.small_style))
            elements.append(Spacer(1, 0.15*inch))
        
        # Application summary
        elements.append(Paragraph("APPLICATION SUMMARY", self.heading2_style))
        summary_data = [
            ['Total Applications:', str(summary['total_applications'])],
            ['Selected:', str(summary['selected'])],
            ['Rejected:', str(summary['rejected'])],
            ['Pending:', str(summary['pending'])],
            ['Average Score:', f"{summary['average_composite_score']:.2f}" if summary['average_composite_score'] else 'N/A'],
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Best application highlight
        if summary.get('best_application'):
            best_app = summary['best_application']
            elements.append(Paragraph("BEST APPLICATION", self.heading3_style))
            best_data = [
                ['Job Role:', best_app['job_role']],
                ['Composite Score:', f"{best_app['composite_score']:.2f}"],
                ['Rank:', f"#{best_app.get('rank', 'N/A')}"],
                ['Decision:', best_app['decision']],
            ]
            best_table = Table(best_data, colWidths=[1.5*inch, 3*inch])
            best_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#d5f4e6')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.darkgreen),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(best_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Detailed applications analysis
        if applications and len(applications) > 0:
            elements.append(PageBreak())
            elements.append(Paragraph(f"DETAILED APPLICATION ANALYSIS - {profile['name']}", self.heading2_style))
            elements.append(Spacer(1, 0.1*inch))
            
            for app_idx, app in enumerate(applications[:3], 1):  # Show top 3 applications
                elements.extend(self._create_application_detail(app, app_idx))
                
                if app_idx < min(3, len(applications)):
                    elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_application_detail(self, app, app_number):
        """Create detailed analysis for a single application"""
        elements = []
        
        job_details = app.get('job_details', {})
        scores = app.get('scores', {})
        decision = app.get('decision', {})
        fraud = app.get('fraud_detection', {})
        skill_analysis = app.get('skill_analysis', {})
        
        # Application header
        app_title = f"Application #{app_number}: {job_details.get('role', 'N/A')}"
        elements.append(Paragraph(app_title, self.heading3_style))
        elements.append(Spacer(1, 0.08*inch))
        
        # Scores visualization
        if scores:
            score_chart = self._create_score_chart(scores)
            if score_chart:
                elements.append(score_chart)
                elements.append(Spacer(1, 0.1*inch))
        
        # Scores table
        scores_data = [
            ['Metric', 'Score'],
            ['Role Fit Score (RFS)', f"{scores.get('role_fit_score', 0):.2f}"],
            ['Domain Competency (DCS)', f"{scores.get('domain_competency_score', 0):.2f}"],
            ['Experience Match (ELC)', f"{scores.get('experience_level_compatibility', 0):.2f}"],
            ['Composite Score', f"{scores.get('composite_score', 0):.2f}"],
            ['Ranking', scores.get('rank_description', 'N/A')],
        ]
        
        scores_table = Table(scores_data, colWidths=[2.5*inch, 1.5*inch])
        scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(scores_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # Decision
        decision_status = decision.get('status', 'Pending')
        decision_color = colors.green if decision_status == 'Selected' else colors.red
        decision_text = f"<b>DECISION:</b> <font color='{decision_color.hexval()}'>{decision_status}</font>"
        elements.append(Paragraph(decision_text, self.normal_style))
        
        if decision.get('reason'):
            reason_text = f"<i>{decision['reason'][:200]}</i>"
            elements.append(Paragraph(reason_text, self.small_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Fraud detection
        if fraud.get('fraud_flag'):
            fraud_text = f"<b><font color='red'>FRAUD DETECTED</font></b> - Similarity: {fraud.get('similarity_index', 0):.2f}"
            elements.append(Paragraph(fraud_text, self.normal_style))
            elements.append(Spacer(1, 0.1*inch))
        
        # Skill match
        skill_match = skill_analysis.get('skill_match', {})
        if skill_match:
            matched = skill_match.get('matched_skills', [])
            missing = skill_match.get('missing_skills', [])
            
            if matched or missing:
                elements.append(Paragraph("<b>SKILL ANALYSIS</b>", self.heading3_style))
                
                if matched:
                    matched_text = f"<b>Matched:</b> {', '.join(matched[:10])}"
                    if len(matched) > 10:
                        matched_text += f" ... (+{len(matched)-10} more)"
                    elements.append(Paragraph(matched_text, self.small_style))
                
                if missing:
                    missing_text = f"<b>Missing:</b> {', '.join(missing[:10])}"
                    if len(missing) > 10:
                        missing_text += f" ... (+{len(missing)-10} more)"
                    elements.append(Paragraph(missing_text, self.small_style))
                
                elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_score_chart(self, scores):
        """Create a bar chart for scores"""
        try:
            # Extract scores
            score_names = ['RFS', 'DCS', 'ELC', 'Composite']
            score_values = [
                scores.get('role_fit_score', 0) * 100,
                scores.get('domain_competency_score', 0) * 100,
                scores.get('experience_level_compatibility', 0) * 100,
                scores.get('composite_score', 0) * 100,
            ]
            
            # Create figure
            fig, ax = plt.subplots(figsize=(6, 2.5))
            
            # Colors
            colors_list = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
            
            # Create bars
            bars = ax.barh(score_names, score_values, color=colors_list)
            
            # Add value labels
            for bar in bars:
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2, 
                       f'{width:.1f}%',
                       ha='left', va='center', fontsize=9, fontweight='bold')
            
            ax.set_xlim(0, 100)
            ax.set_xlabel('Score (%)', fontsize=10, fontweight='bold')
            ax.set_title('Score Breakdown', fontsize=11, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            # Save to BytesIO
            img_buffer = BytesIO()
            plt.tight_layout()
            plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            
            img_buffer.seek(0)
            
            # Create Image object
            img = Image(img_buffer, width=5*inch, height=2*inch)
            return img
            
        except Exception as e:
            print(f"Error creating score chart: {e}")
            return None


# Singleton instance
master_report_generator = MasterReportGenerator()
