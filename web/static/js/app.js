// Enable Bootstrap tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

// Voting animation
document.addEventListener('DOMContentLoaded', function () {
    const voteButtons = document.querySelectorAll('.vote-btn');

    voteButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            // Add visual feedback
            this.style.transform = 'scale(1.4)';
            setTimeout(() => {
                this.style.transform = '';
            }, 300);
        });
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }

            form.classList.add('was-validated');
        });
    });
});

// Simple fade-in animation for elements
function fadeInElements() {
    const elements = document.querySelectorAll('.post-item, .circle-item, .activity-item');

    elements.forEach((element, index) => {
        element.style.opacity = 0;
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';

        setTimeout(() => {
            element.style.opacity = 1;
            element.style.transform = 'translateY(0)';
        }, 100 + (index * 100));
    });
}

// Run when document is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fadeInElements);
} else {
    fadeInElements();
}