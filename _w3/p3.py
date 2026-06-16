from PIL import Image, ImageEnhance, ImageFilter, ImageChops
import numpy as np, os
IMG="/sessions/beautiful-pensive-edison/mnt/outputs/img"
def cover(im,w,h):
    iw,ih=im.size;s=max(w/iw,h/ih)
    n=im.resize((max(w,int(iw*s)+1),max(h,int(ih*s)+1)),Image.LANCZOS)
    x=(n.width-w)//2;y=(n.height-h)//2
    return n.crop((x,y,x+w,y+h)).convert("RGB")
def bloom(im,amt): return Image.blend(im,ImageChops.screen(im,im.filter(ImageFilter.GaussianBlur(18))),amt)
def wash(im,color,a): return Image.blend(im,Image.new("RGB",im.size,color),a)
def shine(im,strength):
    w,h=im.size;yy,xx=np.mgrid[0:h,0:w];d=(xx/w+(h-yy)/h)/2
    g=np.clip((d-0.42)*2.2,0,1)**1.6
    m=Image.fromarray((g*255*strength).astype("uint8"),"L")
    return Image.composite(ImageChops.screen(im,Image.new("RGB",(w,h),(255,255,255))),im,m)
def vignette(im,amt):
    w,h=im.size;yy,xx=np.mgrid[0:h,0:w]
    r=(((xx-w/2)/(w/2))**2+((yy-h/2)/(h/2))**2)**.5
    v=np.clip(1-(r-.6)*amt,0,1)
    a=(np.asarray(im).astype(float)*v[:,:,None])
    return Image.fromarray(np.clip(a,0,255).astype("uint8"),"RGB")
def light(src,w,h):
    im=cover(Image.open(f"{IMG}/{src}"),w,h)
    im=ImageEnhance.Brightness(im).enhance(1.2);im=ImageEnhance.Contrast(im).enhance(.9);im=ImageEnhance.Color(im).enhance(1.02)
    im=wash(im,(255,235,245),.16);im=bloom(im,.55);im=shine(im,.22);return im.filter(ImageFilter.GaussianBlur(2.6))
def dark(src,w,h):
    im=cover(Image.open(f"{IMG}/{src}"),w,h)
    im=ImageEnhance.Brightness(im).enhance(.66);im=ImageEnhance.Contrast(im).enhance(1.12);im=ImageEnhance.Color(im).enhance(1.16)
    im=wash(im,(20,30,70),.18);im=bloom(im,.4);im=shine(im,.14);im=vignette(im,1.1);return im.filter(ImageFilter.GaussianBlur(2.2))
light("crystal.jpg",600,800).save(f"{IMG}/frag_light1.jpg",quality=85);print("frag_light1")
dark("techno.jpg",820,560).save(f"{IMG}/frag_dark.jpg",quality=85);print("frag_dark")
light("golden.jpg",1100,470).save(f"{IMG}/frag_light2.jpg",quality=85);print("frag_light2")
print("DONE")
