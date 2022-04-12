
from exif import Image

with open('D:/Física/4t/Pràctiques/Codis/Starshot/imatges_analisi/0mm_left_0_0mm_up_0gantry_sag_Starshot.tiff','rb') as image_file:
     my_image = Image(image_file)

print(my_image.has_exif)














def parts_codi():
    '''
    for i in range(len(r_feix)):
    theta = 72 * i *np.pi / 180

    x= r_feix[i]*np.cos(theta)
    y= -r_feix[i]*np.sin(theta)

    x_i = np.cos(theta) * x - np.sin(theta) * y
    y_i = np.sin(theta) * x + np.cos(theta) * y
    #print(x,y)
    #print(x_i, y_i)

def DoseToRGB2(in_matrix):
    nrow= len(in_matrix)
    ncol=len(in_matrix[0])
    out_matrix=np.zeros([nrow, ncol, 3], dtype=np.uint16)

    rA= 9*10**-10
    rB= -2*10**-6
    rC= 0.0014
    rD= 0.0093

    gA = 2*10**-10
    gB = -5*10**-10
    gC = 0.0007
    gD= 0.0012

    bA = 1*10**-10
    bB = -2*10**-7
    bC = 0.0003
    bD= 0.0003
    out_matrix[:,:,0]= (rA*in_matrix**3+rB*in_matrix**2+rC*in_matrix+rD)
    out_matrix[:,:,1]= (gA*in_matrix**3+gB*in_matrix**2+gC*in_matrix+gD)
    out_matrix[:,:,2]= (bA*in_matrix**3+bB*in_matrix**2+bC*in_matrix+bD)



    def DepthDose(mx, pix_size):
    """Returns a Percentage Depth Dose function"""
    m_1 = -0.0029778
    n_1 = 1.97194
    m_2 = -0.003299
    n_2 = 1.2526
    b_1 = -1.3961 * 10 ** -5
    a_1 = 0.0067773
    b_2 = 0.24634
    a_2 = 5.56
    S = 98

    x=[]
    y=[]

    for i in range(len(mx)):
        x.append( mx[i] / pix_size[0])
        y.append((m_1 * S + n_1) * np.exp(-(b_1 * S + a_1) * x[i]) - (m_2 * S + n_2) * np.exp(-(a_2 / S ** 2 + b_2) * x[i]))

    return y









#as1200 = AS1200Image()
#1
#as1200.add_layer(FilteredFieldLayer((5, 270), alpha=0.5, cax_offset_mm=(-100, 0)))
#primer offset corresponent a la y; si és positiu, anirà cap avall i viceversa.
#segon offset corresponent a la x; si és positiu anirà a la dreta i viceversa

as1200 = AS1200Image()
as1200.add_layer(DepthDoseTrapezeLayer((270, 10), alpha=0.5, cax_offset_mm=(0, 0)))
#as1200.add_layer(GaussianFilterLayer(sigma_mm=3))
#as1200.generate_dicom(file_out_name= "prova")

ds=dcmread("prova")
#plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
#plt.savefig("imatge_exemple.png", format="png", dpi=1000)

plt.show()

as500 = AS500Image()
as500.add_layer(DepthDoseTrapezeLayer((270, 10), alpha=0.5, cax_offset_mm=(0, 0)))
#as1200.add_layer(GaussianFilterLayer(sigma_mm=3))
as500.generate_dicom(file_out_name= "prova")

ds=dcmread("prova")
plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
plt.savefig("imatge_exemple.png", format="png", dpi=1000)

#plt.show()


for _ in range(6):
    as1200.add_layer(FilteredFieldLayer((270, 5), alpha=0.5))
    as1200.image = ndimage.rotate(as1200.image, 30, reshape=False, mode='nearest')
as1200.add_layer(GaussianFilterLayer(sigma_mm=0))
as1200.generate_dicom(file_out_name=star_path)
as1200= as1200.generate_image()
#RGB=DoseToRGB(as1200)
tiff.imsave(star_path2, as1200)

f, axarr = plt.subplots(1,2)
ds=dcmread(star_path)
image= imread(star_path2)
axarr[0].imshow(ds.pixel_array, cmap=plt.cm.gray)
axarr[1].imshow(image, cmap=plt.cm.gray)
plt.show()

# analyze it
star = pylinac.Starshot(star_path)
star.analyze()
print(star.results())
star.plot_analyzed_image()

star= pylinac.Starshot(star_path2, sid=1000)
star.analyze()
print(star.results())
star.plot_analyzed_image()
   '''