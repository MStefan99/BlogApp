
def get_text(username, link, template):
    if template == 'register':
        template = '''
        <style>
            :root {        
                font-family: sans-serif;
                color: black
            }
        </style>
        <h1>%s, you have successfully registered on galera.dev!</h1>
        <br>
        <h2>To fully enjoy your new account, you need to follow the link below and verify your email</h2>
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
    elif template == 'email_changed':
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
                    you need to follow the link below and verify your email</h2>
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

    else:
        template = 'Error! <br><br> Template not found!'
    return template % (username, link, link)
