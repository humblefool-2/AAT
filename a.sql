/*CREATE TABLE `app_db`.`apps` (
  `app_id` BIGINT NULL AUTO_INCREMENT,
  `app_name` VARCHAR(45) NULL,
  `pkg_name` VARCHAR(45) NULL UNIQUE,
  `app_score` FLOAT DEFAULT 0,
  PRIMARY KEY (`app_id`));*/
/*USE `app_db`;
DROP procedure IF EXISTS `app_db`.`sp_createapp`;

DELIMITER $$
USE `app_db`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createapp`( 
    IN p_name VARCHAR(45),
    IN p_pkg NVARCHAR(45),
    IN p_score float,
    OUT p_id bigint
)
BEGIN
    if ( select exists (select 1 from apps where pkg_name = p_pkg) ) THEN
     
        select app_id into p_id from apps where pkg_name = p_pkg;
     
    ELSE
        
        insert into apps(app_name,pkg_name,app_score) values(p_name,p_pkg,p_score);
        select app_id from apps order by app_id desc limit 1 into p_id;
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
            user_id,
            app_id
        )
        values
        (
            select user_id from users where user_id=u_id,
            select app_id from apps where app_id=p_id
        );
END$$
DELIMITER ;
/*USE `app_db`;
DROP procedure IF EXISTS `app_db`.`sp_createuser`;

DELIMITER $$
USE `app_db`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createuser`( 
    IN p_name VARCHAR(45),
    IN p_score float,
    OUT p_id bigint
)
BEGIN
    if ( select exists (select 1 from users where user_name = p_name) ) THEN
     
        select user_id into p_id from users where user_name = p_name;
     
    ELSE
        insert into users(user_name,user_score) values(p_name,p_score);
        select user_id from users order by user_id desc limit 1 into p_id;
    END IF;
END$$
DELIMITER ;*/
