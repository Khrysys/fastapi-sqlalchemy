from alembic.config import main
from typing import Any

class Migration:
    def __init__(self, init_options: 'dict[str,Any]' = {}):
        argv = ['init', 'migrations']
        argv.extend(init_options)
        main(argv)
        
    def migrate(self, options: 'dict[str,Any]' = {}):
        argv = ['migrate']
        argv.extend(options)
        main(argv)
        
    def revision(self, options: 'dict[str,Any]' = {}, revision_name:str = 'Commit'):
        argv = ['revision', revision_name]
        argv.extend(options)
        main(argv)
        
    def upgrade(self, options: 'dict[str,Any]' = {}, branch:str = 'Head'):
        self.revision()
        argv = ['upgrade', branch]
        argv.extend(options)
        main(argv)
        
    def current(self):
        main(['current'])
        
    def history(self, options: 'dict[str,Any]' = {}):
        argv = ['history']
        argv.extend(options)
        main(argv)