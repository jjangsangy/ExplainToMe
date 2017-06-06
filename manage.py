import os

from flask_script import Manager, Server
from ExplainToMe import create_app

app = create_app()
manager = Manager(app=app, disable_argcomplete=False)

server = Server(host=os.getenv('HOST', '127.0.0.1'), port=os.getenv('PORT', 5000))
manager.add_command('runserver', server)


if __name__ == '__main__':
    manager.run()
