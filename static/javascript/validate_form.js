class form {

    // Setting check variables
    form_element;
    email_ok = true;
    email_match_ok = true;
    username_ok = true;
    password_match_ok = true;

    constructor(element) {
        this.form_element = element;
    }

    setup() {
//  Input fields
        this.email = this.form_element.querySelector("input.email");
        this.repeat_email = this.form_element.querySelector("input.repeat-email");
        this.username = this.form_element.querySelector("input.username");
        this.new_password = this.form_element.querySelector("input.new-password");
        this.repeat_new_password = this.form_element.querySelector("input.repeat-new-password");
        this.submit = this.form_element.querySelector("button.submit-button");


// Feedback elements
        this.email_msg = this.form_element.querySelector("p.email-check");
        this.repeat_email_msg = this.form_element.querySelector("p.email-match-check");
        this.username_msg = this.form_element.querySelector("p.username-check");
        this.repeat_new_password_msg = this.form_element.querySelector("p.repeat-new-password-check");


// Setting listeners

        try {
            ["keyup", "paste", "load"].forEach((event) => {
                this.email.addEventListener(event, () => {
                    this.check_email(this.email, this.email_msg);
                });
            });
        } catch (e) {
            console.log("No 'email' field, continuing...");
        }

        try {
            ["keyup", "paste", "load"].forEach((event) => {
                this.repeat_email.addEventListener(event, () => {
                    this.check_email_match(this.email, this.repeat_email, this.repeat_email_msg);
                });
                this.email.addEventListener(event, () => {
                    this.check_email_match(this.email, this.repeat_email, this.repeat_email_msg);
                });
            });
        } catch (e) {
            console.log("No 'repeat-email' field, continuing...");
        }

        try {
            ["keyup", "paste", "load"].forEach((event) => {
                this.username.addEventListener(event, () => {
                    this.check_username(this.username, this.username_msg);
                });
            });
        } catch (e) {
            console.log("No 'username' field, continuing...");
        }

        try {
            ["keyup", "paste", "load"].forEach((event) => {
                this.new_password.addEventListener(event, () => {
                    this.check_password_match(this.new_password,
                        this.repeat_new_password, this.repeat_new_password_msg);
                });
                this.repeat_new_password.addEventListener("keyup", () => {
                    this.check_password_match(this.new_password,
                        this.repeat_new_password, this.repeat_new_password_msg);
                });
            });
        } catch (e) {
            console.log("No password fields, continuing...");
        }
    }

    disable_submit() {
// Disable sending directly by using submit button
        this.submit.addEventListener("click", (e) => {
            e.preventDefault();
            this.submit.classList.add("disabled");
            this.submit.innerText = "Sending, please wait...";
            if (this.validate_all()) {
                this.submit_form();
            } else {
                this.submit.innerText = "Submit";
            }
        });


// Disable submitting directly using Enter key
        form.onkeypress = (e) => {
            let key = e.key;
            if (key === "Enter") {
                e.preventDefault();
                submit.classList.add("disabled");
                submit.innerText = "Sending, please wait...";
                if (this.validate_all()) {
                    this.submit_form();
                } else {
                    submit.innerText = "Submit";
                }
            }
        };
    }


//Check functions
    check_username(element, element_to_set, async = true) {
        element.value = element.value.trim().replace(/\s+/g, '');
        if (!element.value.trim()) {
            element_to_set.innerHTML = "";
            this.username_ok = !element.hasAttribute('required');
            this.validate_form();
        } else {
            let xhr = new XMLHttpRequest();
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    let response = xhr.responseText.split(";", 2);
                    element_to_set.className = "credentials-check " + response[0];
                    element_to_set.innerHTML = response[1];
                    this.username_ok = response[0] === "ok";
                    this.validate_form();
                }
            };

            xhr.open("POST", "/check_username/", async);
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhr.send("username=" + element.value);
        }
    }

    check_email(element, element_to_set, async = true) {
        element.value = element.value.trim().replace(/\s+/g, '');
        if (!element.value) {
            element_to_set.innerHTML = "";
            this.email_ok = !element.hasAttribute('required');
            this.validate_form();
        } else {
            let xhr = new XMLHttpRequest();
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    let response = xhr.responseText.split(";", 2);
                    element_to_set.className = "credentials-check " + response[0];
                    element_to_set.innerHTML = response[1];
                    this.email_ok = response[0] === "ok";
                    this.validate_form();
                }
            };
            xhr.open("POST", "/check_email/", async);
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhr.send("email=" + element.value);
        }
    }

    check_email_match(element1, element2, element_to_set) {
        if (!element1.value && element1.hasAttribute('required') &&
            !element2.value && element2.hasAttribute('required')) {
            this.email_match_ok = false;
        } else if (element1.value !== element2.value) {
            element_to_set.innerHTML = "Emails do not match";
            element_to_set.className = "credentials-check error";
            this.email_match_ok = false;
        } else {
            element_to_set.innerHTML = "";
            this.email_match_ok = true;
        }
        this.validate_form();
    }

    check_password_match(element1, element2, element_to_set) {
        if (!element1.value && element1.hasAttribute('required') &&
            !element2.value && element2.hasAttribute('required')) {
            element_to_set.innerHTML = "";
            this.password_match_ok = false;
        } else if (!element1.value.trim() && !element2.value.trim()) {
            element_to_set.innerHTML = "";
        } else if (element1.value !== element2.value) {
            element_to_set.innerHTML = "Passwords do not match";
            element_to_set.className = "credentials-check error";
            this.password_match_ok = false;
        } else if (element1.value === element2.value) {
            element_to_set.innerHTML = "Passwords match";
            element_to_set.className = "credentials-check ok";
            this.password_match_ok = true;
        }
        this.validate_form();
    }


// Enabling or disabling form submission
    validate_form() {
        if (!this.email_ok || !this.email_match_ok || !this.username_ok || !this.password_match_ok) {
            this.submit.classList.add("disabled");
            return false;
        } else {
            this.submit.classList.remove("disabled");
            return true;
        }
    }

    validate_all() {
        this.check_username(this.username, this.username_msg, false);
        this.check_email(this.email, this.email_msg, false);
        this.check_password_match(this.new_password, this.repeat_new_password, this.repeat_new_password_msg);
        try {
            this.check_email_match(this.email, this.repeat_email, this.repeat_email_msg);
        } catch (e) {
            console.log("Failed to validate field. " + e);
        }
        return !(!this.email_ok || !this.email_match_ok || !this.username_ok || !this.password_match_ok);
    }

    submit_form() {
        if (this.validate_all()) {
            this.form_element.submit()
        }
    }

}


let forms = document.getElementsByClassName("validated");
Array.from(forms).forEach((f) => {
    f = new form(f);
    f.setup();
    f.disable_submit();

});