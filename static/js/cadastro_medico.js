let currentStep = 1;

function showStep(step) {
    const steps = document.querySelectorAll(".step-form");
    steps.forEach((el, index) => {
        if (index === step - 1) {
            el.classList.add("active");
            el.style.display = "block";
        } else {
            el.classList.remove("active");
            el.style.display = "none";
        }
    });
}

function nextStep() {
    if (currentStep < 3) {
        currentStep++;
        showStep(currentStep);
    }
}

function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
    }
}