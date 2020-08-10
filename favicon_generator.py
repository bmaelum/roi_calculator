
## https://stackoverflow.com/questions/45507/is-there-a-python-library-for-generating-ico-files

from PIL import Image
filename = r'/Users/bjornar/Documents/roi_calculator/static/dist/img/calcinvest_logo.png'
img = Image.open(filename)

icon_sizes = [(16,16), (32, 32), (48, 48), (64,64)]
img.save('/Users/bjornar/Documents/roi_calculator/static/dist/img/icon/logo.ico', sizes=icon_sizes)
