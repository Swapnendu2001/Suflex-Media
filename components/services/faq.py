def faq_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;700&display=swap');
        
        .services-faq-section {
            background-color: #4A4A4A;
            padding: 8vh 5vw;
            display: flex;
            gap: 5vw;
            font-family: 'Lexend', sans-serif;
            color: white;
        }
        
        .services-faq-title-container {
            width: 40vw;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .services-faq-title {
            font-size: 3.5vw;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 2vh;
            font-family: 'Lexend', sans-serif;
        }
        
        .services-faq-subtitle {
            font-size: 1.2vw;
            font-weight: 400;
            color: #E0E0E0;
            font-family: 'Lexend', sans-serif;
        }
        
        .services-faq-accordion {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 2vh;
        }
        
        .services-faq-item {
            background-color: white;
            border-radius: 1.5vh;
            padding: 2.5vh 2vw;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .services-faq-item:hover {
            transform: translateY(-0.3vh);
            box-shadow: 0 0.5vh 2vh rgba(0, 0, 0, 0.2);
        }
        
        .services-faq-question {
            display: flex;
            align-items: center;
            font-weight: 600;
            color: #1A1A1A;
            font-size: 1.3vw;
            font-family: 'Lexend', sans-serif;
        }
        
        .services-faq-question .icon {
            font-size: 2vw;
            margin-right: 1.5vw;
            font-weight: 400;
            color: #1A1A1A;
            transition: transform 0.3s ease;
            flex-shrink: 0;
        }
        
        .services-faq-item.active .services-faq-question .icon {
            transform: rotate(45deg);
        }
        
        .services-faq-answer {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease-in-out, padding-top 0.4s ease-in-out;
            color: #666;
            font-size: 1.1vw;
            padding-left: 3.5vw;
            padding-top: 0;
            font-family: 'Lexend', sans-serif;
            line-height: 1.6;
        }
        
        .services-faq-item.active .services-faq-answer {
            max-height: 50vh;
            padding-top: 2vh;
        }
        
        @media (max-width: 992px) {
            .services-faq-section {
                flex-direction: column;
                gap: 5vh;
                padding: 6vh 6vw;
            }
            
            .services-faq-title-container {
                width: 100%;
                text-align: center;
            }
            
            .services-faq-title {
                font-size: 6vw;
                margin-bottom: 2vh;
            }
            
            .services-faq-subtitle {
                font-size: 3vw;
            }
            
            .services-faq-accordion {
                gap: 2.5vh;
            }
            
            .services-faq-item {
                padding: 2.5vh 3vw;
                border-radius: 2vh;
            }
            
            .services-faq-question {
                font-size: 3.5vw;
            }
            
            .services-faq-question .icon {
                font-size: 4vw;
                margin-right: 2vw;
            }
            
            .services-faq-answer {
                font-size: 3vw;
                padding-left: 6vw;
                line-height: 1.7;
            }
            
            .services-faq-item.active .services-faq-answer {
                max-height: 60vh;
                padding-top: 2vh;
            }
        }
        
        @media (max-width: 576px) {
            .services-faq-section {
                padding: 5vh 6vw;
                gap: 4vh;
            }
            
            .services-faq-title {
                font-size: 7.5vw;
                line-height: 1.3;
            }
            
            .services-faq-subtitle {
                font-size: 3.8vw;
            }
            
            .services-faq-accordion {
                gap: 2vh;
            }
            
            .services-faq-item {
                padding: 2.5vh 4vw;
                border-radius: 2vh;
            }
            
            .services-faq-question {
                font-size: 4.2vw;
                line-height: 1.4;
            }
            
            .services-faq-question .icon {
                font-size: 5vw;
                margin-right: 3vw;
            }
            
            .services-faq-answer {
                font-size: 3.8vw;
                padding-left: 8vw;
                line-height: 1.7;
            }
            
            .services-faq-item.active .services-faq-answer {
                max-height: 70vh;
                padding-top: 2vh;
            }
        }
    </style>
    """

def faq_html():
    return """
    <section class="services-faq-section">
        <div class="services-faq-title-container">
            <h2 class="services-faq-title">Most-Asked Questions About Our Our Ghostwriting Services</h2>
            <p class="services-faq-subtitle">Collected from 100+ Leaders During Our Discovery Calls</p>
        </div>
        <div class="services-faq-accordion">
            <div class="services-faq-item">
                <div class="services-faq-question">
                    <span class="icon">+</span>
                    <span>What If I Don't Like Your Content?</span>
                </div>
                <div class="services-faq-answer">
                    <p>We offer unlimited revisions to ensure the content meets your expectations. Your satisfaction is our priority, and we'll work closely with you until the manuscript perfectly captures your vision and voice.</p>
                </div>
            </div>
            <div class="services-faq-item">
                <div class="services-faq-question">
                    <span class="icon">+</span>
                    <span>How long will your ghostwriters take to write a book?</span>
                </div>
                <div class="services-faq-answer">
                    <p>Typically, a full-length book takes 4-6 months to complete, depending on the complexity and length. This includes research, writing, and multiple rounds of revisions to ensure quality and accuracy.</p>
                </div>
            </div>
            <div class="services-faq-item">
                <div class="services-faq-question">
                    <span class="icon">+</span>
                    <span>Do you help me with publishing after the book is written?</span>
                </div>
                <div class="services-faq-answer">
                    <p>Yes! We can guide you through the publishing process, whether you choose traditional publishing or self-publishing. We have partnerships with publishers and can help with formatting, cover design, and distribution strategies.</p>
                </div>
            </div>
            <div class="services-faq-item">
                <div class="services-faq-question">
                    <span class="icon">+</span>
                    <span>How involved will I be with the book writing process?</span>
                </div>
                <div class="services-faq-answer">
                    <p>You decide your level of involvement. Some clients prefer regular check-ins and chapter reviews, while others provide initial input and review the final manuscript. We adapt our process to match your availability and preferences.</p>
                </div>
            </div>
            <div class="services-faq-item">
                <div class="services-faq-question">
                    <span class="icon">+</span>
                    <span>Can I speak with the book writer directly?</span>
                </div>
                <div class="services-faq-answer">
                    <p>Absolutely! We encourage direct communication between you and your assigned ghostwriter. This ensures your voice, ideas, and expertise are accurately captured throughout the writing process.</p>
                </div>
            </div>
            <div class="services-faq-item">
                <div class="services-faq-question">
                    <span class="icon">+</span>
                    <span>Will I own the copyrights to the book?</span>
                </div>
                <div class="services-faq-answer">
                    <p>Yes, you will own 100% of the copyrights to your book. All intellectual property rights are transferred to you upon completion and final payment. You have complete ownership and control.</p>
                </div>
            </div>
            <div class="services-faq-item">
                <div class="services-faq-question">
                    <span class="icon">+</span>
                    <span>Do ghostwriters sign non-disclosure agreements (NDAs)?</span>
                </div>
                <div class="services-faq-answer">
                    <p>Yes, confidentiality is paramount. All our ghostwriters sign comprehensive NDAs before starting any project. Your ideas, information, and the entire collaboration remain completely confidential.</p>
                </div>
            </div>
            <div class="services-faq-item">
                <div class="services-faq-question">
                    <span class="icon">+</span>
                    <span>Do I need to give credit to the book writers?</span>
                </div>
                <div class="services-faq-answer">
                    <p>No, you don't need to credit the ghostwriter. The book is published under your name alone. Our writers work behind the scenes to help you achieve your publishing goals while you receive full authorship credit.</p>
                </div>
            </div>
        </div>
    </section>
    <script>
        document.querySelectorAll('.services-faq-item').forEach(item => {
            item.addEventListener('click', () => {
                const currentlyActive = document.querySelector('.services-faq-item.active');
                if (currentlyActive && currentlyActive !== item) {
                    currentlyActive.classList.remove('active');
                }
                item.classList.toggle('active');
            });
        });
    </script>
    """
