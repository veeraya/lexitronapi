"""
Random list of functions used to manually create table or test getting data from api.
You can safely ignore this file.
"""
import boto3
import simplejson

def create_table():
    # Get the service resource.
    dynamodb = boto3.resource('api', region_name='ap-southeast-1')

    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName='english_thai_dict_v2',
        KeySchema=[
            {
                'AttributeName': 'english_word',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'english_word',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 20
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='english_thai_dict_v2')

    # Print out some data about the table.
    print(table.item_count)

def put_item():
    dynamodb = boto3.resource('api', region_name='ap-southeast-1')
    table = dynamodb.Table('english_thai_dict')
    dict = {"a" : set()}
    dict["a"].add("อะไร")
    dict["a"].add("ยังไง")
    table.put_item(
        Item={
            'english_word': 'a',
            'thai_definitions': dict["a"],
        }
    )

    response = table.get_item(
        Key={
            'english_word': 'a'
        }
    )
    item = response['Item']
    print(item)

def drop_table():
    dynamodb = boto3.resource('api', region_name='ap-southeast-1')
    table = dynamodb.Table('english_thai_dict')
    table.delete()


def get_item(word):
    dynamodb = boto3.resource('api', region_name='ap-southeast-1')
    table = dynamodb.Table('english_thai_dict')

    # response = api.batch_get_item(
    #     RequestItems={
    #         'english_thai_dict': {
    #             'Keys': [
    #                 {
    #                     'english_word': "hello"
    #                 },
    #                 {
    #                     'english_word': "world"
    #                 },
    #             ]
    #         }
    #     }
    # )
    response = table.get_item(
        Key={
            'english_word': word,
        }
    )

    item = response['Item']
    print(item)
    data = {"found": True, "search_term": word, "closest_search_term": word,
            "definitions": list(item['thai_definitions'])}
    print(simplejson.dumps(data))

if __name__ == "__main__":
    create_table()