#! c:/program/python/python.exe	-u
"""	Monty's	Postcard Server



"""
import os, cgi
import HTMLgen
from CONST import *
import smtplib
import time
import os
import string, random
import Image				# PIL

#print 'content-type: text/plain\n'
	
def	CreateThumbnail(imagedir,infile):
	"""	Creates	a thumbnail	of the <infile>, 
	if <imagedir> doesn't exists creates the subdirectory"""
	thumbdir = os.path.join(imagedir,'.thumbnails')
	if not os.access(thumbdir,0):
		os.mkdir(thumbdir)
	
	outfile	= os.path.join(thumbdir,infile)
	if not os.access(outfile,0):
		infilepath = os.path.join(imagedir,infile)
		try:
			im = Image.open(infilepath)
			im.thumbnail((75, 112))
			im.save(outfile, "JPEG")
		except IOError:
			print "cannot create thumbnail for", infilepath
	
		

def	xCreateTable(imagedir,imglist):
	"""	Creates	a table	with all the pictures in imglist
	"""
	tlist =	[]
	row	= []
	i =	1
	for	img	in imglist:
		if not os.path.isdir(os.path.join(imagedir,img)):
			CreateThumbnail(imagedir,img)
			if i % MAXIMGPERROW	== 0:
				tlist.append(row)
				row	= []
			imgTitle = os.path.splitext(img)
			imgsrc = '<img src="' +	imagedir + '/.thumbnails/' + img + '" >'
			imgpath	= os.path.join(imagedir,img)
			reftag = '<a href="' + CREATECARD +	'?image=' +	imgpath	+ '">' + imgsrc	+ '</a><br>' + imgTitle[0]
			row.append(reftag)
			i =	i +	1
	tlist.append(row)									# append the last pictures	  
	t =	HTMLgen.Table('Previews')
	t.border = 0
	t.width	= ''
	t.border = '1'
	t.body = tlist
	return t

def	CreateDirTable(imagedir,dirlist):
	"""	Creates	a table	with all the subdirectories	
	"""
	tlist =	[]
	row	= []
	i =	0
	for	d in dirlist:
		if '.' != d[0]:
			files =	os.listdir(os.path.join(imagedir,d))
			nFiles = len(files)
			i =	i +	1
			if i % MAXIMGPERROW	== 0:
				tlist.append(row)
				row	= []
			reftag = '<a href="' + HTTPHOME	+ '?path=' + os.path.join(imagedir,d) +	'">' + d + '</a>(' + str(nFiles) + ')'
			row.append(reftag)
	tlist.append(row)									# append the last pictures	  
	t =	HTMLgen.Table('Groups')
	t.border = 0
	t.width	= ''
	t.body = tlist
	return t



def	CreatePreview():
	"""	Scans the IMAGEDIR and creates an HTML-page	with all the images
	"""
	env	= cgi.FieldStorage()
	imglist	= []
	hreflist = []
	dirlist	= []
	if env.has_key('path'):
		imagedir = env['path'].value
	else:
		imagedir = IMAGEDIR
	
	
	tmplist	= os.listdir(imagedir)
	for	i in tmplist:
		if(os.path.isdir(os.path.join(imagedir,i))):
			dirlist.append(i)
		else:
			CreateThumbnail(imagedir,i)
			imgpath	= os.path.join(imagedir,".thumbnails",i)
			imglist.append(imgpath)
			imgpath = os.path.join(imagedir,i)
			href = CREATECARD +	'?image=' +	imgpath
			hreflist.append(href)
		
	preview	= HTMLgen.TemplateDocument(PREVIEWHTML)
	preview.cgi	= 1					  
	dirTable = CreateDirTable(imagedir,dirlist)
	imgTable = CreateTable(hreflist,imglist)
	preview.substitutions =	{DIRTABLE:dirTable,IMGTABLE:imgTable}
	preview.write()



def	CreateCard():
	env	= cgi.FieldStorage()
	img	= env['image']
	page = HTMLgen.TemplateDocument(CREATECARDHTML)
	page.cgi = 1
	imgsrc = img.value
	page.substitutions = {'mpPicture':imgsrc,'mpFormAction':FORMACTION}
	page.write()


def	randStr(n, lower=1,	duplicates=1):
	if lower:
		chars =	string.lowercase
	else:
		chars =	string.letters
	chars =	list(chars)
	char_list =	[None]*n
	for	i in range(0,n):
		ch = random.choice(chars)
		char_list[i] = ch
		if not duplicates:
			chars.remove(ch)
	return string.join(char_list, '')


def	RemoveCard():
	cardlist = os.listdir(POSTCARDDIR)
	today =	time.time()
	for	card in	cardlist:
		path = POSTCARDDIR + card
		if not os.path.isdir(path):
			if (today -	os.path.getmtime(path))	> (MAXDAYS * 86400):
				os.remove(path)


def	CreateHTMLCard(env):
	fname =	randStr(8) + '.htm'
	while os.access(POSTCARDDIR	+ fname,0):
		fname =	randStr(8) + '.htm'

	pcard =	HTMLgen.TemplateDocument (PCARDHTML)
	pcard.bgcolor =	env['bgcolor']
	pcard.textcolor	= env['textcolor']
	snd	= '<a href="mailto://%s">%s</a>' % (env['smail'].value,env['sname'].value)
	msg= string.replace(env['message'].value,"\012","<br>")
	pcard.substitutions	= {'mpPicture':env['image'].value,'mpMsg':msg,'mpSender':snd,'mpHttp':HTTPHOME}
	pcard.write(POSTCARDDIR	+ fname)
	return POSTCARDHTTP	+ fname

def	SendCard():
	env	= cgi.FieldStorage()
	fromaddr ='From: ' + env['smail'].value
	toaddr = 'To: '	+ env['rmail'].value
	pcardlink =	CreateHTMLCard(env)
	msg	= EMAILMSG % (env['sname'].value,pcardlink,MAXDAYS)
	try:
		server = smtplib.SMTP(SMTPHOST)
		server.sendmail(fromaddr, toaddr, msg)
		server.quit()
		mailOK = 1
	except:
		print 'content-type: text/plain\n'
		print '-' *	60
		traceback.print_exc(file=sys.stdout)
		print '*' *	60
		mailOK = 0

	# remove old postcards
	RemoveCard()
	# create thank you page
	if mailOK:
		thanks = HTMLgen.TemplateDocument(THANKSHTML)
		thanks.substitutions = {'mpHttpCard':pcardlink,'mpReceiver':toaddr,'mpHttp':HTTPHOME}
		thanks.cgi = 1
		thanks.write()
	else:
		pass


def	CreateThumb():
	"""	Scans the IMAGEDIR and creates an HTML-page	with all the images
	"""
	env	= cgi.FieldStorage()
	imglist	= []
	dirlist	= []
	if env.has_key('path'):
		imagedir = env['path'].value
	else:
		imagedir = IMAGEDIR
	
	
	tmplist	= os.listdir(imagedir)
	for	i in tmplist:
		if(os.path.isdir(os.path.join(imagedir,i))):
			pass
		else:
			CreateThumbnail(imagedir,i)
			

# below is meHTML

import string


TD = """<TD></TD>
<TD></TD>
<!--Start of picture-->
<TD valign="top">
<TABLE>
  <TBODY>
    <TR align="left" valign="top">
      <TD>
        <TABLE bgcolor="#c0c0c0" border="4" bordercolordark="#000000" bordercolorlight="#666666">
          <TBODY>
            <TR>
              <TD align="middle" height="152" valign="center" width="137">
                <TABLE>
                  <TBODY>
                    <TR>
                      <TD>
                        <A href="MEHREF">
                        <IMG height="112" src="MEIMG" width="75"></A>
                      </TD>
                    </TR>
                  </TBODY>
                </TABLE>
              </TD>
            </TR>
          </TBODY>
        </TABLE>
      </TD>
    </TR>
    <TR>
      <TD>
      </TD>
    </TR>
  </TBODY>
</TABLE>
</TD>
"""

TABLE="""<TABLE border="0" cellpadding="0" cellspacing="0" width="100%">
<TBODY align="center">
<TR>
  <TD valign="top">
    <TABLE>
      <TBODY>"""
      
eTABLE="""</TBODY>
        </TABLE>
      </TD>
    </TR>
  </TBODY>
</TABLE>
"""

TR="""<TR>"""
eTR="""</TR>"""


def CreateCell(href,img):
	""" creates the HTML code for one table column. Using href as link and img as image."""
	tmp = string.replace (TD, "MEHREF",href)
	htmlPicture = string.replace(tmp,"MEIMG",img)
	return htmlPicture
	
	
def CreateTable(hrefList,imgList):
	""" creates the HTML code for the thumbnail table"""
	nLen = len(hrefList)
	nRows = nLen / 4
	if nLen % 4 > 0:
		nRows = nRows + 1
	n = 0;
	sTable = TABLE
	for i in range(nRows):
		sRow = TR
		for i in range(4):
			if n < nLen:
				sRow = sRow + CreateCell(hrefList[n],imgList[n])
			n = n + 1
		sRow = sRow + eTR
		sTable = sTable + sRow
	sTable = sTable + eTABLE
	return sTable
		


if __name__ == '__main__':
	hrefList = []
	imgList = []
	for i in range(25):
		href = "pic/img%d.jpg" % i
		hrefList.append(href)
		img = "img%d.jpg" % i
		imgList.append(img)
	str = CreateTable(hrefList,imgList)
	f = open("xxx.html","w")
	f.write(str)
	f.close()
	print "done"
	
		