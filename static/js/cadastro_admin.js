let currentStep = 1;

function showStep(step) {
    const steps = document.querySelectorAll(".step-form");
    steps.forEach((el, index) => {
        el.classList.remove("active");
        if (index === step - 1) {
            el.classList.add("active");
        }
    });
}

function nextStep() {
    if (currentStep < 2) {
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