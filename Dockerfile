FROM tensorflow:2.12.0-gpu

RUN apt-get update \
    && apt install -y git

RUN useradd -m tf
USER tf

RUN cd /home/tf \
    && git clone https://github.com/chatotp/HackyAIMod.git \
    && cd HackyAIMod \
    && pip install -r reqs-without-tf.txt

WORKDIR /home/tf/HackyAIMod
ENTRYPOINT python /home/tf/HackyAIMod/main.py