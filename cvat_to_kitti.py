#------------------------------------------------------------------------------------------------------------------
#
# cvat-xml to master kitti and kitti
# 
# converts a cvat xml file into kitti and master_kitti where master_kitti stores attributes other than labels in kitti 
#
# Creates a label_log text file which maps the label name in kitti to label name in master kitti
#
# Creates a text file which contains a list of distinct label names.
#
# Reads only 2 kitti labels [ label_name and bounding_box_coordinates]; other labels are hardcoded as 0.00
#
# Reads only box label not polygon,line.
#
# Applicable for CVAT annotations XML v1.1
#
# Reads XML files from a folder and creates 2 folders Master_kitti files and kitti files in the same directory containing the files with their same name.
#
#------------------------------------------------------------------------------------------------------------------


#Importing BeautifulSoup for parsing operations and os for file operations

from bs4 import BeautifulSoup
import os

# Creating Directories and folders

path_to_dir=''

entries = os.listdir(path_to_dir)
create_dir=os.path.dirname(path_to_dir)

# Creating required folders

m=create_dir+"/"+"Master_kitti files"
q=create_dir+"/"+"kitti files"
p=create_dir+"/"+"label_log_files"

os.mkdir(m)
os.mkdir(q)
os.mkdir(p)

# List to maintain distinct labels

label_distinct=list()

# Traversing the folders and picking up files

for i1 in entries:
    
    k1=path_to_dir+"/"+i1
    
    # Loading the file on to the variable

    soup = BeautifulSoup(open(k1), 'xml')

    # List containing the master kitti details

    k=list()
    l1=str()

    # Dictionary to store all the extra attributes other than the kitti labels

    Master_kitti_labels = []

    # Collecting all extra attributes present in the file and storing in Master_kitti_labels

    for i in soup.find_all('box'):
        for y in i.find_all('attribute'):
            if y.attrs['name'] not in Master_kitti_labels:
                Master_kitti_labels.append(y.attrs['name'])
            

    # Looping through all tags named box in xml file

    for i in soup.find_all('box'):
            
        # Dictionary to store extra attributes of the current box
    
        Master_kitti_dict={}
    
        # Storing the kitti values into the list and generating distinct labels list
        
        if i.attrs['label'] not in label_distinct:
            
            label_distinct.append(i.attrs['label'])
    
        k=[i.attrs["label"],"0.00", i.attrs["occluded"], "0.00", i.attrs["xtl"], i.attrs["ytl"], i.attrs["xbr"], i.attrs["ybr"], "0.00", "0.00", "0.00", "0.00", "0.00", "0.00", "0.00"]

        # Looping through the attribute subtag in a box tag
    
        for y in i.find_all('attribute'):
        
            Master_kitti_dict[y.attrs['name']]=y.text
        
        # Setting the Non-present attribute's value to 0.00
    
        for x in Master_kitti_labels:
    
            if x not in Master_kitti_dict.keys():
        
                Master_kitti_dict[x]='0.00'
            
        # Appending the extra labels to list k 
    
        for x in Master_kitti_labels:
        
            k.append("'%s'" % Master_kitti_dict[x])
            
        kitti_format=" ".join(k[0:15])
                
        for x in Master_kitti_labels:
            
            k[0]=Master_kitti_dict[x]+"*"+k[0]

            
        # converting the list into Kitti and Master_kitti format
    
        master_kitti=" ".join(k[0:15])
        
        
        # Getting file names
        
        n=os.path.splitext(i.parent.attrs['name'])[0]
        l=os.path.basename(n)
        l3=l1
        l1=m+"/"+l+".txt"
        l2=q+"/"+l+".txt"
        l4=p+"/"+l+".txt"
            
        # Creating the files; Flag variable used to do the below operations only once 
        
        if(l3!=l1):
            f = open(l1, "a")
            f.write("------------------------------------------------------------------------------------")
            f.write("\n")
            f.write("Note:")
            f.write("\n")
            f.write("Master kitti extra labels - %s" % Master_kitti_labels[::-1])
            f.write("\n")        
            f.write("0.00 in the extra labels means the label is not present.")
            f.write("\n")
            f.write("Blank fields means the label is present and the value is left blank")
            f.write("\n")
            f.write("------------------------------------------------------------------------------------")
            f.write("\n")
            f.close()
    
        # writing data into respective files
        
        f = open(l1, "a")
        f1= open(l2, "a")
        f2= open(l4,"a")
        f.write("\n")
        f.write(master_kitti)
        f.close()
        f1.write(kitti_format)
        f1.write("\n")
        f1.close()
        f2.write(kitti_format.split(' ', 1)[0])
        f2.write(":-")
        f2.write(master_kitti.split(' ', 1)[0])
        f2.write('\n')
        f2.close()

        
f3= open(create_dir+'/'+'distinct_label.txt',"a")
f3.write(str(label_distinct))
f3.close()

###___END___###



