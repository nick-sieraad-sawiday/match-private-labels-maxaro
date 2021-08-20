from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


def start_session(url):
    """Starts session and 'visits' product page

    :param url: The desired url to visit
    :return:
    """
    session = HTMLSession()
    response = session.get(url)

    return response


def get_main_categories(response):

    main_cats = list(response.html.find('.slider-native__items')[0].absolute_links)
    main_categories_urls = [url for url in main_cats]

    return main_categories_urls


def visit_sub_cat(sub_urls):
    max_threads = 30
    threads = min(max_threads, len(sub_urls))

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(get_products, sub_urls)


def get_products(url):
    try:
        # starts session and 'visits' product page
        session = HTMLSession()
        response = session.get(url)
        print(response.status_code, response.url)

        try:
            nr_pages = int(response.html.find('.pagination__link')[-1].text)
        except:
            nr_pages = 1

        print('Nr. of pages:', nr_pages)

        products = response.html.find('.product-tile')
        product_url = [list(url.absolute_links)[0] for url in products]
        if nr_pages == 1:
            all_product_url.extend(product_url)
            print('Products:', len(product_url))
        else:
            temp_all_product_url = []
            temp_all_product_url.extend(product_url)
            print('Products:', len(temp_all_product_url))

            for page in range(nr_pages):
                print('Page:', page + 1, '/', nr_pages)
                if page != nr_pages - 1:
                    page_ = page + 2

                    # goes to the next page
                    # base_url = response.url[:-39]
                    next_page = url + '?p=%s' % page_
                    print(next_page)

                    session = HTMLSession()
                    response = session.get(next_page)

                    products = response.html.find('.product-tile')
                    product_url = [list(url.absolute_links)[0] for url in products]
                    temp_all_product_url.extend(product_url)
                    print('Products:', len(temp_all_product_url))

            all_product_url.extend(temp_all_product_url)

    except Exception as e:
        print(e)


def loop_product_urls(main_categories_urls: list) -> list:
    """Loops through the product pages urls to collect all the product urls.
    run_function_async is called to run the process simultaneously

    :param main_categories_urls: List with all the categories
    :return: (1) List with the urls of all the categories, (2) List with all the product urls
    """

    all_all_product_url = []
    url_count = 0
    for sub in main_categories_urls:
        url_count += 1
        print('url_count:', url_count)
        global all_product_url
        all_product_url = []
        print(sub)
        visit_sub_cat([sub])
        all_all_product_url.append(all_product_url)

    return all_all_product_url


def create_dataframe(main_categories_urls, all_all_product_url):

    product_urls = pd.DataFrame()
    product_urls['main_category_url'] = main_categories_urls
    product_urls['product_url'] = all_all_product_url
    product_urls["main_category"] = [main_cat.split('/')[-2] for main_cat in product_urls["main_category_url"]]
    product_urls = product_urls[["main_category", "main_category_url", "product_url"]]
    product_urls.head()

    # stack 'Product URLs'
    s = product_urls.apply(lambda x: pd.Series(x['product_url']), axis=1).stack().reset_index(level=1, drop=True)
    s.name = 'product_url'
    product_urls = product_urls.drop('product_url', axis=1).join(s)
    product_urls = product_urls.reset_index(drop=True)

    return product_urls


def main():

    response = start_session("https://www.maxaro.nl")
    main_categories_urls = get_main_categories(response)
    all_all_product_url = loop_product_urls(main_categories_urls[:1])
    product_urls = create_dataframe(main_categories_urls[:1], all_all_product_url)

    return product_urls


if __name__ == "__main__":
    main()
