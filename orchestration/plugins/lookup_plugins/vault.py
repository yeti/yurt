from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError

from hvac import Client
import json
import os
import re

# Modeled after https://github.com/jhaals/ansible-vault/blob/master/vault.py


class LookupModule(LookupBase):

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
        vault = LookupModule.get_vault_from_path('../{}'.format(path))
        client = Client(**vault)
        if client.is_authenticated() and not client.is_sealed():
            result = client.read(key)['data'][field]
            return result
        else:
            raise AnsibleError('Unable to authenticate with Vault!')
