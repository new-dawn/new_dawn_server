import filecmp

def db_consistency_check():
	if not filecmp.cmp('db.sqlite3', 'db.sqlite3.copy'):
        raise Exception('db.sqlite3 is not in sync with the latest migration. Make sure you have run manage.py makemigrations & manage.py migrate')

def main():
    db_consistency_check()

if __name__ == "__main__":
    main()
