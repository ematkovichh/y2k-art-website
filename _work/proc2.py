from PIL import Image, ImageEnhance, ImageFilter, ImageChops
import numpy as np, os
W="/sessions/beautiful-pensive-edison/mnt/outputs/_work"
OUT="/sessions/beautiful-pensive-edison/mnt/outputs/img"

def cover(im,w,h):
    iw,ih=im.size; s=max(w/iw,h/ih)
    nim=im.resize((max(w,int(iw*s)+1),max(h,int(ih*s)+1)),Image.LANCZOS)
    x=(nim.width-w)//2; y=(nim.height-h)//2
    return nim.crop((x,y,x+w,y+h)).convert("RGB")
def grade(im,pink=0.12,sat=1.10,contrast=1.04,bright=1.05,bloom=0.4):
    im=ImageEnhance.Color(im).enhance(sat); im=ImageEnhance.Contrast(im).enhance(contrast); im=ImageEnhance.Brightness(im).enhance(bright)
    im=Image.blend(im,Image.new("RGB",im.size,(255,170,205)),pink)
    im=Image.blend(im,ImageChops.screen(im,im.filter(ImageFilter.GaussianBlur(16))),bloom)
    return im
def shine(im,strength=0.2):
    w,h=im.size; yy,xx=np.mgrid[0:h,0:w]; d=(xx/w+(h-yy)/h)/2.0
    g=np.clip((d-0.42)*2.2,0,1)**1.6
    mask=Image.fromarray((g*255*strength).astype("uint8"),"L")
    return Image.composite(ImageChops.screen(im,Image.new("RGB",(w,h),(255,255,255))),im,mask)
def save(im,n,q=84): im.save(os.path.join(OUT,n),quality=q); print("saved",n,im.size)

n1=Image.open(f"{W}/new1.png").convert("RGB")  # 688x384 nightlife
n2=Image.open(f"{W}/new2.png").convert("RGB")  # 688x384 nostalgia
C={
 "club":  (n1,(12,46,335,158)),
 "rave":  (n1,(356,46,676,158)),
 "office":(n1,(12,223,335,338)),
 "street":(n1,(356,223,676,338)),
 "game":  (n2,(12,46,335,158)),
 "pile":  (n2,(356,72,676,172)),
 "golden":(n2,(12,223,335,338)),
 "techno":(n2,(356,223,676,338)),
}
for name,(src,box) in C.items():
    im=cover(src.crop(box),520,690)
    im=grade(im,pink=0.13,sat=1.12)
    im=shine(im,0.20)
    im=im.filter(ImageFilter.GaussianBlur(2.4))
    save(im,name+".jpg")
print("DONE")
