## About the App

This python Script will take the numerator and Denominator of a DHIS application and replace the UID with the dataelement Name and the category option combo Name


### Run the App

#### Download the database tables 
    - Indicators
    - categoryoptioncombo
    - Data element

Use the SQL View in maintainance if you don't have access to the database, Download the whole dataset for (Dataelement and categoryoptioncombo)
Maintaine the structure of the database tables 
or
Make sure the following column are available


    - Indicators [name, numerator, denominator]
    - categoryoptioncombo [name, uid]
    - Data element [name, uid]