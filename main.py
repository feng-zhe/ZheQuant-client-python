'''
Main file of the Client for ZheQuant
'''
from cmd2 import Cmd

class ZheQuantClient(Cmd):
    '''ZheQuant Client implementation class'''

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

    def do_schedule(self, line):
        '''
        Schedule jobs.

        Usage: TODO
        '''
        #TODO
        pass

    def do_show(self, line):
        '''
        Show information.

        Usage: TODO
        '''
        #TODO
        pass

    def preloop(self):
        print(  'Welcome to ZheQuant python client!\n' +
                'Please see the documents here for usage:\n' +
                'https://github.com/feng-zhe/ZheQuant-client-python');

if __name__ == '__main__':
    ZheQuantClient().cmdloop()
