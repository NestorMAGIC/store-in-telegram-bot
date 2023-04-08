from db import Database 
from config import * 
import time

db = Database()

def main():
    while True:

        orders = db.get_orders_in_proccess()
        if orders:
            for order in orders:
                if not db.get_lifetime_status(order['order_id']):

                    order_data = db.get_order_by_id(order['order_id'])
                    db.item_in_stock(order_data['item_id'])
                    
                    db.delete_order(order['order_id'])
                    print(f"Удален заказ {order['order_id']}")
                    
                time.sleep(1)

        print("Истекших заказов не найдено")

        time.sleep(10)

if __name__ == '__main__':
    main()