import { showLoading, verifyAuth, handleLogout, getCookie, deleteCookie, initAuth, authenticatedFetch } from './shared/auth-utils.js';
import { showModal, closeModal } from './shared/ui-utils.js';
import { initGalleryOnLoad } from './shared/gallery-utils.js';
import { ExpandableTabs } from './shared/admin-tabs.js';
import { initializeLabelsSection, addLabelRow, populateLabelsFromData, collectLabelsData } from './shared/admin-labels.js';
import {
    showLinkDialog, closeLinkModal, insertLink,
    showBulletDialog, closeBulletModal, insertBulletList, addBulletPoint, resetBulletPoints,
    showDeleteConfirmModal, closeDeleteConfirmModal, updateDeleteButtonState, confirmDeleteBlog,
    showBlogUrl, closeBlogUrlModal, copyBlogUrl, openBlogInNewTab, initModalEventListeners
} from './shared/admin-modals.js';

window.closeModal = closeModal;
window.showModal = showModal;
window.closeLinkModal = closeLinkModal;
window.closeBulletModal = closeBulletModal;
window.closeDeleteConfirmModal = closeDeleteConfirmModal;
window.closeBlogUrlModal = closeBlogUrlModal;
window.copyBlogUrl = copyBlogUrl;
window.openBlogInNewTab = openBlogInNewTab;
window.handleLogout = handleLogout;

initAuth();
initGalleryOnLoad();
initModalEventListeners();

function showContentSection(tabTitle) {

    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });


    let sectionId = '';
    switch (tabTitle) {
        case 'Add Blogs':
            sectionId = 'addBlogs';
            break;
        case 'Edit/Delete Blog':
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
        const blogDateInput = document.getElementById('blogDate');
        if (blogDateInput) blogDateInput.value = today;
    }


    const dynamicSections = collectDynamicSections();
    data.dynamicSections = dynamicSections;

    try {

        const loadPreviewBtn = document.getElementById('loadPreviewBtn');
        const originalText = loadPreviewBtn.innerHTML;
        loadPreviewBtn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 mr-2 animate-spin"></i>Loading...';
        loadPreviewBtn.disabled = true;


        const endpoint = '/api/admin_blog_preview';

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
        const blogDateInput = document.getElementById('blogDate');
        if (blogDateInput) blogDateInput.value = today;
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

        const endpoint = '/api/admin_save_blog';
        const response = await authenticatedFetch(endpoint, {
            method: 'POST',
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
        const blogDateInput = document.getElementById('blogDate');
        if (blogDateInput) blogDateInput.value = today;
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

        const endpoint = '/api/admin_save_blog';
        const response = await authenticatedFetch(endpoint, {
            method: 'POST',
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

            const dynamicSectionsContainer = document.getElementById('dynamicSections');
            if (dynamicSectionsContainer) {
                dynamicSectionsContainer.innerHTML = '';
            }
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
                <div contenteditable="true" data-name="dynamic_text_${sectionId}" class="form-input content-editable" style="min-height: 4rem; max-height: 20rem; overflow-y: auto;" data-placeholder="Enter your text content...">${content}</div>
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
                <div contenteditable="true" data-name="dynamic_h1_${sectionId}" class="form-input content-editable" data-placeholder="Enter H2 header text...">${content}</div>
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
                <div contenteditable="true" data-name="dynamic_h2_${sectionId}" class="form-input content-editable" data-placeholder="Enter H3 header text...">${content}</div>
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
                <div contenteditable="true" data-name="dynamic_h3_${sectionId}" class="form-input content-editable" data-placeholder="Enter H4 header text...">${content}</div>
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
                <div contenteditable="true" data-name="dynamic_h4_${sectionId}" class="form-input content-editable" data-placeholder="Enter H5 header text...">${content}</div>
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

    const contentEditables = section.querySelectorAll('[contenteditable="true"]');
    contentEditables.forEach(editable => {
        editable.addEventListener('input', updatePreviewIfVisible);
        
        editable.addEventListener('focus', function() {
            if (this.textContent === '' && this.dataset.placeholder) {
                this.classList.remove('empty');
            }
        });
        
        editable.addEventListener('blur', function() {
            if (this.textContent.trim() === '') {
                this.classList.add('empty');
            }
        });
        
        if (editable.textContent.trim() === '') {
            editable.classList.add('empty');
        }
    });

    const formatBtns = section.querySelectorAll('.format-btn');
    formatBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const format = this.dataset.format;
            const textInput = section.querySelector('[contenteditable="true"], input[type="text"], textarea');

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
    if (textInput.isContentEditable) {
        textInput.focus();
        
        switch (format) {
            case 'bold':
                document.execCommand('bold', false, null);
                break;
            case 'italic':
                document.execCommand('italic', false, null);
                break;
            case 'underline':
                document.execCommand('underline', false, null);
                break;
            case 'link':
                const selection = window.getSelection();
                const selectedText = selection.toString();
                const range = selection.getRangeAt(0);
                showLinkDialogForContentEditable(textInput, selectedText, range);
                return;
            case 'list':
                const sel = window.getSelection();
                const text = sel.toString();
                const rng = sel.getRangeAt(0);
                showBulletDialogForContentEditable(textInput, text, rng);
                return;
            default:
                return;
        }
    } else {
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
            case 'list':
                showBulletDialog(textInput, selectedText, beforeText, afterText, start);
                return;
            default:
                return;
        }

        textInput.value = beforeText + formattedText + afterText;

        const newCursorPos = start + formattedText.length;
        textInput.setSelectionRange(newCursorPos, newCursorPos);
        textInput.focus();
    }
}

let currentContentEditableElement = null;
let currentContentEditableRange = null;

function showLinkDialogForContentEditable(element, selectedText, range) {
    currentContentEditableElement = element;
    currentContentEditableRange = range;

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

function insertLinkInContentEditable() {
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
        alert('Please enter a valid URL (including http:// or https://)');
        document.getElementById('linkUrl').focus();
        return;
    }

    if (currentContentEditableElement && currentContentEditableRange) {
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(currentContentEditableRange);
        
        currentContentEditableRange.deleteContents();
        
        const link = document.createElement('a');
        link.href = linkUrl;
        link.textContent = linkDisplayName;
        
        currentContentEditableRange.insertNode(link);
        
        currentContentEditableElement.focus();
    }

    currentContentEditableElement = null;
    currentContentEditableRange = null;
    closeLinkModal();
}

window.insertLink = insertLinkInContentEditable;

function showBulletDialogForContentEditable(element, selectedText, range) {
    currentContentEditableElement = element;
    currentContentEditableRange = range;

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

function insertBulletListInContentEditable() {
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

    if (currentContentEditableElement && currentContentEditableRange) {
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(currentContentEditableRange);
        
        currentContentEditableRange.deleteContents();
        
        const ul = document.createElement('ul');
        bulletPoints.forEach(point => {
            const li = document.createElement('li');
            li.textContent = ' • ' + point;
            ul.appendChild(li);
        });
        
        currentContentEditableRange.insertNode(ul);
        
        currentContentEditableElement.focus();
    }

    currentContentEditableElement = null;
    currentContentEditableRange = null;
    closeBulletModal();
}

window.insertBulletList = insertBulletListInContentEditable;

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
                const textElement = section.querySelector(`[data-name="dynamic_text_${sectionId}"]`);
                if (textElement && textElement.hasAttribute('contenteditable')) {
                    sectionData.content = textElement.innerHTML;
                } else {
                    const input = section.querySelector(`[name="dynamic_text_${sectionId}"]`);
                    sectionData.content = input ? input.value : '';
                }
                break;
            case 'h1':
                const h1Element = section.querySelector(`[data-name="dynamic_h1_${sectionId}"]`);
                if (h1Element && h1Element.hasAttribute('contenteditable')) {
                    sectionData.content = h1Element.innerHTML;
                } else {
                    const input = section.querySelector(`[name="dynamic_h1_${sectionId}"]`);
                    sectionData.content = input ? input.value : '';
                }
                break;
            case 'h2':
                const h2Element = section.querySelector(`[data-name="dynamic_h2_${sectionId}"]`);
                if (h2Element && h2Element.hasAttribute('contenteditable')) {
                    sectionData.content = h2Element.innerHTML;
                } else {
                    const input = section.querySelector(`[name="dynamic_h2_${sectionId}"]`);
                    sectionData.content = input ? input.value : '';
                }
                break;
            case 'h3':
                const h3Element = section.querySelector(`[data-name="dynamic_h3_${sectionId}"]`);
                if (h3Element && h3Element.hasAttribute('contenteditable')) {
                    sectionData.content = h3Element.innerHTML;
                } else {
                    const input = section.querySelector(`[name="dynamic_h3_${sectionId}"]`);
                    sectionData.content = input ? input.value : '';
                }
                break;
            case 'h4':
                const h4Element = section.querySelector(`[data-name="dynamic_h4_${sectionId}"]`);
                if (h4Element && h4Element.hasAttribute('contenteditable')) {
                    sectionData.content = h4Element.innerHTML;
                } else {
                    const input = section.querySelector(`[name="dynamic_h4_${sectionId}"]`);
                    sectionData.content = input ? input.value : '';
                }
                break;
            case 'h5':
                const h5Element = section.querySelector(`[data-name="dynamic_h5_${sectionId}"]`);
                if (h5Element && h5Element.hasAttribute('contenteditable')) {
                    sectionData.content = h5Element.innerHTML;
                } else {
                    const input = section.querySelector(`[name="dynamic_h5_${sectionId}"]`);
                    sectionData.content = input ? input.value : '';
                }
                break;
            case 'h6':
                const h6Element = section.querySelector(`[data-name="dynamic_h6_${sectionId}"]`);
                if (h6Element && h6Element.hasAttribute('contenteditable')) {
                    sectionData.content = h6Element.innerHTML;
                } else {
                    const input = section.querySelector(`[name="dynamic_h6_${sectionId}"]`);
                    sectionData.content = input ? input.value : '';
                }
                break;
            case 'header':
                const headerElement = section.querySelector(`[data-name="dynamic_header_${sectionId}"]`);
                if (headerElement && headerElement.hasAttribute('contenteditable')) {
                    sectionData.content = headerElement.innerHTML;
                } else {
                    const input = section.querySelector(`[name="dynamic_header_${sectionId}"]`);
                    sectionData.content = input ? input.value : '';
                }
                break;
            case 'subheader':
                const subheaderElement = section.querySelector(`[data-name="dynamic_subheader_${sectionId}"]`);
                if (subheaderElement && subheaderElement.hasAttribute('contenteditable')) {
                    sectionData.content = subheaderElement.innerHTML;
                } else {
                    const input = section.querySelector(`[name="dynamic_subheader_${sectionId}"]`);
                    sectionData.content = input ? input.value : '';
                }
                break;
            case 'subheader-text':
                const subheaderTextElement = section.querySelector(`[data-name="dynamic_subheader_text_${sectionId}"]`);
                if (subheaderTextElement && subheaderTextElement.hasAttribute('contenteditable')) {
                    sectionData.content = subheaderTextElement.innerHTML;
                } else {
                    const input = section.querySelector(`[name="dynamic_subheader_text_${sectionId}"]`);
                    sectionData.content = input ? input.value : '';
                }
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
        console.log('📡 Fetching blogs from /api/blogs?include_deleted=false...');
        const response_blogs = await authenticatedFetch('/api/blogs?include_deleted=false');
        const result_blogs = await response_blogs.json();

        blogsLoading.classList.add('hidden');
        
        let blogs = [];
        if (result_blogs.status === 'success' && Array.isArray(result_blogs.blogs)) {
            blogs = result_blogs.blogs;
        }

        allFetchedBlogs = [...blogs];
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
    const filterContentTypeInput = document.getElementById('filterContentType');
    
    const filterTitleValue = filterTitleInput ? filterTitleInput.value.trim().toLowerCase() : '';
    const filterContentTypeValue = filterContentTypeInput ? filterContentTypeInput.value : 'ALL';

    console.log('🔍 Applying filters:');
    console.log(`  - Title filter: "${filterTitleValue}" (${filterTitleValue ? 'ACTIVE' : 'INACTIVE'})`);
    console.log(`  - Type filter: "${filterContentTypeValue}"`);
    console.log(`  - Total blogs before filtering: ${allFetchedBlogs.length}`);

    const filteredBlogs = allFetchedBlogs.filter(blog => {
        if (!blog) {
            console.warn('⚠️ Null blog encountered in filter');
            return false;
        }

        let blogData = {};
        try {
            if (typeof blog.blogcontent === 'string') {
                blogData = JSON.parse(blog.blogcontent);
            } else if (typeof blog.blogcontent === 'object' && blog.blogcontent !== null) {
                blogData = blog.blogcontent;
            }
        } catch (e) {
            console.error('Failed to parse blog.blogcontent in filter:', e);
            blogData = {};
        }

        const title = (blogData.blogTitle || blog.title || '').toLowerCase();
        const type = blog.type || 'BLOG';

        const titleMatch = !filterTitleValue || title.includes(filterTitleValue);
        const typeMatch = filterContentTypeValue === 'ALL' || type === filterContentTypeValue;

        const matches = titleMatch && typeMatch;

        if (filterTitleValue || filterContentTypeValue !== 'ALL') {
            console.log(`  Blog "${title}": titleMatch=${titleMatch}, typeMatch=${typeMatch}, result=${matches}`);
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
            if (typeof blog.blogContent === 'string') {
                blogData = JSON.parse(blog.blogContent);
            } else if (typeof blog.blogContent === 'object' && blog.blogContent !== null) {
                blogData = blog.blogContent;
            }
        } catch (e) {
            console.error(`Failed to parse blog.blogContent for blog ${index + 1}:`, e);
            blogData = {};
        }

        console.log(`📝 Blog ${index + 1}:`, {
            id: blog.id,
            status: blog.status,
            type: blog.type,
            category: blog.category,
            date: blog.date,
            blogDataType: typeof blog.blogContent,
            parsedBlogData: blogData
        });

        const title = blogData.blogTitle || blog.title || 'Untitled';
        const date = blogData.blogDate || blog.date || new Date().toISOString();
        const status = blog.status || 'draft';
        const mainImageUrl = blogData.mainImageUrl || '';
        const mainImageAlt = blogData.mainImageAlt || title;
        const type = blog.type || 'BLOG';
        const slug = blog.slug || '';

        console.log(`  Title: "${title}", Slug: "${slug}", Date: "${date}", Status: "${status}", Type: "${type}"`);

        return `
            <div class="p-4 bg-white/5 rounded-lg border border-white/10 hover:bg-white/10 transition-colors">
                <div class="flex justify-between items-start mb-3">
                    <div class="flex-1">
                        <h3 class="font-semibold mb-2 text-white line-clamp-2">${escapeHtml(title)}</h3>
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
        if (typeof blog.blogContent === 'string') {
            blogData = JSON.parse(blog.blogContent);
        } else if (typeof blog.blogContent === 'object' && blog.blogContent !== null) {
            blogData = blog.blogContent;
        }
    } catch (e) {
        console.error('Failed to parse blog.blogContent in populateEditForm:', e);
        blogData = {};
    }
    
    console.log('📝 Populating form with blog data:', blogData);

    const mainImageUrl = document.getElementById('mainImageUrl');
    const mainImageAlt = document.getElementById('mainImageAlt');
    const blogTitle = document.getElementById('blogTitle');
    const blogDate = document.getElementById('blogDate');
    const blogSummary = document.getElementById('blogSummary');
    
    if (mainImageUrl) mainImageUrl.value = blogData.mainImageUrl || '';
    if (mainImageAlt) mainImageAlt.value = blogData.mainImageAlt || '';
    if (blogTitle) blogTitle.value = blogData.blogTitle || '';
    if (blogDate) blogDate.value = blogData.blogDate || '';
    if (blogSummary) blogSummary.value = blogData.blogSummary || '';

    const statusRadios = document.querySelectorAll('input[name="blogStatus"]');
    statusRadios.forEach(radio => {
        radio.checked = radio.value === blog.status;
    });

    const blogCategory = document.getElementById('blogCategory');
    if (blogCategory) blogCategory.value = blogData.blogCategory || '';
    
    const editorsChoice = document.getElementById('editorsChoice');
    if (editorsChoice) editorsChoice.checked = blogData.editors_choice === 'Y';

    populateLabelsFromData(blog.keyword || {});

    const seoTitle = document.getElementById('seoTitle');
    const seoMetaDescription = document.getElementById('seoMetaDescription');
    const seoCanonicalUrl = document.getElementById('seoCanonicalUrl');
    
    if (seoTitle) seoTitle.value = blogData.seoTitle || '';
    if (seoMetaDescription) seoMetaDescription.value = blogData.seoMetaDescription || '';
    if (seoCanonicalUrl) seoCanonicalUrl.value = blogData.seoCanonicalUrl || '';

    const dynamicSections = document.getElementById('dynamicSections');
    if (dynamicSections) {
        dynamicSections.innerHTML = '';
    }
    sectionCounter = 0;

    if (blogData.contentType) {
        const contentType = blogData.contentType;
        const contentTypeInput = document.getElementById('contentType');
        if (contentTypeInput) contentTypeInput.value = contentType;
        
        const blogTypeBtn = document.getElementById('blogTypeBtn');
        const caseStudyTypeBtn = document.getElementById('caseStudyTypeBtn');
        
        if (blogTypeBtn && caseStudyTypeBtn) {
            if (contentType === 'BLOG') {
                blogTypeBtn.classList.add('active');
                blogTypeBtn.classList.remove('bg-white/10', 'text-white');
                blogTypeBtn.classList.add('bg-white', 'text-black');
                
                caseStudyTypeBtn.classList.remove('active');
                caseStudyTypeBtn.classList.add('bg-white/10', 'text-white');
                caseStudyTypeBtn.classList.remove('bg-white', 'text-black');
            } else if (contentType === 'CASE STUDY') {
                caseStudyTypeBtn.classList.add('active');
                caseStudyTypeBtn.classList.remove('bg-white/10', 'text-white');
                caseStudyTypeBtn.classList.add('bg-white', 'text-black');
                
                blogTypeBtn.classList.remove('active');
                blogTypeBtn.classList.add('bg-white/10', 'text-white');
                blogTypeBtn.classList.remove('bg-white', 'text-black');
            }
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
    const sectionTitle = document.querySelector('#addBlogs .section-title');
    if (sectionTitle) sectionTitle.textContent = 'Edit Blog';

    const blogStatusSection = document.getElementById('blogStatusSection');
    if (blogStatusSection) blogStatusSection.style.display = 'block';

    const addModeButtons = document.getElementById('addModeButtons');
    const editModeButtons = document.getElementById('editModeButtons');
    if (addModeButtons) addModeButtons.style.display = 'none';
    if (editModeButtons) editModeButtons.style.display = 'flex';
}

function switchToAddMode() {
    const sectionTitle = document.querySelector('#addBlogs .section-title');
    if (sectionTitle) sectionTitle.textContent = 'Add New Blog';

    const blogStatusSection = document.getElementById('blogStatusSection');
    if (blogStatusSection) blogStatusSection.style.display = 'none';

    const addModeButtons = document.getElementById('addModeButtons');
    const editModeButtons = document.getElementById('editModeButtons');
    if (addModeButtons) addModeButtons.style.display = 'flex';
    if (editModeButtons) editModeButtons.style.display = 'none';

    currentEditingBlog = null;

    const addBlogForm = document.getElementById('addBlogForm');
    if (addBlogForm) addBlogForm.reset();
    
    const dynamicSections = document.getElementById('dynamicSections');
    if (dynamicSections) dynamicSections.innerHTML = '';
    sectionCounter = 0;

    const blogCategory = document.getElementById('blogCategory');
    const seoTitle = document.getElementById('seoTitle');
    const seoMetaDescription = document.getElementById('seoMetaDescription');
    const seoCanonicalUrl = document.getElementById('seoCanonicalUrl');
    
    if (blogCategory) blogCategory.value = '';
    if (seoTitle) seoTitle.value = '';
    if (seoMetaDescription) seoMetaDescription.value = '';
    if (seoCanonicalUrl) seoCanonicalUrl.value = '';

    const labelsContainer = document.getElementById('labelsContainer');
    if (labelsContainer) {
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
    }
    
    const labelsNotMandatory = document.getElementById('labelsNotMandatory');
    if (labelsNotMandatory) labelsNotMandatory.checked = false;
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
        const blogDateInput = document.getElementById('blogDate');
        if (blogDateInput) blogDateInput.value = today;
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
            blogContent: data,
            status: data.status,
            keyword: data.labels,
            editors_choice: data.editors_choice || 'N'
        };

        const response = await authenticatedFetch(endpoint, {
            method: 'PUT',
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

window.editBlog = editBlog;
window.showBlogUrl = showBlogUrl;
window.deleteBlog = deleteBlog;
window.confirmDeleteBlog = confirmDeleteBlog;

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

    const cancelEditBtn = document.getElementById('cancelEditBtn');
    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', function () {
            switchToAddMode();
            showModal('Info', 'Edit cancelled. All changes have been discarded.', 'info');
            
            const navbarTabs = document.querySelectorAll('#navbarTabs .tab-button');
            const editDeleteTab = Array.from(navbarTabs).find(btn => {
                const text = btn.textContent.trim();
                return text.includes('Edit/Delete') || text.includes('Edit');
            });
            
            if (editDeleteTab) {
                editDeleteTab.click();
            }
        });
    }


    document.getElementById('addTextBtn').addEventListener('click', () => addDynamicSection('text'));
    document.getElementById('addH1Btn').addEventListener('click', () => addDynamicSection('h1'));
    document.getElementById('addH2Btn').addEventListener('click', () => addDynamicSection('h2'));
    document.getElementById('addH3Btn').addEventListener('click', () => addDynamicSection('h3'));
    document.getElementById('addH4Btn').addEventListener('click', () => addDynamicSection('h4'));
    document.getElementById('addH5Btn').addEventListener('click', () => addDynamicSection('h5'));
    document.getElementById('addImageBtn').addEventListener('click', () => addDynamicSection('image'));

    const filterTitleInput = document.getElementById('filterTitle');

    function setupFilterListeners() {
        const applyFilters = () => applyFiltersAndRender(1);

        const debounce = (func, delay) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(func, delay);
        };

        console.log('✓ Setting up filter listeners (Title text input)');
        if (filterTitleInput) {
            filterTitleInput.addEventListener('input', () => debounce(applyFilters, 300));
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


document.addEventListener('paste', function(e) {
    if (e.target.getAttribute('contenteditable') === 'true' || e.target.isContentEditable) {
        e.preventDefault();
        
        const htmlData = e.clipboardData.getData('text/html');
        const plainText = e.clipboardData.getData('text/plain');
        
        if (htmlData) {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = htmlData;
            
            const allElements = tempDiv.querySelectorAll('*');
            allElements.forEach(el => {
                el.style.color = '';
                el.style.backgroundColor = '';
                el.style.background = '';
                el.removeAttribute('color');
                el.removeAttribute('bgcolor');
                if (el.style.length === 0) {
                    el.removeAttribute('style');
                }
            });
            
            while (tempDiv.firstChild && (tempDiv.firstChild.nodeType === 3 && !tempDiv.firstChild.textContent.trim() ||
                   tempDiv.firstChild.nodeType === 1 && !tempDiv.firstChild.textContent.trim())) {
                tempDiv.removeChild(tempDiv.firstChild);
            }
            
            while (tempDiv.lastChild && (tempDiv.lastChild.nodeType === 3 && !tempDiv.lastChild.textContent.trim() ||
                   tempDiv.lastChild.nodeType === 1 && !tempDiv.lastChild.textContent.trim())) {
                tempDiv.removeChild(tempDiv.lastChild);
            }
            
            const selection = window.getSelection();
            if (!selection.rangeCount) return;
            
            const range = selection.getRangeAt(0);
            range.deleteContents();
            
            const frag = document.createDocumentFragment();
            const children = Array.from(tempDiv.childNodes);
            children.forEach(child => frag.appendChild(child.cloneNode(true)));
            
            range.insertNode(frag);
            range.collapse(false);
            selection.removeAllRanges();
            selection.addRange(range);
        } else if (plainText) {
            const trimmedText = plainText.trim();
            document.execCommand('insertText', false, trimmedText);
        }
    }
});
