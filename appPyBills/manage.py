import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #Appends the project directory to sys paths
from flask_script import Manager, Server
from appPyBills import app
from flask_migrate import MigrateCommand
manager = Manager(app)

manager.add_command('db', MigrateCommand)

manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    )
                    )
if __name__ == '__main__':
    manager.run()
