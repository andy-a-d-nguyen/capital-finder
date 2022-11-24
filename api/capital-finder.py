from http.server import BaseHTTPRequestHandler
from urllib import parse

import requests


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        url_components = parse.urlsplit(path)
        query_string_list = parse.parse_qsl(url_components.query)
        params = dict(query_string_list)

        if "country" in params:
            request_url = f"https://restcountries.com/v3.1/name/{params['country']}"
            response = requests.get(request_url)
            if response.status_code == 200:
                data = response.json()
                capital = data[0]["capital"][0]
                message = f"The capital of {params['country'].capitalize()} is {capital}"
            else:
                message = "This is an invalid country. Please try again with a valid country"

        elif "capital" in params:
            request_url = f"https://restcountries.com/v3.1/capital/{params['capital']}"
            response = requests.get(request_url)
            if response.status_code == 200:
                data = response.json()
                country = data[0]["name"]["common"]
                message = f"{params['capital'].capitalize()} is the capital of {country}"
            else:
                message = "This is an invalid capital. Please try again with a valid capital"

        else:
            message = "Please use the endpoint in this format: " + \
                      "capital-finder?country={country name} or " + \
                      "capital-finder?capital={capital name}"

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode())
        return
