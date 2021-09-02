# PostgreSQL commands

| command              | action                                     |
|----------------------|--------------------------------------------|
| `\c database_name;`  | Connect to a database
| `\q`                 | To quit the psql |
| `\l`                 | List databases |
| `\dn`                | List schemas |
| `\df`                | List stored procedures and functions |
| `\dv`                | List views |
| `\dt`                | Lists all tables |
| `\dt+`               | List tables with more info |
| `\d+ table_name`     | Get detailed information on a table. |
| `\df+ function_name` | Show a stored procedure or function code: |
| `\x`                 | Show query output in the pretty-format: |  
| `\du`                | List all users: |  

Create a new role:
`CREATE ROLE role_name;`

Create a new role with a username and password:
`CREATE ROLE username NOINHERIT LOGIN PASSWORD password;`

Change role for the current session to the new_role:
`SET ROLE new_role;`

Allow role_1 to set its role as role_2:
`GRANT role_2 TO role_1;`

## Managing databases

Create a new database:
`CREATE DATABASE [IF NOT EXISTS] db_name;`

Delete a database permanently:
`DROP DATABASE [IF EXISTS] db_name;`

## Managing tables

Create a new table or a temporary table
```sql
CREATE [TEMP] TABLE [IF NOT EXISTS] table_name(
   pk SERIAL PRIMARY KEY,
   c1 type(size) NOT NULL,
   c2 type(size) NULL,
   ...
);
```
Add a new column to a table:
```sql
ALTER TABLE table_name 
ADD COLUMN new_column_name TYPE;
```
Drop a column in a table:
```sql
ALTER TABLE table_name 
DROP COLUMN column_name;
```
Rename a column:
```sql
ALTER TABLE table_name 
RENAME column_name 
TO new_column_name;
```
Set or remove a default value for a column:
```sql
ALTER TABLE table_name 
ALTER COLUMN [SET DEFAULT value | DROP DEFAULT]
```
Add a primary key to a table.
```sql
ALTER TABLE table_name 
ADD PRIMARY KEY (column,...);
```
Remove the primary key from a table.
```sql
ALTER TABLE table_name 
DROP CONSTRAINT primary_key_constraint_name;
```
Rename a table.
```sql
ALTER TABLE table_name 
RENAME TO new_table_name;
```
Drop a table and its dependent objects:
```sql
DROP TABLE [IF EXISTS] table_name CASCADE;
```

## Managing views

Create a view:

```sql
CREATE OR REPLACE view_name AS query;
```

Create a recursive view:

```sql
CREATE RECURSIVE VIEW view_name(column_list) AS
SELECT column_list;
```

Create a materialized view:

```sql
CREATE MATERIALIZED VIEW view_name
AS
query
WITH [NO] DATA;
```

Refresh a materialized view:

```sql
REFRESH MATERIALIZED VIEW CONCURRENTLY view_name;
```

Drop a view:

```sql
DROP VIEW [ IF EXISTS ] view_name;
```

Drop a materialized view:

```sql
DROP MATERIALIZED VIEW view_name;
```

Rename a view:

```sql
ALTER VIEW view_name RENAME TO new_name;
```

## Managing indexes

Creating an index with the specified name on a table

```sql
CREATE [UNIQUE] INDEX index_name
ON table (column,...)
```

Removing a specified index from a table

```sql
DROP INDEX index_name;
```

## Querying data from tables

Query all data from a table:

```sql
SELECT * FROM table_name;
Query data from specified columns of all rows in a table:
SELECT column_list
FROM table;
```

Query data and select only unique rows:

```sql
SELECT DISTINCT (column)
FROM table;
```

Query data from a table with a filter:

```sql
SELECT *
FROM table
WHERE condition;
```

Assign an alias to a column in the result set:

```sql
SELECT column_1 AS new_column_1, ...
FROM table;
```

Query data using the LIKE operator:

```sql
SELECT * FROM table_name
WHERE column LIKE '%value%'
```

Query data using the BETWEEN operator:

```sql
SELECT * FROM table_name
WHERE column BETWEEN low AND high;
```

Query data using the IN operator:

```sql
SELECT * FROM table_name
WHERE column IN (value1, value2,...);
```

Constrain the returned rows with the LIMIT clause:

```sql
SELECT * FROM table_name
LIMIT limit OFFSET offset
ORDER BY column_name;
```

Query data from multiple using the inner join, left join, full outer join, cross join and natural join:

```sql
SELECT * 
FROM table1
INNER JOIN table2 ON conditions
SELECT * 
FROM table1
LEFT JOIN table2 ON conditions
SELECT * 
FROM table1
FULL OUTER JOIN table2 ON conditions
SELECT * 
FROM table1
CROSS JOIN table2;
SELECT * 
FROM table1
NATURAL JOIN table2;
Return the number of rows of a table.
SELECT COUNT (*)
FROM table_name;
```

Sort rows in ascending or descending order:

```sql
SELECT select_list
FROM table
ORDER BY column ASC [DESC], column2 ASC [DESC],...;
```

Group rows using GROUP BY clause.

```sql
SELECT *
FROM table
GROUP BY column_1, column_2, ...;
```

Filter groups using the HAVING clause.

```sql
SELECT *
FROM table
GROUP BY column_1
HAVING condition;
Set operations
```

Combine the result set of two or more queries with UNION operator:

```sql
SELECT * FROM table1
UNION
SELECT * FROM table2;
```

Minus a result set using EXCEPT operator:

```sql
SELECT * FROM table1
EXCEPT
SELECT * FROM table2;
```

Get intersection of the result sets of two queries:

```sql
SELECT * FROM table1
INTERSECT
SELECT * FROM table2;
```

## Modifying data

Insert a new row into a table:

```sql
INSERT INTO table(column1,column2,...)
VALUES(value_1,value_2,...);
```

Insert multiple rows into a table:

```sql
INSERT INTO table_name(column1,column2,...)
VALUES(value_1,value_2,...),
      (value_1,value_2,...),
      (value_1,value_2,...)...
```

Update data for all rows:

```sql
UPDATE table_name
SET column_1 = value_1,
    ...;
```

Update data for a set of rows specified by a condition in the WHERE clause.

```sql
UPDATE table
SET column_1 = value_1,
    ...
WHERE condition;
```

Delete all rows of a table:

```sql
DELETE FROM table_name;
```

Delete specific rows based on a condition:

```sql
DELETE FROM table_name
WHERE condition;
```

## Performance

Show the query plan for a query:

```sql
EXPLAIN query;
```

Show and execute the query plan for a query:

```sql
EXPLAIN ANALYZE query;
```

Collect statistics:

```sql
ANALYZE table_name;
```
