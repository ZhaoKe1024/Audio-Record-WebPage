USE cough_schema;

-- ALTER TABLE cough_main ADD COLUMN gender tinyint default NULL after filename;
-- ALTER TABLE cough_main ADD COLUMN age smallint DEFAULT NULL after gender;
-- ALTER TABLE cough_main DROP COLUMN issmkoing;
-- ALTER TABLE cough_main ADD COLUMN issmoking tinyint DEFAULT NULL after age;
-- ALTER TABLE cough_main ADD COLUMN ishealth tinyint DEFAULT NULL AFTER filename;
ALTER TABLE cough_main ADD COLUMN disease tinyint DEFAULT NULL AFTER filename;
