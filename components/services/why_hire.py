def why_hire_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700&display=swap');
        
        .suflex-media-intro {
            padding: 8vh 5vw;
            text-align: center;
            font-family: 'Lexend', sans-serif;
        }
        
        .suflex-media-intro .section-title {
            font-size: 3.5vw;
            font-weight: 700;
            color: #1A1A1A;
            margin-bottom: 3vh;
            font-family: 'Lexend', sans-serif;
        }
        
        .suflex-media-intro .section-description {
            font-size: 1.4vw;
            color: #333;
            max-width: 55vw;
            margin: 0 auto 6vh auto;
            line-height: 1.6;
            font-family: 'Lexend', sans-serif;
        }
        
        .key-metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 2.5vw;
            padding: 0 8vw;
            margin-bottom: 10vh;
        }
        
        .metric-card {
            border: 0.2vw solid #017AFF;
            border-radius: 2vh;
            padding: 4vh 2vw;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 28vh;
            background: white;
            font-family: 'Lexend', sans-serif;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .metric-card:hover {
            background: #017AFF;
        }
        
        .metric-card .metric-icon {
            width: 7vh;
            height: 7vh;
            margin-bottom: 2.5vh;
            transition: filter 0.3s ease;
        }
        
        .metric-card:hover .metric-icon {
            filter: brightness(0) invert(1);
        }
        
        .metric-card .metric-value {
            font-size: 3.5vw;
            font-weight: 700;
            color: #1A1A1A;
            margin-bottom: 1.5vh;
            font-family: 'Lexend', sans-serif;
            transition: color 0.3s ease;
        }
        
        .metric-card:hover .metric-value {
            color: #FFFFFF;
        }
        
        .metric-card .metric-label {
            font-size: 1.1vw;
            color: #1A1A1A;
            font-weight: 400;
            font-family: 'Lexend', sans-serif;
            transition: color 0.3s ease;
        }
        
        .metric-card:hover .metric-label {
            color: #FFFFFF;
        }
        
        .book-types-section {
            padding: 8vh 5vw;
            background: #FFFFFF;
            font-family: 'Lexend', sans-serif;
            position: relative;
        }
        
        .book-types-section::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3vh;
            background: linear-gradient(to bottom, rgba(1, 122, 255, 0) 0%, rgba(1, 122, 255, 0.4) 100%);
            pointer-events: none;
        }
        
        .book-types-section .section-subtitle {
            font-size: 3.5vw;
            font-weight: 700;
            color: #1A1A1A;
            text-align: center;
            margin-bottom: 6vh;
            font-family: 'Lexend', sans-serif;
        }
        
        .book-types-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 3vw;
            max-width: 75vw;
            margin: 0 auto 6vh auto;
        }
        
        .book-type-card {
            border: 0.1vw solid #E8E8E8;
            border-radius: 1.5vh;
            padding: 3.5vh 2.5vw;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            background-color: white;
            box-shadow: 0 0.2vh 1vh rgba(0,0,0,0.05);
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            font-family: 'Lexend', sans-serif;
            min-height: 18vh;
            justify-content: center;
        }
        
        .book-type-card:hover {
            transform: translateY(-0.8vh);
            box-shadow: 0 0.8vh 2vh rgba(0,0,0,0.1);
        }
        
        .book-type-card .book-type-icon {
            width: 6vh;
            height: 6vh;
            margin-bottom: 2vh;
            flex-shrink: 0;
        }
        
        .book-type-card .book-type-label {
            font-size: 1.3vw;
            font-weight: 500;
            color: #1A1A1A;
            line-height: 1.4;
            font-family: 'Lexend', sans-serif;
        }
        
        .cta-container {
            text-align: center;
            margin-top: 6vh;
        }
        
        .cta-container .cta-button {
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
        
        .cta-container .cta-button:hover {
            background: #0052CC;
            transform: translateY(-0.3vh);
            box-shadow: 0 0.8vh 2.5vh rgba(0, 102, 255, 0.4);
        }
        
        .cta-container .cta-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 4vh;
            height: 4vh;
            background: #FFFFFF;
            border-radius: 50%;
        }
        
        .cta-container .cta-icon img {
            width: 2vh;
            height: 2vh;
        }
        
        @media (max-width: 992px) {
            .suflex-media-intro {
                padding: 6vh 6vw;
            }
            
            .suflex-media-intro .section-title {
                font-size: 6vw;
                margin-bottom: 2.5vh;
            }
            
            .suflex-media-intro .section-description {
                font-size: 3.5vw;
                max-width: 85vw;
                margin-bottom: 5vh;
            }
            
            .key-metrics-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 3vw;
                padding: 0 6vw;
                margin-bottom: 8vh;
            }
            
            .metric-card {
                padding: 3.5vh 3vw;
                min-height: 25vh;
            }
            
            .metric-card .metric-icon {
                width: 6vh;
                height: 6vh;
                margin-bottom: 2vh;
            }
            
            .metric-card .metric-value {
                font-size: 6vw;
                margin-bottom: 1.5vh;
            }
            
            .metric-card .metric-label {
                font-size: 3vw;
            }
            
            .book-types-section {
                padding: 6vh 6vw;
            }
            
            .book-types-section .section-subtitle {
                font-size: 6vw;
                margin-bottom: 5vh;
            }
            
            .book-types-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 3vw;
                max-width: 90vw;
                margin-bottom: 5vh;
            }
            
            .book-type-card {
                padding: 3vh 3vw;
                min-height: 16vh;
            }
            
            .book-type-card .book-type-icon {
                width: 5.5vh;
                height: 5.5vh;
                margin-bottom: 1.5vh;
            }
            
            .book-type-card .book-type-label {
                font-size: 3vw;
            }
            
            .cta-container {
                margin-top: 5vh;
            }
            
            .cta-container .cta-button {
                font-size: 3.5vw;
                padding: 2vh 6vw;
                border-radius: 2vw;
                gap: 1.5vw;
            }
            
            .cta-container .cta-icon {
                width: 4.5vh;
                height: 4.5vh;
            }
            
            .cta-container .cta-icon img {
                width: 2.2vh;
                height: 2.2vh;
            }
        }
        
        @media (max-width: 576px) {
            .suflex-media-intro {
                padding: 5vh 6vw;
            }
            
            .suflex-media-intro .section-title {
                font-size: 7.5vw;
                margin-bottom: 2vh;
            }
            
            .suflex-media-intro .section-description {
                font-size: 4.2vw;
                max-width: 90vw;
                margin-bottom: 4vh;
                line-height: 1.7;
            }
            
            .key-metrics-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 3vw;
                padding: 0 6vw;
                margin-bottom: 6vh;
            }
            
            .metric-card {
                padding: 3vh 3vw;
                min-height: 20vh;
            }
            
            .metric-card .metric-icon {
                width: 6vh;
                height: 6vh;
                margin-bottom: 1.5vh;
            }
            
            .metric-card .metric-value {
                font-size: 8vw;
                margin-bottom: 1vh;
            }
            
            .metric-card .metric-label {
                font-size: 3.5vw;
            }
            
            .book-types-section {
                padding: 5vh 6vw;
            }
            
            .book-types-section .section-subtitle {
                font-size: 7vw;
                margin-bottom: 4vh;
            }
            
            .book-types-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 3vw;
                max-width: 90vw;
                margin-bottom: 4vh;
            }
            
            .book-type-card {
                padding: 3vh 3vw;
                min-height: 15vh;
            }
            
            .book-type-card .book-type-icon {
                width: 5.5vh;
                height: 5.5vh;
                margin-bottom: 1.5vh;
            }
            
            .book-type-card .book-type-label {
                font-size: 3.8vw;
            }
            
            .cta-container {
                margin-top: 4vh;
            }
            
            .cta-container .cta-button {
                font-size: 4.2vw;
                padding: 0.5vh 5vw;
                border-radius: 9vw;
                gap: 2vw;
            }
            
            .cta-container .cta-icon {
                width: 3vh;
                height: 3vh;
                margin: 1vh 1vh 1vh 1vh;
            }
            
            .cta-container .cta-icon img {
                width: 2.5vh;
                height: 1.5vh;
            }
        }
    </style>
    """

def why_hire_html():
    return """
    <section class="suflex-media-intro">
        <h2 class="section-title">Why Should We Work With Suflex Media and Its Writing Team?</h2>
        <p class="section-description">Suflex Media is not just another book writing service - it is a team of passionate individuals that have and will continue to deliver excellence.</p>
    </section>
    
    <div class="key-metrics-grid">
        <div class="metric-card">
            <img src="/static/icons/Years of Experience.png" alt="Years of Experience Icon" class="metric-icon">
            <span class="metric-value">5+</span>
            <span class="metric-label">Years of<br/>Experience</span>
        </div>
        <div class="metric-card">
            <img src="/static/icons/Book Written Yearly.png" alt="Books Icon" class="metric-icon">
            <span class="metric-value">25+</span>
            <span class="metric-label">Books Written<br/>Yearly</span>
        </div>
        <div class="metric-card">
            <img src="/static/icons/Happy Clients.png" alt="Stars Icon" class="metric-icon">
            <span class="metric-value">100+</span>
            <span class="metric-label">Happy Clients</span>
        </div>
        <div class="metric-card">
            <img src="/static/icons/In House Team.png" alt="Team Icon" class="metric-icon">
            <span class="metric-value">100%</span>
            <span class="metric-label">In-House Team</span>
        </div>
    </div>

    <section class="book-types-section">
        <h3 class="section-subtitle">What Kind Of Books Do We Write?</h3>
        <div class="book-types-grid">
            <div class="book-type-card">
                <img src="/static/icons/Thought Leadership Books.png" alt="Brain Icon" class="book-type-icon">
                <span class="book-type-label">Thought Leadership<br/>Books</span>
            </div>
            <div class="book-type-card">
                <img src="/static/icons/Business & Entrepreneurship Books.png" alt="Briefcase & Book Icon" class="book-type-icon">
                <span class="book-type-label">Business &<br/>Entrepreneurship Books</span>
            </div>
            <div class="book-type-card">
                <img src="/static/icons/Personal Brand & Influence Books.png" alt="User Icon" class="book-type-icon">
                <span class="book-type-label">Personal Brand &<br/>Influence Books</span>
            </div>
            <div class="book-type-card">
                <img src="/static/icons/Biographies & Memoirs.png" alt="Book Icon" class="book-type-icon">
                <span class="book-type-label">Biographies &<br/>Memoirs</span>
            </div>
            <div class="book-type-card">
                <img src="/static/icons/Self-Help & Personal Development Books.png" alt="Heart Icon" class="book-type-icon">
                <span class="book-type-label">Self-Help & Personal<br/>Development Books</span>
            </div>
            <div class="book-type-card">
                <img src="/static/icons/Industry-Specific Books.png" alt="Industry Icon" class="book-type-icon">
                <span class="book-type-label">Industry-Specific<br/>Books</span>
            </div>
        </div>
        <div class="cta-container">
            <button class="cta-button">
                Book a free strategy call
                <div class="cta-icon">
                    <img src="/static/icons/arrow.png" alt="arrow">
                </div>
            </button>
        </div>
    </section>
    """
