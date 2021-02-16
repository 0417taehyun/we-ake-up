import boto3


def create_member_table():
    dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')

    table    = dynamodb.create_table(
        TableName = "We-ake-up",
        KeySchema = [
            {
                "AttributeName": "name",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "github_id",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "count",
                "KeyType": "RANGE"
            }
        ],
        AttributeDefinitions = [
            {
                "AttributeName": "name",
                "AttributeType": "S"
            },
            {
                "AttributeName": "github_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "count",
                "AttributeType": "N"
            }
        ],
        ProvisionedThroughput = {
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10
        }
    )

    return table


print(create_member_table())