from alembic.config import main
from alembic import command
from alembic.config import Config
from typing import Any
import os

class Migration:
    sqlalchemy = None
    cfg = Config()
    
    @staticmethod
    def init():
        command.init(Migration.cfg, 'migrations', template='async', package=True)
        
    @staticmethod
    def revision():
        Migration.cfg.set_main_option('script_location', 'migrations')
        command.revision(Migration.cfg)
        
    @staticmethod
    def upgrade():
        Migration.cfg.set_main_option('script_location', 'migrations')
        command.upgrade(Migration.cfg, 'head')
        
    @staticmethod
    def branches():
        Migration.cfg.set_main_option('script_location', 'migrations')
        command.branches(Migration.cfg)
        
    @staticmethod
    def stamp():
        Migration.cfg.set_main_option('script_location', 'migrations')
        command.stamp(Migration.cfg)
    
    @staticmethod
    def check():
        Migration.cfg.set_main_option('script_location', 'migrations')
        command.check(Migration.cfg)
        
    @staticmethod
    def edit():
        Migration.cfg.set_main_option('script_location', 'migrations')
        command.edit(Migration.cfg)
    
    @staticmethod
    def downgrade():
        Migration.cfg.set_main_option('script_location', 'migrations')
        command.downgrade(Migration.cfg)
        
    @staticmethod
    def current():
        Migration.cfg.set_main_option('script_location', 'migrations')
        command.current(Migration.cfg)
        
    