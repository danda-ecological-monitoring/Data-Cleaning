use demp;
load data local infile "some_csv" 
	IGNORE
    into table PurpleAir
	FIELDS TERMINATED BY ','
	LINES TERMINATED BY '\r'
	IGNORE 1 LINES; 

/* the above creates an empty row at end */
set SQL_SAFE_UPDATES = 0; 
delete from PurpleAir
Where Sensor = '';
set SQL_SAFE_UPDATES = 1; 

show variables like 'local_infile';