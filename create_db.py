import csv
import json
import os
import sqlite3
from contextlib import closing, contextmanager
from typing import Callable

from views.views import create_views

DB_FILENAME = "./output/db_neu.sqlite"
MISSIONS_FOLDER_PATH = "./input/missions/"

# Paths to tables in csv format
CATEGORY_PATH = "./input/csvs_for_tables/category.csv"
CAUSE_GROUP_PATH = "./input/csvs_for_tables/cause_group.csv"
ERROR_TYPE_PATH = "./input/csvs_for_tables/error_type.csv"
MISSION_PATH = "./input/csvs_for_tables/mission.csv"
SAMPLE_ORIGINAL_PATH = "./input/csvs_for_tables/sample_original.csv"
SAMPLE_EVALUATION_PATH = "./input/csvs_for_tables/sample_evaluation.csv"

INPUT_FILES: list[str] = []

for item in os.listdir(MISSIONS_FOLDER_PATH):
    INPUT_FILES.insert(0, (MISSIONS_FOLDER_PATH + str(item)))


def check_DB_FILENAME():
    if os.path.exists(DB_FILENAME):
        os.remove(DB_FILENAME)
        print(
            "The old database was deleted and is created from scratch now. This can take 1 to 2 minutes."
        )
    else:
        print(
            "The database is created from scratch now. This can take 1 to 2 minutes."
        )


@contextmanager
def get_db_connection(DB_FILENAME: str):
    conn = sqlite3.connect(DB_FILENAME)
    _ = conn.execute("pragma foreign_keys = on")
    try:
        yield conn
    finally:
        conn.close()


def init_db(conn: sqlite3.Connection):
    """Initialize the database."""
    with closing(conn.cursor()) as cursor:
        _ = cursor.execute(
            """
            DROP TABLE IF EXISTS category
            ;"""
        )
        _ = cursor.execute(
            """
            DROP TABLE IF EXISTS cause_group
            ;"""
        )
        _ = cursor.execute(
            """
            DROP TABLE IF EXISTS error_type
            ;"""
        )
        _ = cursor.execute(
            """
            DROP TABLE IF EXISTS mission
            ;"""
        )
        _ = cursor.execute(
            """
            CREATE TABLE category (
                id integer primary key autoincrement,
                name text not null,
                description text not null
            );"""
        )
        _ = cursor.execute(
            """
            CREATE TABLE cause_group (
                id integer primary key autoincrement,
	            name text not null unique,
                description text not null
            );"""
        )
        _ = cursor.execute(
            """
            CREATE TABLE error_type (
                id integer primary key autoincrement,
                code text not null unique,
	            name text not null,
                cause_group_id integer not null,
                description text not null,
                assessment text,
                FOREIGN KEY (cause_group_id)
                    REFERENCES cause_group (id)
            );"""
        )
        _ = cursor.execute(
            """
            CREATE TABLE mission (
                id integer primary key autoincrement,
                original_id integer not null unique,
                name text not null,
                year integer not null,
                amount_of_categories integer not null,
                amount_validated_by_system integer not null,
                amount_finished_by_herbonauts integer not null,
                amount_herbonauts_involved integer not null
            );"""
        )

        _ = cursor.execute(
            """
            DROP TABLE IF EXISTS sample_evaluation;
            """
        )
        _ = cursor.execute(
            """
            DROP TABLE IF EXISTS specimen;
            """
        )

        _ = cursor.execute(
            """
            CREATE TABLE specimen  (
                id integer primary key autoincrement unique,
                voucher_id text not null,
                mission_id integer not null,
                in_sample boolean not null default false,
                validated_data jsonb,
                raw_data jsonb,
                FOREIGN KEY (mission_id)
                    REFERENCES mission (id)
            );"""
        )

        _ = cursor.execute(
            """
            CREATE TABLE sample_evaluation (
                id integer primary key autoincrement,
                specimen_id integer,
                error_type_id integer not null,
                category_id integer not null,
                discussion_available boolean not null default false,
                notes text,
                FOREIGN KEY (specimen_id)
                    REFERENCES specimen (id),
                FOREIGN KEY (error_type_id)
                    REFERENCES error_type (id),
                FOREIGN KEY (category_id)
                    REFERENCES category (id)
            );"""
        )

        conn.commit()


def in_sample(sample_set: "set[str]") -> Callable[[str], bool]:
    def inner(voucher_id: str) -> bool:
        return voucher_id in sample_set

    return inner


def cast_values(data):
    """cast strings with boolean or null like values to the correct type."""
    for key, value in data.items():
        if value.lower() == "null":
            data[key] = None
        elif value.lower() == "true":
            data[key] = True
        elif value.lower() == "false":
            data[key] = False

    return data


def insert_category_data(conn: sqlite3.Connection, input_file: str):
    with open(input_file, encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";", quotechar='"')
        data = [(row["id"], row["name"], row["description"]) for row in reader]
        with closing(conn.cursor()) as cursor:
            _ = cursor.executemany(
                """
                INSERT INTO category (id, name, description) VALUES (?, ?, ?)
                """,
                data,
            )
        conn.commit()


def insert_cause_group_data(conn: sqlite3.Connection, input_file: str):
    with open(input_file, encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";", quotechar='"')
        data = [(row["id"], row["name"], row["description"]) for row in reader]
        with closing(conn.cursor()) as cursor:
            _ = cursor.executemany(
                """
                INSERT INTO cause_group (id, name, description) VALUES (?, ?, ?)
                """,
                data,
            )
        conn.commit()


def insert_error_type_data(conn: sqlite3.Connection, input_file: str):
    with open(input_file, encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";", quotechar='"')
        data = [
            (
                row["id"],
                row["code"],
                row["name"],
                row["cause_group_id"],
                row["description"],
                row["assessment"],
            )
            for row in reader
        ]
        with closing(conn.cursor()) as cursor:
            _ = cursor.executemany(
                """
                INSERT INTO error_type (id, code, name, cause_group_id, description, assessment) VALUES (?, ?, ?, ?, ?, ?)
                """,
                data,
            )
        conn.commit()


def insert_mission_data(conn: sqlite3.Connection, input_file: str):
    with open(input_file, encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";", quotechar='"')
        data = [
            (
                row["id"],
                row["original_id"],
                row["name"],
                row["year"],
                row["amount_of_categories"],
                row["amount_validated_by_system"],
                row["amount_finished_by_herbonauts"],
                row["amount_herbonauts_involved"],
            )
            for row in reader
        ]
        with closing(conn.cursor()) as cursor:
            _ = cursor.executemany(
                """
                INSERT INTO mission (id, original_id, name, year, amount_of_categories, amount_validated_by_system, amount_finished_by_herbonauts, amount_herbonauts_involved) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                data,
            )
        conn.commit()


def load_sample_set():
    with open(SAMPLE_ORIGINAL_PATH, encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";", quotechar='"')
        return {row["voucher_id"] for row in reader}
        # return {row["voucher_id"].replace(" ", "").strip() for row in reader}


def insert_specimen_data(
    conn: sqlite3.Connection, in_sample: Callable[[str], bool], input_file: str
):
    with open(input_file, encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";", quotechar='"')
        data = [
            (
                row["specimen - code"],
                row["mission - id"],
                in_sample(row["specimen - code"]),
                json.dumps(cast_values(row)),
                None,
            )
            for row in reader
        ]
        with closing(conn.cursor()) as cursor:
            _ = cursor.executemany(
                """
                INSERT INTO specimen (voucher_id, mission_id, in_sample, validated_data, raw_data) VALUES (?, ?, ?, ?, ?)
                """,
                data,
            )
        conn.commit()


def insert_sample_evaluation_data(conn: sqlite3.Connection, input_file: str):
    with open(input_file, encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";", quotechar='"')
        data = [
            (
                row["id"],
                row["voucher_id"],
                row["error_type_id"],
                row["category_id"],
                row["discussion_available"],
                row["notes"],
            )
            for row in reader
        ]

        with closing(conn.cursor()) as cursor:
            _ = cursor.executemany(
                """
                INSERT INTO sample_evaluation (id, specimen_id, error_type_id, category_id, discussion_available, notes) VALUES(?,
                (SELECT id FROM specimen WHERE specimen.voucher_id = ?), ?, ?, ?, ?);""",
                (data),
            )
        conn.commit()


# def main():
#     check_DB_FILENAME()
#     with get_db_connection(DB_FILENAME) as conn:
#         init_db(conn)
#         insert_category_data(conn, CATEGORY_PATH)
#         insert_cause_group_data(conn, CAUSE_GROUP_PATH)
#         insert_error_type_data(conn, ERROR_TYPE_PATH)
#         insert_mission_data(conn, MISSION_PATH)
#         sample_set = load_sample_set()
#         is_in = in_sample(sample_set)
#         for input_file in INPUT_FILES:
#             insert_specimen_data(conn, is_in, input_file)
#         insert_sample_evaluation_data(conn, SAMPLE_EVALUATION_PATH)
#         create_views(conn)
#         print("The database is now ready to explore, you can find it in the output folder.")


# # untoggle this if you ONLY want to create views again, toggle line comment for line 316 to 329
def main():
    with get_db_connection(DB_FILENAME) as conn:
        create_views(conn)
        


if __name__ == "__main__":
    main()
