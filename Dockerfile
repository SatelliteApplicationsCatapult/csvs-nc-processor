FROM continuumio/miniconda3

COPY requirements.txt /tmp/

RUN conda install --yes -c conda-forge iris
RUN conda update -n base -c defaults conda
RUN conda install --yes --file /tmp/requirements.txt

WORKDIR /usr/src/
COPY src /usr/src/

ENV S3_URL=http://s3-uk-1.sa-catapult.co.uk
ENV S3_BUCKET=csvs-netcdf
ENV S3_ID=testID
ENV S3_KEY=test_key

CMD tail -f /dev/null
