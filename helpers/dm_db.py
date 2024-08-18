from db_client.db_client import DbClient


class DmDataBase:
    def __init__(
            self,
            user,
            password,
            host,
            database
    ):
        connection_string = f'postgresql://{user}:{password}@{host}/{database}'
        self.db = DbClient(
            user,
            password,
            host,
            database
        )

    def get_all_users(
            self
    ):
        query = 'select * from "public"."Users"  '
        dataset = self.db.send_query(query=query)
        return dataset

    def get_user_by_login(
            self,
            login
    ):
        query = f'''
        select * from "Users"
        where "Login" = '{login}'
        '''
        dataset = self.db.send_query(query=query)
        return dataset

    def activate_user_by_login(
            self,
            login
    ):
        query = f'''
        update  "Users"
        set "Activated" = True
        where "Login" = '{login}'
        '''
        dataset = self.db.send_query(query=query)
        return dataset

    def delete_user_by_login(
            self,
            login
    ):
        query = f'''
        delete from  "Users"
        where "Login" = '{login}'
        '''
        dataset = self.db.send_bulk_query(query=query)
        return dataset
