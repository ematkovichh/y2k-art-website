from PIL import Image, ImageEnhance, ImageFilter, ImageChops
import numpy as np
IMG="/sessions/beautiful-pensive-edison/mnt/outputs/img"
W,H=900,1120
im=Image.open(f"{IMG}/soft.jpg").convert("RGB")  # dreamy woman/figure base
iw,ih=im.size;s=max(W/iw,H/ih)
im=im.resize((max(W,int(iw*s)+1),max(H,int(ih*s)+1)),Image.LANCZOS)
x=(im.width-W)//2;y=(im.height-H)//2;im=im.crop((x,y,x+W,y+H))
im=ImageEnhance.Color(im).enhance(.55)            # desaturated, artsy
im=ImageEnhance.Brightness(im).enhance(1.12)
im=Image.blend(im,Image.new("RGB",(W,H),(238,232,224)),0.20)  # pale warm white wash
im=im.filter(ImageFilter.GaussianBlur(6.5))       # very blurry / artsy
# grain
n=np.random.normal(0,11,(H,W,1));im=Image.fromarray(np.clip(np.asarray(im).astype(float)+n,0,255).astype("uint8"),"RGB")
# soft vignette
yy,xx=np.mgrid[0:H,0:W];r=(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)**.5
v=np.clip(1-(r-.55)*.7,0,1);im=Image.fromarray(np.clip(np.asarray(im).astype(float)*v[:,:,None],0,255).astype("uint8"),"RGB")
im.save(f"{IMG}/liminal.jpg",quality=86);print("liminal.jpg ok",im.size)
