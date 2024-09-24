select 
org.organisationunitid,
org.name as name,
org.uid as uid,
org.code as code ,
org2.uid as parent
org.shortname as shortname,
org.openingdate as openingdate,
org.hierarchylevel as level,
org2.name as ward,
org3.name as subcounty,
org4.name as county
from
organisationunit as org,
organisationunit as org2, 
organisationunit as org3,
organisationunit as org4
where
 org.parentid = org2.organisationunitid
and org2.parentid = org3.organisationunitid
and org3.parentid = org4.organisationunitid
and org.hierarchylevel = 5