from components.header import header_style, header_content
from components.footer import footer_style, footer_content

def contact_css():
    return """
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Lexend', sans-serif;
        }

        html, body {
            background: #e8ecf0;
            width: 100%;
            overflow-x: hidden;
        }

        .contact-container {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 12vh 0vh 0vh 0vh;
        }

        .contact-wrapper {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0;
            width: 100%;
            min-height: 80vh;
            position: relative;
        }

        .contact-wrapper::before {
            content: '';
            position: absolute;
            left: 50%;
            top: 10%;
            bottom: 10%;
            width: 0.2vw;
            background: #c8cdd3;
            transform: translateX(-50%);
        }

        .contact-form-section {
            padding: 8vh 12vw;
            background: transparent;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .contact-form-section h2 {
            font-size: 3vh;
            color: #1a1a1a;
            margin-bottom: 4vh;
            line-height: 1.5;
            font-weight: 600;
        }

        .form-group {
            margin-bottom: 2.5vh;
        }

        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2vw;
            margin-bottom: 2.5vh;
        }

        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 2vh 2vw;
            border: none;
            background: #d8dce2;
            border-radius: 1vh;
            font-size: 1.8vh;
            font-family: 'Lexend', sans-serif;
            color: #333;
            outline: none;
            transition: all 0.3s ease;
        }

        .form-group input::placeholder,
        .form-group textarea::placeholder {
            color: #999;
            font-weight: 400;
        }

        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            background: #cfd3d9;
        }

        .form-group select {
            appearance: none;
            color: #999;
            background-color: #d8dce2;
            background-image: url('data:image/svg+xml;charset=UTF-8,<svg width="14" height="8" viewBox="0 0 14 8" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 1L7 7L13 1" stroke="%23666" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>');
            background-repeat: no-repeat;
            background-position: right 2vw center;
            padding-right: 4vw;
            cursor: pointer;
        }

        .form-group textarea {
            min-height: 18vh;
            resize: vertical;
            font-family: 'Lexend', sans-serif;
        }

        .checkbox-group {
            display: flex;
            align-items: flex-start;
            gap: 1.5vw;
            margin-bottom: 3vh;
            margin-top: 3vh;
        }

        .checkbox-group input[type="checkbox"] {
            width: 2.2vh;
            height: 2.2vh;
            min-width: 2.2vh;
            margin-top: 0.2vh;
            cursor: pointer;
            accent-color: #0d6efd;
        }

        .checkbox-group label {
            font-size: 1.6vh;
            color: #666;
            line-height: 1.6;
            font-weight: 400;
        }

        .submit-btn {
            background: #0d6efd;
            color: white;
            border: none;
            padding: 2vh 6vw;
            border-radius: 1vh;
            font-size: 2vh;
            font-family: 'Lexend', sans-serif;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-block;
            box-shadow: 0 0.4vh 1vh rgba(13, 110, 253, 0.3);
        }

        .submit-btn:hover {
            background: #0b5ed7;
            transform: translateY(-0.2vh);
            box-shadow: 0 0.6vh 1.5vh rgba(13, 110, 253, 0.4);
        }

        .submit-btn:active {
            transform: translateY(0);
        }

        .contact-info-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 8vh 8vw;
            background: transparent;
        }

        .illustration {
            width: 100%;
            max-width: 35vw;
            height: auto;
            margin-bottom: 4vh;
            object-fit: contain;
        }

        .contact-info-section h3 {
            font-size: 2.2vh;
            color: #1a1a1a;
            margin-bottom: 1vh;
            font-weight: 500;
        }

        .contact-info-section h2 {
            font-size: 4.5vh;
            color: #1a1a1a;
            margin-bottom: 3vh;
            font-weight: 700;
        }

        .phone-number {
            font-size: 4.5vh;
            color: #0d6efd;
            font-weight: 700;
            margin-bottom: 2vh;
            text-decoration: none;
            display: block;
            letter-spacing: 0.05vh;
        }

        .email-address {
            font-size: 2.2vh;
            color: #1a1a1a;
            text-decoration: none;
            display: block;
            font-weight: 400;
        }

        .email-address:hover,
        .phone-number:hover {
            opacity: 0.8;
        }

        @media (max-width: 1024px) {
            .contact-form-section {
                padding: 6vh 8vw;
            }

            .illustration {
                max-width: 40vw;
            }
        }

        @media (max-width: 768px) {
            .contact-wrapper::before {
                display: none;
            }

            .contact-wrapper {
                grid-template-columns: 1fr;
            }

            .form-row {
                grid-template-columns: 1fr;
                gap: 2.5vh;
            }

            .illustration {
                max-width: 60vw;
            }

            .contact-form-section h2 {
                font-size: 2.4vh;
            }

            .contact-info-section h2 {
                font-size: 3.8vh;
            }

            .phone-number {
                font-size: 3.8vh;
            }

            .contact-form-section,
            .contact-info-section {
                padding: 5vh 6vw;
            }
        }
    </style>
    """

def contact_html():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contact Us - Suflex Media</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap" rel="stylesheet">
        {header_style()}
        {contact_css()}
        {footer_style()}
    </head>
    <body>
        {header_content()}

        <div class="contact-container">
            <div class="contact-wrapper">
                <div class="contact-form-section">
                    <h2>Have An Enquiry Or Some Feedback For Us?<br>Fill Out The Form Below To Contact Our Team.</h2>
                    
                    <form id="contactForm">
                        <div class="form-row">
                            <div class="form-group">
                                <input type="text" name="name" placeholder="Name" required>
                            </div>
                            <div class="form-group">
                                <input type="email" name="email" placeholder="Email" required>
                            </div>
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <input type="tel" name="phone" placeholder="Phone Number" required>
                            </div>
                            <div class="form-group">
                                <select name="service" required>
                                    <option value="" disabled selected>Select Service</option>
                                    <option value="web-development">Web Development</option>
                                    <option value="app-development">App Development</option>
                                    <option value="digital-marketing">Digital Marketing</option>
                                    <option value="seo">SEO Services</option>
                                    <option value="graphic-design">Graphic Design</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <textarea name="message" placeholder="Message" required></textarea>
                        </div>
                        
                        <div class="checkbox-group">
                            <input type="checkbox" id="consent" name="consent" required>
                            <label for="consent">I hereby authorize to send notifications on SMS/Messages/Promotional/Informational Messages</label>
                        </div>
                        
                        <button type="submit" class="submit-btn">Submit Now</button>
                    </form>
                </div>
                
                <div class="contact-info-section">
                    <img src="/static/contact-us-hero.png" alt="Contact Illustration" class="illustration">
                    
                    <h3>Want To See Us In Action?</h3>
                    <h2>Let's Connect!</h2>
                    
                    <a href="tel:+911234567890" class="phone-number">+91 123456789</a>
                    <a href="mailto:hello@suflexmedia.com" class="email-address">hello@suflexmedia.com</a>
                </div>
            </div>
        </div>
        
        {footer_content()}
        
        <script>
            document.getElementById('contactForm').addEventListener('submit', function(e) {{
                e.preventDefault();
                alert('Thank you for your message! We will get back to you soon.');
                this.reset();
            }});
        </script>
    </body>
    </html>
    """

def contact():
    return contact_html()
