# class to convert cvat-xml file containing annotations into KITTI format


# import statements

from bs4 import BeautifulSoup
from pathlib import Path

class cvat_xml_to_kitti:

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
    
    """
    Converting the file path into a pathlib path variable and storing the folder location.

    """

    path1=Path(path_to_xml_file)
    self.path_to_folder=Path(path1.parents[0])
            
    # Generating the soup variable 
    self.soup = BeautifulSoup(open(path_to_xml_file), 'xml')

    # Assigning the separating charachter between two entries
    self.attribute_separator=attribute_separator


  def create_folder(self,folder_name):

    """
    Function to create a folder in the same directory as the cvat-xml file and returns the path of the created folder.

    Parameters
    -----------

    folder_name:
      
      Name of the folder to be created.
    
    """

    Path(self.path_to_folder,folder_name).mkdir(exist_ok = True)
    return Path(self.path_to_folder,folder_name)


  def write_specific_labels_with_attributes(self,specific_label_list=dict()):
    
    """
    Reads a xml file and creates a folder containing text files (<image_name>.txt) containing data in kitti format.
    
    Specified labels with specified attributes are only written in the file.
    
    Parameters:
    
        specific_label_list (dictionary) : Dictionary containing required labels as key and corresponding attribute list as values.
        
        Ex: specific_label_list={'Helmet':['colour'],'Suit':['reflective'],'Missing_PPE':['Sleeping_Person','type']}


    """   
    
    # case : incorrect datatype passed ; Raises an error
    
    if(type(specific_label_list)!=dict):

      raise Exception('Incorrect Datatype : Specific_label_list is not a dictionary')
      return

    # Case : Empty dictionary is passed ; Writes labels with all attributes.

    if(len(specific_label_list)==0):

      self.write_kitti_with_attributes()
      return


    # creating a folder for the files

    path_to_specific_labels_folder=self.create_folder('specific_labels')

    # Finding all tags named as 'box'
    for i in self.soup.find_all('box'):

        # Reading the image name from the file and creating all the parent directories in the image name and creating a path with the image name with a .txt extension for writing the kitti files 

        img_path=Path(path_to_specific_labels_folder,i.parent.attrs['name'])
        path_to_specific_label_file=img_path.with_suffix(".txt")
        path_to_specific_label_file.parent.mkdir(parents=True, exist_ok=True)


        # Mentioned labels and attributes are picked and written on to the file

        modified_label=list()

        if i.attrs['label'] in specific_label_list.keys():
                  
            for j in i.find_all('attribute'):

                for k in specific_label_list[i.attrs['label']]:

                    if j.attrs['name'] == k:

                        modified_label.append(j.text)

            modified_label.append(i.attrs['label'])
                  
            with open(path_to_specific_label_file,"a") as f1:

              f1.write(f"{self.attribute_separator.join(modified_label)} 0.00 {i.attrs['occluded']} 0.00 {i.attrs['xtl']} {i.attrs['ytl']} {i.attrs['xbr']} {i.attrs['ybr']} 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n")
            

  def write_kitti_with_attributes(self):
    
    """
    Reads a xml file and creates a folder containing text files (<image_name>.txt) containing data in kitti format with all its attribute data appended to the label name.

    """ 

    # Initialising a empty list to collect all distinct attributes
    distinct_labels=list()

    path_to_kitti_with_attributes_folder=self.create_folder('kitti_with_attributes')


    for i in self.soup.find_all('box'):

      for y in i.find_all('attribute'):
    
        # Traversing through every attributes and appending unique attributes
        
        if y.attrs['name'] not in distinct_labels:
                
          distinct_labels.append(y.attrs['name'])

    # Writing a template_file with the header label names

    path_to_template_file=Path(path_to_kitti_with_attributes_folder,'template_file.txt')

    with open(path_to_template_file,'a') as f2:

      f2.write("Kitti files have the following attribute's text appended with their label\n")
      f2.write(f"{distinct_labels}\n\n")

    for i in self.soup.find_all('box'):
    
      attribute_label_dict=dict()
      modified_label=list()

      # Reading the image name from the file and creating all the parent directories in the image name and creating a path with the image name with a .txt extension for writing the kitti files 

      img_path=Path(path_to_kitti_with_attributes_folder,i.parent.attrs['name'])
      path_to_kitti_with_attributes_file=img_path.with_suffix(".txt")
      path_to_kitti_with_attributes_file.parent.mkdir(parents=True, exist_ok=True)

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

      with open(path_to_kitti_with_attributes_file,'a') as f1:
            
        f1.write(f"{self.attribute_separator.join(modified_label)} 0.00 {i.attrs['occluded']} 0.00 {i.attrs['xtl']} {i.attrs['ytl']} {i.attrs['xbr']} {i.attrs['ybr']} 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n")


    # just read the xml and create normal kitti file

  def write_kitti_without_attributes(self):

    """
    Reads a xml file and creates a folder containing text files (<image_name>.txt) containing annotated data in kitti format.

    """

    path_to_kitti_files_folder=self.create_folder('kitti_files')

    for i in self.soup.find_all('box'):

      # Reading the image name from the file and creating all the parent directories in the image name and creating a path with the image name with a .txt extension for writing the kitti files 
      img_path=Path(path_to_kitti_files_folder,i.parent.attrs['name'])
      path_to_kitti_file=img_path.with_suffix(".txt")
      path_to_kitti_file.parent.mkdir(parents=True, exist_ok=True)

      with open(path_to_kitti_file,'a') as f1:

        f1.write(f"{i.attrs['label']} 0.00 {i.attrs['occluded']} 0.00 {i.attrs['xtl']} {i.attrs['ytl']} {i.attrs['xbr']} {i.attrs['ybr']} 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n")
