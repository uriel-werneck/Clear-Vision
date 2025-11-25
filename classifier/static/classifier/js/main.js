document.addEventListener("DOMContentLoaded", () => {
    const navLinks = document.querySelectorAll("nav a");

    navLinks.forEach(link => {
        link.addEventListener("mouseover", () => {
            console.log(`Hovering: ${link.textContent}`);
        });
    });
});

const imageInput = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const clearBtn = document.getElementById('clearBtn');
const placeholder = document.getElementById('placeholder-text');

// Show preview when image is selected
imageInput.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = 'block';
        placeholder.style.display = 'none';
    }
});

// Clear image
clearBtn.addEventListener('click', function () {
    imageInput.value = "";
    preview.src = "";
    preview.style.display = "none";
    placeholder.style.display = "block";
});

document.addEventListener("DOMContentLoaded", () => {
    const resultItems = document.querySelectorAll(".result-item");

    resultItems.forEach(item => {
        item.addEventListener("mouseover", () => {
            console.log("Hovering result:", item.href);
        });
    });
});
