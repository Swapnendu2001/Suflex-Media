function handleLogout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('adminToken');
    localStorage.removeItem('userSession');
    sessionStorage.clear();
    deleteCookie('hashed_email');
    deleteCookie('hashed_password');
    window.location.href = '/login';
}
function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
}

function showLoading(show) {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        if (show) {
            loadingOverlay.classList.remove('hidden');
        } else {
            loadingOverlay.classList.add('hidden');
        }
    }
}

async function verifyAuth() {
    const hashedEmail = getCookie('hashed_email');
    const hashedPassword = getCookie('hashed_password');
    
    if (!hashedEmail || !hashedPassword) {
        console.log("No credentials found, redirecting to login...");
        setTimeout(() => {
            window.location.href = "/login";
        }, 1000);
        return false;
    }

    try {
        console.log("Verifying stored credentials...");
        const res = await fetch("/api/auto-login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({
                hashed_email: hashedEmail,
                hashed_password: hashedPassword
            }),
            credentials: 'include'
        });

        if (!res.ok) {
            console.log("Authentication failed, clearing credentials...");
            deleteCookie('hashed_email');
            deleteCookie('hashed_password');
            setTimeout(() => {
                window.location.href = "/login";
            }, 1000);
            return false;
        }

        const data = await res.json().catch(() => null);
        if (data && data.status === "success") {
            console.log("✓ Authentication successful");
            showLoading(false);
            return true;
        } else {
            console.log("Invalid response, clearing credentials...");
            deleteCookie('hashed_email');
            deleteCookie('hashed_password');
            setTimeout(() => {
                window.location.href = "/login";
            }, 1000);
            return false;
        }
    } catch (err) {
        console.error("Error during authentication:", err);
        setTimeout(() => {
            window.location.href = "/login";
        }, 1000);
        return false;
    }
}

(function initAuth() {
    showLoading(true);
    verifyAuth();

let galleryState = {
    isCollapsed: false
};

function toggleGallerySection() {
    const leftSection = document.getElementById('leftSection');
    
    if (!leftSection) {
        console.error('❌ [Gallery Toggle] Left section not found');
        return;
    }
    
    console.log('🔄 [Gallery Toggle] Toggle triggered (width: ' + window.innerWidth + 'px)');
    console.log('📊 [Gallery Toggle] Current state before toggle:', galleryState.isCollapsed ? 'collapsed' : 'expanded');
    
    galleryState.isCollapsed = !galleryState.isCollapsed;
    
    if (galleryState.isCollapsed) {
        console.log('➡️ [Gallery Toggle] Collapsing gallery section');
        leftSection.classList.add('collapsed');
    } else {
        console.log('⬅️ [Gallery Toggle] Expanding gallery section');
        leftSection.classList.remove('collapsed');
    }
    
    console.log('✅ [Gallery Toggle] New state after toggle:', galleryState.isCollapsed ? 'collapsed' : 'expanded');
    console.log('📐 [Gallery Toggle] Left section classes:', leftSection.classList.toString());
}

function initGalleryToggle() {
    console.log('🎨 [Gallery Toggle] Initializing gallery toggle functionality');
    
    const toggleBtn = document.getElementById('toggleGalleryBtn');
    const galleryHeader = document.getElementById('galleryHeader');
    const leftSection = document.getElementById('leftSection');
    
    if (!toggleBtn) {
        console.error('❌ [Gallery Toggle] Toggle button not found');
        return;
    }
    
    if (!galleryHeader) {
        console.error('❌ [Gallery Toggle] Gallery header not found');
        return;
    }
    
    if (!leftSection) {
        console.error('❌ [Gallery Toggle] Left section not found');
        return;
    }
    
    console.log('✅ [Gallery Toggle] Elements found:', {
        toggleBtn: toggleBtn,
        galleryHeader: galleryHeader,
        leftSection: leftSection
    });
    
    toggleBtn.addEventListener('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        console.log('🖱️ [Gallery Toggle] Toggle button clicked directly');
        toggleGallerySection();
    });
    
    galleryHeader.addEventListener('click', function(event) {
        const isTabButton = event.target.closest('.left-tab-button');
        const isToggleButton = event.target === toggleBtn || toggleBtn.contains(event.target);
        
        if (isTabButton) {
            console.log('🖱️ [Gallery Toggle] Tab button clicked - Ignoring for toggle');
            return;
        }
        
        if (!isToggleButton && galleryState.isCollapsed) {
            console.log('🖱️ [Gallery Toggle] Collapsed bar clicked - Expanding');
            toggleGallerySection();
        }
    });
    
    const tabButtons = document.querySelectorAll('.left-tab-button');
    tabButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.stopPropagation();
            console.log('🖱️ [Gallery Toggle] Tab button clicked - Propagation stopped');
        });
    });
    
    console.log('✅ [Gallery Toggle] Event listeners attached successfully');
    console.log('📋 [Gallery Toggle] Button triggers collapse on desktop');
    console.log('📋 [Gallery Toggle] Collapsed bar is clickable to expand');
    console.log('🔒 [Gallery Toggle] Tab button clicks will not trigger collapse');
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 [Gallery Toggle] DOM Content Loaded - Initializing');
    initGalleryToggle();
    lucide.createIcons();
    console.log('✅ [Gallery Toggle] Lucide icons created');
});
})();


function showModal(title, message, type = 'info') {
    const modal = document.getElementById('messageModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');
    const modalContent = modal.querySelector('.modal-content');


    modalTitle.textContent = title;
    modalMessage.style.whiteSpace = 'pre-line';


    const urlRegex = /(https?:\/\/[^\s]+)/g;
    if (urlRegex.test(message)) {
        modalMessage.innerHTML = message.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer" class="modal-url-link">$1</a>');
    } else {
        modalMessage.textContent = message;
    }


    modalContent.classList.remove('error-modal', 'success-modal');


    if (type === 'error') {
        modalContent.classList.add('error-modal');
    } else if (type === 'success') {
        modalContent.classList.add('success-modal');
    }


    modal.classList.add('show');


    lucide.createIcons();
}

function closeModal() {
    const modal = document.getElementById('messageModal');
    modal.classList.remove('show');
}



document.addEventListener('click', function (event) {
    const modal = document.getElementById('messageModal');
    if (event.target === modal) {
        closeModal();
    }
});


document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        closeModal();
        closeLinkModal();
        closeBulletModal();
        closeDeleteConfirmModal();
        closeBlogUrlModal();
    }
});

let currentLinkTextInput = null;
let currentLinkSelectedText = '';
let currentLinkBeforeText = '';
let currentLinkAfterText = '';
let currentLinkStart = 0;

function showLinkDialog(textInput, selectedText, beforeText, afterText, start) {
    currentLinkTextInput = textInput;
    currentLinkSelectedText = selectedText;
    currentLinkBeforeText = beforeText;
    currentLinkAfterText = afterText;
    currentLinkStart = start;

    const linkModal = document.getElementById('linkModal');
    const linkUrlInput = document.getElementById('linkUrl');
    const linkDisplayNameInput = document.getElementById('linkDisplayName');

    linkUrlInput.value = '';
    linkDisplayNameInput.value = selectedText || '';

    linkModal.classList.add('show');

    setTimeout(() => {
        linkUrlInput.focus();
    }, 100);

    lucide.createIcons();
}

function closeLinkModal() {
    const linkModal = document.getElementById('linkModal');
    linkModal.classList.remove('show');

    currentLinkTextInput = null;
    currentLinkSelectedText = '';
    currentLinkBeforeText = '';
    currentLinkAfterText = '';
    currentLinkStart = 0;
}

function insertLink() {
    const linkUrl = document.getElementById('linkUrl').value.trim();
    const linkDisplayName = document.getElementById('linkDisplayName').value.trim();

    if (!linkUrl) {
        alert('Please enter a URL');
        document.getElementById('linkUrl').focus();
        return;
    }

    if (!linkDisplayName) {
        alert('Please enter display text for the link');
        document.getElementById('linkDisplayName').focus();
        return;
    }

    try {
        new URL(linkUrl);
    } catch (e) {
        alert('Please enter a valid URL (including http:// or https://)//');
        document.getElementById('linkUrl').focus();
        return;
    }

    const formattedText = `<a href="${linkUrl}">${linkDisplayName}</a>`;

    if (currentLinkTextInput) {
        currentLinkTextInput.value = currentLinkBeforeText + formattedText + currentLinkAfterText;

        const newCursorPos = currentLinkStart + formattedText.length;
        currentLinkTextInput.setSelectionRange(newCursorPos, newCursorPos);
        currentLinkTextInput.focus();
    }

    closeLinkModal();
}

document.addEventListener('keydown', function (event) {
    const linkModal = document.getElementById('linkModal');
    if (linkModal && linkModal.classList.contains('show')) {
        if (event.key === 'Enter') {
            event.preventDefault();
            insertLink();
        }
    }
});

document.addEventListener('click', function (event) {
    const linkModal = document.getElementById('linkModal');
    if (event.target === linkModal) {
        closeLinkModal();
    }
});

let currentBulletTextInput = null;
let currentBulletSelectedText = '';
let currentBulletBeforeText = '';
let currentBulletAfterText = '';
let currentBulletStart = 0;

function showBulletDialog(textInput, selectedText, beforeText, afterText, start) {
    currentBulletTextInput = textInput;
    currentBulletSelectedText = selectedText;
    currentBulletBeforeText = beforeText;
    currentBulletAfterText = afterText;
    currentBulletStart = start;

    const bulletModal = document.getElementById('bulletModal');
    const bulletInputs = document.querySelectorAll('.bullet-input');

    bulletInputs.forEach(input => input.value = '');

    if (selectedText) {
        const lines = selectedText.split('\n').filter(line => line.trim());
        lines.forEach((line, index) => {
            if (index < bulletInputs.length) {
                bulletInputs[index].value = line.trim();
            } else {
                addBulletPoint(line.trim());
            }
        });
    }

    bulletModal.classList.add('show');

    setTimeout(() => {
        const firstInput = document.querySelector('.bullet-input');
        if (firstInput) firstInput.focus();
    }, 100);

    lucide.createIcons();
}

function closeBulletModal() {
    const bulletModal = document.getElementById('bulletModal');
    bulletModal.classList.remove('show');

    resetBulletPoints();

    currentBulletTextInput = null;
    currentBulletSelectedText = '';
    currentBulletBeforeText = '';
    currentBulletAfterText = '';
    currentBulletStart = 0;
}

function addBulletPoint(value = '') {
    const container = document.getElementById('bulletPointsContainer');
    const bulletCount = container.children.length + 1;

    const bulletItem = document.createElement('div');
    bulletItem.className = 'bullet-point-item flex items-center gap-2';
    bulletItem.innerHTML = `
        <input type="text" class="bullet-input form-input flex-1" placeholder="Bullet point ${bulletCount}" value="${value}" />
        <button type="button" class="remove-bullet-btn text-white/50 hover:text-red-500 transition-colors p-1" title="Remove">
            <i data-lucide="x" class="w-4 h-4"></i>
        </button>
    `;

    container.appendChild(bulletItem);
    lucide.createIcons();

    const newInput = bulletItem.querySelector('.bullet-input');
    if (newInput) newInput.focus();
}

function resetBulletPoints() {
    const container = document.getElementById('bulletPointsContainer');
    container.innerHTML = `
        <div class="bullet-point-item flex items-center gap-2">
            <input type="text" class="bullet-input form-input flex-1" placeholder="Bullet point 1" />
            <button type="button" class="remove-bullet-btn text-white/50 hover:text-red-500 transition-colors p-1" title="Remove">
                <i data-lucide="x" class="w-4 h-4"></i>
            </button>
        </div>
        <div class="bullet-point-item flex items-center gap-2">
            <input type="text" class="bullet-input form-input flex-1" placeholder="Bullet point 2" />
            <button type="button" class="remove-bullet-btn text-white/50 hover:text-red-500 transition-colors p-1" title="Remove">
                <i data-lucide="x" class="w-4 h-4"></i>
            </button>
        </div>
    `;
    lucide.createIcons();
}

function insertBulletList() {
    const bulletInputs = document.querySelectorAll('.bullet-input');
    const bulletPoints = [];

    bulletInputs.forEach(input => {
        const value = input.value.trim();
        if (value) {
            bulletPoints.push(value);
        }
    });

    if (bulletPoints.length === 0) {
        alert('Please enter at least one bullet point');
        const firstInput = document.querySelector('.bullet-input');
        if (firstInput) firstInput.focus();
        return;
    }

    const listItems = bulletPoints.map(point => `<li> • ${point}</li>`);
    const formattedText = `<ul>\n${listItems.join('\n')}\n</ul>`;

    if (currentBulletTextInput) {
        currentBulletTextInput.value = currentBulletBeforeText + formattedText + currentBulletAfterText;

        const newCursorPos = currentBulletStart + formattedText.length;
        currentBulletTextInput.setSelectionRange(newCursorPos, newCursorPos);
        currentBulletTextInput.focus();
    }

    closeBulletModal();
}

document.addEventListener('click', function (event) {
    if (event.target.id === 'addBulletBtn' || event.target.closest('#addBulletBtn')) {
        event.preventDefault();
        addBulletPoint();
    }

    if (event.target.closest('.remove-bullet-btn')) {
        event.preventDefault();
        const bulletItem = event.target.closest('.bullet-point-item');
        const container = document.getElementById('bulletPointsContainer');

        if (container.children.length > 1) {
            bulletItem.remove();
        } else {
            const input = bulletItem.querySelector('.bullet-input');
            if (input) input.value = '';
        }
    }

    const bulletModal = document.getElementById('bulletModal');
    if (event.target === bulletModal) {
        closeBulletModal();
    }
});

document.addEventListener('keydown', function (event) {
    const bulletModal = document.getElementById('bulletModal');
    if (bulletModal && bulletModal.classList.contains('show')) {
        if (event.key === 'Enter') {
            if (event.target.classList.contains('bullet-input')) {
                event.preventDefault();
                addBulletPoint();
            } else {
                event.preventDefault();
                insertBulletList();
            }
        } else if (event.key === 'Escape') {
            event.preventDefault();
            closeBulletModal();
        }
    }
});

let currentDeleteBlogId = null;
let currentDeleteBlogTitle = '';

function showDeleteConfirmModal(blogId, blogTitle) {
    currentDeleteBlogId = blogId;
    currentDeleteBlogTitle = blogTitle;

    const deleteModal = document.getElementById('deleteConfirmModal');
    const deleteBlogTitleElement = document.getElementById('deleteBlogTitle');
    const redirectUrlInput = document.getElementById('redirectUrl');
    const confirmCheckbox = document.getElementById('confirmDeleteCheckbox');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

    deleteBlogTitleElement.textContent = blogTitle;

    redirectUrlInput.value = '';
    confirmCheckbox.checked = false;
    confirmDeleteBtn.disabled = true;

    deleteModal.classList.add('show');

    lucide.createIcons();
}

function closeDeleteConfirmModal() {
    const deleteModal = document.getElementById('deleteConfirmModal');
    deleteModal.classList.remove('show');

    currentDeleteBlogId = null;
    currentDeleteBlogTitle = '';
}

function updateDeleteButtonState() {
    const confirmCheckbox = document.getElementById('confirmDeleteCheckbox');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

    confirmDeleteBtn.disabled = !confirmCheckbox.checked;
}

async function confirmDeleteBlog() {
    if (!currentDeleteBlogId) {
        showModal('Error', 'No blog selected for deletion', 'error');
        return;
    }

    const redirectUrl = document.getElementById('redirectUrl').value.trim();
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

    if (redirectUrl) {
        try {
            new URL(redirectUrl);
        } catch (e) {
            alert('Please enter a valid redirect URL (including http:// or https://)');
            document.getElementById('redirectUrl').focus();
            return;
        }
    }

    try {
        const originalText = confirmDeleteBtn.innerHTML;
        confirmDeleteBtn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 mr-2 animate-spin"></i>Deleting...';
        confirmDeleteBtn.disabled = true;

        const response = await fetch(`/api/blogs/${currentDeleteBlogId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        confirmDeleteBtn.innerHTML = originalText;
        confirmDeleteBtn.disabled = false;

        const result = await response.json();

        if (result.status === 'success') {
            let message = `Blog "${currentDeleteBlogTitle}" has been marked as deleted successfully.`;
            if (redirectUrl) {
                message += `\n\nVisitors will be redirected to: ${redirectUrl}`;
            } else {
                message += `\n\nVisitors will see a 403 Forbidden page when trying to access this blog.`;
            }

            showModal('Success', message, 'success');

            closeDeleteConfirmModal();

            fetchBlogs();
        } else {
            showModal('Error', result.message || 'Failed to mark blog as deleted', 'error');
        }

    } catch (error) {
        console.error('Error deleting blog:', error);

        confirmDeleteBtn.innerHTML = '<i data-lucide="trash-2" class="w-4 h-4 mr-2"></i>Delete Blog';
        confirmDeleteBtn.disabled = false;

        showModal('Error', 'An error occurred while deleting the blog. Please try again.', 'error');
    }
}

document.addEventListener('change', function (event) {
    if (event.target.id === 'confirmDeleteCheckbox') {
        updateDeleteButtonState();
    }
});

document.addEventListener('click', function (event) {
    const deleteModal = document.getElementById('deleteConfirmModal');
    if (event.target === deleteModal) {
        closeDeleteConfirmModal();
    }
});

document.addEventListener('keydown', function (event) {
    const deleteModal = document.getElementById('deleteConfirmModal');
    if (deleteModal && deleteModal.classList.contains('show')) {
        if (event.key === 'Enter') {
            event.preventDefault();
            const confirmCheckbox = document.getElementById('confirmDeleteCheckbox');
            if (confirmCheckbox.checked) {
                confirmDeleteBlog();
            }
        } else if (event.key === 'Escape') {
            event.preventDefault();
            closeDeleteConfirmModal();
        }
    }
});

let currentBlogUrl = '';

function showBlogUrl(blogSlug, blogTitle) {
    blogSlug = blogSlug.replace("[quotetation_here]", "'");
    blogTitle = blogTitle.replace("[quotetation_here]", "'");

    if (!blogSlug) {
        showModal('Error', 'Blog slug not found', 'error');
        return;
    }

    const baseUrl = window.location.origin;
    const blogUrl = `${baseUrl}/blog/${blogSlug}`;
    currentBlogUrl = blogUrl;

    const urlModal = document.getElementById('blogUrlModal');
    const urlBlogTitle = document.getElementById('urlBlogTitle');
    const blogUrlDisplay = document.getElementById('blogUrlDisplay');

    urlBlogTitle.textContent = blogTitle;
    blogUrlDisplay.value = blogUrl;

    urlModal.classList.add('show');

    lucide.createIcons();
}

function closeBlogUrlModal() {
    const urlModal = document.getElementById('blogUrlModal');
    urlModal.classList.remove('show');

    currentBlogUrl = '';
}

function copyBlogUrl() {
    const blogUrlDisplay = document.getElementById('blogUrlDisplay');
    const copyBtn = document.getElementById('copyUrlBtn');

    blogUrlDisplay.select();
    blogUrlDisplay.setSelectionRange(0, 99999);

    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(currentBlogUrl).then(() => {
            showCopyFeedback(copyBtn, 'Copied!');
        }).catch(() => {
            fallbackCopyTextToClipboard(currentBlogUrl, copyBtn);
        });
    } else {
        fallbackCopyTextToClipboard(currentBlogUrl, copyBtn);
    }
}

function openBlogInNewTab() {
    if (currentBlogUrl) {
        window.open(currentBlogUrl, '_blank', 'noopener,noreferrer');
    }
}

function showCopyFeedback(button, message) {
    const originalContent = button.innerHTML;
    button.innerHTML = `<i data-lucide="check" class="w-4 h-4"></i>`;
    button.classList.add('bg-green-600', 'hover:bg-green-700');
    button.classList.remove('bg-blue-600', 'hover:bg-blue-700');

    lucide.createIcons();

    setTimeout(() => {
        button.innerHTML = originalContent;
        button.classList.remove('bg-green-600', 'hover:bg-green-700');
        button.classList.add('bg-blue-600', 'hover:bg-blue-700');
        lucide.createIcons();
    }, 2000);
}

function fallbackCopyTextToClipboard(text, button) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.width = "2em";
    textArea.style.height = "2em";
    textArea.style.padding = "0";
    textArea.style.border = "none";
    textArea.style.outline = "none";
    textArea.style.boxShadow = "none";
    textArea.style.background = "transparent";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        document.execCommand('copy');
        showCopyFeedback(button, 'Copied!');
    } catch (err) {
        console.error('Failed to copy URL', err);
        showModal('Copy Failed', 'Unable to copy URL to clipboard. Please select and copy manually.', 'error');
    }

    document.body.removeChild(textArea);
}

document.addEventListener('click', function (event) {
    const urlModal = document.getElementById('blogUrlModal');
    if (event.target === urlModal) {
        closeBlogUrlModal();
    }
});

document.addEventListener('keydown', function (event) {
    const urlModal = document.getElementById('blogUrlModal');
    if (urlModal && urlModal.classList.contains('show')) {
        if (event.key === 'Enter') {
            event.preventDefault();
            openBlogInNewTab();
        } else if (event.key === 'Escape') {
            event.preventDefault();
            closeBlogUrlModal();
        }
    }
});

class ExpandableTabs {
    constructor(container, options = {}) {
        this.container = container;
        this.tabs = options.tabs || [];
        this.activeColor = options.activeColor || 'text-blue-600';
        this.onChange = options.onChange || (() => { });
        this.selected = null;
        this.init();
    }
    init() {
        this.render();
        this.bindEvents();
    }
    render() {
        this.container.innerHTML = '';
        this.tabs.forEach((tab, index) => {
            if (tab.type === 'separator') {
                const separator = this.createSeparator();
                this.container.appendChild(separator);
            } else {
                const button = this.createTabButton(tab, index);
                this.container.appendChild(button);
            }
        });
    }
    createSeparator() {
        const separator = document.createElement('div');
        separator.className = 'separator';
        separator.style.background = 'rgba(255, 255, 255, 0.3)';
        separator.setAttribute('aria-hidden', 'true');
        return separator;
    }
    createTabButton(tab, index) {
        const button = document.createElement('button');
        const isSelected = this.selected === index;
        button.className = `tab-button relative flex items-center text-sm font-medium tracking-wide transition-all duration-[600ms] ${isSelected ? 'selected' : ''
            }`;
        if (isSelected) {
            button.style.color = this.activeColor || 'rgb(147, 197, 253)';
        } else {
            button.style.color = 'rgba(255, 255, 255, 0.6)';
        }
        button.dataset.index = index;
        const iconWrapper = document.createElement('div');
        iconWrapper.className = 'flex-shrink-0';
        iconWrapper.innerHTML = `<i data-lucide="${tab.icon}" class="w-4 h-4"></i>`;
        const textElement = document.createElement('span');
        textElement.className = `tab-text ${isSelected ? 'expanded' : ''}`;
        textElement.textContent = tab.title;
        button.appendChild(iconWrapper);
        button.appendChild(textElement);
        button.addEventListener('mouseenter', () => {
            if (!button.classList.contains('selected')) {
                button.style.color = 'rgba(255, 255, 255, 0.9)';
            }
        });
        button.addEventListener('mouseleave', () => {
            if (!button.classList.contains('selected')) {
                button.style.color = 'rgba(255, 255, 255, 0.6)';
            }
        });
        return button;
    }
    handleSelect(index) {
        this.selected = index;
        const buttons = this.container.querySelectorAll('.tab-button');
        buttons.forEach((button, i) => {
            const buttonIndex = parseInt(button.dataset.index);
            const textElement = button.querySelector('.tab-text');
            if (this.selected === buttonIndex) {
                button.classList.add('selected');
                button.style.color = this.activeColor || 'rgb(147, 197, 253)';
                textElement.classList.add('expanded');
            } else {
                button.classList.remove('selected');
                button.style.color = 'rgba(255, 255, 255, 0.6)';
                textElement.classList.remove('expanded');
            }
        });
        this.onChange(this.selected);
    }
    bindEvents() {
        if (this.eventsbound) return;
        this.eventsbound = true;
        this.container.addEventListener('click', (e) => {
            const button = e.target.closest('.tab-button');
            if (button && button.dataset.index !== undefined) {
                this.handleSelect(parseInt(button.dataset.index));
            }
        });
    }
}

function showContentSection(tabTitle) {

    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });


    let sectionId = '';
    switch (tabTitle) {
        case 'Add Blogs':
        case 'Add Case Study':
            sectionId = 'addBlogs';
            break;
        case 'Edit/Delete Blog':
        case 'Edit/Delete Case Study':
            sectionId = 'editBlogs';
            break;
    }

    if (sectionId) {
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
        }
    }
}

function initializeLabelsSection() {
    const addLabelBtn = document.getElementById('addLabelBtn');
    const labelsContainer = document.getElementById('labelsContainer');
    const labelsNotMandatory = document.getElementById('labelsNotMandatory');

    addLabelBtn.addEventListener('click', function () {
        addLabelRow();
    });

    labelsContainer.addEventListener('click', function (e) {
        if (e.target.closest('.remove-label-btn')) {
            const labelItem = e.target.closest('.label-item');
            const allLabels = labelsContainer.querySelectorAll('.label-item');

            if (allLabels.length > 1) {
                labelItem.remove();
            } else {
                labelItem.querySelector('.label-input').value = '';
                labelItem.querySelector('.weight-input').value = '';
            }
        }
    });
}

function addLabelRow() {
    const labelsContainer = document.getElementById('labelsContainer');
    const labelItem = document.createElement('div');
    labelItem.className = 'label-item flex items-center gap-3';
    labelItem.innerHTML = `
        <div class="flex-1">
            <input type="text" class="label-input form-input" placeholder="Enter label name..." />
        </div>
        <div class="w-24">
            <input type="number" class="weight-input form-input" placeholder="Weight" min="1" max="100" />
        </div>
        <button type="button" class="remove-label-btn text-white/50 hover:text-red-500 transition-colors p-2 rounded-lg hover:bg-white/[0.05]" title="Remove">
            <i data-lucide="x" class="w-4 h-4"></i>
        </button>
    `;
    labelsContainer.appendChild(labelItem);
    lucide.createIcons();
}

function populateLabelsFromData(labelsData) {
    const labelsContainer = document.getElementById('labelsContainer');
    const labelsNotMandatory = document.getElementById('labelsNotMandatory');

    labelsContainer.innerHTML = '';

    if (labelsData && typeof labelsData === 'object' && Object.keys(labelsData).length > 0) {
        Object.entries(labelsData).forEach(([label, weight]) => {
            const labelItem = document.createElement('div');
            labelItem.className = 'label-item flex items-center gap-3';
            labelItem.innerHTML = `
                <div class="flex-1">
                    <input type="text" class="label-input form-input" placeholder="Enter label name..." value="${label}" />
                </div>
                <div class="w-24">
                    <input type="number" class="weight-input form-input" placeholder="Weight" min="1" max="100" value="${weight}" />
                </div>
                <button type="button" class="remove-label-btn text-white/50 hover:text-red-500 transition-colors p-2 rounded-lg hover:bg-white/[0.05]" title="Remove">
                    <i data-lucide="x" class="w-4 h-4"></i>
                </button>
            `;
            labelsContainer.appendChild(labelItem);
        });
        labelsNotMandatory.checked = false;
    } else {
        addLabelRow();
        labelsNotMandatory.checked = true;
    }

    lucide.createIcons();
}

function collectLabelsData() {
    const labelsNotMandatory = document.getElementById('labelsNotMandatory').checked;
    const labelItems = document.querySelectorAll('.label-item');
    const labelsObj = {};
    let hasLabels = false;

    labelItems.forEach(item => {
        const labelInput = item.querySelector('.label-input').value.trim();
        const weightInput = item.querySelector('.weight-input').value.trim();

        if (labelInput && weightInput) {
            labelsObj[labelInput] = parseInt(weightInput);
            hasLabels = true;
        }
    });

    if (!labelsNotMandatory && !hasLabels) {
        showModal('Labels Required', 'Please add at least one label or check the "Labels are not mandatory" option.', 'error');
        return null;
    }

    return { labels: labelsObj, labelsNotMandatory: labelsNotMandatory };
}


function handleFormSubmit(event) {
    event.preventDefault();

    const labelsResult = collectLabelsData();
    if (labelsResult === null) {
        return;
    }

    const formData = new FormData(event.target);
    const data = {};
    for (let [key, value] of formData.entries()) {
        if (key === 'editors_choice') {
            data[key] = value === 'on' ? 'Y' : 'N';
        } else {
            data[key] = value;
        }
    }
    if (!data.editors_choice) {
        data.editors_choice = 'N';
    }

    data.labels = labelsResult.labels;
    data.labelsNotMandatory = labelsResult.labelsNotMandatory;

    // Add content type to the data
    data.contentType = document.getElementById('contentType').value || 'BLOG';

    if (!data.blogDate) {
        const today = new Date().toISOString().split('T')[0];
        data.blogDate = today;
    }

    console.log('Form submitted:', data);
    alert('Blog added successfully! (This is a demo)');
    event.target.reset();
}


async function handleLoadPreview() {
    const form = document.getElementById('addBlogForm');
    const formData = new FormData(form);
    const data = {};
    for (let [key, value] of formData.entries()) {

        if (!key.startsWith('dynamic_')) {
            data[key] = value;
        }
    }


    if (!data.blogDate) {
        const today = new Date().toISOString().split('T')[0];
        data.blogDate = today;
        document.getElementById('blogDate').value = today;
    }


    const dynamicSections = collectDynamicSections();
    data.dynamicSections = dynamicSections;

    try {

        const loadPreviewBtn = document.getElementById('loadPreviewBtn');
        const originalText = loadPreviewBtn.innerHTML;
        loadPreviewBtn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 mr-2 animate-spin"></i>Loading...';
        loadPreviewBtn.disabled = true;


        const contentType = document.getElementById('contentType').value;
        const endpoint = contentType === 'CASE STUDY' ? '/api/admin_case_study_preview' : '/api/admin_blog_preview';

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();


        loadPreviewBtn.innerHTML = originalText;
        loadPreviewBtn.disabled = false;

        if (result.status === 'success') {

            const previewWindow = window.open('', 'preview', 'width=800,height=600,scrollbars=yes');
            previewWindow.document.write(result.data);
            previewWindow.document.close();
        } else {
            alert('Error generating preview: ' + (result.message || 'Unknown error'));
        }

    } catch (error) {

        const loadPreviewBtn = document.getElementById('loadPreviewBtn');
        loadPreviewBtn.innerHTML = '<i data-lucide="eye" class="w-4 h-4 mr-2"></i>Load Preview';
        loadPreviewBtn.disabled = false;

        console.error('Error loading preview:', error);
        alert('Error loading preview: ' + error.message);
    }
}


async function handleSaveDraft() {
    const labelsResult = collectLabelsData();
    if (labelsResult === null) {
        return;
    }

    const form = document.getElementById('addBlogForm');
    const formData = new FormData(form);
    const data = {};
    for (let [key, value] of formData.entries()) {
        if (!key.startsWith('dynamic_')) {
            data[key] = value;
        }
    }

    data.labels = labelsResult.labels;
    data.labelsNotMandatory = labelsResult.labelsNotMandatory;

    if (!data.blogDate) {
        const today = new Date().toISOString().split('T')[0];
        data.blogDate = today;
        document.getElementById('blogDate').value = today;
    }

    const dynamicSections = collectDynamicSections();
    data.dynamicSections = dynamicSections;

    data.blogStatus = 'draft';
    
    // Add content type to the data
    data.contentType = document.getElementById('contentType').value || 'BLOG';

    try {
        const saveDraftBtn = document.getElementById('saveDraftBtn');
        const originalText = saveDraftBtn.innerHTML;
        saveDraftBtn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 mr-2 animate-spin"></i>Saving...';
        saveDraftBtn.disabled = true;

        const endpoint = data.contentType === 'CASE STUDY' ? '/api/admin_save_case_study' : '/api/admin_save_blog';
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        saveDraftBtn.innerHTML = originalText;
        saveDraftBtn.disabled = false;

        if (!response.ok) {
            let errorMessage = `Server error (${response.status})`;
            try {
                const errorResult = await response.json();
                errorMessage = errorResult.message || errorResult.error || errorMessage;
            } catch (e) {
                errorMessage = response.statusText || errorMessage;
            }
            showModal('Error Saving Draft', errorMessage, 'error');
            return;
        }

        const result = await response.json();

        if (result.status === 'success') {
            let message = 'Blog saved as draft successfully!';
            if (result.url) {
                message += `\n\nBlog URL: ${result.url}`;
            }
            showModal('Success', message, 'success');
        } else {
            showModal('Error Saving Draft', result.message || 'Unknown error', 'error');
        }

    } catch (error) {
        const saveDraftBtn = document.getElementById('saveDraftBtn');
        saveDraftBtn.innerHTML = '<i data-lucide="file-text" class="w-4 h-4 mr-2"></i>Save as Draft';
        saveDraftBtn.disabled = false;

        console.error('Error saving draft:', error);
        showModal('Error Saving Draft', error.message, 'error');
    }
}


async function handleSavePublish() {
    const labelsResult = collectLabelsData();
    if (labelsResult === null) {
        return;
    }

    const form = document.getElementById('addBlogForm');
    const formData = new FormData(form);
    const data = {};
    for (let [key, value] of formData.entries()) {
        if (!key.startsWith('dynamic_')) {
            data[key] = value;
        }
    }

    data.labels = labelsResult.labels;
    data.labelsNotMandatory = labelsResult.labelsNotMandatory;

    if (!data.blogDate) {
        const today = new Date().toISOString().split('T')[0];
        data.blogDate = today;
        document.getElementById('blogDate').value = today;
    }

    const dynamicSections = collectDynamicSections();
    data.dynamicSections = dynamicSections;

    data.blogStatus = 'published';
    
    // Add content type to the data
    data.contentType = document.getElementById('contentType').value || 'BLOG';

    try {
        const savePublishBtn = document.getElementById('savePublishBtn');
        const originalText = savePublishBtn.innerHTML;
        savePublishBtn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 mr-2 animate-spin"></i>Publishing...';
        savePublishBtn.disabled = true;

        const endpoint = data.contentType === 'CASE STUDY' ? '/api/admin_save_case_study' : '/api/admin_save_blog';
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        savePublishBtn.innerHTML = originalText;
        savePublishBtn.disabled = false;

        if (!response.ok) {
            let errorMessage = `Server error (${response.status})`;
            try {
                const errorResult = await response.json();
                errorMessage = errorResult.message || errorResult.error || errorMessage;
            } catch (e) {
                errorMessage = response.statusText || errorMessage;
            }
            showModal('Error Publishing Blog', errorMessage, 'error');
            return;
        }

        const result = await response.json();

        if (result.status === 'success') {
            let message = 'Blog published successfully!';
            if (result.url) {
                message += `\n\nBlog URL: ${result.url}`;
            }
            showModal('Success', message, 'success');

            form.reset();

            document.getElementById('dynamicSections').innerHTML = '';
            sectionCounter = 0;
        } else {
            showModal('Error Publishing Blog', result.message || 'Unknown error', 'error');
        }

    } catch (error) {
        const savePublishBtn = document.getElementById('savePublishBtn');
        savePublishBtn.innerHTML = '<i data-lucide="send" class="w-4 h-4 mr-2"></i>Save & Publish';
        savePublishBtn.disabled = false;

        console.error('Error publishing blog:', error);
        showModal('Error Publishing Blog', error.message, 'error');
    }
}


let sectionCounter = 0;

function createDynamicSection(type, content = '') {
    sectionCounter++;
    const sectionId = `section_${sectionCounter}`;
    const sectionDiv = document.createElement('div');
    sectionDiv.className = 'dynamic-section p-4 rounded-lg  relative';
    sectionDiv.dataset.sectionId = sectionId;
    sectionDiv.dataset.sectionType = type;

    let sectionHTML = '';

    switch (type) {
        case 'text':
            sectionHTML = `
                <div class="flex justify-between items-center mb-2">
                    <label class="form-label text-sm flex items-center">
                        <i data-lucide="type" class="w-4 h-4 mr-2"></i>Text Content
                    </label>
                    <button type="button" class="remove-section" data-section-id="${sectionId}">
                        <i data-lucide="x" class="w-4 h-4"></i>
                    </button>
                </div>
                <div class="text-formatting-toolbar mb-2 flex flex-wrap gap-1">
                    <button type="button" class="format-btn" data-format="bold" title="Bold"><i data-lucide="bold" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="italic" title="Italic"><i data-lucide="italic" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="underline" title="Underline"><i data-lucide="underline" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="link" title="Hyperlink"><i data-lucide="link" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="list" title="Bullet Points"><i data-lucide="list" class="w-4 h-4"></i></button>
                </div>
                <textarea name="dynamic_text_${sectionId}" class="form-input" style="height: 4rem; resize: vertical;" placeholder="Enter your text content...">${content}</textarea>
            `;
            break;
        case 'h1':
            sectionHTML = `
                <div class="flex justify-between items-center mb-2">
                    <label class="form-label text-sm flex items-center">
                        <i data-lucide="heading-1" class="w-4 h-4 mr-2"></i>H1 Header
                    </label>
                    <button type="button" class="remove-section" data-section-id="${sectionId}">
                        <i data-lucide="x" class="w-4 h-4"></i>
                    </button>
                </div>
                <div class="text-formatting-toolbar mb-2 flex flex-wrap gap-1">
                    <button type="button" class="format-btn" data-format="bold" title="Bold"><i data-lucide="bold" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="italic" title="Italic"><i data-lucide="italic" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="underline" title="Underline"><i data-lucide="underline" class="w-4 h-4"></i></button>
                </div>
                <input type="text" name="dynamic_h1_${sectionId}" class="form-input" placeholder="Enter H2 header text..." value="${content}">
            `;
            break;
        case 'h2':
            sectionHTML = `
                <div class="flex justify-between items-center mb-2">
                    <label class="form-label text-sm flex items-center">
                        <i data-lucide="heading-2" class="w-4 h-4 mr-2"></i>H2 Header
                    </label>
                    <button type="button" class="remove-section" data-section-id="${sectionId}">
                        <i data-lucide="x" class="w-4 h-4"></i>
                    </button>
                </div>
                <div class="text-formatting-toolbar mb-2 flex flex-wrap gap-1">
                    <button type="button" class="format-btn" data-format="bold" title="Bold"><i data-lucide="bold" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="italic" title="Italic"><i data-lucide="italic" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="underline" title="Underline"><i data-lucide="underline" class="w-4 h-4"></i></button>
                </div>
                <input type="text" name="dynamic_h2_${sectionId}" class="form-input" placeholder="Enter H3 header text..." value="${content}">
            `;
            break;
        case 'h3':
            sectionHTML = `
                <div class="flex justify-between items-center mb-2">
                    <label class="form-label text-sm flex items-center">
                        <i data-lucide="heading-3" class="w-4 h-4 mr-2"></i>H3 Header
                    </label>
                    <button type="button" class="remove-section" data-section-id="${sectionId}">
                        <i data-lucide="x" class="w-4 h-4"></i>
                    </button>
                </div>
                <div class="text-formatting-toolbar mb-2 flex flex-wrap gap-1">
                    <button type="button" class="format-btn" data-format="bold" title="Bold"><i data-lucide="bold" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="italic" title="Italic"><i data-lucide="italic" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="underline" title="Underline"><i data-lucide="underline" class="w-4 h-4"></i></button>
                </div>
                <input type="text" name="dynamic_h3_${sectionId}" class="form-input" placeholder="Enter H4 header text..." value="${content}">
            `;
            break;
        case 'h4':
            sectionHTML = `
                <div class="flex justify-between items-center mb-2">
                    <label class="form-label text-sm flex items-center">
                        <i data-lucide="heading-4" class="w-4 h-4 mr-2"></i>H4 Header
                    </label>
                    <button type="button" class="remove-section" data-section-id="${sectionId}">
                        <i data-lucide="x" class="w-4 h-4"></i>
                    </button>
                </div>
                <div class="text-formatting-toolbar mb-2 flex flex-wrap gap-1">
                    <button type="button" class="format-btn" data-format="bold" title="Bold"><i data-lucide="bold" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="italic" title="Italic"><i data-lucide="italic" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="underline" title="Underline"><i data-lucide="underline" class="w-4 h-4"></i></button>
                </div>
                <input type="text" name="dynamic_h4_${sectionId}" class="form-input" placeholder="Enter H5 header text..." value="${content}">
            `;
            break;
        case 'h5':
            sectionHTML = `
                <div class="flex justify-between items-center mb-2">
                    <label class="form-label text-sm flex items-center">
                        <i data-lucide="heading-5" class="w-4 h-4 mr-2"></i>H5 Header
                    </label>
                    <button type="button" class="remove-section" data-section-id="${sectionId}">
                        <i data-lucide="x" class="w-4 h-4"></i>
                    </button>
                </div>
                <div class="text-formatting-toolbar mb-2 flex flex-wrap gap-1">
                    <button type="button" class="format-btn" data-format="bold" title="Bold"><i data-lucide="bold" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="italic" title="Italic"><i data-lucide="italic" class="w-4 h-4"></i></button>
                    <button type="button" class="format-btn" data-format="underline" title="Underline"><i data-lucide="underline" class="w-4 h-4"></i></button>
                </div>
                <input type="text" name="dynamic_h5_${sectionId}" class="form-input" placeholder="Enter H6 header text..." value="${content}">
            `;
            break;
        case 'subheader-text':
            sectionHTML = `
                <div class="flex justify-between items-center mb-2">
                    <label class="form-label text-sm flex items-center">
                        <i data-lucide="heading-3" class="w-4 h-4 mr-2"></i>Subheader Text
                    </label>
                    <button type="button" class="remove-section" data-section-id="${sectionId}">
                        <i data-lucide="x" class="w-4 h-4"></i>
                    </button>
                </div>
                <textarea name="dynamic_subheader_text_${sectionId}" class="form-input" style="height: 3rem; resize: vertical;" placeholder="Enter subheader text content...">${content}</textarea>
            `;
            break;
        case 'image':
            sectionHTML = `
                <div class="flex justify-between items-center mb-2">
                    <label class="form-label text-sm flex items-center">
                        <i data-lucide="image" class="w-4 h-4 mr-2"></i>Image + Alt Text
                    </label>
                    <button type="button" class="remove-section" data-section-id="${sectionId}">
                        <i data-lucide="x" class="w-4 h-4"></i>
                    </button>
                </div>
                <div class="space-y-2">
                    <input type="url" name="dynamic_image_url_${sectionId}" class="form-input" placeholder="Image URL..." value="${content.url || ''}">
                    <input type="text" name="dynamic_image_alt_${sectionId}" class="form-input" placeholder="Alt text for image..." value="${content.alt || ''}">
                </div>
            `;
            break;
    }

    sectionDiv.innerHTML = sectionHTML;
    return sectionDiv;
}

function addDynamicSection(type) {
    const container = document.getElementById('dynamicSections');
    const section = createDynamicSection(type);
    container.appendChild(section);


    lucide.createIcons();


    const removeBtn = section.querySelector('.remove-section');
    removeBtn.addEventListener('click', function () {
        section.remove();
        updatePreviewIfVisible();
    });


    const inputs = section.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', updatePreviewIfVisible);
    });

    const formatBtns = section.querySelectorAll('.format-btn');
    formatBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const format = this.dataset.format;
            const textInput = section.querySelector('input[type="text"], textarea');

            if (textInput) {
                applyFormatting(textInput, format);
            }
        });
    });


    setTimeout(() => {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }, 100);

    updatePreviewIfVisible();
}

function applyFormatting(textInput, format) {
    const start = textInput.selectionStart;
    const end = textInput.selectionEnd;
    const selectedText = textInput.value.substring(start, end);
    const beforeText = textInput.value.substring(0, start);
    const afterText = textInput.value.substring(end);

    let formattedText = '';

    switch (format) {
        case 'bold':
            formattedText = selectedText ? `<strong>${selectedText}</strong>` : '<strong></strong>';
            break;
        case 'italic':
            formattedText = selectedText ? `<em>${selectedText}</em>` : '<em></em>';
            break;
        case 'underline':
            formattedText = selectedText ? `<u>${selectedText}</u>` : '<u></u>';
            break;
        case 'link':
            showLinkDialog(textInput, selectedText, beforeText, afterText, start);
            return;
            break;
        case 'list':
            showBulletDialog(textInput, selectedText, beforeText, afterText, start);
            return;
            break;
        default:
            return;
    }

    textInput.value = beforeText + formattedText + afterText;

    const newCursorPos = start + formattedText.length;
    textInput.setSelectionRange(newCursorPos, newCursorPos);
    textInput.focus();
}

function updatePreviewIfVisible() {


}

function collectDynamicSections() {
    const sections = [];
    const dynamicSections = document.querySelectorAll('.dynamic-section');

    dynamicSections.forEach(section => {
        const type = section.dataset.sectionType;
        const sectionId = section.dataset.sectionId;

        let sectionData = { type, id: sectionId };

        switch (type) {
            case 'text':
                sectionData.content = section.querySelector(`[name="dynamic_text_${sectionId}"]`).value;
                break;
            case 'h1':
                sectionData.content = section.querySelector(`[name="dynamic_h1_${sectionId}"]`).value;
                break;
            case 'h2':
                sectionData.content = section.querySelector(`[name="dynamic_h2_${sectionId}"]`).value;
                break;
            case 'h3':
                sectionData.content = section.querySelector(`[name="dynamic_h3_${sectionId}"]`).value;
                break;
            case 'h4':
                sectionData.content = section.querySelector(`[name="dynamic_h4_${sectionId}"]`).value;
                break;
            case 'h5':
                sectionData.content = section.querySelector(`[name="dynamic_h5_${sectionId}"]`).value;
                break;
            case 'h6':
                sectionData.content = section.querySelector(`[name="dynamic_h6_${sectionId}"]`).value;
                break;
            case 'header':
                sectionData.content = section.querySelector(`[name="dynamic_header_${sectionId}"]`).value;
                break;
            case 'subheader':
                sectionData.content = section.querySelector(`[name="dynamic_subheader_${sectionId}"]`).value;
                break;
            case 'subheader-text':
                sectionData.content = section.querySelector(`[name="dynamic_subheader_text_${sectionId}"]`).value;
                break;
            case 'image':
                sectionData.content = {
                    url: section.querySelector(`[name="dynamic_image_url_${sectionId}"]`).value,
                    alt: section.querySelector(`[name="dynamic_image_alt_${sectionId}"]`).value
                };
                break;
        }

        sections.push(sectionData);
    });

    return sections;
}

let currentPage = 1;
let totalPages = 1;
let searchTimeout = null;
const blogsPerPage = 8;
let allFetchedBlogs = [];

async function fetchBlogs() {
    const blogsLoading = document.getElementById('blogsLoading');
    const noBlogsFound = document.getElementById('noBlogsFound');
    const blogsList = document.getElementById('blogsList');
    const paginationControls = document.getElementById('paginationControls');

    blogsLoading.classList.remove('hidden');
    noBlogsFound.classList.add('hidden');
    blogsList.innerHTML = '';
    paginationControls.classList.add('hidden');

    try {
        console.log('📡 Fetching blogs from /api/blogs...');
        const response_blogs = await fetch('/api/blogs');
        const result_blogs = await response_blogs.json();
        
        const response_case_studies = await fetch('/api/case_studies');
        const result_case_studies = await response_case_studies.json();

        blogsLoading.classList.add('hidden');
        
        let blogs = [];
        if (result_blogs.status === 'success' && Array.isArray(result_blogs.blogs)) {
            blogs = result_blogs.blogs;
        }

        let case_studies = [];
        if (result_case_studies.status === 'success' && Array.isArray(result_case_studies.case_studies)) {
            case_studies = result_case_studies.case_studies;
        }

        allFetchedBlogs = [...blogs, ...case_studies];
        console.log(`✓ Stored ${allFetchedBlogs.length} items in allFetchedBlogs array`);
        
        applyFiltersAndRender(1);
    } catch (error) {
        console.error('✗ Error fetching blogs:', error);
        blogsLoading.classList.add('hidden');
        blogsList.innerHTML = `<div class="text-center py-8"><p class="text-white/60">Error loading blogs. Please try again later.</p></div>`;
    }
}

function applyFiltersAndRender(page = 1) {
    const filterTitleInput = document.getElementById('filterTitle');
    const filterCategoryInput = document.getElementById('filterCategory');
    const filterContentTypeInput = document.getElementById('filterContentType');
    
    const filterTitleValue = filterTitleInput ? filterTitleInput.value.trim().toLowerCase() : '';
    const filterCategoryValue = filterCategoryInput ? filterCategoryInput.value.trim().toLowerCase() : '';
    const filterContentTypeValue = filterContentTypeInput ? filterContentTypeInput.value : 'ALL';

    console.log('🔍 Applying filters:');
    console.log(`  - Title filter: "${filterTitleValue}" (${filterTitleValue ? 'ACTIVE' : 'INACTIVE'})`);
    console.log(`  - Category filter: "${filterCategoryValue}" (${filterCategoryValue ? 'ACTIVE' : 'INACTIVE'})`);
    console.log(`  - Type filter: "${filterContentTypeValue}"`);
    console.log(`  - Total blogs before filtering: ${allFetchedBlogs.length}`);

    const filteredBlogs = allFetchedBlogs.filter(blog => {
        if (!blog) {
            console.warn('⚠️ Null blog encountered in filter');
            return false;
        }

        let blogData = {};
        try {
            if (typeof blog.blog === 'string') {
                blogData = JSON.parse(blog.blog);
            } else if (typeof blog.blog === 'object' && blog.blog !== null) {
                blogData = blog.blog;
            }
        } catch (e) {
            console.error('Failed to parse blog.blog in filter:', e);
            blogData = {};
        }

        const title = (blogData.blogTitle || blog.title || '').toLowerCase();
        const category = (blog.category || blogData.blogCategory || '').toLowerCase();
        const type = blog.type || 'BLOG';

        const titleMatch = !filterTitleValue || title.includes(filterTitleValue);
        const categoryMatch = !filterCategoryValue || category.includes(filterCategoryValue);
        const typeMatch = filterContentTypeValue === 'ALL' || type === filterContentTypeValue;

        const matches = titleMatch && categoryMatch && typeMatch;
        
        if (filterTitleValue || filterCategoryValue || filterContentTypeValue !== 'ALL') {
            console.log(`  Blog "${title}": titleMatch=${titleMatch}, categoryMatch=${categoryMatch}, typeMatch=${typeMatch}, result=${matches}`);
        }

        return matches;
    });

    console.log(`✅ Filtered result: ${filteredBlogs.length} blogs from ${allFetchedBlogs.length} total`);

    const noBlogsFound = document.getElementById('noBlogsFound');
    const blogsList = document.getElementById('blogsList');
    const paginationControls = document.getElementById('paginationControls');

    if (filteredBlogs.length > 0) {
        noBlogsFound.classList.add('hidden');
        blogsList.classList.remove('hidden');

        totalPages = Math.ceil(filteredBlogs.length / blogsPerPage);
        currentPage = page;
        const startIndex = (page - 1) * blogsPerPage;
        const endIndex = startIndex + blogsPerPage;
        const paginatedBlogs = filteredBlogs.slice(startIndex, endIndex);

        console.log(`📄 Pagination info:`);
        console.log(`  - Current page: ${currentPage} of ${totalPages}`);
        console.log(`  - Showing blogs ${startIndex + 1}-${Math.min(endIndex, filteredBlogs.length)} of ${filteredBlogs.length}`);
        console.log(`  - Displaying ${paginatedBlogs.length} blogs on this page`);

        displayBlogs(paginatedBlogs);

        if (totalPages > 1) {
            updatePaginationControls();
            paginationControls.classList.remove('hidden');
            console.log(`✓ Pagination controls shown (${totalPages} pages total)`);
        } else {
            paginationControls.classList.add('hidden');
            console.log(`✓ Single page - pagination controls hidden`);
        }
    } else {
        blogsList.innerHTML = '';
        blogsList.classList.add('hidden');
        noBlogsFound.classList.remove('hidden');
        paginationControls.classList.add('hidden');
    }
}

function displayBlogs(blogs) {
    const blogsList = document.getElementById('blogsList');

    console.log('📄 Displaying', blogs.length, 'blogs');

    blogsList.innerHTML = blogs.map((blog, index) => {
        let blogData = {};
        
        try {
            if (typeof blog.blog === 'string') {
                blogData = JSON.parse(blog.blog);
            } else if (typeof blog.blog === 'object' && blog.blog !== null) {
                blogData = blog.blog;
            }
        } catch (e) {
            console.error(`Failed to parse blog.blog for blog ${index + 1}:`, e);
            blogData = {};
        }

        console.log(`📝 Blog ${index + 1}:`, {
            id: blog.id,
            status: blog.status,
            type: blog.type,
            category: blog.category,
            date: blog.date,
            blogDataType: typeof blog.blog,
            parsedBlogData: blogData
        });

        const title = blogData.blogTitle || blog.title || 'Untitled';
        const date = blogData.blogDate || blog.date || new Date().toISOString();
        const status = blog.status || 'draft';
        const mainImageUrl = blogData.mainImageUrl || '';
        const mainImageAlt = blogData.mainImageAlt || title;
        const category = blog.category || blogData.blogCategory || 'Uncategorized';
        const type = blog.type || 'BLOG';
        const slug = blog.slug || '';

        console.log(`  Title: "${title}", Slug: "${slug}", Date: "${date}", Status: "${status}", Type: "${type}", Category: "${category}"`);

        return `
            <div class="p-4 bg-white/5 rounded-lg border border-white/10 hover:bg-white/10 transition-colors">
                <div class="flex justify-between items-start mb-3">
                    <div class="flex-1">
                        <h3 class="font-semibold mb-2 text-white line-clamp-2">${escapeHtml(title)}</h3>
                        ${category ? `
                            <p class="text-xs text-white/50 mb-2 flex items-center gap-2">
                                <i data-lucide="tag" class="w-3 h-3"></i>
                                <span>${escapeHtml(category)}</span>
                            </p>
                        ` : ''}
                        <p class="text-sm text-white/60 mb-2 flex items-center gap-2 flex-wrap">
                            <span class="flex items-center gap-1">
                                <i data-lucide="calendar" class="w-3 h-3"></i>
                                <span>${formatDate(date)}</span>
                            </span>
                            <span>•</span>
                            <span class="px-2 py-1 rounded-full text-xs ${status === 'published' ? 'bg-green-600/20 text-green-400' : 'bg-yellow-600/20 text-yellow-400'}">${status}</span>
                            <span>•</span>
                            <span class="px-2 py-1 rounded-full text-xs ${type === 'CASE STUDY' ? 'bg-purple-600/20 text-purple-400' : 'bg-blue-600/20 text-blue-400'}">${type}</span>
                        </p>
                    </div>
                    ${mainImageUrl ? `
                        <div class="ml-4 flex-shrink-0">
                            <img src="${escapeHtml(mainImageUrl)}" alt="${escapeHtml(mainImageAlt)}"
                                 class="w-16 h-16 object-cover rounded-lg border border-white/10">
                        </div>
                    ` : ''}
                </div>
                <div class="flex gap-2 flex-wrap">
                    <button class="form-button text-xs px-4 py-2 min-w-[70px] bg-white/10 hover:bg-white/20 border border-white/20 text-white" onclick="editBlog('${blog.id.replace("'", "[quotetation_here]")}')">
                        <div class="flex items-center gap-2">
                            <i data-lucide="edit" class="w-3 h-3"></i>
                            <p>Edit</p>
                        </div>
                    </button>
                    <button class="form-button text-xs px-4 py-2 min-w-[60px] bg-white/10 hover:bg-white/20 border border-white/20 text-white" onclick="showBlogUrl('${slug.replace("'", "[quotetation_here]")}', '${title.replace("'", "[quotetation_here]")}')">
                        <div class="flex items-center gap-2">
                            <i data-lucide="external-link" class="w-3 h-3"></i>
                            <p>URL</p>
                        </div>
                    </button>
                    <button class="form-button text-xs px-4 py-2 min-w-[75px] bg-red-600 hover:bg-red-700 text-white" onclick="deleteBlog('${blog.id.replace("'", "[quotetation_here]")}', '${title.replace("'", "[quotetation_here]")}')">
                        <div class="flex items-center gap-2">
                            <i data-lucide="trash-2" class="w-3 h-3"></i>
                            <p>Delete</p>
                        </div>
                    </button>
                </div>
            </div>
        `;
    }).join('');

    lucide.createIcons();
}

function updatePaginationControls() {
    const prevBtn = document.getElementById('prevPage');
    const nextBtn = document.getElementById('nextPage');
    const pageInfo = document.getElementById('pageInfo');

    if (prevBtn) {
        prevBtn.disabled = currentPage <= 1;
    }
    if (nextBtn) {
        nextBtn.disabled = currentPage >= totalPages;
    }
    if (pageInfo) {
        pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    if (!dateString) return 'No date';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    } catch (e) {
        return dateString;
    }
}

let currentEditingBlog = null;
let isEditing = false;

async function editBlog(blogId) {
    blogId = blogId.replace("[quotetation_here]", "'");
    console.log('✏️ Editing blog with ID:', blogId);
    
    if (!blogId) {
        showModal('Error', 'Blog ID not found', 'error');
        return;
    }

    const blog = allFetchedBlogs.find(b => b.id === blogId);
    if (blog) {
        console.log('✓ Found blog to edit:', blog);
        isEditing = true;
        populateEditForm(blog);
        switchToEditMode();
        
        const navbarTabs = document.querySelectorAll('#navbarTabs .tab-button');
        const createBlogTab = Array.from(navbarTabs).find(btn => {
            const text = btn.textContent.trim();
            return text.includes('Add Blogs') || text.includes('Add Blog');
        });
        
        if (createBlogTab) {
            console.log('✓ Clicking Create Blog tab');
            createBlogTab.click();
        } else {
            console.warn('⚠️ Create Blog tab not found, available tabs:', Array.from(navbarTabs).map(t => t.textContent.trim()));
            showContentSection('Add Blogs');
        }
        
        isEditing = false;
    } else {
        showModal('Error', 'Blog not found in the list. Please refresh.', 'error');
    }
}

function populateEditForm(blog) {
    currentEditingBlog = blog;
    
    let blogData = {};
    try {
        if (typeof blog.blog === 'string') {
            blogData = JSON.parse(blog.blog);
        } else if (typeof blog.blog === 'object' && blog.blog !== null) {
            blogData = blog.blog;
        }
    } catch (e) {
        console.error('Failed to parse blog.blog in populateEditForm:', e);
        blogData = {};
    }
    
    console.log('📝 Populating form with blog data:', blogData);

    document.getElementById('mainImageUrl').value = blogData.mainImageUrl || '';
    document.getElementById('mainImageAlt').value = blogData.mainImageAlt || '';
    document.getElementById('blogTitle').value = blogData.blogTitle || '';
    document.getElementById('blogDate').value = blogData.blogDate || '';
    document.getElementById('blogSummary').value = blogData.blogSummary || '';

    const statusRadios = document.querySelectorAll('input[name="blogStatus"]');
    statusRadios.forEach(radio => {
        radio.checked = radio.value === blog.status;
    });

    document.getElementById('blogCategory').value = blogData.blogCategory || '';
    document.getElementById('editorsChoice').checked = blogData.editors_choice === 'Y';

    populateLabelsFromData(blog.keyword || {});

    document.getElementById('seoTitle').value = blogData.seoTitle || '';
    document.getElementById('seoMetaDescription').value = blogData.seoMetaDescription || '';
    document.getElementById('seoCanonicalUrl').value = blogData.seoCanonicalUrl || '';

    document.getElementById('dynamicSections').innerHTML = '';
    sectionCounter = 0;

    // Set the content type if it exists in the blog data
    if (blogData.contentType) {
        const contentType = blogData.contentType;
        document.getElementById('contentType').value = contentType;
        
        // Update the UI to reflect the saved type
        if (contentType === 'BLOG') {
            document.getElementById('blogTypeBtn').classList.add('active');
            document.getElementById('blogTypeBtn').classList.remove('bg-white/10', 'text-white');
            document.getElementById('blogTypeBtn').classList.add('bg-white', 'text-black');
            
            document.getElementById('caseStudyTypeBtn').classList.remove('active');
            document.getElementById('caseStudyTypeBtn').classList.add('bg-white/10', 'text-white');
            document.getElementById('caseStudyTypeBtn').classList.remove('bg-white', 'text-black');
        } else if (contentType === 'CASE STUDY') {
            document.getElementById('caseStudyTypeBtn').classList.add('active');
            document.getElementById('caseStudyTypeBtn').classList.remove('bg-white/10', 'text-white');
            document.getElementById('caseStudyTypeBtn').classList.add('bg-white', 'text-black');
            
            document.getElementById('blogTypeBtn').classList.remove('active');
            document.getElementById('blogTypeBtn').classList.add('bg-white/10', 'text-white');
            document.getElementById('blogTypeBtn').classList.remove('bg-white', 'text-black');
        }
    }

    if (blogData.dynamicSections && Array.isArray(blogData.dynamicSections)) {
        blogData.dynamicSections.forEach(section => {
            const sectionElement = createDynamicSection(section.type, section.content);
            document.getElementById('dynamicSections').appendChild(sectionElement);

            const removeBtn = sectionElement.querySelector('.remove-section');
            removeBtn.addEventListener('click', function () {
                sectionElement.remove();
            });
        });
    }

    console.log('✓ Form populated successfully');
    lucide.createIcons();
}

function switchToEditMode() {
    document.querySelector('#addBlogs .section-title').textContent = 'Edit Blog';

    document.getElementById('blogStatusSection').style.display = 'block';

    document.getElementById('addModeButtons').style.display = 'none';
    document.getElementById('editModeButtons').style.display = 'flex';
}

function switchToAddMode() {
    document.querySelector('#addBlogs .section-title').textContent = 'Add New Blog';

    document.getElementById('blogStatusSection').style.display = 'none';

    document.getElementById('addModeButtons').style.display = 'flex';
    document.getElementById('editModeButtons').style.display = 'none';

    currentEditingBlog = null;

    document.getElementById('addBlogForm').reset();
    document.getElementById('dynamicSections').innerHTML = '';
    sectionCounter = 0;

    document.getElementById('blogCategory').value = '';
    document.getElementById('seoTitle').value = '';
    document.getElementById('seoMetaDescription').value = '';
    document.getElementById('seoCanonicalUrl').value = '';

    const labelsContainer = document.getElementById('labelsContainer');
    labelsContainer.innerHTML = `
        <div class="label-item flex items-center gap-3">
            <div class="flex-1">
                <input type="text" class="label-input form-input" placeholder="Enter label name..." />
            </div>
            <div class="w-24">
                <input type="number" class="weight-input form-input" placeholder="Weight" min="1" max="100" />
            </div>
            <button type="button" class="remove-label-btn text-white/50 hover:text-red-500 transition-colors p-2 rounded-lg hover:bg-white/[0.05]" title="Remove">
                <i data-lucide="x" class="w-4 h-4"></i>
            </button>
        </div>
    `;
    document.getElementById('labelsNotMandatory').checked = false;
    lucide.createIcons();
}

async function handleUpdateBlog() {
    if (!currentEditingBlog) {
        showModal('Error', 'No blog selected for editing', 'error');
        return;
    }

    const labelsResult = collectLabelsData();
    if (labelsResult === null) {
        return;
    }

    const form = document.getElementById('addBlogForm');
    const formData = new FormData(form);
    const data = {};
    for (let [key, value] of formData.entries()) {
        if (!key.startsWith('dynamic_')) {
            data[key] = value;
        }
    }

    data.labels = labelsResult.labels;
    data.labelsNotMandatory = labelsResult.labelsNotMandatory;

    const statusRadio = document.querySelector('input[name="blogStatus"]:checked');
    data.status = statusRadio ? statusRadio.value : 'draft';

    if (!data.blogDate) {
        const today = new Date().toISOString().split('T')[0];
        data.blogDate = today;
        document.getElementById('blogDate').value = today;
    }

    const dynamicSections = collectDynamicSections();
    data.dynamicSections = dynamicSections;

    data.blog_id = currentEditingBlog.id;
    data.base_url = window.location.origin;
    data.reason = 'update';
    
    // Add content type to the data
    data.contentType = document.getElementById('contentType').value || 'BLOG';

    try {
        const updateBlogBtn = document.getElementById('updateBlogBtn');
        const originalText = updateBlogBtn.innerHTML;
        updateBlogBtn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 mr-2 animate-spin"></i>Updating...';
        updateBlogBtn.disabled = true;

        const endpoint = data.contentType === 'CASE STUDY'
            ? `/api/case_studies/${currentEditingBlog.id}`
            : `/api/blogs/${currentEditingBlog.id}`;

        const payload = {
            status: data.status,
            category: data.blogCategory,
            keyword: data.labels
        };

        if (data.contentType === 'CASE STUDY') {
            payload.case_study = data;
        } else {
            payload.blog = data;
        }

        const response = await fetch(endpoint, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        updateBlogBtn.innerHTML = originalText;
        updateBlogBtn.disabled = false;

        if (!response.ok) {
            let errorMessage = `Server error (${response.status})`;
            try {
                const errorResult = await response.json();
                errorMessage = errorResult.message || errorResult.error || errorMessage;
            } catch (e) {
                errorMessage = response.statusText || errorMessage;
            }
            showModal('Error Updating Blog', errorMessage, 'error');
            return;
        }

        const result = await response.json();

        if (result.status === 'success') {
            let message = 'Blog updated successfully!';
            if (result.blog && result.blog.slug) {
                const blogUrl = `${window.location.origin}/blog/${result.blog.slug}`;
                message += `\n\nBlog URL: ${blogUrl}`;
            }
            showModal('Success', message, 'success');

            switchToAddMode();
            showContentSection('Edit/Delete Blog');
        } else {
            showModal('Error Updating Blog', result.message || 'Unknown error', 'error');
        }

    } catch (error) {
        const updateBlogBtn = document.getElementById('updateBlogBtn');
        updateBlogBtn.innerHTML = '<i data-lucide="save" class="w-4 h-4 mr-2"></i>Update Blog';
        updateBlogBtn.disabled = false;

        console.error('Error updating blog:', error);
        showModal('Error Updating Blog', error.message, 'error');
    }
}

function deleteBlog(blogId, blogTitle) {
    blogId = blogId.replace("[quotetation_here]", "'");
    blogTitle = blogTitle.replace("[quotetation_here]", "'");
    console.log('🗑️ Deleting blog - ID:', blogId, 'Title:', blogTitle);
    
    if (!blogId) {
        showModal('Error', 'Blog ID not found', 'error');
        return;
    }

    showDeleteConfirmModal(blogId, blogTitle);
}

document.addEventListener('DOMContentLoaded', function () {
    lucide.createIcons();

    initializeLabelsSection();

    const blogDateInput = document.getElementById('blogDate');
    if (blogDateInput && !blogDateInput.value) {
        const today = new Date().toISOString().split('T')[0];
        blogDateInput.value = today;
    }

    const addBlogForm = document.getElementById('addBlogForm');
    if (addBlogForm) {
        addBlogForm.addEventListener('submit', handleFormSubmit);
    }

    const blogTypeBtn = document.getElementById('blogTypeBtn');
    const caseStudyTypeBtn = document.getElementById('caseStudyTypeBtn');
    const contentTypeInput = document.getElementById('contentType');

    if (blogTypeBtn && caseStudyTypeBtn && contentTypeInput) {
        const toggleContainer = blogTypeBtn.closest('.toggle-switch-buttons');

        function updateTogglePosition(activeBtn, inactiveBtn, index) {
            activeBtn.classList.add('active');
            inactiveBtn.classList.remove('active');
            
            if (toggleContainer) {
                toggleContainer.style.setProperty('--active-index', index.toString());
            }
        }

        blogTypeBtn.addEventListener('click', function() {
            updateTogglePosition(blogTypeBtn, caseStudyTypeBtn, 0);
            contentTypeInput.value = 'BLOG';
        });

        caseStudyTypeBtn.addEventListener('click', function() {
            updateTogglePosition(caseStudyTypeBtn, blogTypeBtn, 1);
            contentTypeInput.value = 'CASE STUDY';
        });
    }
    
    const filterBlogTypeBtn = document.getElementById('filterBlogTypeBtn');
    const filterBlogsTypeBtn = document.getElementById('filterBlogsTypeBtn');
    const filterCaseStudiesTypeBtn = document.getElementById('filterCaseStudiesTypeBtn');
    const filterContentTypeInput = document.getElementById('filterContentType');

    if (filterBlogTypeBtn && filterBlogsTypeBtn && filterCaseStudiesTypeBtn && filterContentTypeInput) {
        const filterToggleContainer = filterBlogTypeBtn.closest('.toggle-switch-buttons');

        function updateFilterTogglePosition(activeBtn, index, ...inactiveBtns) {
            activeBtn.classList.add('active');
            inactiveBtns.forEach(btn => btn.classList.remove('active'));
            
            if (filterToggleContainer) {
                filterToggleContainer.style.setProperty('--active-index', index.toString());
            }
        }

        filterBlogTypeBtn.addEventListener('click', function() {
            updateFilterTogglePosition(filterBlogTypeBtn, 0, filterBlogsTypeBtn, filterCaseStudiesTypeBtn);
            filterContentTypeInput.value = 'ALL';
            applyFiltersAndRender(1);
        });

        filterBlogsTypeBtn.addEventListener('click', function() {
            updateFilterTogglePosition(filterBlogsTypeBtn, 1, filterBlogTypeBtn, filterCaseStudiesTypeBtn);
            filterContentTypeInput.value = 'BLOG';
            applyFiltersAndRender(1);
        });

        filterCaseStudiesTypeBtn.addEventListener('click', function() {
            updateFilterTogglePosition(filterCaseStudiesTypeBtn, 2, filterBlogTypeBtn, filterBlogsTypeBtn);
            filterContentTypeInput.value = 'CASE STUDY';
            applyFiltersAndRender(1);
        });
    }


    const loadPreviewBtn = document.getElementById('loadPreviewBtn');
    if (loadPreviewBtn) {
        loadPreviewBtn.addEventListener('click', handleLoadPreview);
    }


    const saveDraftBtn = document.getElementById('saveDraftBtn');
    if (saveDraftBtn) {
        saveDraftBtn.addEventListener('click', handleSaveDraft);
    }


    const savePublishBtn = document.getElementById('savePublishBtn');
    if (savePublishBtn) {
        savePublishBtn.addEventListener('click', handleSavePublish);
    }

    const loadPreviewEditBtn = document.getElementById('loadPreviewEditBtn');
    if (loadPreviewEditBtn) {
        loadPreviewEditBtn.addEventListener('click', handleLoadPreview);
    }

    const deleteBlogBtn = document.getElementById('deleteBlogBtn');
    if (deleteBlogBtn) {
        deleteBlogBtn.addEventListener('click', function () {
            if (currentEditingBlog) {
                const title = currentEditingBlog.json_data?.blogTitle || 'Untitled';
                deleteBlog(currentEditingBlog.id, title);
            }
        });
    }

    const updateBlogBtn = document.getElementById('updateBlogBtn');
    if (updateBlogBtn) {
        updateBlogBtn.addEventListener('click', handleUpdateBlog);
    }


    document.getElementById('addTextBtn').addEventListener('click', () => addDynamicSection('text'));
    document.getElementById('addH1Btn').addEventListener('click', () => addDynamicSection('h1'));
    document.getElementById('addH2Btn').addEventListener('click', () => addDynamicSection('h2'));
    document.getElementById('addH3Btn').addEventListener('click', () => addDynamicSection('h3'));
    document.getElementById('addH4Btn').addEventListener('click', () => addDynamicSection('h4'));
    document.getElementById('addH5Btn').addEventListener('click', () => addDynamicSection('h5'));
    document.getElementById('addImageBtn').addEventListener('click', () => addDynamicSection('image'));

    const filterTitleInput = document.getElementById('filterTitle');
    const filterCategoryInput = document.getElementById('filterCategory');

    function setupFilterListeners() {
        const applyFilters = () => applyFiltersAndRender(1);

        const debounce = (func, delay) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(func, delay);
        };

        console.log('✓ Setting up filter listeners (Title, Category and Type text inputs)');
        filterTitleInput.addEventListener('input', () => debounce(applyFilters, 300));
        filterCategoryInput.addEventListener('input', () => debounce(applyFilters, 300));
        
        // Add listener for type filter buttons
        const filterBlogTypeBtn = document.getElementById('filterBlogTypeBtn');
        const filterBlogsTypeBtn = document.getElementById('filterBlogsTypeBtn');
        const filterCaseStudiesTypeBtn = document.getElementById('filterCaseStudiesTypeBtn');
        
        if (filterBlogTypeBtn) {
            filterBlogTypeBtn.addEventListener('click', () => applyFiltersAndRender(1));
        }
        
        if (filterBlogsTypeBtn) {
            filterBlogsTypeBtn.addEventListener('click', () => applyFiltersAndRender(1));
        }
        
        if (filterCaseStudiesTypeBtn) {
            filterCaseStudiesTypeBtn.addEventListener('click', () => applyFiltersAndRender(1));
        }
    }

    setupFilterListeners();

    const prevPage = document.getElementById('prevPage');
    const nextPage = document.getElementById('nextPage');

    if (prevPage) {
        prevPage.addEventListener('click', () => {
            if (currentPage > 1) {
                applyFiltersAndRender(currentPage - 1);
            }
        });
    }

    if (nextPage) {
        nextPage.addEventListener('click', () => {
            if (currentPage < totalPages) {
                applyFiltersAndRender(currentPage + 1);
            }
        });
    }

    const originalShowContentSection = showContentSection;
    showContentSection = function (tabTitle) {
        if (tabTitle !== 'Add Blogs' && currentEditingBlog) {
            switchToAddMode();
        }

        originalShowContentSection(tabTitle);

        if (tabTitle === 'Edit/Delete Blog') {
            setTimeout(() => {
                fetchBlogs();
            }, 100);
        }
    };

    const navbarTabs = [
        { title: "Add Blogs", icon: "plus-circle" },
        { title: "Edit/Delete Blog", icon: "edit" },
    ];
    const navbarContainer = document.getElementById('navbarTabs');
    const expandableTabs = new ExpandableTabs(navbarContainer, {
        tabs: navbarTabs,
        activeColor: 'text-blue-400',
        onChange: (index) => {
            console.log('Navbar tab changed:', index);
            if (index !== null && navbarTabs[index]) {
                console.log('Selected tab:', navbarTabs[index].title);
                if (navbarTabs[index].title === "Add Blogs") {
                    if (!isEditing) {
                        switchToAddMode();
                    }
                    showContentSection('Add Blogs');
                } else if (navbarTabs[index].title === "Edit/Delete Blog") {
                    showContentSection('Edit/Delete Blog');
                }
            }
        }
    });
    expandableTabs.selected = 0;
    expandableTabs.render();

    const leftTabButtons = document.querySelectorAll('.left-tab-button');
    const leftContentSections = document.querySelectorAll('.left-content-section');

    leftTabButtons.forEach(button => {
        button.addEventListener('click', function () {
            const tabName = this.getAttribute('data-left-tab');

            leftTabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            leftContentSections.forEach(section => section.classList.remove('active'));
            const targetSection = document.getElementById(tabName + 'Content');
            if (targetSection) {
                targetSection.classList.add('active');
            }

            if (tabName === 'storage') {
                setTimeout(() => {
                    loadGallery();
                    loadMagazines();
                }, 100);
            }
        });
    });

    const storageSubTabs = document.querySelectorAll('.storage-sub-tab');
    const storageSubContents = document.querySelectorAll('.storage-sub-content');

    storageSubTabs.forEach(tab => {
        tab.addEventListener('click', function () {
            const subTabName = this.getAttribute('data-storage-tab');

            storageSubTabs.forEach(subTab => {
                subTab.classList.remove('active');
                subTab.style.background = 'rgba(255, 255, 255, 0.05)';
                subTab.style.color = 'rgba(255, 255, 255, 0.6)';
                subTab.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            });

            this.classList.add('active');
            this.style.background = 'rgba(59, 130, 246, 0.2)';
            this.style.color = 'white';
            this.style.borderColor = 'rgba(59, 130, 246, 0.4)';

            storageSubContents.forEach(content => content.classList.remove('active'));

            const targetSubContent = document.getElementById(subTabName + 'SubContent');
            if (targetSubContent) {
                targetSubContent.classList.add('active');
            }

            if (subTabName === 'gallery') {
                setTimeout(() => loadGallery(), 100);
            } else if (subTabName === 'magazines') {
                setTimeout(() => loadMagazines(), 100);
            }
        });
    });

    let imageFilesToUpload = [];
    let magazineFilesToUpload = [];
    let imageFiles = [];
    let magazineFiles = [];

    const magazineDropzone = document.getElementById('magazineDropzone');
    const magazineFileInput = document.getElementById('magazineFileInput');
    const magazineFileQueue = document.getElementById('magazineFileQueue');
    const magazineUploadBtn = document.getElementById('magazineUploadBtn');
    const magazineUploadBtnText = document.getElementById('magazineUploadBtnText');

    if (magazineDropzone && magazineFileInput) {
        setupFileUpload(
            magazineDropzone, magazineFileInput, magazineFileQueue, magazineUploadBtn, magazineUploadBtnText,
            magazineFilesToUpload, 'pdf', 'magazines'
        );
    }

    function setupFileUpload(dropzone, fileInput, fileQueue, uploadBtn, uploadBtnText, filesToUpload, fileType, displayType) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, e => { e.preventDefault(); e.stopPropagation(); });
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropzone.addEventListener(eventName, () => dropzone.classList.add('dragover'));
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, () => dropzone.classList.remove('dragover'));
        });

        dropzone.addEventListener('drop', (e) => handleFiles(e.dataTransfer.files, fileType, filesToUpload, fileQueue, uploadBtn, uploadBtnText));
        fileInput.addEventListener('change', (e) => handleFiles(e.target.files, fileType, filesToUpload, fileQueue, uploadBtn, uploadBtnText));

        uploadBtn.addEventListener('click', async () => {
            if (filesToUpload.length === 0) {
                showToast(`No ${displayType} selected for upload`, 'error');
                return;
            }

            uploadBtn.disabled = true;
            uploadBtnText.textContent = 'Uploading...';

            let successCount = 0;
            let errorCount = 0;
            let errorMessages = [];

            for (let i = 0; i < filesToUpload.length; i++) {
                const file = filesToUpload[i];
                try {
                    const formData = new FormData();
                    formData.append('file', file);

                    const response = await fetch('/upload_file', {
                        method: 'POST',
                        body: formData
                    });

                    const result = await response.json();

                    if (response.ok && result.status === 'success') {
                        successCount++;
                    } else {
                        errorCount++;
                        errorMessages.push(result.message || `Failed to upload ${file.name}`);
                        console.error(`Failed to upload ${file.name}:`, result.message);
                    }
                } catch (error) {
                    errorCount++;
                    errorMessages.push(`Network error uploading ${file.name}`);
                    console.error(`Network error uploading ${file.name}:`, error);
                }

                uploadBtnText.textContent = `Uploading... (${i + 1}/${filesToUpload.length})`;
            }

            if (successCount > 0 && errorCount === 0) {
                showToast(`Successfully uploaded ${successCount} ${displayType.slice(0, -1)}${successCount !== 1 ? 's' : ''}!`, 'success');
            } else if (successCount > 0 && errorCount > 0) {
                showToast(`Uploaded ${successCount} ${displayType} successfully, but ${errorCount} failed: ${errorMessages.join(', ')}`, 'warning');
            } else {
                showToast(`All uploads failed: ${errorMessages.join(', ')}`, 'error');
            }

            if (successCount > 0) {
                if (fileType === 'image') {
                    await loadGallery();
                } else if (fileType === 'pdf') {
                    await loadMagazines();
                }
            }

            filesToUpload.length = 0;
            updateFileQueueUI(filesToUpload, fileQueue, uploadBtn, uploadBtnText);
        });

        fileQueue.addEventListener('click', (e) => {
            const removeBtn = e.target.closest('.remove-file-btn');
            if (removeBtn) {
                filesToUpload.splice(parseInt(removeBtn.dataset.index), 1);
                updateFileQueueUI(filesToUpload, fileQueue, uploadBtn, uploadBtnText);
            }
        });
    }

    function handleFiles(files, fileType, filesToUpload, fileQueue, uploadBtn, uploadBtnText) {
        const validFiles = [];
        const invalidFiles = [];

        Array.from(files).forEach(file => {
            if (fileType === 'image') {
                if (file.type.startsWith('image/') &&
                    ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/bmp', 'image/svg+xml'].includes(file.type.toLowerCase())) {
                    validFiles.push(file);
                } else {
                    invalidFiles.push(file);
                }
            } else if (fileType === 'pdf') {
                if (file.name.toLowerCase().endsWith('.pdf') &&
                    (file.type === 'application/pdf' || file.type === '')) {
                    validFiles.push(file);
                } else {
                    invalidFiles.push(file);
                }
            }
        });

        if (invalidFiles.length > 0) {
            const fileNames = invalidFiles.map(f => f.name).join(', ');
            const expectedTypes = fileType === 'image' ? 'PNG, JPG, JPEG, GIF, WEBP, BMP, SVG' : 'PDF';
            showToast(`Invalid file type(s): ${fileNames}. Expected: ${expectedTypes}`, 'error');
        }

        if (validFiles.length > 0) {
            filesToUpload.push(...validFiles);
            updateFileQueueUI(filesToUpload, fileQueue, uploadBtn, uploadBtnText);
        }
    }

    function updateFileQueueUI(filesToUpload, fileQueue, uploadBtn, uploadBtnText) {
        fileQueue.innerHTML = '';
        if (filesToUpload.length > 0) {
            filesToUpload.forEach((file, index) => {
                const fileItem = document.createElement('div');
                fileItem.className = 'file-queue-item';
                const iconName = file.type.startsWith('image/') ? 'image' : 'file-text';
                fileItem.innerHTML = `
                    <div class="flex-shrink-0 mr-3">
                        <i data-lucide="${iconName}" class="w-5 h-5 text-white/70"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium truncate">${file.name}</p>
                        <p class="text-xs text-white/50">${(file.size / 1024 / 1024).toFixed(2)} MB</p>
                    </div>
                    <button data-index="${index}" class="remove-file-btn ml-4 text-white/50 hover:text-red-500 transition-colors p-1">
                        <i data-lucide="x" class="w-5 h-5"></i>
                    </button>
                `;
                fileQueue.appendChild(fileItem);
            });
            lucide.createIcons();
        }
        uploadBtn.disabled = filesToUpload.length === 0;
        uploadBtnText.textContent = `Upload ${filesToUpload.length} File${filesToUpload.length !== 1 ? 's' : ''}`;
    }

    async function loadGallery() {
        try {
            const response = await fetch('/get_file_details?bucket_name=blog-images');
            const result = await response.json();

            if (result.status === 'success' && result.data) {
                imageFiles = result.data.map(file => ({
                    id: file.id,
                    name: file.name,
                    url: file.public_url,
                    size: file.size
                }));
                renderGallery();
            }
        } catch (error) {
            console.error('Error loading gallery:', error);
        }
    }

    async function loadMagazines() {
        try {
            const response = await fetch('/get_file_details?bucket_name=magazine-pdfs');
            const result = await response.json();

            if (result.status === 'success' && result.data) {
                magazineFiles = result.data
                    .filter(file => file.name.toLowerCase().endsWith('.pdf'))
                    .map(file => ({
                        id: file.id,
                        name: file.name,
                        url: file.public_url,
                        size: file.size
                    }));
                renderMagazines();
            }
        } catch (error) {
            console.error('Error loading magazines:', error);
        }
    }

    function renderGallery(searchTerm = '') {
        const galleryGrid = document.getElementById('galleryGrid');
        const noItemsDiv = document.getElementById('noGalleryItems');

        if (!galleryGrid) return;

        let filteredImages = imageFiles;
        if (searchTerm) {
            filteredImages = imageFiles.filter(item =>
                item.name.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }

        galleryGrid.innerHTML = '';

        if (filteredImages.length === 0) {
            noItemsDiv.classList.remove('hidden');
        } else {
            noItemsDiv.classList.add('hidden');
            filteredImages.forEach(item => {
                const itemEl = document.createElement('div');
                itemEl.className = 'gallery-item group aspect-square';
                itemEl.innerHTML = `
                    <img src="${item.url}" alt="${item.name}" class="absolute inset-0 w-full h-full object-cover" loading="lazy">
                    <div class="overlay"></div>
                    <div class="relative z-10 text-white p-2 flex flex-col justify-end h-full opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                        <p class="text-xs font-semibold truncate">${item.name}</p>
                    </div>
                    <div class="actions">
                        <button class="action-btn" data-action="copy" data-url="${item.url}" title="Copy URL">
                            <i data-lucide="link" class="w-3 h-3 text-white"></i>
                        </button>
                        <button class="action-btn" data-action="view" data-url="${item.url}" title="View">
                            <i data-lucide="external-link" class="w-3 h-3 text-white"></i>
                        </button>
                        <button class="action-btn delete" data-action="delete" data-id="${item.id}" data-name="${item.name}" title="Delete">
                            <i data-lucide="trash-2" class="w-3 h-3 text-white"></i>
                        </button>
                    </div>
                `;
                galleryGrid.appendChild(itemEl);
            });
        }
        lucide.createIcons();
    }

    function renderMagazines(searchTerm = '') {
        const magazinesGrid = document.getElementById('magazinesGrid');
        const noItemsDiv = document.getElementById('noMagazineItems');

        if (!magazinesGrid) return;

        let filteredMagazines = magazineFiles;
        if (searchTerm) {
            filteredMagazines = magazineFiles.filter(item =>
                item.name.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }

        magazinesGrid.innerHTML = '';

        if (filteredMagazines.length === 0) {
            noItemsDiv.classList.remove('hidden');
        } else {
            noItemsDiv.classList.add('hidden');
            filteredMagazines.forEach(item => {
                const itemEl = document.createElement('div');
                itemEl.className = 'gallery-item group aspect-[3/4]';
                itemEl.innerHTML = `
                    <div class="absolute inset-0 w-full h-full bg-white/5 border border-white/20 rounded-lg flex flex-col items-center justify-center">
                        <i data-lucide="file-text" class="w-12 h-12 text-white/60 mb-2"></i>
                        <p class="text-xs text-white/80 text-center px-2">${item.name}</p>
                        <p class="text-xs text-white/50 mt-1">${item.size}</p>
                    </div>
                    <div class="overlay"></div>
                    <div class="actions">
                        <button class="action-btn" data-action="copy" data-url="${item.url}" title="Copy URL">
                            <i data-lucide="link" class="w-3 h-3 text-white"></i>
                        </button>
                        <button class="action-btn" data-action="view" data-url="${item.url}" title="View">
                            <i data-lucide="external-link" class="w-3 h-3 text-white"></i>
                        </button>
                        <button class="action-btn delete" data-action="delete" data-id="${item.id}" data-name="${item.name}" title="Delete">
                            <i data-lucide="trash-2" class="w-3 h-3 text-white"></i>
                        </button>
                    </div>
                `;
                magazinesGrid.appendChild(itemEl);
            });
        }
        lucide.createIcons();
    }

    const galleryGrid = document.getElementById('galleryGrid');
    const magazinesGrid = document.getElementById('magazinesGrid');

    if (galleryGrid) {
        galleryGrid.addEventListener('click', (e) => {
            const actionBtn = e.target.closest('.action-btn');
            if (!actionBtn) return;

            const action = actionBtn.dataset.action;
            const itemUrl = actionBtn.dataset.url;
            const itemId = actionBtn.dataset.id;
            const itemName = actionBtn.dataset.name;

            if (action === 'copy') {
                if (navigator.clipboard && window.isSecureContext) {
                    navigator.clipboard.writeText(itemUrl).then(() => {
                        showToast('URL copied to clipboard!', 'success');
                    }).catch(() => {
                        fallbackCopyTextToClipboard(itemUrl);
                    });
                } else {
                    fallbackCopyTextToClipboard(itemUrl);
                }
            } else if (action === 'view') {
                window.open(itemUrl, '_blank');
            } else if (action === 'delete') {
                handleGalleryDelete(itemId, itemName, 'image');
            }
        });
    }

    if (magazinesGrid) {
        magazinesGrid.addEventListener('click', (e) => {
            const actionBtn = e.target.closest('.action-btn');
            if (!actionBtn) return;

            const action = actionBtn.dataset.action;
            const itemUrl = actionBtn.dataset.url;
            const itemId = actionBtn.dataset.id;
            const itemName = actionBtn.dataset.name;

            if (action === 'copy') {
                if (navigator.clipboard && window.isSecureContext) {
                    navigator.clipboard.writeText(itemUrl).then(() => {
                        showToast('URL copied to clipboard!', 'success');
                    }).catch(() => {
                        fallbackCopyTextToClipboard(itemUrl);
                    });
                } else {
                    fallbackCopyTextToClipboard(itemUrl);
                }
            } else if (action === 'view') {
                window.open(itemUrl, '_blank');
            } else if (action === 'delete') {
                handleGalleryDelete(itemId, itemName, 'magazine');
            }
        });
    }

    const magazinesSearchInput = document.getElementById('magazinesSearchInput');

    if (magazinesSearchInput) {
        const magazinesSearchContainer = magazinesSearchInput.parentElement;

        magazinesSearchInput.addEventListener('focus', () => {
            magazinesSearchContainer.classList.add('focused');
        });

        magazinesSearchInput.addEventListener('blur', () => {
            magazinesSearchContainer.classList.remove('focused');
        });

        magazinesSearchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.trim();
            renderMagazines(searchTerm);
        });
    }

    function fallbackCopyTextToClipboard(text) {
        const textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        textArea.style.top = "0";
        textArea.style.left = "0";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            showToast('URL copied to clipboard!', 'success');
        } catch (err) {
            console.error('Failed to copy', err);
            showToast('Failed to copy URL', 'error');
        }
        document.body.removeChild(textArea);
    }

    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        let bgColor = 'bg-green-600';
        if (type === 'error') {
            bgColor = 'bg-red-600';
        } else if (type === 'warning') {
            bgColor = 'bg-yellow-600';
        }
        toast.className = `fixed top-4 right-4 ${bgColor} text-white px-4 py-2 rounded-lg shadow-lg z-50 transition-all duration-300`;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                if (toast.parentElement) {
                    document.body.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }

    async function handleGalleryDelete(itemId, itemName, type) {
        if (!itemName) {
            console.error('No file name provided to handleGalleryDelete');
            showToast('Error: File name is missing', 'error');
            return;
        }

        const displayType = type === 'image' ? 'image' : 'magazine';

        if (confirm(`Are you sure you want to delete "${itemName}"? This action cannot be undone.`)) {
            showToast('Deleting file...', 'success');

            try {
                const response = await fetch('/delete_file', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        file_name: itemName
                    })
                });

                const result = await response.json();

                if (response.ok && result.status === 'success') {
                    if (type === 'image') {
                        const itemIndex = imageFiles.findIndex(item => item.id == itemId);
                        if (itemIndex > -1) {
                            imageFiles.splice(itemIndex, 1);
                            renderGallery();
                        } else {
                            await loadGallery();
                        }
                    } else {
                        const itemIndex = magazineFiles.findIndex(item => item.id == itemId);
                        if (itemIndex > -1) {
                            magazineFiles.splice(itemIndex, 1);
                            renderMagazines();
                        } else {
                            await loadMagazines();
                        }
                    }
                    showToast(`${displayType.charAt(0).toUpperCase() + displayType.slice(1)} "${itemName}" deleted successfully!`, 'success');
                } else {
                    console.error('Delete failed:', result.message);
                    showToast(`Failed to delete ${displayType}: ${result.message || 'Unknown error'}`, 'error');
                }
            } catch (error) {
                console.error('Error deleting file:', error);
                showToast(`Error deleting ${displayType}: ${error.message}`, 'error');
            }
        }
    }

    setTimeout(() => {
        lucide.createIcons();
    }, 100);
});

document.addEventListener('DOMContentLoaded', function() {
    const imageFileInput = document.getElementById('imageFileInput');
    const imageDropzone = document.getElementById('imageDropzone');
    const imageFileQueue = document.getElementById('imageFileQueue');
    const imageUploadBtn = document.getElementById('imageUploadBtn');
    const imageUploadBtnText = document.getElementById('imageUploadBtnText');
    
    let selectedFiles = [];

    if (imageDropzone) {
        imageDropzone.addEventListener('click', function(e) {
            if (e.target.tagName !== 'BUTTON') {
                imageFileInput.click();
            }
        });

        imageDropzone.addEventListener('dragover', function(e) {
            e.preventDefault();
            imageDropzone.classList.add('dragover');
        });

        imageDropzone.addEventListener('dragleave', function() {
            imageDropzone.classList.remove('dragover');
        });

        imageDropzone.addEventListener('drop', function(e) {
            e.preventDefault();
            imageDropzone.classList.remove('dragover');
            
            const files = Array.from(e.dataTransfer.files).filter(file => 
                file.type.startsWith('image/')
            );
            
            if (files.length > 0) {
                handleImageFiles(files);
            }
        });
    }

    if (imageFileInput) {
        imageFileInput.addEventListener('change', function(e) {
            const files = Array.from(e.target.files);
            if (files.length > 0) {
                handleImageFiles(files);
            }
            imageFileInput.value = '';
        });
    }

    function handleImageFiles(files) {
        files.forEach(file => {
            if (!selectedFiles.find(f => f.name === file.name)) {
                selectedFiles.push(file);
                addFileToQueue(file);
            }
        });
        updateUploadButton();
    }

    function addFileToQueue(file) {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-queue-item flex items-center justify-between p-3 rounded-lg bg-white/5 border border-white/10';
        fileItem.dataset.fileName = file.name;
        
        const fileInfo = document.createElement('div');
        fileInfo.className = 'flex items-center gap-3 flex-1';
        
        const icon = document.createElement('i');
        icon.setAttribute('data-lucide', 'image');
        icon.className = 'w-5 h-5 text-white/60';
        
        const textInfo = document.createElement('div');
        textInfo.className = 'flex-1';
        
        const fileName = document.createElement('p');
        fileName.className = 'text-sm text-white/90 truncate';
        fileName.textContent = file.name;
        
        const fileSize = document.createElement('p');
        fileSize.className = 'text-xs text-white/50';
        fileSize.textContent = formatFileSize(file.size);
        
        textInfo.appendChild(fileName);
        textInfo.appendChild(fileSize);
        fileInfo.appendChild(icon);
        fileInfo.appendChild(textInfo);
        
        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'p-2 rounded-lg hover:bg-white/10 transition-colors';
        removeBtn.innerHTML = '<i data-lucide="x" class="w-4 h-4 text-white/60"></i>';
        removeBtn.onclick = function() {
            selectedFiles = selectedFiles.filter(f => f.name !== file.name);
            fileItem.remove();
            updateUploadButton();
        };
        
        fileItem.appendChild(fileInfo);
        fileItem.appendChild(removeBtn);
        imageFileQueue.appendChild(fileItem);
        
        lucide.createIcons();
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
    }

    function updateUploadButton() {
        if (selectedFiles.length > 0) {
            imageUploadBtn.disabled = false;
            imageUploadBtnText.textContent = `Upload ${selectedFiles.length} File${selectedFiles.length > 1 ? 's' : ''}`;
        } else {
            imageUploadBtn.disabled = true;
            imageUploadBtnText.textContent = 'Upload 0 Files';
        }
    }

    if (imageUploadBtn) {
        imageUploadBtn.addEventListener('click', async function() {
            if (selectedFiles.length === 0) return;
            
            imageUploadBtn.disabled = true;
            imageUploadBtnText.textContent = 'Uploading...';
            
            try {
                let successCount = 0;
                let failCount = 0;
                
                for (const file of selectedFiles) {
                    const formData = new FormData();
                    formData.append('file', file);
                    
                    try {
                        const response = await fetch('/api/upload-image', {
                            method: 'POST',
                            body: formData
                        });
                        
                        if (response.ok) {
                            successCount++;
                            const fileItem = imageFileQueue.querySelector(`[data-file-name="${file.name}"]`);
                            if (fileItem) fileItem.remove();
                        } else {
                            failCount++;
                        }
                    } catch (error) {
                        failCount++;
                        console.error('Upload error:', error);
                    }
                }
                
                selectedFiles = [];
                updateUploadButton();
                
                if (successCount > 0) {
                    showModal('Success', `${successCount} image${successCount > 1 ? 's' : ''} uploaded successfully!`, 'success');
                    loadGalleryImages();
                }
                
                if (failCount > 0) {
                    showModal('Warning', `${failCount} image${failCount > 1 ? 's' : ''} failed to upload.`, 'error');
                }
                
            } catch (error) {
                console.error('Upload error:', error);
                showModal('Error', 'Failed to upload images. Please try again.', 'error');
            } finally {
                imageUploadBtn.disabled = false;
                updateUploadButton();
            }
        });
    }

    loadGalleryImages();
});

async function loadGalleryImages() {
    const galleryGrid = document.getElementById('galleryGrid');
    const noGalleryItems = document.getElementById('noGalleryItems');
    
    if (!galleryGrid) return;
    
    try {
        const response = await fetch('/api/list-images');
        const data = await response.json();
        
        if (data.status === 'success' && data.images.length > 0) {
            galleryGrid.innerHTML = '';
            noGalleryItems.classList.add('hidden');
            
            data.images.forEach(image => {
                const imageItem = createGalleryItem(image);
                galleryGrid.appendChild(imageItem);
            });
            
            lucide.createIcons();
        } else {
            galleryGrid.innerHTML = '';
            noGalleryItems.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Failed to load gallery images:', error);
        showModal('Error', 'Failed to load gallery images.', 'error');
    }
}

function createGalleryItem(image) {
    const item = document.createElement('div');
    item.className = 'gallery-item relative rounded-lg overflow-hidden aspect-square cursor-pointer';
    item.dataset.imageUrl = image.public_url;
    item.dataset.imageName = image.object_name;
    
    const img = document.createElement('img');
    img.src = image.public_url;
    img.alt = image.object_name;
    img.className = 'w-full h-full object-cover';
    
    const overlay = document.createElement('div');
    overlay.className = 'overlay absolute inset-0 bg-gradient-to-t from-black/80 to-transparent opacity-0 hover:opacity-100 transition-opacity';
    
    const actions = document.createElement('div');
    actions.className = 'actions absolute top-2 right-2 flex gap-2';
    
    const copyBtn = document.createElement('button');
    copyBtn.className = 'p-2 rounded-full bg-black/50 hover:bg-black transition-colors';
    copyBtn.innerHTML = '<i data-lucide="copy" class="w-4 h-4 text-white"></i>';
    copyBtn.title = 'Copy URL';
    copyBtn.onclick = function(e) {
        e.stopPropagation();
        copyImageUrl(image.public_url);
    };
    
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'p-2 rounded-full bg-black/50 hover:bg-red-600 transition-colors';
    deleteBtn.innerHTML = '<i data-lucide="trash-2" class="w-4 h-4 text-white"></i>';
    deleteBtn.title = 'Delete Image';
    deleteBtn.onclick = function(e) {
        e.stopPropagation();
        deleteImage(image.object_name);
    };
    
    actions.appendChild(copyBtn);
    actions.appendChild(deleteBtn);
    
    item.appendChild(img);
    item.appendChild(overlay);
    item.appendChild(actions);
    
    item.addEventListener('click', function() {
        selectGalleryImage(item, image.public_url);
    });
    
    return item;
}

function selectGalleryImage(item, imageUrl) {
    document.querySelectorAll('.gallery-item').forEach(el => {
        el.classList.remove('selected');
    });
    
    item.classList.add('selected');
    
    const mainImageUrlInput = document.getElementById('mainImageUrl');
    if (mainImageUrlInput) {
        mainImageUrlInput.value = imageUrl;
        mainImageUrlInput.dispatchEvent(new Event('input'));
    }
    
    showModal('Image Selected', `Image URL copied to Main Image field:\n${imageUrl}`, 'success');
}

function copyImageUrl(url) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(url).then(() => {
            showModal('Copied', 'Image URL copied to clipboard!', 'success');
        }).catch(() => {
            fallbackCopyText(url);
        });
    } else {
        fallbackCopyText(url);
    }
}

function fallbackCopyText(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.top = "0";
    textArea.style.left = "0";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showModal('Copied', 'Image URL copied to clipboard!', 'success');
    } catch (err) {
        showModal('Error', 'Failed to copy URL.', 'error');
    }
    
    document.body.removeChild(textArea);
}

async function deleteImage(objectName) {
    if (!confirm('Are you sure you want to delete this image?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/delete-image/${encodeURIComponent(objectName)}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showModal('Success', 'Image deleted successfully!', 'success');
            loadGalleryImages();
        } else {
            showModal('Error', data.message || 'Failed to delete image.', 'error');
        }
    } catch (error) {
        console.error('Delete error:', error);
        showModal('Error', 'Failed to delete image. Please try again.', 'error');
    }
}
