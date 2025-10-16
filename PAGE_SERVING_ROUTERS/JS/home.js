document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger) {
        hamburger.addEventListener('click', function () {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        const links = navLinks.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', function () {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const bookingSection = document.getElementById('booking-section');
    if (!bookingSection) return;

    const calendarView = bookingSection.querySelector('.calendar-view');
    const timeSlotView = bookingSection.querySelector('.time-slot-view');
    const yearSelector = bookingSection.querySelector('.year-selector');
    const monthYearEl = bookingSection.querySelector('.month-year');
    const calendarGrid = bookingSection.querySelector('.calendar-grid');
    const selectedDateHeader = bookingSection.querySelector('.selected-date-header');
    const timeSlotsContainer = bookingSection.querySelector('.time-slots');
    const detailsForm = bookingSection.querySelector('.details-form');
    const ctaBtn = bookingSection.querySelector('.cta-btn');
    const backToCalendarBtn = bookingSection.querySelector('.back-to-calendar');

    let selectedDate = {};
    let currentDate = new Date();
    currentDate.setHours(0, 0, 0, 0);

    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

    function renderCalendar(year, month) {
        monthYearEl.textContent = `${monthNames[month]} ${year}`;
        calendarGrid.innerHTML = `
            <div class="day-header">Mon</div>
            <div class="day-header">Tue</div>
            <div class="day-header">Wed</div>
            <div class="day-header">Thu</div>
            <div class="day-header">Fri</div>
            <div class="day-header">Sat</div>
            <div class="day-header">Sun</div>
        `;

        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();

        let startingDay = firstDay.getDay();
        startingDay = startingDay === 0 ? 6 : startingDay - 1;

        const prevLastDay = new Date(year, month, 0);
        const prevMonthDays = prevLastDay.getDate();
        for (let i = startingDay; i > 0; i--) {
            const day = prevMonthDays - i + 1;
            const cell = document.createElement('div');
            cell.classList.add('date-cell', 'other-month');
            cell.textContent = day;
            calendarGrid.appendChild(cell);
        }

        for (let i = 1; i <= daysInMonth; i++) {
            const cell = document.createElement('div');
            cell.classList.add('date-cell');
            cell.textContent = i;
            const cellDate = new Date(year, month, i);
            if (cellDate < new Date(new Date().setDate(new Date().getDate() - 1))) {
                cell.classList.add('other-month');
            } else {
                cell.addEventListener('click', () => {
                    calendarGrid.querySelectorAll('.date-cell.selected').forEach(c => c.classList.remove('selected'));
                    cell.classList.add('selected');

                    selectedDate.day = i;
                    selectedDate.month = month + 1;
                    selectedDate.year = year;
                    selectedDate.dayOfWeek = new Date(year, month, i).toLocaleString('en-us', {
                        weekday: 'long'
                    });

                    selectedDateHeader.textContent = `${selectedDate.dayOfWeek}, ${i} ${monthNames[month]}`;
                    renderTimeSlots();
                    calendarView.style.display = 'none';
                    timeSlotView.style.display = 'block';
                });
            }
            calendarGrid.appendChild(cell);
        }
        const totalCells = startingDay + daysInMonth;
        const nextMonthStart = 42 - totalCells;
        for (let i = 1; i <= nextMonthStart; i++) {
            const cell = document.createElement('div');
            cell.classList.add('date-cell', 'other-month');
            cell.textContent = i;
            calendarGrid.appendChild(cell);
        }
    }

    function renderTimeSlots() {
        timeSlotsContainer.innerHTML = '';
        let timeSlots = [];
        const now = new Date();
        for (let hour = 9; hour <= 21; hour++) {
            for (let min = 0; min < 60; min += 30) {
                if (hour === 21 && min > 0) continue;

                let displayHour = hour % 12 || 12;
                let period = hour >= 12 ? 'pm' : 'am';
                let displayMin = min === 0 ? '00' : min;
                const timeString = `${displayHour}:${displayMin} ${period}`;

                const timeSlotDate = new Date(selectedDate.year, selectedDate.month - 1, selectedDate.day, hour, min);

                timeSlots.push({
                    time: timeString,
                    disabled: timeSlotDate < now
                });
            }
        }

        const renderButtons = (start, end) => {
            for (let i = start; i < end; i++) {
                const slot = timeSlots[i];
                const btn = document.createElement('button');
                btn.classList.add('time-slot-btn');
                btn.textContent = slot.time;
                if (slot.disabled) {
                    btn.classList.add('disabled');
                    btn.disabled = true;
                }
                timeSlotsContainer.appendChild(btn);
            }
        }

        renderButtons(0, Math.min(5, timeSlots.length));

        timeSlotsContainer.parentElement.onscroll = (e) => {
            if (e.target.scrollTop + e.target.clientHeight >= e.target.scrollHeight - 5) {
                const currentCount = timeSlotsContainer.children.length;
                if (currentCount < timeSlots.length) {
                    const nextStart = currentCount;
                    const nextEnd = Math.min(nextStart + 5, timeSlots.length);
                    renderButtons(nextStart, nextEnd);
                }
            }
        }
    }

    timeSlotsContainer.addEventListener('click', function (e) {
        if (e.target.classList.contains('time-slot-btn') && !e.target.disabled && !e.target.parentElement.classList.contains('time-slot-selected-row')) {
            const clickedBtn = e.target;
            const time = clickedBtn.textContent;

            const hiddenBtn = timeSlotsContainer.querySelector('.time-slot-btn[data-hidden="true"]');
            if (hiddenBtn) {
                hiddenBtn.style.display = '';
                delete hiddenBtn.dataset.hidden;
                const rowToRemove = hiddenBtn.nextElementSibling;
                if (rowToRemove && rowToRemove.classList.contains('time-slot-selected-row')) {
                    rowToRemove.remove();
                }
            }

            clickedBtn.style.display = 'none';
            clickedBtn.dataset.hidden = 'true';

            const row = document.createElement('div');
            row.classList.add('time-slot-selected-row');

            const selectedBtn = document.createElement('button');
            selectedBtn.classList.add('time-slot-btn', 'selected');
            selectedBtn.textContent = time;

            const nextBtn = document.createElement('button');
            nextBtn.classList.add('next-btn');
            nextBtn.textContent = 'Next';
            nextBtn.addEventListener('click', () => {
                detailsForm.scrollIntoView({
                    behavior: 'smooth'
                });
            });

            row.appendChild(selectedBtn);
            row.appendChild(nextBtn);

            clickedBtn.after(row);

            let time24 = time;
            let [timePart, period] = time24.split(' ');
            let [h, m] = timePart.split(':');
            h = parseInt(h);
            if (period.toLowerCase() === 'pm' && h !== 12) h += 12;
            if (period.toLowerCase() === 'am' && h === 12) h = 0;
            selectedDate.time = `${String(h).padStart(2, '0')}${m}`;
        }
    });

    function renderYearSelector() {
        const ul = yearSelector.querySelector('ul');
        ul.innerHTML = '';
        const currentYear = new Date().getFullYear();
        for (let i = currentYear - 4; i <= currentYear + 8; i++) {
            const li = document.createElement('li');
            li.textContent = i;
            if (i === currentDate.getFullYear()) {
                li.classList.add('selected-year');
            }
            li.addEventListener('click', () => {
                currentDate.setFullYear(i);
                renderCalendar(currentDate.getFullYear(), currentDate.getMonth());
                yearSelector.style.display = 'none';
            });
            ul.appendChild(li);
        }
    }

    bookingSection.querySelector('.prev-month').addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate.getFullYear(), currentDate.getMonth());
    });

    bookingSection.querySelector('.next-month').addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate.getFullYear(), currentDate.getMonth());
    });

    monthYearEl.addEventListener('click', () => {
        yearSelector.style.display = yearSelector.style.display === 'none' ? 'block' : 'none';
    });

    backToCalendarBtn.addEventListener('click', () => {
        timeSlotView.style.display = 'none';
        calendarView.style.display = 'block';
    });

    document.addEventListener('click', function (event) {
        if (yearSelector && monthYearEl && !yearSelector.contains(event.target) && !monthYearEl.contains(event.target)) {
            yearSelector.style.display = 'none';
        }
    });

    ctaBtn.addEventListener('click', () => {
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;

        if (!selectedDate.time) {
            alert('Please select a time slot.');
            return;
        }

        if (name && email && phone) {
            const bookingData = {
                date: `${String(selectedDate.day).padStart(2, '0')}/${String(selectedDate.month).padStart(2, '0')}/${selectedDate.year}`,
                time: selectedDate.time,
                name: name,
                email: email,
                phone: phone
            };
            console.log(JSON.stringify(bookingData, null, 2));
            calendarView.style.display = 'block';
            timeSlotView.style.display = 'none';
            document.getElementById('name').value = '';
            document.getElementById('email').value = '';
            document.getElementById('phone').value = '';
            selectedDate = {};
            currentDate = new Date();
            renderCalendar(currentDate.getFullYear(), currentDate.getMonth());

        } else {
            alert('Please fill in all details.');
        }
    });

    renderCalendar(currentDate.getFullYear(), currentDate.getMonth());
    renderYearSelector();
});

document.querySelectorAll('.faq-item').forEach(item => {
    item.addEventListener('click', () => {
        const currentlyActive = document.querySelector('.faq-item.active');
        if (currentlyActive && currentlyActive !== item) {
            currentlyActive.classList.remove('active');
            currentlyActive.querySelector('.icon').textContent = '+';
        }

        item.classList.toggle('active');
        const icon = item.querySelector('.icon');
        if (item.classList.contains('active')) {
            icon.textContent = '-';
        } else {
            icon.textContent = '+';
        }
    });
});