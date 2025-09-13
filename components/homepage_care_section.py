def care_section_html():
    return '''
<section class="care-section">
    <div class="care-heading">
        <h1>Things We Can Take Care Of,</h1>
        <h2>So You Don't Have To</h2>
    </div>
    <div class="care-grid">
        <div class="care-card">
            <div class="card-left">
                <img src="/static/icons/PerformanceMarketing.png" alt="Performance Marketing Icon">
                <p>Performance<br>Marketing</p>
            </div>
            <img src="/static/icons/Blue-Arrow.png" alt="Arrow" class="card-arrow">
        </div>
        <div class="care-card">
            <div class="card-left">
                <img src="/static/icons/LinkedinBranding.png" alt="LinkedIn Branding Icon">
                <p>LinkedIn<br>Branding</p>
            </div>
            <img src="/static/icons/Blue-Arrow.png" alt="Arrow" class="card-arrow">
        </div>
        <div class="care-card">
            <div class="card-left">
                <img src="/static/icons/GraphicDesign.png" alt="Graphic Design Icon">
                <p>Graphic<br>Design</p>
            </div>
            <img src="/static/icons/Blue-Arrow.png" alt="Arrow" class="card-arrow">
        </div>
        <div class="care-card">
            <div class="card-left">
                <img src="/static/icons/BookWriting.png" alt="Book Writing Icon">
                <p>Book<br>Writing</p>
            </div>
            <img src="/static/icons/Blue-Arrow.png" alt="Arrow" class="card-arrow">
        </div>
        <div class="care-card">
            <div class="card-left">
                <img src="/static/icons/WebDevelopment.png" alt="Web Development Icon">
                <p>Web<br>Development</p>
            </div>
            <img src="/static/icons/Blue-Arrow.png" alt="Arrow" class="card-arrow">
        </div>
        <div class="care-card">
            <div class="card-left">
                <img src="/static/icons/ContentWriting.png" alt="Content Writing Icon">
                <p>Content<br>Writing</p>
            </div>
            <img src="/static/icons/Blue-Arrow.png" alt="Arrow" class="card-arrow">
        </div>
    </div>
    <button class="care-cta-button">Book a free strategy call</button>
</section>
'''

def care_section_css():
    return '''
<style>
    .care-section {
        background-color: #fff;
        padding: 10vh 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'Lexend', sans-serif;
    }
    .care-heading {
        text-align: center;
        margin-bottom: 8vh;
    }
    .care-heading h1 {
        font-size: 3vw;
        font-weight: bold;
        color: #000;
        margin: 0;
    }
    .care-heading h2 {
        font-size: 2.5vw;
        font-weight: bold;
        color: #007bff;
        margin-top: 1vh;
    }
    .care-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2.5vw;
        width: 70vw;
        margin: 0 auto;
    }
    .care-card {
        background-color: #fff;
        border-radius: 1vw;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.3);
        padding: 2vw;
        padding-right: 1vw;
        padding-bottom: 2vw;
        display: flex;
        justify-content: space-between;
        align-items: center;
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
        font-weight: 600;
    }
    .card-arrow {
        width: 3vw;
        position: relative;
        top: 7vh;
    }
    .care-cta-button {
        margin-top: 8vh;
        padding: 2vh 3vw;
        font-size: 1.2vw;
        font-weight: bold;
        color: #fff;
        background-color: #007bff;
        border: none;
        border-radius: 0.5vw;
        cursor: pointer;
    }
</style>
'''