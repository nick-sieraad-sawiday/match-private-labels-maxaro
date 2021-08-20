import logging

from src.scrape.main import main as run_scrape
from src.match.main import main as run_match


def create_logger() -> logging.Logger:
    """Creates a logger to track the process

    :return: logger
    """

    logger = logging.getLogger("logging_tryout2")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def main():
    """Main function
    Runs up-sell

    Runs:
        - run_scrape
        - run_main
    """

    logger = create_logger()

    logger.info('start preprocessing')
    run_scrape()

    logger.info('start modelling')
    run_main()

    logger.info('matching complete')


if __name__ == '__main__':
    main()




