from typing import re
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, acces_token
from core import VKTools
from data_store import DataStore


class BotInterface:
    vk_tools = False

    def __init__(self, comunity_token, acces_token):
        self.vk = vk_api.VkApi(token=comunity_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VKTools(acces_token)
        self.params = None
        self.worksheets = []
        self.offset = 0
        self.data = DataStore()

    def message_send(self, user_id, message, attachment=None):
        self.vk.method('messages.send',
                       {'user_id': user_id,
                        'message': message,
                        'attachment': attachment,
                        'random_id': get_random_id()}
                       )
        
    def get_worksheet(self, user_id):
        #делаем запрос в бд
        #если вернулся фолс работаем с ней дальше
        if not self.data.request_id(id(['id']), user_id):
            # делаем запрос в бэк боту - он у себя уже обрабатывает и возвращает ссылку на фотки
            # получаем фото
            return self.vk_tools.get_photos(user_id)
        return self.get_worksheet()

    def event_handler(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()
                if command == 'привет':
                    self.params = self.vk_tools.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'Приветствую тебя {self.params["name"]}')
                elif command == 'поиск':
                    if self.params is None or any(
                            field not in self.params for field in ['age', 'sex', 'city', 'relation']):
                        self.message_send(event.user_id, 'Для поиска нужно указать данные отсутствующие у вас в анкете.')
                        self.params = self.request_missing_data(event.user_id)
                        #print(self.params)
                        if self.params is None:
                            self.message_send(event.user_id, 'Некорректные данные. Повторите попытку.')
                            continue
                    self.message_send(
                        event.user_id, 'Начинаем поиск')
                    flag = True
                    # запускаем вечный цикл
                    while flag: 
                        # если список пуст запускаем новый
                        if not self.worksheets:
                            self.worksheets = self.vk_tools.search_worksheet(self.params)
                            self.offset += 10
                        worksheet = self.worksheets.pop()
                        attach = self.get_worksheet(worksheet['id'])
                        photo_string = ''
                        for photo in attach:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                        # если анкета прошла здесь уже фото
                        if attach:
                            if not self.data.request_id(profile_id = event.user_id, worksheet_id=worksheet['id']):
                                self.data.add_user(profile_id = event.user_id, worksheet_id=worksheet['id']) 
                            break
                    self.message_send(
                                event.user_id,
                                f'имя: {worksheet["name"]} ссылка: vk.com/{worksheet["id"]}', attachment = photo_string
                            ) 
                elif command == 'пока':
                    self.message_send(event.user_id, 'Прощай')
                else :
                    self.message_send(event.user_id, 'Команда не опознана, введите новый запрос')

    def request_missing_data(self, user_id):
        if 'age' not in self.params:
            self.message_send(user_id, 'Введите возраст для поиска:')
            response = self.wait_for_user_response(user_id)
            if response is not None:
                age = int(response)
                self.params['age'] = age

        if 'sex' not in self.params:
            self.message_send(user_id, 'Введите пол для поиска (мужской или женский):')
            response = self.wait_for_user_response(user_id)
            if response is not None:
                sex = 2 if response.lower() == 'женский' else 1
                self.params['sex'] = sex

        if 'city' not in self.params:
            self.message_send(user_id, 'Введите город для поиска:')
            response = self.wait_for_user_response(user_id)
            if response is not None:
                city = response
                self.params['city'] = city

        if 'relation' not in self.params:
            self.message_send(user_id, 'Введите семейное положение для поиска:')
            response = self.wait_for_user_response(user_id)
            if response is not None:
                relation = self.get_relation_code(response)
                self.params['relation'] = relation

        return self.params

    def wait_for_user_response(self, user_id) :
        for event in self.longpoll.listen() :
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == user_id:
                return event.text
        return None

    def get_relation_code(self, relation):
        relation = relation.lower()
        relation_code = None

        if relation == 'не женат' or relation == 'не замужем':
            relation_code = 1
        elif relation == 'встречается' or relation == 'есть друг' or relation == 'есть подруга':
            relation_code = 2
        elif relation == 'помолвлен' or relation == 'помолвлена':
            relation_code = 3
        elif relation == 'женат' or relation == 'замужем':
            relation_code = 4
        elif relation == 'все сложно':
            relation_code = 5
        elif relation == 'в активном поиске':
            relation_code = 6
        elif relation == 'влюблен' or relation == 'влюблена':
            relation_code = 7
        elif relation == 'в гражданском браке':
            relation_code = 8

        return relation_code


if __name__ == '__main__':
    bot_interface = BotInterface(comunity_token, acces_token)
    bot_interface.event_handler()
    eng = BotInterface(comunity_token, acces_token)
    user_id = 77176530
    attach = eng.get_worksheet(user_id=user_id)
    photo_string = ''
    for photo in attach:
        photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
    print(attach)
