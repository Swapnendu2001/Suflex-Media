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

    const slidingText = document.querySelector('.sliding-text');
    if (slidingText) {
        const texts = [
            'strive to give 110%',
            'always work hard',
            'inspire avant-garde results',
            'produce creative solutions'
        ];
        let currentIndex = 0;

        function cycleText() {
            currentIndex = (currentIndex + 1) % texts.length;
            slidingText.style.animation = 'none';
            setTimeout(() => {
                slidingText.textContent = texts[currentIndex];
                slidingText.style.animation = 'slideUp 0.5s ease-in-out';
            }, 50);
        }

        setInterval(cycleText, 3000);
    }
});