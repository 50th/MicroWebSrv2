from MicroWebSrv2  import *
from time          import sleep
from _thread       import allocate_lock

# ============================================================================
# ============================================================================
# ============================================================================

@WebRoute(GET, '/test-redir')
def RequestTestRedirect(microWebSrv2, request) :
    request.Response.ReturnRedirect('/test.pdf')

# ============================================================================
# ============================================================================
# ============================================================================

@WebRoute(GET, '/test-post', name='TestPost1/2')
def RequestTestPost(microWebSrv2, request) :
    content = """\
    <!DOCTYPE html>
    <html>
        <head>
            <title>POST 1/2</title>
        </head>
        <body>
            <h2>MicroWebSrv2 - POST 1/2</h2>
            User address: %s<br />
            <form action="/test-post" method="post">
                First name: <input type="text" name="firstname"><br />
                Last name:  <input type="text" name="lastname"><br />
                <input type="submit" value="OK">
            </form>
        </body>
    </html>
    """ % request.UserAddress[0]
    request.Response.ReturnOk(content)

# ------------------------------------------------------------------------

@WebRoute(POST, '/test-post', name='TestPost2/2')
def RequestTestPost(microWebSrv2, request) :
    data = request.GetPostedForm()
    try :
        firstname = data['firstname']
        lastname  = data['lastname']
    except :
        request.Response.ReturnBadRequest()
        return
    content   = """\
    <!DOCTYPE html>
    <html>
        <head>
            <title>POST 2/2</title>
        </head>
        <body>
            <h2>MicroWebSrv2 - POST 2/2</h2>
            Hello %s %s :)<br />
        </body>
    </html>
    """ % ( MicroWebSrv2.HTMLEscape(firstname),
            MicroWebSrv2.HTMLEscape(lastname) )
    request.Response.ReturnOk(content)

# ------------------------------------------------------------------------

@WebRoute(GET, '/test-upload', name='TestUpload1/2')
def RequestTestPost(microWebSrv2, request):
    content = """\
        <!DOCTYPE html>
        <html>

        <head>
        <title>File Upload Test</title>
        </head>

        <body>
        <h2>MicroWebSrv2 - File Upload Test</h2>
        <form action="/test-upload"
                method="post"
                enctype="multipart/form-data"
                >
            First name: <input type="text" name="firstname"><br />
            Last name: <input type="text" name="lastname"><br />
            File: <INPUT TYPE=FILE ID=UPLOAD_IMG_ID NAME=UPLOAD_FILE />
            <input type="submit" value="OK">
        </form>
        </body>

        </html>
    """
    request.Response.ReturnOk(content)

# ------------------------------------------------------------------------

@WebRoute(POST, '/test-upload', name='TestUpload2/2')
def RequestTestPost(microWebSrv2, request) :
    data = request.GetPostedForm()
    try:
        firstname = data['firstname']
        lastname = data['lastname']
        saved_as = data['saved_as']
        filename = data['UPLOAD_FILE']
    except:
        firstname = ""
        lastname = ""
        filename = ""
    # content = """\
    # <!DOCTYPE html>
    # <html>
    #     <head>
    #         <title>File upload result</title>
    #     </head>
    #     <body>
    #         <h2>File upload result</h2>
    #         Hello %s %s :) -- you uploaded %s (server saved to %s)<br />
    #     </body>
    # </html>
    # """ % (MicroWebSrv2.HTMLEscape(firstname),
    #        MicroWebSrv2.HTMLEscape(lastname),
    #        MicroWebSrv2.HTMLEscape(filename),
    #        MicroWebSrv2.HTMLEscape(saved_as)
    #        )
    request.Response.ReturnOk('ok')


print()

# Loads the PyhtmlTemplate module globally and configure it,
pyhtmlMod = MicroWebSrv2.LoadModule('PyhtmlTemplate')
pyhtmlMod.ShowDebug = True
pyhtmlMod.SetGlobalVar('TestVar', 12345)

# Instanciates the MicroWebSrv2 class,
mws2 = MicroWebSrv2()

# SSL is not correctly supported on MicroPython.
# But you can uncomment the following for standard Python.
# mws2.EnableSSL( certFile = 'SSL-Cert/openhc2.crt',
#                 keyFile  = 'SSL-Cert/openhc2.key' )

# For embedded MicroPython, use a very light configuration,
mws2.SetLightConfig()

# Allow up to 32 MB upload
mws2.MaxRequestContentLength = 32 * 1024 * 1024

# On a slower network, upload might take a while
mws2.RequestsTimeoutSec = 60

# All pages not found will be redirected to the home '/',
mws2.NotFoundURL = '/'
mws2.UploadPath = './www'
mws2.BindAddress = ("0.0.0.0", 8765)

# Starts the server as easily as possible in managed mode,
mws2.StartManaged()

# Main program loop until keyboard interrupt,
try :
    while mws2.IsRunning :
        sleep(1)
except KeyboardInterrupt :
    pass

# End,
print()
mws2.Stop()
print('Bye')
print()

# ============================================================================
# ============================================================================
# ============================================================================
