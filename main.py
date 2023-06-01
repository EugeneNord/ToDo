# import requests
# import json
# import logging
# import configparser


# class BadIdError(Exception):
#     """
#     Класс для обработки ошибки
#     неверного номера задачи
#     (< 0 или > 25).
#     """

#     def __init__(self, head="BadIdError", message="< 0 или > 25"):
#         Exception.__init__(self, message)
#         self.head = head


# class BadNameError(Exception):
#     """
#     Класс для обработки ошибки
#     неверного наименования задачи
#     (< 3 символов).
#     """

#     def __init__(self, head="BadNameError", message="< 3 символов"):
#         Exception.__init__(self, message)
#         self.head = head


# class BadPriorityError(Exception):
#     """
#     Класс для обработки ошибки
#     неверного приоритета задачи
#     (< 0 или > 100).
#     """

#     def __init__(self, head="BadPriorityError", message="< 0 или > 100"):
#         Exception.__init__(self, message)
#         self.head = head


# class Logger:
#     """Класс для записи информации об ошибках в файл."""

#     def __init__(self):
#         FORMAT = "%(name)s:%(levelname)s:%(asctime)s:%(message)s"
#         logging.basicConfig(
#             filename="ToDo_exc.log",
#             filemode="a",
#             encoding="UTF-8",
#             format=FORMAT,
#         )
#         self.logger = logging.getLogger(__name__)
#         self.logger.setLevel(logging.DEBUG)


# class Config:
#     """Класс для чтения конфигурации."""

#     def __init__(self):
#         self.config = configparser.ConfigParser()
#         self.config.read("config.ini")


# class ToDo:
#     def __init__(self, config: Config):
#         self.my_config = config
#         self.key_names = ["id", "name", "priority"]
#         self.key_widths = [25, 25, 25]
#         self.h_close = {"Connection": "Close"}
#         self.h_content = {"Content-type": "application/json"}

#     def custom_menu(self):
#         """Метод для вывода пользовательского меню."""
#         print(
#             """
#          __________________________________________________
#         |             Программа "ToDo"                     |
#         |    1 - Пользовательское меню.                    |
#         |    2 - Список текущих задач.                     |
#         |    3 - Добавить задачу.                          |
#         |    4 - Изменить задачу.                          |
#         |    5 - Удалить задачу.                           |
#         |    6 - Сортировка по приоритету(возрастание).    |
#         |    7 - Документация.                             |
#         |    0 - Выход.                                    |
#         |__________________________________________________|
#         """
#         )

#     def show_head(self):
#         """Метод для создания шаблона отображения списка."""
#         for name, width in zip(self.key_names, self.key_widths):
#             print(name.ljust(width), end="|")
#         print()

#     def show_empty_list(self):
#         """Метод для отображения пустого списка."""
#         for width in self.key_widths:
#             print(" ".ljust(width), end="|")
#         print()

#     def show_task(self, task):
#         """Метод для отображения задачи из списка."""
#         for name, width in zip(self.key_names, self.key_widths):
#             print(str(task[name]).ljust(width), end="|")
#         print()

#     def show(self, json):
#         self.show_head()
#         if type(json) is list:
#             for task in json:
#                 self.show_task(task)
#         elif type(json) is dict:
#             if json:
#                 self.show_task(json)
#             else:
#                 self.show_empty_list()

#     def show_tasks(self):
#         """Метод для отображения списка текущих задач."""
#         try:
#             reply = requests.get(self.my_config.config["LH"]["adress"])
#         except requests.RequestException:
#             print("Communication error")
#         else:
#             if reply.status_code == requests.codes.ok:
#                 self.show(reply.json())
#             elif reply.status_code == requests.codes.not_found:
#                 print("Resourse not found")
#             else:
#                 print("Server error")

#     def add_task(self):
#         """Метод для добавления новой задачи в список."""
#         self.task_id = int(input("Введите id: "))
#         if self.task_id < 1 or self.task_id > 25:
#             raise BadPriorityError(
#                 self.task_id, "Приоритет д.б. от 1 до 25 включительно."
#             )

#         self.task_name = input("Введите имя задачи: ").upper()
#         if len(self.task_name) < 3 or self.task_name.isspace():
#             raise BadNameError(
#                 self.task_name, "Имя не введено или содержит < 3 символов."
#             )

#         self.task_priority = int(input("Введите приоритет задачи: "))
#         if self.task_priority < 1 or self.task_priority > 100:
#             raise BadPriorityError(
#                 self.task_priority, "Приоритет д.б. от 1 до 100 включительно."
#             )

#         task_to_add = {
#             "id": self.task_id,
#             "name": self.task_name,
#             "priority": self.task_priority,
#         }
#         print(json.dumps(task_to_add))
#         try:
#             reply = requests.post(
#                 self.my_config.config["LH"]["adress"],
#                 headers=self.h_content,
#                 data=json.dumps(task_to_add),
#             )
#             print("reply=" + str(reply.status_code))
#             reply = requests.get(
#                 self.my_config.config["LH"]["adress"], headers=self.h_close
#             )
#         except requests.RequestException:
#             print("Communication error")
#         else:
#             print("Connection=" + reply.headers["Connection"])
#             if reply.status_code == requests.codes.ok:
#                 self.show(reply.json())
#             elif reply.status_code == requests.codes.not_found:
#                 print("Resourse not found")
#             else:
#                 print("Server error")

#     def change_task(self):
#         """Метод для изменения текущей задачи в списке."""
#         self.new_task_id = int(input("Введите id: "))
#         if self.new_task_id < 1 or self.new_task_id > 25:
#             raise BadPriorityError(
#                 self.new_task_id, "Приоритет д.б. от 1 до 25 включительно."
#             )

#         self.new_task_name = input("Введите имя задачи: ").upper()
#         if len(self.new_task_name) < 3 or self.new_task_name.isspace():
#             raise BadNameError(
#                 self.new_task_name, "Имя не введено или содержит < 3 символов."
#             )

#         self.new_task_priority = int(input("Введите приоритет задачи: "))
#         if self.new_task_priority < 1 or self.new_task_priority > 100:
#             raise BadPriorityError(
#                 self.new_task_priority, "Приоритет д.б. от 1 до 100."
#             )

#         new_task = {
#             "id": self.new_task_id,
#             "name": self.new_task_name,
#             "priority": self.new_task_priority,
#         }
#         try:
#             reply = requests.put(
#                 f"{self.my_config.config['LH']['adress']}{self.new_task_id}",
#                 headers=self.h_content,
#                 data=json.dumps(new_task),
#             )
#             print("reply=" + str(reply.status_code))
#             reply = requests.get(
#                 self.my_config.config["LH"]["adress"], headers=self.h_close
#             )
#         except requests.RequestException:
#             print("Communiacation error")
#         else:
#             print("Connection=" + reply.headers["Connection"])
#             if reply.status_code == requests.codes.ok:
#                 self.show(reply.json())
#             elif reply.status_code == requests.codes.not_found:
#                 print("Resourse not found")
#             else:
#                 print("Server error")

#     def delete_task(self):
#         """Метод для удаления задачи из списка."""
#         id_to_delete = int(input("Введите id задачи, которую нужно удалить: "))
#         try:
#             reply = requests.delete(
#                 f'{self.my_config.config["LH"]["adress"]}{id_to_delete}'
#             )
#             print("res=" + str(reply.status_code))
#             reply = requests.get(
#                 self.my_config.config["LH"]["adress"], headers=self.h_close
#             )
#         except requests.RequestException:
#             print("Communication error")
#         else:
#             print("Connection=" + reply.headers["Connection"])
#             if reply.status_code == requests.codes.ok:
#                 self.show(reply.json())
#             elif reply.status_code == requests.codes.not_found:
#                 print("Resourse not found")
#             else:
#                 print("Server error")

#     def priority_sort_ascending(self):
#         """Метод для сортировки задач по приоритету в порядке возрастания."""
#         try:
#             reply = requests.get(self.my_config.config["LH"]["sort"])
#         except requests.RequestException:
#             print("Communiacation error")
#         else:
#             if reply.status_code == requests.codes.ok:
#                 self.show(reply.json())
#             elif reply.status_code == requests.codes.not_found:
#                 print("Resourse not found")
#             else:
#                 print("Server error")

#     def help(self):
#         """Метод для вывода документации."""
#         help(ToDo)

#     def close_connection(self):
#         """Метод для закрытия соединения с сервером."""
#         try:
#             reply = requests.get(
#                 self.my_config.config["LH"]["adress"], headers=self.h_close
#             )
#         except requests.RequestException:
#             print("Communication error")
#         else:
#             print("Connection " + reply.headers["Connection"])


# def main():
#     my_config = Config()
#     todo = ToDo(my_config)
#     log = Logger()
#     todo.custom_menu()

#     condition_number = int(input("Выберите номер операции: "))
#     while condition_number != 0:
#         if condition_number == 1:
#             todo.custom_menu()
#         elif condition_number == 2:
#             todo.show_tasks()
#         elif condition_number == 3:
#             try:
#                 todo.add_task()
#             except BadIdError as error:
#                 log.logger.exception(error)
#             except BadNameError as error:
#                 log.logger.exception(error)
#             except BadPriorityError as error:
#                 log.logger.exception(error)
#         elif condition_number == 4:
#             todo.change_task()
#         elif condition_number == 5:
#             todo.delete_task()
#         elif condition_number == 6:
#             todo.priority_sort_ascending()
#         elif condition_number == 7:
#             todo.help()
#         else:
#             print("Выберите другую операцию.")
#         condition_number = int(input("Выберите номер операции: "))
#     todo.close_connection()


# if __name__ == "__main__":
#     print('Запущена программа "ToDo"')
#     main()
