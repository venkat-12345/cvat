# To generate a text file containing image path from a cvat xml file

def get_image_path(path_to_xml):
    
    """
    Creates a text file containing the image path of images present in a cvat xml file.

    Parameters:
    
        path_to_xml (str): The path of xml file.

    """
    
    from bs4 import BeautifulSoup
    from pathlib import Path
    
    soup = BeautifulSoup(open(path_to_xml), 'xml')

    path=Path(path_to_xml)
    path_to_img_file=Path((path.parent),'image_path.txt')
    
    for i in soup.find_all('image'):
        
        f1=open(path_to_img_file,'a')
        f1.write(i.attrs['name'])
        f1.write('\n')
        f1.close()
    
    
