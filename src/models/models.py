import argparse
import csv
from dataclasses import dataclass
import datetime
from dateutil.relativedelta import relativedelta
import os
import re
import subprocess
import time
from typing import List

import folium
from folium.plugins import HeatMap
import ipinfo
import pandas as pd
import requests

import settings.config as config
import settings.custom_logger as logger


class BatchError(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


@dataclass
class Ipcheck:
    today: datetime = datetime.date.today()
    CSV = f"ipcheck_{today.strftime('%Y%m%d')}.csv"
    BATCH_MODE: bool = False
    TOKEN = os.environ.get('access_token')

    @classmethod
    def get_args(cls) -> str:
        parser = argparse.ArgumentParser()
        parser.add_argument('-b', help='batch mode', action='store_true')
        parser.add_argument('-f', help='file name to parse', required=True)
        args = parser.parse_args()
        if args.b:
            Ipcheck.BATCH_MODE = True

        return args.f

    @classmethod
    def get_accesslog(cls, filename) -> List:
        process = subprocess.run(
            "cat %s | awk '{print $1}' | sort | uniq -c | sort -nr"
            % (filename),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8'
        )

        if process.stderr != '':
            raise BatchError(f'Error in command: {process.stderr}')

        accesslog = process.stdout
        accesslog = accesslog.split('\n')

        return accesslog

    @classmethod
    def create_csvfile(cls, accesslog: list):
        if accesslog[0] == '':
            raise BatchError(f'No logs to parse')

        with open(Ipcheck.CSV, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Create CSV header
            writer.writerow(['No.',
                             'Count',
                             'IP address',
                             'Region',
                             'Country',
                             'Loc',
                             ])

            row_num = 1
            re_count = re.compile(r'\d{1,}')
            re_ip = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
            for row in accesslog:
                if row == '':
                    break
                count = re_count.search(row)
                ip = re_ip.search(row)
                writer.writerow([row_num,
                                 count.group(),
                                 ip.group(),
                                 'unconfirmed',
                                 'unconfirmed',
                                 'unconfirmed',
                                 ])
                row_num += 1

    @classmethod
    def fetch_ipinfo(cls, csvfile):
        csv_df = pd.read_csv(csvfile)
        iplist = [f'{ip}' for ip in csv_df["IP address"]]
        coords = []

        if Ipcheck.BATCH_MODE is True:
            logger.custom_logging('Batching Requests')
            if Ipcheck.TOKEN is None:
                raise BatchError(f'Token not set: {Ipcheck.TOKEN}')

            handler = ipinfo.getHandler(Ipcheck.TOKEN)
            response = list(handler.getBatchDetails(iplist).values())

            for row in response:
                csv_df.loc[csv_df['IP address'] == row["ip"], ['Region']] = row['region']
                csv_df.loc[csv_df['IP address'] == row["ip"], ['Country']] = row['country']
                csv_df.loc[csv_df['IP address'] == row["ip"], ['Loc']] = row['loc']

                coord = row['loc']
                lat, long = coord.split(',')
                lat, long = float(lat), float(long)
                coords.append([lat, long])

        else:
            for ip in iplist:
                response = requests.get(f'{config.common_setting["url"]}/{ip}')
                response = response.json()

                csv_df.loc[csv_df['IP address'] == ip, ['Region']] = response['region']
                csv_df.loc[csv_df['IP address'] == ip, ['Country']] = response['country']
                csv_df.loc[csv_df['IP address'] == ip, ['Loc']] = response['loc']

                coord = response['loc']
                lat, long = coord.split(',')
                lat, long = float(lat), float(long)
                coords.append([lat, long])

                time.sleep(1)

        # Update CSV file
        csv_df.to_csv(csvfile, index=False)

        return coords

    @classmethod
    def output_heatmap(cls, loc):
        m = folium.Map(location=[36, 140], zoom_start=3)
        HeatMap(data=loc, radius=15,).add_to(m)
        m.save('heatmap.html')

        return
