FROM frolvlad/alpine-glibc:alpine-3.12

# Install python and pip
RUN apk add --no-cache --update python3 py3-pip bash
ADD ./webapp/requirements.txt /tmp/requirements.txt

# Install dependencies
#RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt


ARG CONDA_VERSION="4.7.12.1"
ARG CONDA_MD5="81c773ff87af5cfac79ab862942ab6b3"
ARG CONDA_DIR="/opt/conda"

ENV PATH="$CONDA_DIR/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1

# Install conda
RUN echo "**** install dev packages ****" && \
    apk add --no-cache --virtual .build-dependencies bash ca-certificates wget && \
    \
    echo "**** get Miniconda ****" && \
    mkdir -p "$CONDA_DIR" && \
    wget "http://repo.continuum.io/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh" -O miniconda.sh && \
    echo "$CONDA_MD5  miniconda.sh" | md5sum -c && \
    \
    echo "**** install Miniconda ****" && \
    bash miniconda.sh -f -b -p "$CONDA_DIR" && \
    echo "export PATH=$CONDA_DIR/bin:\$PATH" > /etc/profile.d/conda.sh && \
    \
    echo "**** setup Miniconda ****" && \
    conda update --all --yes && \
    conda config --set auto_update_conda False && \
    \
    echo "**** cleanup ****" && \
    apk del --purge .build-dependencies && \
    rm -f miniconda.sh && \
    conda clean --all --force-pkgs-dirs --yes && \
    find "$CONDA_DIR" -follow -type f \( -iname '*.a' -o -iname '*.pyc' -o -iname '*.js.map' \) -delete && \
    \
    echo "**** finalize ****" && \
    mkdir -p "$CONDA_DIR/locks" && \
    chmod 777 "$CONDA_DIR/locks"



#RUN conda install --no-cache-dir -q -r /tmp/requirements.txt
RUN conda install --file /tmp/requirements.txt

RUN conda install -c conda-forge matplotlib
RUN conda install --channel cantera cantera


ADD ./webapp /opt/webapp/
WORKDIR /opt/webapp

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
