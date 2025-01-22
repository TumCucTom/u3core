# Dump choices

Either use docker which will automatically use the dump or do the below

## Restoring a Database from a MySQL Dump File

## Steps

1. **Log in to MySQL**
   ```bash
   mysql -u [username] -p
   ```

2. **Create the Database (if needed)**
   ```sql
   CREATE DATABASE MLAIDB;
   ```

3. **Import the Dump File**
   Exit MySQL (`exit`) and run:
   ```bash
   mysql -u [username] -p MLAIDB < dump.sql
   ```

4. **Verify the Restoration**
   Log back into MySQL and check:
   ```sql
   USE MLAIDB;
   SHOW TABLES;
   ```

## Notes
- Ensure correct permissions for the dump file.
- If the dump includes `CREATE DATABASE`, skip step 2.
- Adjust MySQL server settings for large files if needed.
