IN PYTHON CONSOLE 
1. In the same directory as login.db
run comand - $ python

COMMIT TO DB
1. from app import db, User
2. testuser = User(username='TestUser', password='root123')
3. db.session.add(testuser)
4. db.session.commit()

QUERY DB
1. from app import db, User
2. results = User.query.all() OR results = User.query.all() 
   OR user = User.query.filter_by([column name = entry]).first() Example user = User.query.filter_by(username = 'TestUser').first()
3. results[0].[column name] (Example results[0].username)

