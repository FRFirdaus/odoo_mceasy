FROM odoo:17

USER root

COPY ./requirements.txt mceasy-requirements.txt

RUN pip3 install --upgrade pip && \
    pip3 install setuptools && \
    pip3 install -r mceasy-requirements.txt --no-cache-dir && \
    rm -rf mceasy-requirements.txt