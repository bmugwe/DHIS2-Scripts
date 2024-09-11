### Download data progrmatically using dataelement group id
This scripts outputs the data in sthe same format as the Data Export module

## Variables for period and dataelement groups
The periods array of object can be extracted from the period table using the a join query to periodtypeid and 
- toCHAR(startdate,YYYYMM)

For the dataelement group make an array of objects with the uid and the name