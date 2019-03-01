let star_div = document.getElementById('stars');

for (i = 13; i < 100 / window.devicePixelRatio; i++) {
    var star = document.createElement('div');
    star.id = 's' + i;
    star.classList.add('star');
    star.draggable = true;
    star_div.appendChild(star);
}

let stars = document.getElementsByClassName("star");
let star_text = document.getElementById("star-text");

document.getElementById('satellite').onclick = () => window.location.href='/secret/';

function setup() {
    Array.from(stars).forEach((dusk) => {
        dusk.style.top = Math.round(Math.random() * 90 + 5) + '%';
        dusk.style.left = Math.round(Math.random() * 90 + 5) + '%';
        var size = Math.round(Math.random() * 4 + 4);
        dusk.style.webkitFilter = 'blur(' + Math.random() / 4 + 'em)';
        dusk.style.height = (size / 18) + 'em';
        dusk.style.width = (size / 18) + 'em';
    });
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(e) {
    e.dataTransfer.setData("star", e.target.id);
}

function drop(e) {
    e.preventDefault();
    var data = e.dataTransfer.getData("star");
    var star = document.getElementById(data);
    star.style.left = (e.clientX / window.screen.availWidth * 100) + 'vw';
    star.style.top = (e.clientY / window.screen.availHeight * 100) + 'vh';
    e.target.appendChild(star);
}

star_div.addEventListener("dragover", (e) => {
    allowDrop(e);
});

star_div.addEventListener("drop", (e) => {
    drop(e);
});

Array.from(stars).forEach((star) => {
    star.addEventListener("mouseenter", () => {
        var pos = star.getBoundingClientRect();
        star_text.style.top = pos.top + "px";
        star_text.style.left = pos.left + "px";
        star_text.style.opacity = "1";
    });

    star.addEventListener("mouseleave", () => {
        star_text.style.opacity = "0";
    });

    star.addEventListener("dragstart", (e) => {
        drag(e);
    });
});