FROM python:3.4

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         libblas-dev \
         liblapack-dev \
         gfortran \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean -y \
    && apt-get autoremove -y

# Use pip to install the latest packages
RUN pip install --no-cache-dir --upgrade \
      cython \
      numpy \
      scipy
RUN pip install flask
RUN pip install requests
RUN pip install mongoengine
RUN pip install Pillow
ADD microservice1.py microservice1.py
ADD bildverarbeitung.py bildverarbeitung.py
ADD img img
RUN chmod +x microservice1.py

CMD python microservice1.py
EXPOSE 1338
