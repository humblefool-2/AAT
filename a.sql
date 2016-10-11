CREATE TABLE `app_db`.`apps` (
  `app_id` BIGINT NULL AUTO_INCREMENT,
  `app_name` VARCHAR(45) NULL,
  `pkg_name` VARCHAR(45) NULL UNIQUE,
  `app_score` FLOAT DEFAULT 0,
  PRIMARY KEY (`app_id`));