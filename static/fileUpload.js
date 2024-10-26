document.addEventListener('DOMContentLoaded', function() {
    const fileInputCodes = document.getElementById('code_files');
    const fileInputEvaluations = document.getElementById('evaluation_images');

    const updateFileNames = (inputElement, displayElementId) => {
        const displayElement = document.getElementById(displayElementId);
        const files = inputElement.files;
        let fileNames = '';

        for (let i = 0; i < files.length; i++) {
            fileNames += files[i].name + (i < files.length - 1 ? ', ' : '');
        }

        displayElement.textContent = fileNames;
    };

    fileInputCodes.addEventListener('change', function() {
        updateFileNames(fileInputCodes, 'file-upload-code-names');
    });

    fileInputEvaluations.addEventListener('change', function() {
        updateFileNames(fileInputEvaluations, 'file-upload-evaluation-names');
    });
});