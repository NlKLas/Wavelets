import PIL
import numpy as np
import matplotlib.pyplot as plt
from images import NonstandardSynthesis, NonstandardDecomposition


#lena = np.asarray(PIL.Image.open('mona.jpg'))
#lena = np.mean(lena, axis=2)
#print(lena)
#lena = np.random.randint(0, 256, (256,256))
lena = 32*np.ones((256,256))
lena[0][0] += 256*63.5
lena = NonstandardSynthesis(lena)
lena = np.array([[3*[round(lena[i][j])] for j in range(len(lena[i]))] for i in range(len(lena))], dtype=np.uint8)
#lena = np.mean(lena, axis=2)
#lena = NonstandardDecomposition(lena)

plt.imshow(lena, cmap='gray')
plt.show()

j = PIL.Image.fromarray(lena)
j.save("worstCase.jpg")