def get_email_text(username, link, template):
    if template == 'register':
        subject = 'galera.dev registration'
        template = '''
        <style>
            :root {        
                font-family: sans-serif;
                color: black
            }
        </style>
        <h1>%s, you have successfully registered on galera.dev!</h1>
        <br>
        <h2>To fully enjoy your new account, you need to follow the link below and verify your email:</h2>
        <br>
        <h3>We are happy to see you with us!</h3>
        <br>
        <a href = "https://blog.mstefan99.com/verify/?key=%s" style="display:block">
            <p>
                Verify your email
            </p>
        </a>
        <br><br>
        If you can't open the link, copy and paste this into your browser:
        https://blog.mstefan99.com/verify/?key=%s
        '''

    elif template == 'email_change':
        subject = 'galera.dev email change'
        template = '''
                <style>
                    :root {        
                        font-family: sans-serif;
                        color: black
                    }
                </style>
                <h1>%s, you have successfully changed your email on galera.dev!</h1>
                <br>
                <h2>To fully enjoy your account with new email, 
                    you need to follow the link below and verify your email:</h2>
                <br>
                <a href = "https://blog.mstefan99.com/verify/?key=%s" style="display:block">
                    <p>
                        Verify your email
                    </p>
                </a>
                <br><br>
                If you can't open the link, copy and paste this into your browser:
                https://blog.mstefan99.com/verify/?key=%s
                '''

    elif template == 'password-recovery':
        subject = 'galera.dev password change request'
        template = '''
                <style>
                    :root {        
                        font-family: sans-serif;
                        color: black
                    }
                </style>
                <h1>%s, you have requested a password change on galera.dev</h1>
                <br>
                <h2>To reset the password, you need to follow the link below:</h2>
                <br>
                <h2>If you did not request changing the password, you can just ignore this message:</h2>
                <br>
                <a href = "https://blog.mstefan99.com/recover/?key=%s" style="display:block">
                    <p>
                        Reset password
                    </p>
                </a>
                <br><br>
                If you can't open the link, copy and paste this into your browser:
                https://blog.mstefan99.com/recover/?key=%s
                '''

    else:
        subject = 'galera.dev'
        template = 'Error! <br><br> Template not found!'

    return subject, template % (username, link, link)
