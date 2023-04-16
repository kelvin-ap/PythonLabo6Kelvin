import argparse
import os
import time
import json

from server_management import ServerManagement
from ping import Ping
from report import Report

# Start de server in een apart proces
if __name__ == '__main__':
    #instancies maken
    report = Report()
    server_management = ServerManagement(data_file="servers.json")
    # report_file = "report.json"

    def doesFileExists(filePathAndName):
        return os.path.exists(filePathAndName)
    
    # def read_report_data():
    #     try:
    #         with open(report_file, 'r') as file:
    #             report_data = json.load(file)
    #     except FileNotFoundError:
    #         report_data = []
    #     return report_data

    def interactive_mode(server_management):
        print("Select an action:")
        print("1. Add server")
        print("2. Remove server")
        print("3. Show servers")
        print("4. Ping all servers")
        action = input()
        if action == "1":
            address = input("Enter server address: ")
            server_management.add_server(address)
        elif action == "2":
            server_management.show_servers()
            index = input("Enter server index: ")
            server_management.remove_server(int(index))
        elif action == "3":
            server_management.show_servers()
        elif action == "4":
            print("interval ?")
            interval = int(input())   
            if doesFileExists('./servers.json'):
                while True:
                    report_data = report.read_report_data()
                    for server in server_management.servers:
                        ping = Ping(server["Address"])
                        status = ping.do_ping()

                        #Controleer of de server al in de report.json-file zit
                        for i in range(len(report_data)):
                            if report_data[i]['Address'] == server['Address']:
                                #Als de server al in de report.json-file zit en de status is hetzelfde, doe niets
                                if report_data[i]['Status'] == status:
                                    print(f"Status van {server['Name']} ({server['Address']}) is hetzelfde")
                                    break
                                #Als de server al in de report.json-file zit en de status is verschillend, update de status
                                else:
                                    report_data[i]['Status'] = status
                                    with open(report.data_file, 'w') as f:
                                        json.dump(report_data, f, indent=4)
                                    print(f"Status van {server['Name']} ({server['Address']}) is geüpdatet naar {status}")
                                    break
                        #Als de server niet in de report.json-file zit, voeg toe
                        else:
                            report.add_server(server["Name"], server["Address"], status)
                            print(f"{server['Name']} ({server['Address']}) is toegevoegd aan report.json met status {status}")

                    # Genereer de HTML-pagina
                    report.generate_html()   
                                         
                    time.sleep(interval)
            else:
                print("geen servers")
        else:
            print("Invalid action")

    # Creëer een parser voor de command-line argumenten
    parser = argparse.ArgumentParser(description='Network monitoring tool')
    parser.add_argument('mode', nargs='?', default='interactive', help='Management mode or check mode (default: interactive)')
    parser.add_argument('--add', help='Add a server to the list')
    parser.add_argument('--remove', help='Remove a server from the list')
    parser.add_argument('--show', action='store_true', help='Show the list of servers')
    parser.add_argument('--interval', type=int, help='Time interval for the checks')
    args = parser.parse_args()


    # Als de gebruiker management mode heeft gekozen
    if args.mode == 'management':
        # Als de gebruiker een server wil toevoegen
        if args.add:
            print(f"Server address to add: {args.add}")
            server_management.add_server(args.add)  
        # Als de gebruiker een server wil verwijderen
        elif args.remove:
            server_management.remove_server(args.remove)
        # Als de gebruiker de lijst van servers wil zien
        elif args.show:
            server_management.show_servers()
        # Als er geen opties zijn opgegeven
        else:
            print('Please enter a valid option.')

    # Als de gebruiker check mode heeft gekozen
    elif args.mode == 'check':
        # Als de gebruiker een interval heeft opgegeven
        if args.interval:
            if doesFileExists('./servers.json'):
                while True:
                    report_data = report.read_report_data()
                    for server in server_management.servers:
                        ping = Ping(server["Address"])
                        status = ping.do_ping()
                        
                        #Controleer of de server al in de report.json-file zit
                        for i in range(len(report_data)):
                            if report_data[i]['Address'] == server['Address']:
                                #Als de server al in de report.json-file zit en de status is hetzelfde, doe niets
                                if report_data[i]['Status'] == status:
                                    print(f"Status van {server['Name']} ({server['Address']}) is hetzelfde")
                                    break
                                #Als de server al in de report.json-file zit en de status is verschillend, update de status
                                else:
                                    report_data[i]['Status'] = status
                                    with open(report.data_file, 'w') as f:
                                        json.dump(report_data, f, indent=4)
                                    print(f"Status van {server['Name']} ({server['Address']}) is geüpdatet naar {status}")
                                    break
                        #Als de server niet in de report.json-file zit, voeg toe
                        else:
                            report.add_server(server["Name"], server["Address"], status)
                            print(f"{server['Name']} ({server['Address']}) is toegevoegd aan report.json met status {status}")

                    # Genereer de HTML-pagina
                    report.generate_html()

                    time.sleep(args.interval)
            else:
                print("geen servers")
        else:
            print('Please enter an interval for the checks.')

    elif args.mode == 'interactive':
        while True:
            interactive_mode(server_management)
    else:
        print('Please enter a valid mode (management, check or interactive).')
