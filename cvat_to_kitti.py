#------------------------------------------------------------------------------------------------------------------
#
# cvat-xml to kitti_with_attributes and kitti 
# 
# converts a cvat xml file into kitti and kitti_with_attributes where kitti_with_attributes stores attributes other than labels in kitti 
#
# Creates a label_map text file which maps the label name in kitti to label name in kitti_with_attributes
#
# Creates a text file which contains a list of distinct label names in kitti and kitti_with_attributes file.
#
# Reads only 3 kitti labels [ label_name, Occlusion, bounding_box_coordinates]; other labels are hardcoded as 0.00
#
# Reads only box label not polygon,line.
#
# Applicable for CVAT annotations XML v1.1
#
# Reads XML files from a folder and creates 2 folders kitti_with_attributes files and kitti files in the same directory containing the files with their same name.
# and 3 files for label map, distinct kitti labels and distinct kitti with attributes label
#
#------------------------------------------------------------------------------------------------------------------


#Importing BeautifulSoup for parsing operations and os for file operations

from bs4 import BeautifulSoup
import os

# path_to_dir is the path of folder containing the xml file
# Separator variable to separate attribute values in kitti_with_attributes file

def cvat_xml_to_kitti(path_to_dir,attribute_separator = "*"):
    

    # Getting the Required file paths 

    entries = os.listdir(path_to_dir)
    create_dir=os.path.dirname(path_to_dir)

    # Creating required folders

    path_to_kitti_with_attributes = create_dir+"/"+"kitti_with_attributes_files"
    path_to_kitti=create_dir+"/"+"kitti_files"

    os.mkdir(path_to_kitti_with_attributes)
    os.mkdir(path_to_kitti)

    # List to maintain distinct labels of kitti and kitti_with_attributes

    kitti_distinct_label=list()
    kitti_with_attributes_distinct_label=list()

    path_to_xml=path_to_dir+"/"+entries[0]
    
    # Loading the file on to the variable

    soup = BeautifulSoup(open(path_to_xml), 'xml')

    # List containing the kitti_with_attributes details

    kitti_labels_list=list()

    path_to_kitti_with_attributes_file=str()

    # Dictionary to store all the extra attributes other than the kitti labels

    kitti_with_attributes_labels = []

    # flag variable to print description on the label_map file

    flag1=True


    # Collecting all extra attributes present in the file and storing in kitti_with_attributes_labels

    for i in soup.find_all('box'):
        for y in i.find_all('attribute'):
            if y.attrs['name'] not in kitti_with_attributes_labels:
                kitti_with_attributes_labels.append(y.attrs['name'])
                        
    # Looping through all tags named box in xml file

    for i in soup.find_all('box'):
            
        # Dictionary to store extra attributes of the current box
    
        kitti_with_attributes_dict={}
    
        # Storing the kitti values into the list and generating distinct labels list
        
        if i.attrs['label'] not in kitti_distinct_label:
            
            kitti_distinct_label.append(i.attrs['label'])
    
        kitti_labels_list=[i.attrs["label"],"0.00", i.attrs["occluded"], "0.00", i.attrs["xtl"], i.attrs["ytl"], i.attrs["xbr"], i.attrs["ybr"], "0.00", "0.00", "0.00", "0.00", "0.00", "0.00", "0.00"]

        # Looping through the attribute subtag in a box tag
    
        for y in i.find_all('attribute'):
        
            kitti_with_attributes_dict[y.attrs['name']]=y.text
        
        # Setting the Non-present attribute's value to 0.00
    
        for x in kitti_with_attributes_labels:
    
            if x not in kitti_with_attributes_dict.keys():
        
                kitti_with_attributes_dict[x]='NaN'
            
        # Appending the extra labels to list k 
    
        for x in kitti_with_attributes_labels:
        
            kitti_labels_list.append("'%s'" % kitti_with_attributes_dict[x])
            
        kitti_format=" ".join(kitti_labels_list[0:15])
                
        for x in kitti_with_attributes_labels:
            
            kitti_labels_list[0]=kitti_with_attributes_dict[x]+attribute_separator+kitti_labels_list[0]

            
        # converting the list into Kitti and kitti_with_attributes format
    
        if kitti_labels_list[0] not in kitti_with_attributes_distinct_label:
        
            kitti_with_attributes_distinct_label.append(kitti_labels_list[0])
        
    
        kitti_with_attributes=" ".join(kitti_labels_list[0:15])
        
        
        # Getting file names
        
        image_name=os.path.splitext(i.parent.attrs['name'])[0]
    
        l=os.path.basename(image_name)
    
        flag=path_to_kitti_with_attributes_file
    
        path_to_kitti_with_attributes_file=path_to_kitti_with_attributes+"/"+l+".txt"
    
        path_to_kitti_file=path_to_kitti+"/"+l+".txt"
    
        path_to_label_map_file=create_dir+'/'+'label_map.txt'
            
        
    
        # Creating the files; Flag variable used to do the below operations only once 
        
        if(flag!=path_to_kitti_with_attributes_file):
        
            f = open(path_to_kitti_with_attributes_file, "a")
            f.write("------------------------------------------------------------------------------------")
            f.write("\n")
            f.write("Note:")
            f.write("\n")
            f.write("kitti_with_attributes extra labels - %s" % kitti_with_attributes_labels[::-1])
            f.write("\n")        
            f.write("NaN in the extra labels means the label is not present.")
            f.write("\n")
            f.write("Blank fields means the label is present and the value is left blank")
            f.write("\n")
            f.write("------------------------------------------------------------------------------------")
            f.write("\n")
            f.close()
        
        if(flag1):
        
            f2= open(path_to_label_map_file,"a")
            f2.write("------------------------------------------------------------------------------------")
            f2.write("\n")
            f2.write("Note:")
            f2.write("\n")
            f2.write("kitti_with_attributes extra labels - %s" % kitti_with_attributes_labels[::-1])
            f2.write("\n")        
            f2.write("NaN in the extra labels means the label is not present.")
            f2.write("\n")
            f2.write("Blank fields means the label is present and the value is left blank")
            f2.write("\n")
            f2.write("kitti label class name : kitti_with_attributes label class name")
            f2.write("\n")
            f2.write("------------------------------------------------------------------------------------")
            f2.write("\n")
            f2.close()
            flag1=False

    
        # writing data into respective files
        
        f = open(path_to_kitti_with_attributes_file, "a")
        f1= open(path_to_kitti_file, "a")
        f2= open(path_to_label_map_file,"a")
        f.write("\n")
        f.write(kitti_with_attributes)
        f.close()
        f1.write(kitti_format)
        f1.write("\n")
        f1.close()
        f2.write(kitti_format.split(' ', 1)[0])
        f2.write(" : ")
        f2.write(kitti_with_attributes.split(' ', 1)[0])
        f2.write('\n')
        f2.close()

    path_to_kitti_distinct_label_file=create_dir+'/'+'kitti_distinct_label.txt'
    f3= open(path_to_kitti_distinct_label_file,"a")
    f3.write(str(kitti_distinct_label))
    f3.close()

    path_to_kitti_with_attributes_distinct_label_file=create_dir+'/'+'kitti_with_attributes_distinct_label.txt'
    f4= open(path_to_kitti_with_attributes_distinct_label_file,"a")
    f4.write(str(kitti_with_attributes_distinct_label))
    f4.close()


###___END___###



