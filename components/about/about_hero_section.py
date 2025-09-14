def about_hero_section_style():
    return """
    <style>
        .about-hero-section {
            padding: 5vh 5vw;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5vh;
        }
        .about-hero-intro {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
        }
        .about-hero-text {
            max-width: 38vw;
            position: relative;
            top: -4vh;
        }
        .about-hero-text h1 {
            font-size: 3.5vw;
            font-weight: 500;
            color: #000;
            margin: 0;
        }
        .about-hero-text h2 {
            font-size: 4vw;
            font-weight: 500;
            color: #007bff;
            margin: 0;
            line-height: 1.2;
        }
        .about-hero-text p {
            font-size: 1.7vw;
            color: #333;
            margin-top: 2vh;
        }
        .about-hero-image {
            max-width: 45vw;
        }
        .about-hero-image img {
            width: 100%;
        }
        .mission-section {
            text-align: center;
            max-width: 65vw;
            position: relative;
        }
        .mission-section h3 {
            font-size: 4vw;
            font-weight: 600;
            color: #007bff;
            margin-bottom: 1vh;
        }
        .mission-section p {
            font-size: 1.7vw;
            color: #333;
        }
        .mission-section .star-left {
            position: absolute;
            left: 9vw;
            top: -2vh;
            width: 5vw;
        }
        .mission-section .star-right {
            position: absolute;
            right: 2vw;
            bottom: -8vh;
            width: 2.5vw;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 5vw;
            justify-items: center;
            align-items: center;
            position: relative;
            margin-top: 5vh;
        }
        .stat-item {
            text-align: center;
        }
        .stat-item .label {
            font-size: 1.7vw;
            color: #000;
            font-weight: 500;
        }
        .stat-item .value {
            font-size: 2.5vw;
            font-weight: 600;
            color: #007bff;
            max-width: 55vh;
        }
        .stats-grid .stat-item-bottom {
            grid-column: 1 / -1;
            margin-top: 2vh;
        }
        .stats-grid .pencil-icon {
            position: absolute;
            left: -14vw;
            top: 0;
            width: 7vw;
        }
        .stats-grid .clover-icon {
            position: absolute;
            left: -1vw;
            bottom: 0vh;
            width: 4.5vw;
        }
        .stats-grid .spring-icon {
            position: absolute;
            right: -11vw;
            top: 8vw;
            width: 6vw;
        }
    </style>
    """

def about_hero_section_content():
    return """
    <div class="about-hero-section">
        <div class="about-hero-intro">
            <div class="about-hero-text">
                <h1>Suflex Media is a</h1>
                <h2>Results-Driven Digital<br>Marketing Agency</h2>
                <p>We've helped founders, operators, and teams look sharp, sound smarter, and scale faster.</p>
                <p>Fueled by passion and of course - coffee!  <img src="/static/icons/coffee.png" alt="coffee cup" style="width:1.6vw; margin-top:2vh;"></p>
                
            </div>
            <div class="about-hero-image">
                <img src="/static/About-page-hero-section.gif" alt="Digital Marketing Agency">
            </div>
        </div>
        <div class="mission-section">
            <img src="/static/icons/star.png" alt="star" class="star-left">
            <h3>Mission</h3>
            <p>Our mission at Suflex is to inspire results, innovate solutions, and garner customer success while forging strong bonds with every business we touch.</p>
            <img src="/static/icons/star.png" alt="star" class="star-right">
        </div>
        <div class="stats-grid">
            <img src="/static/icons/pencil.png" alt="pencil" class="pencil-icon">
            <div class="stat-item">
                <p class="label">Served more than</p>
                <p class="value">300+ Clients</p>
            </div>
            <div class="stat-item">
                <p class="label">Helping Clients</p>
                <p class="value">Achieve 4X ROIs</p>
            </div>
            <div class="stat-item stat-item-bottom">
                <p class="label">In House Team of</p>
                <p class="value">10+ Talented Individuals</p>
            </div>
            <img src="/static/icons/clover.png" alt="clover" class="clover-icon">
            <img src="/static/icons/spring.png" alt="spring" class="spring-icon">
        </div>
    </div>
    """