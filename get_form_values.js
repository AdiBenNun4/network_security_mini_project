// Initialize an empty object to store user data
var data = {};


// Add an event listeners to the 'change' events of the input fields
// When the value of the input field changes, the username, password and ID are stored in the data object
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


// This function sends the data object to a server with a POST request
// The data object is sent in the body of the request as a JSON string
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
