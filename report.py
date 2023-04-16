import json
from jinja2 import Environment, FileSystemLoader, PackageLoader

class Report:
    def __init__(self):
        # self.name = name
        # self.address = address
        # self.status = status
        self.data_file = "report.json"
    
    def read_data(self):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        # Convert each server to a dictionary with keys 'name', 'address', and 'status'
        formatted_data = []
        for server in data:
            name_key = 'Name' if 'Name' in server else 'name'
            address_key = 'Address' if 'Address' in server else 'address'
            status_key = 'Status' if 'Status' in server else 'status'
            formatted_data.append({'Name': server[name_key], 'Address': server[address_key], 'Status': server[status_key]})
        return formatted_data
        
    def add_server(self, name, address, status):
        data = self.read_data()
        data.append({'Name': name, 'Address': address, 'Status': status})
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

    def generate_html(self):
        data = self.read_data()
        fileLoader = FileSystemLoader("templates")
        env = Environment(loader=fileLoader)

        template = env.get_template("index.html")
        rendered = template.render(servers=data)

        with open(f"./site/index.html", "w") as q:
            q.write(rendered)        
            
    def read_report_data(self):
        try:
            with open(self.data_file, 'r') as file:
                report_data = json.load(file)
        except FileNotFoundError:
            report_data = []
        return report_data
    
