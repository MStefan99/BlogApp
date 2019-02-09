function check_username(element, element_to_set) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            document.getElementById(element_to_set).innerHTML =
            this.responseText;
       }
    };
    xhttp.open("GET", "/check_username/?username=" + element.value, true);
    xhttp.send();
}

function check_email(element , element_to_set) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            document.getElementById(element_to_set).innerHTML =
            this.responseText;
       }
    };
    xhttp.open("GET", "/check_email/?email=" + element.value, true);
    xhttp.send();
}

function check_email_match(element1, element2, element_to_set) {
    if (element1.value !== element2.value) {
        document.getElementById(element_to_set).innerHTML = "<p class='error'>Emails do not match</p>"
    } else {
        document.getElementById(element_to_set).innerHTML = "";
    }

}