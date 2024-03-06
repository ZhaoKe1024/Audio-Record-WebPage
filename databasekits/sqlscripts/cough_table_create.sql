-- CREATE DATABASE cough_schema;
use cough_schema;

DROP TABLE IF EXISTS cough_main;

CREATE TABLE cough_main(
    `id` int NOT NULL AUTO_INCREMENT,
    `filename` varchar(32) NOT NULL,
    PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb3 COMMENT="cough_main";

LOCK TABLES cough_main WRITE;
INSERT INTO TABLE cough_main VALUES (0, "create_then_test_item");

SELECT * FROM cough_main;
