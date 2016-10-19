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
    IN p_downloads bigint,
    IN p_stars float, 
    IN p_company VARCHAR(100),
    IN  p_category VARCHAR(100),
    OUT p_id bigint                                                                                                                                                                         
)                                                                                                                                                                                           
BEGIN                                                                                                                                                                                       
    if ( select exists (select 1 from apps where pkg_name = p_pkg) ) THEN                                                                                                                   
                                                                                                                                                                                            
        select app_id into p_id from apps where pkg_name = p_pkg;                                                                                                                           
                                                                                                                                                                                            
    ELSE                                                                                                                                                                                    
                                                                                                                                                                                                   
        insert into apps(app_name,pkg_name,app_score,app_downloads,app_star_rating,app_company,app_category) values(p_name,p_pkg,p_score,p_downloads,p_stars,p_company,p_category);                                                             
        select app_id from apps order by app_id desc limit 1 into p_id;                                                                                                                     
    END IF;                                                                                                                                                                                 
END$$                                                                                                                                                                                       
DELIMITER ;*/                                                                                                                                                                                 
                                                                                                                                                                                            
/*DELIMITER $$                                                                                                                                                                              
USE `app_db`$$                                                                                                                                                                              
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_userapp`(                                                                                                                                   
    IN u_id bigint,                                                                                                                                                                         
    IN p_id bigint,
    IN u_rating int,
    IN u_date varchar(100)
)                                                                                                                                                                                           
BEGIN                                                                                                                                                                                       
        insert into user_apps                                                                                                                                                               
        (                                                                                                                                                                                   
            user_id,                                                                                                                                                                        
            app_id,
            user_rating,
            user_review_date
        )                                                                                                                                                                                   
        values                                                                                                                                                                              
        (                                                                                                                                                                                   
            select user_id from users where user_id=u_id,                                                                                                                                   
            select app_id from apps where app_id=p_id                                                                                                                                       
        );                                                                                                                                                                                  
END$$                                                                                                                                                                                       
DELIMITER ; */                                                                                                                                                                                
/*USE `app_db`;                                                                                                                                                                             
DROP procedure IF EXISTS `app_db`.`sp_createuser`;                                                                                                                                          
                                                                                                                                                                                            
DELIMITER $$                                                                                                                                                                                
USE `app_db`$$                                                                                                                                                                              
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createuser`(                                                                                                                                
    IN p_name VARCHAR(45),                                                                                                                                                                  
    IN p_score float, 
    IN p_img_url varchar(500),
    OUT p_id bigint                                                                                                                                                                         
)                                                                                                                                                                                           
BEGIN                                                                                                                                                                                       
    if ( select exists (select 1 from users where user_name = p_name) ) THEN                                                                                                                
                                                                                                                                                                                            
        select user_id into p_id from users where user_name = p_name;                                                                                                                       
                                                                                                                                                                                            
    ELSE                                                                                                                                                                                    
        insert into users(user_name,user_score,user_img_url) values(p_name,p_score,p_img_url);                                                                                                                     
        select user_id from users order by user_id desc limit 1 into p_id;                                                                                                                  
    END IF;                                                                                                                                                                                 
END$$                                                                                                                                                                                       
DELIMITER ;*/
USE `app_db`;                                                                                                                                                                             
DROP procedure IF EXISTS `app_db`.`sp_appstar`;                                                                                                                                          
                                                                                                                                                                                            
DELIMITER $$                                                                                                                                                                                
USE `app_db`$$                                                                                                                                                                              
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_appstar`(                                                                                                                                
    IN p_id bigint(20),                                                                                                                                                                  
    IN s_type int, 
    IN no_users bigint                                                                                                                                                                         
)                                                                                                                                                                                           
BEGIN                                                                                                                                                                                       
                                                                                                                                                                                     
        insert into app_stars(app_id,star_type,no_of_users) values(p_id,s_type,no_users);                                                                                                                     
                                                                                                                                                                                                                                                                                                          
END$$                                                                                                                                                                                       
DELIMITER ;