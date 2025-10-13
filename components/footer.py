def footer_style():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;700&display=swap');
        .footer {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 25vh 5vh 5vw 5vw;
            background: linear-gradient(180deg, rgba(217, 217, 217, 0) 0%, rgba(1, 122, 255, 0.25) 100%);
            font-family: 'Lexend', sans-serif;
            gap: 5vh;
            position: static;
            bottom: 0;
            left: 0;
            right: 0;
            width: 100vw;

        }
        .footer-content {
            display: flex;
            justify-content: space-around;
            width: 100vw;
            align-items: flex-start;
            padding: 0 5vw;
        }
        .footer-section {
            display: flex;
            flex-direction: column;
            gap: 1.5vh;
        }
        .footer-section h3 {
            font-size: 1.5vw;
            margin-bottom: 1vh;
        }
        .footer-section a, .footer-section p {
            text-decoration: none;
            color: #000;
            font-size: 1.1vw;
        }
        .footer-section.cta {
            border-right: 3px solid #000;
            padding-right: 2vw;
        }
        .footer-section.cta h2 {
            font-size: 2vw;
            color: #017AFF;
        }
        .footer-section.cta .button {
            background-color: #017AFF;
            color: #fff;
            padding: 1.5vh 2vw;
            border-radius: 0.5vw;
            text-align: center;
            font-size: 1.2vw;
        }
        .social-links {
            display: flex;
            gap: 1vw;
        }
        .social-links img {
            width: 2vw;
            height: 2vw;
        }
        .footer-bottom {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2vh;
            border-top: 1px solid #ddd;
            padding-top: 3vh;
            width: 100%;
        }
        .footer-logo img {
            height: 15vh;
        }
        .copyright {
            font-size: 1vw;
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            .footer {
                padding: 15vh 8vw 8vw 8vw;
            }
            .footer-content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                grid-template-rows: auto auto auto;
                gap: 6vh 6vw;
                padding: 0;
                width: 100%;
            }
            .footer-section.cta {
                grid-column: 1 / -1;
                border-right: none;
                padding-right: 0;
                text-align: center;
            }
            .footer-section {
                text-align: left;
                width: 100%;
            }
            .footer-section h3 {
                font-size: 5vw;
                margin-bottom: 2vh;
            }
            .footer-section a, .footer-section p {
                font-size: 4vw;
            }
            .footer-section.cta h2 {
                font-size: 8vw;
            }
            .footer-section.cta .button {
                font-size: 4vw;
                padding: 2vh 6vw;
                border-radius: 2vw;
                max-width: 60vw;
                margin: 0 auto;
            }
            .social-links {
                justify-content: flex-start;
                gap: 4vw;
            }
            .social-links img {
                width: 8vw;
                height: 8vw;
            }
            .footer-logo img {
                height: 10vh;
            }
            .copyright {
                font-size: 3.5vw;
                text-align: center;
            }
        }
    </style>
    """

def footer_content():
    return """
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section cta">
                <h2>Ready to grow your<br>business?</h2>
                <a href="#" class="button">Book a free strategy call</a>
            </div>
            <div class="footer-section">
                <h3>Quick Links</h3>
                <a href="/">Home</a>
                <a href="/about">About Us</a>
                <a href="/services">Services</a>
                <a href="/blog">Blog</a>
                <a href="/careers">Careers</a>
            </div>
            <div class="footer-section">
                <h3>Services</h3>
                <a href="/services">Book Writing</a>
                <a href="/services">LinkedIn Branding</a>
                <a href="/services">Content Writing</a>
                <a href="/services">Performance Marketing</a>
                <a href="/services">Website Development</a>
            </div>
            <div class="footer-section social-section">
                <h3>Social Links</h3>
                <div class="social-links">
                    <a href="#"><img src="/static/icons/instagram.png" alt="Instagram"></a>
                    <a href="#"><img src="/static/icons/linkedin.png" alt="LinkedIn"></a>
                    <a href="#"><img src="/static/icons/x.png" alt="X"></a>
                </div>
            </div>
            <div class="footer-section contact-section">
                <h3>Contact Us</h3>
                <a href="mailto:hello@suflexmedia.com">hello@suflexmedia.com</a>
            </div>
        </div>
        <div class="footer-bottom">
            <div class="footer-logo">
                <img src="/static/logo_header.png" alt="Suflex Media Logo">
            </div>
            <div class="copyright">
                <p>Copyright © 2024 SuflexMedia | All Rights Reserved</p>
            </div>
        </div>
    </footer>
    """