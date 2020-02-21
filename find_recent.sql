SELECT Sensor, Max(`Time`) FROM demp.PurpleAir
group by Sensor;