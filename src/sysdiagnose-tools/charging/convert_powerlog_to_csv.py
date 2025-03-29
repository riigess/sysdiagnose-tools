import argparse
import csv
import io
import json
import os
import sqlite3 as sqlite
import tarfile


def load_powerlog_from_tarball(tarball_path:str) -> str:
    d = None
    if not tarfile.is_tarfile(tarball_path):
        return None
    tar_fileobj = io.BytesIO()
    tarball_name = tarball_path.split("/")[-1][:-len('.tar.gz')]
    with tarfile.open(name=tarball_path, mode='r') as tar:
        for member in tar.getmembers():
            if f"{tarball_name}/logs/powerlogs/powerlog_" in member.name and ".plsql" in member.name.lower():
                d = tar.extractfile(member).read()
                break
    return d

def setup_and_read_argparse() -> dict:
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--file', '-f', action='store', required=True, help='The sysdiagnose file to parse')

    known_args = argparser.parse_known_args()[0]
    return known_args

def load_plsql_in_memory(plsql) -> sqlite.Connection:
    con = sqlite.connect(":memory:")
    con.deserialize(plsql)
    return con

def query_battery_thermals_from_sqlite(conn:sqlite.Connection) -> list[list[str]]:
    cur = conn.cursor()
    cur.execute("SELECT datetime(timestamp, 'unixepoch', 'localtime'),Level,RawLevel,Voltage,IsCharging,VirtualTemperature,Temperature FROM PLBatteryAgent_EventBackward_Battery;")
    resp = [[i[0] for i in cur.description]] + cur.fetchall()
    return resp

def write_rows_to_csv(rows:list[list[str]]):
    with open(os.environ['HOME'] + '/Desktop/powerlogs.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            spamwriter.writerow(row)

if __name__ == "__main__":
    args_from_parser = setup_and_read_argparse()
    sysdiagnose_filename = args_from_parser.file

    powerlog = load_powerlog_from_tarball(sysdiagnose_filename)
    if powerlog == None:
        raise Error("[ERROR] Could not extract powerlog from tarball. Please ensure this is a sysdiagnose tarball.")

    cnx = load_plsql_in_memory(powerlog)
    responses = query_battery_thermals_from_sqlite(cnx)
    write_rows_to_csv(responses)
