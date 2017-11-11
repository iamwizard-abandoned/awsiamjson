from awsiamjson import *
import json

_logger = logger.get_logger(__name__)

def main():
    _logger.info("IAM Wizard - AWS IAM JSON - Version 0.1")
    output_object = {}
    output_object = add_services(output_object)
    print(json.dumps(output_object, sort_keys=True, indent=4))
    _logger.info("Exiting...")

if __name__ == '__main__':
    main()