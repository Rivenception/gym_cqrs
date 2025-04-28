-- Create the Write Side Schema
CREATE TABLE machines (
    machine_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(255) NOT NULL,
    model VARCHAR(100) NOT NULL,
    installation_date DATE NOT NULL,
    status ENUM('active', 'maintenance', 'inactive') NOT NULL DEFAULT 'active'
);

INSERT INTO machines (location, model, installation_date, status) VALUES
('Hospital Ward 1', 'BP-Check Pro 100', '2023-01-15', 'active'),
('Hospital Ward 2', 'BP-Check Pro 200', '2023-02-20', 'maintenance'),
('Clinic Downtown', 'HeartRate BP 300', '2023-03-12', 'active'),
('Remote Clinic A', 'Mobile BP 1X', '2023-04-25', 'active'),
('Health Fair', 'Portable BP-2', '2023-05-30', 'inactive'),
('University Health Center', 'BP-Check Pro 100', '2023-06-10', 'active'),
('Community Health Clinic', 'HeartRate BP 300', '2023-07-15', 'maintenance'),
('Nursing Home', 'BP-Advanced 400', '2023-08-05', 'active'),
('Pharmacy Branch 1', 'BP-Check Pro 200', '2023-09-20', 'active'),
('Pharmacy Branch 2', 'Mobile BP 1X', '2023-10-11', 'active');



CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    weight DECIMAL(5,2) -- Assuming weight is in kilograms with two decimal places for precision
);

INSERT INTO patients (first_name, last_name, dob, weight) VALUES
('Alex', 'Johnson', '1985-02-15', 75.5),
('Jamie', 'Smith', '1990-07-24', 65.2),
('Sam', 'Lee', '1975-11-30', 82.3),
('Jordan', 'Diaz', '2003-03-09', 90.1),
('Casey', 'Wong', '1988-05-19', 68.4),
('Taylor', 'Garcia', '1995-01-22', 74.8),
('Morgan', 'Brown', '2000-09-05', 59.0),
('Charlie', 'Miller', '1992-12-17', 83.5),
('Drew', 'Wilson', '1983-08-11', 70.2),
('Pat', 'Davis', '1978-04-26', 76.3);


CREATE TABLE readings (
    reading_id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id INT NOT NULL,
    patient_id INT, -- This can be NULL if machines are not assigned to specific patients.
    systolic_pressure INT NOT NULL,
    diastolic_pressure INT NOT NULL,
    pulse_rate INT NOT NULL,
    reading_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE maintenance_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id INT NOT NULL,
    maintenance_date DATE NOT NULL,
    details TEXT NOT NULL,
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
);


#ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';