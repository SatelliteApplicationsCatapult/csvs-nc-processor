FROM continuumio/miniconda3

RUN conda install --yes -c conda-forge iris
RUN conda update -n base -c defaults conda
RUN conda install boto3

WORKDIR /usr/src/app/
COPY ./csvs_nc_processor /usr/src/app/csvs_nc_processor

CMD tail -f /dev/null
