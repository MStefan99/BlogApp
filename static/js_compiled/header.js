"use strict";

var header = document.querySelector("header");
window.addEventListener("scroll", function () {
    if (window.scrollY > 150) {
        header.classList.add("collapsed");
    } else {
        header.classList.remove("collapsed");
    }
});
//# sourceMappingURL=header.js.map