// Constants
const API_URL = "/generate"; // This will be a route in the Flask server

// DOM Elements
const optionSelect = document.getElementById("optionSelect");
const argomentoContainer = document.getElementById("argomentoContainer");
const filePathContainer = document.getElementById("filePathContainer");
const buttonsContainer = document.getElementById("buttonsContainer");
const formContainer = document.getElementById("formContainer");
const resultContainer = document.getElementById("resultContainer");
const resultContent = document.getElementById("resultContent");
const backButton = document.getElementById("backButton");
const argomentoInput = document.getElementById("argomento")

// Event Listeners
window.onload = resetForm;
optionSelect.addEventListener('change', updateForm);

// Form Update Functions
function updateForm() {
    const selectedValue = optionSelect.value;
    
    // Hide all containers initially
    [argomentoContainer, filePathContainer, buttonsContainer].forEach(container => {
        container.classList.add("hidden");
    });

    // Show relevant containers based on selection
    if (selectedValue === "creareFavola" || selectedValue === "rispondereDomanda") {
        argomentoContainer.classList.remove("hidden");
        buttonsContainer.classList.remove("hidden");
        if (selectedValue === "creareFavola") {
            argomentoInput.placeholder = "es. 'La principessa di ghiaccio', 'Il procione ciccione'";
        } else {
            argomentoInput.placeholder = "es. 'Cosa succede quando si entra in un buco nero?'";
        }
    } else if (selectedValue === "rispondereDomandaImg") {
        argomentoContainer.classList.remove("hidden");
        filePathContainer.classList.remove("hidden");
        buttonsContainer.classList.remove("hidden");
        argomentoInput.placeholder = "Inserisci la domanda sull'immagine";
    }
}

function resetForm() {
    optionSelect.selectedIndex = 0;
    document.getElementById("dynamicForm").reset();
    backButton.classList.add("hidden");
    updateForm();
}

function showForm() {
    formContainer.classList.remove("hidden");
    resultContainer.classList.add("hidden");
    backButton.classList.add("hidden")
    document.querySelector('.container').classList.remove('expanded');
    argomentoInput.value = "";
}

// Form Submission
async function submitForm(event) {
    event.preventDefault();
    const selectedValue = optionSelect.value;
    const argomento = document.getElementById("argomento").value;

    const formData = new FormData();
    formData.append('task', selectedValue);
    formData.append('prompt', argomento);

    let imageUrl = null;
    if (selectedValue === "rispondereDomandaImg") {
        const fileInput = document.getElementById("filePath");
        const file = fileInput.files[0];
        if (file) {
            formData.append('image', file);
            imageUrl = URL.createObjectURL(file);
        }
    }

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.text();
            displayResult(result, imageUrl);
        } else {
            throw new Error(`Risposta server ${response.status}: ${response.statusText}`);
        }
    } catch (error) {
        console.error("Dettagli errore:", error);
        alert("E' stato rilevato un errore, guardare la console per più informazioni.");
    }
}

// Result Display
function displayResult(result, imageUrl) {
    resultContent.innerHTML = result;
    const uploadedImage = document.getElementById("uploadedImage");
    
    if (imageUrl) {
        uploadedImage.src = imageUrl;
        uploadedImage.classList.remove("hidden");
    } else {
        uploadedImage.classList.add("hidden");
    }
    
    document.querySelector('.container').classList.add('expanded');
    resultContainer.classList.remove("hidden");
    formContainer.classList.add("hidden");
    backButton.classList.remove("hidden");
}

// Scroll Functions
function scrollToTop() {
    resultContainer.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

function scrollToBottom() {
    resultContainer.scrollTo({
        top: resultContainer.scrollHeight,
        behavior: 'smooth'
    });
}