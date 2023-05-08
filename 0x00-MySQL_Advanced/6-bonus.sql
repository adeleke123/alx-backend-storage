-- Script creates a stored procedure AddBonus that adds a new correction for a student.
-- The procedure takes 3 inputs - user_id, project_name, and score - in the given order.
-- It creates a new project if the project_name doesn't exist in the table,
-- then adds the correction to the corresponding user and project.

DELIMITER //
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
    DECLARE project_id INT;
    SELECT id INTO project_id FROM projects WHERE name = project_name;
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END //
DELIMITER ;
