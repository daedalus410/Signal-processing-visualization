document.getElementById('signal-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const equation = document.getElementById('equation').value;
    const processing = document.getElementById('processing').value;

    fetch('/api/process_signal', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ equation, processing }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            visualizeData(data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function visualizeData(data) {
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.x_values,
            datasets: [
                {
                    label: 'Original Signal',
                    data: data.original_signal,
                    borderColor: 'blue',
                    fill: false,
                },
                {
                    label: 'Processed Signal',
                    data: data.processed_signal,
                    borderColor: 'red',
                    fill: false,
                }
            ],
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'x' } },
                y: { title: { display: true, text: 'Amplitude' } },
            },
        },
    });
}

