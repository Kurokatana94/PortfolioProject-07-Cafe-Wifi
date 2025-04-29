#Use this to pass the data from the old version of the database to the new in main.py

from sqlalchemy import Integer, String, Boolean, Text, MetaData, Table, select

def get_table_data():
    metadata = MetaData()
    table = Table('cafe', metadata, autoload_with=db.engine)

    # Create and execute the select statement
    stmt = select(table)
    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        data = [dict(row._mapping) for row in result]  # _mapping allows safe dict conversion

    return {'data': data}

with app.app_context():
    for row in get_table_data()['data']:
        print(row)
        db.session.add(Cafe(
            author_id=1,
            name=row['name'],
            map_url=row['map_url'],
            img_url=row['img_url'],
            location=row['location'],
            seats=row['seats'],
            has_toilet=row['has_toilet'],
            has_wifi=row['has_wifi'],
            has_sockets=row['has_sockets'],
            can_take_calls=row['can_take_calls'],
            coffee_price=row['coffee_price'],
        ))
    db.session.commit()