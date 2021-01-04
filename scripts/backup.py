import datetime
import json
import os
import re
import shutil
import sys
from os.path import basename
from zipfile import ZipFile

import requests
from bump import run_commands, print_lines

database_regex = re.compile(r'===\sBackup\s(\w+)')
database_type_regex = re.compile(r'Database:\s+(DATABASE)')
started_regex = re.compile(r'Started\sat:\s+(20\d{2}\-\d{2}\-\d{2}\s\d{2}:\d{2}:\d{2}\s\+0000)')
finished_regex = re.compile(r'Finished\sat:\s+(20\d{2}\-\d{2}\-\d{2}\s\d{2}:\d{2}:\d{2}\s\+0000)')
status_regex = re.compile(r'Status:\s+(Completed)')
type_regex = re.compile(r'Type:\s+(Manual)')
original_size_regex = re.compile(r'Original\sDB\sSize:\s+(\d+\.\d{2}[KMGT]?B)')
size_regex = re.compile(r'Backup\sSize:\s+(\d+\.\d{2}[KMGT]?B)\s\(\d+%\scompression\)')

info_regexps = dict()
info_regexps['name'] = {'regexp': database_regex, 'line': 0}
info_regexps['type'] = {'regexp': database_type_regex, 'line': 1}
info_regexps['started_at'] = {'regexp': started_regex, 'line': 2}
info_regexps['finished_at'] = {'regexp': finished_regex, 'line': 3}
info_regexps['status'] = {'regexp': status_regex, 'line': 4}
info_regexps['backup_type'] = {'regexp': type_regex, 'line': 5}
info_regexps['original_size'] = {'regexp': original_size_regex, 'line': 6}
info_regexps['backup_size'] = {'regexp': size_regex, 'line': 7}

ENVIRONMENTS = {
    'production': {
        'app_name': 'rec-demo',
        'folder': 'rec_demo_prod',
        'base_url': 'https://rec-demo.herokuapp.com'
    },
    'staging': {
        'app_name': 'rec-demo-staging',
        'folder': 'rec_demo_staging',
        'base_url': 'https://rec-demo-staging.herokuapp.com'
    },
}


def parse_backup(lines):
    # --------------------------------------------------------------------------------
    # Errors
    # --------------------------------------------------------------------------------
    # Line 1: Starting backup of postgresql-perpendicular-69325... done
    # Line 2: Backing up DATABASE to b006... done

    regexp = re.compile(r'Backing\sup\sDATABASE\sto\s(\w+)\.\.\. (\w+)')
    match = regexp.match(lines[1])
    if match:
        return match.group(1), match.group(2) == 'done'
    else:
        return None, False


def parse_info(lines):
    metadata = dict()
    for attribute in info_regexps.keys():
        metadata[attribute] = ''
        match = info_regexps[attribute]['regexp'].match(lines[info_regexps[attribute]['line']])
        if match:
            metadata[attribute] = match.group(1)

    return metadata


def metadata_is_valid(database_name, metadata):
    names = database_name == metadata['name']
    status = metadata['status'] == 'Completed'
    has_blanks = False
    for attribute in metadata.keys():
        has_blanks = metadata[attribute] == ''
        if has_blanks:
            break
    return names and status and not has_blanks


def parse_download(lines):
    regexp = re.compile(r'Getting\sbackup\sfrom\s([a-z\-]+)\.\.\.\s([a-z\-]+),\s#\d+')
    match = regexp.match(lines[1])
    if match:
        return match.group(1), match.group(2)
    else:
        return None, None


def get_version_number(url):
    response = requests.get(url)
    data = response.json()
    return data['version']


if __name__ == '__main__':
    DROPBOX_FOLDER = '/Users/luiscberrocal/Dropbox/Temp'
    DEFAULT_BACKUP_NAME = 'latest.dump'
    VERSION_URL = 'api/v1/app-data/'

    import argparse

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--env", required=False, help="Environment to backup")
    ap.add_argument("-v", "--verbose", required=False, help="Print results", default=False)

    args = vars(ap.parse_args())
    environment = args.get('env')
    verbose = args.get('verbose')

    if environment is None:
        environment = 'staging'
    elif environment == 'prod':
        environment = 'production'

    version = get_version_number(ENVIRONMENTS[environment]['base_url'] + '/' + VERSION_URL)

    app = ENVIRONMENTS[environment]['app_name']
    now = datetime.datetime.now()

    base_filename = '{}_backup_{}_{}'.format(now.strftime('%Y%m%d_%H%M%S'), app, version)

    cmd = ['heroku', 'pg:backups:capture', '-a', app]
    results, errors = run_commands(cmd)
    if verbose:
        print_lines('Results Capture', results)
        print_lines('Errors Capture', errors)

    backup_name, success = parse_backup(errors)
    print('Backup: {}'.format(backup_name))
    print('Success: {}'.format(success))

    # print_lines('Results', results)
    print_lines('Errors', errors)

    cmd = ['heroku', 'pg:backups:info', '-a', app]
    results, errors = run_commands(cmd)
    if verbose:
        print_lines('Results Info', results)
        print_lines('Errors Info', errors)

    metadata = parse_info(results)
    metadata['app'] = app
    metadata['environment'] = environment
    metadata['version'] = version

    if verbose:
        print(metadata)

    is_valid = metadata_is_valid(backup_name, metadata)
    if is_valid:
        cmd = ['heroku', 'pg:backups:download', '-a', app]
        if verbose:
            print_lines('Results Download', results)
            print_lines('Errors Download', errors)
        results, errors = run_commands(cmd)
        metadata_file = os.path.join(DROPBOX_FOLDER, ENVIRONMENTS[environment]['folder'], base_filename + '.json')
        with open(metadata_file, 'w') as mf:
            json_metadata = json.dumps(metadata)
            mf.write(json_metadata)
        if not os.path.exists(metadata_file):
            sys.exit(100)
    else:
        sys.exit(101)

    app_name, status = parse_download(errors)
    print('App name: {}'.format(app_name))
    print('Status: {}'.format(status))

    backup_filename = os.path.join(DROPBOX_FOLDER, ENVIRONMENTS[environment]['folder'], base_filename + '.dump')

    shutil.move(DEFAULT_BACKUP_NAME, backup_filename)

    if not os.path.exists(backup_filename):
        sys.exit(102)

    zip_filename = os.path.join(DROPBOX_FOLDER, ENVIRONMENTS[environment]['folder'], base_filename + '.zip')

    with ZipFile(zip_filename, 'w') as zip:
        zip.write(backup_filename, basename(backup_filename))
        zip.write(metadata_file, basename(metadata_file))

    if not os.path.exists(zip_filename):
        sys.exit(103)

    os.remove(backup_filename)
    os.remove(metadata_file)

    print('Backup successful {}'.format(backup_filename))

    # print_lines('Results Info', results)
    # print_lines('Errors Info', errors)
# --------------------------------------------------------------------------------
# Errors
# --------------------------------------------------------------------------------
# Line 1: Starting backup of postgresql-perpendicular-69325... done
# Line 2: Backing up DATABASE to b006... done

##Line 1: === Backup b006
# Line 2: Database:         DATABASE
# Line 3: Started at:       2019-12-28 21:23:40 +0000
# Line 4: Finished at:      2019-12-28 21:23:43 +0000
# Line 5: Status:           Completed
# Line 6: Type:             Manual
# Line 7: Original DB Size: 11.35MB
# Line 8: Backup Size:      178.13KB (98% compression)

# Errors
# --------------------------------------------------------------------------------
# Line 2: Getting backup from emr-practice-staging... done, #18
