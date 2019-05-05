let header = document.querySelector("header");

window.addEventListener("scroll", () => {
    if (window.scrollY > 150) {
        header.classList.add("collapsed")
    } else {
        header.classList.remove("collapsed")
    }
});