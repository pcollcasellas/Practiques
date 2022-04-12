from scipy import ndimage
from pylinac import WinstonLutz
from pylinac.core.image_generator import (FilteredFieldLayer, AS1200Image, GaussianFilterLayer, generate_winstonlutz)
from pydicom import dcmread
import matplotlib.pyplot as plt

angle= 72





star_path = 'offset_starshot.dcm'
as1200 = AS1200Image()
#1
as1200.add_layer(FilteredFieldLayer((270, 5), alpha=0.5, cax_offset_mm=(0, 6.8)))

as1200.image = ndimage.rotate(as1200.image, -angle , reshape=False, mode='nearest')
#2
as1200.add_layer(FilteredFieldLayer((270, 5), alpha=0.5, cax_offset_mm=(0, 0)))
as1200.image = ndimage.rotate(as1200.image, -angle, reshape=False, mode='nearest')
#3
as1200.add_layer(FilteredFieldLayer((270, 5), alpha=0.5, cax_offset_mm=(0, -6.8)))
as1200.image = ndimage.rotate(as1200.image, -angle, reshape=False, mode='nearest')
#4
as1200.add_layer(FilteredFieldLayer((270, 5), alpha=0.5, cax_offset_mm=(0, -10)))
#as1200.image = ndimage.rotate(as1200.image, -angle, reshape=False, mode='nearest')



as1200.add_layer(GaussianFilterLayer(sigma_mm=3))
as1200.generate_dicom(file_out_name=star_path)

#filename= "D:/Física/4t/Pràctiques/Codis/Starshot/" + star_path
#ds=dcmread(filename)

#plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
#plt.show()

#star = pylinac.Starshot(star_path)
#star.analyze()
#print(star.results())
#star.plot_analyzed_image()
#star.publish_pdf('mystar.pdf')
