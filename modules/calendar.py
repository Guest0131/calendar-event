from modules.constants import *

import json

class Calendar:

    def __init__(self, login):
        self.login = login

        file = open(USERS_FILE, 'r', encoding='utf-8') 
        users_dict = json.loads(file.read())
        file.close()

        self.name = users_dict[login]['fullname']

    def add_event(self, form_data):
        data_dict = self.get_data_dict()
        
        data_dict[self.login].append({
            'start' : {
                'year'   : int(form_data['start[year]']),
                'month'  : int(form_data['start[month]']),
                'day'    : int(form_data['start[day]']),
                'hour'   : int(form_data['start[hour]']),
                'minute' : int(form_data['start[minute]'])
            },
            'end' : {
                'year'   : int(form_data['end[year]']),
                'month'  : int(form_data['end[month]']),
                'day'    : int(form_data['end[day]']),
                'hour'   : int(form_data['end[hour]']),
                'minute' : int(form_data['end[minute]'])
            },
            'title' : form_data['title'] if 'title' in form_data else '',
            'description' : form_data['description'] if 'description' in form_data else '',
            'color' : form_data['color'] if 'color' in form_data else '#5ac8fa'
        })
        
        self.update_file(data_dict)
            

    def update_file(self, data):
        file = open(DATA_FILE, 'w', encoding='utf-8') 
        file.write(json.dumps(data, ensure_ascii=False))
        file.close()

    def get_data_dict(self):
        file = open(DATA_FILE, 'r', encoding='utf-8') 
        data = json.loads(file.read())
        file.close()

        if self.login not in data:
            data[self.login] = []
            self.update_file(data)

        return data

    def update_event(self, form_data):
        data_dict = self.get_data_dict()
        data_dict[self.login][int(form_data['id']) - 1] = {
            'start' : {
                'year'   : int(form_data['start[year]']),
                'month'  : int(form_data['start[month]']),
                'day'    : int(form_data['start[day]']),
                'hour'   : int(form_data['start[hour]']),
                'minute' : int(form_data['start[minute]'])
            },
            'end' : {
                'year'   : int(form_data['end[year]']),
                'month'  : int(form_data['end[month]']),
                'day'    : int(form_data['end[day]']),
                'hour'   : int(form_data['end[hour]']),
                'minute' : int(form_data['end[minute]'])
            },
            'title' : form_data['title'] if 'title' in form_data else '',
            'description' : form_data['description'] if 'description' in form_data else '',
            'color' : form_data['color'] if 'color' in form_data else '#5ac8fa'
        }
        self.update_file(data_dict)


    def deleteEvent(self, form_data):
        data_dict = self.get_data_dict()
        data_dict[self.login].pop(int(form_data['id']) - 1)
        self.update_file(data_dict)