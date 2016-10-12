/*CREATE TABLE `app_db`.`apps` (
  `app_id` BIGINT NULL AUTO_INCREMENT,
  `app_name` VARCHAR(45) NULL,
  `pkg_name` VARCHAR(45) NULL UNIQUE,
  `app_score` FLOAT DEFAULT 0,
  PRIMARY KEY (`app_id`));*/
  
/*DELIMITER $$
USE `app_db`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createuser`(
    IN p_name VARCHAR(45),
    IN p_score float,
    OUT p_id bigint(20)
)
BEGIN
    if ( select exists (select 1 from users where user_name = p_name) ) THEN
     
        select user_id into p_id from users where user_name = p_name;
     
    ELSE
     
        insert into users
        (
            user_name,
            user_score
        )
        values
        (
            p_name,
            p_score
        );
     select SCOPE_IDENTITY() into p_id;
    END IF;
END$$
DELIMITER ;*/

DELIMITER $$
USE `app_db`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_userapp`(
    IN u_id bigint,
    IN p_id bigint,
)
BEGIN 
        insert into user_apps
        (
            app_id,
            user_idid
        )
        values
        (
            p_id,
            u_id
        );
END$$
DELIMITER ;