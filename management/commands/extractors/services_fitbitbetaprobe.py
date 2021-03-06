# pylint: disable=line-too-long, too-many-boolean-expressions

import datetime
import psycopg2
import pytz

CREATE_PROBE_TABLE_SQL = 'CREATE TABLE services_fitbitbetaprobe(id SERIAL PRIMARY KEY, user_id TEXT, guid TEXT, timestamp DOUBLE PRECISION, utc_logged TIMESTAMP);'
CREATE_PROBE_USER_ID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe(user_id);'
CREATE_PROBE_GUID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe(guid);'
CREATE_PROBE_UTC_LOGGED_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe(utc_logged);'

CREATE_HEART_TABLE_SQL = 'CREATE TABLE services_fitbitbetaprobe_heart(id SERIAL PRIMARY KEY, user_id TEXT, reading_id BIGINT, utc_logged TIMESTAMP, sensor_timestamp DOUBLE PRECISION, sensor_timestamp_utc TIMESTAMP, avg_heartrate DOUBLE PRECISION);'
CREATE_HEART_USER_ID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_heart(user_id);'
CREATE_HEART_ID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_heart(reading_id);'
CREATE_HEART_UTC_LOGGED_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_heart(utc_logged);'

CREATE_DISTANCE_TABLE_SQL = 'CREATE TABLE services_fitbitbetaprobe_distance(id SERIAL PRIMARY KEY, user_id TEXT, reading_id BIGINT, utc_logged TIMESTAMP, sensor_timestamp DOUBLE PRECISION, sensor_timestamp_utc TIMESTAMP, distance DOUBLE PRECISION);'
CREATE_DISTANCE_USER_ID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_distance(user_id);'
CREATE_DISTANCE_ID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_distance(reading_id);'
CREATE_DISTANCE_UTC_LOGGED_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_distance(utc_logged);'

CREATE_CALORIES_TABLE_SQL = 'CREATE TABLE services_fitbitbetaprobe_calories(id SERIAL PRIMARY KEY, user_id TEXT, reading_id BIGINT, utc_logged TIMESTAMP, sensor_timestamp DOUBLE PRECISION, sensor_timestamp_utc TIMESTAMP, calories DOUBLE PRECISION);'
CREATE_CALORIES_USER_ID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_calories(user_id);'
CREATE_CALORIES_ID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_calories(reading_id);'
CREATE_CALORIES_UTC_LOGGED_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_calories(utc_logged);'

CREATE_STEPS_TABLE_SQL = 'CREATE TABLE services_fitbitbetaprobe_steps(id SERIAL PRIMARY KEY, user_id TEXT, reading_id BIGINT, utc_logged TIMESTAMP, sensor_timestamp DOUBLE PRECISION, sensor_timestamp_utc TIMESTAMP, steps DOUBLE PRECISION);'
CREATE_STEPS_USER_ID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_steps(user_id);'
CREATE_STEPS_ID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_steps(reading_id);'
CREATE_STEPS_UTC_LOGGED_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_steps(utc_logged);'

CREATE_FLOORS_TABLE_SQL = 'CREATE TABLE services_fitbitbetaprobe_floors(id SERIAL PRIMARY KEY, user_id TEXT, reading_id BIGINT, utc_logged TIMESTAMP, sensor_timestamp DOUBLE PRECISION, sensor_timestamp_utc TIMESTAMP, floors DOUBLE PRECISION);'
CREATE_FLOORS_USER_ID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_floors(user_id);'
CREATE_FLOORS_ID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_floors(reading_id);'
CREATE_FLOORS_UTC_LOGGED_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_floors(utc_logged);'

CREATE_ELEVATION_TABLE_SQL = 'CREATE TABLE services_fitbitbetaprobe_elevation(id SERIAL PRIMARY KEY, user_id TEXT, reading_id BIGINT, utc_logged TIMESTAMP, sensor_timestamp DOUBLE PRECISION, sensor_timestamp_utc TIMESTAMP, elevation DOUBLE PRECISION);'
CREATE_ELEVATION_USER_ID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_elevation(user_id);'
CREATE_ELEVATION_ID_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_elevation(reading_id);'
CREATE_ELEVATION_UTC_LOGGED_INDEX = 'CREATE INDEX ON services_fitbitbetaprobe_elevation(utc_logged);'


def exists(connection_str, user_id, reading):
    conn = psycopg2.connect(connection_str)
    cursor = conn.cursor()

    if probe_table_exists(conn) is False or heart_table_exists(conn) is False or distance_table_exists(conn) is False or calories_table_exists(conn) is False or steps_table_exists(conn) is False or floors_table_exists(conn) is False or elevation_table_exists(conn) is False:
        conn.close()
        return False

    cursor.execute('SELECT id FROM services_fitbitbetaprobe WHERE (user_id = %s AND guid = %s);', (user_id, reading['GUID']))

    row_exists = (cursor.rowcount > 0)

    cursor.close()
    conn.close()

    return row_exists


def probe_table_exists(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT table_name FROM information_schema.tables WHERE (table_schema = \'public\' AND table_name = \'services_fitbitbetaprobe\')')

    table_exists = (cursor.rowcount > 0)

    cursor.close()

    return table_exists


def heart_table_exists(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT table_name FROM information_schema.tables WHERE (table_schema = \'public\' AND table_name = \'services_fitbitbetaprobe_heart\')')

    table_exists = (cursor.rowcount > 0)

    cursor.close()

    return table_exists


def steps_table_exists(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT table_name FROM information_schema.tables WHERE (table_schema = \'public\' AND table_name = \'services_fitbitbetaprobe_steps\')')

    table_exists = (cursor.rowcount > 0)

    cursor.close()

    return table_exists


def distance_table_exists(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT table_name FROM information_schema.tables WHERE (table_schema = \'public\' AND table_name = \'services_fitbitbetaprobe_distance\')')

    table_exists = (cursor.rowcount > 0)

    cursor.close()

    return table_exists


def calories_table_exists(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT table_name FROM information_schema.tables WHERE (table_schema = \'public\' AND table_name = \'services_fitbitbetaprobe_calories\')')

    table_exists = (cursor.rowcount > 0)

    cursor.close()

    return table_exists


def floors_table_exists(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT table_name FROM information_schema.tables WHERE (table_schema = \'public\' AND table_name = \'services_fitbitbetaprobe_floors\')')

    table_exists = (cursor.rowcount > 0)

    cursor.close()

    return table_exists


def elevation_table_exists(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT table_name FROM information_schema.tables WHERE (table_schema = \'public\' AND table_name = \'services_fitbitbetaprobe_elevation\')')

    table_exists = (cursor.rowcount > 0)

    cursor.close()

    return table_exists


def insert(connection_str, user_id, reading, check_exists=True):  # pylint: disable=too-many-branches, too-many-statements
    conn = psycopg2.connect(connection_str)
    cursor = conn.cursor()

    if check_exists and probe_table_exists(conn) is False:
        cursor.execute(CREATE_PROBE_TABLE_SQL)
        cursor.execute(CREATE_PROBE_USER_ID_INDEX)
        cursor.execute(CREATE_PROBE_GUID_INDEX)
        cursor.execute(CREATE_PROBE_UTC_LOGGED_INDEX)

    if check_exists and heart_table_exists(conn) is False:
        cursor.execute(CREATE_HEART_TABLE_SQL)
        cursor.execute(CREATE_HEART_USER_ID_INDEX)
        cursor.execute(CREATE_HEART_ID_INDEX)
        cursor.execute(CREATE_HEART_UTC_LOGGED_INDEX)

    if check_exists and distance_table_exists(conn) is False:
        cursor.execute(CREATE_DISTANCE_TABLE_SQL)
        cursor.execute(CREATE_DISTANCE_USER_ID_INDEX)
        cursor.execute(CREATE_DISTANCE_ID_INDEX)
        cursor.execute(CREATE_DISTANCE_UTC_LOGGED_INDEX)

    if check_exists and calories_table_exists(conn) is False:
        cursor.execute(CREATE_CALORIES_TABLE_SQL)
        cursor.execute(CREATE_CALORIES_USER_ID_INDEX)
        cursor.execute(CREATE_CALORIES_ID_INDEX)
        cursor.execute(CREATE_CALORIES_UTC_LOGGED_INDEX)

    if check_exists and steps_table_exists(conn) is False:
        cursor.execute(CREATE_STEPS_TABLE_SQL)
        cursor.execute(CREATE_STEPS_USER_ID_INDEX)
        cursor.execute(CREATE_STEPS_ID_INDEX)
        cursor.execute(CREATE_STEPS_UTC_LOGGED_INDEX)

    if check_exists and floors_table_exists(conn) is False:
        cursor.execute(CREATE_FLOORS_TABLE_SQL)
        cursor.execute(CREATE_FLOORS_USER_ID_INDEX)
        cursor.execute(CREATE_FLOORS_ID_INDEX)
        cursor.execute(CREATE_FLOORS_UTC_LOGGED_INDEX)

    if check_exists and elevation_table_exists(conn) is False:
        cursor.execute(CREATE_ELEVATION_TABLE_SQL)
        cursor.execute(CREATE_ELEVATION_USER_ID_INDEX)
        cursor.execute(CREATE_ELEVATION_ID_INDEX)
        cursor.execute(CREATE_ELEVATION_UTC_LOGGED_INDEX)

    conn.commit()

    reading_cmd = 'INSERT INTO services_fitbitbetaprobe(user_id, ' + \
                                                       'guid, ' + \
                                                       'timestamp, ' + \
                                                       'utc_logged) VALUES (%s, %s, %s, %s) RETURNING id;'

    cursor.execute(reading_cmd, (user_id,
                                 reading['GUID'],
                                 reading['TIMESTAMP'],
                                 datetime.datetime.fromtimestamp(reading['TIMESTAMP'], tz=pytz.utc)))

    for row in cursor.fetchall():
        reading_id = row[0]

        reading_cursor = conn.cursor()

        if 'DISTANCE' in reading:
            for i in range(0, len(reading['DISTANCE'])):
                value = reading['DISTANCE'][i]
                timestamp = reading['DISTANCE_TIMESTAMPS'][i]

                reading_cmd = 'INSERT INTO services_fitbitbetaprobe_distance(user_id, ' + \
                                                                         'reading_id, ' + \
                                                                         'utc_logged, ' + \
                                                                         'sensor_timestamp, ' + \
                                                                         'sensor_timestamp_utc, ' + \
                                                                         'distance) VALUES (%s, %s, %s, %s, %s, %s);'

                values = [user_id, reading_id, datetime.datetime.fromtimestamp(reading['TIMESTAMP'], tz=pytz.utc), timestamp, datetime.datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc), value]

                reading_cursor.execute(reading_cmd, values)

        if 'CALORIES' in reading:
            for i in range(0, len(reading['CALORIES'])):
                value = reading['CALORIES'][i]
                timestamp = reading['CALORIES_TIMESTAMPS'][i]

                reading_cmd = 'INSERT INTO services_fitbitbetaprobe_calories(user_id, ' + \
                                                                         'reading_id, ' + \
                                                                         'utc_logged, ' + \
                                                                         'sensor_timestamp, ' + \
                                                                         'sensor_timestamp_utc, ' + \
                                                                         'calories) VALUES (%s, %s, %s, %s, %s, %s);'

                values = [user_id, reading_id, datetime.datetime.fromtimestamp(reading['TIMESTAMP'], tz=pytz.utc), timestamp, datetime.datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc), value]

                reading_cursor.execute(reading_cmd, values)

        if 'STEPS' in reading:
            for i in range(0, len(reading['STEPS'])):
                value = reading['STEPS'][i]
                timestamp = reading['STEP_TIMESTAMPS'][i]

                reading_cmd = 'INSERT INTO services_fitbitbetaprobe_steps(user_id, ' + \
                                                                         'reading_id, ' + \
                                                                         'utc_logged, ' + \
                                                                         'sensor_timestamp, ' + \
                                                                         'sensor_timestamp_utc, ' + \
                                                                         'steps) VALUES (%s, %s, %s, %s, %s, %s);'

                values = [user_id, reading_id, datetime.datetime.fromtimestamp(reading['TIMESTAMP'], tz=pytz.utc), timestamp, datetime.datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc), value]

                reading_cursor.execute(reading_cmd, values)

        if 'FLOORS' in reading:
            for i in range(0, len(reading['FLOORS'])):
                value = reading['FLOORS'][i]
                timestamp = reading['FLOORS_TIMESTAMPS'][i]

                reading_cmd = 'INSERT INTO services_fitbitbetaprobe_floors(user_id, ' + \
                                                                         'reading_id, ' + \
                                                                         'utc_logged, ' + \
                                                                         'sensor_timestamp, ' + \
                                                                         'sensor_timestamp_utc, ' + \
                                                                         'floors) VALUES (%s, %s, %s, %s, %s, %s);'

                values = [user_id, reading_id, datetime.datetime.fromtimestamp(reading['TIMESTAMP'], tz=pytz.utc), timestamp, datetime.datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc), value]

                reading_cursor.execute(reading_cmd, values)

        if 'HEART' in reading:
            for i in range(0, len(reading['HEART'])):
                value = reading['HEART'][i]
                timestamp = reading['HEART_TIMESTAMPS'][i]

                reading_cmd = 'INSERT INTO services_fitbitbetaprobe_heart(user_id, ' + \
                                                                         'reading_id, ' + \
                                                                         'utc_logged, ' + \
                                                                         'sensor_timestamp, ' + \
                                                                         'sensor_timestamp_utc, ' + \
                                                                         'avg_heartrate) VALUES (%s, %s, %s, %s, %s, %s);'

                values = [user_id, reading_id, datetime.datetime.fromtimestamp(reading['TIMESTAMP'], tz=pytz.utc), timestamp, datetime.datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc), value]

                reading_cursor.execute(reading_cmd, values)

        if 'ELEVATION' in reading:
            for i in range(0, len(reading['ELEVATION'])):
                value = reading['ELEVATION'][i]
                timestamp = reading['ELEVATION_TIMESTAMPS'][i]

                reading_cmd = 'INSERT INTO services_fitbitbetaprobe_elevation(user_id, ' + \
                                                                         'reading_id, ' + \
                                                                         'utc_logged, ' + \
                                                                         'sensor_timestamp, ' + \
                                                                         'sensor_timestamp_utc, ' + \
                                                                         'elevation) VALUES (%s, %s, %s, %s, %s, %s);'

                values = [user_id, reading_id, datetime.datetime.fromtimestamp(reading['TIMESTAMP'], tz=pytz.utc), timestamp, datetime.datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc), value]

                reading_cursor.execute(reading_cmd, values)

        reading_cursor.close()

    conn.commit()

    cursor.close()
    conn.close()
