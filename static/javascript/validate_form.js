class form {
    // Setting check variables
    form_element;
    email_ok = true;
    email_match_ok = true;
    login_ok = true;
    username_ok = true;
    password_match_ok = true;
    required_ok = true;


    constructor(element) {
        this.form_element = element;
    }


    enable_smart_submit() {
        if (this.submit) {
// Disable sending directly by using submit button
            this.submit.addEventListener("click", (e) => {
                e.preventDefault();
                this.submit.classList.add("disabled");
                this.submit.innerText = "Sending, please wait...";
                if (this.validate_all()) {
                    this.form_element.submit()
                } else {
                    this.submit.innerText = "Submit";
                }
            });


// Disable submitting directly using Enter key
            form.onkeypress = (e) => {
                let key = e.key;
                if (key === "Enter") {
                    e.preventDefault();
                    this.submit.classList.add("disabled");
                    this.submit.innerText = "Sending, please wait...";
                    if (this.validate_all()) {
                        this.form_element.submit()
                    } else {
                        this.submit.innerText = "Submit";
                    }
                }
            };
        }
    }


    setup() {
//  Input fields
        this.email = this.form_element.querySelector("input.email");
        this.repeat_email = this.form_element.querySelector("input.repeat-email");
        this.username = this.form_element.querySelector("input.username");
        this.login = this.form_element.querySelector("input.login");
        this.new_password = this.form_element.querySelector("input.new-password");
        this.repeat_new_password = this.form_element.querySelector("input.repeat-new-password");
        this.required = this.form_element.querySelectorAll("input[required]");
        this.submit = this.form_element.querySelector("button");


// Feedback elements
        this.login_msg = this.form_element.querySelector("p.login-check");
        this.email_msg = this.form_element.querySelector("p.email-check");
        this.repeat_email_msg = this.form_element.querySelector("p.email-match-check");
        this.username_msg = this.form_element.querySelector("p.username-check");
        this.repeat_new_password_msg = this.form_element.querySelector("p.repeat-new-password-check");
        this.required_msg = this.form_element.querySelector("p.required-check");


// Setting listeners

        if (this.email) {
            if (this.email.classList.contains("realtime-validate")) {
                ["keyup", "paste", "load"].forEach((event) => {
                    this.email.addEventListener(event, () => {
                        this.check_email(this.email, this.email_msg);
                    });
                    if (this.repeat_email) {
                        this.email.addEventListener(event, () => {
                            this.check_email_match(this.email, this.repeat_email, this.repeat_email_msg);
                        });
                    }
                });
            }
        } else {
            console.log("No email field, continuing...");
        }

        if (this.repeat_email) {
            if (this.repeat_email.classList.contains("realtime-validate")) {
                ["keyup", "paste", "load"].forEach((event) => {
                    this.repeat_email.addEventListener(event, () => {
                        this.check_email_match(this.email, this.repeat_email, this.repeat_email_msg);
                    });
                });
            }
        } else {
            console.log("No email-repeat field, continuing...");
        }

        if (this.username) {
            if (this.username.classList.contains("realtime-validate")) {
                ["keyup", "paste", "load"].forEach((event) => {
                    this.username.addEventListener(event, () => {
                        this.check_username(this.username, this.username_msg);
                    });
                });
            }
        } else {
            console.log("No username field, continuing...");
        }

        if (this.login) {
            if (this.login.classList.contains("realtime-validate")) {
                ["keyup", "paste", "load"].forEach((event) => {
                    this.login.addEventListener(event, () => {
                        this.check_login(this.login, this.login_msg);
                    });
                });
            }
        } else {
            console.log("No login field, continuing...");
        }

        if (this.new_password) {
            if (this.new_password.classList.contains("realtime-validate")) {
                ["keyup", "paste", "load"].forEach((event) => {
                    this.new_password.addEventListener(event, () => {
                        this.check_password_match(this.new_password,
                            this.repeat_new_password, this.repeat_new_password_msg);
                    });
                });
            }
        } else {
            console.log("No new-password field, continuing...");
        }

        if (this.repeat_new_password) {
            if (this.repeat_new_password.classList.contains("realtime-validate")) {
                ["keyup", "paste", "load"].forEach((event) => {
                    this.repeat_new_password.addEventListener(event, () => {
                        this.check_password_match(this.new_password,
                            this.repeat_new_password, this.repeat_new_password_msg);
                    });
                });
            }
        } else {
            console.log("No repeat-new-password field, continuing...")
        }
        this.enable_smart_submit()
    }


//Check functions
    check_username(username, username_msg, async = true) {
        username.value = username.value.trim().replace(/\s+/g, '');
        if (!username.value.trim()) {
            username_msg.innerHTML = "";
            this.username_ok = !username.hasAttribute('required');
        } else {
            let xhr = new XMLHttpRequest();
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    let response = xhr.responseText.split(";", 2);
                    username_msg.className = "credentials-check " + response[0];
                    username_msg.innerHTML = response[1];
                    this.username_ok = response[0] === "ok";
                    this.validate_form();
                }
            };

            xhr.open("POST", "/check_username/", async);
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhr.send("username=" + username.value);
        }
        this.validate_form();
    }


    check_login(login, login_msg, async = true) {
        login.value = login.value.trim().replace(/\s+/g, '');
        if (!login.value.trim()) {
            login_msg.innerHTML = "";
            this.login_ok = !login.hasAttribute('required');
        } else {
            let xhr = new XMLHttpRequest();
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    let response = xhr.responseText.split(";", 2);
                    login_msg.className = "credentials-check " + response[0];
                    login_msg.innerHTML = response[1];
                    this.login_ok = response[0] === "ok";
                    this.validate_form();
                }
            };

            xhr.open("POST", "/check_login/", async);
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhr.send("login=" + login.value);
        }
        this.validate_form();
    }


    check_email(email, email_msg, async = true) {
        email.value = email.value.trim().replace(/\s+/g, '');
        if (!email.value) {
            email_msg.innerHTML = "";
            this.email_ok = !email.hasAttribute('required');
        } else {
            let xhr = new XMLHttpRequest();
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    let response = xhr.responseText.split(";", 2);
                    email_msg.className = "credentials-check " + response[0];
                    email_msg.innerHTML = response[1];
                    this.email_ok = response[0] === "ok";
                    this.validate_form();
                }
            };
            xhr.open("POST", "/check_email/", async);
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhr.send("email=" + email.value);
        }
        this.validate_form();
    }


    check_email_match(email, email_repeat, email_match_msg) {
        if (!email.value && email.hasAttribute('required') &&
            !email_repeat.value && email_repeat.hasAttribute('required')) {
            this.email_match_ok = false;
        } else if (email.value !== email_repeat.value) {
            email_match_msg.innerHTML = "Emails do not match";
            email_match_msg.className = "credentials-check error";
            this.email_match_ok = false;
        } else {
            email_match_msg.innerHTML = "";
            this.email_match_ok = true;
        }
        this.validate_form();
    }


    check_password_match(password, password_repeat, password_msg) {
        if (!password.value && password.hasAttribute('required') &&
            !password_repeat.value && password_repeat.hasAttribute('required')) {
            password_msg.innerHTML = "";
            this.password_match_ok = false;
        } else if (!password.value.trim() && !password_repeat.value.trim()) {
            password_msg.innerHTML = "";
        } else if (password.value !== password_repeat.value) {
            password_msg.innerHTML = "Passwords do not match";
            password_msg.className = "credentials-check error";
            this.password_match_ok = false;
        } else if (password.value === password_repeat.value) {
            password_msg.innerHTML = "Passwords match";
            password_msg.className = "credentials-check ok";
            this.password_match_ok = true;
        }
        this.validate_form();
    }

    check_required(required_msg) {
        this.required_ok = true;
        required_msg.innerHTML = "";
        Array.from(this.required).forEach((i) => {
            if (!i.value) {
                this.required_ok = false;
                required_msg.innerHTML = "Please fill in all required fields";
                required_msg.className = "credentials-check error";
            }
        });
        this.validate_form();
    }


    validate_all() {
        if (this.username) {
            this.check_username(this.username, this.username_msg, false);
        }
        if (this.login) {
            this.check_login(this.login, this.login_msg, false);
        }
        if (this.email) {
            this.check_email(this.email, this.email_msg, false);
        }
        if (this.repeat_email) {
            this.check_email_match(this.email, this.repeat_email, this.repeat_email_msg);
        }
        if (this.new_password && this.repeat_new_password) {
            this.check_password_match(this.new_password, this.repeat_new_password, this.repeat_new_password_msg);
        }
        if (this.required) {
            this.check_required(this.required_msg);
        }
        // Enabling or disabling form submission
        var ok = this.email_ok && this.email_match_ok && this.username_ok && this.login_ok && this.password_match_ok && this.required_ok;
        if (!ok) {
            this.submit.classList.add("disabled")
        } else {
            this.submit.classList.remove("disabled");
        }
        return ok;
    }


    // Enabling or disabling form submission
    validate_form() {
        if (this.email_ok && this.email_match_ok && this.username_ok && this.login_ok && this.password_match_ok && this.required_ok) {
            this.submit.classList.remove("disabled");
            return false;
        } else {
            this.submit.classList.add("disabled");
            return true;
        }
    }
}


let forms = document.getElementsByClassName("validated");
Array.from(forms).forEach((f) => {
    f = new form(f);
    f.setup();
});