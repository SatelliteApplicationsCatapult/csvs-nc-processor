FROM continuumio/miniconda3

RUN conda install --yes -c conda-forge iris
RUN conda update -n base -c defaults conda
RUN conda install boto3

WORKDIR /usr/src/app/
COPY . /usr/src/app/

ENV CLIMATE_DATA_URL=http://37.128.186.209/LAURA/ERA5/
ENV S3_URL=http://s3-uk-1.sa-catapult.co.uk
ENV S3_BUCKET=csvs-netcdf
ENV S3_ID=testID
ENV S3_KEY=test_key

CMD tail -f /dev/null
