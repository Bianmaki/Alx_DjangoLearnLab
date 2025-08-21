// blog/static/blog/script.js

// Runs when the page is loaded
document.addEventListener("DOMContentLoaded", function () {
    console.log("Blog authentication page loaded successfully ✅");
    
    // Optional: attach to form submit button
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function () {
            console.log("Form submitted 🚀");
        });
    }
});
