def homepage_hero_section_style():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');
        
        .hero-section {
            position: relative;
            width: 100vw;
            height: 100vh;
            background-color: #f8fafc;
            font-family: 'Lexend', sans-serif;
            overflow: hidden;
        }
        
        .hero-content {
            position: relative;
            width: 100%;
            height: 100%;
        }
        
        /* Main Heading */
        .hero-section h1 {
            position: absolute;
            width: 75.06vw; /* 1201px at 1600px */
            height: 11.25vh; /* 180px at 1600px */
            left: calc(50% - 75.06vw/2 - 0.03vw);
            top: 20.19vh; /* 323px at 1600px */
            
            font-family: 'Lexend';
            font-style: normal;
            font-weight: 400;
            font-size: 5vw; /* 80px at 1600px */
            line-height: 6.25vh; /* 100px at 1600px */
            text-align: center;
            letter-spacing: -0.04em;
            
            color: #080808;
            margin: 0;
        }
        
        .hero-section .highlight {
            color: #017AFF;
        }
        
        /* Sub heading */
        .hero-section .sub-heading {
            position: absolute;
            width: 32.25vw; /* 516px at 1600px */
            height: 2.81vh; /* 45px at 1600px */
            left: calc(50% - 32.25vw/2 - 0.06vw);
            top: 36.13vh; /* 578px at 1600px */
            
            font-family: 'Lexend';
            font-style: normal;
            font-weight: 300;
            font-size: 2.25vw; /* 36px at 1600px */
            line-height: 2.81vh; /* 45px at 1600px */
            text-align: center;
            letter-spacing: -0.04em;
            
            color: #080808;
            margin: 0;
        }
        
        /* CTA Button Container */
        .cta-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            padding: 1.71vh 0; /* 27.4311px */
            gap: 1.71vh;
            
            position: absolute;
            width: 37.38vw; /* 598px at 1600px */
            height: 8.74vh; /* 139.9px at 1600px */
            left: 35.56vw; /* 569px at 1600px */
            top: 41.81vh; /* 669px at 1600px */
            
            filter: drop-shadow(0px 0.34vh 0.21vh rgba(0, 0, 0, 0.25));
        }
        
        /* CTA Button */
        .hero-section .cta-button {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 0.34vh 0; /* 5.48623px */
            gap: 1.71vh;
            
            width: 33.95vw; /* 543.14px at 1600px */
            height: 5.32vh; /* 85.04px at 1600px */
            
            background: #017AFF;
            border-radius: 3.6vh; /* 57.6054px at 1600px */
            
            flex: none;
            order: 0;
            align-self: stretch;
            flex-grow: 0;
            text-decoration: none;
        }
        
        .cta-inner {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            padding: 1.71vh;
            gap: 1.71vh;
            
            width: 32.89vw; /* 526.18px at 1600px */
            height: 6.24vh; /* 99.86px at 1600px */
            
            flex: none;
            order: 0;
            flex-grow: 0;
        }
        
        .cta-text {
            width: 25vw; /* 400px at 1600px */
            height: 2.81vh; /* 45px at 1600px */
            
            font-family: 'Lexend';
            font-style: normal;
            font-weight: 400;
            font-size: 2.23vw; /* 35.6605px at 1600px */
            line-height: 2.81vh; /* 45px at 1600px */
            text-align: center;
            letter-spacing: -0.04em;
            
            color: #FFFFFF;
            
            flex: none;
            order: 0;
            flex-grow: 0;
        }
        
        .cta-icon {
            display: flex;
            flex-direction: row;
            align-items: center;
            padding: 0.69vh;
            gap: 1.71vh;
            
            width: 2.74vw; /* 43.89px at 1600px */
            height: 2.74vh; /* 43.89px at 1600px */
            
            background: #FFFFFF;
            border-radius: 1.37vh; /* 21.9449px at 1600px */
            
            flex: none;
            order: 1;
            flex-grow: 0;
        }
        
        .cta-icon img {
            width: 1.37vw; /* 21.94px at 1600px */
            height: 1.37vh; /* 21.94px at 1600px */
            
            flex: none;
            order: 0;
            flex-grow: 0;
        }
        
        /* Trusted Logos */
        .trusted-logos {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            padding: 0px;
            gap: 2.72vw; /* 43.45px at 1600px */
            
            position: absolute;
            width: 47.42vw; /* 758.79px at 1600px */
            height: 3.94vh; /* 63px at 1600px */
            left: calc(50% - 47.42vw/2 + 0.02vw);
            top: 52.63vh; /* 842px at 1600px */
        }
        
        .trusted-logos .brandlution {
            width: 12.90vw; /* 206.38px at 1600px */
            height: 2.67vh; /* 42.65px at 1600px */
            background: url('/static/brandlution.png') no-repeat center;
            background-size: contain;
            flex: none;
            order: 0;
            flex-grow: 0;
        }
        
        .trusted-logos .excelra {
            width: 9.41vw; /* 150.51px at 1600px */
            height: 2.30vh; /* 36.78px at 1600px */
            background: url('/static/excelra.png') no-repeat center;
            background-size: contain;
            flex: none;
            order: 1;
            flex-grow: 0;
        }
        
        .trusted-logos .decisionalgo {
            width: 19.69vw; /* 315px at 1600px */
            height: 3.94vh; /* 63px at 1600px */
            background: url('/static/decisionalgo.png') no-repeat center;
            background-size: contain;
            flex: none;
            order: 2;
            flex-grow: 0;
        }
        
        /* Left Side Card - Turning Ideas into Books */
        .side-card-left {
            box-sizing: border-box;
            
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            padding: 2.63vh 2.91vw;
            gap: 1.39vh;
            
            position: absolute;
            width: 23.15vw; /* 370.47px at 1600px */
            height: 43.81vh; /* 701px at 1600px */
            left: 4.19vw; /* 67px at 1600px */
            top: 50.31vh; /* 805px at 1600px */
            
            background: url('/static/idea.gif') no-repeat center, #FBFBFB;
            background-size: cover;
            border: 0.03vw solid #000000;
            box-shadow: 0.28vw -0.42vh 0.47vw rgba(0, 0, 0, 0.25);
            border-radius: 3.33vh;
        }
        
        .side-card-left h3 {
            width: 17.19vw; /* 275.08px at 1600px */
            height: 5.50vh; /* 88px at 1600px */
            
            font-family: 'Lexend';
            font-style: normal;
            font-weight: 500;
            font-size: 2.22vw; /* 35.4937px at 1600px */
            line-height: 2.75vh; /* 44px at 1600px */
            display: flex;
            align-items: flex-end;
            letter-spacing: -0.04em;
            
            color: #080808;
            
            flex: none;
            order: 0;
            flex-grow: 0;
            margin: 0;
        }
        
        /* Right Side Card - Turning Content into Lead Magnets */
        .side-card-right {
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            padding: 2.36vh 2.91vw;
            gap: 1.39vh;
            
            position: absolute;
            width: 23.15vw; /* 370.47px at 1600px */
            height: 43.81vh; /* 701px at 1600px */
            left: 80.75vw; /* 1292px at 1600px */
            top: 50.31vh; /* 805px at 1600px */
            
            background: url('/static/6913652_Motion_Graphics_Motion_Graphic_1080x1920.gif') no-repeat center;
            background-size: cover;
            filter: drop-shadow(0.28vw -0.42vh 0.47vw rgba(0, 0, 0, 0.25));
            border-radius: 3.33vh;
        }
        
        .side-card-right h3 {
            width: 17.19vw; /* 275.08px at 1600px */
            height: 8.25vh; /* 132px at 1600px */
            
            font-family: 'Lexend';
            font-style: normal;
            font-weight: 500;
            font-size: 2.22vw; /* 35.4937px at 1600px */
            line-height: 2.75vh; /* 44px at 1600px */
            display: flex;
            align-items: flex-end;
            letter-spacing: -0.04em;
            
            color: #000000;
            
            flex: none;
            order: 0;
            flex-grow: 0;
            margin: 0;
        }
        
        /* Center Main Card */
        .center-main-card {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
            padding: 1.63vh 2.81vw;
            gap: 0.63vh;
            
            position: absolute;
            width: 48.81vw; /* 781px at 1600px */
            height: 20.69vh; /* 331px at 1600px */
            left: calc(50% - 48.81vw/2 - 0.03vw);
            top: 73.44vh; /* 1175px at 1600px */
            
            background: url('/static/sequence_01_3.gif') no-repeat center;
            background-size: cover;
            filter: drop-shadow(0.13vw -0.19vh 0.21vw rgba(0, 0, 0, 0.25));
            border-radius: 1.5vh;
        }
        
        .center-main-card h3 {
            width: 16vw; /* 256px at 1600px */
            height: 11.25vh; /* 180px at 1600px */
            
            font-family: 'Lexend';
            font-style: normal;
            font-weight: 500;
            font-size: 2.25vw; /* 36px at 1600px */
            line-height: 2.81vh; /* 45px at 1600px */
            display: flex;
            align-items: flex-end;
            letter-spacing: -0.04em;
            
            color: #FFFFFF;
            
            flex: none;
            order: 0;
            flex-grow: 0;
            margin: 0;
        }
        
        /* Stats Container */
        .stats-container {
            display: flex;
            flex-direction: row;
            align-items: center;
            padding: 0px;
            gap: 1.13vw; /* 18px at 1600px */
            
            position: absolute;
            width: 48.63vw; /* 778px at 1600px */
            height: 12.44vh; /* 199px at 1600px */
            left: calc(50% - 48.63vw/2 + 0.03vw);
            top: 59.81vh; /* 957px at 1600px */
        }
        
        /* Stat Box Left */
        .stat-box-left {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 0.99vh 1.73vw;
            gap: 0.82vh;
            
            width: 23.75vw; /* 380px at 1600px */
            height: 12.44vh; /* 199px at 1600px */
            
            background: #2D91FF;
            box-shadow: 0.16vw -0.25vh 0.28vw rgba(0, 0, 0, 0.25);
            border-radius: 1.98vh;
            
            flex: none;
            order: 0;
            flex-grow: 0;
        }
        
        .stat-inner-left {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            padding: 0px;
            gap: 0.49vw;
            
            width: 17.63vw; /* 282px at 1600px */
            height: 7.38vh; /* 118px at 1600px */
            
            flex: none;
            order: 0;
            flex-grow: 0;
        }
        
        .stat-icon-left {
            width: 7.09vw; /* 113.47px at 1600px */
            height: 7.09vh; /* 113.47px at 1600px */
            background: url('/static/icons/brand-asset-management.png') no-repeat center;
            background-size: contain;
            flex: none;
            order: 0;
            flex-grow: 0;
        }
        
        .stat-text-left {
            width: 10.04vw; /* 160.62px at 1600px */
            height: 4.94vh; /* 79.07px at 1600px */
            
            font-family: 'Lexend';
            font-style: normal;
            font-weight: 500;
            font-size: 1.98vw; /* 31.6291px at 1600px */
            line-height: 2.5vh; /* 40px at 1600px */
            text-align: center;
            letter-spacing: -0.04em;
            
            color: #FFFFFF;
            
            flex: none;
            order: 1;
            flex-grow: 1;
            margin: 0;
        }
        
        /* Stat Box Right */
        .stat-box-right {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 1.24vh 1.73vw;
            gap: 0.82vh;
            
            width: 23.75vw; /* 380px at 1600px */
            height: 12.44vh; /* 199px at 1600px */
            
            background: #2D91FF;
            box-shadow: 0.16vw -0.25vh 0.28vw rgba(0, 0, 0, 0.25);
            border-radius: 1.98vh;
            
            flex: none;
            order: 1;
            flex-grow: 0;
        }
        
        .stat-inner-right {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            padding: 0px;
            gap: 1.32vw;
            
            width: 18.38vw; /* 294px at 1600px */
            height: 6.44vh; /* 103px at 1600px */
            
            flex: none;
            order: 0;
            flex-grow: 0;
        }
        
        .stat-icon-right {
            width: 5.69vw; /* 91px at 1600px */
            height: 5.69vh; /* 91px at 1600px */
            background: url('/static/icons/open-book.png') no-repeat center;
            background-size: contain;
            flex: none;
            order: 0;
            flex-grow: 0;
        }
        
        .stat-text-right {
            width: 11.37vw; /* 181.91px at 1600px */
            height: 4.94vh; /* 79.07px at 1600px */
            
            font-family: 'Lexend';
            font-style: normal;
            font-weight: 500;
            font-size: 1.98vw; /* 31.6291px at 1600px */
            line-height: 2.5vh; /* 40px at 1600px */
            display: flex;
            align-items: flex-end;
            text-align: center;
            letter-spacing: -0.04em;
            
            color: #FFFFFF;
            
            flex: none;
            order: 1;
            flex-grow: 1;
            margin: 0;
        }
    </style>
    """

def homepage_hero_section_content():
    return """
    <section class="hero-section">
        <div class="hero-content">
            <!-- Main Heading -->
            <h1>We Obsess Over Your Brand so <span class="highlight">You Don't Have To</span></h1>
            
            <!-- Sub Heading -->
            <p class="sub-heading">300+ Customers Served 🙌</p>
            
            <!-- CTA Button -->
            <div class="cta-container">
                <a href="#" class="cta-button">
                    <div class="cta-inner">
                        <span class="cta-text">Book a free strategy call</span>
                        <div class="cta-icon">
                            <img src="/static/icons/arrow.png" alt="arrow">
                        </div>
                    </div>
                </a>
            </div>
            
            <!-- Trusted Logos -->
            <div class="trusted-logos">
                <div class="brandlution"></div>
                <div class="excelra"></div>
                <div class="decisionalgo"></div>
            </div>
            
            <!-- Stats Container -->
            <div class="stats-container">
                <div class="stat-box-left">
                    <div class="stat-inner-left">
                        <div class="stat-icon-left"></div>
                        <div class="stat-text-left">40+<br>Personal Brands Built</div>
                    </div>
                </div>
                <div class="stat-box-right">
                    <div class="stat-inner-right">
                        <div class="stat-icon-right"></div>
                        <div class="stat-text-right">20+<br>Books Published Annually</div>
                    </div>
                </div>
            </div>
            
            <!-- Center Main Card -->
            <div class="center-main-card">
                <h3>Turning Leaders into Thought Leaders</h3>
            </div>
            
            <!-- Left Side Card -->
            <div class="side-card-left">
                <h3>Turning Ideas into Books</h3>
            </div>
            
            <!-- Right Side Card -->
            <div class="side-card-right">
                <h3>Turning Content into Lead Magnets</h3>
            </div>
        </div>
    </section>
    """
