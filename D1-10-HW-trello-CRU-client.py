# ToDo:
# 1. Добавьте рядом с названием колонки цифру, отражающую количество задач в ней.
# 2. Реализуйте создание колонок.
# 3. Обработайте совпадающие имена задач *
# Как вы думаете, что случится, если у нас появится две задачи с одинаковым именем? Реализуйте обработку такой ситуации. Пользователь должен иметь возможность управлять всеми задачами вне зависимости от того, как он их называет. Сейчас при работе с задачей мы перебираем все задачи и работаем с первой найденной по имени. 
# a) Нужно проверять, имеются ли еще задачи с таким именем и выводить их в консоль. Помимо имени должны быть указаны: колонка, в которой находится эта задача, и другие параметры, по которым можно было бы отличить одну задачу от другой. 
# b) Пользователю должно быть предложено дополнительно ввести (при помощи функции input) номер для выбора задачи из полученного списка. Наш клиент должен работать с выбранной задачей.

import sys
import requests
import datetime as dt
import dateutil.parser as dup
  
# Данные авторизации в API Trello  
auth_params = {    
    'key': "414d13a43ea879c2f26c593e26a2fd3d",    
    'token': "36dfb3c022ef0c912bbcf7b895531a1dfd735efe66f93c6f51f910396fc1a841", 
}  

# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}"

# id доски 'Created with TrelloApi' https://trello.com/b/Fx11R3X9/created-with-trelloapi
# {'id': '5ed3993eb091f30d88e84582', 'name': 'Created with TrelloApi', ...}

board_id = '5ed3993eb091f30d88e84582'

# печать списка задач по колонкам
def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        # печать наименвоания колонки и количества задач в ней      
        print(column['name'], len(task_data))    
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'])  

# создание колонки|list по имени column_name
def list_(column_name):      
    # Получим данные всех колонок на доске, и проверим - есть ли column_name:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    if len( list( filter(lambda c: c['name'] == column_name, column_data) ) ) > 0 :
        print('Список "{}" уже существует!'.format(column_name)) 

    else:
        url = "https://api.trello.com/1/boards/{}/lists"
        requests.post(url.format(board_id), data={'name': column_name, **auth_params})

        print('Список "{}" создан!'.format(column_name)) 

# создание задачи name в колонке column_name
def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке 
            requests.post(base_url.format('cards'), data={'name': name,  'idList': column['id'], **auth_params})      
            break
    print( 'Задача "{n}" добавлена в колонку "{c}"!'.format(n=name, c=column_name) )
    
# перемещение задачи name в колонку column_name
def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Среди задач всех колонок нужно найти все задачи с именем name    
    tasks = []
    task_id = None    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:
                task['column'] = column['name']
                tasks.append(task)    
                
    if len(tasks) == 0:
        print('"{n}" - нет такой задачи!'.format(n = name))
        return
    elif len(tasks) == 1:
        task = tasks[0]
        task_id = task['id']
        ind = tasks.index(task) + 1
    else:
        while True:
            for task in tasks:
                ind = tasks.index(task) + 1
                print( '{i}. \"{t}\" - Список: \"{c}\" LastActivity: {d}'.format( i = ind, t = task['name'], c = task['column'], d = dup.parse(task['dateLastActivity']).strftime("%d.%m.%Y %H:%M:%S") ) )
            ind = int(input('Укажите № задачи: '))
            if ind > 0 and ind <= len(tasks):
                task_id = tasks[ind-1]['id']
                break            

    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break  

    print( 'Задача "{n}" перемещена в колонку "{c}"!'.format(n=name, c=column_name) )

if __name__ == "__main__":
    if len(sys.argv) <= 2: # =='read'     
        read()      
    elif sys.argv[1] == 'list':
        list_(sys.argv[2])
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    