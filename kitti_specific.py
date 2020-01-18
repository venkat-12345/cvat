def specific_labels(path_to_file,attribute_separator='*',specific_label_list=dict()):
    
    """
    Reads a xml file and creates a text file (kitti_with_specified_labels.txt) containing data in kitti format.
    
    Specified labels with specified attributes are only written in the file.
    
    Parameters:
    
        path_to_file (str): The path to xml file.
        specific_label_list (dictionary) : Dictionary containing required labels as key and corresponding attribute list as values.
        attribute_separator (char) : Charachter to separate attribute values in kitti file.

    """
    from bs4 import BeautifulSoup
    from pathlib import Path    
    
    # case : incorrect datatype passed
    
    if(type(specific_label_list)!=dict):
        raise Exception('Incorrect Datatype : Specific_label_list is not a dictionary')
        return
    
    # Importing required libraries
    
    from bs4 import BeautifulSoup
    from pathlib import Path
    
    # Loading the path of xml to a Pathlib variable
    path1=Path(path_to_file)
    
    # Generating path to the kitti file
    path_to_kitti_labels_file=Path(path1.parents[0],'kitti_with_specified_labels.txt')
            
    # Generating the soup variable 
    soup = BeautifulSoup(open(path_to_file), 'xml')
    
    # file to write the kitti file
    f1=open(path_to_kitti_labels_file,'a')
    
    # Case : Empty dictionary is passed ; Writes labels with all attributes
    if(len(specific_label_list)==0):
        
        # Initialising a empty list to collect all distinct attributes
        distinct_labels=list()
        
        for i in soup.find_all('box'):

            for y in i.find_all('attribute'):
    
                # Traversing through every attributes and appending unique attributes
        
                if y.attrs['name'] not in distinct_labels:
                
                    distinct_labels.append(y.attrs['name'])
                
        # Writing header information on the kitti text file
        f1.write("Kitti files have the following attribute's text along with their label\n")
        f1.write(f"{distinct_labels}\n\n")
                    
        for i in soup.find_all('box'):
    
            attribute_label_dict=dict()
            modified_label=list()
    
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
            
            f1.write(f"{attribute_separator.join(modified_label)} 0.00 {i.attrs['occluded']} 0.00 {i.attrs['xtl']} {i.attrs['ytl']} {i.attrs['xbr']} {i.attrs['ybr']} 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n")

    # Case : Mentioned labels and attributes are picked and written on to the file
    else:
        
        # Finding all tags named as 'box'
        for i in soup.find_all('box'):
        
            modified_label=list()
        
            if i.attrs['label'] in specific_label_list.keys():
        
                for j in i.find_all('attribute'):
                
                    for k in specific_label_list[i.attrs['label']]:
                
                        if j.attrs['name'] == k:
                    
                            modified_label.append(j.text)
        
                modified_label.append(i.attrs['label'])
            
                f1.write(f"{attribute_separator.join(modified_label)} 0.00 {i.attrs['occluded']} 0.00 {i.attrs['xtl']} {i.attrs['ytl']} {i.attrs['xbr']} {i.attrs['ybr']} 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n")


