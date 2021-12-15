import os
from PIL import ImageEnhance

index=[]

def listforindex():
    global index
    if len(index)==0:
        index.append(1)
        return index
    elif len(index)==1:
        index.append(2)
        return index
    elif len(index)==2:
        index.append(3)
        return index
    else:    
        index.append(index[2]+1)
        index.remove(index[0])
    return index


def deletefiles(path,i):
    '''
    if i<=3:
        return "You have less than 3 items in your directory!"
        '''
    files = os.listdir(path)
    files = sorted(files)#,key=lambda f: os.path.splitext(f))
    os.remove(f"./Revert/imgstate_{i}.jpg")
    return f"File imgstate_{i}.jpg deleted successfully"


def enh_contrast(image, level):
    enhancer = ImageEnhance.Contrast(image)
    img = enhancer.enhance(level)
    return img 
