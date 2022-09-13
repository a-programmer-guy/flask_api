from api import create_api, db
from api.models import User, Task

api = create_api()

if __name__ == '__main__':
    api.run(debug=True, use_reloader=True)

# flask shell context preimports app, the db and models
# use flask shell to run it on the command line
@api.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task}






