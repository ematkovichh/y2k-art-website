from PIL import Image, ImageEnhance, ImageFilter, ImageChops, ImageDraw
import numpy as np, random
IMG="/sessions/beautiful-pensive-edison/mnt/outputs/img"
def cover(im,w,h):
    iw,ih=im.size;s=max(w/iw,h/ih)
    n=im.resize((max(w,int(iw*s)+1),max(h,int(ih*s)+1)),Image.LANCZOS)
    x=(n.width-w)//2;y=(n.height-h)//2
    return n.crop((x,y,x+w,y+h)).convert("RGB")
def dream(src,tint,a,seed,out,blur=2.0,W=600,H=800):
    base=cover(Image.open(f"{IMG}/{src}"),W,H)
    base=ImageEnhance.Brightness(base).enhance(1.07);base=ImageEnhance.Color(base).enhance(1.08)
    base=Image.blend(base,Image.new("RGB",(W,H),tint),a)
    yy,xx=np.mgrid[0:H,0:W]
    def band(c,wd,ph):
        t=((xx+(H-yy))/(W+H))
        r=0.5+0.5*np.sin(2*np.pi*(t*3+ph));g=0.5+0.5*np.sin(2*np.pi*(t*3+ph+.33));b=0.5+0.5*np.sin(2*np.pi*(t*3+ph+.66))
        m=np.exp(-((t-c)**2)/(2*wd**2));return (np.stack([r,g,b],-1)*m[...,None]*255).astype("uint8")
    rb=Image.fromarray(np.clip(band(0.6,0.1,0)+band(0.3,0.07,0.4),0,255).astype("uint8"),"RGB").filter(ImageFilter.GaussianBlur(6))
    base=Image.blend(base,ImageChops.screen(base,rb),0.34)
    spk=Image.new("RGB",(W,H),(0,0,0));d=ImageDraw.Draw(spk);random.seed(seed)
    for _ in range(7):
        x,y=random.randint(40,W-40),random.randint(30,H-60);s=random.randint(8,18)
        d.line((x-s,y,x+s,y),fill=(255,255,255),width=2);d.line((x,y-s,x,y+s),fill=(255,255,255),width=2)
        d.ellipse((x-2,y-2,x+2,y+2),fill=(255,255,255))
    base=ImageChops.screen(base,spk.filter(ImageFilter.GaussianBlur(1.4)))
    base=Image.blend(base,ImageChops.screen(base,base.filter(ImageFilter.GaussianBlur(20))),0.45)
    g=np.clip(((xx/W+(H-yy)/H)/2-0.4)*2.2,0,1)**1.6
    m=Image.fromarray((g*255*0.28).astype("uint8"),"L")
    base=Image.composite(ImageChops.screen(base,Image.new("RGB",(W,H),(255,255,255))),base,m)
    base.filter(ImageFilter.GaussianBlur(blur)).save(f"{IMG}/{out}",quality=86);print(out)
dream("angels.jpg",(255,178,214),0.17,3,"dream1.jpg",blur=2.0)   # pink
dream("crystal.jpg",(186,150,255),0.20,11,"dream2.jpg",blur=2.2) # purple
print("DONE")
