function check_username(element) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("username-check").innerHTML =
            this.responseText;
       }
    };
    xhttp.open("GET", "/check_username/?username=" + element.value, true);
    xhttp.send();
}

function check_email(element) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("email-check").innerHTML =
            this.responseText;
       }
    };
    xhttp.open("GET", "/check_email/?email=" + element.value, true);
    xhttp.send();
}