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

const blogsPerPage = 3;

function createBlogCard(blog) {
    return `
        <div class="blog-card" data-category="${blog.category}" onclick="window.location.href='/blog/${blog.id}'">
            <div class="blog-card-header">
                <div class="blog-dot" style="background-color: ${blogColors[blog.colorIndex % blogColors.length]}"></div>
                <span class="blog-read-time">${blog.readTime}</span>
            </div>
            <h3 class="blog-title">${blog.title}</h3>
            <p class="blog-date">${blog.date}</p>
            <div class="blog-footer">
                <p class.blog-description">${blog.description}</p>
                <div class="blog-arrow">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M5 12h14m-7-7l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
            </div>
        </div>
    `;
}

function renderSection(sectionId, paginationId, blogs, page) {
    const grid = document.getElementById(sectionId);
    const pagination = document.getElementById(paginationId);

    if (!grid || !pagination) return;

    const startIndex = (page - 1) * blogsPerPage;
    const endIndex = startIndex + blogsPerPage;
    const paginatedBlogs = blogs.slice(startIndex, endIndex);

    grid.innerHTML = paginatedBlogs.map(blog => createBlogCard(blog)).join('');

    const totalPages = Math.ceil(blogs.length / blogsPerPage);
    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }

    let paginationHTML = '';

    if (totalPages <= 4) {
        for (let i = 1; i <= totalPages; i++) {
            paginationHTML += `<button class="page-btn page-number ${i === page ? 'active' : ''}" data-page="${i}">${i}</button>`;
        }
    } else {
        paginationHTML += `<button class="page-btn page-number ${1 === page ? 'active' : ''}" data-page="1">1</button>`;

        if (page > 2) {
            paginationHTML += `<span class="page-dots">...</span>`;
        }

        if (page > 1 && page < totalPages) {
            paginationHTML += `<button class="page-btn page-number active" data-page="${page}">${page}</button>`;
        }

        if (page < totalPages - 1) {
            paginationHTML += `<span class="page-dots">...</span>`;
        }

        paginationHTML += `<button class="page-btn page-number ${totalPages === page ? 'active' : ''}" data-page="${totalPages}">${totalPages}</button>`;
    }

    pagination.innerHTML = paginationHTML;
}

document.addEventListener('DOMContentLoaded', function () {
    const latestGossipsBlogs = sampleBlogs.slice(0, 12);
    const editorsChoiceBlogs = sampleBlogs.slice(0, 12);

    let latestGossipsPage = 1;
    let editorsChoicePage = 1;

    renderSection('latest-gossips-grid', 'latest-gossips-pagination', latestGossipsBlogs, latestGossipsPage);
    renderSection('editors-choice-grid', 'editors-choice-pagination', editorsChoiceBlogs, editorsChoicePage);

    document.getElementById('latest-gossips-pagination').addEventListener('click', function (e) {
        if (e.target.classList.contains('page-btn')) {
            latestGossipsPage = parseInt(e.target.dataset.page);
            renderSection('latest-gossips-grid', 'latest-gossips-pagination', latestGossipsBlogs, latestGossipsPage);
        }
    });

    document.getElementById('editors-choice-pagination').addEventListener('click', function (e) {
        if (e.target.classList.contains('page-btn')) {
            editorsChoicePage = parseInt(e.target.dataset.page);
            renderSection('editors-choice-grid', 'editors-choice-pagination', editorsChoiceBlogs, editorsChoicePage);
        }
    });
});