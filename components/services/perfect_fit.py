def perfect_fit_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;700&display=swap');
        
        .perfect-fit-section {
            background: #FFFFFF;
            padding: 8vh 5vw;
            font-family: 'Lexend', sans-serif;
        }
        
        .perfect-fit-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 5vw;
            align-items: center;
            max-width: 90vw;
            margin: 0 auto;
        }
        
        .perfect-fit-content {
            padding-right: 2vw;
        }
        
        .perfect-fit-content h2 {
            font-size: 3.5vw;
            font-weight: 700;
            color: #1A1A1A;
            margin-bottom: 3vh;
            line-height: 1.3;
            font-family: 'Lexend', sans-serif;
        }
        
        .perfect-fit-content h2 .highlight {
            color: #017AFF;
            display: block;
        }
        
        .perfect-fit-content p {
            font-size: 1.3vw;
            color: #333;
            line-height: 1.6;
            margin-bottom: 4vh;
            font-family: 'Lexend', sans-serif;
        }
        
        .perfect-fit-content .cta-button {
            background: #017AFF;
            color: white;
            border: none;
            padding: 1.5vh 3vw;
            font-size: 1.3vw;
            border-radius: 5vw;
            cursor: pointer;
            display: inline-block;
            transition: all 0.3s ease;
            font-weight: 600;
            font-family: 'Lexend', sans-serif;
            text-decoration: none;
        }
        
        .perfect-fit-content .cta-button:hover {
            background: #0052CC;
            transform: translateY(-0.3vh);
        }
        
        .perfect-fit-illustration {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .perfect-fit-illustration img {
            max-width: 100%;
            height: auto;
            filter: drop-shadow(0 1vh 3vh rgba(0, 0, 0, 0.1));
        }
        
        .brand-philosophy-section {
            background-image: url('/static/what goes into a book background.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            padding: 8vh 5vw;
            text-align: center;
            position: relative;
            overflow: hidden;
            font-family: 'Lexend', sans-serif;
        }
        
        .brand-philosophy-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            z-index: 0;
        }
        
        .brand-philosophy-section::after {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 40vw;
            height: 100%;
            background-image: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 1vh,
                rgba(255, 255, 255, 0.03) 1vh,
                rgba(255, 255, 255, 0.03) 2vh
            );
            pointer-events: none;
            z-index: 0;
        }
        
        .philosophy-content {
            position: relative;
            z-index: 1;
            max-width: 70vw;
            margin: 0 auto;
        }
        
        .philosophy-quote {
            font-size: 3vw;
            font-weight: 700;
            color: white;
            margin-bottom: 3vh;
            line-height: 1.4;
            font-family: 'Lexend', sans-serif;
        }
        
        .philosophy-attribution {
            font-size: 1.2vw;
            color: #CCCCCC;
            font-weight: 400;
            font-family: 'Lexend', sans-serif;
        }
        
        @media (max-width: 992px) {
            .perfect-fit-section {
                padding: 6vh 6vw;
            }
            
            .perfect-fit-container {
                grid-template-columns: 1fr;
                gap: 5vh;
                max-width: 100%;
            }
            
            .perfect-fit-content {
                padding-right: 0;
                text-align: center;
            }
            
            .perfect-fit-content h2 {
                font-size: 6vw;
                margin-bottom: 2.5vh;
            }
            
            .perfect-fit-content p {
                font-size: 3.5vw;
                margin-bottom: 3vh;
                line-height: 1.7;
            }
            
            .perfect-fit-content .cta-button {
                font-size: 3.5vw;
                padding: 2vh 6vw;
                border-radius: 3vw;
            }
            
            .perfect-fit-illustration {
                order: -1;
            }
            
            .brand-philosophy-section {
                padding: 6vh 6vw;
            }
            
            .philosophy-content {
                max-width: 85vw;
            }
            
            .philosophy-quote {
                font-size: 5vw;
                margin-bottom: 2.5vh;
            }
            
            .philosophy-attribution {
                font-size: 2.5vw;
            }
        }
        
        @media (max-width: 576px) {
            .perfect-fit-section {
                padding: 5vh 6vw;
            }
            
            .perfect-fit-container {
                gap: 4vh;
            }
            
            .perfect-fit-content h2 {
                font-size: 7.5vw;
                margin-bottom: 2vh;
                line-height: 1.3;
            }
            
            .perfect-fit-content p {
                font-size: 4.2vw;
                margin-bottom: 3vh;
                line-height: 1.7;
            }
            
            .perfect-fit-content .cta-button {
                font-size: 4.2vw;
                padding: 2.5vh 7vw;
                border-radius: 4vw;
            }
            
            .brand-philosophy-section {
                padding: 5vh 6vw;
            }
            
            .brand-philosophy-section::after {
                width: 60vw;
            }
            
            .philosophy-content {
                max-width: 90vw;
            }
            
            .philosophy-quote {
                font-size: 4.5vw;
                margin-bottom: 2vh;
                line-height: 1.4;
            }
            
            .philosophy-attribution {
                font-size: 3.5vw;
            }
        }
    </style>
    """

def perfect_fit_html():
    return """
    <section class="perfect-fit-section">
        <div class="perfect-fit-container">
            <div class="perfect-fit-content">
                <h2>
                    Not Seeing the Perfect Fit?
                    <span class="highlight">We've Got You.</span>
                </h2>
                <p>If your book falls within our listed categories, great! We have a proven process to bring it to life. However, as our services are fully customisable, we would be delighted to welcome the challenge and take on this voyage together.</p>
                <a href="#contact" class="cta-button">Book a free strategy call</a>
            </div>
            <div class="perfect-fit-illustration">
                <img src="/static/NotSeeingPerfectFit.png" alt="Writing illustration with books and quill">
            </div>
        </div>
    </section>
    
    <section class="brand-philosophy-section">
        <div class="philosophy-content">
            <p class="philosophy-quote">"No shortcuts. No compromises. Just exceptional books."</p>
            <p class="philosophy-attribution">- The Suflex Founding Philosophy</p>
        </div>
    </section>
    """
