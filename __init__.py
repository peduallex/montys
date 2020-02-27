"""

    The idea of electronically sending postcard has always appealed to me. 
    I have search for a CGI application that was
        Easy to install
        Easy to incorporate into my own style of web
        Easy to support, changing the images, etc
        Easy to expand. if I don't like it I can change it
        
    what I found was
        Hard to install
        Impossible to incorporate into my web
        Demanded a rewrite of the code if I wanted to change the images
        Either in binary code or in perl. Don't know which is harder to understand
        

    Montys is
        Written in Python!
        Uses html templates 
        Creates thumbnails automatically
        Will automatically change the presentation if you change the images.


                                  --------------------

""" 

# save the current path!
MONTYSPATH = __path__[0]
VERSION = "Montys version 0.1"