/* ----------------------- CONFIG ----------------------- */
let habits = [];

const monthNames = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

/* ----------------------- HELPERS ---------------------- */
const daysInMonth = (m, y) => new Date(y, m + 1, 0).getDate();

const pad = (n) => (n < 10 ? "0" + n : n);

// Build a unique localStorage key for a particular habit/day
const makeKey = (y, m, d, hIdx) => `${y}-${pad(m)}-${pad(d)}-${hIdx}`;

/* ----------------------- STATE ------------------------ */
let currentDate = new Date(); // Today (month-level navigation will mutate this)

/* ---------------------- RENDERING --------------------- */
function fetchAndRenderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth() + 1;
    fetch(`/api/monthly_habits?year=${year}&month=${month}`)
        .then(response => response.json())
        .then(data => {
            habits = data;
            renderCalendar();
        });
}

function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const totalDays = daysInMonth(month, year);

    // Table element
    let tbl = document.getElementById("calendar");
    tbl.innerHTML = ""; // Reset

    /* ----------------- Build table header ---------------- */
    const dowLabels = ["M", "T", "W", "T", "F", "S", "S"];

    let headerRow1 = "<tr><th></th>";
    let headerRow2 = "<tr><th></th>";

    for (let day = 1; day <= totalDays; day++) {
        headerRow1 += `<th>${day}</th>`;

        // JavaScript Date: 0 = Sunday, so adjust to make Monday first (0..6 -> 0..6)
        const dow = (new Date(year, month, day).getDay() + 6) % 7;
        headerRow2 += `<th>${dowLabels[dow]}</th>`;
    }

    headerRow1 += "</tr>";
    headerRow2 += "</tr>";
    tbl.insertAdjacentHTML("beforeend", `<thead>${headerRow1}${headerRow2}</thead>`);

    /* ----------------- Build table body ------------------ */
    let tbodyHtml = "<tbody>";

    habits.forEach((habit, hIdx) => {
        tbodyHtml += `<tr><th class="text-start">${habit.name}</th>`;
        for (let day = 1; day <= totalDays; day++) {
            const dayData = habit.days[day - 1];
            const style = dayData.completed ? `style="background:${habit.color};"` : "";
            tbodyHtml += `<td data-habit="${hIdx}" data-day="${day}" ${style}></td>`;
        }
        tbodyHtml += "</tr>";
    });

    tbodyHtml += "</tbody>";
    tbl.insertAdjacentHTML("beforeend", tbodyHtml);

    /* ---------------- Cell click handlers --------------- */
    tbl.querySelectorAll("td").forEach((cell) => {
        cell.addEventListener("click", () => {
            const key = cell.dataset.key;
            const hIdx = parseInt(cell.dataset.habit, 10);
            const habitColor = habits[hIdx].color;

            const wasDone = cell.style.backgroundColor !== "";
            if (wasDone) {
                // Toggle off
                cell.style.backgroundColor = "";
                localStorage.removeItem(key);
            } else {
                // Mark as done
                cell.style.backgroundColor = habitColor;
                localStorage.setItem(key, "1");
            }
        });
    });
}

function initMonthYearSelectors() {
    const monthSelect = document.getElementById("monthSelect");
    const yearSelect = document.getElementById("yearSelect");
    monthSelect.innerHTML = "";
    yearSelect.innerHTML = "";

    monthNames.forEach((name, idx) => {
        const option = document.createElement("option");
        option.value = idx;
        option.text = name;
        monthSelect.appendChild(option);
    });

    const currentYear = new Date().getFullYear();
    for (let y = currentYear - 2; y <= currentYear + 2; y++) {
        const option = document.createElement("option");
        option.value = y;
        option.text = y;
        yearSelect.appendChild(option);
    }

    monthSelect.value = currentDate.getMonth();
    yearSelect.value = currentDate.getFullYear();

    monthSelect.addEventListener("change", () => {
        currentDate.setMonth(parseInt(monthSelect.value));
        fetchAndRenderCalendar();
    });
    yearSelect.addEventListener("change", () => {
        currentDate.setFullYear(parseInt(yearSelect.value));
        fetchAndRenderCalendar();
    });
}

document.addEventListener("DOMContentLoaded", function() {
    initMonthYearSelectors();
    fetchAndRenderCalendar();
});