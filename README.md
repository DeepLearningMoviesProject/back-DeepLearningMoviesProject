# back-DeepLearningMoviesProject
Python Back-end for the deep learning movies project 

You can find the project description [here](http://air.imag.fr/index.php/Suggestion_intelligente_de_films_bas%C3%A9e_sur_TensorFlow).

## Installation

To operate the back-end, the working environment must be installed. To do this, you can directly use a docker container or install all the environment on your computer / server.

### How use Docker ?

The Dockerfile provided in "Docker" folder how to install all necessary environment on a docker container.
You can find more information about Docker [here](https://www.docker.com/)

First at all, [install docker on your machine](https://docs.docker.com/engine/installation/) and download the Dockerfile, allowed to build the Docker image.

To build the Docker image follow the command lines below ("." is the path to the Dockerfile, here we run the command in the file containing the Dockerfile) :
```
docker build .
```
Note image id, you just built. You also can find this id by running the command:
```
docker ps -a
```

The back-end API uses port 5000. The easiest way is to link port 80 of your machine to port 5000 of the docker container using the command line below.
Furthermore, some files aren't provided in our git project, but must be present for its operation. You will find these files [here](). Copy them into a folder on your computer, which you will bind to the docker container, thanks to the command line below :
```
docker run -ti -p 80:5000 -v [PathHote]:/root/git/back-DeepLearningMoviesProject/MovieProject/resources/persist/ [ImageID]
```
This last command open the container console, so you can launch the back-end API (or execute another file):
```
python /root/git/back-DeepLearningMoviesProject/MovieProject/api/api.py
```

### Environment installation on your computer / server

#### Liblinear

Liblinear is a library for Large Linear Classification, more informations [here](http://www.csie.ntu.edu.tw/~cjlin/liblinear).
To install it on python follow the command lines below:
```
wget http://www.csie.ntu.edu.tw/~cjlin/liblinear/liblinear-2.1.zip
unzip liblinear-2.1.zip 
cd liblinear-2.1/python
make
```

And add the folder "liblinear-2.1/python" into $PYTHONPATH:
```
cd liblinear-2.1/python
export PYTHONPATH="$PYTHONPATH:$(pwd)"
```

#### MySQL
```
RUN apt-get install mysql mysql-python sqlalchemy
```

#### Other dependencies
Run the following command to install all dependencies needed by this project :
```
pip install atlas numpy scipy nltk tmdbsimple scikit-learn h5py enum34 TwitterSearch pandas flask flask-cors bcrypt PyJWT pickle Tensorflow Keras && pip install -U gensim

```

#### Project
To install the project you have to clone the Git project and install all dependencies listed above:
```
git clone "https://github.com/DeepLearningMoviesProject/back-DeepLearningMoviesProject.git"
```
And add project's root folder to the $PYTHONPATH:
```
cd back-DeepLearningMoviesProject
export PYTHONPATH="$PYTHONPATH:$(pwd)"
```

### MySQL Server
To run the MySQL Server, refer to the "README.md" into the "mysql" folder


## Unit tests

You can run all unit tests by using the command below anywhere on the path "back-DeepLearningMoviesProject/MovieProject/tests/unit", the command will run scripts looking like 'test_something.py'.
```
python -m unittest discover
``` 

To run only one test file, you just have to execute the script the classic way :
```
python test_something.py
```