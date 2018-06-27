#!/usr/bin/env python3.6
# A simple command line utility inspired by from user:fmasanori on github

import requests
import json
from collections import OrderedDict


class WoCu():
    """
    WoCu() includes all the functions that deals with parsing and presenting
    all the worldcup information.
    """
    
    def __init__(self):
        # The following line is to connect to the internet for the json file.
        # This is the intended use of the script.
        try:
            self.matches = requests.get('http://worldcup.sfg.io/matches').json()
        
        # In case of no network. A file a provided. It may not be updated.
        except:
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
            print(match_time)
            if match['status'] == 'future':
                details = [match_time+' ' + str(match['home_team']['country'])+ \
                        ' ' + match['away_team']['country']]
            elif match['status'] in ['completed', 'in progress']:
                details = [match_time+ ' '+str(match['home_team']['country']) +\
                        ' ' + \
                            str(match['home_team']['goals']) + ' '+ 'x'+ ' ' + \
                            str(match['away_team']['country']) +' '+ \
                            str(match['away_team']['goals'])]

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

    def PrintResults(self, results):
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

    def Main(self):
        """
        This function processes the arguments and runs the required functions. 
        """
        self.PrintResults(self.Scores())

# Boilerplate code:
if __name__ == '__main__':
    instance = WoCu()
    instance.Main()
