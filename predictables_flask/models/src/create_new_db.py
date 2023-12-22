# Initialize the database
def create_new_db(
    path_to_db: str,
    table_name: str,
    columns: list,
    column_types: list,
    primary_key: str = "id",
    primary_key_type: str = "INTEGER",
    drop_existing: bool = False,
):
    """
    Create a new *SQLite* database with a single table.

    This function creates a new SQLite database at the specified path, and adds a single table to it.
    The table is defined by the provided table name, columns, and column types.
    If the database already exists, the function will prompt the user to confirm whether they want to delete it and create a new one.
    If the user confirms, the existing database will be deleted and a new one will be created.
    If the user does not confirm, the function will return without creating a new database.
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
    drop_existing : bool, optional
        A flag indicating whether to automatically drop the existing database if it exists. By default, it is set to False.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If there is an error deleting the existing database, connecting to the new database, creating the table, or committing the changes to the database, an exception will be raised and the error message will be printed.

    """
    import os
    import sqlite3

    # Prompt user to confirm that they want to delete the existing database if it exists
    if os.path.exists(path_to_db):
        try:
            if not drop_existing:
                print(
                    f"Database {path_to_db} already exists, and will have to be deleted to continue."
                )
                if (
                    input(
                        f"Are you sure you want to delete {path_to_db}? (y/n) "
                    ).lower()
                    == "y"
                ):
                    os.remove(path_to_db)
                else:
                    return
            else:
                os.remove(path_to_db)
                print(f"Database {path_to_db} deleted successfully.")
        except Exception as e:
            raise f"Error deleting database {path_to_db}: {e}"

    # Connect to the SQLite database. This will create a new file if it doesn't exist.
    try:
        conn = sqlite3.connect(path_to_db)
    except Exception as e:
        raise f"Error connecting to database {path_to_db}: {e}"

    # Create a cursor object
    cursor = conn.cursor()

    # Write a SQL query to create tables
    create_table_query = f"""CREATE TABLE {table_name} (
                                {primary_key} {primary_key_type} PRIMARY KEY
                                {" ".join([f", {columns[i]} {column_types[i]}" for i in range(len(columns))])}
                            );"""

    # Execute the query
    try:
        cursor.execute(create_table_query)
    except Exception as e:
        raise f"Error creating table {table_name}: {e}"

    # Commit the changes and close the connection
    try:
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error committing changes to database {path_to_db}: {e}")
        return

    print(f"Database {path_to_db} created successfully.")
