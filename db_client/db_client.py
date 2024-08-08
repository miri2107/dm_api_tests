import uuid
import records
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


class DbClient:
    def __init__(
            self,
            user,
            password,
            host,
            database
    ):
        connection_string = f'postgresql://{user}:{password}@{host}/{database}'
        self.db = records.Database(connection_string)
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='db')

    def send_query(
            self,
            query
    ):
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=query
        )
        dataset = self.db.query(query=query).as_dict()
        log.msg(
            event='response',
            dataset=dataset
        )
        return dataset


# if __name__ == '__main__':
#     db = DbClient('postgres', 'admin', '5.63.153.31', 'dm3.5')
#     query = 'select * from "public"."Users"   limit 10'
#     db.send_query(query)

    # rows = db.query('select * from  "public"."Users" limit 10')
    # for row in rows.as_dict():
    #     print(row)
