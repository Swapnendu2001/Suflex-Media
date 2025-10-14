def blogs_list_section_html():
    return '''
<section class="blogs-list-section">
    <div class="search-wrapper">
        <div class="search-container">
            <input type="text" class="search-input" placeholder="Search" id="blogSearch">
            <svg class="search-icon" width="18" height="18" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 17A8 8 0 1 0 9 1a8 8 0 0 0 0 16zM18 18l-4.35-4.35" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
    </div>
    
    <div class="blogs-grid" id="blogsGrid">
        <!-- Blog cards will be dynamically inserted here -->
    </div>
    
    <div class="pagination-container">
        <div class="pagination-buttons">
            <button class="page-btn page-number active" data-page="1">1</button>
            <button class="page-btn page-number" data-page="2">2</button>
            <button class="page-btn page-number" data-page="3">3</button>
            <button class="page-btn page-number" data-page="4">4</button>
            <span class="page-dots">...</span>
            <button class="page-btn page-number" data-page="7">7</button>
            <button class="page-btn next-btn" id="nextPageBtn">
                Next page
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M7.5 15l5-5-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </button>
        </div>
    </div>
</section>
'''

def blogs_list_section_css():
    return '''
<style>
    .blogs-list-section {
        background-color: #f8f9fa;
        padding: 8vh 5vw 10vh 5vw;
        display: flex;
        flex-direction: column;
        align-items: center;
        font-family: 'Lexend', sans-serif;
        width: 100%;
        max-width: 100vw;
        box-sizing: border-box;
        overflow-x: hidden;
    }
    
    .search-wrapper {
        width: 85vw;
        display: flex;
        justify-content: flex-end;
        margin-bottom: 4vh;
    }
    
    .search-container {
        position: relative;
        width: 20vw;
    }
    
    .search-input {
        width: 100%;
        padding: 1vh 3vw 1vh 1.2vw;
        font-size: 0.9vw;
        font-family: 'Lexend', sans-serif;
        border: 0.15vw solid #e0e0e0;
        border-radius: 2vw;
        background-color: #fff;
        transition: border-color 0.3s ease;
    }
    
    .search-input:focus {
        outline: none;
        border-color: #007bff;
    }
    
    .search-input::placeholder {
        color: #999;
    }
    
    .search-icon {
        position: absolute;
        right: 1.2vw;
        top: 50%;
        transform: translateY(-50%);
        color: #999;
        width: 1.2vw;
        height: 1.2vw;
        pointer-events: none;
    }
    
    .blogs-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 3vw;
        width: 85vw;
        margin: 0 auto 6vh auto;
    }
    
    .blog-card {
        background-color: #fff;
        border: 0.15vw solid #007bff;
        border-radius: 1.5vw;
        padding: 2vw;
        display: flex;
        flex-direction: column;
        gap: 1.5vh;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
    }
    
    .blog-card:hover {
        transform: translateY(-1vh);
        box-shadow: 0 1vh 2vw rgba(0, 123, 255, 0.15);
    }
    
    .blog-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }
    
    .blog-dot {
        width: 1.5vw;
        height: 1.5vw;
        border-radius: 50%;
        flex-shrink: 0;
    }
    
    .blog-read-time {
        font-size: 0.9vw;
        color: #666;
        white-space: nowrap;
    }
    
    .blog-title {
        font-size: 1.4vw;
        font-weight: 600;
        color: #000;
        margin: 0;
        line-height: 1.3;
    }
    
    .blog-date {
        font-size: 0.85vw;
        color: #999;
        margin: 0;
    }
    
    .blog-description {
        font-size: 1vw;
        color: #333;
        line-height: 1.5;
        margin: 0;
        flex-grow: 1;
    }
    
    .blog-arrow {
        width: 3vw;
        height: 3vw;
        border-radius: 50%;
        border: 0.15vw solid #000;
        background-color: transparent;
        display: flex;
        align-items: center;
        justify-content: center;
        align-self: flex-end;
        transition: all 0.3s ease;
    }
    
    .blog-card:hover .blog-arrow {
        border-color: #007bff;
        background-color: #007bff;
        transform: scale(1.1);
    }
    
    .blog-arrow svg {
        width: 1.5vw;
        height: 1.5vw;
        stroke: #000;
        stroke-width: 0.15vw;
        fill: none;
        transition: stroke 0.3s ease;
    }
    
    .blog-card:hover .blog-arrow svg {
        stroke: #fff;
    }
    
    .pagination-container {
        display: flex;
        justify-content: center;
        margin-top: 4vh;
    }
    
    .pagination-buttons {
        display: flex;
        align-items: center;
        gap: 1vw;
    }
    
    .page-btn {
        background-color: #e8e8e8;
        color: #333;
        border: none;
        border-radius: 0.5vw;
        padding: 1.2vh 1.5vw;
        font-size: 1vw;
        font-family: 'Lexend', sans-serif;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .page-btn:hover:not(.active) {
        background-color: #d0d0d0;
    }
    
    .page-btn.active {
        background-color: #007bff;
        color: #fff;
    }
    
    .page-dots {
        color: #666;
        font-size: 1.2vw;
        padding: 0 0.5vw;
    }
    
    .next-btn {
        background-color: #007bff;
        color: #fff;
        display: flex;
        align-items: center;
        gap: 0.5vw;
        padding: 1.2vh 2vw;
    }
    
    .next-btn:hover {
        background-color: #0056b3;
    }
    
    .next-btn svg {
        width: 1.2vw;
        height: 1.2vw;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .blogs-list-section {
            padding: 6vh 5vw 8vh 5vw;
        }
        
        .search-wrapper {
            width: 90vw;
            justify-content: center;
            margin-bottom: 4vh;
        }
        
        .search-container {
            width: 70vw;
        }
        
        .search-input {
            padding: 2vh 15vw 2vh 4vw;
            font-size: 3.5vw;
            border-radius: 0.5vw;
            border-width: 0.3vw;
        }
        
        .search-icon {
            right: 4vw;
            width: 5vw;
            height: 5vw;
        }
        
        .blogs-grid {
            grid-template-columns: 1fr;
            gap: 4vw;
            width: 90vw;
            margin-bottom: 4vh;
        }
        
        .blog-card {
            border-radius: 4vw;
            padding: 5vw;
            gap: 2vh;
            border-width: 0.3vw;
        }
        
        .blog-dot {
            width: 4vw;
            height: 4vw;
        }
        
        .blog-read-time {
            font-size: 3vw;
        }
        
        .blog-title {
            font-size: 4.5vw;
        }
        
        .blog-date {
            font-size: 3vw;
        }
        
        .blog-description {
            font-size: 3.5vw;
        }
        
        .blog-arrow {
            width: 10vw;
            height: 10vw;
            border-width: 0.4vw;
        }
        
        .blog-arrow svg {
            width: 5vw;
            height: 5vw;
            stroke-width: 0.4vw;
        }
        
        .pagination-buttons {
            gap: 2vw;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .page-btn {
            padding: 1.5vh 4vw;
            font-size: 3.5vw;
            border-radius: 2vw;
        }
        
        .page-dots {
            font-size: 4vw;
        }
        
        .next-btn {
            padding: 1.5vh 5vw;
            gap: 2vw;
        }
        
        .next-btn svg {
            width: 4vw;
            height: 4vw;
        }
    }
</style>

<script>
    // Sample blog data - Replace with actual API call
    const blogColors = ['#22c55e', '#ef4444', '#06b6d4', '#22c55e', '#eab308', '#3b82f6', '#22c55e', '#ec4899', '#06b6d4', '#eab308', '#a855f7', '#22c55e'];
    
    const sampleBlogs = [
        {
            id: 1,
            title: 'What happened to Zomato Losses?',
            date: 'mediamuscle, March 5, 2025',
            description: 'Marketing is the art of connecting products with people. It involves understanding...',
            readTime: '5 mins read',
            category: 'all',
            colorIndex: 0
        },
        {
            id: 2,
            title: 'What happened to Zomato Losses?',
            date: 'mediamuscle, March 5, 2025',
            description: 'Marketing is the art of connecting products with people. It involves understanding...',
            readTime: '5 mins read',
            category: 'linkedin-prospecting',
            colorIndex: 1
        },
        {
            id: 3,
            title: 'What happened to Zomato Losses?',
            date: 'mediamuscle, March 5, 2025',
            description: 'Marketing is the art of connecting products with people. It involves understanding...',
            readTime: '5 mins read',
            category: 'linkedin-scraping',
            colorIndex: 2
        },
        {
            id: 4,
            title: 'What happened to Zomato Losses?',
            date: 'mediamuscle, March 5, 2025',
            description: 'Marketing is the art of connecting products with people. It involves understanding...',
            readTime: '5 mins read',
            category: 'sales-tools',
            colorIndex: 3
        },
        {
            id: 5,
            title: 'What happened to Zomato Losses?',
            date: 'mediamuscle, March 5, 2025',
            description: 'Marketing is the art of connecting products with people. It involves understanding...',
            readTime: '5 mins read',
            category: 'cold-email',
            colorIndex: 4
        },
        {
            id: 6,
            title: 'What happened to Zomato Losses?',
            date: 'mediamuscle, March 5, 2025',
            description: 'Marketing is the art of connecting products with people. It involves understanding...',
            readTime: '5 mins read',
            category: 'linkedin-plans',
            colorIndex: 5
        },
        {
            id: 7,
            title: 'What happened to Zomato Losses?',
            date: 'mediamuscle, March 5, 2025',
            description: 'Marketing is the art of connecting products with people. It involves understanding...',
            readTime: '5 mins read',
            category: 'linkedin-networking',
            colorIndex: 6
        },
        {
            id: 8,
            title: 'What happened to Zomato Losses?',
            date: 'mediamuscle, March 5, 2025',
            description: 'Marketing is the art of connecting products with people. It involves understanding...',
            readTime: '5 mins read',
            category: 'linkedin-marketing',
            colorIndex: 7
        },
        {
            id: 9,
            title: 'What happened to Zomato Losses?',
            date: 'mediamuscle, March 5, 2025',
            description: 'Marketing is the art of connecting products with people. It involves understanding...',
            readTime: '5 mins read',
            category: 'linkedin-automation',
            colorIndex: 8
        },
        {
            id: 10,
            title: 'What happened to Zomato Losses?',
            date: 'mediamuscle, March 5, 2025',
            description: 'Marketing is the art of connecting products with people. It involves understanding...',
            readTime: '5 mins read',
            category: 'email-deliverability',
            colorIndex: 9
        },
        {
            id: 11,
            title: 'What happened to Zomato Losses?',
            date: 'mediamuscle, March 5, 2025',
            description: 'Marketing is the art of connecting products with people. It involves understanding...',
            readTime: '5 mins read',
            category: 'b2b-lead-generation',
            colorIndex: 10
        },
        {
            id: 12,
            title: 'What happened to Zomato Losses?',
            date: 'mediamuscle, March 5, 2025',
            description: 'Marketing is the art of connecting products with people. It involves understanding...',
            readTime: '5 mins read',
            category: 'all',
            colorIndex: 11
        }
    ];
    
    let currentFilter = 'all';
    let currentPage = 1;
    const blogsPerPage = 9;
    
    function createBlogCard(blog) {
        return `
            <div class="blog-card" data-category="${blog.category}" onclick="window.location.href='/blog/${blog.id}'">
                <div class="blog-card-header">
                    <div class="blog-dot" style="background-color: ${blogColors[blog.colorIndex % blogColors.length]}"></div>
                    <span class="blog-read-time">${blog.readTime}</span>
                </div>
                <h3 class="blog-title">${blog.title}</h3>
                <p class="blog-date">${blog.date}</p>
                <p class="blog-description">${blog.description}</p>
                <div class="blog-arrow">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M5 12h14m-7-7l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
            </div>
        `;
    }
    
    function renderBlogs(filter = 'all', page = 1) {
        const blogsGrid = document.getElementById('blogsGrid');
        if (!blogsGrid) return;
        
        let filteredBlogs = sampleBlogs;
        if (filter !== 'all') {
            filteredBlogs = sampleBlogs.filter(blog => blog.category === filter);
        }
        
        const startIndex = (page - 1) * blogsPerPage;
        const endIndex = startIndex + blogsPerPage;
        const paginatedBlogs = filteredBlogs.slice(startIndex, endIndex);
        
        blogsGrid.innerHTML = paginatedBlogs.map(blog => createBlogCard(blog)).join('');
    }
    
    function updatePagination(currentPage) {
        const pageButtons = document.querySelectorAll('.page-number');
        pageButtons.forEach(btn => {
            const page = parseInt(btn.getAttribute('data-page'));
            if (page === currentPage) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        // Initial render
        renderBlogs('all', 1);
        
        // Listen for filter changes
        document.addEventListener('blogFilterChanged', function(e) {
            currentFilter = e.detail.filter;
            currentPage = 1;
            renderBlogs(currentFilter, currentPage);
            updatePagination(currentPage);
        });
        
        // Search functionality
        const searchInput = document.getElementById('blogSearch');
        if (searchInput) {
            searchInput.addEventListener('input', function(e) {
                const searchTerm = e.target.value.toLowerCase();
                const blogCards = document.querySelectorAll('.blog-card');
                
                blogCards.forEach(card => {
                    const title = card.querySelector('.blog-title').textContent.toLowerCase();
                    const description = card.querySelector('.blog-description').textContent.toLowerCase();
                    
                    if (title.includes(searchTerm) || description.includes(searchTerm)) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        }
        
        // Pagination
        const pageButtons = document.querySelectorAll('.page-number');
        pageButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                currentPage = parseInt(this.getAttribute('data-page'));
                renderBlogs(currentFilter, currentPage);
                updatePagination(currentPage);
            });
        });
        
        // Next button
        const nextBtn = document.getElementById('nextPageBtn');
        if (nextBtn) {
            nextBtn.addEventListener('click', function() {
                currentPage++;
                if (currentPage > 7) currentPage = 7; // Max page
                renderBlogs(currentFilter, currentPage);
                updatePagination(currentPage);
            });
        }
    });
</script>
'''
