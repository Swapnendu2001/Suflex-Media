from components.header import header_style, header_content
from components.footer import footer_style, footer_content
from components.homepage_hero_section import homepage_hero_section_style, homepage_hero_section_content
from components.homepage_work_with_us import work_with_us_css, work_with_us_html
from components.homepage_scaling_section import scaling_section_css, scaling_section_html
from components.homepage_care_section import care_section_css, care_section_html
from components.homepage_insights_section import insights_section_css, insights_section_html



def homepage():
    style = """
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            margin: 0;
            padding: 0;
            font-family: 'Lexend', sans-serif;
        }
        .content-wrapper {
            margin-top: 10vh;
        }
    </style>
    """
    return f"""
    <html>
        <head>
            <title>Suflex Media</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap" rel="stylesheet">
            {style}
            {header_style()}
            {homepage_hero_section_style()}
            {work_with_us_css()}
            {scaling_section_css()}
            {care_section_css()}
            {insights_section_css()}
            {footer_style()}
            
        </head>
        <body>
            {header_content()}
            <div class="content-wrapper">
                {homepage_hero_section_content()}
                {work_with_us_html()}
                {scaling_section_html()}
                {care_section_html()}
                {insights_section_html()}
            </div>
            {footer_content()}
        </body>
    </html>
    """