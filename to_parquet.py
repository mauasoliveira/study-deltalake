# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from sqlite3 import connect

import pandas as pd
from rich.console import Console

DATABASE_FOLDER = './databases/'

if __name__ == '__main__':
    console = Console()
    # console.clear()

    parser = ArgumentParser()

    parser.add_argument('database', type=str)
    parser.add_argument('table_name', type=str)

    args = parser.parse_args()

    database = args.database
    table_name = args.table_name

    console.print(f'Processing table [bold]{table_name}[/bold]')

    console.rule('Connecting to database ' + database)

    with connect(DATABASE_FOLDER + database) as db_connection:
        db_connection.text_factory = bytes

        df = pd.read_sql(f'SELECT * FROM {table_name}', db_connection)

        console.print(f'Exprting {df.count()} {table_name} to PARQUET')

        df.to_parquet(path=DATABASE_FOLDER + table_name + '.parquet')

    console.rule('DONE')
