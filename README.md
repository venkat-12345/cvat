# CVAT

Powerful and efficient Computer Vision Annotation Tool (CVAT)

## Setup

### Install Packages

* Install docker
```sh
sudo apt-get update
sudo apt-get --no-install-recommends install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg-agent \
  software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"
sudo apt-get update
sudo apt-get --no-install-recommends install -y docker-ce docker-ce-cli containerd.io
```

* Perform post-installation steps to run docker without root permissions.
```sh
sudo groupadd docker
sudo usermod -aG docker $USER
```

* Install docker-compose (1.19.0 or newer).
```sh
sudo apt-get --no-install-recommends install -y python3-pip python3-setuptools
sudo python3 -m pip install setuptools docker-compose
```

### Setup Cloud Mount (AWS)

* Install s3fs-fuse
```sh
sudo apt install s3fs
```

* Get AWS credentials and **replace** ACCESS_KEY_ID and SECRET_ACCESS_KEY in the following command
```sh
echo ACCESS_KEY_ID:SECRET_ACCESS_KEY > ${HOME}/.passwd-s3fs
chmod 600 ${HOME}/.passwd-s3fs
```

* Mount S3 path. **Replace** <bucket-name> with your bucket name/
```sh
mkdir /home/ubuntu/cloud-mount
s3fs <bucket-name> /home/ubuntu/cloud-mount -o allow_other -o passwd_file=${HOME}/.passwd-s3fs
```

### Clone CVAT
* Clone CVAT source code from the GitHub repository.
```sh
sudo apt-get --no-install-recommends install -y git
git clone -b dt-v2.1.0 https://github.com/detecttechnologies/cvat.git
cd cvat
```

* To access CVAT over a network or through a different system, export CVAT_HOST environment variable. **Replace** your-ip-address
```sh
export CVAT_HOST=your-ip-address
```

* Export Cloud Mount path
```sh
export CVAT_MOUNT=/home/ubuntu/cloud-mount
```

* Build and run docker containers
```sh
docker-compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.override.yml up --build -d
```

* Ignore if upgrading, Create superuser
```sh
docker exec -it cvat bash -ic 'python3 ~/manage.py createsuperuser'
```
### User Analytics Implementation
 * Export your IP address and Cloud Mount path as done in above steps
 * But use this command to build and run docker containers to include kibana
 ```sh
docker-compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.override.yml -f components/analytics/docker-compose.analytics.yml up --build -d
```
 * After the installation you can find Analytics Section in CVAT Dashboard
 * By clicking on it you will be redirected to Kibana Dashboard Page
 * For Creating Polygon+Box Count and Total Count Fields Below steps should be followed
    * Go to Management->Index Patterns->Scripted Fields->Add Scripted Field
        - Name = 'Total Count'
        - Let the remaining Attributes as default
        - Scroll to the Script Section and Paste the BelowCode and Click on Create Field
        ```painless
        doc['box count'].value + doc['frame count'].value + doc['object count'].value + doc['points count'].value + doc['polygon count'].value + doc['polyline count'].value + doc['track count'].value
        ```
    * Click the Add Script Field
        - Name = 'Polygon+Box Count'
        - Let the remaining Attributes as default
        - Scroll to the Script Section and Paste the BelowCode and Click on Create Field
        ```painless
        doc['box count'].value + doc['polygon count'].value
        ```
 * Now Creating a table for User Activity
    * Got to Vizualize->List of Users
        - On the left side you can find all the metrics used in the tabel
            1. Click on Add Metrics->Metric
            1. In Aggregation dropdown box Select Unique Count(Under Metrict Aggregation Section)
            1. In Feild dropdown box Select Total Count (Under number Section)
            1. Custom Name = Total Count
        * Repeat the Above Steps for Polygon+Box Count
    * Final Save the Table (On Top Right)
    * Enable Save as new Visualization
    * Title = User Activity and Click on Confirm Save
