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

// // Function to handle file selection
// function handleFileSelect(event) {
//     const file = event.target.files[0];
//     if (file) {
//         const reader = new FileReader();
//         reader.onload = function(e) {
//             const csvData = e.target.result;
//             const data = parseCSV(csvData);

//             if (data[0][0].toLowerCase() === 'date') {
//                 data.shift();
//             }
//             createTableRows(data);
//         };
//         reader.readAsText(file);
//     }
// }

// // Add this function to update the plot image
// function updatePlotImage(csvFilename) {
//     // Extract zip code and date from CSV filename
//     const match = csvFilename.match(/weather_forecast_(\d{5})_(\d{8})\.csv/);
//     if (match) {
//         const [_, zipCode, date] = match;
//         const plotFilename = `temperature_plot_${zipCode}_${date}.png`;
//         document.getElementById('temperature-plot').src = plotFilename;
//     }
// }

// // Modify handleFileSelect to call updatePlotImage
// function handleFileSelect(event) {
//     const file = event.target.files[0];
//     if (file) {
//         const reader = new FileReader();
//         reader.onload = function(e) {
//             const csvData = e.target.result;
//             const data = parseCSV(csvData);

//             if (data[0][0].toLowerCase() === 'date') {
//                 data.shift();
//             }
//             createTableRows(data);
//             updatePlotImage(file.name);  // Add this line
//         };
//         reader.readAsText(file);
//     }
// }

// // Add event listener to file input
// document.getElementById('csv-file').addEventListener('change', handleFileSelect, false);

// // Read and process CSV file on page load
// window.addEventListener('DOMContentLoaded', function() {
//     const csvFile = document.getElementById('csv-file').files[0];
//     if (csvFile) {
//         handleFileSelect({ target: { files: [csvFile] } });
//     }
// });

// Function to update plot image
function updatePlotImage(csvFilename) {
    const plotImg = document.getElementById('temperature-plot');
    const noDataMessage = document.getElementById('no-data-message');
    
    // Extract zip code and date from CSV filename
    const match = csvFilename.match(/weather_forecast_(\d{5})_(\d{8})\.csv/);
    if (match) {
        const [_, zipCode, date] = match;
        const plotFilename = `temperature_plot_${zipCode}_${date}.png`;
        
        // Create new Image object to verify the plot exists
        const img = new Image();
        img.onload = function() {
            // Image exists and loaded successfully
            plotImg.src = plotFilename;
            plotImg.style.display = 'block';
            noDataMessage.style.display = 'none';
        };
        img.onerror = function() {
            // Image failed to load
            plotImg.style.display = 'none';
            noDataMessage.style.display = 'block';
            noDataMessage.textContent = 'Error loading temperature plot';
        };
        img.src = plotFilename;
    } else {
        // Invalid filename format
        plotImg.style.display = 'none';
        noDataMessage.style.display = 'block';
        noDataMessage.textContent = 'Invalid file format';
    }
}

// Function to handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        if (!file.name.endsWith('.csv')) {
            alert('Please upload a CSV file');
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            const csvData = e.target.result;
            const data = parseCSV(csvData);

            if (data.length > 0) {
                if (data[0][0].toLowerCase() === 'date') {
                    data.shift();
                }
                createTableRows(data);
                updatePlotImage(file.name);
            } else {
                document.getElementById('temperature-plot').style.display = 'none';
                document.getElementById('no-data-message').textContent = 'No data found in CSV file';
                document.getElementById('no-data-message').style.display = 'block';
            }
        };
        reader.readAsText(file);
    } else {
        // Reset the display when no file is selected
        document.getElementById('temperature-plot').style.display = 'none';
        document.getElementById('no-data-message').style.display = 'block';
        document.getElementById('no-data-message').textContent = 'Upload a CSV file to view temperature plot';
    }
}

// Add event listener to file input
document.getElementById('csv-file').addEventListener('change', handleFileSelect, false);

// Initialize the display state
window.addEventListener('DOMContentLoaded', function() {
    const plotImg = document.getElementById('temperature-plot');
    const noDataMessage = document.getElementById('no-data-message');
    
    plotImg.style.display = 'none';
    noDataMessage.style.display = 'block';
});
