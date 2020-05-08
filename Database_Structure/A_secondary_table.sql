CREATE TABLE `PA_A_Secondary` (
  `Time` datetime NOT NULL,
  `entry_id` int(11) DEFAULT NULL,
  `0.3um` float DEFAULT NULL,
  `0.5um` float DEFAULT NULL,
  `1.0um` float DEFAULT NULL,
  `2.5um` float DEFAULT NULL,
  `5.0um` float DEFAULT NULL,
  `10.0um` float DEFAULT NULL,
  `PM1.0_ATM` double DEFAULT NULL,
  `PM10_ATM` double DEFAULT NULL,
  `Sensor` varchar(45) NOT NULL,
  UNIQUE KEY `sensor_time` (`Sensor`,`Time`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;