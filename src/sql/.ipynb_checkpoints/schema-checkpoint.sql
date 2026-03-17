CREATE TABLE prices (
id INT AUTO_INCREMENT PRIMARY KEY,
date DATE,
crop VARCHAR(50),
market VARCHAR(50),
price_per_kg FLOAT
);

CREATE TABLE demand (
id INT AUTO_INCREMENT PRIMARY KEY,
date DATE,
crop VARCHAR(50),
market VARCHAR(50),
demand INT
);

CREATE TABLE supply (
id INT AUTO_INCREMENT PRIMARY KEY,
date DATE,
farmer_id INT,
crop VARCHAR(50),
quantity_supplied INT
);

CREATE TABLE transport_costs (
id INT AUTO_INCREMENT PRIMARY KEY,
origin VARCHAR(50),
market VARCHAR(50),
cost_per_kg FLOAT,
capacity INT
);

CREATE TABLE sales (
id INT AUTO_INCREMENT PRIMARY KEY,
date DATE,
crop VARCHAR(50),
market VARCHAR(50),
quantity INT,
revenue FLOAT
);