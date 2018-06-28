#!/usr/bin/env python3.6
# A simple command line utility inspired by from user:fmasanori on github

import requests
import json
import datetime
import argparse
from collections import OrderedDict

parser = argparse.ArgumentParser(description='A simple cli script for\
 Worldcup scores and fixtures.')
parser.add_argument('-today', action='store_true', help='Returns todays scores/fixtures.')
parser.add_argument('-save', action='store_true', help='Saves the\
 score/fixture.')
args = parser.parse_args()


class WoCu():
    """
    WoCu() includes all the functions that deals with parsing and presenting
    all the worldcup information.
    """
    
    def __init__(self):
        # The following line is to connect to the internet for the json file.
        # This is the intended use of the script.
        self.server = 'https://worldcup.sfg.io/matches'
        try:
            print('Connecting to {}'.format(self.server))
            self.matches = requests.get(self.server).json()
        
        # In case of no network. A file a provided. It may not be updated.
        except:
            print('Unable to connect to server.')
            print('Trying to open local file.')
            with open('resources/matches.json', 'r') as f:
                self.matches = json.load(f)


    def Scores(self):
        """
        This function prints out all the completed matches.
        """
        results = {}; prev =''
        for match in self.matches:
            match_date = match['datetime'][:10]
            match_time = self.TimeConvert(match['datetime'][-10:-1])
            if match['status'] == 'future':
                details = [match_time+' ' + str(match['home_team']['country'])+ \
                        ' ' +'x'+' '+ match['away_team']['country']]
            elif match['status'] in ['completed', 'in progress']:
                details = [match_time+ ' '+str(match['home_team']['country']) +\
                        ' ' + \
                            str(match['home_team']['goals']) + ' '+ 'x'+ ' ' + \
                            str(match['away_team']['country']) +' '+ \
                            str(match['away_team']['goals'])]
            
            # Adding matches to dictionary using match_date as key 
            if match_date not in results:                      
                results[match_date] = [details]
            else: 
                results[match_date].append(details)
        
        # Returns a ordered dictionary that's been sorted 
        return OrderedDict(sorted(results.items()))


    def TimeConvert(self, time):
        """
        This function converts from UTC to Melbourne time.
        """
        time_val = int(time[1:3])+10
        if time_val >= 24:
            time_val = time_val - 24
        else: pass
        return '{}:00:00'.format(time_val)


    def PrintResults(self, results, today=False, save=False):
        """
        This function prints out the results.
        """
        if today:
            now = str(datetime.datetime.now())[:11]
            int_now = (int(now[0:4]),int(now[5:7]), int(now[8:10]))
            for result in results.items():
                int_result_date =\
                (int(result[0][0:4]),int(result[0][5:7]),int(result[0][8:10]))
                if int_result_date == int_now:
                    for item in result[1]:
                        print(item[0])
        elif save:
            print('Saving score/fixtures to resources/save.txt')
            with open('resources/save.txt', 'w+') as f:
                f.write(str(results))
            print('Scores/Fixtures saved.')
        else:
            for result in results.items():
                self.PrintSeparator(10)
                print(result[0])
                self.PrintSeparator(10)
                for item in result[1]:
                    print(item[0])

    
    def PrintSeparator(self, n):
        """
        This function prints rows of stars to help with data presentation.
        """
        print('*' * n)

    
    def Main(self, args):
        """
        This function processes the arguments and runs the required functions. 
        """
        if args.today:
            self.PrintResults(self.Scores(), today=True)
        elif args.save:
            self.PrintResults(self.Scores(), save=True)
        else:
            self.PrintResults(self.Scores())

# Boilerplate code:
if __name__ == '__main__':
    instance = WoCu()
    instance.Main(args)
