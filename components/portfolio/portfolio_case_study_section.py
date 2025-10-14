def portfolio_case_study_section_html():
    return '''
<section class="case-study-section">
    <div class="case-study-container">
        <div class="case-study-card">
            <div class="case-study-image">
                <img src="/static/Frame1.jpg" alt="Case Study">
            </div>
            <div class="case-study-content">
                <div class="case-study-badge">Personal Branding</div>
                <h3 class="case-study-title">How we helped a Data Science consultancy 3x their Lead Pipeline</h3>
                <p class="case-study-description">
                    At Suflex Media, we chart insights, you can strategize, too. 
                    We are a team of experts who carefully analyze your company's 
                    online behavior and audience insights. Whether your business owner 
                    or a marketer, our articles will help you convert more visitors 
                    into paying customers, as we explore effective tactics and best 
                    practices to keep you ahead in the ever-evolving world of performance 
                    marketing.
                </p>
                <p class="case-study-description">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                    Nullam id dolor malesuada odio dictum Fusce vel rutrum quil. 
                    Etiam sed ipsum cursus et dictum finibus ut at purus est. Duis 
                    commodo ex vel ut molestie nerum eget porttitor nec ullamcorper. 
                    Fusce nec fingiila malis. Aliquam quis lectus et eros dapibus 
                    modu: tempus in ut. Mauris euismod malesuada dapibus. Nunc 
                    blandit arcu vel augue tincidunt, sed non porta pretium.
                </p>
                <a href="#" class="read-more-link">Read More</a>
            </div>
        </div>
        
        <div class="case-study-card dark">
            <div class="case-study-image">
                <img src="/static/Frame2.jpg" alt="Case Study">
            </div>
            <div class="case-study-content">
                <div class="case-study-badge">Ghost Writing</div>
                <h3 class="case-study-title">How we helped a Data Science consultancy 3x their Lead Pipeline</h3>
                <p class="case-study-description">
                    At Suflex Media, we chart insights, you can strategize, too. 
                    We are a team of experts who carefully analyze your company's 
                    online behavior and audience insights. Whether your business owner 
                    or a marketer, our articles will help you convert more visitors 
                    into paying customers, as we explore effective tactics and best 
                    practices to keep you ahead in the ever-evolving world of performance 
                    marketing.
                </p>
                <p class="case-study-description">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                    Nullam id dolor malesuada odio dictum Fusce vel rutrum quil. 
                    Etiam sed ipsum cursus et dictum finibus ut at purus est. Duis 
                    commodo ex vel ut molestie nerum eget porttitor nec ullamcorper. 
                    Fusce nec fingiila malis. Aliquam quis lectus et eros dapibus 
                    modu: tempus in ut. Mauris euismod malesuada dapibus. Nunc 
                    blandit arcu vel augue tincidunt, sed non porta pretium.
                </p>
                <a href="#" class="read-more-link">Read More</a>
            </div>
        </div>
        
        <div class="case-study-card">
            <div class="case-study-image">
                <img src="/static/Frame3.jpg" alt="Case Study">
            </div>
            <div class="case-study-content">
                <div class="case-study-badge">Performance Marketing</div>
                <h3 class="case-study-title">How we helped a Data Science consultancy 3x their Lead Pipeline</h3>
                <p class="case-study-description">
                    At Suflex Media, we chart insights, you can strategize, too. 
                    We are a team of experts who carefully analyze your company's 
                    online behavior and audience insights. Whether your business owner 
                    or a marketer, our articles will help you convert more visitors 
                    into paying customers, as we explore effective tactics and best 
                    practices to keep you ahead in the ever-evolving world of performance 
                    marketing.
                </p>
                <p class="case-study-description">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                    Nullam id dolor malesuada odio dictum Fusce vel rutrum quil. 
                    Etiam sed ipsum cursus et dictum finibus ut at purus est. Duis 
                    commodo ex vel ut molestie nerum eget porttitor nec ullamcorper. 
                    Fusce nec fingiila malis. Aliquam quis lectus et eros dapibus 
                    modu: tempus in ut. Mauris euismod malesuada dapibus. Nunc 
                    blandit arcu vel augue tincidunt, sed non porta pretium.
                </p>
                <a href="#" class="read-more-link">Read More</a>
            </div>
        </div>
        
        <div class="case-study-card dark">
            <div class="case-study-image">
                <img src="/static/Frame4.jpg" alt="Case Study">
            </div>
            <div class="case-study-content">
                <div class="case-study-badge">Website Development</div>
                <h3 class="case-study-title">How we helped a Data Science consultancy 3x their Lead Pipeline</h3>
                <p class="case-study-description">
                    At Suflex Media, we chart insights, you can strategize, too. 
                    We are a team of experts who carefully analyze your company's 
                    online behavior and audience insights. Whether your business owner 
                    or a marketer, our articles will help you convert more visitors 
                    into paying customers, as we explore effective tactics and best 
                    practices to keep you ahead in the ever-evolving world of performance 
                    marketing.
                </p>
                <p class="case-study-description">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                    Nullam id dolor malesuada odio dictum Fusce vel rutrum quil. 
                    Etiam sed ipsum cursus et dictum finibus ut at purus est. Duis 
                    commodo ex vel ut molestie nerum eget porttitor nec ullamcorper. 
                    Fusce nec fingiila malis. Aliquam quis lectus et eros dapibus 
                    modu: tempus in ut. Mauris euismod malesuada dapibus. Nunc 
                    blandit arcu vel augue tincidunt, sed non porta pretium.
                </p>
                <a href="#" class="read-more-link">Read More</a>
            </div>
        </div>
    </div>
    
    <div class="pagination">
        <button class="pagination-btn active">1</button>
        <button class="pagination-btn">2</button>
        <button class="pagination-btn">3</button>
        <button class="pagination-btn">4</button>
        <span class="pagination-dots">...</span>
        <button class="pagination-btn">7</button>
        <button class="pagination-btn next-btn">Next page →</button>
    </div>
</section>
'''

def portfolio_case_study_section_css():
    return '''
<style>
    .case-study-section {
        background-color: transparent;
        font-family: 'Lexend', sans-serif;
    }
    
    .case-study-container {
        max-width: 100%;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
    }
    
    .case-study-card {
        display: flex;
        gap: 3vw;
        align-items: stretch;
        background-color: transparent;
        overflow: hidden;
        width: 100%;
        padding: 6vh 10vh;
    }
    
    .case-study-card.dark {
        background-color: #1a1a1a;
    }
    
    .case-study-card.dark .case-study-title {
        color: #fff;
    }
    
    .case-study-card.dark .case-study-description {
        color: #ccc;
    }
    
    .case-study-card.dark .read-more-link {
        color: #007bff;
    }
    
    .case-study-image {
        flex: 0 0 30vw;
        width: 30vw;
        min-height: 45vh;
        overflow: hidden;
    }
    
    .case-study-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 1vh;
    }
    
    .case-study-content {
        flex: 1;
        padding: 3vh 3vw;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    
    .case-study-badge {
        display: inline-block;
        background-color: #007bff;
        color: #fff;
        padding: 0.8vh 1.5vw;
        border-radius: 2vw;
        font-size: 0.9vw;
        font-weight: 500;
        margin-bottom: 2vh;
        width: fit-content;
    }
    
    .case-study-title {
        font-size: 1.8vw;
        font-weight: 600;
        color: #000;
        margin: 0 0 2vh 0;
        line-height: 1.3;
    }
    
    .case-study-description {
        font-size: 0.95vw;
        color: #666;
        line-height: 1.7;
        margin: 0 0 1.5vh 0;
        font-weight: 400;
    }
    
    .read-more-link {
        color: #007bff;
        font-size: 1vw;
        font-weight: 500;
        text-decoration: none;
        margin-top: auto;
        padding-top: 1vh;
    }
    
    .read-more-link:hover {
        text-decoration: underline;
    }
    
    .pagination {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1vw;
        margin-top: 6vh;
    }
    
    .pagination-btn {
        min-width: 3vw;
        height: 3vw;
        border: 0.15vw solid #ddd;
        background-color: #fff;
        color: #333;
        border-radius: 0.5vw;
        font-size: 1vw;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Lexend', sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0 1vw;
    }
    
    .pagination-btn:hover,
    .pagination-btn.active {
        background-color: #007bff;
        color: #fff;
        border-color: #007bff;
    }
    
    .next-btn {
        background-color: #007bff;
        color: #fff;
        border-color: #007bff;
        padding: 1vh 2vw;
        min-width: auto;
        height: auto;
    }
    
    .pagination-dots {
        color: #666;
        font-size: 1.2vw;
        padding: 0 0.5vw;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .case-study-section {
            padding: 6vh 5vw;
        }
        
        .case-study-container {
            max-width: 90vw;
            gap: 3vh;
        }
        
        .case-study-card {
            flex-direction: column;
            gap: 0;
            border-radius: 3vw;
        }
        
        .case-study-image {
            flex: none;
            width: 100%;
            min-height: 30vh;
        }
        
        .case-study-content {
            padding: 3vh 5vw;
        }
        
        .case-study-badge {
            font-size: 3vw;
            padding: 1vh 4vw;
            border-radius: 4vw;
            margin-bottom: 1.5vh;
        }
        
        .case-study-title {
            font-size: 5vw;
            margin-bottom: 1.5vh;
        }
        
        .case-study-description {
            font-size: 3.5vw;
            line-height: 1.6;
            margin-bottom: 1.5vh;
        }
        
        .read-more-link {
            font-size: 3.5vw;
        }
        
        .pagination {
            flex-wrap: wrap;
            gap: 2vw;
            margin-top: 4vh;
        }
        
        .pagination-btn {
            min-width: 10vw;
            height: 10vw;
            font-size: 3.5vw;
            border-radius: 2vw;
            border-width: 0.3vw;
        }
        
        .next-btn {
            padding: 2vh 6vw;
            min-width: auto;
            height: auto;
        }
        
        .pagination-dots {
            font-size: 4vw;
        }
    }
</style>
'''
