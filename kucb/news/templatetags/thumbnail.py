from django import template
import os
import Image
register = template.Library()
THUMBSIZE = 320

@register.filter
def thumbnail(img):
    p = img.path.split('.')
    u = img.url.split('.')
    thumb_path = ".".join(p[:-1])+"_thumbnail."+p[-1]
    thumb_url = ".".join(u[:-1])+"_thumbnail."+u[-1]

    if os.path.exists(thumb_path):
        return thumb_url
    orig = Image.open(img.path)
    if orig.size[0]<THUMBSIZE:
        return img.url

    ratio = float(orig.size[1])/orig.size[0]
    x = THUMBSIZE
    y = int(x * ratio)
    thumb = orig.resize((x,y),Image.ANTIALIAS)
    thumb.save(thumb_path, orig.format)
    return thumb_url
