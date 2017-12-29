'''
Main file of the Client for ZheQuant
'''
import json
import os
import requests
from cmd2 import Cmd
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
        url = self.config.server_url + '/user/auth'
        inputs = cmd_str2dic(line)
        payload = {
                "userId"   : inputs['-u'],
                "password" : inputs['-p']
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
        url = self.config.server_url + '/quant/jobs'
        inputs = cmd_str2dic(line)
        payload = {
                "userId"      : self.session['userId'],
                "token"       : self.session['token'],
                "job_name"    : inputs['-n'],
                "description" : inputs['-d'],
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

        Usage: TODO
        '''
        #TODO
        pass

    def preloop(self):
        '''
        Print banner
        '''
        print('Welcome to ZheQuant python client!\n'
                + 'Please see the documents here for usage:\n'
                + 'https://github.com/feng-zhe/ZheQuant-client-python')

if __name__ == '__main__':
    ZheQuantClient().cmdloop()
