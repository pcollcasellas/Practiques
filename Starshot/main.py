from funcions import starshot, WL_vec, WL, starshot_dicom, circle_param, distancia, circle
import numpy as np
#Si tens el fitxer funcions i el fitxer main al mateix directori, pots importar les funcions d'un fitxer a l'altre i així el codi
#de main queda més net.

#Exemple d'starshot amb els desplaçaments desitjats
vec=[0.2,0.4,-0.3,0.5,1]
filename= "[0_5 0_5 0_5 0_5 0_5]".format()
starshot(vec, filename, 3)

angle=72

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
                    
                    if any(distancia(pos,i)>radi for i in coord):
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
print(r,centre)
