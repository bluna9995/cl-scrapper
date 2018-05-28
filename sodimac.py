import traceback
import datetime
import unicodedata
import operator
import csv
import grequests

from bs4 import BeautifulSoup

from resources import URLS


def scrap():
    rs = (grequests.get(u) for u in URLS.get('sillas'))
    items = []

    for response in grequests.map(rs):
        soup = BeautifulSoup(response.content, 'html.parser')

        containers = soup.find_all('div', class_='informationContainer')
        for container in containers:
            try:
                item_name = container.find_all('a')[1].get_text().strip()
                sku = container.find_all(class_='sku')[0].get_text().strip()[4:]
                price = get_price(container.find('b'))
                normal_price = get_normal_price(container.find_all('p', class_='normal-price'), price)

                percent_saving = difference(price, normal_price)
                saving = abs(price - normal_price)

                if percent_saving > 0:
                    items.append({
                        'name': item_name,
                        'sku': sku,
                        'normal': normal_price,
                        'price': price,
                        'saving': saving,
                        'percent': percent_saving,
                        'url': 'http://www.sodimac.cl/sodimac-cl/product/%s/' % (sku.replace('-', ''),)
                    })
            except Exception:
                print(traceback.format_exc())

    items = sorted(items, key=lambda k: k['percent'], reverse=True)
    to_csv(items)


def get_price(element):
    try:
        dirty_price = element.get_text() \
            .strip() \
            .replace("$", "") \
            .replace("C/U", "") \
            .replace("Caja", "") \
            .replace("Display", "") \
            .replace("ML", "") \
            .replace("Juego", "") \
            .replace("DSPL", "") \
            .replace("M2", "") \
            .replace("Pack", "") \
            .replace(".", "") \
            .strip()
        return int(dirty_price)
    except Exception as exception:
        print('No hay precio', exception, element.get_text())


def get_normal_price(elements, default_price):
    try:
        for element in elements:
            dirty_price = element.get_text() \
                .strip() \
                .replace("\n", "") \
                .replace("$", "") \
                .replace(".", "") \
                .replace("Caja", "") \
                .replace("&nbsp;", "") \
                .replace("Juego", "") \
                .replace("M2", "") \
                .replace("C/U", "")
            dirty_price = unicodedata.normalize('NFKD', dirty_price).replace(" ", "")

            if dirty_price.startswith('Ahorro'):
                continue
            elif dirty_price.startswith('Normal'):
                return int(dirty_price[7:])
            else:
                return default_price
        raise Exception('Precio no encontrado')
    except Exception as exception:
        print('Err normal price', exception)
        return default_price


def to_csv(items):
    data = []

    for item in items:
        data.append(
            (
                item['name'],
                item['sku'],
                item['normal'],
                item['price'],
                item['saving'],
                item['percent'],
                item['url'],
            )
        )

    filename = 'savings_{date:%d-%m-%Y_%H-%M-%S}.csv'.format(date=datetime.datetime.now())

    output = open(filename, 'w', newline='')
    out = csv.writer(output, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    out.writerow(['Nombre', 'sku', 'Precio normal', 'Precio Actual', 'Ahorro', '%', 'url'])
    out.writerows(data)
    del out
    output.close()


def print_items(items):
    for item in items:
        if item['normal'] == 1:
            continue

        try:
            percent_saving = difference(item['price'], item['normal'])
            saving = abs(item['price'] - item['normal'])

            if percent_saving > 0:
                print('Nombre: %s / %s' % (item['name'], item['sku']))
                print('Normal: ${:,.0f}'.format(item['normal']))
                print('Actual: ${:,.0f}'.format(item['price']))
                print('Ahorro: ${:,.0f} {}%'.format(saving, percent_saving))
                print()
        except Exception as exception:
            print('Skipping', item, exception)


def difference(value1, value2):
    return abs(int((((value1 - value2) / value2) * 100)))


if __name__ == "__main__":
    scrap()
