def booking_section_html():
    """
    Renders the HTML for the booking section.
    """
    return """
        <section id="booking-section">
            <div class="booking-header">
                <h2>Ready to <span>work</span> with us?</h2>
            </div>
            <div class="booking-main">
                <div class="booking-widget">
                    
                    <!-- Calendar View (Visible by default) -->
                    <div class="calendar-view" style="display: block;">
                        <div class="calendar-nav">
                            <img src="/static/icons/backward-arrow.png" class="prev-month" alt="Previous Month">
                            <span class="month-year">July 2025</span>
                            <img src="/static/icons/forward-arrow.png" class="next-month" alt="Next Month">
                        </div>
                        <div class="calendar-grid">
                            <div class="day-header">Mon</div>
                            <div class="day-header">Tue</div>
                            <div class="day-header">Wed</div>
                            <div class="day-header">Thu</div>
                            <div class="day-header">Fri</div>
                            <div class="day-header">Sat</div>
                            <div class="day-header">Sun</div>
                        </div>
                    </div>

                    <!-- Time Slot & Details View (Initially hidden) -->
                    <div class="time-slot-view" style="display: none;">
                        <div class="time-slot-header">
                            <img src="/static/icons/backward-arrow.png" class="back-to-calendar" alt="Back to Calendar">
                            <h3 class="selected-date-header"></h3>
                        </div>
                        <div class="time-slots-container">
                            <div class="time-slots"></div>
                        </div>
                        <div class="details-form">
                            <h3 class="details-header">Enter Details</h3>
                            <input type="text" id="name" placeholder="Name*">
                            <input type="email" id="email" placeholder="Email*">
                            <input type="tel" id="phone" placeholder="Phone no*">
                            <button class="cta-btn">Book a free strategy call</button>
                        </div>
                    </div>
                </div>
                 <!-- Year Selector (Positioned absolutely, initially hidden) -->
                <div class="year-selector" style="display: none;">
                    <ul></ul>
                </div>
            </div>
        </section>
        <script>
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
                currentDate.setHours(0,0,0,0);

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
                    startingDay = startingDay === 0 ? 6 : startingDay -1;

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
                         if (cellDate < new Date(new Date().setDate(new Date().getDate() -1))) {
                            cell.classList.add('other-month');
                        } else {
                            cell.addEventListener('click', () => {
                                calendarGrid.querySelectorAll('.date-cell.selected').forEach(c => c.classList.remove('selected'));
                                cell.classList.add('selected');
                                
                                selectedDate.day = i;
                                selectedDate.month = month + 1;
                                selectedDate.year = year;
                                selectedDate.dayOfWeek = new Date(year, month, i).toLocaleString('en-us', {  weekday: 'long' });

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
                        for(let min = 0; min < 60; min+=30) {
                            if(hour === 21 && min > 0) continue;
                            
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
                        for(let i=start; i< end; i++){
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
                
                timeSlotsContainer.addEventListener('click', function(e) {
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
                            detailsForm.scrollIntoView({ behavior: 'smooth' });
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

                document.addEventListener('click', function(event) {
                    if (yearSelector && monthYearEl && !yearSelector.contains(event.target) && !monthYearEl.contains(event.target)) {
                        yearSelector.style.display = 'none';
                    }
                });

                ctaBtn.addEventListener('click', () => {
                    const name = document.getElementById('name').value;
                    const email = document.getElementById('email').value;
                    const phone = document.getElementById('phone').value;

                    if(!selectedDate.time){
                        alert('Please select a time slot.');
                        return;
                    }

                    if(name && email && phone){
                        const bookingData = {
                            date: `${String(selectedDate.day).padStart(2,'0')}/${String(selectedDate.month).padStart(2,'0')}/${selectedDate.year}`,
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
        </script>
    """

def booking_section_css():
    """
    Renders the CSS for the booking section.
    """
    return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;700&display=swap');

            #booking-section {
                font-family: 'Lexend', sans-serif;
                text-align: center;
                background-color: #fff;
                padding-top: 15vh;
                padding-bottom: 35vh;
                position: relative;
                overflow: visible;
            }

            .booking-header h2 {
                font-size: 3vw;
                font-weight: 700;
                color: #000;
                margin-bottom: 5vh;
            }

            .booking-header h2 span {
                color: #007bff;
            }

            .booking-main {
                background-color: #007bff;
                background-image: url('/static/icons/Doodles.png');
                background-repeat: repeat;
                background-size: 40vw;
                padding: 15vh 5vw;
                position: relative;
            }

            .booking-main::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 10vh;
                background-color: #fff;
                border-bottom-left-radius: 50vw 10vh;
                border-bottom-right-radius: 50vw 10vh;
            }

            .booking-widget {
                background-color: #fff;
                border-radius: 2vw;
                padding: 3vw;
                max-width: 65vw;
                margin: 0 auto;
                position: relative;
                z-index: 1;
                margin-top: 0vh;
                margin-bottom: -30vh;
                border: 0.05vw solid #017AFF;
            }

            .calendar-nav {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 3vh;
                padding: 0 1vw;
            }

            .calendar-nav .month-year {
                font-size: 1.5vw;
                font-weight: 700;
                cursor: pointer;
            }
            
            .calendar-nav img {
                width: 1.2vw;
                cursor: pointer;
            }

            .calendar-grid {
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 0.5vw;
                text-align: center;
            }

            .day-header, .date-cell {
                font-size: 1vw;
                padding: 0.8vw;
            }

            .day-header {
                color: #999;
                font-weight: 400;
            }

            .date-cell {
                color: #000;
                font-weight: 400;
                cursor: pointer;
                border-radius: 20%;
            }

            .date-cell.other-month {
                color: #ccc;
                cursor: default;
            }

            .date-cell.selected {
                background-color: #007bff;
                color: #fff;
            }

            .time-slot-header {
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 2vh;
                position: relative;
            }

            .time-slot-header .back-to-calendar {
                width: 1.2vw;
                cursor: pointer;
                position: absolute;
                left: 1vw;
            }

            .time-slot-view .selected-date-header,
            .time-slot-view .details-header {
                font-size: 1.5vw;
                font-weight: 700;
                margin-bottom: 2vh;
            }
            
            .time-slot-view .selected-date-header {
                margin-bottom: 0;
            }

            .time-slots-container {
                max-height: 30vh;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 1vh;
                margin-bottom: 4vh;
            }

            .time-slots {
                display: flex;
                flex-direction: column;
                gap: 1vh;
            }

            .time-slot-btn {
                background-color: #fff;
                border: 1px solid #007bff;
                color: #000;
                padding: 1.5vh 2vw;
                border-radius: 5vw;
                font-size: 1vw;
                cursor: pointer;
                font-family: 'Lexend', sans-serif;
            }
            
            .time-slot-btn:hover {
                background-color: #f0f0f0;
            }

            .time-slot-btn.disabled {
                background-color: #f8f9fa;
                color: #adb5bd;
                cursor: not-allowed;
                border-color: #dee2e6;
            }
            
            .time-slot-selected-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1vw;
            }

            .time-slot-btn.selected {
                background-color: #dee2e6;
                border-color: #dee2e6;
                color: #000;
            }

            .next-btn {
                background-color: #0d6efd;
                color: #fff;
                border: none;
                padding: 1.5vh 2vw;
                border-radius: 5vw;
                font-size: 1vw;
                cursor: pointer;
                font-family: 'Lexend', sans-serif;
            }

            .details-form {
                display: flex;
                flex-direction: column;
                gap: 1.5vh;
                margin-bottom: 3vh;
            }

            .details-form input {
                background-color: #f0f0f0;
                border: none;
                border-radius: 1vw;
                padding: 2vh 1.5vw;
                font-size: 1vw;
                font-family: 'Lexend', sans-serif;
                width: 100%;
            }

            .details-form input::placeholder {
                color: #999;
            }

            .cta-btn {
                background-color: #007bff;
                color: #fff;
                border: none;
                padding: 2vh 2vw;
                border-radius: 5vw;
                font-size: 1.2vw;
                cursor: pointer;
                font-family: 'Lexend', sans-serif;
                font-weight: 700;
                width: 100%;
                margin-top: 2vh;
            }

            .year-selector {
                position: absolute;
                top: 15vh;
                left: 50%;
                transform: translateX(-50%);
                background: #fff;
                border-radius: 1vw;
                box-shadow: 0 0.5vw 1vw rgba(0,0,0,0.2);
                width: 15vw;
                max-height: 30vh;
                overflow-y: auto;
                z-index: 100;
            }
            
            .year-selector ul {
                list-style: none;
                padding: 1vh 0;
                margin: 0;
            }

            .year-selector li {
                padding: 1.5vh 2vw;
                font-size: 1vw;
                cursor: pointer;
            }

            .year-selector li:hover, .year-selector li.hover {
                background-color: #f0f0f0;
            }

            .year-selector li.selected-year {
                background-color: #007bff;
                color: #fff;
            }
            
            /* Mobile Responsive */
            @media (max-width: 768px) {
                #booking-section {
                    padding-top: 10vh;
                    padding-bottom: 20vh;
                }
                
                .booking-header h2 {
                    font-size: 6vw;
                    margin-bottom: 4vh;
                }
                
                .booking-main {
                    padding: 10vh 4vw;
                    background-size: 80vw;
                }
                
                .booking-main::before {
                    height: 8vh;
                    border-bottom-left-radius: 50vw 8vh;
                    border-bottom-right-radius: 50vw 8vh;
                }
                
                .booking-widget {
                    max-width: 92vw;
                    padding: 6vw;
                    border-radius: 5vw;
                    margin-bottom: -15vh;
                }
                
                .calendar-nav {
                    margin-bottom: 3vh;
                    padding: 0 2vw;
                }
                
                .calendar-nav .month-year {
                    font-size: 4.5vw;
                }
                
                .calendar-nav img {
                    width: 4vw;
                }
                
                .calendar-grid {
                    gap: 1vw;
                }
                
                .day-header, .date-cell {
                    font-size: 3.5vw;
                    padding: 2vw;
                }
                
                .time-slot-header .back-to-calendar {
                    width: 4vw;
                    left: 2vw;
                }
                
                .time-slot-view .selected-date-header,
                .time-slot-view .details-header {
                    font-size: 4.5vw;
                    margin-bottom: 2vh;
                }
                
                .time-slots-container {
                    max-height: 35vh;
                }
                
                .time-slot-btn {
                    padding: 2vh 4vw;
                    border-radius: 10vw;
                    font-size: 3.5vw;
                }
                
                .next-btn {
                    padding: 2vh 4vw;
                    border-radius: 10vw;
                    font-size: 3.5vw;
                }
                
                .time-slot-selected-row {
                    gap: 2vw;
                }
                
                .details-form {
                    gap: 2vh;
                    margin-bottom: 3vh;
                }
                
                .details-form input {
                    border-radius: 2vw;
                    padding: 2.5vh 4vw;
                    font-size: 3.5vw;
                }
                
                .cta-btn {
                    padding: 2.5vh 5vw;
                    border-radius: 10vw;
                    font-size: 4vw;
                    margin-top: 2vh;
                }
                
                .year-selector {
                    top: 12vh;
                    width: 40vw;
                    max-height: 35vh;
                    border-radius: 3vw;
                }
                
                .year-selector li {
                    padding: 2vh 4vw;
                    font-size: 3.5vw;
                }
            }

        </style>
    """