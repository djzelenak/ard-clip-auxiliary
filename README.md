# clip_auxiliary

Provide the ability to automate the tiling of various auxiliary data sets used 
by LCMAP classification.  Tiling in this sense means granularizing a CONUS 
dataset based on the ARD tile grid with a spatial reference system defined by 
the LCMAP-specific Albers Equal Area projection and datum:


```bash
PROJCS["Albers",
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378140,298.2569999999957,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0],
        UNIT["degree",0.0174532925199433],
        AUTHORITY["EPSG","4326"]],
    PROJECTION["Albers_Conic_Equal_Area"],
    PARAMETER["standard_parallel_1",29.5],
    PARAMETER["standard_parallel_2",45.5],
    PARAMETER["latitude_of_center",23],
    PARAMETER["longitude_of_center",-96],
    PARAMETER["false_easting",0],
    PARAMETER["false_northing",0],
    UNIT["metre",1,
        AUTHORITY["EPSG","9001"]]]
```

To accommodate different auxiliary input types, the code uses a base filename 
pattern with the following format: 
* AUX_CU_HHHVVV_20000731_CURRENT-DATE_V01_AUX-NAME.tif

Variable Components:
* HHHVVV = tile horizontal-vertical identifier
* AUX-NAME = auxiliary type identifier	
* CURRENT-DATE = processing date (YYYYMMDD)

Static Components:
* AUX = identifies dataset as auxiliary
* CU = sourced from CONUS dataset
* 20000731 = arbitrary date that matches with the LCMAP classification base date
* V01 = version 1
* .tif = All outputs in GeoTiff format

Auxiliary type identifiers used in output filenames:
* aspect = ASPECT
* slope = SLOPE
* posidex = POSIDEX
* dem = DEM
* trends = TRENDS
* mpw = MPW
* nlcd = NLCD
* eroded nlcd = NLCDTRN





