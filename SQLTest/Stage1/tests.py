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

        aircraft_result = self.check_aircraft_count(required_count=43)
        if aircraft_result != True:
            return aircraft_result

        popular_aircraft = self.check_popular_aircraft("X-Wing")
        if popular_aircraft != True:
            return popular_aircraft

        largest_aircraft = self.check_largest_aircraft(required="R5-D4")
        if largest_aircraft != True:
            return largest_aircraft

        return correct()

    def setup_table(self):
        self.execute('create_hangar_table')

        result_table = self.execute_and_fetch_all("PRAGMA table_info(hangar);")

        if not result_table:
            return Exception("We couldn't setup the `hangar` table for you to complete this task")

        self.execute('populate_rows')

    def check_aircraft_count(self, required_count: int):
        # execute user query
        aircraft_count = self.execute('available_aircraft').fetchone()[0]

        # check the type
        try:
            aircraft_count = int(aircraft_count)
        except ValueError:
            return wrong(f"Expected value was integer type, found {type(aircraft_count)}")

        # check if the result is the required amount
        if aircraft_count != required_count:
            # show error for sum function, if it is not found in the query
            if 'sum' not in self.queries['available_aircraft'].lower():
                return wrong("SUM function doesn't exist in your query.")

            # show error for `aircraft_in_hangar` column, if it isn't found in the query
            if 'aircraft_in_hangar' not in self.queries['available_aircraft']:
                return wrong("Are you calling SUM function on `aircraft_in_hangar` column?\n"
                             "`aircraft_in_hangar` doesn't exist in your query.")

            # show error for `hangar` table, if it's found in the query
            if 'hangar' not in self.queries['available_aircraft']:
                return wrong("Are you sure you are selecting from `hangar` table?"
                             "`hangar` doesn't exist in your query.")

            # check the final result
            return wrong(f"The available craft supposed to be {required_count}, found {aircraft_count}.")

        return True

    def check_popular_aircraft(self, required: str):
        # execute user query
        popular_aircraft = self.execute('most_popular_aircraft').fetchone()[0]

        # check the type
        if type(popular_aircraft) != str:
            return wrong(f"Expected value was string value, found {type(popular_aircraft)}")

        # check if the result is the required amount
        if popular_aircraft != required:
            # show error for sum function, if it is not found in the query
            if 'sum' not in self.queries['most_popular_aircraft'].lower():
                return wrong("SUM function doesn't exist in your query.")

            # show error for `type_of_aircraft` column, if it isn't found in the query
            if 'type_of_aircraft' not in self.queries['most_popular_aircraft']:
                return wrong("Are you calling SUM function on `type_of_aircraft` column?\n"
                             "`type_of_aircraft` doesn't exist in your query.")

            # show error for `hangar` table, if it's not  found in the query
            if 'hangar' not in self.queries['most_popular_aircraft']:
                return wrong("Are you sure you are selecting from `hangar` table?"
                             "`hangar` doesn't exist in your query.")

            # show error for `GROUP BY`, if it's not found in the query
            if 'group by' not in self.queries['most_popular_aircraft'].lower():
                return wrong("Are you grouping your the rows by `type_of_aircraft`?"
                             "`GROUP BY` doesn't exist in your query.")

            # show error for `ORDER BY`, if it's not found in the query
            if 'order by' not in self.queries['most_popular_aircraft'].lower():
                return wrong("Are you ordering your result by the count of `aircraft_in_hangar`?"
                             "`ORDER BY` doesn't exist in your query.")

            # check the final result
            return wrong(f"The most popular craft supposed to be {required}, found {popular_aircraft}.")

        return True

    def check_largest_aircraft(self, required: str):
        # execute user query
        largest_aircraft = self.execute('largest_number_of_aircraft').fetchone()[0]

        # check the type
        if type(largest_aircraft) != str:
            return wrong(f"Expected value was string value, found {type(largest_aircraft)}")

        # check if the result is the required amount
        if largest_aircraft != required:
            # show error for `hangar_id` column, if it isn't found in the query
            if 'hangar_id' not in self.queries['largest_number_of_aircraft']:
                return wrong("Are you selecting `hangar_id` column?\n"
                             "`hangar_id` doesn't exist in your query.")

            # show error for `hangar` table, if it's not  found in the query
            if 'hangar' not in self.queries['largest_number_of_aircraft']:
                return wrong("Are you sure you are selecting from `hangar` table?"
                             "`hangar` doesn't exist in your query.")

            # show error for `GROUP BY`, if it's not found in the query
            if 'group by' not in self.queries['largest_number_of_aircraft'].lower():
                return wrong("Are you grouping your the rows by `hangar_id`?"
                             "`GROUP BY` doesn't exist in your query.")

            # show error for `ORDER BY`, if it's not found in the query
            if 'order by' not in self.queries['largest_number_of_aircraft'].lower():
                return wrong("Are you ordering your result by the count of `aircraft_in_hangar`?"
                             "`ORDER BY` doesn't exist in your query.")

            # check the final result
            return wrong(f"The most popular craft supposed to be {required}, found {largest_aircraft}.")

        return True


if __name__ == '__main__':
    Test().run_tests()
