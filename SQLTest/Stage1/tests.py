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
        'available_aircraft': None,
        'most_popular_aircraft': None,
        'largest_number_of_aircraft': None
    }

    @dynamic_test
    def test_create_table(self):
        # setting up the table to work
        self.setup_table()

        aircraft_result = self.check_answer("available_aircraft", 43, 1)
        if aircraft_result != True:
            return aircraft_result

        popular_aircraft = self.check_answer("most_popular_aircraft", "X-Wing", 1,
                                 ["B-Wing", "Slave 1", "Jedi Starfighter"])
        if popular_aircraft != True:
            return popular_aircraft

        largest_aircraft = self.check_answer("largest_number_of_aircraft", "R5-D4", 1,
                                ["R9-G3", "R9-G13", "R5-D8", "R2-C6", "R2-C1", "R9-G11", "R2-C4", "R9-G8", "R5-D11"])
        if largest_aircraft != True:
            return largest_aircraft

        return correct()

    def setup_table(self):
        self.execute('create_hangar_table')

        result_table = self.execute_and_fetch_all("PRAGMA table_info(hangar);")

        if not result_table:
            return Exception("We couldn't setup the `hangar` table for you to complete this task")

        self.execute('populate_rows')

    def check_answer(
        self, query, expected_value: any,
        required_len_of_answer: int = None, close_answers: dict|list = None
    ):
        result = self.execute_and_fetch_all(query)

        if required_len_of_answer and len(result) != required_len_of_answer:
            return wrong(f"Are you sure your query for {query} returns {required_len_of_answer} "
                         f"number of row{'s' if required_len_of_answer > 1 else ''}?")

        if type(expected_value) == list:
            if set(expected_value) != set(result):
                return wrong("Your query doesn't return the expected values.")
        else:
            if expected_value not in result[0]:
                if result[0] in close_answers:
                    return wrong("Your query returns one of the close values.\n"
                                 "Did you arranged your queries in the correct order?")

                return wrong(f"Your query doesn't return the expected value. The expected value was {expected_value}")

        return True


if __name__ == '__main__':
    Test().run_tests()
