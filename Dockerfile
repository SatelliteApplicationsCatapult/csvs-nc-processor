FROM continuumio/miniconda3

RUN conda install --yes -c conda-forge iris
RUN conda update -n base -c defaults conda
COPY requirements.txt /tmp/
RUN conda install --yes --file /tmp/requirements.txt

WORKDIR /app/
COPY . /app/

ENV PYTHONPATH /app/

ENV S3_URL=http://s3-uk-1.sa-catapult.co.uk
ENV S3_BUCKET=csvs-netcdf
ENV S3_ID=testID
ENV S3_KEY=test_key

CMD tail -f /dev/null
