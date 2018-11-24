import numpy as np
import matplotlib.pyplot as plt


sizes = ['30x30','60x60','120x120','240x240','480x480']



times = [0.01, 0.02, 0.09, 0.37, 1]

plt.plot(sizes, times)
plt.title('Time per iteration vs Board Size')
plt.show()




