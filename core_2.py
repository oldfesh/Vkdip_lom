from pprint import pprint
from datetime import datetime
# импорты

import vk_api
from vk_api.exceptions import ApiError
from datetime import date

from config_2 import acces_token


class VKTools:
    def __init__(self, acces_token):
        self.vkapi = vk_api.VkApi(token=acces_token)
        self.offset = 0

    def get_profile_info(self, sender_id:int) -> dict:
        """Получаем информацию об отправителе:
        :sender_id: id начавшего диалог
        :return: {'id': ..., 'name' : ..., 'city': ..., 'age': ..., 'sex': ...}"""
        data =  {'id': sender_id, 'name': "Иван", 'city': 'Ростов', 
                 'age': 26, 'sex': 2}
        try:
            info, = self.vkapi.method('users.get', {'user_ids': sender_id,
                                'fields': ('bdate, city, sex'),})
            data['name'] = f"{info.get('first_name')} {info.get('last_name')}"
            city = info.get('city')
            data['city'] = city.get('title') if city else None
            age = info.get('bdate')
            if age and len(age.split('.')) == 3:
                data['age'] = date.today().year - int(age.split('.')[-1])
            data['sex'] = info.get('sex')
        except ApiError as e:
            print(e.error['error_msg'])
        finally:
            return data
    
    def search_worksheet(self, params: dict) -> None|list:
        """Наинаем поиск подходящих анкет
        :params: словарь содержайщий: 
            :cityт: Москва
            :age: 35
            :sex: 1- Жен, 2-Муж
        :return: [(id,), (id,)] список анке"""
        values = {'count': 5, 'offset': self.offset,
                  'age_from': params['age'] - 3,
                  'age_to': params['age'] + 3,
                  'sex': 1 if params['sex'] == 2 else 2,
                  'hometown': params['city'], 'has_photo': 1,
                  'status': 6, 'is_closed': False,}
        self.offset += 5
        users = self.vkapi.method('users.search', values=values)
        if users.get('items'):
            users = [{'id': user['id'], 
                      'name': f"{user.get('first_name', '')} {user.get('last_name', '')}"} 
                     for user in users['items'] if not user['is_closed']]
            return users

    def get_photos(self, id):
        try:
            photos = self.vkapi.method('photos.get',
                                       {'owner_id': id,
                                        'album_id': 'profile',
                                        'extended': 1
                                        }
                                       )
        except ApiError as e:
            photos = []
            print(f'error = {e}')

        result = [
            {
                'owner_id': item['owner_id'],
                'id': item['id'],
                'likes': item['likes']['count'],
                'comments': item['comments']['count']
            } for item in photos['items']
        ]

        result.sort(key=lambda x: (x['likes'], x['comments']), reverse=True)

        return result[:3]

if __name__ == '__main__':
    user_id = 77176530
    tools = VKTools(acces_token)
    params = tools.get_profile_info(user_id)
    worksheets = tools.search_worksheet(params)
    worksheet = worksheets.pop()
    photos = tools.get_photos(worksheet['id'])
    pprint(params)
