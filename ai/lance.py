# import boto3
# from botocore.config import Config


# class CustomLanceDBConnection(LanceDBConnection):


# class CustomLanceDB(LanceDB):
#     def __init__(self, chat_id: int, embeddings) -> None:
#         self._chat_id = chat_id
#         self._embedding = embeddings
#         table = self._get_table()
#         super().__init__(table, embeddings)

# def connect_to_s3(self):
#     # https://lance-db-test.fra1.digitaloceanspaces.com
#
#     session = boto3.session.Session()
#     client = session.client(
#         's3',
#         endpoint_url='https://lance-db-test.fra1.digitaloceanspaces.com',
#         # Find your endpoint in the control panel, under Settings. Prepend "https://".
#         config=Config(s3={'addressing_style': 'virtual'}),
#         # Configures to use subdomain/virtual calling format.
#         region_name='fra1',  # Use the region in your endpoint.
#         aws_access_key_id='DO00WLJCAHVYMEU6MB9D',
#         # Access key pair. You can create access key pairs using the control panel or API.
#         aws_secret_access_key='B1hGmK29JeQV/QgAh93Yf08Uc/cYnWz5JOhv+LBL9us',
#     )  # Secret access key defined through an environment variable.
#     print(type(client))

# def _get_table(self) -> LanceTable:
#     os.environ['AWS_ACCESS_KEY_ID'] = 'DO00QJ8P79VAUN6X67Q6'
#     os.environ['AWS_SECRET_ACCESS_KEY'] = 'D6Jtq+Afyec31gekdtulpRrQOoWHR2mN/epgg0Ib2jY'
#     os.environ['AWS_ACCESS_KEY_ID'] = 'fra1'
#     session = connect('s3fs://lance-db-test.fra1.digitaloceanspaces.com/lance-db-test')
#     print(session.table_names())
#     table_name = f'table-{self._chat_id}'
#     if table_name not in session.table_names():
#         data = 'System message: conversation with user started'
#         table = session.create_table(
#             table_name,
#             data=[
#                 {
#                     'vector': self._embedding.embed_query(data),
#                     'text': data,
#                     'id': '1',
#                 },
#             ],
#         )
#         print(table)
#     else:
#         table = session.open_table(table_name)
#
#     return table
