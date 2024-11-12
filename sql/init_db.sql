-- Create the database
CREATE DATABASE IF NOT EXISTS multi_tenant_db;
USE multi_tenant_db;

-- Create the Tenant table
CREATE TABLE tenant (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create the User table
CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    tenant_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenant(id)
);

-- Create the Document table
CREATE TABLE document (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(255) NOT NULL,
    s3_key VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    file_size INT,
    tenant_id INT NOT NULL,
    uploaded_by INT NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP,
    version INT NOT NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenant(id),
    FOREIGN KEY (uploaded_by) REFERENCES user(id)
);

-- Create indexes for better query performance
CREATE INDEX idx_user_tenant_id ON user(tenant_id);
CREATE INDEX idx_document_tenant_id ON document(tenant_id);
CREATE INDEX idx_document_uploaded_by ON document(uploaded_by);
CREATE INDEX idx_document_upload_date ON document(upload_date);

-- Insert sample tenants
INSERT INTO tenant (name) VALUES
('Santosh'),
('Chiju'),
('Max'),
('Vishnu');

-- Insert sample users (Note: In a real application, you'd use securely hashed passwords)
INSERT INTO user (username, email, password_hash, tenant_id) VALUES
('santosh_user', 'santosh@example.com', 'pbkdf2:sha256:150000$aBc123$hashedpassword1', 1),
('chiju_user', 'chiju@example.com', 'pbkdf2:sha256:150000$dEf456$hashedpassword2', 2),
('max_user', 'max@example.com', 'pbkdf2:sha256:150000$gHi789$hashedpassword3', 3),
('vishnu_user', 'vishnu@example.com', 'pbkdf2:sha256:150000$jKl012$hashedpassword4', 4);

-- Insert sample documents
INSERT INTO document (filename, s3_key, file_type, file_size, tenant_id, uploaded_by, version) VALUES
('santosh_doc.pdf', 'Santosh/santosh_doc.pdf', 'pdf', 1024000, 1, 1, 1),
('chiju_image.jpg', 'Chiju/chiju_image.jpg', 'jpg', 2048000, 2, 2, 1),
('max_report.docx', 'Max/max_report.docx', 'docx', 3072000, 3, 3, 1),
('vishnu_presentation.pptx', 'Vishnu/vishnu_presentation.pptx', 'pptx', 4096000, 4, 4, 1);

-- Create a view for easy document retrieval
CREATE VIEW document_view AS
SELECT
    d.id,
    d.filename,
    d.s3_key,
    d.file_type,
    d.file_size,
    d.upload_date,
    d.last_accessed,
    t.name AS tenant_name,
    u.username AS uploaded_by_username
FROM
    document d
JOIN
    tenant t ON d.tenant_id = t.id
JOIN
    user u ON d.uploaded_by = u.id;

-- Create a stored procedure for adding new documents
DELIMITER //
CREATE PROCEDURE add_document(
    IN p_filename VARCHAR(255),
    IN p_s3_key VARCHAR(255),
    IN p_file_type VARCHAR(50),
    IN p_file_size INT,
    IN p_tenant_id INT,
    IN p_uploaded_by INT,
    IN p_version INT
)
BEGIN
    INSERT INTO document (filename, s3_key, file_type, file_size, tenant_id, uploaded_by, version)
    VALUES (p_filename, p_s3_key, p_file_type, p_file_size, p_tenant_id, p_uploaded_by, p_version);
END //
DELIMITER ;
