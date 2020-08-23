# Creates a procedure that creates an up to date "Recent Entries" table
#this can be called to see when new data needs to be pulled from
#the reccomended table is the oldest of the "new" data among the channels
#given in database time zone
#reccommend going back at least 24 hours earlier to download data, to account 
# for time zones 
use demp;

Delimiter //
create procedure FindRecentTimes()
begin
#clean things up
drop table if exists TempTime1, TempTime2, TempTime3,TempTime4, RecentEntries;

#selecting the most recent times on each channel
CREATE temporary table TempTime1 as
SELECT Sensor, Max(`Time`) as `TimeA1`  FROM PurpleAir group by Sensor;
CREATE temporary table TempTime2 AS 
SELECT Sensor, Max(`Time`) as `TimeA2`  FROM PA_A_Secondary group by Sensor;
CREATE temporary table TempTime3 AS 
SELECT Sensor, Max(`Time`) as `TimeB1`  FROM PA_B_Primary group by Sensor;
CREATE temporary table TempTime4 AS 
SELECT Sensor, Max(`Time`) as `TimeB2`  FROM PA_B_Secondary group by Sensor;

# Joining each of the created tables to RecentEntries
create temporary table RecentEntries as
SELECT Site_List.ID as Sensor,  Active, TimeA1, TimeA2, TimeB1, TimeB2, Least(TimeA1, TimeA2, TimeB1, TimeB2) as Recommended FROM
Site_List 
LEFT JOIN TempTime1
on Site_List.ID = TempTime1.Sensor
LEFT JOIN TempTime2
on Site_List.ID = TempTime2.Sensor
Left Join TempTime3
on Site_List.ID = TempTime3.Sensor
LEFT Join TempTime4
on Site_List.ID = TempTime4.Sensor;

END //
Delimiter ;


