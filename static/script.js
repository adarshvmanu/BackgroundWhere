
document.addEventListener('DOMContentLoaded', () => {
    const uploadInput = document.getElementById('upload-image');
    const processButton = document.getElementById('process-btn');
    const originalImageElement = document.getElementById('original-image');
    const processedImageElement = document.getElementById('processed-image');
    const downloadLink = document.getElementById('download-link');

    processButton.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('image', uploadInput.files[0]);
        fetch('/process_image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            //originalImageElement.src = URL.createObjectURL(uploadInput.files[0]);
            processedImageElement.src = `/processed/${data.processed_image}`;
            downloadLink.href = `/processed/${data.processed_image}`;
            downloadLink.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
