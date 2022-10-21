available_aircraft = "SELECT SUM(aircraft_in_hangar) as count FROM hangar;"

most_popular_aircraft = "SELECT type_of_aircraft, SUM(aircraft_in_hangar) as count
    FROM hangar GROUP BY type_of_aircraft ORDER BY count DESC LIMIT 1;"

largest_number_of_aircraft = "SELECT hangar_id, SUM(aircraft_in_hangar) as count
    FROM hangar GROUP BY hangar_id ORDER BY count DESC LIMIT 1;"