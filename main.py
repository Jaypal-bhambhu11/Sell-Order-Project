import xml.etree.ElementTree as ET
from collections import defaultdict
import time
import bisect
from datetime import datetime
class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.unordered_map_buy={}
        self.unordered_map_sell={}
    # Function to add a new order to the order book
    def add_order(self, order):
        #print('adding order', order['orderId'])
        if order['operation'] == 'BUY':
            #self.buy_orders.append(order)
            
            order_touple = (-order['price'],order['volume'],order['timestamp'],order['orderId'])
            self.unordered_map_buy[order['orderId']]=order_touple
            #self.buy_orders.sort(key=lambda x: (-x['price'], x['timestamp']))  # Sort by price and timestamp
            bisect.insort_left(self.buy_orders, order_touple)
        elif order['operation'] == 'SELL':
            flag=0
            x=[]
            for a in self.buy_orders:

                if(abs(a[0])>=order['price']):
                    b=min(abs(a[1]),order['volume'])
                    c=a
                    self.unordered_map_buy.pop(a[3])
                    #self.buy_orders.remove(a)
                    x.append(a)
                    order_touple = {
                    'price':c[0],
                    'volume': c[1],
                    'timestamp': c[2],
                    'orderId': c[3]
                    } 
                    order_touple['volume']=order_touple['volume']-b
                    order['volume']-=b
                   # if(a[0]==0):
                           # x.append(a)
                    if(order['volume']==0):
                        flag=1
                       # self.unordered_map_sell.pop(b[3])
                        if c[1]!=0:
                            order_toupl=(order_touple['price'],order_touple['volume'],order_touple['timestamp'],order_touple['orderId'])
                            bisect.insort_left(self.buy_orders, order_toupl)
                             # Use the current time as the timestamp
                            self.unordered_map_buy[order_touple['orderId']]=order_toupl
                            break

            #self.buy_orders.sort(key=lambda x: (-x['price'], x['timestamp']))  # Sort by price and timestamp
                            
                        
                    
                else:
                    break
            for j in x:
                self.buy_orders.remove(j)
                #self.unordered_map_buy.pop(j['orderId'])
            if flag==0:
                #self.sell_orders.append(order)
                
                order_touple = (order['price'],order['volume'],order['timestamp'],order['orderId'])
                self.unordered_map_sell[order['orderId']]=order_touple
            #self.buy_orders.sort(key=lambda x: (-x['price'], x['timestamp']))  # Sort by price and timestamp
                bisect.insort_left(self.sell_orders, order_touple)
                #self.sell_orders.sort(key=lambda x: (x['price'], x['timestamp']))# Sort by price and timestamp

    # Function to delete an order from the order book
    def delete_order(self, order_id):
        
            od=self.unordered_map_buy.get(order_id,None)
            if od:
                # order_touple = (od['price'],od['volume'],od['timestamp'],od['orderId'])
                 self.buy_orders.remove(od)
                 self.unordered_map_buy.pop(od[3])
            od=self.unordered_map_sell.get(order_id,None)
            if od:
                 self.sell_orders.remove(od)
                 self.unordered_map_sell.pop(od[3])
#       for order in self.buy_orders:
           # if order['orderId'] == order_id:
           #     self.buy_orders.remove(order)
           #     break
       # for order in self.sell_orders:
       #     if order['orderId'] == order_id:
       #         self.sell_orders.remove(order)
       #         break

def process_orders(xml_file):
    #print("dfkdskfdsa")
    tree = ET.parse(xml_file)
    root = tree.getroot()

    order_books = defaultdict(OrderBook)
    start_time = time.time()
    start_time_formatted = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S.%f')
    print(f"Processing started at: {start_time_formatted}")
    for order in root:
        if order.tag == 'AddOrder':
            order_data = {
                'book': order.get('book'),
                'operation': order.get('operation'),
                'price': float(order.get('price')),
                'volume': int(order.get('volume')),
                'orderId': int(order.get('orderId')),
                'timestamp': time.time()  # Use the current time as the timestamp
            }
            # Process the AddOrder logic here
            order_books[order_data['book']].add_order(order_data)
        elif order.tag == 'DeleteOrder':
            book = order.get('book')
            order_id = int(order.get('orderId'))
            # Process the DeleteOrder logic here
            order_books[book].delete_order(order_id)

    end_time = time.time()
    duration = end_time - start_time

    # Print the order books
    for book, order_book in order_books.items():
        print(f"book: {book}")
        print("    ","Buy","----","Sell","      ")
        print("========================")
        a=min(len(order_book.buy_orders),len(order_book.sell_orders))
        for i in range(a):
            print(order_book.buy_orders[i][1],'@',-order_book.buy_orders[i][0],"--",order_book.sell_orders[i][1],'@',order_book.sell_orders[i][0])
            #print(order['volume'],'@',order['price'])
            #print(f"Price: {order['price']}, Volume: {order['volume']}, OrderID: {order['orderId']}")
        #print("Sell:")
        #for order in order_book.sell_orders:
            #print(order['volume'],'@',order['price'])
            #print(f"Price: {order['price']}, Volume: {order['volume']}, OrderID: {order['orderId']}")
        i=a
        while(i<len(order_book.buy_orders)):
            
            print(order_book.buy_orders[i][1],'@',-order_book.buy_orders[i][0],"--")
            i+=1
        i=a
        while(i<len(order_book.sell_orders)):
            print("            ",order_book.sell_orders[i][1],'@',order_book.sell_orders[i][0])
            i+=1
        print()   
    end_time = time.time()
    end_time_formatted = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S.%f')
    print(f"Processing completed at: {end_time_formatted}")
    print(f"Processing duration: {duration} seconds")

if __name__ == '__main__':
   # print("aadfkjdsafs")
    process_orders('Temp12.xml')