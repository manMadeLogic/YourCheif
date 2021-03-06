import boto3
from boto3.dynamodb import conditions
import os
import decimal


class DishHelper:
    def __init__(self, name="DishInfo"):
        self.table_name_ManageDish = name
        region = os.environ.get('region')
        aws_id = os.environ.get('Access_key_ID')
        aws_key = os.environ.get('Secret_access_key')
        dynamodb = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_id,
                                  aws_secret_access_key=aws_key)
        self.table = dynamodb.Table(self.table_name_ManageDish)
        # todo price type

    def add_dish(self, restaurant, dishname, price):
        response = self.table.query(
            KeyConditionExpression=conditions.Key('restaurant').eq(restaurant)
                                   & conditions.Key('dishname').eq(dishname)
        )

        if response['Items']:
            return False, restaurant + " " + dishname + " already exist."

        # print("[" + price + "]")
        response = self.table.put_item(
            Item={
                'restaurant': restaurant,
                'dishname': dishname,
                'price': price
            }
        )
        if response:
            return True, "Success"
        else:
            return False, "Insert fail"

    def delete_dish(self, restaurant, dishname):
        response = self.table.delete_item(
            Key={'restaurant': restaurant, 'dishname': dishname}
        )
        if response:
            return True
        else:
            return False

    def change_price(self, restaurant, dishname, price):
        response = self.table.update_item(
            Key={
                'restaurant': restaurant,
                'dishname': dishname
            },
            UpdateExpression="set price = :p",
            ExpressionAttributeValues={
                # ':r': decimal.Decimal(5.5),
                ':p': decimal.Decimal(price)
            },
            ReturnValues="UPDATED_NEW"
        )
        # todo not tested
        if response:
            return True
        else:
            return False

    def get_dish(self, restaurant):
        response = self.table.query(
            KeyConditionExpression=conditions.Key('restaurant').eq(restaurant)
        )
        dishes = []
        if response['Items']:
            for i in response['Items']:
                dishes.append([i['dishname'], str(i['price'])])
            return dishes
        else:
            # print(response)
            # todo what to do if no dishes?
            return []

    def get_dish_price(self, restaurant, dishname):
        response = self.table.query(
            KeyConditionExpression=conditions.Key('restaurant').eq(restaurant)
                                   & conditions.Key('dishname').eq(dishname)
        )
        if response['Items']:
            return response['Items'][0], "Success"
        else:
            return None, "No dish"
