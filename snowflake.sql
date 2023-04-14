-- This is everything I did in Snowflake to get the data into the database
-- Ready to make public
CREATE ROLE MY_READ_ROLE;
CREATE ROLE MY_WRITE_ROLE;
CREATE ROLE MY_DDL_ROLE;
CREATE ROLE MY_DATA_LOAD_ROLE;

create database pets_db;
use database pets_db;
create schema original;
use schema original;

create table pets (
date DATETIME,
pet_name VARCHAR(50),
color VARCHAR(50),
age VARCHAR(50),
primary_breed VARCHAR(50),
seconday_breed VARCHAR(50),
sex VARCHAR(20),
age_in_days DECIMAL(10,1)
);
-- Grant read privileges
GRANT USAGE ON DATABASE pets_db TO ROLE MY_READ_ROLE;
GRANT USAGE ON SCHEMA original TO ROLE MY_READ_ROLE;
GRANT SELECT ON ALL TABLES IN SCHEMA original TO ROLE MY_READ_ROLE;

-- Grant write privileges
GRANT USAGE ON DATABASE pets_db TO ROLE MY_WRITE_ROLE;
GRANT USAGE ON SCHEMA original TO ROLE MY_WRITE_ROLE;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA original TO ROLE MY_WRITE_ROLE;

-- Grant DDL privileges
GRANT ALL PRIVILEGES ON DATABASE pets_db TO ROLE MY_DDL_ROLE;
GRANT ALL PRIVILEGES ON SCHEMA original TO ROLE MY_DDL_ROLE;

-- Grant data loading privileges
GRANT USAGE ON DATABASE pets_db TO ROLE MY_DATA_LOAD_ROLE;
GRANT USAGE ON SCHEMA original TO ROLE MY_DATA_LOAD_ROLE;

GRANT ROLE MY_DATA_LOAD_ROLE TO USER admin;
GRANT ROLE MY_DDL_ROLE TO USER admin;
GRANT ROLE MY_READ_ROLE TO USER admin
GRANT ROLE MY_WRITE_ROLE TO USER admin;

-- Still need to create a stage
-- First we create an azure storage integration
CREATE OR REPLACE STORAGE INTEGRATION azure_storage_integration
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = 'AZURE'
ENABLED = TRUE
AZURE_TENANT_ID = 'tenant_id'
STORAGE_ALLOWED_LOCATIONS = ('storage_account_container');

DESC STORAGE INTEGRATION azure_storage_integration;

CREATE OR REPLACE STAGE azure_stage
URL = 'storage_account_container'
STORAGE_INTEGRATION = azure_storage_integration
FILE_FORMAT = (TYPE = 'CSV', FIELD_DELIMITER=',', SKIP_HEADER=1)
COMMENT = 'bc-pets azure storage container';

LIST '@azure_stage';

-- Stil need to run these commands
GRANT USAGE ON STAGE azure_stage TO ROLE MY_DATA_LOAD_ROLE;
GRANT SELECT ON TABLE pets TO ROLE MY_DATA_LOAD_ROLE;

CREATE NOTIFICATION INTEGRATION azure_pets
ENABLED = TRUE
TYPE = QUEUE
NOTIFICATION_PROVIDER = AZURE_STORAGE_QUEUE
AZURE_STORAGE_QUEUE_PRIMARY_URI = "queue_storage_primary_uri"
AZURE_TENANT_ID = 'tenant_id';

DESC NOTIFICATION INTEGRATION azure_pets;

create or replace pipe pets_db.original.mypipe
  auto_ingest = true
  integration = 'AZURE_PETS'
  as
  copy into pets_db.original.pets
  from @pets_db.original.azure_stage
  file_format = (type = 'CSV', FIELD_DELIMITER=',', SKIP_HEADER=1)
  on_error='CONTINUE';

alter pipe mypipe refresh;

select count(*) from pets;
select * from pets;