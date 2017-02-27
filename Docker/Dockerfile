FROM 	ubuntu:14.04
MAINTAINER Niogret Edwin <niogret.edwin@live.fr>

WORKDIR /root

#----------------------------------------------------------------------------------------


# Update the sources list----------------------------------------------------------------
RUN apt-get update
#----------------------------------------------------------------------------------------


#Utilitaires-----------------------------------------------------------------------------
RUN apt-get -qq -y install python2.7
RUN apt-get -yqq install python-pip
RUN apt-get -y install python-dev
RUN python -m pip install --upgrade pip
RUN pip install numpy 
RUN pip install nltk
RUN pip install tmdbsimple
RUN pip install gensim
RUN apt-get install tree
RUN apt-get -yqq install git
RUN pip install scipy
RUN pip install scikit-learn
RUN pip install pillow
RUN pip install h5py
RUN mkdir git
#----------------------------------------------------------------------------------------


#TensorFlow/Keras-----------------------------------------------------------------------------------
RUN pip install tensorflow
RUN pip install keras
#----------------------------------------------------------------------------------------


#Scala/Hadoop/Scala----------------------------------------------------------------------
COPY .updatescala /root/.updatescala
RUN apt-get -yqq install software-properties-common
RUN apt-add-repository ppa:webupd8team/java 
RUN apt-get update
RUN echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN apt-get install -y oracle-java7-installer
RUN java -version
RUN wget www.scala-lang.org/files/archive/scala-2.10.4.deb
RUN apt-get -yqq install libjansi-java
RUN dpkg -i scala-2.10.4.deb
RUN apt-get update
RUN apt-get -yqq install scala
RUN chmod 777 .updatescala
RUN ./.updatescala 11.8.2
RUN scala -version
RUN wget http://d3kbcqa49mib13.cloudfront.net/spark-1.2.0-bin-hadoop2.4.tgz
RUN tar -xzvf spark-1.2.0-bin-hadoop2.4.tgz
COPY test.py /root/spark-1.2.0-bin-hadoop2.4/test.py
RUN rm /root/spark-1.2.0-bin-hadoop2.4/python/pyspark/mllib/__init__.py
COPY __init__.py /root/spark-1.2.0-bin-hadoop2.4/python/pyspark/mllib/__init__.py
RUN rm scala-2.10.4.deb
RUN rm scala-2.11.8.deb
RUn rm spark-1.2.0-bin-hadoop2.4.tgz
RUN echo "export SPARK_HOME=/usr/local/Cellar/apache-spark/1.5.1" >> .bashrc
RUN echo "export PYTHONPATH=\$SPARK_HOME/libexec/python:\$SPARK_HOME/libexec/python/build:\$PYTHONPATH" >> .bashrc
RUN echo "export PYTHONPATH=\$SPARK_HOME/python/lib/py4j-0.8.2.1-src.zip:\$PYTHONPATH" >> .bashrc
RUN echo "export PYTHONPATH=\$SPARK_HOME/python:\$SPARK_HOME/python/build:\$PYTHONPATH" >> .bashrc
RUN echo "export PYTHONPATH=\$SPARK_HOME/python/:\$PYTHONPATH" >> .bashrc
RUN echo "export SPARK_HOME=\"/opt/spark\"" >> .bashrc
RUN echo "export PATH=\$PATH:~/spark-1.2.0-bin-hadoop2.4/bin" >> .bashrc	
RUN echo "export PATH=~/spark-1.2.0-bin-hadoop2.4/bin:\$PATH" >> .bashrc
#----------------------------------------------------------------------------------------


#Elephas---------------------------------------------------------------------------------
RUN pip install elephas
RUN pip install py4j
RUN pip install --upgrade six>=1.70
RUN sudo pip install Flask
RUN pip install --upgrade --no-deps git+git://github.com/maxpumperla/elephas
#----------------------------------------------------------------------------------------


#MySQL-----------------------------------------------------------------------------------
RUN apt-get -y install mysql-server
RUN apt-get -y install libmysqlclient-dev
RUN pip install mysql
RUN pip install mysql-connector
#----------------------------------------------------------------------------------------


#liblinear-------------------------------------------------------------------------------
RUN git clone https://github.com/ninjin/liblinear.git
RUN cd liblinear && make
RUN cd liblinear/python && make
RUN echo "export PYTHONPATH=\$PYTHONPATH:~/liblinear/python/" >> .bashrc
#----------------------------------------------------------------------------------------


#GitProjet------------------------------------------------------------------------------
RUN git clone https://github.com/DeepLearningMoviesProject/back-DeepLearningMoviesProject.git
RUN mv back-DeepLearningMoviesProject/ git/back-DeepLearningMoviesProject/
RUN echo "export PYTHONPATH=\$PYTHONPATH:~/git/back-DeepLearningMoviesProject/" >> .bashrc
COPY glove.6B.50d.txt /root/git/back-DeepLearningMoviesProject/MovieProject/resources/glove.6B.50d.txt
#----------------------------------------------------------------------------------------


#Mesos-----------------------------------------------------------------------------------
RUN git clone https://git-wip-us.apache.org/repos/asf/mesos.git
RUN sudo apt-get update
# Install a few utility tools.
RUN sudo apt-get install -y tar wget git
# Install the latest OpenJDK.
RUN sudo apt-get install -y openjdk-7-jdk
# Install autotools (Only necessary if building from git repository).
RUN sudo apt-get install -y autoconf libtool
# Install other Mesos dependencies.
RUN sudo apt-get -y install build-essential libcurl4-nss-dev libsasl2-dev libsasl2-modules maven libapr1-dev libsvn-dev
# Bootstrap (Only required if building from git repository).
RUN cd mesos && ./bootstrap
# Configure and build.
RUN cd mesos && mkdir build
RUN cd mesos/build && ../configure
RUN cd mesos/build && make
#make check
RUN cd mesos/build && make install
#----------------------------------------------------------------------------------------

RUN apt-get update
