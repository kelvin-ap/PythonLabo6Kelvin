import json

class ServerManagement:
    def __init__(self, data_file):
        self.data_file = data_file
        self.servers = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file) as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.servers, f, indent=4)

    def show_servers(self):
        print("server list:")
        for i, server in enumerate(self.servers):
            print(f"{i }. {server['Name']} ({server['Address']})")

    def add_server(self, address):
        name = input('Enter the name of the server: ')
        server = {'Name': name, 'Address': address}
        self.servers.append(server)
        self.save_data()
        print(f"Server {name} ({address}) added.")

    def remove_server(self, index):
        index = int(index)
        if 0 <= index < len(self.servers):
            server = self.servers.pop(index)
            self.save_data()
            print(f"Server {server['Name']} ({server['Address']}) removed.")
        else:
            print(f"Invalid index: {index}")
