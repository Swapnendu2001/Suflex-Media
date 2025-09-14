def best_section_html():
    return """
    <section class="best-section">
        <div class="best-section-title">
            <h2>Why are we the best?</h2>
            <p>Take a look for yourself!</p>
        </div>
        <div class="feature-cluster">
            <div id="creative-solution" class="feature-item item-blue">
                <img src="/static/icons/solution.png" alt="Creative Solution">
                <span>Creative<br>Solution</span>
            </div>
            <div id="transparency" class="feature-item item-white">
                <img src="/static/icons/transparency.png" alt="Transparency">
                <span>Transparency</span>
            </div>
            <div id="client-satisfaction" class="feature-item item-blue">
                <img src="/static/icons/satisfaction.png" alt="Client Satisfaction">
                <span>100% Client<br>Satisfaction</span>
            </div>
            <div id="affordability" class="feature-item item-white">
                <img src="/static/icons/affordability.png" alt="Affordability">
                <span>Affordability</span>
            </div>
            <div id="fast-responds" class="feature-item item-blue">
                <img src="/static/icons/response.png" alt="Fast Responds">
                <span>Fast<br>Responds</span>
            </div>
            <div id="witty-content" class="feature-item item-white">
                <img src="/static/icons/witty-content.png" alt="Witty Content">
                <span>Witty Content</span>
            </div>
            <div id="attention-to-details" class="feature-item item-blue">
                <img src="/static/icons/attention-to-detail.png" alt="Attention to Details">
                <span>Attention to<br>Details</span>
            </div>
            <div id="aesthetic-design" class="feature-item item-white">
                <img src="/static/icons/aesthetic-design.png" alt="Aesthetic Design">
                <span>Aesthetic<br>Design</span>
            </div>
            <div id="fast-delivery" class="feature-item item-blue">
                <img src="/static/icons/on-time.png" alt="Fast Delivery">
                <span>Fast Delivery</span>
            </div>
            <div id="timeless-quality" class="feature-item item-white">
                <img src="/static/icons/timeless-quality.png" alt="Timeless Quality">
                <span>Timeless<br>Quality</span>
            </div>
        </div>
    </section>
    """

def best_section_css():
    return """
    <style>
        .best-section {
            background-color: #000;
            padding: 8vh 5vw;
            text-align: center;
            font-family: 'Lexend', sans-serif;
            color: white;
            position: relative;
            overflow: hidden;
            min-height: 80vh;
        }

        .best-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url('/static/icons/Doodles.png');
            background-size: cover;
            background-position: center;
            opacity: 0.3;
            z-index: 0;
        }

        .best-section > * {
            position: relative;
            z-index: 1;
        }

        .best-section-title h2 {
            font-size: 4vw;
            font-weight: 700;
            margin-bottom: 1vh;
            line-height: 1.2;
        }

        .best-section-title p {
            font-size: 2.8vw;
            font-weight: 400;
            margin-bottom: 6vh;
            opacity: 0.9;
        }

        .feature-cluster {
            position: relative;
            width: 85vw;
            height: 50vh;
            margin: 0 auto;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
        }

        .feature-item {
            position: absolute;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 2vw;
            text-align: center;
            box-sizing: border-box;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
        }

        .feature-item:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 1vh 2vh rgba(0, 0, 0, 0.3);
            z-index: 10;
        }

        .feature-item img {
            width: 3vw;
            height: 3vw;
            margin-bottom: 1vh;
            object-fit: contain;
        }

        .feature-item span {
            font-size: 1vw;
            font-weight: 600;
            display: block;
            line-height: 1.3;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Colors */
        .item-blue {
            background-color: #0d6efd;
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.1);
        }

        .item-white {
            background-color: white;
            color: #0d6efd;
            border: 2px solid rgba(13, 110, 253, 0.1);
            box-shadow: 0 0.5vh 1vh rgba(255, 255, 255, 0.1);
        }
        
        .item-white img {
            filter: invert(37%) sepia(97%) saturate(2397%) hue-rotate(211deg) brightness(101%) contrast(101%);
        }

        /* Positioning and Shapes - Top Row */
        #creative-solution {
            width: 14vw; 
            height: 14vw;
            clip-path: polygon(0 0, 100% 0, 100% 75%, 50% 100%, 0 75%);
            top: 3vh; 
            left: 8vw;
            transform: rotate(-8deg);
        }

        #transparency {
            width: 12vw; 
            height: 12vw;
            clip-path: circle(50% at 50% 50%);
            top: 1vh; 
            left: 24vw;
            transform: rotate(3deg);
        }

        #client-satisfaction {
            width: 15vw; 
            height: 15vw;
            clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
            top: 0vh; 
            left: 38vw;
            transform: rotate(-3deg);
        }

        #affordability {
            width: 13vw; 
            height: 13vw;
            border-radius: 25%;
            top: 2vh; 
            left: 55vw;
            transform: rotate(5deg);
        }

        #fast-responds {
            width: 14vw; 
            height: 14vw;
            clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
            top: 4vh; 
            left: 70vw;
            transform: rotate(-6deg);
        }

        /* Bottom Row */
        #witty-content {
            width: 13vw; 
            height: 13vw;
            clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
            top: 26vh; 
            left: 12vw;
            transform: rotate(7deg);
        }

        #attention-to-details {
            width: 14vw; 
            height: 14vw;
            border-radius: 25%;
            top: 24vh; 
            left: 27vw;
            transform: rotate(-4deg);
        }
        
        #aesthetic-design {
            width: 13vw; 
            height: 13vw;
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            top: 27vh; 
            left: 43vw;
            transform: rotate(4deg);
        }

        #fast-delivery {
            width: 12vw; 
            height: 12vw;
            clip-path: circle(50% at 50% 50%);
            top: 25vh; 
            left: 58vw;
            transform: rotate(-2deg);
        }

        #timeless-quality {
            width: 14vw; 
            height: 14vw;
            clip-path: polygon(0 25%, 50% 0, 100% 25%, 100% 100%, 0 100%);
            top: 28vh; 
            left: 72vw;
            transform: rotate(6deg);
        }

        /* Responsive Design */
        @media (max-width: 1200px) {
            .best-section-title h2 {
                font-size: 5vw;
            }
            
            .best-section-title p {
                font-size: 2.2vw;
            }
            
            .feature-item {
                padding: 1.5vw;
            }
            
            .feature-item img {
                width: 4vw;
                height: 4vw;
            }
            
            .feature-item span {
                font-size: 1.3vw;
            }
        }

        @media (max-width: 768px) {
            .best-section {
                padding: 6vh 3vw;
                min-height: 70vh;
            }
            
            .best-section-title h2 {
                font-size: 7vw;
            }
            
            .best-section-title p {
                font-size: 3vw;
                margin-bottom: 4vh;
            }
            
            .feature-cluster {
                width: 95vw;
                height: 60vh;
            }
            
            .feature-item {
                padding: 3vw;
            }
            
            .feature-item img {
                width: 6vw;
                height: 6vw;
                margin-bottom: 2vh;
            }
            
            .feature-item span {
                font-size: 2vw;
            }
            
            /* Adjust positioning for mobile */
            #creative-solution, #transparency, #client-satisfaction, 
            #affordability, #fast-responds {
                width: 18vw;
                height: 18vw;
            }
            
            #witty-content, #attention-to-details, #aesthetic-design, 
            #fast-delivery, #timeless-quality {
                width: 18vw;
                height: 18vw;
            }
        }
    </style>
    """