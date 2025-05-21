document.getElementById('downloadForm').addEventListener('submit', function(event) {
    const urlInput = document.getElementById('url').value;
    if (!urlInput) {
        event.preventDefault();  // Prevent form submission
        showError("Please enter a valid YouTube URL.");
    } else {
        document.getElementById('errorMessage').innerText = '';  // Clear previous errors
    }
});

function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.innerText = message;
}
