// Constants
const API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyCCm6Aoj2M18Gho95y7LEYIcCG9NjAIYdE";

// DOM Elements
const optionSelect = document.getElementById("optionSelect");
const argomentoContainer = document.getElementById("argomentoContainer");
const filePathContainer = document.getElementById("filePathContainer");
const buttonsContainer = document.getElementById("buttonsContainer");
const formContainer = document.getElementById("formContainer");
const resultContainer = document.getElementById("resultContainer");
const resultContent = document.getElementById("resultContent");
const backButton = document.getElementById("backButton");

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
    } else if (selectedValue === "rispondereDomandaImg") {
        argomentoContainer.classList.remove("hidden");
        filePathContainer.classList.remove("hidden");
        buttonsContainer.classList.remove("hidden");
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
    document.querySelector('.container').classList.remove('expanded');
    backButton.classList.add("hidden");
}

// Form Submission
async function submitForm(event) {
    event.preventDefault();
    const selectedValue = optionSelect.value;
    const argomento = document.getElementById("argomento").value;
    let data;

    try {
        data = await prepareRequestData(selectedValue, argomento);
        const response = await sendApiRequest(data);
        const generatedText = response.candidates[0].content.parts[0].text;
        displayResult(generatedText);
    } catch (error) {
        console.error("Error details:", error);
        alert("An error occurred while processing your request. Please check the console for more details.");
    }
}

// API Request Helpers
async function prepareRequestData(selectedValue, argomento) {
    let data = {
        contents: [{
            parts: []
        }]
    };

    if (selectedValue === "creareFavola") {
        data.contents[0].parts.push({ text: `Crea una favola: ${argomento}` });
    } else if (selectedValue === "rispondereDomanda") {
        data.contents[0].parts.push({ text: `${argomento}?` });
    } else if (selectedValue === "rispondereDomandaImg") {
        const fileInput = document.getElementById("filePath");
        const file = fileInput.files[0];
        if (!file) {
            throw new Error("Please select an image file.");
        }

        const base64Image = await getBase64(file);
        data.contents[0].parts.push(
            { text: argomento },
            { inline_data: { mime_type: file.type, data: base64Image } }
        );
    }

    return data;
}

async function sendApiRequest(data) {
    console.log("Sending request:", JSON.stringify(data));
    const response = await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    console.log("Response status:", response.status);
    if (response.ok) {
        const result = await response.json();
        console.log("API response:", result);
        return result;
    } else {
        const errorText = await response.text();
        console.error("API error response:", errorText);
        throw new Error(`API request failed: ${response.status} ${errorText}`);
    }
}

// Result Display
function displayResult(result) {
    resultContent.textContent = result;
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

// Utility Functions
function getBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.onerror = error => reject(error);
    });
}