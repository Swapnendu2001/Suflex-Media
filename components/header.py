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
            height: 15vh;
            box-shadow: 0 0.68vw 4.83vw 0 #017AFF;
            gap: 0.625vw;
            top: 0;
            left: 0;
            right: 0;
            width: 100%;
            box-sizing: border-box;
            z-index: 1000;
            margin: 0;
            position: relative;
            overflow: hidden;
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
        
        /* Hide Contact Us inside nav-links on desktop */
        .nav-links .contact-us {
            display: none;
        }
        
        /* Hamburger Menu */
        .hamburger {
            display: none;
            flex-direction: column;
            gap: 5px;
            cursor: pointer;
            z-index: 1001;
        }
        .hamburger span {
            width: 25px;
            height: 3px;
            background-color: #000;
            transition: all 0.3s ease;
        }
        .hamburger.active span:nth-child(1) {
            transform: rotate(45deg) translate(5px, 4px);
        }
        .hamburger.active span:nth-child(2) {
            opacity: 0;
        }
        .hamburger.active span:nth-child(3) {
            transform: rotate(-45deg) translate(7px, -7px);
        }
        
        /* Tablet Responsive */
        @media (max-width: 1024px) {
            .nav-links {
                gap: 1vw;
            }
            .nav-links a {
                font-size: 1.5vw;
            }
            .contact-us {
                font-size: 1.5vw;
            }
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            .header {
                padding: 4vw 6vw !important;
                height: 12vh !important;
                justify-content: center !important;
                position: relative !important;
                overflow: visible !important;
            }
            .logo {
                position: absolute !important;
                left: 50% !important;
                transform: translateX(-50%) !important;
            }
            .logo img {
                height: 6vh !important;
            }
            .nav-links {
                position: fixed !important;
                top: 12vh !important;
                left: -100% !important;
                width: 100vw !important;
                height: calc(100vh - 12vh) !important;
                background-color: #fff !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: flex-start !important;
                padding-top: 5vh !important;
                gap: 4vh !important;
                transition: left 0.3s ease !important;
                z-index: 999 !important;
                overflow-y: auto !important;
            }
            .nav-links.active {
                left: 0 !important;
            }
            .nav-links a {
                font-size: 5vw !important;
                padding: 2vh 0 !important;
                width: 80% !important;
                text-align: center !important;
            }
            /* Show Contact Us inside nav-links on mobile */
            .nav-links .contact-us {
                display: flex !important;
                font-size: 5vw !important;
                gap: 3vw !important;
                justify-content: center !important;
                align-items: center !important;
            }
            .nav-links .contact-us .icon {
                width: 6vw !important;
                height: 3vh !important;
            }
            .hamburger {
                display: flex !important;
                position: absolute !important;
                right: 6vw !important;
                top: 50% !important;
                transform: translateY(-50%) !important;
                z-index: 1001 !important;
            }
            /* Hide desktop contact-us button on mobile, show it in menu */
            .header > .contact-us {
                display: none !important;
            }
        }
        
        /* Extra small mobile devices */
        @media (max-width: 480px) {
            .header {
                padding: 3vw 5vw !important;
                height: 10vh !important;
                box-shadow: none;
            }
            .logo img {
                height: 5vh !important;
            }
            .nav-links {
                top: 10vh !important;
                height: calc(100vh - 10vh) !important;
            }
            .hamburger {
                width: 30px !important;
            }
            .hamburger span {
                width: 30px !important;
                height: 3px !important;
            }
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
            <a href="/contact" class="contact-us">
                <img src="/static/icons/phone-icon.png" alt="Phone icon" class="icon">
                <span>Contact Us</span>
            </a>
        </nav>
        <a href="/contact" class="contact-us">
            <img src="/static/icons/phone-icon.png" alt="Phone icon" class="icon">
            <span>Contact Us</span>
        </a>
        <div class="hamburger">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </header>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const hamburger = document.querySelector('.hamburger');
            const navLinks = document.querySelector('.nav-links');
            
            if (hamburger) {
                hamburger.addEventListener('click', function() {
                    hamburger.classList.toggle('active');
                    navLinks.classList.toggle('active');
                });
                
                // Close menu when clicking on a link
                const links = navLinks.querySelectorAll('a');
                links.forEach(link => {
                    link.addEventListener('click', function() {
                        hamburger.classList.remove('active');
                        navLinks.classList.remove('active');
                    });
                });
            }
        });
    </script>
    """