
//  Input fields
let email = document.getElementById("email");
let repeat_email = document.getElementById("repeat-email"); 
let username = document.getElementById("username");
let new_password = document.getElementById("new-password");
let repeat_new_password = document.getElementById("repeat-new-password");

// Feedback elements
let email_msg = document.getElementById("email-check");
let repeat_email_msg = document.getElementById("email-match-check");
let username_msg = document.getElementById("username-check");
let repeat_new_password_msg = document.getElementById("repeat-new-password-check");

// Setting listeners
try {
    ["change", "keyup", "paste"].forEach(function(event) {
        email.addEventListener(event, function () {
            check_email(email, email_msg);
        });
    });
} catch (e) {
    console.log("No 'email' field, continuing...");
}

try {
    ["change", "keyup", "paste"].forEach(function(event) {
        repeat_email.addEventListener(event, function () {
            check_email_match(repeat_email, repeat_email, repeat_email_msg);
        });
    });
} catch (e) {
    console.log("No 'repeat-email' field, continuing...");
}

try {
    ["change", "keyup", "paste"].forEach(function(event) {
        username.addEventListener(event, function () {
            check_username(username, username_msg);
        });
    });
} catch (e) {
    console.log("No 'username' field, continuing...");
}

try {
    ["change", "keyup", "paste"].forEach(function(event) {
        new_password.addEventListener(event, function () {
            check_password_match(new_password, repeat_new_password, repeat_new_password_msg);
        });
        repeat_new_password.addEventListener("keyup", function () {
            check_password_match(new_password, repeat_new_password, repeat_new_password_msg);
        });
    });
} catch (e) {
    console.log("No password fields, continuing...");
}


function check_username(element, element_to_set) {
    if (element.value.trim() === "") {
        element_to_set.innerHTML = "";
    } else {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                let response = this.responseText.split(";", 2);
                element_to_set.className = "credentials-check " + response[0];
                element_to_set.innerHTML = response[1];
            }
        };
        xhttp.open("GET", "/check_username/?username=" + element.value, true);
        xhttp.send();
    }
}

function check_email(element , element_to_set) {
    if (element.value.trim() === "") {
        element_to_set.innerHTML = "";
    } else {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.responseText.trim() === "") {
                element_to_set.innerHTML = "";
            } else if (this.readyState === 4 && this.status === 200) {
                let response = this.responseText.split(";", 2);
                element_to_set.className = "credentials-check " + response[0];
                element_to_set.innerHTML = response[1];
            }
        };
        xhttp.open("GET", "/check_email/?email=" + element.value, true);
        xhttp.send();
    }
}

function check_email_match(element1, element2, element_to_set) {
    if (element1.value !== element2.value) {
        element_to_set.innerHTML = "Emails do not match";
        element_to_set.className = "credentials-check error";
    } else {
        element_to_set.innerHTML = "";
    }
}

function check_password_match(element1, element2, element_to_set) {
    if (element1.value !== element2.value) {
        element_to_set.innerHTML = "Passwords do not match";
        element_to_set.className = "credentials-check error";
    } else {
        element_to_set.innerHTML = "Passwords match";
        element_to_set.className = "credentials-check ok";
    }
}