document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(fileInput => {
        fileInput.addEventListener('change', function() {
            const displayElementId = fileInput.getAttribute('data-display');
            const displayElement = document.getElementById(displayElementId);
            const files = fileInput.files;
            let fileNames = '';

            for (let i = 0; i < files.length; i++) {
                fileNames += files[i].name + (i < files.length - 1 ? ', ' : '');
            }

            displayElement.textContent = fileNames;
        });
    });
});
