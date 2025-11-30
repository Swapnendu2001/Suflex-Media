document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.getElementById('pdf-downloads-table-body');
    const prevPageBtn = document.getElementById('prev-page-btn');
    const nextPageBtn = document.getElementById('next-page-btn');
    const pageInfo = document.getElementById('page-info');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const monthlyDownloadsEl = document.getElementById('kpi-monthly-downloads');
    const mostDownloadedEl = document.getElementById('kpi-most-downloaded');
    const totalDownloadsEl = document.getElementById('kpi-total-downloads');

    let currentPage = 1;
    const rowsPerPage = 10;

    async function fetchPdfDownloads(page = 1) {
        loadingOverlay.style.display = 'flex';
        try {
            const response = await fetch(`/api/pdf-downloads?page=${page}&per_page=${rowsPerPage}`);
            if (!response.ok) {
                throw new Error('Failed to fetch PDF downloads');
            }
            const data = await response.json();
            renderTable(data.pdf_downloads);
            updatePagination(data.page, data.total_pages);
        } catch (error) {
            console.error('Error fetching PDF downloads:', error);
            showToast('Failed to load data. Please try again.', 'error');
        } finally {
            loadingOverlay.style.display = 'none';
        }
    }

    async function fetchKpiData() {
        monthlyDownloadsEl.textContent = '...';
        mostDownloadedEl.textContent = '...';
        totalDownloadsEl.textContent = '...';
        try {
            const response = await fetch('/api/pdf-downloads-kpi');
            if (!response.ok) {
                throw new Error('Failed to fetch KPI data');
            }
            const data = await response.json();
            monthlyDownloadsEl.textContent = data.total_downloads_this_month;
            const fullPdfName = data.most_downloaded_pdf.split('/').pop();
            const truncatedPdfName = fullPdfName.length > 20 ? fullPdfName.substring(0, 20) + '...' : fullPdfName;
            mostDownloadedEl.innerHTML = `
                <a href="${data.most_downloaded_pdf}" target="_blank" title="${fullPdfName}">${truncatedPdfName}</a>
                <div class="tooltip">${fullPdfName}</div>
            `;
            totalDownloadsEl.textContent = data.total_downloads;
        } catch (error) {
            console.error('Error fetching KPI data:', error);
            monthlyDownloadsEl.textContent = '-';
            mostDownloadedEl.textContent = '-';
            totalDownloadsEl.textContent = '-';
        }
    }

    function renderTable(downloads) {
        tableBody.innerHTML = '';
        if (downloads.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = `<td colspan="8" class="text-center">No data available</td>`;
            tableBody.appendChild(row);
            return;
        }

        downloads.forEach((download, index) => {
            const row = document.createElement('tr');
            const rowNumber = (currentPage - 1) * rowsPerPage + index + 1;
            const truncatedEmail = download.email.length > 20 ? download.email.substring(0, 20) + '...' : download.email;
            const truncatedPdfLink = download.pdf_link.length > 30 ? download.pdf_link.substring(0, 30) + '...' : download.pdf_link;
            const truncatedCompanyName = download.company_name.length > 20 ? download.company_name.substring(0, 20) + '...' : download.company_name;

            row.innerHTML = `
                <td>${rowNumber}</td>
                <td>${new Date(download.timestamp).toLocaleString()}</td>
                <td>${download.first_name}</td>
                <td>${download.last_name}</td>
                <td>
                    <a href="mailto:${download.email}" title="${download.email}">${truncatedEmail}</a>
                    <div class="tooltip">${download.email}</div>
                </td>
                <td>
                    <span title="${download.company_name}">${truncatedCompanyName}</span>
                    <div class="tooltip">${download.company_name}</div>
                </td>
                <td>${download.mobile_number}</td>
                <td>
                    <a href="${download.pdf_link}" target="_blank" title="${download.pdf_link}">${truncatedPdfLink}</a>
                    <div class="tooltip">${download.pdf_link}</div>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }

    function updatePagination(page, totalPages) {
        currentPage = page;
        pageInfo.textContent = `Page ${page} of ${totalPages}`;

        prevPageBtn.disabled = page <= 1;
        nextPageBtn.disabled = page >= totalPages;
    }

    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            fetchPdfDownloads(currentPage - 1);
        }
    });

    nextPageBtn.addEventListener('click', () => {
        fetchPdfDownloads(currentPage + 1);
    });

    function showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast show ${type}`;
        setTimeout(() => {
            toast.className = toast.className.replace('show', '');
        }, 3000);
    }

    fetchPdfDownloads();
    fetchKpiData();
});