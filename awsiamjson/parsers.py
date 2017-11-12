from .logger import *
import requests
import re
from lxml import html, etree

_logger = get_logger(__name__)


def add_services(input_dict):
    _logger.debug("Retrieving Service Listing...")
    base_url = 'http://docs.aws.amazon.com/IAM/latest/UserGuide/'
    page = requests.get(base_url + 'reference_policies_actionsconditions.html')
    _logger.debug("Parsing Service Listing...")
    tree = html.fromstring(page.content)
    aws_services = tree.xpath('//*[@id="main-col-body"]/div[@class="highlights"]/ul/li/a')
    services = {}
    for cur_service in aws_services:
        short_name = re.search(r"list_(.+).html", cur_service.attrib['href']).group(1).lower()
        #if short_name != 's3' and short_name != 'execute-api' and short_name != 'datapipeline':
            #continue
        if cur_service.text not in services:
            services[short_name] = {}
            services[short_name]['Name'] = cur_service.text
            services[short_name]['URL'] = base_url + cur_service.attrib['href']
    input_dict['services'] = services
    return input_dict


def add_actions_and_context_keys(input_dict):
    for name, service in input_dict['services'].items():
        _logger.debug("Retrieving Service IAM Page: {0}".format(service['Name']))
        page = requests.get(service['URL'])
        tree = html.fromstring(page.content)
        title = tree.xpath('//h1[@class="topictitle"][1]')[0]
        if title.text != ("Actions and Condition Context Keys for " + service['Name']):
            raise ValueError('Actions and Conditions page title did not match')
        # Potential bug here if the whole document is on one/few lines...
        actions_title_line = tree.xpath(
            '//*[@id="main-col-body"]/p/b[contains(text(), "Actions for ' + service['Name'] + '")]'
        )[0].sourceline
        conditions_title_line = tree.xpath(
            '//*[@id="main-col-body"]/p/b[contains(text(), "Condition context keys for ' + service['Name'] + '")]'
        )[0].sourceline
        code_elements = tree.xpath('//*[@id="main-col-body"]/div[@class="itemizedlist"]/ul/li/p/code')
        for cur_code in code_elements:
            inner_link = cur_code.find('a')
            if inner_link is None:
                api_url = ''
                api_name = cur_code.text
            else:
                api_url = inner_link.attrib['href']
                api_name = inner_link.text
            if actions_title_line < cur_code.sourceline < conditions_title_line:
                api_type = 'Actions'
            elif cur_code.sourceline > conditions_title_line:
                api_type = 'Conditions'
            if api_type not in service:
                service[api_type] = {}
            service[api_type][api_name] = {}
            service[api_type][api_name]['URL'] = re.sub('\s+', ' ', api_url).strip()
    return input_dict


def add_api_descriptions(input_dict):
    for _, service in input_dict['services'].items():
        _logger.debug("Working on Service: {0}".format(service['Name']))
        if 'Actions' in service:
            for action_name, action in service['Actions'].items():
                _logger.debug("Working on Action: {0}".format(action_name))
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
        if 'Conditions' in service:
            for condition_name, condition in service['Conditions'].items():
                _logger.debug("Working on Condition: {0}".format(condition_name))
                if len(action['URL']) == 0:
                    condition['Title'] = 'No AWS Documentation'
                    condition['Description'] = 'No AWS Documentation'
                else:
                    condition['Title'] = 'No AWS Documentation'
                    condition['Description'] = 'No AWS Documentation'
    return input_dict
