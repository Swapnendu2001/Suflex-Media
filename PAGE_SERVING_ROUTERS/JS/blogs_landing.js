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



function setupPagination() {
    const grid = document.getElementById('read-more-grid');
    const pagination = document.getElementById('read-more-pagination');
    if (!grid || !pagination) return;

    const allBlogs = Array.from(grid.querySelectorAll('.blog-card-unified'));
    const totalBlogs = allBlogs.length;
    const totalPages = Math.ceil(totalBlogs / blogsPerPage);
    let currentPage = 1;

    if (totalBlogs <= blogsPerPage) {
        pagination.style.display = 'none';
        allBlogs.forEach(blog => blog.style.display = 'flex');
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
        
        const section = document.querySelector('.read-more-section');
        if (section) {
            section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    function createPaginationControls() {
        let paginationHTML = '';
        
        if (totalPages <= 1) {
            pagination.style.display = 'none';
            return;
        }
        
        pagination.style.display = 'flex';
        
        if (totalPages <= 5) {
            for (let i = 1; i <= totalPages; i++) {
                paginationHTML += `<button class="page-btn ${i === currentPage ? 'active' : ''}" data-page="${i}">${i}</button>`;
            }
        } else {
            if (currentPage > 1) {
                paginationHTML += `<button class="page-btn prev-btn" data-page="${currentPage - 1}"><svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14.25 9H3.75" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 14.25L3.75 9L9 3.75" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Prev</button>`;
            }

            const showPages = new Set();
            
            showPages.add(1);
            if (currentPage > 1) {
                showPages.add(currentPage - 1);
            }
            showPages.add(currentPage);
            if (currentPage < totalPages) {
                showPages.add(currentPage + 1);
            }
            showPages.add(totalPages);
            
            const sortedPages = Array.from(showPages).sort((a, b) => a - b);
            
            let prevPageNum = 0;
            sortedPages.forEach(page => {
                if (prevPageNum > 0 && page > prevPageNum + 1) {
                    paginationHTML += `<span class="page-dots">...</span>`;
                }
                paginationHTML += `<button class="page-btn ${page === currentPage ? 'active' : ''}" data-page="${page}">${page}</button>`;
                prevPageNum = page;
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
        const btn = e.target.closest('.page-btn');
        if (btn && btn.dataset.page) {
            const page = parseInt(btn.dataset.page);
            updatePage(page);
        }
    });

    showPage(1);
    createPaginationControls();
}

function extractBlogImage(blog) {
    if (blog.coverImage) {
        return blog.coverImage;
    }
    
    const blogContent = blog.blogContent || blog;
    if (!blogContent) return null;
    
    if (blogContent.coverImage) {
        return blogContent.coverImage;
    }
    
    if (blogContent.mainImageUrl) {
        return blogContent.mainImageUrl;
    }
    
    if (blogContent.blogTitleImage) {
        return blogContent.blogTitleImage;
    }
    
    if (blogContent.blog_cover_image && blogContent.blog_cover_image.url) {
        return blogContent.blog_cover_image.url;
    }
    
    if (blogContent.blogcontent && blogContent.blogcontent.blocks) {
        for (const block of blogContent.blogcontent.blocks) {
            if (block.type === 'image' && block.data && block.data.file && block.data.file.url) {
                return block.data.file.url;
            }
        }
    }
    
    return null;
}

function renderEditorsChoice(blogs) {
    const container = document.getElementById('editors-choice-grid');
    if (!container) return;
    if (!blogs || blogs.length === 0) {
        setupPagination();
        return;
    }
    container.innerHTML = blogs.map(blog => renderBlogCard(blog, 0)).join('');
}

function renderLatestGossip(blogs) {
    const container = document.getElementById('latest-gossip-grid');
    if (!container) return;
    if (!blogs || blogs.length === 0) return;
    container.innerHTML = blogs.map((blog, index) => renderBlogCard(blog, index)).join('');
}

function renderReadMore(blogs) {
    const container = document.getElementById('read-more-grid');
    if (!container) return;
    if (!blogs || blogs.length === 0) {
        setupPagination();
        return;
    }
    container.innerHTML = blogs.map((blog, index) => renderBlogCard(blog, index)).join('');
    setupPagination();
}

function renderBlogCard(blog, index) {
    const blogData = blog.blogContent || {};
    const imageUrl = extractBlogImage(blog);
    const title = blogData.blogTitle || 'Untitled';
    const summary = blogData.blogSummary || '';
    const dateStr = new Date(blog.date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });

    return `
        <div class="blog-card-unified" onclick="window.location.href='/blog/${blog.slug}'">
            ${imageUrl ? `
            <div class="blog-card-image-container">
                <img src="${imageUrl}" alt="${title}" class="blog-card-image">
            </div>
            ` : ''}
            <div class="blog-card-body">
                <span class="blog-card-date">${dateStr}</span>
                <h3 class="blog-card-title">${title}</h3>
                <p class="blog-card-summary">${summary}</p>
                <a href="/blog/${blog.slug}" class="blog-card-read-more">Read More →</a>
            </div>
        </div>
    `;
}

async function fetchBlogs() {
    try {
        const response = await fetch('/api/blogs?purpose=landing_page');
        const data = await response.json();
        if (data.status === 'success' && data.sections) {
            renderEditorsChoice(data.sections.editors_choice || []);
            renderLatestGossip(data.sections.latest_gossip || []);
            renderReadMore(data.sections.read_more || []);
            
            const mobileGrid = document.getElementById('editors-choice-carousel-mobile');
            if (mobileGrid && data.sections.editors_choice && data.sections.editors_choice.length > 0) {
                mobileGrid.innerHTML = data.sections.editors_choice.map((blog, index) => renderBlogCard(blog, index)).join('');
            }
        }
    } catch (error) {
        console.error('Error fetching blogs:', error);
    }
}