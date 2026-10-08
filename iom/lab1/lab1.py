#%% 1a)
a = 10
b = '20'
c = 30.0
d = "40"

print(type(a), type(b), type(c), type(d))

#%% 1b)
sum1 = a + a
sum2 = b + d

print('sum1 = ', sum1)

#%% 1c)
a = [1, 3, 4, 6, 7]
b = a
print('a initial = ', a)
print('b initial = ', b)
b = b*3
print('a final = ', a)
print('b final = ', b)

#%% 1d)
b = a
print('a initial = ', a)
print('b initial = ', b)
for i in range(len(a)):
    b[i] = b[i]*3
print('a final = ', a)
print('b final = ', b)

#%% 1e)
b = a.copy()
print('a initial = ', a)
print('b initial = ', b)
for i in range(len(a)):
    b[i] = a[i]*3
print('a final = ', a)
print('b final = ', b)

#%% 1f)
import numpy as np
c = np.array(a)
d = c
print('c initial = ', c)
print('d initial = ', d)
d = 3*c
print('c final = ', c)
print('d final = ', d)

#%% 1g)
import numpy as np

a = [1, 3, 4, 6, 7]
print('a = ', a)
print('tip a = ', type(a))
print(type(a[0]))

c = np.array(a)
print('c = ', c)
print('tip c = ', type(c))
print(type(c[0]))

c1 = np.array(a, dtype = 'float')
print('c1 = ', c1)
print('tip c1 = ', type(c1))
print(type(c1[0]))

#%% 2a)
for i in range(0,4):
    print(i*3)
print('test')

#%% 2b)
for i in range(0,4):
    print(i*3)
    print('test')

#%% 4a)
import numpy as np
a2 = np.arange(0,255,50,dtype = 'uint8')
a2[0] = a2[0] - 10
a2[1] = a2[1] - 10
a2[3] = a2[3] + 30
a2[5] = a2[5] + 30
print('a2 = ', a2)

#%% 4b)
import numpy as np
a2 = np.arange(0,255,50,dtype = 'uint8')
a2 = a2.astype(float)
a2[0] = a2[0] - 10
a2[1] = a2[1] - 10
a2[3] = a2[3] + 30
a2[5] = a2[5] + 30
a2 = np.clip(a2,0,255)
a2 = a2.astype('uint8')
print('a2 = ', a2)

#%% 5)
def putere2(k):
    k1 = np.arange(1,k+1)
    rez1 = 2**k1
    return rez1

rez2 = putere2(4)
print('rez2 = ', rez2)

#%% 6)
X = np.array([[1,2,3,4],
              [5,6,7,8]])
X1 = np.array([np.arange(2,6), np.arange(6,10)])

print(X1.shape)
print(X1.size)
