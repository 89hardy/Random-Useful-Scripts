import PIL
from PIL import Image
import glob

baseheight = 50

types = ('*.jpg', '*.png') # the tuple of file types
files_grabbed = []
for files in types:
    files_grabbed.extend(glob.glob(files))

for img_name in files_grabbed:
    img = Image.open(img_name)
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)

    img.save('compressed_' + img_name, optimize=True)




#For GIFs
glob_img = glob.glob('*.gif')

for img_name in glob_img:
    img = Image.open(img_name)
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    img.save('compressed_' + img_name)