from components.header import header_style, header_content
from components.footer import footer_style, footer_content
from components.homepage_hero_section import homepage_hero_section_style, homepage_hero_section_content



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
        }
        .content-wrapper {
            margin-top: 15vh;
        }
    </style>
    """
    return f"""
    <html>
        <head>
            <title>Suflex Media</title>
            {style}
            {header_style()}
            {homepage_hero_section_style()}
            {footer_style()}
            
        </head>
        <body>
            {header_content()}
            <div class="content-wrapper">
                {homepage_hero_section_content()}
            </div>
            {footer_content()}
        </body>
    </html>
    """