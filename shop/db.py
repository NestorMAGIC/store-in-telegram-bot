import pymysql 
from config import *
import time

class Database:

    def __init__(self):

        try:
            self.connection = pymysql.connect (
                host=host,
                port=port,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor,
            )

        except Exception as ex:
            print('Connection refused...')
            print(ex)


    # ДОБАВЛЕНИЕ В БД


    def add_item(self, price, cat, login, password):

        try:
            
            with self.connection.cursor() as cursor:

                query = f"INSERT INTO `items` (price, cat, login, password) VALUES ({price}, '{cat}', '{login}', '{password}');"
                
                cursor.execute(query)
                self.connection.commit()

        except Exception as ex:
            print('Item was not added...')
            print(ex)

    def add_user(self, user_id):

        try:
            
            with self.connection.cursor() as cursor:

                query = f"INSERT INTO `users` (user_id) VALUES ({user_id});"
                
                cursor.execute(query)
                self.connection.commit()

        except Exception as ex:
            print('User was not added...')
            print(ex)
    
    def add_order(self, order_id, user_id, item_id, price, oldprice, status, item_cat, lifetime):

        try:
            
            with self.connection.cursor() as cursor:

                query = f"INSERT INTO `orders` (order_id, user_id, item_id, price, oldprice, status, item_cat, lifetime) VALUES ({order_id}, {user_id}, {item_id}, {price}, {oldprice}, '{status}', '{item_cat}', {lifetime});"
                
                cursor.execute(query)
                self.connection.commit()

        except Exception as ex:
            print('Order was not added...')
            print(ex)  


    # ПОЛУЧЕНИЕ ИЗ БД


    def get_item_by_id(self, id):
            
        with self.connection.cursor() as cursor:

            query = f"SELECT * FROM `items` WHERE `id` = {id};"
                
            cursor.execute(query)
            item = cursor.fetchone()

            return item

    def get_items_by_cat(self, cat):
            
        with self.connection.cursor() as cursor:

            query = f"SELECT * FROM `items` WHERE `cat` = '{cat}' AND `status` = 'in stock';"
                
            cursor.execute(query)
            items = cursor.fetchall()

            return items

    def get_item_by_cat(self, cat):

        with self.connection.cursor() as cursor:

            query = f"SELECT * FROM `items` WHERE `cat` = '{cat}' AND `status` = 'in stock';"
                
            cursor.execute(query)
            item = cursor.fetchone()

            return item

    def get_all_cat(self):

        with self.connection.cursor() as cursor:

            query = f"SELECT * FROM `cat`;"
                
            cursor.execute(query)
            cats = cursor.fetchall()

            return cats

    def get_cat(self, cat):

        with self.connection.cursor() as cursor:

            query = f"SELECT * FROM `cat` WHERE cat = '{cat}';"
                
            cursor.execute(query)
            cat = cursor.fetchone()

            return cat   

    def get_user(self, user_id):
        
        with self.connection.cursor() as cursor:

            query = f"SELECT * FROM `users` WHERE `user_id` = {user_id};"
                
            cursor.execute(query)
            item = cursor.fetchone()

            return bool(item)

    def get_user_by_user_id(self, user_id):
        
        with self.connection.cursor() as cursor:

            query = f"SELECT * FROM `users` WHERE `user_id` = {user_id};"
                
            cursor.execute(query)
            item = cursor.fetchone()

            return item

    def get_order_by_id(self, order_id):
            
        with self.connection.cursor() as cursor:

            query = f"SELECT * FROM `orders` WHERE `order_id` = {order_id};"
                
            cursor.execute(query)
            order = cursor.fetchone()

            return order

    def get_orders_in_proccess(self):
            
        with self.connection.cursor() as cursor:

            query = f"SELECT * FROM `orders` WHERE status = 'in proccess';"
                
            cursor.execute(query)
            orders = cursor.fetchall()

            return orders

    def get_lifetime(self, order_id):
            
        with self.connection.cursor() as cursor:

            query = f"SELECT `lifetime` FROM `orders` WHERE `order_id` = {order_id};"
                
            cursor.execute(query)
            item = cursor.fetchone()

            return item

    def get_lifetime_status(self, order_id):

        with self.connection.cursor() as cursor:

            query = f"SELECT `lifetime` FROM `orders` WHERE `order_id` = {order_id};"
                
            cursor.execute(query)
            lifetime = cursor.fetchone()

            if int(lifetime['lifetime']) > time.time(): 
                return True #Время есть
            else:
                return False # Времени нет

    def get_user_code_status(self, user_id):

        with self.connection.cursor() as cursor:

            query = f"SELECT `code` FROM `users` WHERE `user_id` = {user_id};"
                
            cursor.execute(query)
            code = cursor.fetchone()

            if code['code']: 
                return True 
            else:
                return False 

    def get_codes(self):
            
        with self.connection.cursor() as cursor:

            query = f"SELECT * FROM `codes`;"
                
            cursor.execute(query)
            codes = cursor.fetchall()

            return codes

    def get_code(self, code):
            
        with self.connection.cursor() as cursor:

            query = f"SELECT * FROM `codes` WHERE code = '{code}';"
                
            cursor.execute(query)
            code = cursor.fetchone()

            return code

    # ИЗМЕНЕНИЯ В БД


    def complete_order(self, order_id):

        with self.connection.cursor() as cursor:

            query = f"UPDATE `orders` SET status = 'completed' WHERE order_id = {order_id};"
                
            cursor.execute(query)
            self.connection.commit()

    def set_lifetime(self, order_id, lifetime):

        with self.connection.cursor() as cursor:

            query = f"UPDATE `orders` SET lifetime = {lifetime} WHERE order_id = {order_id};"
                
            cursor.execute(query)
            self.connection.commit()


    def item_in_proccess(self, item_id):

        with self.connection.cursor() as cursor:

            query = f"UPDATE `items` SET status = 'in proccess' WHERE id = {item_id};"
                
            cursor.execute(query)
            self.connection.commit()

    def item_in_stock(self, item_id):

        with self.connection.cursor() as cursor:

            query = f"UPDATE `items` SET status = 'in stock' WHERE id = {item_id};"
                
            cursor.execute(query)
            self.connection.commit()

    def complete_item(self, item_id):

        with self.connection.cursor() as cursor:

            query = f"UPDATE `items` SET status = 'completed' WHERE id = {item_id};"
                
            cursor.execute(query)
            self.connection.commit()

    def set_code(self, user_id, code):

        with self.connection.cursor() as cursor:

            query = f"UPDATE `users` SET code = '{code}' WHERE user_id = {user_id};"
                
            cursor.execute(query)
            self.connection.commit()

    def add_money_code(self, code, money):

        with self.connection.cursor() as cursor:

            query = f"UPDATE `codes` SET money = `money` + {money} WHERE code = '{code}';"
                
            cursor.execute(query)
            self.connection.commit()


    # УДАЛЕНИЕ ИЗ БД   


    def delete_order(self, order_id):

        with self.connection.cursor() as cursor:

            query = f"DELETE FROM `orders` WHERE order_id = {order_id};"
                    
            cursor.execute(query)
            self.connection.commit()