def header_style():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;700&display=swap');
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 2.25vw 4.75vw;
            background-color: #fff;
            font-family: 'Lexend', sans-serif;
            height: 8vh;
            box-shadow: 0 0.68vw 4.83vw 0 #017AFF;
            gap: 0.625vw;
            top: 0;
            left: 0;
            right: 0;
            width: 100vw;
            height: 15vh;
            box-sizing: border-box;
            z-index: 1000;
            margin: 0;
        }
        .logo img {
            height: 7vh;
        }
        .nav-links {
            display: flex;
            gap: 1.25vw;
        }
        .nav-links a {
            text-decoration: none;
            color: #000;
            font-size: 1.25vw;
        }
        .contact-us {
            display: flex;
            align-items: center;
            gap: 0.5vw;
            text-decoration: none;
            color: #000;
            font-size: 1.25vw;
        }
        .contact-us .icon {
            width: 1.56vw;
            height: 2.5vh;
            flex: none;
            order: 0;
            flex-grow: 0;
        }
    </style>
    """

def header_content():
    return """
    <header class="header">
        <div class="logo">
            <img src="/static/logo_header.png" alt="Suflex Media Logo">
        </div>
        <nav class="nav-links">
            <a href="/">Home</a>
            <a href="/about">About Us</a>
            <a href="/services">Services</a>
            <a href="/portfolio">Portfolio</a>
            <a href="/blog">Blog</a>
            <a href="/careers">Careers</a>
        </nav>
        <a href="/contact" class="contact-us">
            <img src="/static/icons/phone-icon.png" alt="Phone icon" class="icon">
            <span>Contact Us</span>
        </a>
    </header>
    """