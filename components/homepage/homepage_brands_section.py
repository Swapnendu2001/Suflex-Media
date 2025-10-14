def brands_section_html():
    return """
    <div class="brands-section">
        <div class="brands-heading">
            <h1 class="desktop-heading">Big Brands. Smart Founders. One</h1>
            <h1 class="desktop-heading">Thing in Common: <span class="blue-text">Suflex.</span></h1>
            <h1 class="mobile-heading">Real Brands<br><span class="blue-text">Real Stories</span></h1>
        </div>
        <div class="brands-content">
            <div class="brands-left">
                <div class="image-container">
                     <img src="/static/Man-with-bulb.png" alt="Man with bulb" class="brands-image">
                </div>
                <img src="/static/icons/Play.png" alt="Play button" class="play-button">
            </div>
            <div class="brands-right">
                <h2>How we helped a Data Science consultancy 3x their Lead Pipeline</h2>
                <ul>
                    <li>At Suflex Media, we share insights, tips, and strategies to maximize your performance marketing efforts. Whether you're a business owner or a marketer, our</li>
                    <li>At Suflex Media, we share insights, tips, and strategies to maximize your performance marketing efforts. Whether you're a business owner or a marketer, our</li>
                    <li>At Suflex Media, we share insights, tips, and strategies to maximize your performance marketing efforts. Whether you're a business owner or a marketer, our</li>
                </ul>
                <div class="brands-buttons">
                    <button class="read-more-btn">Read more</button>
                    <button class="view-all-btn">View All Case Stuides</button>
                </div>
            </div>
        </div>
    </div>
    """

def brands_section_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap');

    .brands-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #fff;
        padding: 8vh 8vw;
        font-family: 'Lexend', sans-serif;
        width: 100%;
        max-width: 100vw;
        box-sizing: border-box;
        overflow-x: hidden;
    }

    .brands-heading {
        text-align: center;
        margin-bottom: 6vh;
    }

    .brands-heading h1 {
        font-size: 4.2vw;
        font-weight: 700;
        color: #000;
        margin: 0;
        line-height: 1.2;
    }

    .brands-heading .blue-text {
        color: #007bff;
    }

    .mobile-heading {
        display: none;
    }

    .desktop-heading {
        display: block;
    }

    .brands-content {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 4vw;
        width: 100%;
    }

    .brands-left {
        position: relative;
        width: 45vw;
        height: 35vw;
    }

    .brands-left .image-container {
        width: 100%;
        height: 100%;
        background-color: #0d6efd; /* A shade of blue */
        border-radius: 2.5vw;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        background-image: url('/static/icons/Doodles.png');
        background-size: 50%;
        background-repeat: no-repeat;
        background-position: 10% 20%;
    }

    .brands-left .brands-image {
        width: 100%;
        height: auto;
        object-fit: contain;
    }

    .brands-left .play-button {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 10vw;
        height: 10vw;
        cursor: pointer;
        filter: brightness(0) invert(1);
    }

    .brands-right {
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 40vw;
    }

    .brands-right h2 {
        font-size: 2vw;
        font-weight: 700;
        margin-bottom: 3vh;
        line-height: 1.3;
    }

    .brands-right ul {
        list-style-position: outside;
        padding-left: 1.5vw;
        margin-bottom: 4vh;
    }

    .brands-right li {
        font-size: 1vw;
        color: #333;
        margin-bottom: 2vh;
        padding-left: 0.5vw;
    }

    .brands-buttons {
        display: flex;
        gap: 1.5vw;
    }

    .brands-buttons button {
        padding: 1.8vh 2.8vw;
        border-radius: 0.8vw;
        border: 0.15vw solid #000;
        cursor: pointer;
        font-size: 1vw;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .brands-buttons .read-more-btn {
        background-color: #007bff;
        color: #fff;
        border-color: #007bff;
    }

    .brands-buttons .view-all-btn {
        background-color: #fff;
        color: #000;
    }
    
    .brands-buttons .read-more-btn:hover {
        background-color: #0056b3;
        border-color: #0056b3;
    }

    .brands-buttons .view-all-btn:hover {
        background-color: #f0f0f0;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .brands-section {
            padding: 6vh 6vw;
        }
        
        .brands-heading {
            margin-bottom: 5vh;
        }
        
        .desktop-heading {
            display: none;
        }
        
        .mobile-heading {
            display: block;
            font-size: 6.5vw;
            line-height: 1.3;
            font-weight: 700;
            color: #000;
            margin: 0;
        }
        
        .brands-content {
            flex-direction: column;
            gap: 5vh;
        }
        
        .brands-left {
            width: 90vw;
            height: 60vw;
        }
        
        .brands-left .image-container {
            border-radius: 6vw;
        }
        
        .brands-left .play-button {
            width: 20vw;
            height: 20vw;
        }
        
        .brands-right {
            width: 90vw;
        }
        
        .brands-right h2 {
            font-size: 5vw;
            margin-bottom: 3vh;
            line-height: 1.4;
        }
        
        .brands-right ul {
            padding-left: 5vw;
            margin-bottom: 4vh;
        }
        
        .brands-right li {
            font-size: 3.5vw;
            margin-bottom: 2vh;
            padding-left: 1vw;
            line-height: 1.6;
        }
        
        .brands-buttons {
            flex-direction: row;
            gap: 3vw;
        }
        
        .brands-buttons button {
            padding: 2.5vh 5vw;
            border-radius: 2vw;
            font-size: 3.5vw;
            flex: 1;
        }
    }

    </style>
    """