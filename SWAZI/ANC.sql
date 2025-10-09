CREATE TABLE ANC_Summary (
    FacilityCode NVARCHAR(50),
    ReportMonth DATE,
    FirstANCCount INT DEFAULT 0,
    Completed4Visits INT DEFAULT 0,
    Completed8Visits INT DEFAULT 0,
    Gestation12To13 INT DEFAULT 0,
    ANC1Count INT DEFAULT 0,
    ANC5Count INT DEFAULT 0,
    OedemaCount INT DEFAULT 0,
    BleedingCount INT DEFAULT 0,
    CesareanSectionCount INT DEFAULT 0,
    ManualPlacentaRemovalCount INT DEFAULT 0,
    APHOrPPHCount INT DEFAULT 0,
    ForcepsVacuumCount INT DEFAULT 0,
    DateCreated DATETIME DEFAULT GETDATE(),
    DateModified DATETIME,
    PRIMARY KEY (FacilityCode, ReportMonth)
);

CREATE OR ALTER PROCEDURE sp_Update_ANCSummary
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @ReportMonth DATE;
    SET @ReportMonth = DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1);

    ;WITH ClientVisits AS (
        SELECT FacilityCode, ClientID, MAX(VisitID) AS MaxVisit
        FROM ANC
        GROUP BY FacilityCode, ClientID
    ),
    Aggregated AS (
        SELECT 
            a.FacilityCode,
            @ReportMonth AS ReportMonth,
            SUM(CASE WHEN a.IsFirstANC = 1 THEN 1 ELSE 0 END) AS FirstANCCount,
            SUM(CASE WHEN cv.MaxVisit >= 4 THEN 1 ELSE 0 END) AS Completed4Visits,
            SUM(CASE WHEN cv.MaxVisit >= 8 THEN 1 ELSE 0 END) AS Completed8Visits,
            SUM(CASE WHEN a.Gestation BETWEEN 12 AND 13 THEN 1 ELSE 0 END) AS Gestation12To13,
            SUM(CASE WHEN a.VisitID = 1 THEN 1 ELSE 0 END) AS ANC1Count,
            SUM(CASE WHEN a.VisitID = 5 THEN 1 ELSE 0 END) AS ANC5Count,
            SUM(CASE WHEN a.Oedema = 1 THEN 1 ELSE 0 END) AS OedemaCount,
            SUM(CASE WHEN a.Bleeding = 1 THEN 1 ELSE 0 END) AS BleedingCount,
            SUM(CASE WHEN a.CesareanSection = 1 THEN 1 ELSE 0 END) AS CesareanSectionCount,
            SUM(CASE WHEN a.ManualRemovalOfPlacenta = 1 THEN 1 ELSE 0 END) AS ManualPlacentaRemovalCount,
            SUM(CASE WHEN a.APHOrPPH = 1 THEN 1 ELSE 0 END) AS APHOrPPHCount,
            SUM(CASE WHEN a.ForcepsOrVacuumExtraction = 1 THEN 1 ELSE 0 END) AS ForcepsVacuumCount
        FROM ANC a
        INNER JOIN ClientVisits cv ON cv.ClientID = a.ClientID AND cv.FacilityCode = a.FacilityCode
        WHERE a.DateCreated >= @ReportMonth
        GROUP BY a.FacilityCode
    )
    MERGE ANC_Summary AS target
    USING Aggregated AS source
    ON target.FacilityCode = source.FacilityCode AND target.ReportMonth = source.ReportMonth
    WHEN MATCHED THEN 
        UPDATE SET 
            FirstANCCount = source.FirstANCCount,
            Completed4Visits = source.Completed4Visits,
            Completed8Visits = source.Completed8Visits,
            Gestation12To13 = source.Gestation12To13,
            ANC1Count = source.ANC1Count,
            ANC5Count = source.ANC5Count,
            OedemaCount = source.OedemaCount,
            BleedingCount = source.BleedingCount,
            CesareanSectionCount = source.CesareanSectionCount,
            ManualPlacentaRemovalCount = source.ManualPlacentaRemovalCount,
            APHOrPPHCount = source.APHOrPPHCount,
            ForcepsVacuumCount = source.ForcepsVacuumCount,
            DateModified = GETDATE()
    WHEN NOT MATCHED THEN 
        INSERT (
            FacilityCode, ReportMonth, FirstANCCount, Completed4Visits, Completed8Visits,
            Gestation12To13, ANC1Count, ANC5Count, OedemaCount, BleedingCount,
            CesareanSectionCount, ManualPlacentaRemovalCount, APHOrPPHCount, ForcepsVacuumCount, DateCreated
        )
        VALUES (
            source.FacilityCode, source.ReportMonth, source.FirstANCCount, source.Completed4Visits, source.Completed8Visits,
            source.Gestation12To13, source.ANC1Count, source.ANC5Count, source.OedemaCount, source.BleedingCount,
            source.CesareanSectionCount, source.ManualPlacentaRemovalCount, source.APHOrPPHCount, source.ForcepsVacuumCount, GETDATE()
        );
END;
GO
