import boto3


    
class ExchangeRatesManager:
    def __init__(self):
        self.session = boto3.session.Session()
        self.dynamodb = self.session.resource('dynamodb', endpoint_url='http://localhost:4566', region_name='us-east-1')
        self.table_name = 'ExchangeRates'
        self.table = None

    # Method to fetch exchange rate data from DynamoDB
    def fetch_exchange_rates_from_db(self,  date: str,  columns: str) -> list:
        try:
           

            if not self.table_exists():
                raise Exception("Table 'ExchangeRates' does not exist. Create the table first using create_dynamodb_table.")

            # Get a reference to the 'ExchangeRates' table
            self.table = self.dynamodb.Table(self.table_name)
            query_params = {
                'KeyConditionExpression': "#date = :date",
                'ExpressionAttributeNames': {
                    "#date": "DATE"
                },
                'ExpressionAttributeValues': {
                    ":date": date
                }
            }
            
            if columns:
                query_params['ProjectionExpression'] = columns
            
            response = self.table.query(**query_params)
            exchange_rates = response.get("Items", [])
            return exchange_rates
        except Exception as e:
            print("Error occurred while fetching data from DynamoDB:", str(e))
            return None

    # Method to check if the DynamoDB table exists
    def table_exists(self):
        return self.table_name in [table.name for table in self.dynamodb.tables.all()]

    # Method to create the DynamoDB table
    def create_dynamodb_table(self):
        if self.table_exists():
            print("Table 'ExchangeRates' already exists.")
            self.table = self.dynamodb.Table(self.table_name)
        else:
            self.table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'DATE',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'CURRENCY',
                        'KeyType': 'RANGE'  # Sort key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'DATE',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'CURRENCY',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            print("Table 'ExchangeRates' created successfully!")

    # Method to drop the DynamoDB table
    def drop_dynamodb_table(self):
        try:
            self.table = self.dynamodb.Table(self.table_name)
            self.table.delete()
            self.table.wait_until_not_exists()
            print("Table 'ExchangeRates' deleted successfully!")
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            print("Table 'ExchangeRates' does not exist. Nothing to delete.")

    # Method to insert data into the DynamoDB table
    def insert_data(self, fetch_data):
        if not self.table_exists():
            raise Exception("Table 'ExchangeRates' does not exist. Create the table first using create_dynamodb_table.")

        # Assuming you have already created the 'ExchangeRates' table

        # Get a reference to the 'ExchangeRates' table
        self.table = self.dynamodb.Table(self.table_name)

        # Sample data
        data = fetch_data

        # Insert data into the table
        with self.table.batch_writer() as batch:
            for item in data:
                batch.put_item(Item=item)

        print("Data inserted successfully!")
