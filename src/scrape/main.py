from src.scrape.product_urls import main as run_product_urls
from src.scrape.product_specs import main as run_product_specs


def main():

    product_urls = run_product_urls()
    run_product_specs(product_urls)


if __name__ == '__main__':
    main()
