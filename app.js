let schedules = null;

function makeTable(title, rows, dest)
{
    const divtimetables = document.createElement("div");
    divtimetables.classList.add("timetables");

    const h2 = document.createElement("h2");
    if (title == "Metro")
    {
        h2.textContent = "Μετρό";
    }
    else
    {
        h2.textContent = "Προαστιακός";
    }
    divtimetables.appendChild(h2);

    const table = document.createElement("table");

    if (dest == "Doukissis")
    {
        if (title == "Metro")
        {
            table.innerHTML = `
                <tr>
                    <th>309B</th>
                    <th>309B (Ππδμτρ)</th>
                    <th>Αναμονή</th>
                    <th>Μετρό</th>
                </tr>
            `;
        }
        else
        {
            table.innerHTML = `
                <tr>
                    <th>309B</th>
                    <th>309B (Ππδμτρ)</th>
                    <th>Αναμονή</th>
                    <th>Προαστιακός</th>
                </tr>
            `;
        }

        rows.forEach(r => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${r[0]}</td>
                <td>${r[3]}</td>
                <td>${r[1]}'</td>
                <td>${r[2]}</td>
            `;
            table.appendChild(tr);
        });

    }
    else
    {
        if (title == "Metro")
        {
            table.innerHTML = `
                <tr>
                    <th>Μετρό</th>
                    <th>Αναμονή</th>
                    <th>309B</th>
                </tr>
            `;
        }
        else
        {
            table.innerHTML = `
                <tr>
                    <th>Προαστιακός</th>
                    <th>Αναμονή</th>
                    <th>309B</th>
                </tr>
            `;
        }

        rows.forEach(r => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${r[0]}</td>
                <td>${r[1]}'</td>
                <td>${r[2]}</td>
            `;
            table.appendChild(tr);
        });

    }

    divtimetables.appendChild(table);
    return divtimetables;
}


function renderTables(data, dest)
{
    const results = document.getElementById("results");
    results.innerHTML = "";

    const div = document.createElement("div");
    div.classList.add("whereto");

    const h2 = document.createElement("h2");
    if (dest == "Doukissis")
    {
        h2.textContent = "Κορωπί προς Δουκίσσης";
    }
    else
    {
        h2.textContent = "Δουκίσσης προς Κορωπί";
    }
    
    div.appendChild(h2);

    results.appendChild(div);
    results.appendChild(makeTable("SubRail", data.SubRail, dest));
    results.appendChild(makeTable("Metro", data.Metro, dest));
}


// Load the JSON once
fetch("schedules.json")
    .then(response => response.json())
    .then(data => { schedules = data; console.log("Schedules loaded"); })
    .catch(err => console.error("Failed to load schedules:", err));

document.getElementById("opts").addEventListener("submit", function (e) {
    e.preventDefault();

    if (!schedules) return;

    const dest = document.getElementById("dest").value;
    const day = document.getElementById("day").value;

    const data = schedules[dest][day];
    renderTables(data, dest);
});
