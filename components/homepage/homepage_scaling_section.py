def scaling_section_html():
    return """
        <div class="scaling-section">
            <div class="scaling-intro">
                <h2 class="desktop-heading">Ready to Start <span class="scaling-blue">Scaling</span> Your Brand?</h2>
                <h2 class="mobile-heading">Ready to Start<br><span class="scaling-blue-full">Scaling Your Brand?</span></h2>
                <p>Let's build a marketing story that sparks genuine connection—only real results and success.</p>
                <p>We shatter the usual playbook to give your brand a voice that's as original as it is authentic as you.</p>
            </div>
            <div class="scaling-cards">
                <div class="scaling-card">
                    <img src="/static/3f7230630b4d46064671041289d3c6935fa51f5e.png" alt="Clear, Uncomplicated, Real" class="card-image">
                    <h3>We're Clear,<br>Uncomplicated, Real</h3>
                    <p>No smoke and mirrors here. From brainstorming to execution, our transparent approach keeps you in the loop—simple, honest, and direct.</p>
                </div>
                <div class="scaling-card">
                    <img src="/static/37372b55afc4c665a23bac17cee0ea4500213f49.png" alt="Unexpected, Impactful, Unforgettable" class="card-image">
                    <h3>Unexpected, Impactful,<br>Unforgettable</h3>
                    <p>No following the crowd here. We blend unconventional creativity with practical strategies for tangible results—innovative, impactful, and unforgettable.</p>
                </div>
            </div>
        </div>
    """

def scaling_section_css():
    return """
        <style>
            .scaling-section {
                background-color: #ffffff;
                padding: 8vh 0;
                text-align: center;
                background-size: contain;
                background-position: center;
                width: 100%;
                max-width: 100vw;
                box-sizing: border-box;
                overflow-x: hidden;
            }
            .scaling-intro h2 {
                font-size: 4.5vw;
                font-weight: bold;
                margin-bottom: 3vh;
            }
            .scaling-blue {
                color: #007bff;
            }
            .scaling-blue-full {
                color: #007bff;
            }
            .mobile-heading {
                display: none;
            }
            .desktop-heading {
                display: block;
            }
            .scaling-intro p {
                font-size: 1.3vw;
                color: #333;
                line-height: 1.6;
                margin-bottom: 6vh;
            }
            .scaling-cards {
                display: flex;
                justify-content: center;
                gap: 3vw;
            }
            .scaling-card {
                background-color: #ffffff;
                border-radius: 1.5vw;
                box-shadow: 0 0.8vw 2vw rgba(0, 0, 0, 0.1);
                padding: 4vh 3vw;
                width: 32vw;
                text-align: center;
            }
            .card-image {
                width: 32vh;
                height: 30vh;
                margin-bottom: 3vh;
                aspect-ratio: 1 / 1;
                object-fit: cover;
            }
            .scaling-card h3 {
                font-size: 2vw;
                font-weight: bold;
                color: #007bff;
                margin-bottom: 3vh;
            }
            .scaling-card p {
                font-size: 1.1vw;
                color: #333;
                line-height: 1.7;
            }
            
            /* Mobile Responsive */
            @media (max-width: 768px) {
                .scaling-section {
                    padding: 6vh 4vw;
                    border-top: 2px solid #e0e0e0;
                }
                .desktop-heading {
                    display: none;
                }
                .mobile-heading {
                    display: block;
                    font-size: 6.5vw;
                    margin-bottom: 3vh;
                    line-height: 1.3;
                }
                .scaling-intro p {
                    font-size: 3.5vw;
                    line-height: 1.5;
                    margin-bottom: 1.5vh;
                    padding: 0 2vw;
                }
                .scaling-intro p:last-of-type {
                    margin-bottom: 5vh;
                }
                .scaling-cards {
                    flex-direction: row;
                    gap: 3vw;
                    padding: 0 2vw;
                }
                .scaling-card {
                    width: 45vw;
                    padding: 2.5vh 2.5vw;
                    border-radius: 3vw;
                    border: 1px solid #e0e0e0;
                }
                .card-image {
                    width: 100%;
                    height: auto;
                    max-height: 18vh;
                    margin-bottom: 1.5vh;
                    object-fit: contain;
                }
                .scaling-card h3 {
                    font-size: 3.8vw;
                    margin-bottom: 1.5vh;
                    line-height: 1.3;
                }
                .scaling-card p {
                    font-size: 2.8vw;
                    line-height: 1.4;
                }
            }
        </style>
    """