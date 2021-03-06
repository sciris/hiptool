FROM continuumio/anaconda:latest
ADD . /app
WORKDIR /app

ARG PORT
ARG REDIS_URL
ENV PORT $PORT
ENV REDIS_URL $REDIS_URL

# Set up apt-get
RUN apt-get update -qq && apt-get install -yqq gnupg curl libgl1-mesa-glx gcc

# Install nodejs
RUN curl -sL https://deb.nodesource.com/setup_9.x | bash
RUN apt-get install -yqq nodejs
RUN apt-get clean -y

# Install sciris
RUN git clone https://github.com/sciris/sciris.git
RUN cd sciris && python setup.py develop
RUN git clone https://github.com/sciris/scirisweb.git
RUN cd scirisweb && python setup.py develop

# Install mpld3
RUN git clone https://github.com/sciris/mpld3.git
RUN cd mpld3 && python setup.py submodule && python setup.py install

# Install hiptool
RUN python setup.py develop

# Install app
WORKDIR client
RUN python install_client.py
RUN python build_client.py

CMD python run.py
