This project is a machine learning application using Apache Spark ML.

Here are the possible methods:
```
http://spark.apache.org/docs/latest/mllib-classification-regression.html
```

# Docker setup method

First setup docker by following [Docker Setup Instructions](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-repository)

Second just one line command to setup all the things:
```
sudo docker run --name <cotainer name> -h <ip> -p 5000:5000  ruiwu1990/wells_fargo_data_mining python views.py
```

<container name> should be replaced by the name of your container and <ip> should be replaced by your machine ip, here is a command working in our machine:

```
sudo docker run --name rui -h 0.0.0.0 -p 5000:5000  ruiwu1990/wells_fargo_data_mining python views.py
```


# Standard installation method

Be sure you have Apark Spark installed in your machine. If not, please follow the [Apark Spark Setup Instructions](https://spark.apache.org/downloads.html)

First create a virtual environment
```
mkvirtualenv -p python2.7 dev
```

If you have created the virtual environment, then use this commend to enter it
```
virtualenv dev && source dev/bin/activate
```

Here is the command to install the backend requirements
```
pip install -r requirements.txt
```
Here is the command to set up and run the program
```
python views.py -h 134.197.20.79 -p 5000 --threaded
```
134.197.20.79 should be replaced with your machine ip address. The command is to set up a server with your machine

