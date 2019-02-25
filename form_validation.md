# Form validation script

In `/static/javascript/` you will find the `validate_form.js` file. This is how you can use it.
It is a script written in js that allows you to check any forms on the website that have supported fields.

##### This script can validate:
* **Fields**
    * `Username` _checks if the username is free._
    * `Email` _checks if the email is free._
    * `Login` _checks if the username **or** email is **taken**_ (used only on user login).
* **Repeat-fields** (to check if the user entered the data correctly)
    * `Email-repeat` _checks if it matches with `Email`._
    * `Password-repeat` _checks if it matches with `Password`._
* **If all the required fields are filled in.**

#### Linking the script
To link the script, just paste this line at the end od the page:
```html
<script src="{{ url_for('static', filename='javascript/validate_form.js') }}"></script>
```

#### How to use:
The script is used just by adding special classes to the elements. To enable the script, you need 
to **add** the `validated` class **to the each form** you want to be validated **itself**. You can 
validate as many forms on one page as you need.

##### Class names used in the script

* Classes for form elements (`input` tag)
    * `email` for emails.  
    * `repeat-email` for repeating emails.  
    * `username` for usernames.  
    * `login` for logins (username or email).  
    * `new-password` for passwords.  
    * `repeat-new-password` for repeating passwords.  

* Classes for feedback elements (`p` tag)
    * `login-check`tells if the login is **present**
    * `email-check` tells if the email is taken
    * `email-match-check` tells if the emails mismatch
    * `username-check` tells if the username is taken
    * `repeat-new-password-check` tells if the passwords mismatch
    * `required-check` tells if the required fields are not filled

***NOTE!*** *The classes above should be **unique** in one form.*
    
If the field is required, add the `required` attribute.

If the field needs to be validated in real time, as the user types, add the `realtime-validate` class.

If your form has labels, you can add the `required` class to mark it with a red star.

##### Form example
```html
<form action="/action/" class="validated">
    
    <label class="required">Register</label>
    
    <input class="email">
    <p class="email-check"></p>
    
    <input class="username realtime-validate" required>           
    <p class="username-check"></p>
    
    <input class="new-password" required>           
    <input class="repeat-new-password realtime-validate" required>           
    <p class="repeat-new-password-check"></p>
    
    <button>Submit</button>
    <p class="required-check"></p>
    
</form>
<script src="{{ url_for('static', filename='javascript/validate_form.js') }}"></script>
```

#### Smart submit
The form is validated as the user types (for all fields with `realtime-validate` class) and one more time
before submission. After each failed validation _Smart submit_ feature activates, blocking the 
submission of the form and notifying the user about the fields that failed to validate. Blocking the
button is achieved by adding the `disabled` class to the button and preventing form submission in
javascript. The button will look disabled, but it is still clickable.   
***Do not disable the button in CSS with `pointer-events: none` as you may block the 
form submission completely!***

