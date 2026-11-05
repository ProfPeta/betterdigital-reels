"""Výřezy a mírné doostření fotek z photos/src do photos/. usage: python3 -I photos/process.py"""
import os
from PIL import Image, ImageFilter
H=os.path.dirname(os.path.abspath(__file__))
def cut(n,box,out,w=None,sharp=False):
    i=Image.open(os.path.join(H,'src',n)).convert('RGB')
    if box: i=i.crop(box)
    if w and i.width!=w: i=i.resize((w,round(i.height*w/i.width)),Image.LANCZOS)
    if sharp: i=i.filter(ImageFilter.UnsharpMask(1.2,70,2))
    i.save(os.path.join(H,out),quality=92); print(out,i.size)
cut('zuckerberg.jpg',(90,20,870,1000),'zuck.jpg',880)
cut('mikolov_portret.jpg',None,'mikolov.jpg',880)
cut('arxiv_1301_3781.jpg',(30,30,1170,860),'arxiv.jpg',900)
cut('mikolov_medaile.jpg',(0,120,1250,1000),'medaile.jpg',1000)
cut('bottlecap_tym.jpg',None,'tym.jpg',1100,True)
