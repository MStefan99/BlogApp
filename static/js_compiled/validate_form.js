"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

var form =
/*#__PURE__*/
function () {
  // Setting check variables
  function form(element) {
    _classCallCheck(this, form);

    _defineProperty(this, "form_element", void 0);

    _defineProperty(this, "email_ok", true);

    _defineProperty(this, "email_match_ok", true);

    _defineProperty(this, "login_ok", true);

    _defineProperty(this, "username_ok", true);

    _defineProperty(this, "new_password_ok", true);

    _defineProperty(this, "new_password_match_ok", true);

    _defineProperty(this, "required_ok", true);

    this.form_element = element;
  }

  _createClass(form, [{
    key: "enable_smart_submit",
    value: function enable_smart_submit() {
      var _this = this;

      if (this.submit) {
        // Disable sending directly by using submit button
        this.submit.addEventListener("click", function (e) {
          e.preventDefault();

          _this.submit.classList.add("disabled");

          if (_this.validate_all()) {
            _this.form_element.submit();
          }
        }); // Disable submitting directly using Enter key

        form.onkeypress = function (e) {
          var key = e.key;

          if (key === "Enter") {
            e.preventDefault();

            _this.submit.classList.add("disabled");

            if (_this.validate_all()) {
              _this.form_element.submit();
            }
          }
        };
      }
    }
  }, {
    key: "setup",
    value: function setup() {
      var _this2 = this;

      //  Input fields
      this.email = this.form_element.querySelector("input.email");
      this.repeat_email = this.form_element.querySelector("input.repeat-email");
      this.username = this.form_element.querySelector("input.username");
      this.login = this.form_element.querySelector("input.login");
      this.new_password = this.form_element.querySelector("input.new-password");
      this.repeat_new_password = this.form_element.querySelector("input.repeat-new-password");
      this.required = this.form_element.querySelectorAll("input[required]");
      this.submit = this.form_element.querySelector("button"); // Feedback elements

      this.login_msg = this.form_element.querySelector("p.login-check");
      this.email_msg = this.form_element.querySelector("p.email-check");
      this.repeat_email_msg = this.form_element.querySelector("p.email-match-check");
      this.username_msg = this.form_element.querySelector("p.username-check");
      this.new_password_msg = this.form_element.querySelector("p.new-password-check");
      this.repeat_new_password_msg = this.form_element.querySelector("p.repeat-new-password-check");
      this.required_msg = this.form_element.querySelector("p.required-check"); // Setting listeners

      if (this.email) {
        if (this.email.classList.contains("realtime-validate")) {
          ["keyup", "paste", "load"].forEach(function (event) {
            _this2.email.addEventListener(event, function () {
              _this2.check_email(_this2.email, _this2.email_msg);
            });

            if (_this2.repeat_email) {
              _this2.email.addEventListener(event, function () {
                _this2.check_email_match(_this2.email, _this2.repeat_email, _this2.repeat_email_msg);
              });
            }
          });
        }
      } else {
        console.log("No email field, continuing...");
      }

      if (this.repeat_email) {
        if (this.repeat_email.classList.contains("realtime-validate")) {
          ["keyup", "paste", "load"].forEach(function (event) {
            _this2.repeat_email.addEventListener(event, function () {
              _this2.check_email_match(_this2.email, _this2.repeat_email, _this2.repeat_email_msg);
            });
          });
        }
      } else {
        console.log("No email-repeat field, continuing...");
      }

      if (this.username) {
        if (this.username.classList.contains("realtime-validate")) {
          ["keyup", "paste", "load"].forEach(function (event) {
            _this2.username.addEventListener(event, function () {
              _this2.check_username(_this2.username, _this2.username_msg);
            });
          });
        }
      } else {
        console.log("No username field, continuing...");
      }

      if (this.login) {
        if (this.login.classList.contains("realtime-validate")) {
          ["keyup", "paste", "load"].forEach(function (event) {
            _this2.login.addEventListener(event, function () {
              _this2.check_login(_this2.login, _this2.login_msg);
            });
          });
        }
      } else {
        console.log("No login field, continuing...");
      }

      if (this.new_password) {
        if (this.new_password.classList.contains("realtime-validate")) {
          ["keyup", "paste", "load"].forEach(function (event) {
            _this2.new_password.addEventListener(event, function () {
              _this2.check_password(_this2.new_password, _this2.new_password_msg);

              _this2.check_password_match(_this2.new_password, _this2.repeat_new_password, _this2.repeat_new_password_msg);
            });
          });
        }
      } else {
        console.log("No new-password field, continuing...");
      }

      if (this.repeat_new_password) {
        if (this.repeat_new_password.classList.contains("realtime-validate")) {
          ["keyup", "paste", "load"].forEach(function (event) {
            _this2.repeat_new_password.addEventListener(event, function () {
              _this2.check_password_match(_this2.new_password, _this2.repeat_new_password, _this2.repeat_new_password_msg);
            });
          });
        }
      } else {
        console.log("No repeat-new-password field, continuing...");
      }

      this.enable_smart_submit();
    } //Check functions

  }, {
    key: "check_username",
    value: function check_username(username, username_msg) {
      var _this3 = this;

      var async = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : true;
      username.value = username.value.trim().replace(/\s+/g, '');

      if (!username.value.trim()) {
        username_msg.innerHTML = "";
        this.username_ok = !username.hasAttribute('required');
      } else {
        var re = /^(?=.*[a-zA-Z]+)[0-9a-zA-Z\-_.]{3,100}$/;
        this.username_ok = re.test(username.value.toLowerCase());

        if (!this.username_ok) {
          username_msg.className = "credentials-check error";
          username_msg.innerHTML = "Your username must be at least 3 symbols long " + "and include only letters, numbers or characters \"-\", \"_\" and \".\". Spaces not allowed.";
        } else {
          var xhr = new XMLHttpRequest();

          xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
              var response = xhr.responseText;

              switch (response) {
                case 'OK':
                  username_msg.className = "credentials-check ok";
                  username_msg.innerHTML = "Username is free";
                  break;

                case 'ALREADY EXISTS':
                  username_msg.className = "credentials-check error";
                  username_msg.innerHTML = "Username is already taken!";
                  break;

                default:
                  username_msg.innerHTML = "";
              }

              _this3.username_ok = response === "OK";

              _this3.validate_form();

              form.set_color(_this3.username_ok, username);
            }
          };

          xhr.open("POST", "/check_username/", async);
          xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
          xhr.send("username=" + username.value);
        }
      }

      this.validate_form();
      form.set_color(this.username_ok, username);
    }
  }, {
    key: "check_login",
    value: function check_login(login, login_msg) {
      var _this4 = this;

      var async = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : true;
      login.value = login.value.trim().replace(/\s+/g, '');

      if (!login.value.trim()) {
        login_msg.innerHTML = "";
        this.login_ok = !login.hasAttribute('required');
      } else {
        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4 && xhr.status === 200) {
            var response = xhr.responseText;

            switch (response) {
              case 'OK':
                login_msg.className = "credentials-check ok";
                login_msg.innerHTML = "User found";
                break;

              case 'NOT FOUND':
                login_msg.className = "credentials-check error";
                login_msg.innerHTML = "User not found!";
                break;

              default:
                login_msg.innerHTML = "";
            }

            _this4.login_ok = response === "OK";

            _this4.validate_form();

            form.set_color(_this4.login_ok, login);
          }
        };

        xhr.open("POST", "/check_login/", async);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send("login=" + login.value);
      }

      this.validate_form();
      form.set_color(this.login_ok, login);
    }
  }, {
    key: "check_email",
    value: function check_email(email, email_msg) {
      var _this5 = this;

      var async = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : true;
      email.value = email.value.trim().replace(/\s+/g, '');

      if (!email.value) {
        email_msg.innerHTML = "";
        this.email_ok = !email.hasAttribute('required');
      } else {
        var re = /^(([^<>()\[\]\\.,;:\s@"][\w]+(\.[^<>()\[\]\\.,;:\s@"][\w]+)*)|("\w+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        this.email_ok = re.test(email.value.toLowerCase());

        if (!this.email_ok) {
          email_msg.className = "credentials-check error";
          email_msg.innerHTML = "Invalid email format";
        } else {
          var xhr = new XMLHttpRequest();

          xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
              var response = xhr.responseText;

              switch (response) {
                case 'OK':
                  email_msg.className = "credentials-check ok";
                  email_msg.innerHTML = "Email is free";
                  break;

                case 'ALREADY EXISTS':
                  email_msg.className = "credentials-check error";
                  email_msg.innerHTML = "Email is already taken!";
                  break;

                default:
                  email_msg.innerHTML = "";
              }

              _this5.email_ok = response === "OK";

              _this5.validate_form();

              form.set_color(_this5.email_ok, email);
            }
          };

          xhr.open("POST", "/check_email/", async);
          xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
          xhr.send("email=" + email.value);
        }
      }

      this.validate_form();
      form.set_color(this.email_ok, email);
    }
  }, {
    key: "check_email_match",
    value: function check_email_match(email, email_repeat, email_match_msg) {
      if (!email.value && email.hasAttribute('required') && !email_repeat.value && email_repeat.hasAttribute('required')) {
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
      form.set_color(this.email_match_ok, email, email_repeat);
    }
  }, {
    key: "check_password",
    value: function check_password(password, password_msg) {
      var re = /^(?=.*[a-zA-Z]+)(?=.*[0-9]+)[0-9a-zA-Z!@#$%^&*(){}\[\]\-_=+,.<>|\\]{8,100}$/;
      var ok = re.test(password.value.toLowerCase());

      if (!ok) {
        password_msg.className = "credentials-check error";
        password_msg.innerHTML = "Your password must be at least 8 characters long " + "and include at least one letter and one number. Spaces not allowed.";
      } else {
        password_msg.innerHTML = "";
      }

      this.new_password_ok = ok;
      this.validate_form();
      form.set_color(this.new_password_ok, password);
    }
  }, {
    key: "check_password_match",
    value: function check_password_match(password, password_repeat, password_msg) {
      if (!password.value && password.hasAttribute('required') && !password_repeat.value && password_repeat.hasAttribute('required')) {
        password_msg.innerHTML = "";
        this.new_password_match_ok = false;
      } else if (!password.value.trim() && !password_repeat.value.trim()) {
        password_msg.innerHTML = "";
      } else if (password.value !== password_repeat.value) {
        password_msg.innerHTML = "Passwords do not match";
        password_msg.className = "credentials-check error";
        this.new_password_match_ok = false;
      } else if (password.value === password_repeat.value) {
        password_msg.innerHTML = "Passwords match";
        password_msg.className = "credentials-check ok";
        this.new_password_match_ok = true;
      }

      this.validate_form();
      form.set_color(this.new_password_ok, password);
      form.set_color(this.new_password_match_ok, password_repeat);
    }
  }, {
    key: "check_required",
    value: function check_required(required_msg) {
      var _this6 = this;

      this.required_ok = true;

      if (this.required_msg) {
        required_msg.innerHTML = "";
      }

      Array.from(this.required).forEach(function (element) {
        if (!element.value) {
          _this6.required_ok = false;
          required_msg.innerHTML = "Please fill in all required fields";
          required_msg.className = "credentials-check error";
          form.set_color(_this6.required_ok, element);
        }
      });
      this.validate_form();
    }
  }, {
    key: "validate_all",
    value: function validate_all() {
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

      if (this.new_password) {
        this.check_password(this.new_password, this.new_password_msg);
      }

      if (this.new_password && this.repeat_new_password) {
        this.check_password_match(this.new_password, this.repeat_new_password, this.repeat_new_password_msg);
      }

      if (this.required) {
        this.check_required(this.required_msg);
      } // Enabling or disabling form submission


      var ok = this.email_ok && this.email_match_ok && this.username_ok && this.login_ok && this.new_password_match_ok && this.required_ok;

      if (!ok) {
        this.submit.classList.add("disabled");
      } else {
        this.submit.classList.remove("disabled");
      }

      return ok;
    } // Enabling or disabling form submission

  }, {
    key: "validate_form",
    value: function validate_form() {
      if (this.email_ok && this.email_match_ok && this.username_ok && this.login_ok && this.new_password_match_ok && this.required_ok) {
        this.submit.classList.remove("disabled");
        return false;
      } else {
        this.submit.classList.add("disabled");
        return true;
      }
    }
  }], [{
    key: "set_color",
    value: function set_color(ok) {
      for (var _len = arguments.length, elements = new Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
        elements[_key - 1] = arguments[_key];
      }

      elements.forEach(function (element) {
        if (!element.value) {
          element.style.borderColor = "var(--accent-color)";
        } else if (ok) {
          element.style.borderColor = "var(--ok)";
        } else {
          element.style.borderColor = "var(--error)";
        }
      });
    }
  }]);

  return form;
}();

var forms = document.getElementsByClassName("validated");
Array.from(forms).forEach(function (f) {
  f = new form(f);
  f.setup();
});
//# sourceMappingURL=validate_form.js.map