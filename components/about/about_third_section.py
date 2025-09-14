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