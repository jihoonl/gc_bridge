# Google Cloud Bridges


## Google Cloud Vision

ROS wrapper service server to query google cloud vision for annotation

## Preparation

#### 1. Install dependencies

```
  > sudo apt-get install python-pip
  > pip install -r requirements.txt
```

#### 2. Create Google Cloud Project, setup API credentials.

* [Google Cloud Vision API - Getting Started](https://cloud.google.com/vision/docs/getting-started)

#### 3. Setup an environment variable 

```
 > export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials 
```

#### 4. Test Google Cloud Vision

```
  > # setup your ros environment
  > cd gc_vision_bridge/tests 
  > ./test_face.py
```

#### 5. Test Service Server

```
  > # setup your ros envionrment
  > roscore
  > rosrun gc_vision_bridge srv_server.py
  
  > rosrun gc_vision_bridge srv_client.py # or test with your own service call 
```
