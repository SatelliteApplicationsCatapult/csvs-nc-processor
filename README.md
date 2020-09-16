# netCDF Processor for CSVS

Processes the netCDF files provided by MetOffice for CS project and covert them into suitable CF compliant files ready 
to be published via thredds/geoserver.

## Usage

- Build the docker image contained in the env folder using the provided makefile

```docker
docker build -t satapps/netcdf-processor .
```

- Modify the env variables and run the container

``` docker
docker run --name netcdf-processor --rm -d  \
    -e CLIMATE_DATA_URL=http://37.128.186.209/LAURA/ERA5/ \
    -e STD_NAME=air_temperature\
    -e S3_URL=http://s3-uk-1.sa-catapult.co.uk \
    -e S3_BUCKET=csvs-netcdf \
    -e S3_ID=id \
    -e S3_KEY=secret_key \
    satapps/netcdf-processor
```

- Execute the netCDF processor
``` docker
docker exec -it netcdf-processor python main.py
```