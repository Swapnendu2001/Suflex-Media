document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger) {
        hamburger.addEventListener('click', function () {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        const links = navLinks.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', function () {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('.filter-btn');

    filterButtons.forEach(button => {
        button.addEventListener('click', function () {
            filterButtons.forEach(btn => btn.classList.remove('active'));

            this.classList.add('active');

            const filterValue = this.getAttribute('data-filter');

            console.log('Filter selected:', filterValue);

            const filterEvent = new CustomEvent('blogFilterChanged', {
                detail: { filter: filterValue }
            });
            document.dispatchEvent(filterEvent);
        });
    });
});

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

document.addEventListener('DOMContentLoaded', function () {
    renderBlogs('all', 1);

    document.addEventListener('blogFilterChanged', function (e) {
        currentFilter = e.detail.filter;
        currentPage = 1;
        renderBlogs(currentFilter, currentPage);
        updatePagination(currentPage);
    });

    const searchInput = document.getElementById('blogSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function (e) {
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

    const pageButtons = document.querySelectorAll('.page-number');
    pageButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            currentPage = parseInt(this.getAttribute('data-page'));
            renderBlogs(currentFilter, currentPage);
            updatePagination(currentPage);
        });
    });

    const nextBtn = document.getElementById('nextPageBtn');
    if (nextBtn) {
        nextBtn.addEventListener('click', function () {
            currentPage++;
            if (currentPage > 7) currentPage = 7;
            renderBlogs(currentFilter, currentPage);
            updatePagination(currentPage);
        });
    }
});