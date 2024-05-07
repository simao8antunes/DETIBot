USE Detibot;

-- Creats update_time table
CREATE TABLE IF NOT EXISTS update_time (
    id INT PRIMARY KEY,
    period_date VARCHAR(20),
    update_period VARCHAR(30)
);

-- Creats source table
CREATE TABLE IF NOT EXISTS source (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url_path VARCHAR(255),
    link_paths VARCHAR(255),
    loader_type VARCHAR(255),
    descript VARCHAR(255),
    wait_time INT,
    recursive_url boolean,
    update_period_id INT,
    FOREIGN KEY (update_period_id) REFERENCES update_time (id)
);

-- inserts the predefined rows of update_time
INSERT INTO update_time (id,period_date, update_period) VALUES (1,'Daily', '2024-03-22 00:00:00');
INSERT INTO update_time (id,period_date, update_period) VALUES (2,'Weekly', '2024-03-22 00:00:00');
INSERT INTO update_time (id,period_date, update_period) VALUES (3,'Monthly', '2024-03-22 00:00:00');
INSERT INTO update_time (id,period_date, update_period) VALUES (4,'Quarter', '2024-03-22 00:00:00');


