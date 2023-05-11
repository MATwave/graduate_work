from dataclasses import astuple, fields

from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch


class PostgresSaver:
    '''
        Класс приемника содержимого таблиц SQLite в PostgreSQL
    '''

    def __init__(self, connection: _connection):
        self.connection = connection

    def save_all_data(self, data: dict, page_size: int):
        '''
        Сохраняет всю собранную из SQLite информацию в соответствующие таблицы PostgreSQL.

        Аргументы:
        - data (dict): словарь, содержащий данные для сохранения в таблицы PostgreSQL.
        - page_size (int): количество строк, которые будут сохранены за одну транзакцию.
        '''

        # Создаем курсор для выполнения запросов
        with self.connection.cursor() as cursor:
            # Для каждой таблицы в словаре data выполняем следующие действия
            for table_name, table_data in data.items():
                # Получаем имена полей таблицы
                table_fields = [field.name for field in fields(table_data[0])]
                # Очищаем таблицу
                cursor.execute(f'TRUNCATE content.{table_name} CASCADE; ')
                # Формируем SQL-запрос для вставки данных в таблицу
                query = f"""INSERT INTO content.{table_name} ({','.join(table_fields)})
                            VALUES ({','.join(['%s'] * len(table_fields))})
                            ON CONFLICT DO NOTHING"""
                # Преобразуем объекты моделей в кортежи для передачи в execute_batch
                rows = [astuple(model) for model in table_data]
                # Выполняем массовую вставку данных
                execute_batch(cursor, query, rows, page_size=page_size)

                # Фиксируем транзакцию
                self.connection.commit()
