import random
import math

current_petrol_price = {'АИ-80': 51.8, 'АИ-92': 41.20, 'АИ-95': 44.45, 'АИ-98': 52.05}


def time_converter_to_min(time_str):
    time_lst = time_str.split(':')
    return int(time_lst[0]) * 60 + int(time_lst[1])


def time_converter_to_str(time):
    time = time % (24 * 60)
    min = str(time % 60)
    hour = str(time // 60)
    if len(min) == 1:
        min = '0' + min
    if len(hour) == 1:
        hour = '0' + hour
    return hour + ':' + min


def get_azs_list(f_azs):
    result = []
    for line in f_azs:
        line_lst = line.strip().split(maxsplit=2)
        result.append({'max_queue': int(line_lst[1]), 'queue': [], 'petrol': line_lst[2].split()})
    return result


def get_petrol(azs_list):
    result = {}
    for azs in azs_list:
        for sort in azs['petrol']:
            result[sort] = 0
    return result


def get_clients_dict_by_time(f_clients):
    result = {}
    for line in f_clients:
        line_lst = line.strip().split()
        key = str(time_converter_to_min(line_lst[0]))
        if key in result:
            result[key].append({
                'liters': int(line_lst[1]),
                'sort': line_lst[2],
                'duration': math.ceil(int(line_lst[1]) / 10) + random.randint(-1, 1),
                'start': int(key),
                'arrival': line_lst[0],
            })
        else:
            result[key] = [{
                'liters': int(line_lst[1]),
                'sort': line_lst[2],
                'duration': math.ceil(int(line_lst[1]) / 10) + random.randint(-1, 1),
                'start': int(key),
                'arrival': line_lst[0],
            }]
    return result


def print_state(azs_list):
    for i in range(len(azs_list)):
        print('Автомат №', i + 1, ' Максимальная очередь: ', azs_list[i]['max_queue'],
              ' Марки бензина: ', *[x + ' ' for x in azs_list[i]['petrol']], '--> ', '*' * len(azs_list[i]['queue']), sep='')


if __name__ == '__main__':
    with open('azs.txt', encoding='utf-8') as f_azs, open('input.txt', encoding='utf-8') as f_clients:
        azs_list = get_azs_list(f_azs)
        petrol_capacity = get_petrol(azs_list)
        clients_dict_by_time = get_clients_dict_by_time(f_clients)

    revenue = 0
    for time in range(2 * 24*60):
        # Проверка окончания заправки
        conds = []
        for i in range(len(azs_list)):
            queue = azs_list[i]['queue']
            if queue:
                if time >= queue[0]['start'] + queue[0]['duration']:
                    # Вывод информации
                    print('В', time_converter_to_str(time), 'клиент, прибывший в', queue[0]['arrival'], 'за',
                          queue[0]['sort'], queue[0]['liters'], 'литров, заправил свой автомобиль и покинул АЗС.')

                    revenue += current_petrol_price[queue[0]['sort']] * queue[0]['liters']
                    petrol_capacity[queue[0]['sort']] += queue[0]['liters']
                    azs_list[i]['queue'] = queue[1:]
                    if azs_list[i]['queue']:
                        azs_list[i]['queue'][0]['start'] = time

                    # Вывод информации
                    print_state(azs_list)
            elif time >= 24*60:
                if conds:
                    conds.append(1)
                else:
                    conds = [1]
        if len(conds) == len(azs_list):
            break
                    
        # Добавление новых клиентов
        if str(time) in clients_dict_by_time:
            for x in clients_dict_by_time[str(time)]:
                chosen_azs = None
                queue_for_the_azs = math.inf
                required_sort = x['sort']
                for i in range(len(azs_list)):
                    if (required_sort in azs_list[i]['petrol'] and len(azs_list[i]['queue']) < azs_list[i]['max_queue']
                            and len(azs_list[i]['queue']) < queue_for_the_azs):
                        chosen_azs = i
                        queue_for_the_azs = len(azs_list[i]['queue'])
                if chosen_azs != None:
                    # Вывод информации
                    print('В', time_converter_to_str(time), 'новый клиент:', x['arrival'], x['sort'],
                          x['liters'], 'литров, встал в очередь к автомату №' + str(chosen_azs + 1) + '.')

                    azs_list[chosen_azs]['queue'].append(x)
                    azs_list[chosen_azs]['queue'][-1]['arrival'] = time_converter_to_str(time)

                    # Вывод информации
                    print_state(azs_list)
                else:
                    # Вывод информации
                    print('В', time_converter_to_str(time), 'новый клиент:', x['arrival'], x['sort'],
                          x['liters'], 'литров, не смог заправить автомобиль и покинул АЗС.')
                    print_state(azs_list)

    print()
    print('Выручка за день:', revenue)
    print('Израсходовно бензина:')
    for sort in petrol_capacity:
        print('    ', sort, '-', petrol_capacity[sort], 'л.')
