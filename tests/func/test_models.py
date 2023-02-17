import pytest

from src.models.models import Ipcheck
import src.settings.custom_logger as logger

test_iplist = ['   1 8.8.8.8', '   1 8.8.4.4', '']
test_coords = [[37.4056, -122.0775], [37.4056, -122.0775]]


def test_ipcheck_normal():
    logger.custom_logging('test start')
    filename = 'testfile'

    logger.custom_logging('Start extracting IP address')
    iplist = Ipcheck.get_accesslog(filename)
    assert iplist == test_iplist

    logger.custom_logging('Create CSV file')
    Ipcheck.create_csvfile(iplist)

    logger.custom_logging('IP address research')
    coords = Ipcheck.fetch_ipinfo(Ipcheck.CSV)
    assert coords == test_coords

    logger.custom_logging('Heatmap output')
    Ipcheck.output_heatmap(coords)
    logger.custom_logging('test end')


def test_ipcheck_batch():
    logger.custom_logging('test start batch mode')
    filename = 'testfile'
    Ipcheck.BATCH_MODE = True

    logger.custom_logging('Start extracting IP address')
    iplist = Ipcheck.get_accesslog(filename)
    assert iplist == test_iplist

    logger.custom_logging('Create CSV file')
    Ipcheck.create_csvfile(iplist)

    logger.custom_logging('IP address research')
    coords = Ipcheck.fetch_ipinfo(Ipcheck.CSV)
    assert coords == test_coords

    logger.custom_logging('Heatmap output')
    Ipcheck.output_heatmap(coords)
    logger.custom_logging('test end')
