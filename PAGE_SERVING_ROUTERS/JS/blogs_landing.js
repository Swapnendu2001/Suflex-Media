document.addEventListener('DOMContentLoaded', function () {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger) {
        hamburger.addEventListener('click', function () {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        const links = navLinks.querySelectorAll('a:not(.dropdown-toggle)');
        links.forEach(link => {
            link.addEventListener('click', function () {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });
    }

    const dropdown = document.querySelector('.dropdown');
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    
    if (dropdown && dropdownToggle) {
        dropdownToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (window.innerWidth <= 768) {
                dropdown.classList.toggle('active');
            }
        });

        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 768 && !dropdown.contains(e.target)) {
                dropdown.classList.remove('active');
            }
        });
    }
    fetchBlogs();
});

const blogColors = ['#22c5e', '#ef4444', '#06b6d4', '#22c55e', '#eab308', '#3b82f6', '#22c55e', '#ec4899', '#06b6d4', '#eab308', '#a855f7', '#22c55e'];

const blogsPerPage = 9; // 9 blogs per page for the "Read More" section

function setupCarousel() {
    const carousel = document.getElementById('editors-choice-carousel');
    if (!carousel) return;

    const items = carousel.querySelectorAll('.editors-choice-card');
    const totalItems = items.length;
    if (totalItems <= 3) {
        const leftArrow = document.getElementById('carousel-arrow-left');
        const rightArrow = document.getElementById('carousel-arrow-right');
        if(leftArrow) leftArrow.style.display = 'none';
        if(rightArrow) rightArrow.style.display = 'none';
        return;
    };

    let currentIndex = 0;
    let autoScrollInterval;

    function updateCarousel() {
        const cardWidth = items[0].offsetWidth;
        const gap = parseFloat(window.getComputedStyle(carousel).columnGap) || 0;
        const offset = -currentIndex * (cardWidth + gap);
        carousel.style.transform = `translateX(${offset}px)`;
    }

    function showNext() {
        const maxIndex = totalItems - 3;
        currentIndex = (currentIndex + 1) > maxIndex ? 0 : currentIndex + 1;
        updateCarousel();
    }
    
    function showPrev() {
        const maxIndex = totalItems - 3;
        currentIndex = (currentIndex - 1) < 0 ? maxIndex : currentIndex - 1;
        updateCarousel();
    }

    function startAutoScroll() {
        stopAutoScroll();
        autoScrollInterval = setInterval(showNext, 3000);
    }

    function stopAutoScroll() {
        clearInterval(autoScrollInterval);
    }

    leftArrow.addEventListener('click', () => {
        stopAutoScroll();
        showPrev();
        startAutoScroll();
    });

    rightArrow.addEventListener('click', () => {
        stopAutoScroll();
        showNext();
        startAutoScroll();
    });

    carousel.parentElement.addEventListener('mouseenter', stopAutoScroll);
    carousel.parentElement.addEventListener('mouseleave', startAutoScroll);

    startAutoScroll();
    updateCarousel();
    window.addEventListener('resize', updateCarousel);
}


function setupMobileCarousel() {
    const mobileCarousel = document.getElementById('editors-choice-carousel-mobile');
    if (!mobileCarousel) return;

    const items = mobileCarousel.querySelectorAll('.blog-card');
    if (items.length <= 1) {
        const leftArrow = document.getElementById('carousel-arrow-left-mobile');
        const rightArrow = document.getElementById('carousel-arrow-right-mobile');
        if(leftArrow) leftArrow.style.display = 'none';
        if(rightArrow) rightArrow.style.display = 'none';
        return;
    }

    let currentIndex = 0;
    const totalItems = items.length;
    let autoScrollInterval;

    const leftArrow = document.getElementById('carousel-arrow-left-mobile');
    const rightArrow = document.getElementById('carousel-arrow-right-mobile');

    function updateCarousel() {
        const card = items[0];
        if (!card) return;
        const carouselStyle = window.getComputedStyle(mobileCarousel);
        const cardWidth = card.offsetWidth;
        const gap = parseFloat(carouselStyle.columnGap) || 0;
        const offset = -currentIndex * (cardWidth + gap);
        mobileCarousel.style.transform = `translateX(${offset}px)`;
    }

    function showNext() {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel();
    }
    
    function showPrev() {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateCarousel();
    }

    function startAutoScroll() {
        stopAutoScroll(); // Ensure no multiple intervals are running
        autoScrollInterval = setInterval(showNext, 3000); // Change slide every 3 seconds
    }

    function stopAutoScroll() {
        clearInterval(autoScrollInterval);
    }

    leftArrow.addEventListener('click', () => {
        stopAutoScroll();
        showPrev();
        startAutoScroll();
    });

    rightArrow.addEventListener('click', () => {
        stopAutoScroll();
        showNext();
        startAutoScroll();
    });

    // Start auto-scrolling
    startAutoScroll();
    
    // Pause on hover
    mobileCarousel.addEventListener('mouseenter', stopAutoScroll);
    mobileCarousel.addEventListener('mouseleave', startAutoScroll);

    // Initial call
    updateCarousel();
    window.addEventListener('resize', updateCarousel);
}


function setupPagination() {
    const grid = document.getElementById('read-more-grid');
    const pagination = document.getElementById('read-more-pagination');
    if (!grid || !pagination) return;

    const allBlogs = Array.from(grid.querySelectorAll('.blog-card'));
    const totalBlogs = allBlogs.length;
    const totalPages = Math.ceil(totalBlogs / blogsPerPage);
    let currentPage = 1;

    if (totalBlogs <= blogsPerPage) {
        pagination.style.display = 'none';
        return;
    }

    function showPage(page) {
        allBlogs.forEach((blog, index) => {
            const startIndex = (page - 1) * blogsPerPage;
            const endIndex = startIndex + blogsPerPage;
            if (index >= startIndex && index < endIndex) {
                blog.style.display = 'flex';
            } else {
                blog.style.display = 'none';
            }
        });
    }

    function createPaginationControls() {
        let paginationHTML = '';
        
        if (totalPages <= 1) {
            pagination.style.display = 'none';
            return;
        }
        
        if (totalPages <= 5) {
            for (let i = 1; i <= totalPages; i++) {
                paginationHTML += `<button class="page-btn ${i === currentPage ? 'active' : ''}" data-page="${i}">${i}</button>`;
            }
        } else {
            if (currentPage > 1) {
                paginationHTML += `<button class="page-btn" data-page="${currentPage - 1}">Prev</button>`;
            }

            const showPages = new Set();
            
            if (currentPage > 1) {
                showPages.add(currentPage - 1);
            }
            showPages.add(currentPage);
            if (currentPage < totalPages) {
                showPages.add(currentPage + 1);
            }
            showPages.add(totalPages);
            
            const sortedPages = Array.from(showPages).sort((a, b) => a - b);
            
            let prevPage = 0;
            sortedPages.forEach(page => {
                if (prevPage > 0 && page > prevPage + 1) {
                    paginationHTML += `<span class="page-dots">...</span>`;
                }
                paginationHTML += `<button class="page-btn ${page === currentPage ? 'active' : ''}" data-page="${page}">${page}</button>`;
                prevPage = page;
            });

            if (currentPage < totalPages) {
                paginationHTML += `<button class="page-btn next-btn" data-page="${currentPage + 1}">Next <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3.75 9H14.25" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 3.75L14.25 9L9 14.25" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>`;
            }
        }
        pagination.innerHTML = paginationHTML;
    }

    function updatePage(page) {
        currentPage = page;
        showPage(currentPage);
        createPaginationControls();
    }

    pagination.addEventListener('click', function (e) {
        if (e.target.classList.contains('page-btn') && e.target.dataset.page) {
            const page = parseInt(e.target.dataset.page);
            updatePage(page);
        }
    });

    showPage(1);
    createPaginationControls();
}

function renderEditorsChoice(blogs) {
    const container = document.getElementById('dynamic-editors-choice-content');
    if (!container) return;

    container.innerHTML = blogs.map(blog => {
        let blogData = {};
        try {
            blogData = typeof blog.blog === 'string' ? JSON.parse(blog.blog) : blog.blog;
        } catch (e) {
            console.error('Error parsing blog data:', e, blog.blog);
        }
        return `
        <div class="editors-choice-card" onclick="window.location.href='/blog/${blog.slug}'">
            <div class="editors-choice-card-image-container">
                <img src="${blogData.blogTitleImage}" alt="${blogData.blogTitle}" class="editors-choice-card-image">
            </div>
            <div class="editors-choice-card-content">
                <h3 class="blog-title">${blogData.blogTitle}</h3>
                <p class="blog-summary">${blogData.blogSummary}</p>
                <div class="blog-footer">
                    <span class="blog-date">${new Date(blog.date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })} • ${blog.category}</span>
                </div>
            </div>
        </div>
    `}).join('');
    setupCarousel();
}

function renderLatestGossip(blogs) {
    const container = document.getElementById('dynamic-latest-gossip-content');
    if (!container) return;
    container.innerHTML = blogs.map((blog, index) => renderBlogCard(blog, index)).join('');
}

function renderReadMore(blogs) {
    const container = document.getElementById('dynamic-read-more-content');
    if (!container) return;
    container.innerHTML = blogs.map((blog, index) => renderBlogCard(blog, index)).join('');
    setupPagination();
}

function renderBlogCard(blog, index) {
    const color = blogColors[index % blogColors.length];
    let blogData = {};
    try {
        blogData = typeof blog.blog === 'string' ? JSON.parse(blog.blog) : blog.blog;
    } catch (e) {
        console.error('Error parsing blog data:', e, blog.blog);
    }

    const readTime = blogData.readTime || '5 mins read';
    const title = blogData.blogTitle || 'No Title';
    const summary = blogData.blogSummary || '';

    return `
        <div class="blog-card" onclick="window.location.href='/blog/${blog.slug}'">
            <div class="blog-card-header">
                <div class="blog-dot" style="background-color: ${color};"></div>
                <span class="blog-read-time">${readTime}</span>
            </div>
            <h2 class="blog-title">${title}</h2>
            <p class="blog-date">${new Date(blog.date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })} • ${blog.category}</p>
            <div class="blog-footer">
                <p class="blog-description">${summary}</p>
                <a href="/blog/${blog.slug}" class="blog-arrow-link">
                    <div class="blog-arrow">
                        <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"></path></svg>
                    </div>
                </a>
            </div>
        </div>
    `;
}

async function fetchBlogs() {
    try {
        const response = await fetch('/api/blogs?purpose=landing_page');
        const data = await response.json();
        if (data.status === 'success' && data.sections) {
            renderEditorsChoice(data.sections.editors_choice);
            renderLatestGossip(data.sections.latest_gossip);
            renderReadMore(data.sections.read_more);
            
            const mobileCarousel = document.getElementById('editors-choice-carousel-mobile');
            if (mobileCarousel) {
                mobileCarousel.innerHTML = data.sections.editors_choice.map((blog, index) => renderBlogCard(blog, index)).join('');
                setupMobileCarousel();
            }
        }
    } catch (error) {
        console.error('Error fetching blogs:', error);
    }
}