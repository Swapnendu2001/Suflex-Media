def blogs_filter_section_html():
    return '''
<section class="blogs-filter-section">
    <div class="filter-heading">
        <h1>The Latest Gossip</h1>
    </div>
    <div class="filter-buttons-container">
        <button class="filter-btn active" data-filter="all">All</button>
        <button class="filter-btn" data-filter="linkedin-prospecting">LinkedIn Prospecting</button>
        <button class="filter-btn" data-filter="linkedin-scraping">LinkedIn Scraping</button>
        <button class="filter-btn" data-filter="linkedin-plans">LinkedIn Plans</button>
        <button class="filter-btn" data-filter="sales-tools">Sales Tools</button>
        <button class="filter-btn" data-filter="cold-email">Cold Email</button>
        <button class="filter-btn" data-filter="linkedin-sales-navigator">LinkedIn Sales Navigator</button>
        <button class="filter-btn" data-filter="linkedin-networking">LinkedIn Networking</button>
        <button class="filter-btn" data-filter="linkedin-marketing">LinkedIn Marketing</button>
        <button class="filter-btn" data-filter="linkedin-automation">LinkedIn Automation</button>
        <button class="filter-btn" data-filter="email-deliverability">Email Deliverability</button>
        <button class="filter-btn" data-filter="b2b-lead-generation">B2B Lead Generation Tools</button>
    </div>
</section>
'''

def blogs_filter_section_css():
    return '''
<style>
    .blogs-filter-section {
        background-color: #fff;
        padding: 8vh 5vw;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'Lexend', sans-serif;
        width: 100%;
        max-width: 100vw;
        box-sizing: border-box;
        overflow-x: hidden;
    }
    .filter-heading {
        text-align: center;
        margin-bottom: 5vh;
    }
    .filter-heading h1 {
        font-size: 3.5vw;
        font-weight: 400;
        color: #000;
        margin: 0;
    }
    .filter-buttons-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1.5vw;
        max-width: 80vw;
        margin: 0 auto;
    }
    .filter-btn {
        background-color: #fff;
        color: #000;
        border: 0.15vw solid #e0e0e0;
        border-radius: 5vw;
        padding: 1.2vh 2vw;
        font-size: 1.1vw;
        font-weight: 400;
        font-family: 'Lexend', sans-serif;
        cursor: pointer;
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    .filter-btn:hover {
        background-color: #007bff;
        color: #fff;
        border-color: #007bff;
        transform: translateY(-0.3vh);
    }
    .filter-btn.active {
        background-color: #007bff;
        color: #fff;
        border-color: #007bff;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .blogs-filter-section {
            padding: 6vh 5vw;
        }
        .filter-heading {
            margin-bottom: 4vh;
        }
        .filter-heading h1 {
            font-size: 7vw;
        }
        .filter-buttons-container {
            gap: 2.5vw;
            max-width: 90vw;
        }
        .filter-btn {
            padding: 1.5vh 4vw;
            font-size: 3.5vw;
            border-radius: 10vw;
            border-width: 0.3vw;
        }
    }
</style>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const filterButtons = document.querySelectorAll('.filter-btn');
        
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                filterButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked button
                this.classList.add('active');
                
                // Get the filter value
                const filterValue = this.getAttribute('data-filter');
                
                // You can emit a custom event or call a function here to filter the blog posts
                console.log('Filter selected:', filterValue);
                
                // Dispatch custom event for filtering
                const filterEvent = new CustomEvent('blogFilterChanged', {
                    detail: { filter: filterValue }
                });
                document.dispatchEvent(filterEvent);
            });
        });
    });
</script>
'''
