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

const blogColors = ['#22c5e', '#ef4444', '#06b6d4', '#22c55e', '#eab308', '#3b82f6', '#22c55e', '#ec4899', '#06b6d4', '#eab308', '#a855f7', '#22c55e'];

const blogsPerPage = 9; // 9 blogs per page for the "Read More" section

function setupCarousel() {
    const carousel = document.getElementById('editors-choice-carousel');
    if (!carousel) return;

    const items = carousel.querySelectorAll('.blog-card');
    if (items.length === 0) return;

    // Clone items for a seamless loop
    items.forEach(item => {
        const clone = item.cloneNode(true);
        carousel.appendChild(clone);
    });

    carousel.addEventListener('mouseenter', () => {
        carousel.style.animationPlayState = 'paused';
    });

    carousel.addEventListener('mouseleave', () => {
        carousel.style.animationPlayState = 'running';
    });
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
        if (totalPages <= 5) {
            for (let i = 1; i <= totalPages; i++) {
                paginationHTML += `<button class="page-btn ${i === currentPage ? 'active' : ''}" data-page="${i}">${i}</button>`;
            }
        } else {
            if (currentPage > 1) {
                paginationHTML += `<button class="page-btn" data-page="${currentPage - 1}">Prev</button>`;
            }

            paginationHTML += `<button class="page-btn ${1 === currentPage ? 'active' : ''}" data-page="1">1</button>`;

            if (currentPage > 3) {
                paginationHTML += `<span class="page-dots">...</span>`;
            }

            if (currentPage > 2 && currentPage < totalPages - 1) {
                paginationHTML += `<button class="page-btn active" data-page="${currentPage}">${currentPage}</button>`;
            }

            if (currentPage < totalPages - 2) {
                paginationHTML += `<span class="page-dots">...</span>`;
            }

            paginationHTML += `<button class="page-btn ${totalPages === currentPage ? 'active' : ''}" data-page="${totalPages}">${totalPages}</button>`;

            if (currentPage < totalPages) {
                paginationHTML += `<button class="page-btn next-btn" data-page="${currentPage + 1}">Next page <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3.75 9H14.25" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 3.75L14.25 9L9 14.25" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>`;
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


document.addEventListener('DOMContentLoaded', function () {
    setupCarousel();
    setupPagination();
});