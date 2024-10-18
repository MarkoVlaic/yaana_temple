import math
pi = math.pi

'''
def normalize(x,y,alpha):
    return x/20, y/20, alpha/pi

def denormalize(x,y,alpha):
    return x*20, y*20, alpha*pi
'''

def normalize(l):
    for j in range(len(l)):
        for i in range(len(l[j])):
            l[j][i] = list(l[j][i])
            l[j][i][0] /= 20
            l[j][i][1] /= 20
            l[j][i][2] /= pi
            l[j][i][3] /= 20
            l[j][i] = tuple(l[j][i])

    return l

def denormalize(l):
    for j in range(len(l)):
        for i in range(len(l[j])):
            l[j][i] = list(l[j][i])
            l[j][i][0] *= 20
            l[j][i][1] *= 20
            l[j][i][2] *= pi
            l[j][i][3] *= 20
            l[j][i] = tuple(l[j][i])

    return l