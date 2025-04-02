from random import SystemRandom
import argparse
import csv
import io
import json
import os
import sqlite3 as sqlite
import sys
import tarfile
from typing import Optional

if __name__ != "__main__":
    from sysdiagnose.utils.SysdiagnoseExtractor import SysdiagnoseExtractor
    from sysdiagnose.utils.WriteToCSV import WriteToCSV

class Powerlog:
    def query_battery_thermals_from_sqlite(self, conn:sqlite.Connection) -> list[list[str]]:
        cur = conn.cursor()
        cur.execute("SELECT datetime(timestamp, 'unixepoch', 'localtime'),Level,RawLevel,Voltage,IsCharging,VirtualTemperature,Temperature FROM PLBatteryAgent_EventBackward_Battery;")
        resp = [[i[0] for i in cur.description]] + cur.fetchall()
        return resp

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    from sysdiagnose.utils.SysdiagnoseExtractor import SysdiagnoseExtractor
    from sysdiagnose.utils.WriteToCSV import WriteToCSV

    def setup_and_read_argparse() -> argparse.Namespace:
        argparser = argparse.ArgumentParser()
        argparser.add_argument('--file', '-f', action='store', required=True, help='The sysdiagnose file to parse')
        known_args = argparser.parse_known_args()[0]
        return known_args

    args_from_parser = setup_and_read_argparse()
    sysdiagnose_filename = args_from_parser.file

    # powerlog = load_powerlog_from_tarball(sysdiagnose_filename)
    sde = SysdiagnoseExtractor(tarball_path=sysdiagnose_filename)
    powerlog = sde.load_powerlog_from_tarball()
    if powerlog == None:
        raise Error("[ERROR] Could not extract powerlog from tarball. Please ensure this is a sysdiagnose tarball.")

    cnx = sde.load_plsql_in_memory(plsql=powerlog)
    pl = Powerlog()
    responses = pl.query_battery_thermals_from_sqlite(cnx)
    wcsv = WriteToCSV()
    wcsv.write_rows_to_csv(rows=responses)
