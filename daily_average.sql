use demp;
create view A1_hourly as
select 
	Sensor,
	date(`Time`) as `Date`,
    hour(`Time`) as `Hour`,
	avg(`PM1.0`) as `PM1.0`, 
	avg( `PM2.5`) as `PM2.5`, 
	avg(`PM10.0`) as `PM10.0`,
	avg(`Internal_Temperature`) as `Temperature`,
    avg(`Humidity`) as `Humidity`, 
    avg(`PM2.5_ATM`) as `PM2.5_ATM`
from PurpleAir
group by Sensor, `Hour`, `Date`;