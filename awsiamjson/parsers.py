from .logger import *
import requests
import re
from lxml import html

_logger = get_logger(__name__)


def add_services(input_dict):
    _logger.info("Retrieving Service Listing...")
    base_url = 'http://docs.aws.amazon.com/IAM/latest/UserGuide/'
    page = requests.get(base_url + 'reference_policies_actionsconditions.html')
    _logger.info("Parsing Service Listing...")
    tree = html.fromstring(page.content)
    aws_services = tree.xpath('//*[@id="main-col-body"]/div[@class="highlights"]/ul/li/a')
    services = {}
    for cur_service in aws_services:
        short_name = re.search(r"list_(.+).html", cur_service.attrib['href']).group(1).lower()
        if short_name != "s3":
            continue
        if cur_service.text not in services:
            services[short_name] = {}
            services[short_name]['Name'] = cur_service.text
            services[short_name]['URL'] = base_url + cur_service.attrib['href']
    input_dict['services'] = services
    return input_dict

def add_actions_and_context_keys(input_dict):
    for name, service in input_dict['services'].items():
        _logger.info("Retrieving Service IAM Page: {0}".format(service['Name']))
        page = requests.get(service['URL'])
        tree = html.fromstring(page.content)
        title = tree.xpath('//h1[@class="topictitle"][1]')[0]
        if title.text != ("Actions and Condition Context Keys for " + service['Name']):
            raise ValueError('Actions and Conditions page title did not match')
        code_elements = tree.xpath('//*[@id="main-col-body"]/div[@class="itemizedlist"]/ul/li/p/code')
        for cur_code in code_elements:
            inner_link = cur_code.find('a')
            if inner_link is None:
                # This is a Context Key
                if 'ContextKeys' not in service:
                    service['ContextKeys'] = []
                service['ContextKeys'].append(cur_code.text)
            else:
                # This is an Action
                if 'Actions' not in service:
                    service['Actions'] = {}
                service['Actions'][inner_link.text] = {}
                service['Actions'][inner_link.text]['URL'] = inner_link.attrib['href']
    return input_dict
