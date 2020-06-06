import sys
import requests  
  
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

def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    print(column_data) # отладка      
      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        print(column['name'])    
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'])  

def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        print(column['name']) # отладка
        if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке 
            print(column['name']) # отладка
            requests.post(base_url.format('cards'), data={'name': name,  'idList': column['id'], **auth_params})      
            break

def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:    
                task_id = task['id']    
                break    
        if task_id:    
            break    
       
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break  

if __name__ == "__main__":
    print(sys.argv, len(sys.argv)) # отладка
    if len(sys.argv) <= 2: # =='read'     
        read()      
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    