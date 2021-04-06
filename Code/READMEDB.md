# Run Python Console
In the same directory as login.db

run command $ `python`

# Commit to Database
1. Import database and user class `from app import db, User`
2. Create new user with User class constructor `testuser = User(username='TestUser', password='root123')`
3. Add user `db.session.add(testuser)`
4. Commit changes to database `db.session.commit()`

# Query Database
1. Import database and user class `from app import db, User`
2. Query all `results = User.query.all()` OR  Query specific column and select first result user = User.query.filter_by([column name = entry]).first() Example `user = User.query.filter_by(username = 'TestUser').first()`
3. results[0].[column name] Example `results[0].username`

