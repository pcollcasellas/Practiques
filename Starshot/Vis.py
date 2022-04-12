import matplotlib.pyplot as plt
from pydicom import dcmread
from pylinac import Starshot
filename=input("Digues el nom del fitxer: ")
directori= "D:/Física/4t/Pràctiques/Codis/Starshot/" + filename
ds=dcmread(directori)
plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
plt.show()

star = Starshot(filename)
star.analyze()
print(star.results())
star.plot_analyzed_image()

star= Starshot('0_0mm_left_0_0mm_up_Starshot.tiff', sid=1000, dpi=72)
star.analyze()
print(star.results())
star.plot_analyzed_image()