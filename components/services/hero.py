def hero_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;700&display=swap');
        
        .services-hero {
            background: transparent;
            padding: 8vh 5vw;
            text-align: center;
            min-height: 50vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: 'Lexend', sans-serif;
        }
        
        .services-hero h1 {
            font-size: 5vw;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 3vh;
            line-height: 1.2;
            font-family: 'Lexend', sans-serif;
        }
        
        .services-hero h1 .highlight {
            color: #017AFF;
            display: block;
        }
        
        .services-hero .tagline {
            font-size: 1.5vw;
            color: #333;
            margin-bottom: 4vh;
            font-weight: 400;
            font-family: 'Lexend', sans-serif;
        }
        
        .services-hero .cta-button {
            background: #017AFF;
            color: white;
            border: none;
            padding: 1.5vh 1vw;
            font-size: 1.3vw;
            border-radius: 1.3vw;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 1vw;
            transition: all 0.3s ease;
            box-shadow: 0 0.5vh 2vh rgba(0, 102, 255, 0.3);
            font-family: 'Lexend', sans-serif;
        }
        
        .services-hero .cta-button:hover {
            background: #0052CC;
            transform: translateY(-0.3vh);
            box-shadow: 0 0.8vh 2.5vh rgba(0, 102, 255, 0.4);
        }
        
        .services-hero .cta-button .icon {
            width: 2vw;
            height: 2vw;
            fill: white;
        }
        
        .services-difference {
            background: #0066FF;
            padding: 0vh 0vw;
            padding-left: 10vh;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 5vw;
            align-items: center;
            position: relative;
            overflow: hidden;
            font-family: 'Lexend', sans-serif;
        }
        
        .services-difference::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 70%;
            height: 100%;
            background-image: url('/static/doodles-hero-section-services.png');
            background-size: cover;
            background-position: left center;
            background-repeat: no-repeat;
            opacity: 0.3;
            pointer-events: none;
            z-index: 0;
        }
        
        .services-difference::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                url('/static/icons/phone.svg'),
                url('/static/icons/chat.svg'),
                url('/static/icons/lightning.svg'),
                url('/static/icons/cloud.svg');
            background-size: 5vw 5vw;
            background-position: 10% 20%, 80% 15%, 20% 70%, 90% 80%;
            background-repeat: no-repeat;
            opacity: 0.1;
            pointer-events: none;
            z-index: 0;
        }
        
        .services-difference .content {
            color: white;
            z-index: 1;
        }
        
        .services-difference h2 {
            font-size: 3.5vw;
            font-weight: 700;
            margin-bottom: 3vh;
            line-height: 1.3;
            font-family: 'Lexend', sans-serif;
        }
        
        .services-difference p {
            font-size: 1.4vw;
            line-height: 1.6;
            margin-bottom: 2vh;
            font-family: 'Lexend', sans-serif;
        }
        
        .services-difference .image-container {
            position: relative;
            z-index: 1;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .services-difference img {
            max-width: 100%;
            height: auto;
            filter: drop-shadow(0 2vh 4vh rgba(0, 0, 0, 0.2));
        }
        
        .mobile-book-header {
            display: none;
        }
        
        .services-stats {
            background: url('/static/what goes into a book background.jpg') center center/cover no-repeat;
            padding: 8vh 5vw;
            text-align: center;
            position: relative;
            font-family: 'Lexend', sans-serif;
        }
        
        .services-stats::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            z-index: 0;
        }
        
        .services-stats > * {
            position: relative;
            z-index: 1;
        }
        
        .services-stats h2 {
            color: white;
            font-size: 3.5vw;
            font-weight: 700;
            margin-bottom: 6vh;
            font-family: 'Lexend', sans-serif;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 5vw;
            margin-bottom: 5vh;
        }
        
        .stat-card {
            padding: 3vh 2vw;
        }
        
        .stat-card .number {
            font-size: 5vw;
            font-weight: 700;
            color: white;
            margin-bottom: 2vh;
            font-family: 'Lexend', sans-serif;
        }
        
        .stat-card .description {
            font-size: 1.5vw;
            color: #ccc;
            line-height: 1.4;
            font-family: 'Lexend', sans-serif;
        }
        
        .services-stats .cta-button {
            background: white;
            color: #000;
            border: none;
            padding: 1.5vh 3vw;
            font-size: 1.3vw;
            border-radius: 5vw;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Lexend', sans-serif;
        }
        
        .services-stats .cta-button:hover {
            background: #f0f0f0;
            transform: translateY(-0.3vh);
        }
        
        @media (max-width: 768px) {
            .services-hero {
                padding: 6vh 6vw;
                min-height: 40vh;
                margin-top: -15vh;
            }

            .services-difference img {
                max-width: 96vw;
                height: auto;
                filter: drop-shadow(0 2vh 4vh rgba(0, 0, 0, 0.2));
                margin-top: -10vh;
            }
            
            .services-hero h1 {
                font-size: 8vw;
                margin-bottom: 2.5vh;
            }
            
            .services-hero .tagline {
                font-size: 4vw;
                margin-bottom: 3vh;
            }
            
            .services-hero .cta-button {
                font-size: 4vw;
                padding: 2vw 2vw 2vw 2vw;
                border-radius: 9vw;
                gap: 2vw;
            }
            
            .services-hero .cta-button .icon {
                width: 5vw;
                height: 5vw;
            }
            
            .cta-icon {
                width: 5vh;
                height: 5vh;
            }
            
            .cta-icon img {
                width: 2.5vh;
                height: 2.5vh;
            }
            
            .services-difference {
                grid-template-columns: 1fr;
                gap: 4vh;
                padding: 5vh 6vw;
                padding-left: 6vw;
                margin-bottom: -8vh;
            }
            
            .services-difference::before {
                width: 100%;
                opacity: 0.2;
            }
            
            .services-difference h2 {
                font-size: 4.5vw;
                margin-bottom: 2.5vh;
            }
            
            .services-difference p {
                font-size: 4vw;
                margin-bottom: 2vh;
            }
            
            .services-difference .image-container {
                margin-bottom: 3vh;
            }
            
            .services-stats {
                padding: 6vh 6vw;
            }
            
            .services-stats h2 {
                display: none;
            }
            
            .mobile-book-header {
                display: block;
                background: white;
                padding: 4vh 6vw;
                text-align: center;
                margin-top: 9vh;
            }
            
            .mobile-book-header h2 {
                font-size: 9vw;
                font-weight: 300;
                color: #017AFF;
                margin: 0;
                font-family: 'Lexend', sans-serif;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 3vw;
                margin-bottom: 4vh;
            }
            
            .stat-card {
                padding: 3vh 2vw;
            }
            
            .stat-card:nth-child(3) {
                grid-column: 1 / -1;
                justify-self: center;
                max-width: 50%;
            }
            
            .stat-card .number {
                font-size: 10vw;
                margin-bottom: 1.5vh;
            }
            
            .stat-card .description {
                font-size: 3.5vw;
                line-height: 1.3;
            }
            
            .services-stats .cta-button {
                font-size: 4vw;
                padding: 2vh 6vw;
                border-radius: 9vw;
            }
        }
        .cta-icon {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 4.0vh;
                height: 4.0vh;
                background: #FFFFFF;
                border-radius: 50%;
            }
            
        .cta-icon img {
                width: 2.0vh;
                height: 1.0vh;
        }
    </style>
    """

def hero_html():
    return """
    <section class="services-hero">
        <h1>
            Books Don't Write Themselves,
            <span class="highlight">But We Can Write Yours</span>
        </h1>
        <p class="tagline">Book Ghostwriting Services Transforming Ideas Into Bestsellers since 2020</p>
        <button class="cta-button">
            Book a free strategy call
            <div class="cta-icon">
                            <img src="/static/icons/arrow.png" alt="arrow">
            </div>
        </button>
    </section>
    
    <section class="services-difference">
        <div class="content">
            <h2>What Makes Ghostwriting Services Different From Other Industries?</h2>
            <p>Ghostwriters like us don't see authors as just clients—because writing a book isn't a transaction, it's a journey.</p>
            <p>For the next 4-6 months, we'll be on that journey with you, shaping your ideas into something extraordinary.</p>
        </div>
        <div class="image-container">
            <img src="static/services-hero.png" alt="Ghost writer at desk" />
        </div>
    </section>
    
    <section class="mobile-book-header">
        <h2>What Goes Into a Book?</h2>
    </section>

    <section class="services-stats">
        <h2>What Goes Into a Book?</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="number">04</div>
                <div class="description">Months of Content<br/>Creation</div>
            </div>
            <div class="stat-card">
                <div class="number">500+</div>
                <div class="description">Hours of In-depth<br/>Research</div>
            </div>
            <div class="stat-card">
                <div class="number">300+</div>
                <div class="description">Pages Infused with<br/>Precision</div>
            </div>
        </div>
        <button class="cta-button">Book a free strategy call</button>
    </section>
    """
