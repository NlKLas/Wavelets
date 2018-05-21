import PIL
import numpy as np
import matplotlib.pyplot as plt
from images import NonstandardSynthesis, NonstandardDecomposition

pluto = np.asarray(PIL.Image.open('Pluto1k.png').convert('RGB'))
pluto = np.array(np.rollaxis(pluto.copy(),2), dtype=float)
#pluto[2048:]=np.array(2048*[4096*[[0, 0, 0, 255]]], dtype=np.uint8)
#pluto = np.array([[3*[round(pluto[i][j])] for j in range(len(pluto[i]))] for i in range(len(pluto))], dtype=np.uint8)
#pluto = np.mean(pluto, axis=2)

for i in range(3):
    plt.imshow(pluto[i], cmap=['Reds', 'Greens', 'Blues'][i])
    plt.show()
    pluto[i] = NonstandardDecomposition(pluto[i])
    #print(pluto)
    n = 2
    #pluto[i] = np.array([[pluto[i][j][k] if j<n**2/1024 else 0 for k in range(len(pluto[i][j]))] for j in range(len(pluto[i]))])
    pluto[i] = np.array([[pluto[i][j][k] if j<n and k<n else 0 for k in range(len(pluto[i][j]))] for j in range(len(pluto[i]))])
    pluto[i] = NonstandardSynthesis(pluto[i])
    plt.imshow(pluto[i], cmap=['Reds', 'Greens', 'Blues'][i])
    plt.show()

#print(pluto, np.shape(pluto))

pluto = np.array(np.rollaxis(pluto, 0, 3), dtype=np.uint8)
#print(pluto, np.shape(pluto))
plt.imshow(pluto)
plt.show()

j = PIL.Image.fromarray(pluto)
j.save("Pluto%d.png"%n)