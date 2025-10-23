from fastapi import APIRouter, Path, Request, HTTPException
from fastapi.responses import HTMLResponse
from typing import Union
from uuid import UUID
import json
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("POSTGRES_CONNECTION_URL")

router = APIRouter()


async def getHeader():
    return """
    <style>
      /* Reset and Base Styles */
      .header * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      /* Header Main Styles */
      .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 2.25vw 4.75vw;
        background-color: #fff;
        font-family: 'Lexend', sans-serif;
        height: 15vh;
        gap: 0.625vw;
        top: 0;
        left: 0;
        right: 0;
        width: 100%;
        box-sizing: border-box;
        z-index: 1000;
        margin: 0;
        position: relative;
        box-shadow: 0 0.68vw 4.83vw 0 #017AFF;
      }

      .header .logo img {
        height: 7vh;
      }

      /* Navigation Links */
      .header .nav-links {
        display: flex;
        gap: 1.25vw;
      }

      .header .nav-links a {
        text-decoration: none;
        color: #000;
        font-size: 1.25vw;
      }

      /* Contact Us Button */
      .header .contact-us {
        display: flex;
        align-items: center;
        gap: 0.5vw;
        text-decoration: none;
        color: #000;
        font-size: 1.25vw;
      }

      .header .contact-us .icon {
        width: 1.56vw;
        height: 2.5vh;
        flex: none;
        order: 0;
        flex-grow: 0;
      }

      .header .nav-links .contact-us {
        display: none;
      }

      /* Hamburger Menu */
      .header .hamburger {
        display: none;
        flex-direction: column;
        gap: 5px;
        cursor: pointer;
        z-index: 1001;
      }

      .header .hamburger span {
        width: 25px;
        height: 3px;
        background-color: #000;
        transition: all 0.3s ease;
      }

      .header .hamburger.active span:nth-child(1) {
        transform: rotate(45deg) translate(5px, 4px);
      }

      .header .hamburger.active span:nth-child(2) {
        opacity: 0;
      }

      .header .hamburger.active span:nth-child(3) {
        transform: rotate(-45deg) translate(7px, -7px);
      }

      /* Tablet Styles */
      @media (max-width: 1024px) {
        .header .nav-links {
          gap: 1vw;
        }

        .header .nav-links a {
          font-size: 1.5vw;
        }

        .header .contact-us {
          font-size: 1.5vw;
        }
      }

      /* Mobile Styles */
      @media (max-width: 768px) {
        .header {
          padding: 4vw 4vw !important;
          height: 12vh !important;
          justify-content: center !important;
          position: relative !important;
          overflow: visible !important;
          margin: 0 !important;
          width: 100% !important;
          max-width: 100vw !important;
          box-sizing: border-box !important;
        }

        .header .logo {
          position: absolute !important;
          left: 50% !important;
          transform: translateX(-50%) !important;
        }

        .header .logo img {
          height: 6vh !important;
        }

        .header .nav-links {
          position: fixed !important;
          top: 12vh !important;
          left: -100% !important;
          width: 100vw !important;
          height: calc(100vh - 12vh) !important;
          background-color: #fff !important;
          flex-direction: column !important;
          align-items: center !important;
          justify-content: flex-start !important;
          padding-top: 5vh !important;
          gap: 4vh !important;
          transition: left 0.3s ease !important;
          z-index: 999 !important;
          overflow-y: auto !important;
        }

        .header .nav-links.active {
          left: 0 !important;
        }

        .header .nav-links a {
          font-size: 5vw !important;
          padding: 2vh 0 !important;
          width: 80% !important;
          text-align: center !important;
        }

        .header .nav-links .contact-us {
          display: flex !important;
          font-size: 5vw !important;
          gap: 3vw !important;
          justify-content: center !important;
          align-items: center !important;
        }

        .header .nav-links .contact-us .icon {
          width: 6vw !important;
          height: 3vh !important;
        }

        .header .hamburger {
          display: flex !important;
          position: absolute !important;
          right: 4vw !important;
          top: 50% !important;
          transform: translateY(-50%) !important;
          z-index: 1001 !important;
        }

        .header > .contact-us {
          display: none !important;
        }
      }

      /* Small Mobile Styles */
      @media (max-width: 480px) {
        .header {
          padding: 3vw 4vw !important;
          height: 10vh !important;
          box-shadow: none;
          margin: 0 !important;
          width: 100% !important;
          max-width: 100vw !important;
        }
      }
    </style>

    <header class="header">
      <div class="logo">
        <img src="/images/logo_header.png" alt="Suflex Media Logo">
      </div>
      <nav class="nav-links">
        <a href="/">Home</a>
        <a href="/about">About Us</a>
        <a href="/services">Services</a>
        <a href="/portfolio">Portfolio</a>
        <a href="/blogs">Blog</a>
        <!-- <a href="/careers">Careers</a> -->
        <a href="/contact" class="contact-us">
          <img src="/icons/phone-icon.png" alt="Phone icon" class="icon">
          <span>Contact Us</span>
        </a>
      </nav>
      <a href="/contact" class="contact-us">
        <img src="/icons/phone-icon.png" alt="Phone icon" class="icon">
        <span>Contact Us</span>
      </a>
      <div class="hamburger">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </header>

    <script>
      (function() {
        // Wait for the header to be inserted into DOM
        setTimeout(function() {
          const hamburger = document.querySelector('.header .hamburger');
          const navLinks = document.querySelector('.header .nav-links');

          if (hamburger && navLinks) {
            hamburger.addEventListener('click', function() {
              hamburger.classList.toggle('active');
              navLinks.classList.toggle('active');
            });

            const links = navLinks.querySelectorAll('a');
            links.forEach(link => {
              link.addEventListener('click', function() {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
              });
            });
          }
        }, 0);
      })();
    </script>
  """


async def getFooter():
    return """
    <style>
      /* Footer Reset and Base Styles */
      .footer * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      /* Footer Main Container */
      .footer {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 25vh 5vh 5vw 5vw;
        background: linear-gradient(180deg, rgba(217, 217, 217, 0) 0%, rgba(1, 122, 255, 0.25) 100%);
        font-family: 'Lexend', sans-serif;
        gap: 5vh;
        position: static;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        max-width: 100vw;
        box-sizing: border-box;
        overflow-x: hidden;
      }

      /* Footer Content Grid */
      .footer .footer-content {
        display: flex;
        justify-content: space-around;
        width: 100vw;
        align-items: flex-start;
        padding: 0 5vw;
        margin-right: 3vw;
      }

      /* Footer Section Styles */
      .footer .footer-section {
        display: flex;
        flex-direction: column;
        gap: 1.5vh;
      }

      .footer .footer-section h3 {
        font-size: 1.5vw;
        margin-bottom: 1vh;
      }

      .footer .footer-section a,
      .footer .footer-section p {
        text-decoration: none;
        color: #000;
        font-size: 1.1vw;
      }

      /* CTA Section */
      .footer .footer-section.cta {
        border-right: 3px solid #000;
        padding-right: 2vw;
      }

      .footer .footer-section.cta h2 {
        font-size: 2vw;
        color: #017AFF;
      }

      .footer .footer-section.cta .button {
        background-color: #017AFF;
        color: #fff;
        padding: 1.5vh 2vw;
        border-radius: 0.5vw;
        text-align: center;
        font-size: 1.2vw;
        text-decoration: none;
        display: inline-block;
      }

      /* Social Links */
      .footer .social-links {
        display: flex;
        gap: 1vw;
      }

      .footer .social-links img {
        width: 2vw;
        height: 2vw;
      }

      /* Footer Bottom */
      .footer .footer-bottom {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2vh;
        border-top: 1px solid #ddd;
        padding-top: 3vh;
        width: 100%;
      }

      .footer .footer-logo img {
        height: 15vh;
      }

      .footer .copyright {
        font-size: 1vw;
      }

      .footer .copyright p {
        font-size: 1vw;
        color: #000;
      }

      @media (max-width: 768px) {
        .footer {
          padding: 15vh 4vw 8vw 4vw !important;
          margin: 0 !important;
          width: 100% !important;
          max-width: 100vw !important;
          box-sizing: border-box !important;
        }

        .footer .footer-content {
          display: grid;
          grid-template-columns: 1fr 1fr;
          grid-template-rows: auto auto auto;
          gap: 6vh 6vw;
          padding: 0 !important;
          width: 100% !important;
          margin: 0 !important;
        }

        .footer .footer-section.cta {
          grid-column: 1 / -1;
          border-right: none;
          padding-right: 0;
          text-align: center;
        }

        .footer .footer-section {
          text-align: left;
          width: 100%;
        }

        .footer .footer-section h3 {
          font-size: 5vw;
          margin-bottom: 2vh;
        }

        .footer .footer-section a,
        .footer .footer-section p {
          font-size: 4vw;
        }

        .footer .footer-section.cta h2 {
          font-size: 8vw;
        }

        .footer .footer-section.cta .button {
          font-size: 4vw;
          padding: 2vh 6vw;
          border-radius: 2vw;
          max-width: 60vw;
          margin: 0 auto;
        }

        .footer .social-links {
          justify-content: flex-start;
          gap: 4vw;
        }

        .footer .social-links img {
          width: 8vw;
          height: 8vw;
        }

        .footer .footer-logo img {
          height: 10vh;
        }

        .footer .copyright,
        .footer .copyright p {
          font-size: 3.5vw;
          text-align: center;
        }
      }
    </style>

    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section cta">
          <h2>Ready to grow your<br>business?</h2>
          <a href="/contact" class="button">Book a free strategy call</a>
        </div>
        <div class="footer-section">
          <h3>Quick Links</h3>
          <a href="/">Home</a>
          <a href="/about">About Us</a>
          <a href="/services">Services</a>
          <a href="/blogs">Blog</a>
          <!-- <a href="/careers">Careers</a> -->
        </div>
        <div class="footer-section">
          <h3>Services</h3>
          <a href="/services">Book Writing</a>
          <a href="/services">LinkedIn Branding</a>
          <a href="/services">Content Writing</a>
          <a href="/services">Performance Marketing</a>
          <a href="/services">Website Development</a>
        </div>
        <div class="footer-section social-section">
          <h3>Social Links</h3>
          <div class="social-links">
            <a href="#"><img src="/icons/instagram.png" alt="Instagram"></a>
            <a href="#"><img src="/icons/linkedin.png" alt="LinkedIn"></a>
            <a href="#"><img src="/icons/x.png" alt="X"></a>
          </div>
        </div>
        <div class="footer-section contact-section">
          <h3>Contact Us</h3>
          <a href="mailto:hello@suflexmedia.com">hello@suflexmedia.com</a>
        </div>
      </div>
      <div class="footer-bottom">
        <div class="footer-logo">
          <img src="/images/logo_header.png" alt="Suflex Media Logo">
        </div>
        <div class="copyright">
          <p>Copyright © 2024 SuflexMedia | All Rights Reserved</p>
        </div>
      </div>
    </footer>
  """


async def get_faq_section():
    return """
    <style>
    /* --- Minimal FAQ Styles --- */
    .faq-container {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .faq-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 80px;
        align-items: start;
    }
    
    .faq-header {
        position: sticky;
        top: 100px;
    }
    
    .faq-badge {
        display: inline-block;
        background: #f3f4f6;
        color: #6b7280;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 24px;
        border: 1px solid #6b7280;
    }
    
    .faq-title {
        font-size: 48px;
        font-weight: 400;
        line-height: 1.1;
        color: #1a1a1a;
        margin: 0 0 24px 0;
    }
    
    .faq-description {
        font-size: 18px;
        line-height: 1.6;
        color: #6b7280;
        margin-bottom: 32px;
    }
    
    .faq-cta {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: #1a1a1a;
        font-size: 16px;
        font-weight: 500;
        text-decoration: none;
        padding: 12px 20px;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        transition: all 0.2s ease;
        background: white;
    }
    
    .faq-cta:hover {
        border-color: #017AFF;
        background: #fafbff;
    }
    
    .faq-cta svg {
        width: 16px;
        height: 16px;
    }
    
    .faq-list {
        border-radius: 12px;
        overflow: hidden;
    }
    
    .faq-item {
        border-bottom: 1px solid #6b7280;
    }
    
    .faq-item:last-child {
        border-bottom: none;
    }
    
    .faq-toggle {
        width: 100%;
        padding: 24px;
        background: none;
        border: none;
        text-align: left;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        transition: background-color 0.2s ease;
    }
    
    
    .faq-question {
        font-size: 16px;
        font-weight: 500;
        color: #1a1a1a;
        line-height: 1.5;
        margin: 0;
    }
    
    .faq-icon {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        transition: transform 0.2s ease;
    }
    
    .faq-toggle[aria-expanded="true"] .faq-icon {
        transform: rotate(180deg);
    }
    
    .faq-icon svg {
        width: 16px;
        height: 16px;
        color: #6b7280;
    }
    
    .faq-content {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease;
    }
    
    .faq-answer {
        padding: 0 24px 24px 24px;
        color: #6b7280;
        line-height: 1.6;
        font-size: 15px;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .faq-grid {
            grid-template-columns: 1fr;
            gap: 48px;
        }
        
        .faq-header {
            position: static;
        }
        
        .faq-title {
            font-size: 36px;
        }
        
        .faq-description {
            font-size: 16px;
        }
        
        .faq-toggle {
            padding: 20px;
        }
        
        .faq-answer {
            padding: 0 20px 20px 20px;
        }
    }
    </style>

    <!-- ========== Minimal FAQ Section Start ========== -->
    <section class="faq-container py-4" id="faq">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="faq-grid">
                <!-- Left Column - Header -->
                <div class="faq-header">
                    <h2 class="faq-title">This is the start of something new</h2>
                    <p class="faq-description">
                        Managing a small business today is already tough. Avoid further complications by ditching outdated, tedious trade methods. Our goal is to streamline SMB trade, making it easier and faster than ever.
                    </p>
                    <a href="#contact" class="faq-cta">
                        <span>Any questions? Reach out</span>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M7 17L17 7M17 7H7M17 7V17"/>
                        </svg>
                    </a>
                </div>
                
                <!-- Right Column - FAQ Items -->
                <div class="faq-list" id="faq-accordion">
                    <!-- FAQ Item 1 -->
                    <div class="faq-item">
                        <button type="button" class="faq-toggle" aria-expanded="false">
                            <h3 class="faq-question">What is Brands Out Loud?</h3>
                            <div class="faq-icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M6 9l6 6 6-6"/>
                                </svg>
                            </div>
                        </button>
                        <div class="faq-content">
                            <div class="faq-answer">
                                Brands Out Loud is a premier digital media platform dedicated to providing in-depth analysis, insightful articles, and the latest news on business, technology, startups, and global trends. We focus on the stories that shape our future, with a special emphasis on innovation in the GCC region and beyond.
                            </div>
                        </div>
                    </div>

                    <!-- FAQ Item 2 -->
                    <div class="faq-item">
                        <button type="button" class="faq-toggle" aria-expanded="false">
                            <h3 class="faq-question">Who is the content for?</h3>
                            <div class="faq-icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M6 9l6 6 6-6"/>
                                </svg>
                            </div>
                        </button>
                        <div class="faq-content">
                            <div class="faq-answer">
                                Our content is created for forward-thinkers, entrepreneurs, business leaders, tech enthusiasts, and anyone curious about the forces driving modern economies. Whether you're a startup founder, a C-suite executive, or an aspiring innovator, you'll find valuable perspectives here.
                            </div>
                        </div>
                    </div>

                    <!-- FAQ Item 3 -->
                    <div class="faq-item">
                        <button type="button" class="faq-toggle" aria-expanded="false">
                            <h3 class="faq-question">Can I contribute an article to Brands Out Loud?</h3>
                            <div class="faq-icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M6 9l6 6 6-6"/>
                                </svg>
                            </div>
                        </button>
                        <div class="faq-content">
                            <div class="faq-answer">
                                We are always open to collaborating with industry experts and thought leaders. If you have a unique perspective or a compelling story to share, please visit our 'Write for Us' page for submission guidelines. We look for original, well-researched, and insightful content that aligns with our core topics.
                            </div>
                        </div>
                    </div>

                    <!-- FAQ Item 4 -->
                    <div class="faq-item">
                        <button type="button" class="faq-toggle" aria-expanded="false">
                            <h3 class="faq-question">How do I subscribe to the newsletter?</h3>
                            <div class="faq-icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M6 9l6 6 6-6"/>
                                </svg>
                            </div>
                        </button>
                        <div class="faq-content">
                            <div class="faq-answer">
                                Subscribing is easy! You can find the newsletter subscription form in the footer of our website. Just enter your email address and click "Subscribe" to receive our latest articles, special reports, and event invitations directly in your inbox.
                            </div>
                        </div>
                    </div>

                    <!-- FAQ Item 5 -->
                    <div class="faq-item">
                        <button type="button" class="faq-toggle" aria-expanded="false">
                            <h3 class="faq-question">What topics do you cover?</h3>
                            <div class="faq-icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M6 9l6 6 6-6"/>
                                </svg>
                            </div>
                        </button>
                        <div class="faq-content">
                            <div class="faq-answer">
                                We cover a wide range of topics including business strategy, technology trends, startup ecosystem, digital transformation, leadership insights, and market analysis with a focus on the GCC region and global markets.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <script>
    // --- FAQ Accordion Logic ---
    document.addEventListener('DOMContentLoaded', function() {
        const faqAccordion = document.getElementById('faq-accordion');
        if (!faqAccordion) return;

        faqAccordion.addEventListener('click', function (e) {
            const toggle = e.target.closest('.faq-toggle');
            if (!toggle) return;

            const item = toggle.closest('.faq-item');
            const content = item.querySelector('.faq-content');
            const isExpanded = toggle.getAttribute('aria-expanded') === 'true';

            // Close all other items
            faqAccordion.querySelectorAll('.faq-item').forEach(otherItem => {
                if (otherItem !== item) {
                    const otherToggle = otherItem.querySelector('.faq-toggle');
                    const otherContent = otherItem.querySelector('.faq-content');
                    
                    otherToggle.setAttribute('aria-expanded', 'false');
                    otherContent.style.maxHeight = '0px';
                }
            });

            // Toggle current item
            if (isExpanded) {
                toggle.setAttribute('aria-expanded', 'false');
                content.style.maxHeight = '0px';
            } else {
                toggle.setAttribute('aria-expanded', 'true');
                content.style.maxHeight = content.scrollHeight + 'px';
            }
        });
    });
    </script>
    <!-- ========== Minimal FAQ Section End ========== -->
    """


async def get_cards(category):
    print(f"Fetching blogs for category: {category}")
    # Hardcoded test data
    xx = []

    # Sample blog 1
    xx.append(
        f"""<a href="/blog/1" class="block">
                <div class="card bg-white rounded-xl shadow-md overflow-hidden flex-1 hover:shadow-lg transition-shadow duration-300">
                    <!-- Card image -->
                    <div class="h-48 overflow-hidden">
                        <img src="https://picsum.photos/seed/blog1/800/400" alt="Sample Blog Image 1" class="w-full h-full object-cover">
                    </div>
                    <!-- Card content -->
                    <div class="p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-2">The Future of Digital Marketing in 2024</h3>
                        <p class="text-gray-600 mb-4">Explore the latest trends and strategies that are shaping the digital marketing landscape this year.</p>
                        <div class="flex items-center text-sm text-gray-500 mb-3">
                            <span>John Doe</span>
                            <span class="mx-2">•</span>
                            <span>Jan 15, 2024</span>
                        </div>
                    </div>
                </div>
            </a>"""
    )

    # Sample blog 2
    xx.append(
        f"""<a href="/blog/2" class="block">
                <div class="card bg-white rounded-xl shadow-md overflow-hidden flex-1 hover:shadow-lg transition-shadow duration-300">
                    <!-- Card image -->
                    <div class="h-48 overflow-hidden">
                        <img src="https://picsum.photos/seed/blog2/800/400" alt="Sample Blog Image 2" class="w-full h-full object-cover">
                    </div>
                    <!-- Card content -->
                    <div class="p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-2">AI and Machine Learning: Transforming Business</h3>
                        <p class="text-gray-600 mb-4">Discover how artificial intelligence is revolutionizing the way businesses operate and make decisions.</p>
                        <div class="flex items-center text-sm text-gray-500 mb-3">
                            <span>Jane Smith</span>
                            <span class="mx-2">•</span>
                            <span>Jan 20, 2024</span>
                        </div>
                    </div>
                </div>
            </a>"""
    )

    # Sample blog 3
    xx.append(
        f"""<a href="/blog/3" class="block">
                <div class="card bg-white rounded-xl shadow-md overflow-hidden flex-1 hover:shadow-lg transition-shadow duration-300">
                    <!-- Card image -->
                    <div class="h-48 overflow-hidden">
                        <img src="https://picsum.photos/seed/blog3/800/400" alt="Sample Blog Image 3" class="w-full h-full object-cover">
                    </div>
                    <!-- Card content -->
                    <div class="p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-2">Sustainable Business Practices for Growth</h3>
                        <p class="text-gray-600 mb-4">Learn how sustainability can drive innovation and create long-term value for your business.</p>
                        <div class="flex items-center text-sm text-gray-500 mb-3">
                            <span>Mike Johnson</span>
                            <span class="mx-2">•</span>
                            <span>Jan 25, 2024</span>
                        </div>
                    </div>
                </div>
            </a>"""
    )

    return "\n".join(xx)


async def get_more_blogs_section(data: dict):
    template = """
    <style>
        more_blogs {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f9fafb;
        }
        .card {
            transition: transform 0.2s ease-in-out;
        }
        .card:hover {
            transform: translateY(-4px);
        }
        .see-more-btn {
            transition: all 0.3s ease;
            background-color: #017AFF;
        }
        .see-more-btn:hover {
            background-color: #2821a8;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(53, 51, 205, 0.3);
        }
    </style>
    
    <section class="py-12 px-4 more_blogs">
    <hr class="border-t border-black my-8 md:my-12 w-full md:w-[90%] lg:w-[80rem] mx-auto" />
    <div class="max-w-6xl mx-auto">
        <!-- Heading -->
        <h2 class="text-4xl font-serif text-center mb-10 text-gray-800">Related Articles and Topics</h2>
        
        <!-- Main content container -->
        <div class="flex flex-col gap-6">
            <!-- Articles container -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Cards -->
                [[cards]]
            </div>

            <!-- See More Button -->
            <div class="flex justify-center mt-8">
                <a href="/blogs" class="see-more-btn px-8 py-3 text-white font-medium rounded-lg inline-flex items-center gap-2">
                    See More Articles
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                </a>
            </div>
        </div>
    </div>
</section>"""
    return template.replace("[[cards]]", await get_cards("sample_category"))


async def get_blog_hero_section(data: dict):
    return f"""
    <style>
        @media (max-width: 768px) {{
            .mobile-breadcrumb {{
                margin-left: 0 !important;
                padding-left: 4vw !important;
                padding-right: 4vw !important;
                width: 100% !important;
                box-sizing: border-box !important;
            }}
            .mobile-hero-article {{
                max-width: 100% !important;
                width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
            .mobile-hero-content {{
                width: 100% !important;
                margin-left: 0 !important;
                margin-right: 0 !important;
                padding-left: 4vw !important;
                padding-right: 4vw !important;
                box-sizing: border-box !important;
            }}
        }}
    </style>
    <article>
    <nav class="mb-4 text-left mobile-breadcrumb ml-0 md:ml-[-39.5rem] mt-4 md:mt-32" aria-label="Breadcrumb">
        <div class="text-sm text-gray-600">
            <span class="font-jakarta font-medium flex items-center flex-wrap">
                <a href="/blogs" class="flex items-center">blogs</a>
                <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
                <span class="flex items-center">{data['blogCategory']}</span>
                <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
            </span>
        </div>
    </nav>
</article>
<article class="relative mobile-hero-article max-w-[95%]">
    <div class="relative w-full h-[300px] md:h-[478px]">
        <div class="absolute inset-0 bg-cover bg-center"></div>
        <img src="{data['mainImageUrl']}" alt="{data['mainImageAlt']}"
            class="w-full h-full object-cover mix-blend-multiply" />
    </div>
    <div
        class="relative bg-white mobile-hero-content md:w-full w-full md:ml-[3.3rem] ml-0 max-w-[1175px] h-auto mx-auto -mt-[40px] sm:-mt-[60px] md:-mt-[76px] p-4 sm:p-6 md:p-8 z-10 ">
        <h1
            class="font-jakarta font-medium text-[28px] sm:text-[34px] md:text-[42px] lg:text-[50px] leading-[1.2] md:leading-[1.25] capitalize text-black mb-3 md:mb-4 text-center hero-text">
            {data['blogTitle']}
        </h1>
        <div class="flex justify-center items-center gap-2 text-center mb-4">
            <p class="font-jakarta font-normal text-[11px] sm:text-[12px] md:text-[14px] leading-[100.9%] text-black">
                {data['blogDate']} </p>
        </div>
    </div>
    <p
        class="font-jakarta font-medium text-[18px] md:text-[22px] leading-[26px] md:leading-[30px] text-[#636363] text-center max-w-[1175px] mx-auto px-2 md:px-0">
        {data['blogSummary']}
    </p>
    <hr class="border-t border-black my-8 md:my-12 w-full md:w-[90%] lg:w-[80rem] mx-auto" />
</article>"""


async def generate_mobile_toc(data):
    """
    Generate a mobile Table of Contents HTML from structured data.

    Args:
        data: List of dictionaries with 'id', 'type', and 'content' keys

    Returns:
        Complete HTML string for the mobile TOC
    """
    toc_sections = await _generate_toc_sections(data)

    complete_toc = f"""<div class="block lg:hidden px-4 mt-8">
            <div class="relative toc-container p-5 bg-white rounded-xl border-gray-100">
                <h2 class="text-xl font-bold text-[#017AFF] mb-4 border-b pb-3">Table of Contents</h2>
                {toc_sections}
                <div class="mt-6 space-y-4 border-t pt-5">
                    <button
                        class="w-full h-[45px] bg-[#017AFF] rounded-xl flex items-center justify-center text-white font-jakarta font-medium text-[16px] leading-[120%] hover:bg-opacity-90 transition-colors shadow-md">
                        <i class="ph ph-download mr-2"></i>Download Article as PDF
                    </button>
                    <div class="flex items-center flex-wrap">
                        <div
                            class="relative inline-flex items-center justify-center gap-2 bg-[#017AFF] rounded-xl h-[45px] px-4 cursor-pointer hover:bg-opacity-90 transition-colors shadow-md">
                            <span class="text-white font-jakarta font-medium text-[16px] leading-[120%] text-center"
                                style="width: 7rem">
                                <i class="ph ph-share-network mr-2"></i>Share
                            </span>
                        </div>
                        <div class="flex space-x-3 ml-3">
                            <img src="/icons/whatsapp_logo.png" alt="WhatsApp"
                                class="w-[35px] h-[35px] object-contain hover:opacity-80 transition-opacity" />
                            <img src="/icons/insta_logo.png" alt="Instagram"
                                class="w-[35px] h-[35px] object-contain hover:opacity-80 transition-opacity" />
                        </div>
                    </div>
                </div>
            </div>
        </div>"""

    return complete_toc


async def _generate_toc_sections(data):
    """
    Helper function to generate the TOC sections that are common to both mobile and desktop versions.

    Args:
        data: List of dictionaries with 'id', 'type', and 'content' keys

    Returns:
        HTML string for the TOC sections only
    """
    # Filter for headers only
    headers = ["h1", "h2"]
    temp_list = [item for item in data if item["type"] in headers]

    final_product = []
    sub_list = []
    base_template = None

    for item in temp_list:
        if item["type"] == "h1":
            # If we have a previous h1 section, finalize it
            if base_template is not None:
                sub_categories = "\n".join(sub_list) if sub_list else ""
                final_section = base_template.replace(
                    "[[sub_categories]]", sub_categories
                )
                final_product.append(final_section)

            # Start new h1 section
            sub_list = []
            base_template = f"""<div class="mb-3 toc-section" data-section-id="{item['id']}">
                        <a href="#{item['id']}"
                            data-toggle-target="#sub-{item['id']}"
                            class="toc-h2-link flex items-center justify-between mt-1 mb-3 no-underline text-gray-800 hover:text-[#017AFF] transition-colors duration-200 toc-link">
                            <div class="text-base font-medium">{item['content']}</div>
                            <i class="ph ph-caret-down text-xs ml-1 toc-arrow transition-transform duration-300"></i>
                        </a>
                        <div id="sub-{item['id']}"
                            class="toc-subcategories hidden pl-4 mb-3 space-y-2">
                            [[sub_categories]]
                        </div>
                    </div>"""

        elif item["type"] == "h2":
            # Add h2 as subcategory
            sub_template = f"""                            <a href="#{item['id']}"
                                class="flex items-center mt-1 no-underline text-gray-600 hover:text-[#017AFF] transition-colors duration-200 toc-link border-l-2 border-gray-200 pl-3 hover:border-[#017AFF]">
                                <div class="text-sm">{item['content']}</div>
                            </a>"""
            sub_list.append(sub_template)

    # Don't forget the last section
    if base_template is not None:
        sub_categories = "\n".join(sub_list) if sub_list else ""
        final_section = base_template.replace("[[sub_categories]]", sub_categories)
        final_product.append(final_section)

    return "\n".join(final_product)


async def generate_desktop_toc(data):
    """
    Generate a desktop/sidebar Table of Contents HTML from structured data.

    Args:
        data: List of dictionaries with 'id', 'type', and 'content' keys

    Returns:
        Complete HTML string for the desktop TOC
    """
    toc_sections = await _generate_toc_sections(data)

    complete_toc = f"""<aside class="sticky top-8 h-8rem lg:order-1 self-start md:mt-[0rem] mt-[-57rem]">
                <div class="p-6 flex flex-col w-full rounded-xl bg-white max-w-[20rem] border-gray-100 hidden lg:block overflow-y- max-h-[calc(100vh-4rem)]"
                    style="scroll-behavior: smooth">
                    <h2 class="text-2xl font-bold text-[#017AFF] mb-6 border-b pb-3">Table of Contents</h2>
                    {toc_sections}
                    <div class="mt-6 space-y-4 border-t pt-5">
                        <button
                            class="w-full h-[45px] bg-[#017AFF] rounded-xl flex items-center justify-center text-white font-jakarta font-medium text-[16px] leading-[120%] hover:bg-opacity-90 transition-colors shadow-md">
                            <i class="ph ph-download mr-2"></i>Download Article as PDF
                        </button>
                        <div class="flex items-center flex-wrap">
                            <div
                                class="relative inline-flex items-center justify-center gap-2 bg-[#017AFF] rounded-xl h-[45px] px-4 cursor-pointer hover:bg-opacity-90 transition-colors shadow-md">
                                <span class="text-white font-jakarta font-medium text-[16px] leading-[120%] text-center"
                                    style="width: 7rem">
                                    <i class="ph ph-share-network mr-2"></i>Share
                                </span>
                            </div>
                            <div class="flex space-x-3 ml-3">
                                <img src="/icons/whatsapp_logo.png" alt="WhatsApp"
                                    class="w-[35px] h-[35px] object-contain hover:opacity-80 transition-opacity" />
                                <img src="/icons/insta_logo.png" alt="Instagram"
                                    class="w-[35px] h-[35px] object-contain hover:opacity-80 transition-opacity" />
                            </div>
                        </div>
                    </div>
                </div>
            </aside>"""

    return complete_toc


async def get_blog_content(data: dict):
    content = []
    for i in data:
        if i["type"] == "text":
            content.append(
                f"""<p class="font-jakarta font-medium text-[15px] md:text-[16px] leading-[26px] md:leading-[30px] text-black" >{i['content']}</p>"""
            )
        if i["type"] == "h1":
            content.append(
                f"""<h1 id="{i['id']}" class="font-jakarta font-bold text-[28px] md:text-[36px] leading-[32px] md:leading-[40px] text-black scroll-mt-20" >{i['content']}</h1>"""
            )
        if i["type"] == "h2":
            content.append(
                f"""<h2 id="{i['id']}" class="font-jakarta font-medium text-[22px] md:text-[28px] leading-[28px] md:leading-[30px] text-black scroll-mt-20" >{i['content']}</h2>"""
            )
        if i["type"] == "h3":
            content.append(
                f"""<h3  class="font-jakarta font-medium text-[20px] md:text-[24px] leading-[26px] md:leading-[28px] text-black scroll-mt-20" >{i['content']}</h3>"""
            )
        if i["type"] == "h4":
            content.append(
                f"""<h4  class="font-jakarta font-medium text-[18px] md:text-[22px] leading-[24px] md:leading-[26px] text-black scroll-mt-20" >{i['content']}</h4>"""
            )
        if i["type"] == "h5":
            content.append(
                f"""<h5  class="font-jakarta font-medium text-[16px] md:text-[20px] leading-[22px] md:leading-[24px] text-black scroll-mt-20" >{i['content']}</h5>"""
            )
        if i["type"] == "h6":
            content.append(
                f"""<h6  class="font-jakarta font-medium text-[14px] md:text-[18px] leading-[20px] md:leading-[22px] text-black scroll-mt-20" >{i['content']}</h6>"""
            )
        if i["type"] == "image":
            content.append(
                f"""<div class="w-full h-[120px] sm:h-[160px] md:h-[236px] my-8 md:my-12"><img src="{i['content']['url']}" alt="{i['content']['alt']}" class="w-full h-full object-cover"/></div>"""
            )
    content = "\n".join(content)
    return f"""<section class="max-w-[43rem] space-y-6 md:space-y-5 text-justify order-1 lg:order-2">{content}</section>"""


async def get_blog_body(data: dict):
    hero_section = await get_blog_hero_section(data)
    mobile_toc = await generate_mobile_toc(data["dynamicSections"])
    desktop_toc = await generate_desktop_toc(data["dynamicSections"])
    blog_content = await get_blog_content(data["dynamicSections"])

    return f"""
        <style>
            @media (max-width: 768px) {{
                .mobile-blog-grid {{
                    margin-left: 0 !important;
                    margin-right: 0 !important;
                    padding: 0 4vw !important;
                    width: 100% !important;
                    box-sizing: border-box !important;
                }}
            }}
        </style>
        {hero_section}
        {mobile_toc}
        <div class="mobile-blog-grid grid grid-cols-1 lg:grid-cols-[300px_1fr] md:ml-[-16rem] gap-8 mt-4 md:mt-8 ml-0 mr-0" style="padding: 0 0.5rem">
        {desktop_toc}
        {blog_content}
        </div>

"""


EMPTY_BLOG_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth w-full">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>News Page Dev</title>
    <link rel="icon" type="image/png" href="static/icon/website_icon.png" />
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/@phosphor-icons/web@2.0.3"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
        rel="stylesheet" />
    <link
        href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@600&family=Inter:wght@500&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;1,700&display=swap"
        rel="stylesheet" />
    <script>
        /* Define custom fonts in Tailwind (optional, better in tailwind.config.js) */
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        jakarta: ['"Plus Jakarta Sans"', "sans-serif"],
                        "helvetica-now": ['"Helvetica Now Display"', "sans-serif"],
                        helvetica: ['"Helvetica"', "sans-serif"],
                        "ibm-plex": ['"IBM Plex Sans"', "sans-serif"],
                        inter: ['"Inter"', "sans-serif"],
                    },
                    backgroundImage: {
                        "header-banner":
                            "url('digital-marketing-agency-website-banner-ad-template-lzytv.png')",
                        "hero-gradient":
                            "linear-gradient(0deg, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('https://picsum.photos/1920/1080')", // Placeholder image used for gradient bg
                        "podcast-bg":
                            "linear-gradient(360deg, rgba(255, 255, 255, 0) 74.02%, #FFFFFF 100%), linear-gradient(180deg, rgba(255, 255, 255, 0) 61.61%, #FFFFFF 100%), url('Your paragraph text (8).png')",
                        "cta-bg":
                            "linear-gradient(0deg, rgba(0, 0, 0, 0.69), rgba(0, 0, 0, 0.69)), url('Screenshot 2024-09-18 at 9.57.41\u202fPM.png')",
                        "gradient-line":
                            "linear-gradient(90deg, #000000 0%, #9747FF 100%)",
                    },
                },
            },
        };
    </script>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const mobileMenuButton = document.getElementById('mobile-menu-button');
            const mobileMenu = document.getElementById('mobile-menu');

            mobileMenuButton.addEventListener('click', function () {
                mobileMenu.classList.toggle('hidden');
                mobileMenuButton.classList.toggle('hamburger-active');

                if (!mobileMenu.classList.contains('hidden')) {
                    mobileMenu.classList.add('slide-down');
                } else {
                    mobileMenu.classList.remove('slide-down');
                }
            });

            // Blog item click handlers
            document.addEventListener('click', function (e) {
                if (e.target.closest('.dropdown-item:not(.know-more-item)')) {
                    const item = e.target.closest('.dropdown-item');
                    const category = item.getAttribute('data-category');
                    const blogId = item.getAttribute('data-id');

                    console.log('Clicked blog:', { category, blogId });
                    // Replace with actual navigation
                    // window.location.href = `/blog/${category}/${blogId}`;
                }
            });

            // Know More click handlers
            document.addEventListener('click', function (e) {
                if (e.target.closest('.know-more-item')) {
                    const item = e.target.closest('.dropdown-container');
                    const category = item.getAttribute('data-category');

                    console.log('Know More clicked for:', category);
                    // Replace with actual navigation
                    // window.location.href = `/category/${category}`;
                }
            });

            // --- Mobile Accordion Menu Logic ---
            const mobileMenuContainer = document.getElementById('mobile-menu');
            if (mobileMenuContainer) {
                mobileMenuContainer.addEventListener('click', function (e) {
                    const toggle = e.target.closest('.accordion-toggle');
                    if (!toggle) return;

                    e.preventDefault();
                    const content = toggle.nextElementSibling;
                    const isCurrentlyOpen = toggle.getAttribute('aria-expanded') === 'true';

                    // Close all other accordions before opening a new one
                    mobileMenuContainer.querySelectorAll('.accordion-toggle').forEach(otherToggle => {
                        if (otherToggle !== toggle) {
                            otherToggle.setAttribute('aria-expanded', 'false');
                            const otherContent = otherToggle.nextElementSibling;
                            if (otherContent) otherContent.style.maxHeight = '0px';
                        }
                    });

                    // Toggle the clicked accordion
                    if (isCurrentlyOpen) {
                        toggle.setAttribute('aria-expanded', 'false');
                        content.style.maxHeight = '0px';
                    } else {
                        toggle.setAttribute('aria-expanded', 'true');
                        content.style.maxHeight = content.scrollHeight + 'px';
                    }
                });
            }

        });
    </script>
    <style>
        @media screen and (max-width: 768px) {
            html, body {
                width: 100% !important;
                max-width: 100vw !important;
                overflow-x: hidden !important;
                margin: 0 !important;
                padding: 0 !important;
            }

            .hero-text {
                font-size: 28px !important;
                line-height: 36px !important;
            }

            .article-container {
                padding-left: 4vw !important;
                padding-right: 4vw !important;
                margin: 0 !important;
                width: 100% !important;
                box-sizing: border-box !important;
            }

            .toc-container {
                padding: 10px !important;
                margin: 0 4vw !important;
                width: calc(100% - 8vw) !important;
                box-sizing: border-box !important;
            }

            section, article, div {
                max-width: 100vw !important;
            }
        }

        @import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@600&family=Inter:wght@500&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;1,700&display=swap");

        @font-face {
            font-family: "Helvetica Now Display";
            src: local("Helvetica Neue"), local("Helvetica"), local("Arial"),
                sans-serif;
            /* Basic fallback */
            font-weight: 700;
        }

        @font-face {
            font-family: "Helvetica";
            src: local("Helvetica Neue"), local("Helvetica"), local("Arial"),
                sans-serif;
            /* Basic fallback */
            font-weight: 400;
        }

        ::-webkit-scrollbar {
            display: none;
        }

        body {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        @media screen and (min-width: 1024px) {
            body {
                zoom: 1.145;
            }
        }

        @keyframes slideDown {
            from {
                transform: translateY(-10px);
                opacity: 0;
            }

            to {
                transform: translateY(0);
                opacity: 1;
            }
        }

        .slide-down {
            animation: slideDown 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        :root {
            --clr-dark-black: #121212;
            --clr-bdr-gray: #2a2a2a;
            --clr-white: #fff;
            --clr-primary: #9747ff;
            --clr-primary-light: #cda7ff;
            --clr-gray-800: #1e1e1e;
        }

        .mobile-menu-item {
            padding: 0.875rem 1rem;
            background: var(--clr-dark-black);
            border-bottom: solid 1px var(--clr-bdr-gray);
            color: var(--clr-white);
            cursor: pointer;
            display: flex;
            align-items: center;
            transition: background-color 0.2s ease;
        }

        .mobile-menu-item:hover {
            background-color: #1a1a1a;
        }

        .mobile-menu-item:active {
            background-color: #252525;
        }

        .item-title {
            flex-grow: 1;
            margin-left: 0.75rem;
            font-weight: 500;
        }

        .hamburger-line {
            transition: all 0.3s ease;
        }

        .hamburger-active .hamburger-line:nth-child(1) {
            transform: translateY(7px) rotate(45deg);
        }

        .hamburger-active .hamburger-line:nth-child(2) {
            opacity: 0;
        }

        .hamburger-active .hamburger-line:nth-child(3) {
            transform: translateY(-7px) rotate(-45deg);
        }

        .search-input {
            transition: all 0.2s ease;
        }

        .search-input:focus {
            box-shadow: 0 0 0 2px rgba(151, 71, 255, 0.5);
        }

        @keyframes shine {
            from {
                transform: translateX(-100%);
            }

            to {
                transform: translateX(100%);
            }
        }

        .login-btn {
            transition: all 0.2s ease;
        }

        .login-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(205, 167, 255, 0.4);
        }

        /* TOC container enhancements */
        aside .p-6 {
            scrollbar-width: thin;
            scrollbar-color: #017AFF #f5f5f5;
            scroll-behavior: smooth;
            transition: all 0.3s ease;
        }

        .toc-container {
            scrollbar-width: thin;
            scrollbar-color: #017AFF #f5f5f5;
            scroll-behavior: smooth;
            transition: all 0.3s ease;
        }

        /* Custom scrollbar for webkit browsers */
        aside .p-6::-webkit-scrollbar,
        .toc-container::-webkit-scrollbar {
            width: 6px;
        }

        aside .p-6::-webkit-scrollbar-track,
        .toc-container::-webkit-scrollbar-track {
            background: #f5f5f5;
            border-radius: 10px;
        }

        aside .p-6::-webkit-scrollbar-thumb,
        .toc-container::-webkit-scrollbar-thumb {
            background: rgba(53, 51, 205, 0.5);
            border-radius: 10px;
        }

        /* Smooth transitions for TOC links */
        .toc-link {
            transition: color 0.3s ease, font-weight 0.2s ease,
                border-color 0.3s ease;
        }

        /* Active indicator animation */
        .toc-link.text-\[\#017AFF\] {
            position: relative;
        }

        .toc-link.text-\[\#017AFF\]::after {
            content: "";
            position: absolute;
            right: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 4px;
            height: 70%;
            border-radius: 2px;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }

            to {
                opacity: 1;
            }
        }

        /* --- UPDATED DROPDOWN STYLES --- */
        .dropdown-container {
            position: relative;
            padding-bottom: 20px;
            /* Creates an invisible area below the link for the cursor to travel over */
            margin-bottom: -20px;
            /* Negative margin to pull layout back up */
        }

        .dropdown-content {
            position: absolute;
            top: 100%;
            /* Positions the dropdown right below the parent's padding area */
            left: 50%;
            transform: translateX(-50%);
            width: 320px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
            border: 1px solid #e5e7eb;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.2s ease, visibility 0.2s;
            z-index: 50;
            pointer-events: none;
            padding: 1rem;
        }

        .dropdown-container:hover .dropdown-content {
            opacity: 1;
            visibility: visible;
            pointer-events: auto;
        }

        .line-clamp-2 {
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .dropdown-item {
            transition: all 0.2s ease;
        }

        .dropdown-item:hover {
            background-color: #f9fafb;
            transform: translateX(2px);
        }

        .dropdown-item:hover .ph-arrow-right {
            transform: translateX(2px);
            color: #017AFF;
        }

        /* --- MOBILE ACCORDION STYLES --- */
        .accordion-toggle .item-title {
            flex-grow: 1;
        }

        .accordion-icon {
            transition: transform 0.3s ease, color 0.3s ease;
        }

        .accordion-toggle[aria-expanded="true"] .accordion-icon {
            transform: rotate(180deg);
            color: white;
        }

        .accordion-content {
            background-color: #1a1a1a;
            overflow: hidden;
            max-height: 0;
            transition: max-height 0.4s cubic-bezier(0.25, 1, 0.5, 1);
        }

        .sub-menu-item {
            display: flex;
            align-items: center;
            padding: 0.5rem;
            border-radius: 0.375rem;
            transition: background-color 0.2s ease;
            color: white;
            text-decoration: none;
        }

        .sub-menu-item:hover {
            background-color: #252525;
        }

        

        /* Mobile TOC arrow styling for better touch targets */
        @media screen and (max-width: 1023px) {
            .toc-arrow {
                padding: 8px;
                margin: -8px;
                cursor: pointer;
                border-radius: 4px;
                transition: background-color 0.2s ease;
                position: relative;
                z-index: 10;
            }

            .toc-arrow:hover {
                background-color: rgba(53, 51, 205, 0.1);
            }
        }
    </style>
</head>

<body class="font-jakarta bg-white text-bol-black flex flex-col items-center w-full max-w-[100vw] mx-auto bg-white overflow-x-hidden relative" style="margin: 0; padding: 0;">

        [[total_body]]


    <script>
        const stripSection = document.querySelector(".strip-section");
        if (stripSection) {
            const stripContent = stripSection.querySelector(".animate-marquee");
            if (stripContent && stripContent.children.length > 0) {
                const contentWidth = stripContent.scrollWidth / 2;
                const containerWidth = stripSection.offsetWidth;
                stripContent.innerHTML += stripContent.innerHTML;
            }
        }
        // Enhanced TOC with auto-scrolling functionality
        document.addEventListener("DOMContentLoaded", function () {
            const tocDesktop = document.querySelector("aside .p-6");
            const tocMobile = document.querySelector(".toc-container");
            const tocLinks = document.querySelectorAll(".toc-link");
            const sections = document.querySelectorAll("h1[id], h2[id], h3[id], p[id]");
            console.log("TOC Debug - Found sections:", sections.length);
            sections.forEach(section => {
                console.log("Section:", section.tagName, section.id);
            });
            // Colors and styles for active/inactive states
            const activeColorClass = "text-[#017AFF]";
            const inactiveColorClass = "text-gray-800";
            const activeFontWeightClass = "font-bold";
            const inactiveFontWeightClass = "font-medium";
            const activeBorderClass = "border-[#017AFF]";
            const inactiveBorderClass = "border-gray-200";        // Collapsible TOC functionality - different behavior for mobile and desktop
            const tocToggleLinks = document.querySelectorAll(
                "a[data-toggle-target]"
            );
            tocToggleLinks.forEach((link) => {
                const arrowIcon = link.querySelector(".toc-arrow");
                const textDiv = link.querySelector("div");
                // Handle arrow clicks for mobile
                if (arrowIcon) {
                    arrowIcon.addEventListener("click", function (event) {
                        event.preventDefault();
                        event.stopPropagation();
                        const targetId = link.getAttribute("data-toggle-target");
                        const targetElement = document.querySelector(targetId);
                        if (targetElement) {
                            targetElement.classList.toggle("hidden");
                            arrowIcon.classList.toggle("rotate-180");
                        }
                    });
                }
                // Handle text clicks for navigation
                if (textDiv) {
                    textDiv.addEventListener("click", function (event) {
                        const href = link.getAttribute("href");
                        if (href && href.startsWith("#")) {
                            event.preventDefault();
                            const targetElement = document.querySelector(href);
                            if (targetElement) {
                                targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                            }
                        }
                    });
                }
                // For desktop, maintain original behavior
                link.addEventListener("click", function (event) {
                    const isMobile = window.innerWidth < 1024;
                    if (!isMobile) {
                        const targetId = this.getAttribute("data-toggle-target");
                        const targetElement = document.querySelector(targetId);
                        if (targetElement) {
                            targetElement.classList.toggle("hidden");
                            if (arrowIcon) {
                                arrowIcon.classList.toggle("rotate-180");
                            }
                        }
                    }
                });
            });
            // Handle sub-category links (those without data-toggle-target)
            const subCategoryLinks = document.querySelectorAll('.toc-link:not([data-toggle-target])');
            subCategoryLinks.forEach((link) => {
                link.addEventListener("click", function (event) {
                    const href = this.getAttribute("href");
                    if (href && href.startsWith("#")) {
                        event.preventDefault();
                        const targetElement = document.querySelector(href);
                        if (targetElement) {
                            targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }
                    }
                });
            });
            // Enhanced scrollspy with TOC auto-scrolling
            function activateTocLink() {
                let currentSectionId = "";
                let currentParentSectionId = "";
                const scrollPosition = window.scrollY;
                const offset = 150; // Adjust based on header height
                let activeLink = null;
                // Find current section in view
                sections.forEach((section) => {
                    const sectionTop = section.offsetTop;
                    if (scrollPosition >= sectionTop - offset) {
                        currentSectionId = section.getAttribute("id");
                        // Determine parent H1 section (main section)
                        let parentH1 = null;
                        if (section.tagName === "H1") {
                            parentH1 = section;
                        } else {
                            // Find preceding H1
                            let previousElement = section.previousElementSibling;
                            while (previousElement) {
                                if (
                                    previousElement.tagName === "H1" &&
                                    previousElement.hasAttribute("id")
                                ) {
                                    parentH1 = previousElement;
                                    break;
                                }
                                previousElement = previousElement.previousElementSibling;
                            }
                            if (!parentH1) {
                                const parentDiv = section.closest("div");
                                if (parentDiv) {
                                    const h1InDiv = parentDiv.querySelector("h1[id]");
                                    if (h1InDiv) parentH1 = h1InDiv;
                                }
                            }
                        }
                        if (parentH1) {
                            currentParentSectionId = parentH1.getAttribute("id");
                        } else if (section.tagName === "H1") {
                            currentParentSectionId = currentSectionId;
                        }
                    }
                });
                // Update TOC link styles and expand sections
                tocLinks.forEach((link) => {
                    const linkHref = link.getAttribute("href");
                    const linkTargetId = linkHref ? linkHref.substring(1) : null;
                    const isH1Link = link.classList.contains("toc-h2-link"); // Note: class name is still "toc-h2-link" but represents H1 sections
                    const parentTocSection = link.closest(".toc-section");
                    const parentSectionDataId = parentTocSection
                        ? parentTocSection.dataset.sectionId
                        : null;
                    // Reset styles
                    link.classList.remove(activeFontWeightClass);
                    link.classList.add(inactiveFontWeightClass);
                    link.classList.replace(activeColorClass, inactiveColorClass);
                    // Border classes for subcategory links (H2 links)
                    if (!isH1Link) {
                        link.classList.replace(activeBorderClass, inactiveBorderClass);
                    }
                    // Highlight active link
                    if (linkTargetId === currentSectionId) {
                        link.classList.add(activeFontWeightClass);
                        link.classList.remove(inactiveFontWeightClass);
                        link.classList.replace(inactiveColorClass, activeColorClass);
                        if (!isH1Link) {
                            link.classList.replace(inactiveBorderClass, activeBorderClass);
                        }
                        activeLink = link; // Store active link for scrolling
                    }
                    // Highlight parent H1 if child is active
                    else if (
                        isH1Link &&
                        parentSectionDataId === currentParentSectionId
                    ) {
                        link.classList.add(activeFontWeightClass);
                        link.classList.remove(inactiveFontWeightClass);
                    }
                });          // Auto-expand/collapse TOC sections - disabled for mobile
                document.querySelectorAll(".toc-section").forEach((tocSection) => {
                    const sectionId = tocSection.dataset.sectionId;
                    const subcategoriesDiv =
                        tocSection.querySelector(".toc-subcategories");
                    const arrowIcon = tocSection.querySelector(".toc-arrow");
                    const isMobile = window.innerWidth < 1024;
                    if (subcategoriesDiv && arrowIcon && !isMobile) {
                        // Only auto-expand/collapse for desktop
                        if (sectionId === currentParentSectionId) {
                            // Expand current section
                            subcategoriesDiv.classList.remove("hidden");
                            arrowIcon.classList.add("rotate-180");
                        } else {
                            // Collapse other sections
                            subcategoriesDiv.classList.add("hidden");
                            arrowIcon.classList.remove("rotate-180");
                        }
                    }
                });
                // Scroll active link into view (for both mobile and desktop TOC)
                if (activeLink) {
                    // Handle desktop TOC scrolling
                    if (tocDesktop && window.innerWidth >= 1024) {
                        const linkTop = activeLink.offsetTop;
                        const tocTop = tocDesktop.scrollTop;
                        const tocHeight = tocDesktop.clientHeight;
                        // Check if link is not visible in the current view
                        if (linkTop < tocTop || linkTop > tocTop + tocHeight - 50) {
                            // Smoothly scroll to the active link
                            tocDesktop.scrollTo({
                                top: linkTop - tocHeight / 3,
                                behavior: "smooth",
                            });
                        }
                    }
                    // Handle mobile TOC scrolling
                    if (tocMobile && window.innerWidth < 1024) {
                        const linkTop = activeLink.offsetTop;
                        const tocTop = tocMobile.scrollTop;
                        const tocHeight = tocMobile.clientHeight;
                        if (linkTop < tocTop || linkTop > tocTop + tocHeight - 40) {
                            tocMobile.scrollTo({
                                top: linkTop - tocHeight / 3,
                                behavior: "smooth",
                            });
                        }
                    }
                }
            }
            // Initialize active state on load
            activateTocLink();
            // Update on scroll
            window.addEventListener("scroll", activateTocLink);
            
            // Add functionality for download and share buttons
            setupDownloadAndShareButtons();
        });
        
        function setupDownloadAndShareButtons() {
            console.log('Setting up download and share buttons');
            
            // Download PDF functionality - find buttons with download icons
            const allButtons = document.querySelectorAll('button');
            let downloadButtonsFound = 0;
            
            console.log('Found total buttons:', allButtons.length);
            
            // Check each button for download icon
            allButtons.forEach(button => {
                const downloadIcon = button.querySelector('i.ph-download');
                if (downloadIcon) {
                    console.log('Found download button, adding click listener');
                    downloadButtonsFound++;
                    button.addEventListener('click', handleDownloadClick);
                }
            });
            
            console.log('Download buttons found and configured:', downloadButtonsFound);
            
            function handleDownloadClick(e) {
                console.log('Download button clicked!');
                e.preventDefault();
                e.stopPropagation();
                
                const articleTitle = document.querySelector('.hero-text')?.textContent?.trim() || document.querySelector('h1')?.textContent?.trim() || 'Article';
                console.log('Article title:', articleTitle);
                
                const mainImage = document.querySelector('article img[src*="pexels"], article img[src*="picsum"], article img[alt]');
                const mainImageUrl = mainImage?.src || '';
                const mainImageAlt = mainImage?.alt || articleTitle;
                
                const summaryP = document.querySelector('article > p.font-jakarta.font-medium');
                const summary = summaryP?.innerHTML || '';
                
                const contentSection = document.querySelector('section.space-y-6, section.order-1');
                const bodyContent = contentSection?.innerHTML || '';
                
                try {
                    const printWindow = window.open('', '_blank');
                    if (printWindow) {
                        printWindow.document.write(`
                            <html>
                                <head>
                                    <title>${articleTitle}</title>
                                    <style>
                                        @media print {
                                            body { font-family: Arial, sans-serif; margin: 40px; max-width: 800px; }
                                            img { max-width: 100%; height: auto; margin: 20px 0; }
                                            .main-image { width: 100%; max-height: 400px; object-fit: cover; margin-bottom: 20px; }
                                            h1 { color: #017AFF; font-size: 32px; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #017AFF; }
                                            .summary { font-size: 18px; color: #636363; margin-bottom: 30px; line-height: 1.6; }
                                            h2 { color: #333; margin-top: 30px; font-size: 24px; }
                                            h3 { color: #333; margin-top: 20px; font-size: 20px; }
                                            p { line-height: 1.6; margin-bottom: 15px; }
                                        }
                                        body { font-family: Arial, sans-serif; margin: 40px; max-width: 800px; }
                                        img { max-width: 100%; height: auto; margin: 20px 0; }
                                        .main-image { width: 100%; max-height: 400px; object-fit: cover; margin-bottom: 20px; }
                                        h1 { color: #017AFF; font-size: 32px; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #017AFF; }
                                        .summary { font-size: 18px; color: #636363; margin-bottom: 30px; line-height: 1.6; }
                                        h2 { color: #333; margin-top: 30px; font-size: 24px; }
                                        h3 { color: #333; margin-top: 20px; font-size: 20px; }
                                        p { line-height: 1.6; margin-bottom: 15px; }
                                    </style>
                                </head>
                                <body>
                                    ${mainImageUrl ? `<img src="${mainImageUrl}" alt="${mainImageAlt}" class="main-image" />` : ''}
                                    <h1>${articleTitle}</h1>
                                    ${summary ? `<div class="summary">${summary}</div>` : ''}
                                    <div class="content">
                                        ${bodyContent}
                                    </div>
                                </body>
                            </html>
                        `);
                        printWindow.document.close();
                        
                        setTimeout(() => {
                            printWindow.print();
                            printWindow.close();
                        }, 1000);
                        
                        console.log('Print window opened successfully');
                    } else {
                        console.log('Failed to open print window, trying fallback');
                        fallbackDownload(articleTitle, mainImageUrl, mainImageAlt, summary, bodyContent);
                    }
                } catch (error) {
                    console.error('Print method failed:', error);
                    fallbackDownload(articleTitle, mainImageUrl, mainImageAlt, summary, bodyContent);
                }
            }
            
            function fallbackDownload(articleTitle, mainImageUrl, mainImageAlt, summary, bodyContent) {
                console.log('Using fallback download method');
                
                const htmlContent = `
                    <!DOCTYPE html>
                    <html>
                        <head>
                            <title>${articleTitle}</title>
                            <style>
                                body { font-family: Arial, sans-serif; margin: 40px; max-width: 800px; }
                                img { max-width: 100%; height: auto; margin: 20px 0; }
                                .main-image { width: 100%; max-height: 400px; object-fit: cover; margin-bottom: 20px; }
                                h1 { color: #017AFF; font-size: 32px; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #017AFF; }
                                .summary { font-size: 18px; color: #636363; margin-bottom: 30px; line-height: 1.6; }
                                h2 { color: #333; margin-top: 30px; font-size: 24px; }
                                h3 { color: #333; margin-top: 20px; font-size: 20px; }
                                p { line-height: 1.6; margin-bottom: 15px; }
                            </style>
                        </head>
                        <body>
                            ${mainImageUrl ? `<img src="${mainImageUrl}" alt="${mainImageAlt}" class="main-image" />` : ''}
                            <h1>${articleTitle}</h1>
                            ${summary ? `<div class="summary">${summary}</div>` : ''}
                            <div class="content">
                                ${bodyContent}
                            </div>
                        </body>
                    </html>
                `;
                
                const blob = new Blob([htmlContent], { type: 'text/html' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = articleTitle.replace(/[^a-z0-9]/gi, '_').toLowerCase() + '.html';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                console.log('HTML file download initiated');
            }
            
            // Share functionality - more specific selector
            const shareIcons = document.querySelectorAll('i.ph-share-network');
            shareIcons.forEach(icon => {
                const button = icon.closest('div');
                if (button) {
                    button.addEventListener('click', function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        const articleTitle = document.querySelector('h1')?.textContent || 'Check out this article';
                        const articleUrl = window.location.href;
                        const shareText = `${articleTitle} - ${articleUrl}`;
                        
                        // Check if Web Share API is supported and we're in a secure context
                        if (navigator.share && window.isSecureContext) {
                            navigator.share({
                                title: articleTitle,
                                url: articleUrl
                            }).catch(err => {
                                console.log('Share failed, falling back to clipboard');
                                fallbackToClipboard(shareText);
                            });
                        } else {
                            // Fallback: Copy to clipboard
                            fallbackToClipboard(shareText);
                        }
                    });
                }
            });
            
            function fallbackToClipboard(shareText) {
                if (navigator.clipboard && window.isSecureContext) {
                    navigator.clipboard.writeText(shareText).then(() => {
                        showNotification('Link copied to clipboard!');
                    }).catch(() => {
                        fallbackToTwitter(shareText);
                    });
                } else {
                    fallbackToTwitter(shareText);
                }
            }
            
            function fallbackToTwitter(shareText) {
                const shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}`;
                window.open(shareUrl, '_blank');
            }
            
            function showNotification(message) {
                const notification = document.createElement('div');
                notification.textContent = message;
                notification.style.cssText = `
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: #017AFF;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 5px;
                    z-index: 1000;
                    font-size: 14px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                `;
                document.body.appendChild(notification);
                setTimeout(() => notification.remove(), 3000);
            }
            
            // WhatsApp share functionality
            const whatsappButtons = document.querySelectorAll('img[alt="WhatsApp"]');
            whatsappButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const articleTitle = document.querySelector('h1')?.textContent || 'Check out this article';
                    const articleUrl = window.location.href;
                    const shareText = `${articleTitle} - ${articleUrl}`;
                    const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(shareText)}`;
                    window.open(whatsappUrl, '_blank');
                });
            });
            
            // Instagram share functionality (opens Instagram in new tab)
            const instagramButtons = document.querySelectorAll('img[alt="Instagram"]');
            instagramButtons.forEach(button => {
                button.addEventListener('click', function() {
                    window.open('https://www.instagram.com/', '_blank');
                });
            });
        }
    </script>
</body>

</html>"""


async def create_blog_html(data: str) -> str:
    l = []
    l.append(await getHeader())
    l.append(await get_blog_body(data))
    l.append(await get_more_blogs_section(data))
    l.append(await get_faq_section())
    l.append(await getFooter())

    l = EMPTY_BLOG_TEMPLATE.replace("[[total_body]]", "\n".join(l))

    return l


@router.get("/blog/{slug}")
async def get_blog(slug: str):
    """
    Render a blog post page by its slug
    Fetches blog data from database and renders it as HTML
    """
    print("=" * 80)
    print(f"[DEBUG] Blog endpoint called with slug: {slug}")
    print("=" * 80)
    
    try:
        print(f"[DEBUG] Attempting to connect to database...")
        conn = await asyncpg.connect(DATABASE_URL)
        print(f"[DEBUG] Database connection established")
        
        print(f"[DEBUG] Querying for blog with slug: {slug}")
        blog_record = await conn.fetchrow(
            """
            SELECT id, blog, status, date, category, slug, isDeleted
            FROM blogs
            WHERE slug = $1 AND isDeleted = FALSE
            """,
            slug
        )
        
        await conn.close()
        print(f"[DEBUG] Database connection closed")
        
        if not blog_record:
            print(f"[DEBUG] Blog not found for slug: {slug}")
            raise HTTPException(status_code=404, detail=f"Blog post not found: {slug}")
        
        print(f"[DEBUG] Blog found - Status: {blog_record['status']}")
        print(f"[DEBUG] Blog data type: {type(blog_record['blog'])}")
        print(f"[DEBUG] Blog data keys: {list(blog_record['blog'].keys()) if isinstance(blog_record['blog'], dict) else json.loads(blog_record['blog']).keys()}")
        
        if blog_record['status'] != 'published':
            print(f"[DEBUG] Blog is not published, status: {blog_record['status']}")
            raise HTTPException(status_code=404, detail="Blog post not available")
        
        blog_data = blog_record['blog'] if isinstance(blog_record['blog'], dict) else json.loads(blog_record['blog'])
        print(f"[DEBUG] Rendering blog HTML...")
        
        html_content = await create_blog_html(blog_data)
        print(f"[DEBUG] HTML generated successfully, length: {len(html_content)}")
        print("=" * 80)
        
        return HTMLResponse(html_content)
        
    except HTTPException:
        print(f"[DEBUG] HTTPException raised")
        raise
    except asyncpg.PostgresError as e:
        print(f"[DEBUG] Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        print(f"[DEBUG] Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/api/admin_blog_preview")
async def admin_blog_preview(request: Request):
    """
    Preview blog from admin panel
    Receives preview data from frontend and logs it to console
    Returns success response for frontend to handle preview rendering
    """
    try:
        data = await request.json()
        
        return {
            "status": "success",
            "message": "Preview data received and logged to console",
            "data": await create_blog_html(data)
        }
        
    except Exception as e:
        print(f"✗ Error in admin_blog_preview: {e}")
        raise HTTPException(status_code=500, detail=str(e))