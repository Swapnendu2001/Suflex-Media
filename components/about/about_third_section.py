def about_third_section_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap');
        .about-third-section {
            font-family: 'Lexend', sans-serif;
            position: relative;
            top: 5vh;
        }
        .about-third-section-top {
            background-color: #000;
            text-align: center;
            padding: 5vh 2vw;
            height: 27vh;
            width: 80vw;
            position: relative;
            left: 20vh;
        }
        .about-third-section-top h1 {
            color: #fff;
            font-size: 3.5vw;
            font-weight: 700;
            margin: 0;
            line-height: 1.2;
        }
        .about-third-section-top h2 {
            color: #FFC94A;
            font-size: 2.3vw;
            font-weight: 400;
            margin: 0;
        }
        .about-third-section-middle {
            background-color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2vh 5vw;
            gap: 5vw;
        }
        .about-third-section-middle-left {
            width: 35vw;
            position: relative;
            color: #333;
        }
        .about-third-section-middle-left::before {
            content: '“';
            position: absolute;
            top: -8vh;
            left: -4vw;
            font-size: 8vw;
            color: #E0E0E0;
            z-index: 1;
        }
        .about-third-section-middle-left::after {
            content: '”';
            position: absolute;
            bottom: -16vh;
            left: 35vw;
            font-size: 8vw;
            color: #E0E0E0;
            z-index: 1;
        }
        .about-third-section-middle-left p {
            font-size: 1.2vw;
            line-height: 1.6;
            position: relative;
            z-index: 2;
            text-align: justify;
        }
        .about-third-section-middle-right {
            width: 30vw;
        }
        .about-third-section-middle-right img {
            width: 100%;
            height: auto;
        }
        .about-third-section-bottom {
            background-color: #212121;
            text-align: center;
            padding: 8vh 0;
        }
        .about-third-section-bottom h3 {
            color: #fff;
            font-size: 2.5vw;
            font-weight: 500;
            margin-bottom: 4vh;
        }
        .about-third-section-cta {
            background-color: #007BFF;
            color: #fff;
            font-size: 1.2vw;
            padding: 1.5vh 3vw;
            border-radius: 50px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 1vw;
            border: none;
            cursor: pointer;
        }
        .about-third-section-cta span {
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #0056b3;
            border-radius: 50%;
            width: 2.5vw;
            height: 2.5vw;
        }
        .about-third-section-cta img {
            width: 1.5vw;
            height: 1.5vw;
        }

        /* Tablet Responsive Design (768px - 1024px) */
        @media (max-width: 1024px) and (min-width: 768px) {
            .about-third-section {
                top: 3vh;
            }
            
            .about-third-section-top {
                width: 90vw;
                left: 5vw;
                padding: 4vh 3vw;
                height: auto;
                min-height: 20vh;
            }
            
            .about-third-section-top h1 {
                font-size: 5vw;
            }
            
            .about-third-section-top h2 {
                font-size: 3.5vw;
            }
            
            .about-third-section-middle {
                padding: 4vh 5vw;
                gap: 4vw;
            }
            
            .about-third-section-middle-left {
                width: 45vw;
            }
            
            .about-third-section-middle-left::before {
                top: -6vh;
                left: -3vw;
                font-size: 10vw;
            }
            
            .about-third-section-middle-left::after {
                bottom: -12vh;
                left: 42vw;
                font-size: 10vw;
            }
            
            .about-third-section-middle-left p {
                font-size: 2vw;
            }
            
            .about-third-section-middle-right {
                width: 40vw;
            }
            
            .about-third-section-bottom {
                padding: 6vh 0;
            }
            
            .about-third-section-bottom h3 {
                font-size: 3.5vw;
                margin-bottom: 3vh;
            }
            
            .about-third-section-cta {
                font-size: 2vw;
                padding: 2vh 4vw;
                gap: 2vw;
            }
            
            .about-third-section-cta span {
                width: 4vw;
                height: 4vw;
            }
            
            .about-third-section-cta img {
                width: 2.5vw;
                height: 2.5vw;
            }
        }

        /* Mobile Responsive Design (Under 768px) */
        @media (max-width: 767px) {
            .about-third-section {
                top: 2vh;
            }
            
            .about-third-section-top {
                width: 90vw;
                left: 5vw;
                padding: 4vh 5vw;
                height: auto;
                min-height: auto;
            }
            
            .about-third-section-top h1 {
                font-size: 7vw;
                line-height: 1.3;
            }
            
            .about-third-section-top h2 {
                font-size: 5vw;
                margin-top: 1vh;
            }
            
            .about-third-section-middle {
                flex-direction: column;
                padding: 4vh 5vw;
                gap: 4vh;
            }
            
            .about-third-section-middle-left {
                width: 100%;
                padding: 0 2vw;
            }
            
            .about-third-section-middle-left::before {
                top: -4vh;
                left: -2vw;
                font-size: 15vw;
            }
            
            .about-third-section-middle-left::after {
                bottom: -8vh;
                left: auto;
                right: -2vw;
                font-size: 15vw;
            }
            
            .about-third-section-middle-left p {
                font-size: 4vw;
                line-height: 1.7;
                text-align: center;
            }
            
            .about-third-section-middle-right {
                width: 80vw;
                margin: 0 auto;
            }
            
            .about-third-section-bottom {
                padding: 5vh 5vw;
            }
            
            .about-third-section-bottom h3 {
                font-size: 6vw;
                margin-bottom: 3vh;
                line-height: 1.3;
            }
            
            .about-third-section-cta {
                font-size: 4vw;
                padding: 2vh 6vw;
                gap: 3vw;
                border-radius: 40px;
            }
            
            .about-third-section-cta span {
                width: 8vw;
                height: 8vw;
            }
            
            .about-third-section-cta img {
                width: 4vw;
                height: 4vw;
            }
        }

        /* Small Mobile Devices (Under 480px) */
        @media (max-width: 480px) {
            .about-third-section-top {
                left: 0;
                width: 92vw;
                padding: 3vh 5vw;
                margin-left: 4vw;
            }
            
            .about-third-section-top h1 {
                font-size: 8vw;
            }
            
            .about-third-section-top h2 {
                font-size: 6vw;
            }
            
            .about-third-section-middle {
                padding: 3vh 4vw;
            }
            
            .about-third-section-middle-left p {
                font-size: 4.5vw;
            }
            
            .about-third-section-middle-right {
                width: 90vw;
            }
            
            .about-third-section-bottom h3 {
                font-size: 7vw;
            }
            
            .about-third-section-cta {
                font-size: 4.5vw;
                padding: 2vh 7vw;
            }
        }
    </style>
    """

def about_third_section_html():
    return """
    <section class="about-third-section">
        <div class="about-third-section-top">
            <h1>At Suflex Media We</h1>
            <h2>produce creative solutions</h2>
        </div>
        <div class="about-third-section-middle">
            <div class="about-third-section-middle-left">
                <p>There are many creative agencies out there, but only a few really care!</p>
                <p>We are Suflex Media are the 1%, who look at your business like ours as we pour our passion into everything we do to dish out the quality and perfection that our clients deserve!</p>
            </div>
            <div class="about-third-section-middle-right">
                <img src="/static/active-solutions.png" alt="Creative Solution Illustration">
            </div>
        </div>
        <div class="about-third-section-bottom">
            <h3>Looking to join our Team?</h3>
            <a href="#" class="about-third-section-cta">
                See Openings
                
                <img src="/static/icons/arrow-button.png" alt="Arrow Icon">
                
            </a>
        </div>
    </section>
    """