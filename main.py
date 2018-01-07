'''
Main file of the Client for ZheQuant
'''
import json
import os
import hashlib
import requests
from cmd2 import Cmd
from terminaltables import AsciiTable
from zq_gen.str import cmd_str2dic

class ZheQuantClient(Cmd):
    '''ZheQuant Client implementation class'''

    def __init__(self):
        '''Initialization '''
        super().__init__()
        # config
        fname = 'config_default.json'
        if os.path.isfile('config.json'):
            fname = 'config.json'
        with open(fname) as the_file:
            self.config = json.load(the_file)
        # session
        self.session = {}

    def do_login(self, line):
        '''
        User login

        Usage: login -u <userId> -p <password>
        '''
        url = self.config['server_url'] + '/user/auth'
        inputs = cmd_str2dic(line)
        # check inputs
        if '-u' not in inputs:
            print('[!] missing -u for user id')
            return
        elif '-p' not in inputs:
            print('[!] missing -p for password')
            return
        # generate requests
        md5 = hashlib.md5()
        md5.update(bytes(inputs['-p'], 'utf-8'))
        payload = {
                "userId"   : inputs['-u'],
                "password" : md5.hexdigest()
                }
        rsp_raw = requests.post(url, data=payload)
        rsp = rsp_raw.json()
        if rsp_raw.status_code == requests.codes['ok'] \
            and rsp['success'] is True:
            self.session['userId'] = rsp['userId']
            self.session['token'] = rsp['token']
        else:
            print('[!] Login failed. Please check your user id or password.')

    def do_schedule(self, line):
        '''
        Schedule jobs.

        Usage: schedule -n <job name> -dsc <job description> -t <job type> -p "<arguments>"

        Example: schedule -n my_job -dsc just_for_test -t mv_avg -p "-d 20 -n 5"
        '''
        url = self.config['server_url'] + '/quant/jobs'
        inputs = cmd_str2dic(line)
        payload = {
                "userId"      : self.session['userId'],
                "token"       : self.session['token'],
                "job_name"    : inputs['-n'],
                "description" : inputs['-dsc'],
                "cmd"         : line
                }
        rsp_raw = requests.post(url, data=payload)
        if rsp_raw.status_code == requests.codes['ok']:
            print('[x] Job scheduled!')
        else:
            print('[!] Scheduling failed!')

    def do_mv_avg(self, line):
        '''
        Calculate the moving average values.

        Usage: mv_avg -d <days> -n <number of the top stocks>
        '''
        #TODO
        pass

    def do_inc_pct(self, line):
        '''
        Calculate the increasing percentage.

        Usage: TODO
        '''
        #TODO
        pass

    def do_display(self, line):
        '''
        Show information.

        Usage: display <target>

        <target>: 'jobs'
        '''
        # check inputs
        inputs = cmd_str2dic(line)
        if len(inputs) < 1: 
            print('[!] missing target')
            return
        if inputs['cmd_name'] == 'jobs':
            url = self.config['server_url'] + '/quant/results'
            # generate requests
            payload = {
                    "userId" : self.session['userId'],
                    "token"  : self.session['token']
                    }
            rsp_raw = requests.post(url, data=payload)
            rsp = rsp_raw.json()
            if rsp_raw.status_code == requests.codes['ok']:
                table_data = [
                        ['name', 'creator', 'create_date', 'status', 'description', 'cmd']
                        ]
                for result in rsp['results']:
                    table_data.append([
                        result['name'],
                        result['creator'],
                        result['create_date'],
                        result['status'],
                        result['description'],
                        result['cmd']
                        ])
                table = AsciiTable(table_data)
                print(table.table)
            else:
                print('[!] Server returns error code: ' + rsp_raw)

    def preloop(self):
        '''
        Print banner
        '''
        print('Welcome to ZheQuant python client!\n'
                + 'Please see the documents here for usage:\n'
                + 'https://github.com/feng-zhe/ZheQuant-client-python')

if __name__ == '__main__':
    ZheQuantClient().cmdloop()
