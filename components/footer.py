def footer_style():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;700&display=swap');
        .footer {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 5vh 5vw;
            background: linear-gradient(180deg, rgba(217, 217, 217, 0) 0%, rgba(1, 122, 255, 0.25) 100%);
            font-family: 'Lexend', sans-serif;
            gap: 5vh;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;

        }
        .footer-content {
            display: flex;
            justify-content: space-around;
            width: 100%;
            align-items: flex-start;
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
            height: 8vh;
        }
        .copyright {
            font-size: 1vw;
        }
    </style>
    """

def footer_content():
    return """
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section cta">
                <h2>Ready to grow your business?</h2>
                <a href="#" class="button">Book a free strategy call</a>
            </div>
            <div class="footer-section">
                <h3>Quick Links</h3>
                <a href="#">Home</a>
                <a href="#">About Us</a>
                <a href="#">Services</a>
                <a href="#">Blog</a>
                <a href="#">Careers</a>
            </div>
            <div class="footer-section">
                <h3>Services</h3>
                <a href="#">Book Writing</a>
                <a href="#">LinkedIn Branding</a>
                <a href="#">Content Writing</a>
                <a href="#">Performance Marketing</a>
                <a href="#">Website Development</a>
            </div>
            <div class="footer-section">
                <h3>Social Links</h3>
                <div class="social-links">
                    <a href="#"><img src="/static/icons/instagram.png" alt="Instagram"></a>
                    <a href="#"><img src="/static/icons/linkedin.png" alt="LinkedIn"></a>
                    <a href="#"><img src="/static/icons/x.png" alt="X"></a>
                </div>
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