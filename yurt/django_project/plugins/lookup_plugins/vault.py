from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError

from hvac import Client
import json
import os
import re

# Modeled after https://github.com/jhaals/ansible-vault/blob/master/vault.py


class LookupModule(LookupBase):

    @classmethod
    def find_vagrantfile_dir(cls, path=None):
        if path is None:
            path = os.getcwd()
        vagrantfile_path = os.path.join(path, "Vagrantfile")
        if os.path.exists(vagrantfile_path):
            return path
        if os.path.expanduser("~") == path:
            raise Exception('Vagrantfile not found! If running `yurt vault`, run `yurt vault --dest=.`')
        return LookupModule.find_vagrantfile_dir(os.path.dirname(path))


    @classmethod
    def get_vault_from_path(cls, path):
        with open(path, 'r') as vault_file:
            vault_details = json.loads(vault_file.read())
            return {
                        'url': vault_details["VAULT_ADDR"],
                        'token': vault_details["VAULT_TOKEN"]
                    }

    def run(self, terms, variables, **kwargs):
        key, field, path = terms
        parent_path = LookupModule.find_vagrantfile_dir()
        vault = LookupModule.get_vault_from_path('{}/{}'.format(parent_path, path))
        client = Client(**vault)
        if client.is_authenticated() and not client.is_sealed():
            result = client.read(key)['data'][field]
            return [result]
        else:
            raise AnsibleError('Unable to authenticate with Vault!')
