def count_label_with_attribute_value(Path_to_xml_file,label_name,attribute_name,attribute_value):
    

    from bs4 import BeautifulSoup

    soup=BeautifulSoup(open(Path_to_xml_file), 'xml')

    count = 0

    for i in soup.find_all('box'):
    
        if i.attrs['label']==label_name:
        
            for j in i.find_all('attribute'):
            
                if (j.attrs['name'] == attribute_name):
                
                    if (j.text == attribute_value):
                    
                        count = count + 1
                    
    print(f"The number of {attribute_value} {attribute_name} {label_name} is {count}")
                    

Path_to_xml_file='/home/murthylogeshwar/Downloads/PPE - BPCL Mumbai Jul 2019 TPulse vids - Day 7-12.xml'
label_name='Suit'
attribute_name='colour'
attribute_value='Red'

count_label_with_attribute_value(Path_to_xml_file,label_name,attribute_name,attribute_value)