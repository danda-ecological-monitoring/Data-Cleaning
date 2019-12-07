use demp;
load data local infile "C:\\Users\\Hannah Fritsch\\Documents\\DEMP Code\\rohini.csv" 
	into table PurpleAir
	FIELDS TERMINATED BY ','
	LINES TERMINATED BY '\n'
	IGNORE 1 LINES; 
show variables like 'local_infile';