sorgUnitspull = ""select 
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
                and org.hierarchylevel = 5""






SELECT
    pi.programid as programid
    p3.name AS program_name,
    pi.programinstanceid ,
    psi.programstageinstanceid,
    t2.trackedentityinstanceid as trackedinstance,
    t3.name AS trackedentitytype_name,
    d.dataelementid,
    psi.organisationunitid as ouid,
    d.name AS dataelement_name,
    t.value,
FROM
    trackedentitydatavalueaudit t
inner JOIN
    programstageinstance psi ON psi.programstageinstanceid = t.programstageinstanceid
inner JOIN
    programinstance pi ON pi.programinstanceid = psi.programinstanceid  
inner join  "program" p3 ON p3.programid = pi.programid 
inner JOIN
    dataelement d ON d.dataelementid = t.dataelementid 
inner JOIN
    trackedentityinstance t2 ON t2.trackedentityinstanceid = pi.trackedentityinstanceid 
inner JOIN
    trackedentitytype t3 ON t3.trackedentitytypeid = t2.trackedentitytypeid
where d.dataelementid = 26257 and t.value like '%${var}%' and p3.uid = '${programid}';