add_floor = "ALTER TABLE hangar ADD COLUMN floor text;"
update_floor = "UPDATE hangar SET floor = substr(hangar_id, 0, 3);"