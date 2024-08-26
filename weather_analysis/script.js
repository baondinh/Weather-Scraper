// Function to parse CSV data
function parseCSV(csv) {
    const lines = csv.split('\n');
    return lines.map(line => line.split(',').map(cell => cell.trim()));
}

// Function to create table rows from data
function createTableRows(data) {
    const tbody = document.getElementById('weather-data');
    tbody.innerHTML = ''; 
    data.forEach(row => {
        if (row.length === 7) { // Ensure the row has all 7 columns
            const tr = document.createElement('tr');
            row.forEach(cell => {
                const td = document.createElement('td');
                td.textContent = cell;
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        }
    });
}

// Function to handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const csvData = e.target.result;
            const data = parseCSV(csvData);

            if (data[0][0].toLowerCase() === 'date') {
                data.shift();
            }
            createTableRows(data);
        };
        reader.readAsText(file);
    }
}

// Add event listener to file input
document.getElementById('csv-file').addEventListener('change', handleFileSelect, false);

// Read and process CSV file on page load
window.addEventListener('DOMContentLoaded', function() {
    const csvFile = document.getElementById('csv-file').files[0];
    if (csvFile) {
        handleFileSelect({ target: { files: [csvFile] } });
    }
});
