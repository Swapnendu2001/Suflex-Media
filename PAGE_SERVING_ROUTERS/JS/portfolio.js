let currentPage = 1;
let totalPages = 1;
const perPage = 4;

function cleanHtml(htmlText) {
    if (!htmlText) return '';
    
    const temp = document.createElement('div');
    temp.innerHTML = htmlText;
    const text = temp.textContent || temp.innerText || '';
    return text.trim();
}

function generateCaseStudyCard(caseStudy, index) {
    const preview = caseStudy.preview || {};
    const slug = caseStudy.slug || '';
    
    const imageUrl = preview.imageUrl || '/images/Frame1.jpg';
    const imageAlt = preview.imageAlt || 'Case Study';
    const blogTitle = preview.blogTitle || 'Untitled Case Study';
    const text = cleanHtml(preview.text || '');
    const projectSnapshots = preview.projectSnapshots || [];
    
    let snapshotsHtml = '';
    if (projectSnapshots.length > 0) {
        snapshotsHtml = "<ul style='margin: 10px 0; padding-left: 20px;'>";
        projectSnapshots.forEach(snapshot => {
            const cleanedSnapshot = cleanHtml(snapshot);
            if (cleanedSnapshot) {
                snapshotsHtml += `<li style='margin: 5px 0;'>${cleanedSnapshot}</li>`;
            }
        });
        snapshotsHtml += "</ul>";
    }
    
    const cardClass = index % 2 === 0 ? 'case-study-card-light' : 'dark';
    
    return `
        <div class="case-study-card ${cardClass}">
            <div class="case-study-image">
                <img src="${imageUrl}" alt="${imageAlt}">
            </div>
            <div class="case-study-content">
                <h3 class="case-study-title">${blogTitle}</h3>
                <p class="case-study-description">${text}</p>
                ${snapshotsHtml ? `<div class="case-study-description">${snapshotsHtml}</div>` : ''}
                <a href="/case-study/${slug}" class="read-more-link">Read More</a>
            </div>
        </div>
    `;
}

function renderCaseStudies(caseStudies, startIndex = 0) {
    const container = document.getElementById('caseStudyContainer');
    if (!container) return;
    
    let html = '';
    caseStudies.forEach((caseStudy, idx) => {
        html += generateCaseStudyCard(caseStudy, startIndex + idx);
    });
    
    container.innerHTML = html;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function generatePaginationButtons() {
    const paginationContainer = document.getElementById('paginationContainer');
    if (!paginationContainer) return;
    
    let html = '';
    
    const maxVisible = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
    let endPage = Math.min(totalPages, startPage + maxVisible - 1);
    
    if (endPage - startPage < maxVisible - 1) {
        startPage = Math.max(1, endPage - maxVisible + 1);
    }
    
    if (startPage > 1) {
        html += `<button class="pagination-btn" data-page="1">1</button>`;
        if (startPage > 2) {
            html += `<span class="pagination-dots">...</span>`;
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        const activeClass = i === currentPage ? 'active' : '';
        html += `<button class="pagination-btn ${activeClass}" data-page="${i}">${i}</button>`;
    }
    
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            html += `<span class="pagination-dots">...</span>`;
        }
        html += `<button class="pagination-btn" data-page="${totalPages}">${totalPages}</button>`;
    }
    
    if (currentPage < totalPages) {
        html += `<button class="pagination-btn next-btn" data-page="${currentPage + 1}">Next page →</button>`;
    }
    
    paginationContainer.innerHTML = html;
    
    const buttons = paginationContainer.querySelectorAll('.pagination-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const page = parseInt(this.getAttribute('data-page'));
            if (page && page !== currentPage) {
                loadPage(page);
            }
        });
    });
}

async function loadPage(page) {
    try {
        const response = await fetch(`/api/case-studies/paginated?page=${page}&per_page=${perPage}`);
        const data = await response.json();
        
        if (data.status === 'success') {
            currentPage = data.page;
            totalPages = data.total_pages;
            
            const startIndex = (currentPage - 1) * perPage;
            renderCaseStudies(data.case_studies, startIndex);
            generatePaginationButtons();
        }
    } catch (error) {
        console.error('Error loading case studies:', error);
    }
}

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
    
    const totalPagesElement = document.getElementById('totalPages');
    if (totalPagesElement) {
        totalPages = parseInt(totalPagesElement.textContent) || 1;
        totalPagesElement.remove();
    }
    
    generatePaginationButtons();
});