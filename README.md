# IAM Wizard - Metadata Generator

Crawls the AWS IAM Documentation pages and generates a easily consumable JSON file describing AWS IAM Actions and
Conditions.

## Build Status

Coming soon!

## Usage

Simply run `__main__.py` and and output file `out/awsiam.json` will be produced.

Optionally modify the `output_override.json` file to override specific fields of the output file. This is useful when
the AWS documentation isn't consistently organized and you wish you manually specify documentation links or more useful
API descriptions.

## License

IAM Wizard - Metadata Generator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

IAM Wizard - Metadata Generator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with IAM Wizard - Metadata Generator.  If not, see <http://www.gnu.org/licenses/>.