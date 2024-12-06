
    
from django.core.cache import cache
import json
from .search_trie import Trie
from django.apps import AppConfig

# Assuming Trie is defined as before

class UsersConfig(AppConfig):
    name = 'Users'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):

        trie = Trie()
        
        with open(r'C:\Users\91703\icareindia_backend\trie_data.json', 'r') as f:
            trie_data = json.load(f)
        trie.deserialize(json.dumps(trie_data))    
        
        cache.set('trie', trie.serialize(),timeout=None)
        print("Trie loaded into cache")


# Calls this during startup (e.g., in ready() method of apps.py)
