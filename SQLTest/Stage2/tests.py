from hstest import SQLTest, dynamic_test, correct, wrong


class Test(SQLTest):
    queries = {
        'create_hangar_table': "CREATE TABLE hangar (\
            id INTEGER NOT NULL,\
            hangar_id VARCHAR NOT NULL,\
            type_of_aircraft VARCHAR,\
            aircraft_in_hangar INTEGER,\
            PRIMARY KEY (id, hangar_id)\
        );",
        'populate_rows': "INSERT INTO hangar (id,hangar_id,type_of_aircraft,aircraft_in_hangar) VALUES\
        (1,'R2-C1','X-Wing',3),\
        (2,'R2-C1','Jedi Starfighter',1),\
        (3,'R2-C4','X-Wing',2),\
        (4,'R2-C6','X-Wing',2),\
        (5,'R2-C6','B-Wing',2),\
        (6,'R5-D4','X-Wing',4),\
        (7,'R5-D4','Jedi Starfighter',2),\
        (8,'R5-D4','B-Wing',3),\
        (9,'R5-D4','Slave 1',1),\
        (10,'R5-D8','B-Wing',2),\
        (11,'R5-D8','Slave 1',2),\
        (12,'R5-D11','Slave 1',1),\
        (13,'R9-G3','X-Wing',5),\
        (14,'R9-G3','Jedi Starfighter',1),\
        (15,'R9-G3','B-Wing',2),\
        (16,'R9-G8','Slave 1',1),\
        (17,'R9-G11','B-Wing',2),\
        (18,'R9-G13','X-Wing',3),\
        (19,'R9-G13','B-Wing',4);",
        'add_floor': None,
        'update_floor': None
    }

    @dynamic_test
    def test_create_table(self):
        # setting up the table to work
        self.setup_table()

        add_floor = self.check_add_floor()
        if add_floor != True:
            return add_floor

        update_floor = self.check_update_floor()
        if update_floor != True:
            return update_floor

        return correct()

    def setup_table(self):
        self.execute('create_hangar_table')

        result_table = self.execute_and_fetch_all("PRAGMA table_info(hangar);")

        if not result_table:
            return Exception("We couldn't setup the `hangar` table for you to complete this task")

        self.execute('populate_rows')

    def check_add_floor(self):
        # execute user query
        self.execute_and_fetch_all('add_floor')
        # check the structure of hangar table
        table_structure = self.execute_and_fetch_all("PRAGMA table_info(hangar);")[-1]

        if 'floor' not in table_structure:
            return wrong("The `floor` column isn't found, make sure you add it.")

        if 'TEXT' not in table_structure:
            return wrong("The data type for the `floor` column must be `TEXT`.")

        return True

    def check_update_floor(self):
        # execute user query
        self.execute_and_fetch_all('update_floor')
        actual_floor = self.execute_and_fetch_all("SELECT substr(hangar_id, 0, 3) FROM hangar")
        user_floor = self.execute_and_fetch_all("SELECT `floor` FROM hangar")

        if actual_floor != user_floor:
            return wrong("The values in `floor` column aren't the right ones.")

        return True


if __name__ == '__main__':
    Test().run_tests()
