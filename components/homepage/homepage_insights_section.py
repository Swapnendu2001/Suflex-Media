def insights_section_html():
    return '''
<section class="insights-section">
    <div class="insights-header">
        <h1 class="desktop-header">Insights and Strategies for</h1>
        <h2 class="desktop-header">Performance Marketing Success</h2>
        <h1 class="mobile-header">Insights and Strategies<br>for Performance<br>Marketing Success</h1>
        <p>At Suflex Media, we share insights, tips, and strategies to maximize your performance marketing efforts. Whether you're a business owner or a marketer, our articles will help you achieve measurable results and</p>
    </div>
    <div class="insights-main">
        <div class="insights-cards">
            <div class="insight-card">
                <div class="card-top">
                    <span class="color-marker green"></span>
                    <span class="read-time">5 mins read</span>
                </div>
                <h3>How a Digital Marketing Agency Can Boost Your Business</h3>
                <p>We are the top digital marketing agency for branding corp. We offer a full rang engine ...</p>
                <img src="/static/icons/arrow.png" alt="Read more" class="card-arrow-icon">
            </div>
            <div class="insight-card">
                <div class="card-top">
                    <span class="color-marker pink"></span>
                    <span class="read-time">5 mins read</span>
                </div>
                <h3>The Latest Trends and Strategies with a Digital Marketing Agency</h3>
                <p>Working with this digital marketing agency has been a true partnership. They have tak...</p>
                <img src="/static/icons/arrow.png" alt="Read more" class="card-arrow-icon">
            </div>
            <div class="insight-card">
                <div class="card-top">
                    <span class="color-marker orange"></span>
                    <span class="read-time">5 mins read</span>
                </div>
                <h3>Maximizing ROI with the Expertise of a Digital Marketing Agency</h3>
                <p>What sets this digital marketing agency apart is their commitment to transparency an</p>
                <img src="/static/icons/arrow.png" alt="Read more" class="card-arrow-icon">
            </div>
        </div>
        <button class="insights-cta">View all blogs</button>
    </div>
</section>
'''

def insights_section_css():
    return '''
<style>
.insights-section {
    font-family: 'Lexend', sans-serif;
    text-align: center;
    padding-top: 10vh;
}

.insights-header {
    background-color: #fff;
    padding: 0 5vw 15vh 5vw;
}

.insights-header h1 {
    font-size: 4.5vw;
    font-weight: bold;
    color: #000;
    margin: 0;
}

.insights-header h2 {
    font-size: 3vw;
    font-weight: bold;
    color: #007bff;
    margin-top: 1vh;
}

.mobile-header {
    display: none;
}

.desktop-header {
    display: block;
}

.insights-header p {
    font-size: 1.2vw;
    color: #333;
    width: 50vw;
    margin: 5vh auto 0 auto;
    line-height: 1.6;
}

.insights-main {
    background-color: #007bff;
    background-image: url('/static/icons/Doodles-2.png');
    background-size: cover;
    padding: 15vh 5vw 10vh 5vw;
    position: relative;
    border-top-left-radius: 50% 10%;
    border-top-right-radius: 50% 10%;
    margin-top: -10vh;
}

.insights-cards {
    display: flex;
    justify-content: center;
    gap: 3vw;
    position: relative;
    z-index: 2;
}

.insight-card {
    background-color: #fff;
    border-radius: 2vw;
    box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.1);
    padding: 2.5vw;
    width: 22vw;
    text-align: left;
    position: relative;
}

.card-top {
    display: flex;
    align-items: center;
    margin-bottom: 2vh;
}

.color-marker {
    width: 1.2vw;
    height: 1.2vw;
    border-radius: 50%;
    margin-right: 0.8vw;
}

.color-marker.green { background-color: #9ef01a; }
.color-marker.pink { background-color: #f000b8; }
.color-marker.orange { background-color: #fca311; }

.read-time {
    font-size: 0.9vw;
    color: #888;
}

.insight-card h3 {
    font-size: 1.5vw;
    font-weight: bold;
    color: #000;
    margin: 0 0 2vh 0;
    line-height: 1.3;
}

.insight-card p {
    font-size: 1vw;
    color: #555;
    line-height: 1.5;
    margin-bottom: 4vh;
}

.card-arrow-icon {
    width: 3vw;
    position: absolute;
    bottom: 2.5vh;
    right: 2.5vw;
}

.insights-cta {
    margin-top: 8vh;
    padding: 1.5vh 2.5vw;
    font-size: 1.1vw;
    font-weight: 600;
    color: #333;
    background-color: #fff;
    border: 1px solid #007bff;
    border-radius: 0.5vw;
    cursor: pointer;
}

/* Mobile Responsive */
@media (max-width: 768px) {
    .insights-section {
        padding-top: 8vh;
    }
    
    .insights-header {
        padding: 0 6vw 10vh 6vw;
    }
    
    .desktop-header {
        display: none;
    }
    
    .mobile-header {
        display: block;
        font-size: 6vw;
        font-weight: bold;
        color: #000;
        margin: 0;
        line-height: 1.3;
    }
    
    .insights-header p {
        font-size: 3.8vw;
        width: 90vw;
        margin: 4vh auto 0 auto;
        line-height: 1.6;
    }
    
    .insights-main {
        padding: 10vh 5vw 8vh 5vw;
        border-top-left-radius: 0;
        border-top-right-radius: 0;
        margin-top: 0;
        background-color: #007bff;
        background-image: url('/static/Doodles file.png');
        background-size: cover;
    }
    
    .insights-cards {
        flex-direction: column;
        gap: 4vh;
        margin-left: 2.5vw;
    }
    
    .insight-card {
        width: 85vw;
        padding: 6vw;
        border-radius: 5vw;
    }
    
    .card-top {
        margin-bottom: 2vh;
    }
    
    .color-marker {
        width: 4vw;
        height: 4vw;
        margin-right: 2vw;
    }
    
    .read-time {
        font-size: 3.5vw;
    }
    
    .insight-card h3 {
        font-size: 4.5vw;
        margin: 0 0 2vh 0;
        line-height: 1.4;
    }
    
    .insight-card p {
        font-size: 3.5vw;
        line-height: 1.6;
        margin-bottom: 5vh;
    }
    
    .card-arrow-icon {
        width: 8vw;
        bottom: 4vw;
        right: 6vw;
    }
    
    .insights-cta {
        margin-top: 6vh;
        padding: 2vh 6vw;
        font-size: 3.8vw;
        border-radius: 2vw;
    }
}
</style>
'''