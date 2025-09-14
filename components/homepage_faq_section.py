def faq_section_css():
    return """
    <style>
        .faq-section {
            background-color: #333;
            padding: 5vh 6vw;
            display: flex;
            font-family: 'Lexend', sans-serif;
            color: white;
        }
        .faq-title-container {
            width: 40vw;
        }
        .faq-title {
            font-size: 3vw;
            font-weight: 600;
            position: relative;
            top: 30%;
            text-align: center;
        }
        .faq-accordion {
            width: 35vw;
        }
        .faq-item {
            background-color: white;
            border-radius: 1vw;
            padding: 2vh 2vw;
            margin-bottom: 2vh;
            cursor: pointer;
        }
        .faq-question {
            display: flex;
            align-items: center;
            font-weight: bold;
            color: #4B0082; /* Dark Purple */
            font-size: 1.5vw;
        }
        .faq-question .icon {
            font-size: 2vw;
            margin-right: 1vw;
            font-weight: 300;
        }
        .faq-answer {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease-in-out, padding-top 0.4s ease-in-out;
            color: #6a5acd; /* Lighter Purple */
            font-size: 1.2vw;
            padding-left: 3vw;
            padding-top: 0;
        }
        .faq-item.active .faq-answer {
            max-height: 100vh; /* A large enough value */
            padding-top: 1vh;
        }
    </style>
    """

def faq_section_html():
    return """
    <div class="faq-section">
        <div class="faq-title-container">
            <h2 class="faq-title">Frequently Asked<br>Questions</h2>
        </div>
        <div class="faq-accordion">
            <div class="faq-item">
                <div class="faq-question">
                    <span class="icon">+</span>
                    <span>How do i sign up for the project?</span>
                </div>
                <div class="faq-answer">
                    <p>Follow our newsletter. We will regularly update our latest project and availability.</p>
                </div>
            </div>
            <div class="faq-item">
                <div class="faq-question">
                    <span class="icon">+</span>
                    <span>What thing that i should prepare before starting?</span>
                </div>
                <div class="faq-answer">
                    <p>To get started, it's helpful to have a clear idea of your project goals, target audience, and any existing brand assets. Don't worry if you don't have everything, we can help you with that!</p>
                </div>
            </div>
            <div class="faq-item">
                <div class="faq-question">
                    <span class="icon">+</span>
                    <span>Does my company need help for marketing advices?</span>
                </div>
                <div class="faq-answer">
                    <p>Every company can benefit from expert marketing advice. We can provide a fresh perspective, identify growth opportunities, and help you create a strategy that delivers real results.</p>
                </div>
            </div>
        </div>
    </div>
    <script>
        document.querySelectorAll('.faq-item').forEach(item => {
            item.addEventListener('click', () => {
                const currentlyActive = document.querySelector('.faq-item.active');
                if (currentlyActive && currentlyActive !== item) {
                    currentlyActive.classList.remove('active');
                    currentlyActive.querySelector('.icon').textContent = '+';
                }

                item.classList.toggle('active');
                const icon = item.querySelector('.icon');
                if (item.classList.contains('active')) {
                    icon.textContent = '-';
                } else {
                    icon.textContent = '+';
                }
            });
        });
    </script>
    """