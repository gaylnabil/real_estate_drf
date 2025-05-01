let chart;

function trainModel() {
    // Get the file input element
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file first');
        return;
    }
    
    // Create a FormData object
    const formData = new FormData();
    
    // Add the file to the FormData object
    formData.append('file', file);
    
    // Send the AJAX request
    $.ajax({
        url: 'http://127.0.0.1:8000/api/predictor/upload',
        type: 'POST',
        data: formData,
        processData: false,  // Important: prevent jQuery from processing the data
        contentType: false,  // Important: prevent jQuery from setting contentType
        success: function(response) {
            // Handle success - update UI, show message, etc.
            console.log('Upload successful', response);
        },
        error: function(xhr, status, error) {
            // Handle error - show error message, etc.
            console.error('Upload failed: ' + error);
        }
    });
}

function visualizeData() {
    const data = {
        labels: [50, 70, 100, 120],
        datasets: [{
            label: 'Prix (€)',
            data: [120000, 170000, 250000, 310000],
            borderColor: '#0ea5e9',
            backgroundColor: 'rgba(14,165,233,0.2)',
            tension: 0.3
        }]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            scales: {
                x: { title: { display: true, text: 'Superficie (m²)' } },
                y: { title: { display: true, text: 'Prix (€)' } }
            }
        }
    };

    if (chart) {
        chart.destroy();
    }
    chart = new Chart(document.getElementById('chart'), config);
}

function predictPrice() {
    const surface = document.getElementById("surface").value;
    if (surface) {
        const price = surface * 2500;
        document.getElementById("prediction").textContent = `Estimation : ${price.toLocaleString()} €`;
    } else {
        document.getElementById("prediction").textContent = "Veuillez saisir une superficie.";
    }
}
