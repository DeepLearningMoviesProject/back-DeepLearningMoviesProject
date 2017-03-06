FROM 	ubuntu:14.04
MAINTAINER Niogret Edwin <niogret.edwin@live.fr>

WORKDIR /root
#----------------------------------------------------------------------------------------


#Utilitaires (Update the sources list)---------------------------------------------------
RUN apt-get update && apt-get -y install git wget && apt-get install nano tree
#----------------------------------------------------------------------------------------


#PYTHON 2.7.13 + Librairies --------------------------------------------------------------
RUN apt-get -y install build-essential checkinstall
RUN apt-get -y install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
RUN cd /usr/src/ && wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz && tar xzf Python-2.7.13.tgz && cd /usr/src/Python-2.7.13 && ./configure --prefix=/usr --enable-unicode=ucs4 && make -i install
COPY get-pip.py /root/get-pip.py
RUN python get-pip.py
RUN pip install atlas numpy scipy nltk tmdbsimple scikit-learn h5py enum34 TwitterSearch pandas flask flask-cors && pip install -U gensim
#----------------------------------------------------------------------------------------


#Scala/Hadoop/Scala----------------------------------------------------------------------
#COPY .updatescala /root/.updatescala
#RUN apt-get -yqq install software-properties-common
#RUN apt-add-repository ppa:webupd8team/java 
#RUN apt-get update
#RUN echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
#RUN apt-get install -y oracle-java7-installer
#RUN java -version
#RUN wget www.scala-lang.org/files/archive/scala-2.10.4.deb
#RUN apt-get -yqq install libjansi-java
#RUN dpkg -i scala-2.10.4.deb
#RUN apt-get update
#RUN apt-get -yqq install scala
#RUN chmod 777 .updatescala
#RUN ./.updatescala 11.8.2
#RUN scala -version
#RUN wget http://d3kbcqa49mib13.cloudfront.net/spark-1.2.0-bin-hadoop2.4.tgz
#RUN tar -xzvf spark-1.2.0-bin-hadoop2.4.tgz
#COPY test.py /root/spark-1.2.0-bin-hadoop2.4/test.py
#RUN rm /root/spark-1.2.0-bin-hadoop2.4/python/pyspark/mllib/__init__.py
#COPY __init__.py /root/spark-1.2.0-bin-hadoop2.4/python/pyspark/mllib/__init__.py
#RUN rm scala-2.10.4.deb
#RUN rm scala-2.11.8.deb
#RUn rm spark-1.2.0-bin-hadoop2.4.tgz
#RUN echo "export SPARK_HOME=/usr/local/Cellar/apache-spark/1.5.1" >> .bashrc
#RUN echo "export PYTHONPATH=\$SPARK_HOME/libexec/python:\$SPARK_HOME/libexec/python/build:\$PYTHONPATH" >> .bashrc
#RUN echo "export PYTHONPATH=\$SPARK_HOME/python/lib/py4j-0.8.2.1-src.zip:\$PYTHONPATH" >> .bashrc
#RUN echo "export PYTHONPATH=\$SPARK_HOME/python:\$SPARK_HOME/python/build:\$PYTHONPATH" >> .bashrc
#RUN echo "export PYTHONPATH=\$SPARK_HOME/python/:\$PYTHONPATH" >> .bashrc
#RUN echo "export SPARK_HOME=\"/opt/spark\"" >> .bashrc
#RUN echo "export PATH=\$PATH:~/spark-1.2.0-bin-hadoop2.4/bin" >> .bashrc	
#RUN echo "export PATH=~/spark-1.2.0-bin-hadoop2.4/bin:\$PATH" >> .bashrc
#----------------------------------------------------------------------------------------


#Elephas---------------------------------------------------------------------------------
#RUN pip install elephas
#RUN pip install py4j
#RUN pip install --upgrade six>=1.70
#RUN sudo pip install Flask
#RUN pip install --upgrade --no-deps git+git://github.com/maxpumperla/elephas
#----------------------------------------------------------------------------------------


#MySQL-----------------------------------------------------------------------------------
RUN apt-get -y install mysql-server libmysqlclient-dev && pip install mysql mysql-connector pymysql sqlalchemy
#RUN echo mysql-server mysql-server/root_password password $MYSQLTMPROOT | debconf-set-selections 
#----------------------------------------------------------------------------------------


#liblinear-------------------------------------------------------------------------------
RUN git clone https://github.com/ninjin/liblinear.git && cd liblinear && make && cd python && make
RUN echo "export PYTHONPATH=\$PYTHONPATH:~/liblinear/python/" >> .bashrc
#----------------------------------------------------------------------------------------


#GitProjet------------------------------------------------------------------------------
RUN mkdir git && git clone https://github.com/DeepLearningMoviesProject/back-DeepLearningMoviesProject.git && mv back-DeepLearningMoviesProject/ git/back-DeepLearningMoviesProject/
RUN echo "export PYTHONPATH=\$PYTHONPATH:~/git/back-DeepLearningMoviesProject/" >> .bashrc
#COPY glove.6B.50d.txt /root/git/back-DeepLearningMoviesProject/MovieProject/resources/glove.6B.50d.txt
#----------------------------------------------------------------------------------------


#TensorFlow------------------------------------------------------------------------------
# Install TensorFlow CPU version from central repo
#RUN pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.11.0-cp27-none-linux_x86_64.whl
#RUN pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.12.0-cp27-none-linux_x86_64.whl
RUN pip install tensorflow
#----------------------------------------------------------------------------------------


#Keras-----------------------------------------------------------------------------------
RUN pip install keras
#----------------------------------------------------------------------------------------


#Mesos-----------------------------------------------------------------------------------
#RUN git clone https://git-wip-us.apache.org/repos/asf/mesos.git
#RUN sudo apt-get update
# Install a few utility tools.
#RUN sudo apt-get install -y tar wget git
# Install the latest OpenJDK.
#RUN sudo apt-get install -y openjdk-7-jdk
# Install autotools (Only necessary if building from git repository).
#RUN sudo apt-get install -y autoconf libtool
# Install other Mesos dependencies.
#RUN sudo apt-get -y install build-essential libcurl4-nss-dev libsasl2-dev libsasl2-modules maven libapr1-dev libsvn-dev
# Bootstrap (Only required if building from git repository).
#RUN cd mesos && ./bootstrap
# Configure and build.
#RUN cd mesos && mkdir build
#RUN cd mesos/build && ../configure
#RUN cd mesos/build && make
#make check
#RUN cd mesos/build && make install
#----------------------------------------------------------------------------------------

EXPOSE 5000


# Only to test---------------------------------------------------------------------------
RUN cd git/back-DeepLearningMoviesProject/ && git checkout features/backOnServer
#RUN cd git/back-DeepLearningMoviesProject/MovieProject/api/
#CMD python ~/git/back-DeepLearningMoviesProject/MovieProject/api/api.py
