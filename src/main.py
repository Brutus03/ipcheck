from models.models import BatchError
from models.models import Ipcheck
import settings.config as config
import settings.custom_logger as logger


def main():
    filename = Ipcheck.get_args()
    logger.custom_logging('main start')
    logger.custom_logging(
        f'Analysis target file: {filename}'
        )

    try:
        logger.custom_logging('Start extracting IP address')
        iplist = Ipcheck.get_accesslog(filename)
    except BaseException as e:
        logger.custom_logging(e)
        raise BatchError('[error]Start extracting IP address')

    try:
        logger.custom_logging('Create CSV file')
        Ipcheck.create_csvfile(iplist)
    except BaseException as e:
        logger.custom_logging(e)
        raise BatchError('[error]Create CSV file')

    try:
        logger.custom_logging('IP address research')
        coords = Ipcheck.fetch_ipinfo(Ipcheck.CSV)
    except BaseException as e:
        logger.custom_logging(e)
        raise BatchError('[error]IP address research')

    try:
        logger.custom_logging('Heatmap output')
        Ipcheck.output_heatmap(coords)
    except BaseException as e:
        logger.custom_logging(e)
        raise BatchError('[error]Heatmap output')

    finally:
        logger.custom_logging('main end')


if __name__ == '__main__':
    main()
