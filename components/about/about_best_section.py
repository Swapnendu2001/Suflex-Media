def best_section_html():
    return """
    <section class="best-section">
        <div class="best-section-title">
            <h2>Why are we the best?</h2>
            <p>Take a look for yourself!</p>
        </div>
        <div class="feature-cluster">
            <img src="/static/about_us_why_we_are_best.svg" alt="Why We Are Best" class="feature-cluster-img desktop-only">
            <img src="/static/about_us_why_we_are_best_mobile.svg" alt="Why We Are Best" class="feature-cluster-img mobile-only">
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
            width: 72vw;
            height: 80vh;
            margin: 0 auto;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
        }

        .feature-cluster-img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }

        .mobile-only {
            display: none;
        }

        .desktop-only {
            display: block;
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
        /* Tablet Design (768px - 1024px) */
        @media (max-width: 1024px) and (min-width: 768px) {
            .best-section {
                padding: 7vh 4vw;
                min-height: 75vh;
            }
            
            .best-section-title h2 {
                font-size: 5.5vw;
                margin-bottom: 1.5vh;
            }
            
            .best-section-title p {
                font-size: 3.5vw;
                margin-bottom: 5vh;
            }
            
            .feature-cluster {
                width: 85vw;
                height: 70vh;
            }
            
            .desktop-only {
                display: block;
            }
            
            .mobile-only {
                display: none;
            }
        }

        /* Mobile Design (Under 768px) */
        @media (max-width: 767px) {
            .best-section {
                padding: 5vh 4vw;
                min-height: auto;
            }
            
            .best-section::before {
                opacity: 0.2;
            }
            
            .best-section-title h2 {
                font-size: 8vw;
                margin-bottom: 1vh;
                font-weight: 700;
            }
            
            .best-section-title p {
                font-size: 5vw;
                margin-bottom: 4vh;
                font-weight: 400;
            }
            
            .feature-cluster {
                width: 100%;
                height: auto;
                min-height: 60vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .mobile-only {
                display: block;
                width: 100%;
                max-width: 100%;
            }

            .desktop-only {
                display: none;
            }
            
            .feature-cluster-img {
                width: 100%;
                height: auto;
            }
            .best-section-title {
                margin-bottom: -20vh;
            }
        }
        
        /* Small Mobile Devices (Under 480px) */
        @media (max-width: 480px) {
            .best-section {
                padding: 4vh 3vw;
            }
            
            .best-section-title h2 {
                font-size: 8vw;
            }
            
            .best-section-title p {
                font-size: 5.5vw;
            }
            
            .feature-cluster {
                min-height: 50vh;
            }
        }
    </style>
    """
