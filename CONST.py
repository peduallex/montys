"""
    CONST.py
    Here are all the constants that we need to change

"""   
 
# The URL to the cgi-bin directory
CGIHTTP = 'http://localhost/cgi-bin/'

# the whole path to the postcard directory
POSTCARDDIR = 'D:\\XITAMI\\WEBPAGES\\POSTCARD\\'
# The url to the postcard directory
POSTCARDHTTP = 'http://localhost/postcard/'

# The path to the image directory
IMAGEDIR = 'D:\\XITAMI\\WEBPAGES\\POSTCARD\\IMAGES\\'
#the url to the image directory
IMAGEHTTP = 'http://localhost/postcard/images/'

# number of images per row
MAXIMGPERROW = 4
# size of postcard image
SIZEX = 275
SIZEY = 412

# size of thumbnail 
TSIZEX = 75
TSIZEY = 112


# number of days that the postcard will be readable. After this it will be erased
MAXDAYS = 10
# the smtp host for sending email!
SMTPHOST = 'smtpserver.swip.net'



#   email message sent to the receipient
#   This message have 3 variables that will be substitutet with these values when run:
#   %s  The name of the sender
#   %s  The link to the postcard
#   %d  The number of days that the postcard will remain on the server
EMAILMSG = """
Your friend %s has sent you a postcard!
To view it please follow this link %s
The card will remain on our server for %d days.
This postcard service is brought to you from MONTY's Postcard Server
http://montys.sourceforge.net/ """ 


# Don't touch anything below this line, unless you know what you're doing!!
# -------------------------------------------------------------------
from Montys import MONTYSPATH

# CGI APP
HTTPHOME = CGIHTTP + 'Postcard.py'
CREATECARD = CGIHTTP + 'Createcard.py'
FORMACTION = CGIHTTP + 'Sendcard.py'


# HTML
PREVIEWHTML = MONTYSPATH + '/previewcard.htm'
CREATECARDHTML = MONTYSPATH + '/createcard.htm'
PCARDHTML = MONTYSPATH + '/postcard.htm'
THANKSHTML = MONTYSPATH + '/thanks.htm'

# Template names
DIRTABLE = 'mpDirtable'
IMGTABLE = 'mpPreviewtable'

# Error message if something goes wrong when posting the mail
MAILERROR = """<h1>ERROR</h1><p>
<h2>An unexpected error occurred during mailing your receiver. Please try again (press Back on your browser)<br>
If this error persist please contact your system admin<h2>
"""