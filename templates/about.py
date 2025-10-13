from components.header import header_style, header_content
from components.footer import footer_style, footer_content
from components.about.about_hero_section import about_hero_section_style, about_hero_section_content
from components.about.about_best_section import best_section_css, best_section_html
from components.about.about_third_section import about_third_section_css, about_third_section_html

def about():
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
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>About Us - Suflex Media</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap" rel="stylesheet">
            {style}
            {header_style()}
            {about_hero_section_style()}
            {best_section_css()}
            {about_third_section_css()}
            {footer_style()}
        </head>
        <body>
            {header_content()}
            <div class="content-wrapper">
                {about_hero_section_content()}
                {best_section_html()}
                {about_third_section_html()}
            </div>
            {footer_content()}
        </body>
    </html>
    """