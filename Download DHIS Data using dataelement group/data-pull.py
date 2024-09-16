
import requests
import pandas as pd
import io
import base64
import os

username = os.getenv("KHIS_USERNAME", '')
password = os.getenv("KHIS_PASSWORD", '')

print(f" Username: {username} - Password: {password}")
domain_name = 'his.org'

credentials = f"{username}:{password}"


auth_coded = base64.b64encode(credentials.encode()).decode('utf-8')

p_url = "https://{}/api/29/sqlViews/DUdU4jGEYPm/data.csv?var=groupuid:{}&var=pstart:{}&var=pend:{}"

# change c.uid and the periodtype appropriately
sql_view_query = """

select
	de.uid as dataelement,
	TO_CHAR(p.startdate ,
	'YYYYMM') as period,
	o.uid as orgunit,
	case 
		when c.uid = 'NhSoXUMPK2K' then 'HllvX50cXC0'
		else c.uid
	end as categoryoptioncombo,
	case 
		when c.uid = '15' then 'HllvX50cXC0'
		else ''
	end as attributeoptioncombo,
	d.value as value,
	d.storedby as storedby,
	d.lastupdated as lastupdated,
	d."comment" as comment,
	d.followup as followup,
	d.deleted as deleted
from
	datavalue d
join dataelement de on
	de.dataelementid = d.dataelementid
join organisationunit o on
	o.organisationunitid = d.sourceid
join categoryoptioncombo c on
	c.categoryoptioncomboid = d.categoryoptioncomboid
join "period" p on
	p.periodid = d.periodid
where
	d.dataelementid in (
	select
		distinct dataelementid
	from
		dataelementgroupmembers d2
	join dataelementgroup d3 on
		d3.dataelementgroupid = d2.dataelementgroupid
	where
		d3.uid = '${groupuid}')
	and p.startdate = '${pstart}'
	and p.enddate = '${pend}'
	and p.periodtypeid = 5;

"""
# Add the output of names for uid for dataelement, orgunit, catcombo
sqlview_2 = """
select
	de.uid as dataelement,
	TO_CHAR(p.startdate ,
	'YYYYMM') as period,
	o.uid as orgunit,
	o.name as facilityName,
	org2.name,
	org3.name,
	org4.name,
	case 
		when c.uid = 'NhSoXUMPK2K' then 'HllvX50cXC0'
		else c.uid
	end as categoryoptioncombo,
	case 
		when c.uid = '15' then 'HllvX50cXC0'
		else ''
	end as attributeoptioncombo,
	d.value as value,
	d.storedby as storedby,
	d.lastupdated as lastupdated
from
	datavalue d
join dataelement de on
	de.dataelementid = d.dataelementid
join categoryoptioncombo c on
	c.categoryoptioncomboid = d.categoryoptioncomboid
join "period" p on
	p.periodid = d.periodid
join organisationunit o on
	o.organisationunitid = d.sourceid,
	organisationunit as org2, 
	organisationunit as org3,
	organisationunit as org4
where
	d.dataelementid in (
	select
		distinct dataelementid
	from
		dataelementgroupmembers d2
	join dataelementgroup d3 on
		d3.dataelementgroupid = d2.dataelementgroupid
	where
			d3.uid = '${groupuid}')
	and p.startdate = '${pstart}'
	and p.enddate = '${pend}'
	and o.parentid = org2.organisationunitid
	and org2.parentid = org3.organisationunitid
	and org3.parentid = org4.organisationunitid
	and o.code notnull
	and o.hierarchylevel in (5)
	and p.periodtypeid = 5;
"""
payload = {}
headers = {
  'Authorization': f'Basic {auth_coded}'
}
# Functions


# Fetch Data from the server
def fetchData(groupuid, pstart, pend):
    url = p_url.format(domain_name,groupuid, pstart, pend)
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Returning null values, cause: {response.status_code}")
            return []
    except Exception as e:
        print(f'Error fetching data {e}')
        
# Save data as output

# Settings
periods = [
  {
    "periodid": 87179876,
    "periodtypeid": 5,
    "startdate": "2023-07-01",
    "enddate": "2023-07-31",
    "name": "Monthly",
    "monthid": 202307
  },
  {
    "periodid": 87464939,
    "periodtypeid": 5,
    "startdate": "2023-08-01",
    "enddate": "2023-08-31",
    "name": "Monthly",
    "monthid": 202308
  },
  {
    "periodid": 87796296,
    "periodtypeid": 5,
    "startdate": "2023-09-01",
    "enddate": "2023-09-30",
    "name": "Monthly",
    "monthid": 202309
  },
  {
    "periodid": 87628028,
    "periodtypeid": 5,
    "startdate": "2023-10-01",
    "enddate": "2023-10-31",
    "name": "Monthly",
    "monthid": 202310
  },
  {
    "periodid": 87796297,
    "periodtypeid": 5,
    "startdate": "2023-11-01",
    "enddate": "2023-11-30",
    "name": "Monthly",
    "monthid": 202311
  },
  {
    "periodid": 86614638,
    "periodtypeid": 5,
    "startdate": "2023-12-01",
    "enddate": "2023-12-31",
    "name": "Monthly",
    "monthid": 202312
  },
  {
    "periodid": 88972558,
    "periodtypeid": 5,
    "startdate": "2024-01-01",
    "enddate": "2024-01-31",
    "name": "Monthly",
    "monthid": 202401
  },
  {
    "periodid": 89384134,
    "periodtypeid": 5,
    "startdate": "2024-02-01",
    "enddate": "2024-02-29",
    "name": "Monthly",
    "monthid": 202402
  },
  {
    "periodid": 89021774,
    "periodtypeid": 5,
    "startdate": "2024-03-01",
    "enddate": "2024-03-31",
    "name": "Monthly",
    "monthid": 202403
  },
  {
    "periodid": 89088839,
    "periodtypeid": 5,
    "startdate": "2024-04-01",
    "enddate": "2024-04-30",
    "name": "Monthly",
    "monthid": 202404
  },
  {
    "periodid": 89235379,
    "periodtypeid": 5,
    "startdate": "2024-05-01",
    "enddate": "2024-05-31",
    "name": "Monthly",
    "monthid": 202405
  },
  {
    "periodid": 89379301,
    "periodtypeid": 5,
    "startdate": "2024-06-01",
    "enddate": "2024-06-30",
    "name": "Monthly",
    "monthid": 202406
  }
]
dgroups = [
    # {
    #     "uid": "fdZJpEtf2Wa",
    #     "name": "MOH 731-2 Prevention of Mother-to-Child Transmission Revision 2018",
    # },
    {"uid": "z7HEu5CTSgg", "name": "MOH 731-3 HIV and TB treatment Revision 2018"},
    {"uid": "ckpcwmnPE8O", "name": "MOH 731-4 Medical Male Circumcision Revision 2018"},
    {"uid": "gYlOHBR0if2", "name": "MOH 731-5 Post Exposure Prophylaxis Revision 2018"},
    {
        "uid": "ig1GVX7tNmh",
        "name": "MOH 731-1 HIV Testing and Prevention services Revision 2018",
    },
]
for group in dgroups:
    combined_df = pd.DataFrame()  # Initialize an empty DataFrame to combine data
    
    for period in periods:
        # Fetch the data
        print(f'Fecting data for {period}')
        ace = fetchData(group['uid'], period['startdate'], period['enddate'])
        
        # Check if any data was returned
        if len(ace) > 0:
            # Read the data into a DataFrame
            df = pd.read_csv(io.StringIO(ace.decode('utf-8')))
            
            # Append the DataFrame to the combined DataFrame
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        else:
            print(f'No records for {group["name"]} during {period["monthid"]}')
    
    # Save the combined DataFrame to a CSV file for the group
    if not combined_df.empty:
        first_period = periods[0]['monthid']
        last_period = periods[-1]['monthid']
        filename = f'{group["name"]} {first_period} - {last_period}.csv'
        
        combined_df.to_csv(filename, index=False)
        print(f'{len(combined_df)} records of {group["name"]} saved to {filename}')
    else:
        print(f'No data to save for {group["name"]}')          
        # break


