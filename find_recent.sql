use demp;


#selecting the most recent times on each channel
CREATE view TempTime1 AS 
SELECT Sensor, Max(`Time`) as `TimeA1`  FROM PurpleAir group by Sensor;
CREATE view TempTime2 AS 
SELECT Sensor, Max(`Time`) as `TimeA2`  FROM PA_A_Secondary group by Sensor;
CREATE view TempTime3 AS 
SELECT Sensor, Max(`Time`) as `TimeB1`  FROM PA_B_Primary group by Sensor;
CREATE view TempTime4 AS 
SELECT Sensor, Max(`Time`) as `TimeB2`  FROM PA_B_Secondary group by Sensor;

# Joining each of the created tables to RecentEntries
create view RecentEntries as
SELECT TempTime1.Sensor, TimeA1, TimeA2, TimeB1, TimeB2, Least(TimeA1, TimeA2, TimeB1, TimeB2) as Recommended FROM TempTime1 RIGHT JOIN TempTime2
on TempTime1.Sensor = TempTime2.Sensor
Right Join TempTime3
on TempTime1.Sensor = TempTime3.Sensor
Right Join  TempTime4
on TempTime1.Sensor = TempTime4.Sensor;



