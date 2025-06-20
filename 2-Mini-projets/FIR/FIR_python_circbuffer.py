import random
import math
import numpy as npy

import matplotlib.pyplot as plt

class CircularBuffer:
    def __init__(self, data):
        self.items = data   # call the samples setter
                    
    @property
    def items(self):
        ix = npy.arange(self.__pointer, self.__pointer + self.__NbItems) % self.__NbItems
        return self.__items[ix]

    @items.setter
    def items(self, x):
        print('items.setter')
        if not hasattr(x, '__iter__'):
            self.__NbItems = x
            self.__items = npy.zeros((x, ), dtype=npy.float64)
        else:
            self.__items = npy.asarray(x, dtype=npy.float64)
            self.__NbItems  = self.__items.shape[0]
        self.__pointer = 0
        
    @property
    def pointer(self):
        return self.__pointer
    
    @pointer.setter
    def pointer(self, x):
        self.__pointer = x
        
    def roll(self, k=1):
        self.pointer += k
        self.pointer %= self.__NbItems
        
    def update(self, s):
        """ insert new sample after current pointer location
        """
        self.roll()
        self.__items[self.__pointer] = s
   
    def __getitem__(self, ix):
        """index relative to current value of pointer
        """
        pointer = (self.pointer + ix) % self.__NbItems
        return self.__items[pointer]
    
class FIR_filter:
    def __init__(self, data):
        self.__buffer = CircularBuffer(data)
        self.weights  = data

    @property
    def NbSamples(self):
        return self.__NbSamples
    
    @property
    def weights(self):
        return self.__weights[::-1]
    
    @weights.setter
    def weights(self, x):
        print('setter')
        if hasattr(x, '__iter__'):
#            self.__weights = npy.asarray(x[::-1], dtype=npy.float) # NE MARCHE PAS EXPLIQUER POURQUOI
            self.__weights = npy.array(x[::-1], dtype=npy.float64)
            self.__NbSamples = self.__weights.shape[0]
        else:
            self.__weights = npy.ones((x, ), dtype=npy.float64) / x
            self.__NbSamples = x
        
    def __call__(self, x):   # implements function call operator.
        self.__buffer.update(x)
        return (self.weights * self.__buffer.items).sum()
#        return (self.__weights[::-1] * self.__buffer.items[-self.__NbSamples:]).sum() # equivalent
    
if __name__ == "__main__":
#    fir = FIR_filter(10)
    weights=npy.array([1/(x+1) for x in range(16)])   
#    weights=npy.ones((16, ))  
    weights /= weights.sum()
#    weights = npy.zeros_like(weights)
#    weights[0]=1
#    print(weights)
    
    fir = FIR_filter(weights)
    print(fir.weights)
    print('------------')
    r=random.seed(1452)

    sf=fir(1)
    print(sf)
    sf=fir(1)
    print(sf)
    sf=fir(1)
    print(sf)   
    
    raw_data=[]
    fir_data=[]
    time =[]
    
    NT=2000
    T =100 # period
    dt=0.5    # time step
    for nt in range(NT):
        t = nt*dt
        r=random.uniform(-1., 1.)
        s=math.sin(2*math.pi/T*t)+r
        sf=fir(s)
        time.append(t)
        raw_data.append(s)
        fir_data.append(sf)

    plt.figure()
    plt.plot(time, raw_data, 'r-')
    plt.plot(time, fir_data, 'b-')
    plt.draw()
    plt.legend(('raw', 'fir'), loc='upper right')

