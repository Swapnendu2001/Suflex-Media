from components.services.hero import hero_css, hero_html
from components.services.why_hire import why_hire_css, why_hire_html
from components.services.perfect_fit import perfect_fit_css, perfect_fit_html
from components.services.faq import faq_css, faq_html
from components.services.book_strategy_cta import book_strategy_cta_css, book_strategy_cta_html
from components.header import header_style, header_content
from components.footer import footer_style, footer_content

def services():
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
        <title>Ghostwriting Services - Suflex Media</title>
        <link rel="stylesheet" href="/static/styles.css">
        {style}
        {header_style()}
        {hero_css()}
        {why_hire_css()}
        {perfect_fit_css()}
        {faq_css()}
        {book_strategy_cta_css()}
        {footer_style()}
    </head>
    <body>
        {header_content()}
        <div class="content-wrapper">
            {hero_html()}
            {why_hire_html()}
            {perfect_fit_html()}
            {faq_html()}
            {book_strategy_cta_html()}
        </div>
        {footer_content()}
    </body>
    </html>
    """
