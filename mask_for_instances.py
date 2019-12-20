#----------------------------------------------------------------
# Generating mask for instance segmentation
#
# Marks each box/polygon with a different colour from a specific colour cycle
#----------------------------------------------------------------

# Importing libraries

from bs4 import BeautifulSoup
from pathlib import Path
import numpy as np
import cv2 as cv
import matplotlib.cm

def create_mask(path_to_file):
    
    """
    Creates Distinct colour masks for annotated box/polygon in an image.

    Parameters:
    
        path_to_file (str): The path of xml file which is generated after annotating an image.

    """

    # Loading the xml file into the soup variable
    soup = BeautifulSoup(open(path_to_file), 'xml')
    
    # Converting path_to_file as pathlib variable
    path1=Path(path_to_file)

    # Choosing the colour map for colour cycle
    cmap = matplotlib.cm.get_cmap("hsv")

    # Searching for image tags in the xml file

    for i in soup.find_all('image'):
    
        # count of number of objects in a image ; To get equallly spaced colours from colour map
    
        count=len(i.find_all(['polygon','box']))
    
        # Getting "count" equally spaced numbers between 0 and 1
        interval=np.linspace(0,1,num=count)
        
        path2=Path(i.attrs['name'])
    
        # Reading the image from the folder path
        img = cv.imread(str(path1.parents[0]/path2))   
    
        # Variable to access the interval array
        interval_count=0
    
        # Traversing every polygon and box in a image

        for y in i.find_all(['polygon','box']):
            
            # List containing the contour points
            master_boundary = list()
        
            if (y.name=='polygon'):
        
                # Accessing boundary points of polygon
            
                boundary=y.attrs['points']
                master_boundary=boundary.rsplit(";")
                for i in range(len(master_boundary)):
                    master_boundary[i]=("".join(master_boundary[i]).rsplit(",")[:])
                    master_boundary[i] = list(map(float, master_boundary[i]))
                       
            else:
                # Accessing boundary points of box
                
                master_boundary.append([float(y.attrs['xtl']),float(y.attrs['ytl'])])
                master_boundary.append([float(y.attrs['xbr']),float(y.attrs['ytl'])])
                master_boundary.append([float(y.attrs['xbr']),float(y.attrs['ybr'])])
                master_boundary.append([float(y.attrs['xtl']),float(y.attrs['ybr'])])
                      
            # Selecting colour from colour map
            
            rgba=cmap(interval[interval_count],bytes=True)
            rgba = list(map(int, rgba))
            interval_count=interval_count+1
            
            # Dictionary containing the attributes of a box/polygon
            
            attr_dict=dict()
            
            for j in y.find_all('attribute'):
                
                attr_dict[j.attrs['name']]=j.text 
            
            # Merging attributes and label information of a box/polygon in a single dictionary
            
            attr_dict.update(y.attrs)
            
            # Mapping each box/label colour with their attributes and writing it into a file
            
            f1=open((Path(path1.parents[0],path2.with_suffix('.txt'))),'a')
            f1.write(f"{rgba} : {attr_dict} \n \n")
            f1.close()
                        
            # Drawing the boundary and filling them up with a colour
            cv.drawContours(img,[np.array(master_boundary,np.int64)],-1,rgba, -1)

            # Storing the generated image into a file        
            cv.imwrite(str(Path(path1.parents[0],path2)),img)
              
def pic_directory(path_to_file):
    
    """
    Creates Images with specified RGB values, Takes paths from XML file.

    Parameters:
    
        path_to_file (str): The path of xml file.

    """
    # loading the xml file into the soup variable
    
    soup = BeautifulSoup(open(path_to_file), 'xml')
    
    #Converting the path as Pathlib.path
    path=Path(path_to_file)
    
    # Traversing through image tags
    
    for i in soup.find_all('image'):
        
        path1=Path(i.attrs['name'])
        path2=Path(path.parents[0],path1.parents[0])
        
        # Creating directory to store images
        path2.mkdir(parents=True,exist_ok=True)
        
        # Creating Black images and storing them with the image name
        im = np.zeros((int(i.attrs['height']),int(i.attrs['width']),3),dtype=np.uint8)
        cv.imwrite(str(Path(path2,path1.name)),im)

