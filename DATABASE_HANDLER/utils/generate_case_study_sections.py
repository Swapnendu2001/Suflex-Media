import re
import json
from html import unescape


def clean_html(html_text):
    """
    Remove HTML tags and clean up text content while preserving readability
    
    Args:
        html_text: HTML string to clean
        
    Returns:
        str: Cleaned text without HTML tags
    """
    if not html_text:
        return ""
    
    text = re.sub(r'<!--.*?-->', '', html_text, flags=re.DOTALL)
    text = re.sub(r'<meta[^>]*>', '', text)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    text = unescape(text)
    text = ' '.join(text.split())
    
    return text.strip()


def generate_case_study_card(case_study_data, index):
    """
    Generate HTML card for a case study
    
    Args:
        case_study_data: Dictionary containing case study information with 'slug' and 'preview'
        index: Position index to determine light/dark theme
        
    Returns:
        str: HTML string for the case study card
    """
    slug = case_study_data.get('slug', '')
    preview = case_study_data.get('preview', {})
    
    if isinstance(preview, str):
        try:
            preview = json.loads(preview)
        except:
            preview = {}
    
    image_url = preview.get('imageUrl', '/images/Frame1.jpg')
    image_alt = preview.get('imageAlt', 'Case Study')
    blog_title = preview.get('blogTitle', 'Untitled Case Study')
    text = clean_html(preview.get('text', ''))
    project_snapshots = preview.get('projectSnapshots', [])
    
    snapshots_html = ""
    if project_snapshots:
        snapshots_html = "<ul style='margin: 10px 0; padding-left: 20px;'>"
        for snapshot in project_snapshots:
            cleaned_snapshot = clean_html(snapshot)
            if cleaned_snapshot:
                snapshots_html += f"<li style='margin: 5px 0;'>{cleaned_snapshot}</li>"
        snapshots_html += "</ul>"
    
    card_class = "case-study-card-light" if index % 2 == 0 else "dark"
    
    html = f"""
                <div class="case-study-card {card_class}">
                    <div class="case-study-image">
                        <img src="{image_url}" alt="{image_alt}">
                    </div>
                    <div class="case-study-content">
                        <h3 class="case-study-title">{blog_title}</h3>
                        <p class="case-study-description">
                            {text}
                        </p>
"""
    
    if snapshots_html:
        html += f"""
                        <div class="case-study-description">
                            {snapshots_html}
                        </div>
"""
    
    html += f"""
                        <a href="/case-study/{slug}" class="read-more-link">Read More</a>
                    </div>
                </div>
"""
    
    return html


def generate_case_studies_html(case_studies_list, start_index=0):
    """
    Generate HTML for multiple case study cards
    
    Args:
        case_studies_list: List of case study dictionaries with 'slug' and 'preview'
        start_index: Starting index for alternating light/dark theme
        
    Returns:
        str: Complete HTML string with all case study cards
    """
    html_output = ""
    for index, case_study_data in enumerate(case_studies_list, start=start_index):
        html_output += generate_case_study_card(case_study_data, index)
    
    return html_output