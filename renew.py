#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import subprocess

def load_config(filename_config):
    with open(filename_config) as fconf:
        return json.load(fconf)

def run_beluga(config, other_args):
    auth_args = ['--username', config['username'], '--password', config['password']]
    output = subprocess.check_output(['beluga'] + auth_args + other_args)
    return json.loads(output)

def renew_certs(config):
    sites = config['sites']
    response = run_beluga(config, ['--path', 'ssl-certificates'])
    
    for cert in response['certificates']:
        site = sites.get(cert['common_name'])

        if site:
            body = {'id': cert['id']}
        
            with open(site['cert_file'], 'r') as fcert:
                body['certificate'] = fcert.read()

            with open(site['chain_file'], 'r') as fchain:
                body['chain'] = fchain.read()

            with open(site['privkey_file'], 'r') as fkey:
                body['key'] = fkey.read()

            query = ['--method', 'PUT', '--path', 'ssl-certificates', '--body', json.dumps(body)]
            print run_beluga(config, query)

def main():
    config = load_config('config.json')
    renew_certs(config)

if __name__ == "__main__":
    main()
