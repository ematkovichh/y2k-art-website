from PIL import Image, ImageEnhance, ImageFilter, ImageChops
import numpy as np, os
IMG="/sessions/beautiful-pensive-edison/mnt/outputs/img"
def cover(im,w,h):
    iw,ih=im.size;s=max(w/iw,h/ih)
    n=im.resize((max(w,int(iw*s)+1),max(h,int(ih*s)+1)),Image.LANCZOS)
    x=(n.width-w)//2;y=(n.height-h)//2
    return n.crop((x,y,x+w,y+h)).convert("RGB")
def wash(im,c,a): return Image.blend(im,Image.new("RGB",im.size,c),a)
def bloom(im,a): return Image.blend(im,ImageChops.screen(im,im.filter(ImageFilter.GaussianBlur(18))),a)
def pix(im,b):
    w,h=im.size;return im.resize((max(1,w//b),max(1,h//b)),Image.BILINEAR).resize((w,h),Image.NEAREST)
def scan(im,s=.15):
    w,h=im.size;a=np.asarray(im).astype(float);r=(np.arange(h)%2==0).astype(float)*s;a*=(1-r)[:,None,None]
    return Image.fromarray(np.clip(a,0,255).astype("uint8"),"RGB")
def grain(im,amt=8):
    w,h=im.size;n=np.random.normal(0,amt,(h,w,1));a=np.clip(np.asarray(im).astype(float)+n,0,255).astype("uint8")
    return Image.fromarray(a,"RGB")
def shine(im,st):
    w,h=im.size;yy,xx=np.mgrid[0:h,0:w];d=(xx/w+(h-yy)/h)/2;g=np.clip((d-.42)*2.2,0,1)**1.6
    m=Image.fromarray((g*255*st).astype("uint8"),"L")
    return Image.composite(ImageChops.screen(im,Image.new("RGB",(w,h),(255,255,255))),im,m)
S=lambda f:Image.open(f"{IMG}/{f}")
def y2k(src,w,h,o):
    im=cover(S(src),w,h);im=ImageEnhance.Color(im).enhance(.95);im=wash(im,(255,160,205),.15);im=pix(im,4);im=scan(im,.16);im=grain(im,8);im.save(f"{IMG}/{o}",quality=84);print(o)
def soft(src,w,h,o):
    im=cover(S(src),w,h);im=ImageEnhance.Brightness(im).enhance(1.12);im=ImageEnhance.Contrast(im).enhance(.9);im=wash(im,(255,225,240),.16);im=bloom(im,.55);im=shine(im,.12);im=im.filter(ImageFilter.GaussianBlur(4.0));im.save(f"{IMG}/{o}",quality=85);print(o)
def shr(src,w,h,o):
    im=cover(S(src),w,h);im=wash(im,(255,170,205),.12);im=pix(im,6);im=scan(im,.14);im.save(f"{IMG}/{o}",quality=84);print(o)
# Y2K (pink bedroom / nostalgia / VHS)
y2k("game.jpg",600,450,"y2kcrt.jpg")
y2k("office.jpg",500,500,"y2k_a.jpg")
y2k("golden.jpg",500,500,"y2k_b.jpg")
y2k("y2k.jpg",500,500,"y2k_c.jpg")
# Soft (pastel dreamy blur)
soft("angels.jpg",600,800,"soft_a.jpg")
soft("crystal.jpg",600,800,"soft_b.jpg")
# Shrine (pixelated found thumbnails)
shr("crystal.jpg",400,400,"shr_a.jpg")
shr("angels.jpg",400,400,"shr_b.jpg")
shr("neon.jpg",400,400,"shr_c.jpg")
shr("soft.jpg",400,400,"shr_d.jpg")
print("DONE")
