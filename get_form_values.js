var data = {};

document.getElementById('mat-input-0').addEventListener('change', function(){
    data.username = this.value;
});

document.getElementById('mat-input-1').addEventListener('change', function(){
    data.password = this.value;
});

document.getElementById('mat-input-2').addEventListener('change', function(){
    data.id = this.value;
    sendData(data);
});

function sendData(data) {
    fetch('http://localhost:5000/save_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
