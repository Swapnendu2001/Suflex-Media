from components.header import header_style, header_content
from components.footer import footer_style, footer_content
from components.portfolio.portfolio_hero_section import portfolio_hero_section_css, portfolio_hero_section_html
from components.portfolio.portfolio_case_study_section import portfolio_case_study_section_css, portfolio_case_study_section_html


def portfolio():
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
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Portfolio - Suflex Media</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap" rel="stylesheet">
            {style}
            {header_style()}
            {portfolio_hero_section_css()}
            {portfolio_case_study_section_css()}
            {footer_style()}
            
        </head>
        <body>
            {header_content()}
            <div class="content-wrapper">
                {portfolio_hero_section_html()}
                {portfolio_case_study_section_html()}
            </div>
            {footer_content()}
        </body>
    </html>
    """
