import os
import csv
import re
import tabulate


class PriceMachine:

    def __init__(self):
        self.data = []

    def load_prices(self, directory):

        for filename in os.listdir(directory):
            if filename.endswith('.csv') and 'price' in filename.lower():
                with open(os.path.join(directory, filename), 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        for column in row:
                            if re.search(r'(товар|название|наименование|продукт)', column, re.IGNORECASE):
                                product = row[column].strip()
                            elif re.search(r'(розница|цена)', column, re.IGNORECASE):
                                price = float(row[column].replace(',', '.').strip())
                            elif re.search(r'(вес|масса|фасовка)', column, re.IGNORECASE):
                                weight = float(row[column].replace(',', '.').strip())
                        if product:
                            self.data.append([filename, product, price, weight, round(price / weight, 2)])

    def export_to_html(self, sorted_result):

        result = '''
                <!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8">
                <title>Позиции продуктов</title>
                </head>
                <body>
                <table>
                    <tr>
                        <th>Номер</th>
                        <th>Название</th>
                        <th>Цена</th>
                        <th>Фасовка</th>
                        <th>Файл</th>
                        <th>Цена за кг.</th>
                    </tr>
                '''
        index = 0
        for i in sorted_result:
            index += 1
            result += f'''
                <tr>
                    <td>{index}</td> 
                            <td>{i[1]}</td> 
                            <td>{i[2]}</td>
                            <td>{i[3]}{' кг'}</td>
                            <td>{i[0]}</td>
                            <td>{i[4]}</td>                        
                        </tr>
                    '''
        result += '''
        </table>
        </body>
        </html>
        '''
        with open('Out data.html', 'w', encoding='utf8') as file:
            file.write(result)

        headers = ['№', 'Наименование', 'Цена', 'Вес', 'Цена\кг.', 'Файл']
        results_num = [[i + 1] + res[1:] + [res[0]] for i, res in enumerate(sorted_result)]
        print(tabulate.tabulate(results_num, headers=headers, tablefmt='simple'))

    def search_engine(self, input_text):

        results = []
        for row in self.data:
            if re.search(input_text, row[1], re.IGNORECASE):
                results.append(row)
        sorted_results = sorted(results, key=lambda x: x[4])
        self.export_to_html(sorted_results)

    def user_input(self, file_path, param=None):

        self.load_prices(file_path)

        while True:
            find_text_value = input('Поиск (или "выход") ?: \n')
            if find_text_value.lower() == 'exit' or find_text_value.lower() == 'выход':
                print('Поиск завершен')
                break
            self.search_engine(find_text_value)


if __name__ == '__main__':
    pm = PriceMachine()
    local_directory = os.path.dirname(os.path.abspath(__file__))
    pm.user_input(local_directory)
