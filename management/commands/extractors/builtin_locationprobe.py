# pylint: disable=line-too-long

import datetime
import psycopg2
import pytz

CREATE_PROBE_TABLE_SQL = 'CREATE TABLE builtin_locationprobe(id SERIAL PRIMARY KEY, user_id TEXT, guid TEXT, timestamp BIGINT, utc_logged TIMESTAMP, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, altitude DOUBLE PRECISION, accuracy DOUBLE PRECISION, provider TEXT, network_available BOOLEAN, gps_available BOOLEAN, cluster TEXT, bearing DOUBLE PRECISION, speed DOUBLE PRECISION);'
CREATE_PROBE_USER_ID_INDEX = 'CREATE INDEX ON builtin_locationprobe(user_id);'
CREATE_PROBE_GUID_INDEX = 'CREATE INDEX ON builtin_locationprobe(guid);'
CREATE_PROBE_UTC_LOGGED_INDEX = 'CREATE INDEX ON builtin_locationprobe(utc_logged);'


def exists(connection_str, user_id, reading):
    conn = psycopg2.connect(connection_str)

    if probe_table_exists(conn) is False:
        conn.close()
        return False

    cursor = conn.cursor()

    cursor.execute('SELECT id FROM builtin_locationprobe WHERE (user_id = %s AND guid = %s);', (user_id, reading['GUID']))

    row_exists = (cursor.rowcount > 0)

    cursor.close()
    conn.close()

    return row_exists


def probe_table_exists(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT table_name FROM information_schema.tables WHERE (table_schema = \'public\' AND table_name = \'builtin_locationprobe\')')

    table_exists = (cursor.rowcount > 0)

    cursor.close()

    return table_exists


def insert(connection_str, user_id, reading, check_exists=True):
    conn = psycopg2.connect(connection_str)
    cursor = conn.cursor()

    if check_exists and probe_table_exists(conn) is False:
        cursor.execute(CREATE_PROBE_TABLE_SQL)
        cursor.execute(CREATE_PROBE_USER_ID_INDEX)
        cursor.execute(CREATE_PROBE_GUID_INDEX)
        cursor.execute(CREATE_PROBE_UTC_LOGGED_INDEX)

    conn.commit()

    reading_cmd = 'INSERT INTO builtin_locationprobe(user_id, ' + \
                                                   'guid, ' + \
                                                   'timestamp, ' + \
                                                   'utc_logged, ' + \
                                                   'latitude, ' + \
                                                   'longitude, ' + \
                                                   'altitude, ' + \
                                                   'accuracy, ' + \
                                                   'provider, ' + \
                                                   'network_available, ' + \
                                                   'gps_available, ' + \
                                                   'cluster,  ' + \
                                                   'bearing,  ' + \
                                                   'speed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;'

    values = [user_id, reading['GUID'], reading['TIMESTAMP'], datetime.datetime.fromtimestamp(reading['TIMESTAMP'], tz=pytz.utc), reading['LATITUDE'], reading['LONGITUDE']]

    if 'ALTITUDE' in reading:
        values.append(reading['ALTITUDE'])
    else:
        values.append(None)

    values.append(reading['ACCURACY'])
    values.append(reading['PROVIDER'])
    values.append(reading['NETWORK_AVAILABLE'])
    values.append(reading['GPS_AVAILABLE'])

    if 'CLUSTER' in reading:
        values.append(reading['CLUSTER'])
    else:
        values.append(None)

    if 'BEARING' in reading:
        values.append(reading['BEARING'])
    else:
        values.append(None)

    if 'SPEED' in reading:
        values.append(reading['SPEED'])
    else:
        values.append(None)

    cursor.execute(reading_cmd, values)

    conn.commit()

    cursor.close()
    conn.close()
