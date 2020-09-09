# netCDF Processor for CSVS

Processes the netCDF files provided by MetOffice for CS project and covert them into suitable CF compliant files ready 
to be published via threeds/geoserver.

## Usage

- Build the docker image contained in the env folder using the provided makefile

```docker
cd env
make build
cd ..
```

- Run the docker image and mount the root directory on it

``` docker
docker run -it --rm --entrypoint /bin/sh  -v $(realpath .):/app satapps/netcdf-processor:0.1
```

- Move to app folder and execute the main file with the test file and test standard name

```bash
# cd app
# python main.py ERA5_daily_mean_2mTemp_1980.tar.gz air_temperature
```

