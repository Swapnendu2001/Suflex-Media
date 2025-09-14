def homepage_hero_section_style():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');
        
        .hero-section {
            position: relative;
            width: 100vw;
            height: 150vh;
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
            width: 75vw;
            height: auto;
            left: 12.5vw;
            top: 5vh;
            
            font-family: 'Lexend', sans-serif;
            font-style: normal;
            font-weight: 700;
            font-size: 5vw;
            line-height: 1.2;
            text-align: center;
            letter-spacing: -0.04em;
            
            color: #080808;
            margin: 0;
        }
        
        .hero-section .highlight {
            font-weight: 700;
            color: #017AFF;
        }
        
        /* Sub heading */
        .hero-section .sub-heading {
            position: absolute;
            width: 32.25vw;
            height: auto;
            left: calc(50% - 16.125vw);
            top: 35vh;
            
            font-family: 'Lexend', sans-serif;
            font-style: normal;
            font-weight: 300;
            font-size: 1.5vw;
            line-height: 1.5;
            text-align: center;
            
            color: #080808;
            margin: 0;
        }
        
        /* CTA Button Container */
        .cta-container {
            display: flex;
            justify-content: center;
            align-items: center;
            position: absolute;
            width: 24vw;
            height: 7vh;
            left: 38vw;
            top: 45vh;
            filter: drop-shadow(0px 0.34vh 0.21vh rgba(0, 0, 0, 0.25));
        }
        
        /* CTA Button */
        .hero-section .cta-button {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            background: #017AFF;
            border-radius: 3vh;
            text-decoration: none;
        }
        
        .cta-inner {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1vw;
        }
        
        .cta-text {
            font-family: 'Lexend', sans-serif;
            font-weight: 400;
            font-size: 1.5vw;
            color: #FFFFFF;
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
            height: 2.0vh;
        }
        
        /* Trusted Logos */
        .trusted-logos {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            padding: 0;
            gap: 1.72vw;
            
            position: absolute;
            width: 48.42vw;
            height: 3.94vh;
            left: calc(50% - 23.71vw);
            top: 59vh;
        }
        
        .trusted-logos .brandlution {
            width: 12.90vw;
            height: 5.67vh;
            background: url('/static/brandlution.png') no-repeat center;
            background-size: contain;
        }
        
        .trusted-logos .excelra {
            width: 11.41vw;
            height: 4.30vh;
            background: url('/static/excelra.png') no-repeat center;
            background-size: contain;
        }
        
        .trusted-logos .decisionalgo {
            width: 17.69vw;
            height: 6.94vh;
            background: url('/static/decisionalgo.png') no-repeat center;
            background-size: contain;
        }
        
        /* Left Side Card */
        .side-card-left {
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            padding: 4vh 3vw;
            
            position: absolute;
            width: 20vw;
            height: 80vh;
            left: 5vw;
            top: 58vh;
            
            background: url('/static/idea.gif') no-repeat center, #FBFBFB;
            background-size: cover;
            border: 1px solid #000000;
            box-shadow: 0.28vw -0.42vh 0.47vw rgba(0, 0, 0, 0.25);
            border-radius: 6.33vh;
        }
        
        .side-card-left h3 {
            font-family: 'Lexend', sans-serif;
            font-weight: 500;
            font-size: 1.8vw;
            text-align: left;
            color: #080808;
            margin: 0;
        }
        
        /* Right Side Card */
        .side-card-right {
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            padding: 4vh 3vw;
            
            position: absolute;
            width: 20vw;
            height: 80vh;
            right: 5vw;
            top: 58vh;
            
            background: url('/static/6913652_Motion_Graphics_Motion_Graphic_1080x1920.gif') no-repeat center;
            background-size: cover;
            filter: drop-shadow(0.28vw -0.42vh 0.47vw rgba(0, 0, 0, 0.25));
            border-radius: 6.33vh;
        }
        
        .side-card-right h3 {
            font-family: 'Lexend', sans-serif;
            font-weight: 500;
            font-size: 1.8vw;
            text-align: left;
            color: #000000;
            margin: 0;
        }
        
        /* Center Block */
        .stats-container {
            position: absolute;
            display: flex;
            flex-direction: row;
            gap: 1.13vw;
            width: 44vw;
            height: 20vh;
            left: 28vw;
            top: 70vh;
        }
        
        .stat-box-left, .stat-box-right {
            box-sizing: border-box;
            width: 21.435vw;
            height: 20vh;
            background: #2D91FF;
            box-shadow: 0.16vw -0.25vh 0.28vw rgba(0, 0, 0, 0.25);
            border-radius: 2.98vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1vh 1vw;
        }
        
        .stat-inner-left, .stat-inner-right {
            display: flex;
            align-items: center;
            gap: 1vw;
            width: 100%;
        }
        
        .stat-icon-left, .stat-icon-right {
            flex-shrink: 0;
        }

        .stat-icon-left {
            width: 8vw;
            height: 11vh;
            background: url('/static/icons/brand-asset-management.png') no-repeat center;
            background-size: contain;
        }
        
        .stat-text-left, .stat-text-right {
            font-family: 'Lexend', sans-serif;
            font-weight: 500;
            font-size: 1.2vw;
            line-height: 1.2;
            color: #FFFFFF;
            text-align: center;
        }
        
        .stat-icon-right {
            width: 4vh;
            height: 4vh;
            background: url('/static/icons/open-book.png') no-repeat center;
            background-size: contain;
        }
        
        .center-main-card {
            box-sizing: border-box;
            position: absolute;
            width: 44vw;
            height: 46vh;
            left: 28vw;
            top: 92vh;
            
            background: url('/static/sequence_01_3.gif') no-repeat center;
            background-size: cover;
            filter: drop-shadow(0.13vw -0.19vh 0.21vw rgba(0, 0, 0, 0.25));
            border-radius: 3.5vh;
            
            display: flex;
            align-items: center;
            padding: 2vh 2vw;
        }
        
        .center-main-card h3 {
            font-family: 'Lexend', sans-serif;
            font-weight: 500;
            font-size: 2vw;
            color: #FFFFFF;
            margin: 0;
        }
    </style>
    """

def homepage_hero_section_content():
    return """
    <section class="hero-section">
        <div class="hero-content">
            <!-- Main Heading -->
            <h1>We Obsess Over Your Brand so <br><span class="highlight">You Don't Have To</span></h1>
            
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

            <!-- Left Side Card -->
            <div class="side-card-left">
                <h3>Turning Ideas into Books</h3>
            </div>
            
            <!-- Right Side Card -->
            <div class="side-card-right">
                <h3>Turning Content into Lead Magnets</h3>
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
                <h3>Turning<br>Leaders into<br>Thought<br>Leaders</h3>
            </div>
        </div>
    </section>
    """
