import os
if os.name == "nt":
    db_file_path = 'sqlite:////' + os.path.dirname(os.path.realpath(__file__)) + "\login.db"
else:
    db_file_path = 'sqlite:////' + os.path.dirname(os.path.realpath(__file__)) + "/login.db"

print(db_file_path)
print(os.name)