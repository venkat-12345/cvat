# import statements

from bs4 import BeautifulSoup
from pathlib import Path

class xml_to_kitti:

  """ 
  Class for converting data into KITTI format from annotated cvat-xml format.
    
    Parameters
    -----------
    path_to_xml_file:
      Path of the cvat-xml file.

    attribute_separator:
      Character to separate attributes and label name in KITTI file.

  """
  def __init__(self,path_to_xml_file,attribute_separator='*'):
    
    # converting the file path into a pathlib path variable and storinng the folder location
    path1=Path(path_to_xml_file)
    self.path_to_folder=Path(path1.parents[0])
            
    # Generating the soup variable 
    self.soup = BeautifulSoup(open(path_to_xml_file), 'xml')

    self.attribute_separator=attribute_separator


  def write_specific_labels_with_attributes(self,specific_label_list=dict()):
    
    """
    Reads a xml file and creates a folder containing text files (<image_name>.txt) containing data in kitti format.
    
    Specified labels with specified attributes are only written in the file.
    
    Parameters:
    
        specific_label_list (dictionary) : Dictionary containing required labels as key and corresponding attribute list as values.
        
        Ex: specific_label_list={'Helmet':['colour'],'Suit':['reflective'],'Missing_PPE':['Sleeping_Person','type']}


    """   
    
    # case : incorrect datatype passed
    
    if(type(specific_label_list)!=dict):
        raise Exception('Incorrect Datatype : Specific_label_list is not a dictionary')
        return
    

    # creating a folder for the files

    path_to_specific_label_folder=Path(self.path_to_folder,'specific_labels')
    path_to_specific_label_folder.mkdir(exist_ok = True)

    
    # Case : Empty dictionary is passed ; Writes labels with all attributes
    if(len(specific_label_list)==0):

      raise Exception("Required labels not specified : Empty dictionary passed")
      return

    # Case : Mentioned labels and attributes are picked and written on to the file
    else:
        
        # Finding all tags named as 'box'
        for i in self.soup.find_all('box'):


            img_path=Path(i.parent.attrs['name'])
            image_name=img_path.stem
            path_to_specific_label_file=Path(path_to_specific_label_folder, image_name+'.txt')

            f1= open(path_to_specific_label_file,"a")
        
            modified_label=list()
        
            if i.attrs['label'] in specific_label_list.keys():
        
                for j in i.find_all('attribute'):
                
                    for k in specific_label_list[i.attrs['label']]:
                
                        if j.attrs['name'] == k:
                    
                            modified_label.append(j.text)
        
                modified_label.append(i.attrs['label'])
            
                f1.write(f"{self.attribute_separator.join(modified_label)} 0.00 {i.attrs['occluded']} 0.00 {i.attrs['xtl']} {i.attrs['ytl']} {i.attrs['xbr']} {i.attrs['ybr']} 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n")
            
            f1.close()

  def write_kitti_with_attributes(self):
    
    """
    Reads a xml file and creates a folder containing text files (<image_name>.txt) containing data in kitti format with all its attribute data appended to the label name.

    """ 

    # Initialising a empty list to collect all distinct attributes
    distinct_labels=list()

    path_to_kitti_with_attributes_folder=Path(self.path_to_folder,'kitti_with_attributes')
    path_to_kitti_with_attributes_folder.mkdir(exist_ok = True)


    for i in self.soup.find_all('box'):

      for y in i.find_all('attribute'):
    
        # Traversing through every attributes and appending unique attributes
        
        if y.attrs['name'] not in distinct_labels:
                
          distinct_labels.append(y.attrs['name'])


    path_to_template_file=Path(path_to_kitti_with_attributes_folder,'template_file.txt')
    f2=open(path_to_template_file,'a')
    f2.write("Kitti files have the following attribute's text appended with their label\n")
    f2.write(f"{distinct_labels}\n\n")

    for i in self.soup.find_all('box'):
    
      attribute_label_dict=dict()
      modified_label=list()

      img_path=Path(i.parent.attrs['name'])
      image_name=img_path.stem
      path_to_kitti_with_attributes_file=Path(path_to_kitti_with_attributes_folder, image_name+'.txt')

      f1= open(path_to_kitti_with_attributes_file,"a")
    
      for j in i.find_all('attribute'):
            
        # Dictionary storing attribute along with their text
          attribute_label_dict[j.attrs['name']]=j.text
    
      for x in distinct_labels:
            
        # Adding missing attributes from distinct_labels to the dictionary and setting value as NaN 
        if x not in attribute_label_dict.keys():
        
          attribute_label_dict[x]='NaN'
            
      for y in distinct_labels:
            
          modified_label.append(attribute_label_dict[y])
    
      modified_label.append(i.attrs['label'])
            
      f1.write(f"{self.attribute_separator.join(modified_label)} 0.00 {i.attrs['occluded']} 0.00 {i.attrs['xtl']} {i.attrs['ytl']} {i.attrs['xbr']} {i.attrs['ybr']} 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n")

      f1.close()

    # just read the xml and create normal kitti file

  def write_kitti_without_attributes(self):


    """
    Reads a xml file and creates a folder containing text files (<image_name>.txt) containing annotated data in kitti format.

    """

    path_to_kitti_files_folder=Path(self.path_to_folder,'kitti_files')
    path_to_kitti_files_folder.mkdir(exist_ok = True)

    for i in self.soup.find_all('box'):

      img_path=Path(i.parent.attrs['name'])
      image_name=img_path.stem
      path_to_kitti_file=Path(path_to_kitti_files_folder, image_name+'.txt')

      f1=open(path_to_kitti_file,'a')

      f1.write(f"{i.attrs['label']} 0.00 {i.attrs['occluded']} 0.00 {i.attrs['xtl']} {i.attrs['ytl']} {i.attrs['xbr']} {i.attrs['ybr']} 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n")

    f1.close()



# Testing //**//**//**//**/*/*/*/*/*/*/*

path_to_xml='/home/murthylogeshwar/Desktop/padipu/detect/test/PPE - BPCL Mumbai Jul 2019 TPulse vids - Day 7-12.xml'

k=xml_to_kitti(path_to_xml)
k.write_kitti_with_attributes()
k.write_kitti_without_attributes()

specific_label_list={'Helmet':['colour'],'Suit':['reflective'],'Missing_PPE':['Sleeping_Person','type']}
k.write_specific_labels_with_attributes(specific_label_list)


#specific_label_list=dict()
#k.write_specific_labels_with_attributes(specific_label_list)

#specific_label_list=4
#k.write_specific_labels_with_attributes(specific_label_list)