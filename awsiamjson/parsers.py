from .logger import *
import requests
import re
from lxml import html, etree
import lxml.html, lxml.html.clean

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
        #if short_name != "s3":
            #continue
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


def add_api_descriptions(input_dict):
    for _, service in input_dict['services'].items():
        _logger.info("Working on Service: {0}".format(service['Name']))
        # TODO: There is still a bug here with API Actions without links
        if 'Actions' not in service:
            continue
        for action_name, action in service['Actions'].items():
            _logger.info("Working on Action: {0}".format(action_name))
            if len(action['URL']) == 0:
                # Documentation links are sometimes blank
                action['Title'] = 'No AWS Documentation'
                action['Description'] = 'No AWS Documentation'
                continue
            page = requests.get(action['URL'])
            tree = html.fromstring(page.content)
            title_element = tree.xpath('//h1[@class="topictitle"][1]')
            if len(title_element) == 0:
                # Documentation links are sometimes broken failing back to Service API Introduction page
                action['Title'] = 'No AWS Documentation'
                action['Description'] = 'No AWS Documentation'
                continue
            action['Title'] = title_element[0].text
            description_element = tree.xpath('//*[@id="main-col-body"]/p[1]')
            # Remove any tags within this HTML
            etree.strip_tags(description_element[0], "*")
            dirty_description = description_element[0].text
            # Remove redundant whitespace caused by HTML formatting
            action['Description'] = re.sub('\s+', ' ', dirty_description).strip()
    return input_dict
