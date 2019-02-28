# Form validation script

In `/static/javascript/` you will find the `validate_form.js` file. 
It is a script written in javascript that allows you to validate any forms on the website that have supported fields.
This is how you can use it.

##### This script can validate the following:
* **Fields**
  * `Username` _is checked for correct syntax and being free._
  * `Email` _is checked for correct syntax and being free._
  * `Password` _is checked for correct syntax._
  * `Login` _is checked for being **taken**_ (used only on user login).
  * `Email-repeat` _is checked for match with `Email`._
  * `Password-repeat` _is checked for match with `Password`._
* **If all the _required_ fields are filled in.**

#### Linking the script
To link the script, just paste this line at the end of the page:
```html
<script src="{{ url_for('static', filename='javascript/validate_form.js') }}"></script>
```

#### How to use:
The script is used just by adding special classes to the elements. To enable the script, you need 
to **add** the `validated` class **to the each form** you want to be validated **itself**. You can 
validate as many forms on one page as you want.

##### Class names used in the script

* Classes for form elements (`input` tag)
    * `email` for emails.  
    * `repeat-email` for repeating emails.  
    * `username` for usernames.  
    * `login` for logins (username or email).  
    * `new-password` for passwords.  
    * `repeat-new-password` for repeating passwords.  

* Classes for feedback elements (`p` tag)
    * `login-check` tells if the login is **present**.
    * `email-check` tells if the email is taken or has incorrect syntax.
    * `email-match-check` tells if the emails mismatch.
    * `username-check` tells if the username is taken or has incorrect syntax.
    * `new-password-check` tells if the passwords mismatch or has incorrect syntax.
    * `repeat-new-password-check` tells if the passwords mismatch.
    * `required-check` tells if the required fields are not filled.

***NOTE!*** *The classes above should be **unique** in one form.*
    
If the field is required, add the `required` attribute.

If the field needs to be validated in real time, as the user types, add the `realtime-validate` class.

##### Validated form example
**This form will be validated by the script:**
```html
<form action="/action/" class="validated">    
    <label>Register</label>
    
    <input class="email">
    <p class="email-check"></p>
    
    <input class="username realtime-validate" required>           
    <p class="username-check"></p>
    
    <input class="new-password" required>    
    <p class="repeat-new-password-check"></p>       
    <input class="repeat-new-password realtime-validate" required>           
    <p class="repeat-new-password-check"></p>
    
    <button>Submit</button>
    <p class="required-check"></p>
</form>
<script src="{{ url_for('static', filename='javascript/validate_form.js') }}"></script>
```

#### Smart submit
The form is validated as the user types (for all fields with `realtime-validate` class) and one more time
before submission. After each failed validation _Smart submit_ feature blocks form submission
and notifies the user about the fields that the script failed to validate. Blocking
is achieved by adding the `disabled` class to the button and preventing form submission in
javascript. The button may look disabled, but it is still clickable.  
***Do not disable the button in CSS with `pointer-events: none` as you may block 
form submission completely!***

