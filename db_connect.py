import psycopg2 as db   

db_params = {
    'host':'localhost',
    'database':'person',
    'password':'LevRaven.1',
    'user':'postgres',
    'port':5432
}

class DbConnect:
    def __init__(self, db_params):
        self.db_params = db_params
        self.conn = db.connect(**self.db_params)

    def __enter__(self):
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

    def save(self):
        try:
            # Prompting the user for information
            fullname = input("Enter your full name: ")
            age = int(input("Enter your age: "))
            email = input("Enter your email: ")

            # Establishing a database connection and executing the insert query
            with DbConnect(self.db_params) as cur:
                insert_query = 'INSERT INTO users (fullname, age, email) VALUES (%s, %s, %s);'
                insert_params = (fullname, age, email)
                cur.execute(insert_query, insert_params)
                print('User information saved successfully!')
        except (ValueError, db.Error) as e:
            print(f"Error: {e}")

    def get_person(self, person_id):
        try:
            with DbConnect(self.db_params) as cur:
                select_query = 'SELECT fullname, age, email FROM users WHERE id = %s;'
                cur.execute(select_query, (person_id,))
                person = cur.fetchone()
                if person:
                    fullname, age, email = person
                    print(f"Person found: Full Name: {fullname}, Age: {age}, Email: {email}")
                else:
                    print("No person found with the provided ID.")
        except db.Error as e:
            print(f"Error: {e}")

def menu():
    db_connection = DbConnect(db_params)
    while True:
        print('1.Save user')
        print('2.Get user')
        choice = input('Choose menu: ')
        if choice == '1':
            db_connection.save()
        elif choice == '2':
            person_id = input("Enter the ID of the person you want to retrieve: ")
            db_connection.get_person(int(person_id))
        else:
            print('Sorry but we do not have this menu yet :(')

# Start the menu
menu()
