
//  Input fields
let email = document.getElementById("email");
let repeat_email = document.getElementById("repeat-email"); 
let username = document.getElementById("username");
let new_password = document.getElementById("new-password");
let repeat_new_password = document.getElementById("repeat-new-password");
let form = document.getElementById("form");
let submit = document.getElementById("submit-button");

// Feedback elements
let email_msg = document.getElementById("email-check");
let repeat_email_msg = document.getElementById("email-match-check");
let username_msg = document.getElementById("username-check");
let repeat_new_password_msg = document.getElementById("repeat-new-password-check");

// Setting check variables
var email_ok = true;
var email_match_ok = true;
var username_ok = true;
var password_match_ok = true;

// Setting listeners
try {
    ["keyup", "paste"].forEach(function(event) {
        email.addEventListener(event, function () {
            check_email(email, email_msg);
        });
    });
} catch (e) {
    console.log("No 'email' field, continuing...");
}

try {
    ["keyup", "paste"].forEach(function(event) {
        repeat_email.addEventListener(event, function () {
            check_email_match(email, repeat_email, repeat_email_msg);
        });
        email.addEventListener(event, function () {
            check_email_match(email, repeat_email, repeat_email_msg);
        });
    });
} catch (e) {
    console.log("No 'repeat-email' field, continuing...");
}

try {
    ["keyup", "paste"].forEach(function(event) {
        username.addEventListener(event, function () {
            check_username(username, username_msg);
        });
    });
} catch (e) {
    console.log("No 'username' field, continuing...");
}

try {
    ["keyup", "paste"].forEach(function(event) {
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

form.onkeypress = function(e) {
    let key = e.key;
    if (key === "Enter") {
        e.preventDefault();
        validate_form();
    }
};


//Check functions
function check_username(element, element_to_set) {
    element.value = element.value.trim().replace(/\s+/g, '');
    if (element.value.trim() === "") {
        element_to_set.innerHTML = "";
        if (element.classList.contains("optional")) {
            username_ok = true;
            validate_form();
        } else {
            username_ok = false;
            validate_form();
        }
    }  else {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                let response = this.responseText.split(";", 2);
                element_to_set.className = "credentials-check " + response[0];
                element_to_set.innerHTML = response[1];
                username_ok = response[0] === "ok";
                validate_form();
            }
        };
        xhttp.open("GET", "/check_username/?username=" + element.value, true);
        xhttp.send();
        return username_msg.classList.contains("ok");
    }
}

function check_email(element, element_to_set) {
    element.value = element.value.trim().replace(/\s+/g, '');
    if (element.value === "") {
        element_to_set.innerHTML = "";
        if (element.classList.contains("optional")) {
            email_ok = true;
            validate_form();
        } else {
            email_ok = false;
            validate_form();
        }
    } else {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                let response = this.responseText.split(";", 2);
                element_to_set.className = "credentials-check " + response[0];
                element_to_set.innerHTML = response[1];
                email_ok = response[0] === "ok";
                validate_form();
            }
        };
        xhttp.open("GET", "/check_email/?email=" + element.value, true);
        xhttp.send();
        return email_msg.classList.contains("ok");
    }
}

function check_email_match(element1, element2, element_to_set) {
    if (element1.value === "" && element1.classList.contains("optional") &&
            element2.value === "" && element2.classList.contains("optional")) {
        email_match_ok = true;
    } else if (element1.value !== element2.value) {
        element_to_set.innerHTML = "Emails do not match";
        element_to_set.className = "credentials-check error";
        email_match_ok = false;
    } else {
        element_to_set.innerHTML = "";
        email_match_ok = true;
    }
    validate_form();
}

function check_password_match(element1, element2, element_to_set) {
    if (element1.value === "" && element1.classList.contains("optional") &&
            element2.value === "" && element2.classList.contains("optional")) {
        password_match_ok = true;
    } else if (element1.value !== element2.value) {
        element_to_set.innerHTML = "Passwords do not match";
        element_to_set.className = "credentials-check error";
        password_match_ok = false;
    } else if (element1.value.trim() === "" || element2.value.trim() === "") {
        element_to_set.innerHTML = "";
        password_match_ok = false;
    } else if (element1.value === element2.value && element1.value.trim() !== "" && element2.value.trim() !== "") {
        element_to_set.innerHTML = "Passwords match";
        element_to_set.className = "credentials-check ok";
        password_match_ok = true;
    }
    validate_form();
}

// Enabling or disabling form submission
function validate_form() {
    console.log("email_ok: " + email_ok + "\n " + "email_match_ok: " + email_match_ok + "\n " + "username_ok: " +
        username_ok + "\n " + "password_match_ok: " + password_match_ok + "\n ");

    if (!email_ok || !email_match_ok || !username_ok || !password_match_ok) {
        submit.classList.add("disabled");
        return false;
    } else {
        submit.classList.remove("disabled");
        return true;
    }
}