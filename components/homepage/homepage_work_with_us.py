def work_with_us_html():
    return """
        <section class="work-with-us">
            <div class="work-with-us-title">
                <h2>Why Should You</h2>
                <h3>Work With Us?</h3>
            </div>
            <div class="work-with-us-content">
                <div class="card-row-top">
                    <div class="card">
                        <img src="static/Frame1.jpg" alt="Breakthrough Idea">
                        <h4>Got a Breakthrough Idea or Product?</h4>
                        <p>We'll match it with the audience that's craving something new—no empty promises.</p>
                        <p>We believe in smarter strategies and marketing that connect on a human level. When you work with us, you're getting a partner who's as invested in your success as you are.</p>
                    </div>
                    <div class="card">
                        <img src="static/Frame2.jpg" alt="Tired of Agencies Going Dark?">
                        <h4>Tired of Agencies Going Dark?</h4>
                        <p>We stick around until your brand thrives—no radio silence or silent treatments here.</p>
                        <p>From real-time reporting dashboards to on-call support, we keep you looped in every step of the way. Transparency is our middle name.</p>
                    </div>
                    <div class="card">
                        <img src="static/Frame3.jpg" alt="Marketing Missteps">
                        <h4>Done with Marketing Missteps?</h4>
                        <p>We turn setbacks into comebacks—no cookie-cutter solutions and guesswork.</p>
                        <p>Using advanced data analytics and proven tactics, we turn businesses around—focusing on outcomes that move the needle and impact your bottom line.</p>
                    </div>
                </div>
                <div class="card-row-bottom">
                    <div class="card">
                        <img src="static/Frame4.jpg" alt="Time-Tested & Data-Driven">
                        <h4>Time-Tested & Data-Driven</h4>
                        <p>We harness insights to fine-tune every campaign—no trial and error, just results.</p>
                        <p>With real-time reporting and open communication, you'll always know exactly where your campaigns stand—and where they're headed next.</p>
                    </div>
                    <div class="card">
                        <img src="static/Frame5.jpg" alt="Capped Number of Projects">
                        <h4>Capped Number of Projects</h4>
                        <p>We never bite off more than we can chew — for your benefit and ours.</p>
                        <p>We cap our project load to give you undivided attention—no rush jobs, no compromise.</p>
                    </div>
                </div>
            </div>
        </section>
    """

def work_with_us_css():
    return """
        <style>
            .work-with-us {
                width: 100vw;
                padding-top: 5vh;
                padding-bottom: 5vh;
            }
            .work-with-us-title {
                text-align: center;
                background-color: white;
                padding-bottom: 5vh;
            }
            .work-with-us-title h2 {
                font-size: 4.5vw;
                font-weight: bold;
                color: #000000;
                margin: 0;
            }
            .work-with-us-title h3 {
                font-size: 3vw;
                font-weight: bold;
                color: #007bff;
                margin: 0;
            }
            .work-with-us-content {
                background-color: #007bff;
                background-image: url('static/icons/Doodles.png');
                background-size: cover;
                padding: 5vh 5vw;
                display: flex;
                flex-direction: column;
                gap: 2vh;
                align-items: center;
            }
            .card-row-top {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 2vw;
                width: 100%;
            }
            .card-row-bottom {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 2vw;
                width: 66%;
            }
            .card {
                background-color: white;
                border-radius: 2vw;
                padding: 2vw;
                box-shadow: 0 0.5vw 1vw rgba(0, 0, 0, 0.1);
                display: flex;
                flex-direction: column;
            }
            .work-with-us-content .card img {
                width: 100%;
                border-radius: 1vw;
                margin-bottom: 1.5vh;
                aspect-ratio: 2 / 1;
                object-fit: cover;
            }
            .work-with-us-content .card h4 {
                font-size: 1.5vw;
                font-weight: bold;
                color: #000000;
                margin: 0 0 1vh 0;
            }
            .work-with-us-content .card p {
                font-size: 1vw;
                color: #333;
                margin: 0.5vh 0;
            }
            
            /* Mobile Responsive */
            @media (max-width: 768px) {
                .work-with-us {
                    padding-top: 5vh;
                    padding-bottom: 5vh;
                }
                .work-with-us-title {
                    padding-bottom: 4vh;
                }
                .work-with-us-title h2 {
                    font-size: 6vw;
                }
                .work-with-us-title h3 {
                    font-size: 7vw;
                }
                .work-with-us-content {
                    padding: 5vh 6vw;
                    background-image: url('/static/handdrawn_doodle.png');
                    background-size: auto;
                    background-repeat: repeat;
                }
                .card-row-top {
                    grid-template-columns: 1fr;
                    gap: 4vh;
                }
                .card-row-bottom {
                    grid-template-columns: 1fr;
                    gap: 4vh;
                    width: 100%;
                }
                .card {
                    padding: 5vw;
                    border-radius: 5vw;
                    aspect-ratio: auto;
                }
                .work-with-us-content .card img {
                    border-radius: 3vw;
                    margin-bottom: 2vh;
                }
                .work-with-us-content .card h4 {
                    font-size: 5vw;
                    margin: 0 0 2vh 0;
                }
                .work-with-us-content .card p {
                    font-size: 3.5vw;
                    margin: 1vh 0;
                    line-height: 1.6;
                }
            }
        </style>
    """