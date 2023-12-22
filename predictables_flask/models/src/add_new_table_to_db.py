def add_new_table_to_db(
    path_to_db: str,
    table_name: str,
    columns: list,
    column_types: list,
    primary_key: str = "id",
    primary_key_type: str = "INTEGER",
):
    """
    Add a new table to an existing SQLite database.

    This function creates a new table in an SQLite database. The table is defined by the provided table name, columns, and column types.
    If the database does not exist, the function will prompt the user to create it first.
    If the table already exists, the function will not create a new one.
    The function will commit the changes and close the connection to the database after creating the table.

    Parameters
    ----------
    path_to_db : str
        The path to the SQLite database file.
    table_name : str
        The name of the table to be created.
    columns : list
        A list of column names for the new table.
    column_types : list
        A list of SQL data types for the new table's columns. Each element in this list corresponds to the column name in the same position in the 'columns' list.
    primary_key : str, optional
        The name of the primary key column for the new table. By default, it is set to 'id'.
    primary_key_type : str, optional
        The SQL data type of the primary key column. By default, it is set to 'INTEGER'.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If there is an error connecting to the database, creating the table, or committing the changes to the database, an exception will be raised and the error message will be printed.

    """
    import os
    import sqlite3

    # Prompt user to confirm that they want to delete the existing database if it exists
    if not os.path.exists(path_to_db):
        print(
            f"Database {path_to_db} does not exist. Please create it first. Run create_new_db() to do so."
        )
        return

    # Connect to the SQLite database. This will create a new file if it doesn't exist.
    try:
        conn = sqlite3.connect(path_to_db)
    except Exception as e:
        print(f"Error connecting to database {path_to_db}: {e}")
        return

    # Create a cursor object
    cursor = conn.cursor()

    # Write a SQL query to create tables
    create_table_query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                                {primary_key} {primary_key_type} PRIMARY KEY
                                {", ".join([f", {columns[i]} {column_types[i]}" for i in range(len(columns))])}
                            );"""

    # Execute the query
    try:
        cursor.execute(create_table_query)
    except Exception as e:
        print(f"Error creating table {table_name}: {e}")
        return

    # Commit the changes and close the connection
    try:
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error committing changes to database {path_to_db}: {e}")
        return

    print(f"Table {table_name} added to database {path_to_db} successfully.")
