def portfolio_hero_section_html():
    return '''
<section class="portfolio-hero-section">
    <div class="portfolio-hero-heading">
        <h1>Suflex Media's Performance Marketing</h1>
        <h2>Case Studies</h2>
    </div>
    <div class="portfolio-hero-grid">
        <div class="portfolio-hero-card">
            <div class="card-left">
                <img src="/static/icons/All_case_studies.png" alt="All Case Studies Icon">
                <p>All<br>Case Studies</p>
            </div>
            <img src="/static/icons/Blue-Arrow.png" alt="Arrow" class="card-arrow">
        </div>
        <div class="portfolio-hero-card">
            <div class="card-left">
                <img src="/static/icons/Personal_Branding.png" alt="Personal Branding Icon">
                <p>Personal<br>Branding</p>
            </div>
            <img src="/static/icons/Blue-Arrow.png" alt="Arrow" class="card-arrow">
        </div>
        <div class="portfolio-hero-card">
            <div class="card-left">
                <img src="/static/icons/Ghost_Writing.png" alt="Ghost Writing Icon">
                <p>Ghost<br>Writing</p>
            </div>
            <img src="/static/icons/Blue-Arrow.png" alt="Arrow" class="card-arrow">
        </div>
        <div class="portfolio-hero-card">
            <div class="card-left">
                <img src="/static/icons/Performance_Marketing.png" alt="Performance Marketing Icon">
                <p>Performance<br>Marketing</p>
            </div>
            <img src="/static/icons/Blue-Arrow.png" alt="Arrow" class="card-arrow">
        </div>
        <div class="portfolio-hero-card">
            <div class="card-left">
                <img src="/static/icons/Website_Development.png" alt="Website Development Icon">
                <p>Website<br>Development</p>
            </div>
            <img src="/static/icons/Blue-Arrow.png" alt="Arrow" class="card-arrow">
        </div>
    </div>
</section>
'''

def portfolio_hero_section_css():
    return '''
<style>
    .portfolio-hero-section {
        background-color: #fff;
        padding: 10vh 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'Lexend', sans-serif;
        width: 100%;
        box-sizing: border-box;
        overflow-x: hidden;
    }
    .portfolio-hero-heading {
        text-align: center;
        margin-bottom: 8vh;
    }
    .portfolio-hero-heading h1 {
        font-size: 3vw;
        font-weight: bold;
        color: #000;
        margin: 0;
        font-weight: 400;
    }
    .portfolio-hero-heading h2 {
        font-size: 2.5vw;
        font-weight: bold;
        color: #007bff;
        margin-top: 1vh;
        font-weight: 400;
    }
    .portfolio-hero-grid {
        display: flex;
        justify-content: center;
        gap: 2vw;
        width: 90vw;
        margin: 0 auto;
    }
    .portfolio-hero-card {
        background-color: #fff;
        border-radius: 1vw;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.3);
        padding: 1vw;
        padding-right: 0.5vw;
        padding-bottom: 0.5vw;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex: 1;
        min-width: 15vw;
        max-width: 17vw;
        transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
        cursor: pointer;
    }
    .portfolio-hero-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.4);
        background-color: #007bff;
    }
    .portfolio-hero-card:hover .card-left p {
        color: #fff;
    }
    .portfolio-hero-card:hover .card-left img,
    .portfolio-hero-card:hover .card-arrow {
        filter: brightness(0) invert(1);
    }
    .card-left {
        display: flex;
        flex-direction: column;
        gap: 2vh;
    }
    .card-left img {
        width: 3.5vw;
    }
    .card-left p {
        margin: 0;
        font-size: 1.4vw;
        color: #333;
        font-weight: 400;
    }
    .card-arrow {
        width: 2.5vw;
        position: relative;
        top: 5.5vh;
        filter: brightness(0);
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .portfolio-hero-section {
            padding: 8vh 5vw;
        }
        .portfolio-hero-heading {
            margin-bottom: 6vh;
        }
        .portfolio-hero-heading h1 {
            font-size: 6vw;
        }
        .portfolio-hero-heading h2 {
            font-size: 6.5vw;
            margin-top: 1vh;
        }
        .portfolio-hero-grid {
            flex-wrap: wrap;
            gap: 3vw;
            width: 90vw;
        }
        .portfolio-hero-card {
            padding: 4vw;
            border-radius: 3vw;
            flex: 0 0 42vw;
            min-width: 42vw;
            max-width: 42vw;
        }
        .card-left {
            gap: 1.5vh;
        }
        .card-left img {
            width: 12vw;
        }
        .card-left p {
            font-size: 4vw;
        }
        .card-arrow {
            width: 7vw;
            top: auto;
            bottom: 4vw;
            right: 4vw;
        }
    }
</style>
'''
