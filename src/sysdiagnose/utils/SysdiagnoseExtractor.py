import argparse
import csv
import io
import json
import os
import sqlite3 as sqlite
import tarfile
from typing import Optional

class SysdiagnoseExtractor:
    def __init__(self, tarball_path:str):
        self.tarball_path = tarball_path

    def load_powerlog_from_tarball(self) -> Optional[bytes]:
        d = None
        if not tarfile.is_tarfile(self.tarball_path):
            return None
        tarball_name = self.tarball_path.split("/")[-1][:-len('.tar.gz')]
        with tarfile.open(name=self.tarball_path, mode='r') as tar:
		    # Slowest part is searching for the right file.. Might provide an option to store this in /tmp
            for member in tar.getmembers():
                if f"{tarball_name}/logs/powerlogs/powerlog_" in member.name and ".plsql" in member.name.lower():
                    d = tar.extractfile(member).read()
                    break
        return d

    def load_plsql_in_memory(self, plsql:bytes) -> sqlite.Connection:
        con = sqlite.connect(":memory:")
        con.deserialize(plsql)
        return con
