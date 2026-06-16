from PIL import Image, ImageEnhance, ImageFilter, ImageChops
import numpy as np
IMG="/sessions/beautiful-pensive-edison/mnt/outputs/img"
def cover(im,w,h):
    iw,ih=im.size;s=max(w/iw,h/ih)
    n=im.resize((max(w,int(iw*s)+1),max(h,int(ih*s)+1)),Image.LANCZOS)
    x=(n.width-w)//2;y=(n.height-h)//2
    return n.crop((x,y,x+w,y+h)).convert("RGB")
def shine(im,st):
    w,h=im.size;yy,xx=np.mgrid[0:h,0:w];d=(xx/w+(h-yy)/h)/2;g=np.clip((d-.4)*2.2,0,1)**1.6
    m=Image.fromarray((g*255*st).astype("uint8"),"L")
    return Image.composite(ImageChops.screen(im,Image.new("RGB",(w,h),(255,255,255))),im,m)
def cryst(src,color,a,w,h,o,sat=1.12):
    im=cover(Image.open(f"{IMG}/{src}"),w,h)
    im=ImageEnhance.Color(im).enhance(sat);im=ImageEnhance.Brightness(im).enhance(1.05)
    im=Image.blend(im,Image.new("RGB",im.size,color),a)
    im=Image.blend(im,ImageChops.screen(im,im.filter(ImageFilter.GaussianBlur(16))),0.5)
    im=shine(im,0.26);im=im.filter(ImageFilter.GaussianBlur(2.6))
    im.save(f"{IMG}/{o}",quality=85);print(o)
cryst("angels.jpg",(165,140,255),0.24,800,460,"cryB.jpg")   # violet
cryst("golden.jpg",(255,188,150),0.22,800,460,"cryC.jpg")   # warm rose-gold
cryst("neon.jpg",(150,225,255),0.22,800,460,"cryD.jpg")     # icy blue
print("DONE")
