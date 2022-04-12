from scipy import ndimage
from pylinac import WinstonLutz
from pylinac.core.image_generator import (FilteredFieldLayer, AS1200Image, GaussianFilterLayer, generate_winstonlutz)
from pylinac.core.image_generator.layers import DepthDoseTrapezeLayer
from pylinac.core.image_generator.simulators import EBT3Image
from pylinac.core.image_generator.utils import generate_winstonlutz_vec
import numpy as np
from tifffile import TiffWriter
import matplotlib.pyplot as plt
from pydicom import dcmread
from PIL import Image

#comentari

def WL(left, up, angle):
    '''
    :param left: Desplaçament del feix cap a la dreta. (el programa desplaça la bola, no el feix)
    :param up: Desplaçament del feix cap a baix.
    :return: Llista de desplaçaments per cada angle
    '''

    vectors = []
    dir = "{}mm_left_{}mm_up".format(left, up).replace(".", "_")
    eixos = []
    for i in range(int(360 / angle)): #Segons l'angle que definim al programa principal, el codi ja generarà imatges necessàries per fer els 360º
        eixos.append((i * angle, 0, 0))
        generate_winstonlutz(simulator=AS1200Image(), field_layer=FilteredFieldLayer,
                             final_layers=[GaussianFilterLayer(3)],
                             dir_out='./WL_starshot/' + dir, field_size_mm=(30, 30), bb_size_mm=10,
                             offset_mm_left=left, offset_mm_up=up,
                             image_axes=eixos
                             )

    wl = WinstonLutz('D:/Física/4t/Pràctiques/Codis/Practiques/Starshot/WL_starshot/' + dir)
    wl.analyze()
    for i in range(int(360 / angle)):
        vectors.append(wl.images[i].cax2bb)
    return vectors #En aquest cas només ens interessen els desplaçaments que és el que utilitzarem per generar els starshots


def WL_vec(vectors):
    '''
    :param vectors: Llista de desplaçaments. Llista de 2 index; a les posicions [i][0] hi ha els desplaçaments respecte el pla xz
     i a les posicions [i][1] hi ha els desplaçaments de l'eix y
    :return: Imatges i anàlisi del Winston-Lutz creat amb els desplaçaments donats
    '''
    dir = "{}".format(vectors).replace(".", "_").replace("," , " ")

    generate_winstonlutz_vec(simulator=AS1200Image(), field_layer=FilteredFieldLayer,
                             final_layers=[GaussianFilterLayer(3)],
                             dir_out='./WL_starshot/'+dir,
                             displacements=vectors,
                             field_size_mm=(30, 30), bb_size_mm=10)

    wl = WinstonLutz('D:/Física/4t/Pràctiques/Codis/Practiques/Starshot/WL_starshot/'+dir)
    wl.analyze()
    wl.publish_pdf(dir+'.pdf')


def DoseToRGB(I):
    """
    :param I: Matriu d'intensitats
    :return: Imatge RGB
    """
    nrow = len(I)
    ncol = len(I[0])
    RGB = np.ones([nrow, ncol, 3], dtype=np.uint16)
    I=I/100
    I+=80
    I=I/100

    rA = 0.055
    rB = 1.819
    rC = -2.926

    gA = -0.087
    gB = 5.586
    gC = -7.678

    bA = -0.961
    bB = 87.348
    bC = -65.604

    RGB[:, :, 0] = ((rA + rB / (I - rC)) * 65535)
    RGB[:, :, 1] = ((gA + gB / (I - gC)) * 65535)
    RGB[:, :, 2] = ((bA + bB / (I - bC)) * 65535)

    return RGB


def circle_params(vec,angle):
    '''
    
    Parameters
    ----------
    vec : LIST
        List of each starshot line displacement.
    angle : INTEGER
        Angle between starshot lines.

    Returns
    -------
    Position of the center and radius of the minimum circle containing every point on the vec list.

    '''
    
    coord=[]

    for i in range(len(vec)):
        x=-np.cos(np.pi/180*angle*i)*vec[i]
        y=np.sin(np.pi/180*angle*i)*vec[i]
        coord.append((x,y))
        
    possible_radi=[]
    possible_centre=[]
    for i in range(len(vec)):
        for j in range(len(vec)):
            if i<j:
                for k in range(len(vec)):
                    if j<k:
                        pos, radi= circle(coord[i],coord[j],coord[k])
                        
                        if any(distancia(pos,i)>radi for i in coord): #if the distance between some point and the center is bigger than the radius we dont include the circle as that point will be outside the circle
                            continue
                        else:
                            possible_radi.append(radi)  
                            possible_centre.append(pos)
                    else: 
                        continue
            else: 
                continue
            
    r= min(possible_radi)
    centre=possible_centre[possible_radi.index(r)]
    
    return centre, r


def starshot(vectors, filename, gantry_sag):
    '''
    :param vectors: Llista de desplaçaments respecte el pla xz a cada angle
    :param filename: Nom del fitxer que contindrà la imatge
    :param gantry_sag: Valor del gantry sag
    :return: Imatge .tiff (amb canals RGB) que contindrà l'starshot amb caiguda de dosi i divergència del feix
    '''

    EBT3 = EBT3Image() #Inicialitzem el simulador

    #Aquest primer bucle permet que si introduïm una llista de desplaçaments amb dos índex (desplaçaments xz i desplaçaments y),
    #retorna només els desplaçaments en el pla xz. També canvia el signe dels desplaçaments ja que els que s'obtenen de l'anàlisi
    #del Winston-Lutz són els desplaçaments de la bola i no del feix.

    if type(vectors[0]) != list:
        des = [-i for i in vectors]
    else:
        temp = []
        for i in range(len(vectors)):
            temp.append(vectors[i][0])
            des = [-j for j in temp]

    #El codi està preparat perquè depenent de la mida de la llista de desplaçaments, ajusta l'angle entre feixos (els starshots
    # resultants sempre presentaran el mateix angle entre feixos i correspondrà a dividir 360 entre el nombre de feixos)

    iteracions = len(vectors)
    angle = int(360/iteracions)

    circle_params(vectors,angle)

    #Bucle que permet calcular els angles que haurà de rotar la imatge quan l'starshot presenti gantry sag

    angles_vec = [(angle*(i+1)+np.sin(np.pi/180*angle*i)*gantry_sag) for i in range(iteracions)]
    rotacions_vec = [angles_vec[i+1]-angles_vec[i] for i in range(iteracions-1)]
    rotacions_vec.append(360-sum(rotacions_vec))

    #El programa rota la imatge horàriament quan crea les línies i això fa que s'hagin de dibuixar primer les línies
    #que corresponen als angles més grans de manera que els índex de la llista de desplaçaments s'han de recorrer de l'últim
    #al primer, cosa que provoca una mica de lio amb els índex. Revisant el codi es podria fer que es dibuixessin amb
    #índex creixent i ho faria més entenedor. Tot i així, tal i com està actualment funciona :)

    for i in range(iteracions):
        EBT3.add_layer(DepthDoseTrapezeLayer((400, 5), alpha=0.5, cax_offset_mm=(0, des[i])))
        # Generem la línia amb un desplaçament corresponent al desplaçament del feix
        # En aquest cas DepthDoseTrapezeLayer es una capa que té en compte la caiguda de dosi i la divergència del feix.
        # Fàcilment es pot canviar per fer que enlloc de dibuixar trapezis dibuixi els altres tipus de capa canviant el
        # nom pel que correspondria (fitxer de layers.py)

        #Aquest if fa que un cop es dibuixa l'última línia, la imatge ja no es torni a rotar, ja que correspon a la línia
        #vertical de 0º.
        EBT3.image = ndimage.rotate(EBT3.image, rotacions_vec[i], reshape=False, mode='constant')

    EBT3.add_layer(GaussianFilterLayer(sigma_mm=2))  # Afegim una capa soroll
    EBT3 = EBT3.generate_image()
    RGB = DoseToRGB(EBT3) #Passem la imatge a RGB amb la calibració corresponent
    with TiffWriter('D:/Física/4t/Pràctiques/Codis/Practiques/Starshot/' + filename + '.tiff') as tif_w:
        tif_w.write(RGB,resolution=(72.,72.,"INCH"), extratags=(centre,))
    #Guardem la imatge amb el tag de resolució corresponent
    return


def starshot_dicom(vectors, filename):
    '''
    Mateixa funció que la funció starshot però en aquest cas enlloc de retornar un fitxer .tiff retorna un fitxer dicom (no està
    implementat el càlcul de gantry sag
    '''

    AS1200 = AS1200Image()
    if type(vectors[0]) != list:
        des = [-i for i in vectors]
    else:
        temp = []
        for i in range(len(vectors)):
            temp.append(vectors[i][0])
            des= [-j for j in temp]

    iteracions = len(vectors)
    angle = int(360/iteracions)
    for i in range(iteracions):
        AS1200.add_layer(DepthDoseTrapezeLayer((300, 5), alpha=0.5, cax_offset_mm=(0, des[-i - 1])))
        # Generem la línia amb un desplaçament corresponent al desplaçament del feix

        if i!=iteracions-1:
            AS1200.image = ndimage.rotate(AS1200.image, -angle, reshape=False, mode='constant')
            # Rotem la imatge -angle degut a que scipy rota antihoràriament

        else:
            continue

    AS1200.generate_dicom(file_out_name=filename + '.dcm')

    return
    
def circle(D,E,F):
    (x1,y1), (x2,y2), (x3,y3)= D, E, F
    
    A= x1*(y2-y3)-y1*(x2-x3)+x2*y3-x3*y2
    B=(x1**2+y1**2)*(y3-y2)+(x2**2+y2**2)*(y1-y3)+(x3**2+y3**2)*(y2-y1)
    C=(x1**2+y1**2)*(x2-x3)+(x2**2+y2**2)*(x3-x1)+(x3**2+y3**2)*(x1-x2)
    D=(x1**2+y1**2)*(x3*y2-x2*y3)+(x2**2+y2**2)*(x1*y3-x3*y1)+(x3**2+y3**2)*(x2*y1-x1*y2)
    
    x=-B/2/A
    y=-C/2/A
    r=((B**2+C**2-4*A*D)/(4*A**2))**0.5
    
    return (x,y), r   
    

def distancia(A,B):
    (x1,y1),(x2,y2) = A,B
    dis=((x2-x1)**2+(y2-y1)**2)**0.5
    
    return dis

    
    
    