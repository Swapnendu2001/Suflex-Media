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

const blogColors = ['#22c55e', '#ef4444', '#06b6d4', '#2c55e', '#eab308', '#3b82f6', '#22c55e', '#ec489', '#06b6d4', '#eab308', '#a855f7', '#22c55e'];

const blogsPerPage = 3;

// Function to handle pagination for server-rendered content
function setupPagination(sectionId, paginationId) {
    const grid = document.getElementById(sectionId);
    const pagination = document.getElementById(paginationId);
    const allBlogs = grid.querySelectorAll('.blog-card');
    const totalBlogs = allBlogs.length;
    const totalPages = Math.ceil(totalBlogs / blogsPerPage);
    let currentPage = 1;

    // If there are no blogs or only 3 or fewer, hide pagination
    if (totalBlogs <= blogsPerPage) {
        pagination.innerHTML = '';
        return;
    }

    // Show first 3 blogs initially, hide the rest
    showPage(currentPage);

    // Create pagination controls
    createPaginationControls(paginationId, totalPages, currentPage);
}

function showPage(page) {
    const latestGrid = document.getElementById('latest-gossips-grid');
    const editorsGrid = document.getElementById('editors-choice-grid');
    const allLatestBlogs = latestGrid.querySelectorAll('.blog-card');
    const allEditorsBlogs = editorsGrid.querySelectorAll('.blog-card');

    // Show/hide blogs for latest gossips section
    allLatestBlogs.forEach((blog, index) => {
        const startIndex = (page - 1) * blogsPerPage;
        const endIndex = startIndex + blogsPerPage;
        if (index >= startIndex && index < endIndex) {
            blog.style.display = 'flex';
        } else {
            blog.style.display = 'none';
        }
    });

    // Show/hide blogs for editor's choice section
    allEditorsBlogs.forEach((blog, index) => {
        const startIndex = (page - 1) * blogsPerPage;
        const endIndex = startIndex + blogsPerPage;
        if (index >= startIndex && index < endIndex) {
            blog.style.display = 'flex';
        } else {
            blog.style.display = 'none';
        }
    });
}

function createPaginationControls(paginationId, totalPages, currentPage) {
    const pagination = document.getElementById(paginationId);
    if (!pagination) return;

    let paginationHTML = '';

    if (totalPages <= 4) {
        for (let i = 1; i <= totalPages; i++) {
            paginationHTML += `<button class="page-btn page-number ${i === currentPage ? 'active' : ''}" data-page="${i}">${i}</button>`;
        }
    } else {
        paginationHTML += `<button class="page-btn page-number ${1 === currentPage ? 'active' : ''}" data-page="1">1</button>`;

        if (currentPage > 2) {
            paginationHTML += `<span class="page-dots">...</span>`;
        }

        if (currentPage > 1 && currentPage < totalPages) {
            paginationHTML += `<button class="page-btn page-number ${currentPage === currentPage ? 'active' : ''}" data-page="${currentPage}">${currentPage}</button>`;
        }

        if (currentPage < totalPages - 1) {
            paginationHTML += `<span class="page-dots">...</span>`;
        }

        paginationHTML += `<button class="page-btn page-number ${totalPages === currentPage ? 'active' : ''}" data-page="${totalPages}">${totalPages}</button>`;
    }

    pagination.innerHTML = paginationHTML;
}

document.addEventListener('DOMContentLoaded', function () {
    // Set up pagination for both sections after the page loads
    setupPagination('latest-gossips-grid', 'latest-gossips-pagination');
    setupPagination('editors-choice-grid', 'editors-choice-pagination');

    // Add event listeners for pagination buttons
    document.getElementById('latest-gossips-pagination').addEventListener('click', function (e) {
        if (e.target.classList.contains('page-btn') && e.target.dataset.page) {
            const page = parseInt(e.target.dataset.page);
            updatePage('latest-gossips-grid', 'latest-gossips-pagination', page);
        }
    });

    document.getElementById('editors-choice-pagination').addEventListener('click', function (e) {
        if (e.target.classList.contains('page-btn') && e.target.dataset.page) {
            const page = parseInt(e.target.dataset.page);
            updatePage('editors-choice-grid', 'editors-choice-pagination', page);
        }
    });
});

function updatePage(gridId, paginationId, page) {
    showPage(page);
    const allBlogs = document.getElementById(gridId).querySelectorAll('.blog-card');
    const totalBlogs = allBlogs.length;
    const totalPages = Math.ceil(totalBlogs / blogsPerPage);
    createPaginationControls(paginationId, totalPages, page);
}