from escpos.printer import Usb
import datetime, os, sys, time

argv = sys.argv
p =  Usb(idVendor=0x0416, idProduct=0x5011, in_ep=0x81, out_ep=0x03, profile="POS-5890")
p.set(custom_size=False, invert=False, align='left')
t = datetime.datetime.now()

    # inv  custom W     H     align   bold  uline
P = [False,False, None, None, 'left', False, False]
    # 0     1     2     3     4       5     6

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
                if lhs == 'center': center = rhs.lower() in ['yes','y','true','t', '1']

        p.qr(content, size=size, ec=ec, center=center)

        if(len(sequel)): return printout(sequel.split(' '))
        return True

    word = words[0]
    sequel = words[1:]
    if '+qr' in word: 
        params = word.split(':')
        return qr(sequel, params)

    # keywords: starting with + - to begin or end formatted sections
    # and : to insert content
    word=word.strip()
    if word == '+em': P[0] = True
    elif word == '-em': P[0] = False 
    elif word == '+big': (P[1], P[2], P[3]) = (True, 2, 2) # double size
    elif word == '-big': (P[1], P[2], P[3]) = (False,None,None)
    elif '+size' in word: (P[1], P[2], P[3]) = (True, int(word.split('size')[1]), int(word.split('size')[1])) # any custom size eg +size3
    elif word == '-big': (P[1], P[2], P[3]) = (False,None,None)
    elif '-size' in word: (P[1], P[2], P[3]) = (False,None,None)
    elif word == '+bold': P[5] = True
    elif word == '-bold': P[5] = False
    elif word == '+ul': P[6] = True
    elif word == '-ul': P[6] = False
    elif word == '+center': P[4] = 'center'
    elif word == '-center': P[4] = 'left'
    elif word == '+right': P[4] = 'right'
    elif word == '-right': P[4] = 'left'
    elif word == ':br': p.text('\n')
    elif word == ':hr': p.text('\n--------------------------------\n')
    elif word == ':date': p.text(t.strftime("%d.%m.%Y" ))
    elif word == ':time': p.text(t.strftime("%d.%m.%Y %H:%M:%S " ))
    elif word == ':user': p.text(str(os.environ.get('USER')) + ' ')
    else: p.text(word+' ')

    p.set(invert=P[0],custom_size=P[1],width=P[2],height=P[3],align=P[4],bold=P[5],underline=P[6])

    if(len(sequel) > 0): return printout(sequel)
    return True

printout(' :br '.join(list(sys.stdin)).split(' '))
P = [False,False, None, None, 'left', False, False]
p.set(invert=P[0],custom_size=P[1],width=P[2],height=P[3],align=P[4],bold=P[5],underline=P[6])
