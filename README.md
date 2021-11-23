---
# Environment variables

create .env file and add:
    
    POSTGRES_USER=<your_username>
    POSTGRES_PASSWORD=<your_password>
    POSTGRES_DB='<db_name>'        # (for example 'Vocabylary')
    POSTGRES_HOST='your_postgres_host>'        # (for example 'localhost')
---
# Installation of necessary packages

 To install all the packages activate your virtualenv and run the folloving command in your terminal:

     pip install -r requirements.txt

---
# Creating a database and table

To create DB - type in your terminal:

    createdb -h <your_postgres_host> -p <your_postgres_port> -U <your_username> <db_name>

    # for example: createdb -h localhost -p 5432 -U postgres VocabularyTask

To create a table in your DB - type in your terminal:

    psql -h <your_postgres_host> -p <your_postgres_port> -U <your_username> <db_name> -a -f db/CREATE_TABLE.sql

    # for example: psql -h localhost -p 5432 -U postgres VocabularyTask -a -f db/CREATE_TABLE.sql

