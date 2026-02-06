const monthYear = document.getElementById("monthYear");
const calendarDays = document.getElementById("calendarDays");
const prevMonth = document.getElementById("prevMonth");
const nextMonth = document.getElementById("nextMonth");

/* ===============================
   CONFIGURATION
================================ */
const minMonth = new Date(2025, 10, 1); // Nov 2025

let currentDate;
let currentStartDate;

// Use server date if available, otherwise client date
if (typeof SERVER_NOW !== "undefined" && SERVER_NOW) {
    const serverDate = new Date(SERVER_NOW);
    currentDate = new Date(serverDate.getFullYear(), serverDate.getMonth(), 1);
    currentStartDate = new Date(serverDate.getFullYear(), serverDate.getMonth(), serverDate.getDate());
} else {
    const now = new Date();
    currentDate = new Date(now.getFullYear(), now.getMonth(), 1);
    currentStartDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
}

// Dynamically calculate maxSelectableDay (1 year - 1 day from today)
let tempMax = new Date(currentStartDate);
tempMax.setFullYear(tempMax.getFullYear() + 1);
tempMax.setDate(tempMax.getDate() - 1); // one year minus one day

const maxSelectableDay = tempMax;
const maxMonth = new Date(maxSelectableDay.getFullYear(), maxSelectableDay.getMonth(), 1);

const companyStartDate = new Date(2025, 10, 20); // Nov 20, 2025

// Ensure currentDate is within allowed min/max
if (currentDate < minMonth) currentDate = new Date(minMonth);
if (currentDate > maxMonth) currentDate = new Date(maxMonth);

let selectedDate = null;

const timeSelect = document.getElementById("timeSelect");
let selectedTime = null;

timeSelect.addEventListener("change", () => {
    selectedTime = timeSelect.value;
});


// Add the showFlashMessage function at the top
function showFlashMessage(message, type = "success") {
    const flashMessage = document.createElement("div");
    flashMessage.classList.add("flash-message", type);
    flashMessage.textContent = message;

    // Append it to the body or a specific container
    document.body.appendChild(flashMessage);

    // Remove the message after 5 seconds
    setTimeout(() => flashMessage.remove(), 5000);
}



/* ===============================
   HELPERS
================================ */
function isFullyDisabledMonth(year, month) {
    // Disable Nov & Dec 2025 completely
    return year === 2025 && (month === 10 || month === 11);
}

function generateTimeSlots() {
    timeSelect.innerHTML = "";
    selectedTime = null;

    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "Select a time";
    placeholder.disabled = true;
    placeholder.selected = true;
    timeSelect.appendChild(placeholder);

    const now = new Date();
    const currentHour = now.getHours();
    const todaySelected = isToday(selectedDate);

    for (let hour = 9; hour <= 17; hour++) {
        const option = document.createElement("option");

        const displayHour = hour > 12 ? hour - 12 : hour;
        const ampm = hour >= 12 ? "PM" : "AM";

        option.value = `${hour}:00`;
        option.textContent = `${displayHour}:00 ${ampm}`;

        // Disable past times ONLY if today
        if (todaySelected && hour <= currentHour) {
            option.disabled = true;
        }

        timeSelect.appendChild(option);
    }

    timeSelect.disabled = false;
}


function isToday(date) {
    const now = new Date();
    return (
        date.getFullYear() === now.getFullYear() &&
        date.getMonth() === now.getMonth() &&
        date.getDate() === now.getDate()
    );
}



/* ===============================
   RENDER CALENDAR
================================ */
function renderCalendar(date) {
    calendarDays.innerHTML = "";

    const year = date.getFullYear();
    const month = date.getMonth();
    const fullyDisabled = isFullyDisabledMonth(year, month);

    // Month/Year display
    monthYear.textContent = date.toLocaleString("default", {
        month: "long",
        year: "numeric"
    });

    // Navigation arrows
    prevMonth.disabled = (year < minMonth.getFullYear() || (year === minMonth.getFullYear() && month <= minMonth.getMonth()));
    prevMonth.title = prevMonth.disabled ? "Bookings start in November 2025" : "";

    nextMonth.disabled = (year > maxMonth.getFullYear() || (year === maxMonth.getFullYear() && month >= maxMonth.getMonth()));
    nextMonth.title = nextMonth.disabled ? `Bookings available up to ${maxSelectableDay.toLocaleDateString()}` : "";

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    let firstSelectable = null;
    let lastDayElement = null;

    // Empty cells for alignment
    for (let i = 0; i < firstDay; i++) {
        calendarDays.appendChild(document.createElement("div"));
    }

    // Generate days
    for (let day = 1; day <= daysInMonth; day++) {
        const dayEl = document.createElement("div");
        dayEl.className = "calendar-day";
        dayEl.textContent = day;

        const thisDate = new Date(year, month, day);

        // Disabled logic
        if (
            fullyDisabled ||
            thisDate < currentStartDate ||
            thisDate > maxSelectableDay
        ) {
            dayEl.classList.add("disabled");
        }

        // Highlight company start date (permanent gray)
        if (
            thisDate.getFullYear() === companyStartDate.getFullYear() &&
            thisDate.getMonth() === companyStartDate.getMonth() &&
            thisDate.getDate() === companyStartDate.getDate()
        ) {
            dayEl.classList.add("company-start");
            dayEl.title = "Company officially started on this day";
        }

        // Clickable days
        dayEl.addEventListener("click", () => {
            if (dayEl.classList.contains("disabled")) return;
            document.querySelectorAll(".calendar-day").forEach(d => d.classList.remove("selected"));
            dayEl.classList.add("selected");
            selectedDate = thisDate;
            generateTimeSlots();
        });

        // Track first selectable day
        if (!dayEl.classList.contains("disabled") && !firstSelectable) {
            firstSelectable = dayEl;
        }

        lastDayElement = dayEl;
        calendarDays.appendChild(dayEl);
    }

    // Auto-select logic: only on initial load if no selection
    if (!selectedDate) {
        const todayEl = Array.from(calendarDays.children).find(d => {
            if (!d.classList.contains("calendar-day") || d.classList.contains("disabled")) return false;
            return parseInt(d.textContent) === currentStartDate.getDate() &&
                date.getMonth() === currentStartDate.getMonth() &&
                date.getFullYear() === currentStartDate.getFullYear();
        });

        if (todayEl) {
            todayEl.classList.add("selected");
            selectedDate = currentStartDate;
            generateTimeSlots();

        } else if (firstSelectable) {
            firstSelectable.classList.add("selected");
            selectedDate = new Date(year, month, parseInt(firstSelectable.textContent));
        }
    } else {
        // Highlight selectedDate if it is in the current month
        if (selectedDate.getFullYear() === year && selectedDate.getMonth() === month) {
            const selectedEl = Array.from(calendarDays.children).find(d =>
                parseInt(d.textContent) === selectedDate.getDate()
            );
            if (selectedEl) selectedEl.classList.add("selected");
        }
    }
}

/* ===============================
   NAVIGATION BUTTONS
================================ */
prevMonth.addEventListener("click", () => {
    if (prevMonth.disabled) return;
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar(currentDate);
});

nextMonth.addEventListener("click", () => {
    if (nextMonth.disabled) return;
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar(currentDate);
});

/* ===============================
   SUBMIT BUTTON
================================ */
function sendCalendarSelection(event) {
    event.preventDefault();  // Prevent the default form submission (page refresh)

    const fullyDisabled = isFullyDisabledMonth(currentDate.getFullYear(), currentDate.getMonth());

    if (fullyDisabled) {
        alert("This month is not available for booking.");
        return;
    }

    if (!selectedDate) {
        alert("Please select a date.");
        return;
    }

    if (!selectedTime) {
        alert("Please select a time.");
        return;
    }

    // Collect email, phone number, and selected messaging apps
    const email = document.getElementById("emailInput").value;
    const phone = document.getElementById("phoneInput").value;
    const whatsapp = document.getElementById("whatsapp").checked;
    const telegram = document.getElementById("telegram").checked;
    const signal = document.getElementById("signal").checked;

    // Check if email is provided (required field)
    if (!email || email.trim() === "") {
        showFlashMessage("Email is required.", "error");
        return;  // Stop submission if email is missing
    }

    fetch("/calendar-selection", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            selected_date: selectedDate.toISOString().split("T")[0],
            selected_time: selectedTime,
            selected_month: {
                year: currentDate.getFullYear(),
                month: currentDate.getMonth() + 1
            },
            emailInput: email,
            phoneInput: phone,
            whatsapp: whatsapp,
            telegram: telegram,
            signal: signal
        })
    })
        .then(res => res.json())
        .then(data => {
            // If the submission is successful, show flash message and prevent page reload
            showFlashMessage(data.message || "Appointment request received!", "success");

            // Optionally redirect after some time (if needed)
            setTimeout(() => {
                window.location.href = '/';  // You can replace '/' with your desired redirect URL
            }, 2000);  // Wait 2 seconds before redirect (adjust time as needed)
        })
        .catch(err => {
            console.error("Fetch error:", err);
            showFlashMessage("Something went wrong. Please try again later.", "error");
        });
}





/* ===============================
   INITIAL RENDER
================================ */
console.log("Calendar starting at:", currentDate.toISOString());

document.addEventListener("DOMContentLoaded", () => {
    renderCalendar(currentDate);

    const confirmBtn = document.getElementById("confirmCalendar");
    if (confirmBtn) {
        confirmBtn.addEventListener("click", (event) => sendCalendarSelection(event));  // Pass the event object
    } else {
        console.error("Confirm button not found!");
    }

    // Phone + messaging toggle logic
    const phoneInput = document.getElementById("phoneInput");
    const messagingChecks = ["whatsapp", "signal", "telegram"]
        .map(id => document.getElementById(id));

    function toggleMessagingOptions() {
        const enabled = phoneInput.value.trim() !== "";
        messagingChecks.forEach(cb => {
            cb.disabled = !enabled;
            if (!enabled) cb.checked = false;
        });
    }

    phoneInput.addEventListener("input", toggleMessagingOptions);
    toggleMessagingOptions(); // initial state
});


