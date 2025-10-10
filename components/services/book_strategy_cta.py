def book_strategy_cta_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;700&display=swap');
        
        .book-strategy-cta-section {
            background: #017AFF;
            background-image: url('/static/doodles-hero-section-services.png');
            background-size: cover;
            background-repeat: no-repeat;
            padding: 8vh 5vw;
            text-align: center;
            position: relative;
            overflow: hidden;
            font-family: 'Lexend', sans-serif;
        }
        
        .book-strategy-cta-section::before {
            content: '';
            position: absolute;
            top: -10vh;
            left: -10vw;
            width: 30vw;
            height: 30vw;
            transform: rotate(-15deg);
        }
        
        .book-strategy-cta-section::after {
            content: '';
            position: absolute;
            bottom: -10vh;
            right: -10vw;
            width: 30vw;
            height: 30vw;
            background: url('/static/icons/pen.svg') no-repeat center;
            background-size: contain;
            opacity: 0.1;
            transform: rotate(15deg);
        }
        
        .book-strategy-cta-content {
            position: relative;
            z-index: 1;
            max-width: 70vw;
            margin: 0 auto;
        }
        
        .book-strategy-cta-title {
            font-size: 4vw;
            font-weight: 700;
            color: white;
            margin-bottom: 4vh;
            line-height: 1.2;
            font-family: 'Lexend', sans-serif;
        }
        
        .book-strategy-cta-button {
            background: white;
            color: #0066FF;
            border: none;
            padding: 2vh 4vw;
            font-size: 1.4vw;
            border-radius: 5vw;
            cursor: pointer;
            display: inline-block;
            transition: all 0.3s ease;
            font-weight: 600;
            font-family: 'Lexend', sans-serif;
            text-decoration: none;
            box-shadow: 0 0.5vh 2vh rgba(0, 0, 0, 0.2);
        }
        
        .book-strategy-cta-button:hover {
            transform: translateY(-0.5vh);
            box-shadow: 0 1vh 3vh rgba(0, 0, 0, 0.3);
            background: #f0f0f0;
        }
        
        @media (max-width: 992px) {
            .book-strategy-cta-title {
                font-size: 5.5vw;
            }
            
            .book-strategy-cta-button {
                font-size: 2.5vw;
                padding: 2.5vh 6vw;
            }
            
            .book-strategy-cta-content {
                max-width: 85vw;
            }
        }
        
        @media (max-width: 576px) {
            .book-strategy-cta-title {
                font-size: 7vw;
            }
            
            .book-strategy-cta-button {
                font-size: 3.5vw;
                padding: 2.5vh 8vw;
            }
            
            .book-strategy-cta-content {
                max-width: 90vw;
            }
        }
    </style>
    """

def book_strategy_cta_html():
    return """
    <section class="book-strategy-cta-section">
        <div class="book-strategy-cta-content">
            <h2 class="book-strategy-cta-title">Start Your Book Writing Process Today!</h2>
            <a href="#contact" class="book-strategy-cta-button">Book a free strategy call</a>
        </div>
    </section>
    """
