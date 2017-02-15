# back-DeepLearningMoviesProject
Python Back-end for the deep learning movies project 

You can find the project description [here](http://air.imag.fr/index.php/Suggestion_intelligente_de_films_bas%C3%A9e_sur_TensorFlow).

## Installation
### Liblinear

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

### Other dependencies
Run the following command to install all dependencies needed by this project :
```
pip install Tensorflow Keras TMDBSimple Flask Gensim numpy scikit-learn nltk pickle
```

### Project
To install the project you have to clone the Git project and install all dependencies listed above:
```
git clone "https://github.com/DeepLearningMoviesProject/back-DeepLearningMoviesProject.git"
```
And add project's root folder to the $PYTHONPATH:
```
cd back-DeepLearningMoviesProject
export PYTHONPATH="$PYTHONPATH:$(pwd)"
```

## Unit tests

You can run all unit tests by using 'python -m unittest discover' command anywhere on the path "back-DeepLearningMoviesProject/MovieProject/tests/unit", the command will run scripts looking like 'test_something.py'.
To run only one test file, you just have to execute the script the classic way :
```
python test_something.py
```


