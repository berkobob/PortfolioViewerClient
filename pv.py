import argparse
import requests
import json
import os
import ntpath
from tabulate import tabulate

url = {'new': "http://localhost:5000/api/new",
       'new1': "http://devserver:5000/api/new",
       'add': "http://localhost:5000/api/add",
       'add1': "http://devserver:5000/api/add",
       'api1': "http://devserver:5000/api/",
       'api': "http://localhost:5000/api/",
       "ports": "http://localhost:5000/api/ports",
       "del": "http://localhost:5000/api/del",
       'head': {"Content-Type": "application/json"},
       'stock': ['port', 'ticker', 'shares', 'price', 'exchange',],
       'port': ['PORT', 'VALUE', 'DELTA'],
       'stocks': ['PORT', 'NAME', 'TICK', 'QTY', 'PRICE', 'EXCH', 'LAST', 'DELTA', '%', 'STAMP', '£'],
       'cmds': ['new', 'add','load', 'ports', 'stocks', 'quit', 'delete'],
       }

class Portfolio_Viewer():

    def __init__(self, cmd=None):
        parser = argparse.ArgumentParser(
            description="View portfolio prices")
        parser.add_argument('command', 
            choices=url['cmds'],
            nargs='?',
            help="Which of these commands do you want to run?")

        if cmd:
            args = parser.parse_args(cmd)
        else:
            #args = parser.parse_args()
            args, parms = parser.parse_known_args()
 
        if args.command != 'quit':
            if args.command in url['cmds']:
                getattr(self, args.command)(parms)
            else:
                print(url['cmds'])
                Portfolio_Viewer(input("PV> ").split(' '))

    def new(self, parms):
        """ Create a new portfolio """
        parser = argparse.ArgumentParser()
        parser.add_argument('file', nargs='+')
        args = parser.parse_args(parms)
        
        for port in args.file:
            data=json.dumps({'port': port})
            reply = requests.post(url['new'], data, headers=url['head'])
            print(reply.json())

    def add(self, parms):
        """ add a stock to a portfolio """
        parser = argparse.ArgumentParser(
            description="Files and subcommands to pass to the /'add/' command")
        parser.add_argument('stock', nargs=5,
            help="Files and subcommands to pass to the /'add/' command")
        args = parser.parse_args(parms)
        self._send_to_api(args.stock)

    def load(self, parms):
        """ load a portfolio from a .csv file """
        parser = argparse.ArgumentParser(
            description="Files and subcommands to pass to the /'add/' command")
        parser.add_argument('file', nargs='?',
            help="Files and subcommands to pass to the /'add/' command")
        args = parser.parse_args(parms)

        port = os.path.splitext(ntpath.basename(args.file))[0]

        try:
            with open(args.file) as file:
                file.readline()  # discard header row
                for row in file:
                    stock = row.rstrip('\n').split(',')
                    stock.insert(0, port)
                    self._send_to_api(stock)
            self.new([port])
        except Exception as e:
            print(str(e))

    def ports(self, _):
        """ return a list of portfolio names """
        reply = requests.get(url['ports'], headers=url['head'])
        print(reply.json())
        if reply.json()['result'] == 'success':
            print (tabulate(reply.json()['ports'], headers=url['port']))
        else:
            print (reply.text)

    def stocks(self, parms):
        """ return stocks in a portfolio """
        parser = argparse.ArgumentParser(
            description="Files and subcommands to pass to the /'add/' command")
        parser.add_argument('file', nargs='?',
            help="Files and subcommands to pass to the /'add/' command")
        args = parser.parse_args(parms)

        reply = requests.get(url['api']+parms[0], headers=url['head'])
        print(tabulate(reply.json()['stocks'], headers=(url['stocks'])))

    def delete(self, parms):
        """ Delete a portfolio """
        parser = argparse.ArgumentParser()
        parser.add_argument('port', nargs='?')
        parser.add_argument('stock', nargs='*')
        args = parser.parse_args(parms)

        data=json.dumps({'port': args.port, 'stock': args.stock})
        print(data)
        reply = requests.post(url['del'], data, headers=url['head'])
        print(reply.json())
        #print(reply.text)

    def _send_to_api(self, args):
        stock = dict(zip(url['stock'], args))
        stock = json.dumps(stock)
        reply = requests.post(url['add'], stock, headers=url['head'])
        print(reply.json())


if __name__ == '__main__':
    Portfolio_Viewer()
