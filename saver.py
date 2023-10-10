import json
import csv

def write_json(file_name: str, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=2)

def read_json(file_name: str):
    with open(file_name, 'r') as file:
        return json.load(file)


def write_csv(file_name: str, data):
    with open(file_name, 'w', newline = '', errors='ignore') as file:    
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка', 'Описание', 'Стоимость', 'Тип оплаты'])
        
        for item in data:            
            writer.writerow([item['title'], item['link'], item['description'],
            item['cost'], item['pay_type']])
    

