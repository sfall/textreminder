import json


def convert(number, carrier):
    with open('gateways.json') as f:
        gateways = json.load(f)
    template = gateways[carrier]
    return template.format(number=number)