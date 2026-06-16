from PIL import Image, ImageEnhance, ImageFilter, ImageChops, ImageDraw
import numpy as np, random
IMG="/sessions/beautiful-pensive-edison/mnt/outputs/img"
W,H=820,470
def cover(im,w,h):
    iw,ih=im.size;s=max(w/iw,h/ih)
    n=im.resize((max(w,int(iw*s)+1),max(h,int(ih*s)+1)),Image.LANCZOS)
    x=(n.width-w)//2;y=(n.height-h)//2
    return n.crop((x,y,x+w,y+h)).convert("RGB")
base=cover(Image.open(f"{IMG}/y2k.jpg"),W,H)   # pink room + CRT = crystalcore base
base=ImageEnhance.Brightness(base).enhance(1.08);base=ImageEnhance.Color(base).enhance(1.06)
base=Image.blend(base,Image.new("RGB",(W,H),(255,193,225)),0.12)  # pink/lilac haze
# rainbow prism light-leaks (two diagonal bands)
yy,xx=np.mgrid[0:H,0:W]
def band(center,width,phase):
    t=((xx+(H-yy))/(W+H))
    r=0.5+0.5*np.sin(2*np.pi*(t*3+phase));g=0.5+0.5*np.sin(2*np.pi*(t*3+phase+.33));b=0.5+0.5*np.sin(2*np.pi*(t*3+phase+.66))
    m=np.exp(-((t-center)**2)/(2*width**2))
    return (np.stack([r,g,b],-1)*m[...,None]*255).astype("uint8")
rb=Image.fromarray(np.clip(band(0.62,0.09,0)+band(0.30,0.06,0.4),0,255).astype("uint8"),"RGB").filter(ImageFilter.GaussianBlur(6))
base=Image.blend(base,ImageChops.screen(base,rb),0.34)
# crystal sparkles
spk=Image.new("RGB",(W,H),(0,0,0));d=ImageDraw.Draw(spk)
random.seed(7)
for _ in range(7):
    x,y=random.randint(40,W-40),random.randint(30,H-60);s=random.randint(8,20)
    d.line((x-s,y,x+s,y),fill=(255,255,255),width=2);d.line((x,y-s,x,y+s),fill=(255,255,255),width=2)
    d.ellipse((x-2,y-2,x+2,y+2),fill=(255,255,255))
spk=spk.filter(ImageFilter.GaussianBlur(1.4))
base=ImageChops.screen(base,spk)
# bloom + shine + heavy blur
base=Image.blend(base,ImageChops.screen(base,base.filter(ImageFilter.GaussianBlur(20))),0.42)
yy,xx=np.mgrid[0:H,0:W];g=np.clip(((xx/W+(H-yy)/H)/2-0.4)*2.2,0,1)**1.6
m=Image.fromarray((g*255*0.3).astype("uint8"),"L")
base=Image.composite(ImageChops.screen(base,Image.new("RGB",(W,H),(255,255,255))),base,m)
base=base.filter(ImageFilter.GaussianBlur(2.5))
base.save(f"{IMG}/cryB.jpg",quality=86);print("cryB rebuilt (crystalcore)")
