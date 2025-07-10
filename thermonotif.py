from escpos.printer import Usb
import sys, os, datetime

argv = sys.argv
p =  Usb(idVendor=0x0416, idProduct=0x5011, in_ep=0x81, out_ep=0x03, profile="POS-5890")
p.set(double_height=False,double_width=False, invert=False, align='left')
t = datetime.datetime.now()

def printout(words):

    # for segments that will be printed as QR
    def qr(words, params):
        content = ' '.join(words).split(' -qr ')[0]
        if(len(words) > 1): sequel = ' '.join(words).split(' -qr ')[1]
        (size, ec, center) = (7, 0, False)
        for param in params:
            if '=' in param:
                (lhs, rhs) = param.split('=')
                if lhs == 'size': size = int(rhs)
                if lhs == 'ec': ec = int(rhs)
                if lhs == 'center': center = rhs in ['Yes','yes','Y','y','True','true','T','t']

        p.qr(content, size=size, ec=ec, center=center)
        # recurse on remaining text
        if(len(sequel)): return printout(sequel.split(' '))
        return True

    word = words[0]
    sequel = words[1:]
    if '+qr' in word: 
        params = word.split(':')
        # process qr code and recurse on remaining text
        return qr(sequel, params)

    # keywords: starting with + - to begin or end formatted sections
    # and : to insert content
    if word == '+em': p.set(invert=True)
    elif word == '-em': p.set(invert=False)
    elif word == '+big': p.set(double_height=True,double_width=True)
    elif word == '-big': p.set(double_height=False,double_width=False, normal_textsize=True)
    elif word == '+center': p.set(align='center')
    elif word == '-center': p.set(align='left')
    elif word == '+right': p.set(align='right')
    elif word == '-right': p.set(align='left')
    elif word == ':br': p.text('\n')
    elif word == ':hr': p.text('\n------------------------\n')
    elif word == ':time': p.text(t.strftime("%d-%m-%Y %H:%M:%S " ))
    elif word == ':user': p.text(str(os.environ.get('USER')) + ' ')
    else: p.text(word+' ')

    # recurse on remaining text
    if(len(sequel) > 0): return printout(sequel)
    return True

printout(' '.join(list(sys.stdin)).split(' '))
p.set(double_height=False,double_width=False, invert=False, align='left')
