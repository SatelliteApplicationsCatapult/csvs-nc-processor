# netCDF Processor for CSVS

Processes the netCDF files provided by MetOffice for CS project and covert them into suitable CF compliant files ready 
to be published via thredds/geoserver.

## Usage

- Build the docker image
```docker
docker build -t satapps/netcdf-processor .
```

- Run the main process
``` docker
docker run --name netcdf-processor --rm -d  \
    -e S3_ID=<s3 bucket id> \
    -e S3_KEY=<s3 bucket key> \
    satapps/netcdf-processor src/entrypoints/main.py
```

- Run the terria catalog generator for ERA5-Land
``` docker
docker run --name netcdf-processor --rm -d  \
    satapps/netcdf-processor python src/entrypoints/generate_era5_land_terria_catalog.py
```

- Inspect the logs during the processing
``` docker
docker logs -f netcdf-processor
```