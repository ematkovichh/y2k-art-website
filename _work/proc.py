from PIL import Image, ImageEnhance, ImageFilter, ImageChops
import numpy as np, os

W="/sessions/beautiful-pensive-edison/mnt/outputs/_work"
OUT="/sessions/beautiful-pensive-edison/mnt/outputs/img"
os.makedirs(OUT, exist_ok=True)

def cover(im,w,h):
    iw,ih=im.size; s=max(w/iw,h/ih)
    nim=im.resize((max(w,int(iw*s)+1),max(h,int(ih*s)+1)),Image.LANCZOS)
    x=(nim.width-w)//2; y=(nim.height-h)//2
    return nim.crop((x,y,x+w,y+h)).convert("RGB")

def grade(im,pink=0.12,sat=1.10,contrast=1.04,bright=1.04,bloom=0.35):
    im=ImageEnhance.Color(im).enhance(sat)
    im=ImageEnhance.Contrast(im).enhance(contrast)
    im=ImageEnhance.Brightness(im).enhance(bright)
    wash=Image.new("RGB",im.size,(255,170,205))
    im=Image.blend(im,wash,pink)
    blur=im.filter(ImageFilter.GaussianBlur(16))
    im=Image.blend(im,ImageChops.screen(im,blur),bloom)
    return im

def shine(im,strength=0.2):
    w,h=im.size
    yy,xx=np.mgrid[0:h,0:w]
    d=(xx/w+(h-yy)/h)/2.0
    g=np.clip((d-0.42)*2.2,0,1)**1.6
    mask=Image.fromarray((g*255*strength).astype("uint8"),"L")
    white=Image.new("RGB",(w,h),(255,255,255))
    return Image.composite(ImageChops.screen(im,white),im,mask)

def pixelate(im,block):
    w,h=im.size
    return im.resize((max(1,w//block),max(1,h//block)),Image.BILINEAR).resize((w,h),Image.NEAREST)

def scanlines(im,strength=0.18):
    w,h=im.size
    a=np.asarray(im).astype(float)
    rows=(np.arange(h)%2==0).astype(float)*strength
    a*=(1-rows)[:,None,None]
    return Image.fromarray(np.clip(a,0,255).astype("uint8"),"RGB")

def grain(im,amt=10):
    w,h=im.size
    n=np.random.normal(0,amt,(h,w,1))
    a=np.clip(np.asarray(im).astype(float)+n,0,255).astype("uint8")
    return Image.fromarray(a,"RGB")

def save(im,name,q=86):
    im.save(os.path.join(OUT,name),quality=q)
    print("saved",name,im.size)

# ---- crop the clean 6-panel grid (src7: 1440x1929, 2 cols x 3 rows) ----
g=Image.open(f"{W}/src7.png").convert("RGB")
cw,ch=g.width//2, g.height//3
cells={
 "crystal":g.crop((0,0,cw,ch)),
 "atrium": g.crop((cw,0,2*cw,ch)),
 "beach":  g.crop((0,ch,cw,2*ch)),
 "crt":    g.crop((cw,ch,2*cw,2*ch)),
 "neon":   g.crop((0,2*ch,cw,3*ch)),
 "arches": g.crop((cw,2*ch,2*cw,3*ch)),
}

# crystal dreams - iridescent liquid glass, shiny, light blur
im=cover(cells["crystal"],900,1125); im=grade(im,pink=0.10,sat=1.14); im=shine(im,0.30); im=im.filter(ImageFilter.GaussianBlur(1.6)); save(im,"crystal.jpg")
# atrium (second crystal box) - shiny
im=cover(cells["atrium"],1280,800); im=grade(im,pink=0.12,sat=1.10); im=shine(im,0.22); im=im.filter(ImageFilter.GaussianBlur(1.8)); save(im,"atrium.jpg")
# neon - shiny blur
im=cover(cells["neon"],900,1200); im=grade(im,pink=0.10,sat=1.16); im=shine(im,0.18); im=im.filter(ImageFilter.GaussianBlur(2.2)); save(im,"neon.jpg")
# digital angels (glass arches in clouds) - ethereal, brighter, soft
im=cover(cells["arches"],1000,1000); im=grade(im,pink=0.16,sat=1.05,bright=1.09,bloom=0.5); im=shine(im,0.24); im=im.filter(ImageFilter.GaussianBlur(2.6)); save(im,"angels.jpg")
# lost y2k (galaxy CRT) - pixelated + scanlines + slight blur (VHS/found footage)
im=cover(cells["crt"],1000,750); im=grade(im,pink=0.08,sat=1.06); im=pixelate(im,5); im=scanlines(im,0.16); im=im.filter(ImageFilter.GaussianBlur(0.8)); im=grain(im,8); save(im,"y2k.jpg")
# soft fantasy (beach hooded figure) - dreamy heavy blur, warm
im=cover(cells["beach"],1680,800); im=grade(im,pink=0.14,sat=1.08,bright=1.06); im=shine(im,0.12); im=im.filter(ImageFilter.GaussianBlur(4.0)); save(im,"soft.jpg")

# ---- moodboard "found image" thumbnails (use a busy collage), pixelated ----
mb=Image.open(f"{W}/src3.png").convert("RGB")
mw,mh=mb.size
crops=[(0,0,mw//2,mh//2),(mw//2,mh//4,mw,mh//4+mw//2),(mw//4,mh//2,mw//4+mw//2,mh)]
for i,c in enumerate(crops,1):
    im=cover(mb.crop(c),500,500); im=grade(im,pink=0.12,sat=1.1); im=pixelate(im,7); im=scanlines(im,0.14); save(im,f"mood{i}.jpg")

print("DONE")
