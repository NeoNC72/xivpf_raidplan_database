import sqlite3

DATABASE = 'raidplans.db'

def add_test_data():
    test_plans = [
        ('The Unending Coil of Bahamut (Ultimate)', 'raidplan.io/ucob/test1'),
        ('The Weapons Refrain (Ultimate)', 'raidplan.io/uwu/test2'),
        ('The Epic of Alexander (Ultimate)', 'raidplan.io/tea/test3'),
        ('Dragonsongs Reprise (Ultimate)', 'raidplan.io/dsr/test4'),
        ('The Omega Protocol (Ultimate)', 'raidplan.io/top/test5'),
        ('Asphodelos: The Fourth Circle (Savage)', 'raidplan.io/p4s/test6'),
        ('Abyssos: The Eighth Circle (Savage)', 'raidplan.io/p8s/test7'),
        ('Anabaseios: The Twelfth Circle (Savage)', 'raidplan.io/p12s/test8'),
        ('Anabaseios: The Twelfth Circle (Savage)', 'raidplan.io/p12s/test9'),
        ('Anabaseios: The Twelfth Circle (Savage)', 'raidplan.io/p12s/test10'),
        ('The Unending Coil of Bahamut (Ultimate)', 'raidplan.io/ucob/test1'),
    ]

    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS raidplans (
            duty_name TEXT,
            url TEXT,
            UNIQUE(duty_name, url)
        )
        ''')

        print(f"Adding {len(test_plans)} test entries (including potential duplicates)...")
        cursor.executemany("INSERT OR IGNORE INTO raidplans (duty_name, url) VALUES (?, ?)", test_plans)

        conn.commit()
        print(f"Successfully added test data. {cursor.rowcount} new rows inserted.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    add_test_data()
