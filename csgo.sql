CREATE TABLE csgo_matches (
    id INT NOT NULL AUTO_INCREMENT,
    dat DATE NOT NULL,
    t1 VARCHAR(50) NOT NULL,
    t1score INT NOT NULL,
    t1rank DECIMAL(3,2),
    t2 VARCHAR(50) NOT NULL,
    t2score INT NOT NULL,
    t2rank DECIMAL(3,2),
    map VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

LOAD DATA LOCAL INFILE '/home/javi/Documents/VitaIndicium/projects/csgodata/matches.csv'
INTO TABLE csgo_matches
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(@dat, t1, t1score, t1rank, t2, t2score, t2rank, map)
SET dat = STR_TO_DATE(@dat, '%d.%m.%y')
