import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from invokes import invoke_http

from datetime import datetime
import json

#import simplejson as json
from decimal import Decimal


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("inventory_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Inventory(db.Model):
    tablename = 'inventory'

    Item_Id = db.Column(db.Integer, primary_key=True)
    Quantity = db.Column(db.Integer, nullable=False)
    Details = db.Column(db.String)
    Item_Name = db.Column(db.String)
    Expiry_Date = db.Column(db.DateTime, nullable=False)
    Price = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, Item_Id, Quantity, Details, Item_Name, Expiry_Date,Price):
        self.Item_Id = Item_Id
        self.Quantity = Quantity
        self.Details = Details
        self.Item_Name = Item_Name
        self.Expiry_Date = Expiry_Date
        self.Price = Price
        

    def json(self):
        return {"Item_Id": self.Item_Id, "Quantity": self.Quantity, "Details": self.Details, "Item_Name": self.Item_Name, "Expiry_Date": self.Expiry_Date, "Price": self.Price}



@app.route("/inventory")
def get_alls():
    Inventorylist = Inventory.query.all()
    if len(Inventorylist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "inventory": [Inventory.json() for Inventory in Inventorylist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no orders."
        }
    ), 404


@app.route("/inventory/<string:Items_ID>")
def find_by_order_id(Item_Id):
    inventory = Inventory.query.filter_by(Item_Id=Item_Id).first()
    if inventory:
        return jsonify(
            {
                "code": 200,
                "data": inventory.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "Item_Id": Item_Id
            },
            "message": "Order not found."
        }
    ), 404





@app.route("/update_inventory", methods=['POST'])
def update_inventory():
    # customer_id = request.json.get('customer_id', None)
    # order = Order(customer_id=customer_id, status='NEW')
    
    cart_item = request.json.get('cart_item')
    data = []
    for item in cart_item:
        Item_Id=item['Item_Id']
        inventory = Inventory.query.filter_by(Item_Id=Item_Id ).first()

        
         
    
        new_quantity = inventory.Quantity - item['quantity']
        inventory.Quantity = new_quantity 
        print(inventory.json())
        data.append(inventory.json())
       
        # db.session.commit()
        # order.order_item.append(Order_Item(
        #     book_id=item['book_id'], quantity=item['quantity']))
        
    #json.dumps(inventory.json(), use_decimal=True)
        
        


    try:
        # db.session.add(order)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": data
        }
    ), 201






@app.route("/backendInventoryManagement")
def get_all():
    Inventorylist = Inventory.query.all()
    if len(Inventorylist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "inventory": [Inventory.json() for Inventory in Inventorylist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no bouquets."
        }
    ), 404

@app.route("/backendInventoryManagement/<string:Item_Id>")
def find_by_Item_Id(Item_Id):
    inventory = Inventory.query.filter_by(Item_Id=Item_Id).first()
    if inventory:
        return jsonify(
            {
                "code": 200,
                "data": inventory.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Bouquet not found."
        }
    ), 404

# app.route default uses GET method, so other method need to declare
@app.route("/backendInventoryManagement/<string:Item_Id>", methods=['POST'])


# Create bouquet
def create_bouquet(Item_Id):
    if (Inventory.query.filter_by(Item_Id=Item_Id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "Item_Id": Item_Id
                },
                "message": "Bouquet already exists."
            }
        ), 400
        
    data = request.get_json()
    newBouquet = Inventory(Item_Id, **data)
    
    try:
        db.session.add(newBouquet)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "Item_Id": Item_Id
                },
                "message": "An error occurred creating the bouquet."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": newBouquet.json()
        }
    ), 201
    
    
# @app.route("/update_inventory", methods=['POST'])
# def update_inventory():
#     # customer_id = request.json.get('customer_id', None)
#     # order = Order(customer_id=customer_id, status='NEW')

#     cart_item = request.json.get('cart_item')
#     for item in cart_item:
#         Item_Id=item['Item_Id']
#         inventory = Inventory.query.filter_by(Item_Id=Item_Id ).first()
    
#         new_quantity = inventory.Quantity - item['quantity']
#         inventory.Quantity = new_quantity 
#         # db.session.commit()
#         # order.order_item.append(Order_Item(
#         #     book_id=item['book_id'], quantity=item['quantity']))


#     try:
#         # db.session.add(order)
#         db.session.commit()
#     except Exception as e:
#         return jsonify(
#             {
#                 "code": 500,
#                 "message": "An error occurred while creating the order. " + str(e)
#             }
#         ), 500

#     return jsonify(
#         {
#             "code": 201,
#             "data": inventory.json(),
#             "message": "Inventory has been updated per customer order"
#         }
#     ), 201


@app.route("/backendInventoryManagement/<string:Item_Id>", methods=['PUT'])
def update_bouquet(Item_Id):
    bouquet = Inventory.query.filter_by(Item_Id=Item_Id).first()
    if bouquet:
        data = request.get_json()
        # if data['Item_Id']:
        #     bouquet.Item_Id = data['Item_Id']
        if data['Item_Name']:
            bouquet.Item_Name = data['Item_Name']
        if data['Quantity']:
            bouquet.Quantity = data['Quantity'] 
        if data['Price']:
            bouquet.Price = data['Price'] 
        if data['Details']:
            bouquet.Details = data['Details'] 
        if data['Expiry_Date']:
            bouquet.Expiry_Date = data['Expiry_Date'] 
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": bouquet.json(),
                "message" : "Admin has updated specific bouquet details"
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "Item_Id": Item_Id
            },
            "message": "Bouquet not found."
        }
    ), 404

@app.route("/backendInventoryManagement/<int:Item_Id>", methods=['DELETE'])
def delete_bouquet(Item_Id):
    bouquet = Inventory.query.filter_by(Item_Id=Item_Id).first()
    if bouquet:
        db.session.delete(bouquet)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Item_Id": Item_Id
                },
                "message":"Admin has deleted specific bouquet from database"
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "Item_Id": Item_Id
            },
            "message": "Bouquet not found."
        }
    ), 404


# @app.route("/inventory/<string:Items_ID>", methods=['PUT'])
# def update_inventory(Items_ID):
#     try:
#         Items = Inventory.query.filter_by(Items_ID=Items_ID).first()
#         if not Items:
#             return jsonify(
#                 {
#                     "code": 404,
#                     "data": {
#                         "Items_ID": Items_ID
#                     },
#                     "message": "Order not found."
#                 }
#             ), 404

#         # update status
#         data = request.get_json()
#         if data['Quantity']:
#             Items.Quantity = data['Quantity']
#             db.session.commit()
#             return jsonify(
#                 {
#                     "code": 200,
#                     "data": Items.json() # Items need connect to inventory.query
#                 }
#             ), 200
#     except Exception as e:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "Items_ID": Items_ID
#                 },
#                 "message": "An error occurred while updating the order. " + str(e)
#             }
#         ), 500


if __name__ == '__main__':
    print("This is flask " + os.path.basename(__file__) +
        " for placing an order...")
    app.run(host="0.0.0.0", port=5002, debug=True)


# if name == 'main':

#     app.run(port=5000, debug=True)