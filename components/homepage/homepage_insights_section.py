def insights_section_html():
    return '''
<section class="insights-section">
    <div class="insights-header">
        <h1>Insights and Strategies for</h1>
        <h2>Performance Marketing Success</h2>
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
    font-size: 2.5vw;
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
</style>
'''