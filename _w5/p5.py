from PIL import Image, ImageEnhance, ImageFilter, ImageChops
import numpy as np
IMG="/sessions/beautiful-pensive-edison/mnt/outputs/img"
im=Image.open(f"{IMG}/crystal.jpg").convert("RGB")
w,h=im.size
# zoom into a different region for a fresh macro
im=im.crop((int(w*0.18),int(h*0.10),int(w*0.92),int(h*0.86)))
im=im.resize((600,800),Image.LANCZOS)
im=ImageEnhance.Color(im).enhance(1.18);im=ImageEnhance.Brightness(im).enhance(1.06)
im=Image.blend(im,Image.new("RGB",im.size,(150,235,255)),0.12)   # cyan/iridescent
im=Image.blend(im,ImageChops.screen(im,im.filter(ImageFilter.GaussianBlur(16))),0.5)
yy,xx=np.mgrid[0:800,0:600];d=(xx/600+(800-yy)/800)/2;g=np.clip((d-.4)*2.2,0,1)**1.6
m=Image.fromarray((g*255*0.28).astype("uint8"),"L")
im=Image.composite(ImageChops.screen(im,Image.new("RGB",(600,800),(255,255,255))),im,m)
im=im.filter(ImageFilter.GaussianBlur(1.8))
im.save(f"{IMG}/crystal2.jpg",quality=85);print("crystal2 ok")
