import pysistence as imm

CONFIG_FILE = 'config.ini'
_config = None

def globalConfig():
    global _config
    assert type(_config) is imm.persistent_dict.PDict, type(_config)
    return _config

def parseCLI(argv):
    import argparse
    from parse import makeDir
    import os
    parser = argparse.ArgumentParser(description='Scarpa the scraper.')
    parser.add_argument('--domain', '-d', type=str, default='', help='regex of the main domain')
    parser.add_argument('--url', '-u', type=str, default='', help='initial url to request')
    parser.add_argument('--project-dir', '-p', type=str, default='', help='path of the project directory')
    parser.add_argument('--level', '-l', type=int, default=-1, help='recur for [n] levels for the main domain')
    parser.add_argument('--external-level', '-e', type=int, default=-1,  help='recur for [n] levels for the external domain')
    parser.add_argument('--check-after-save', type=bool, default=False, help='check if a file can be parsed after save')
    parser.add_argument('--log', '-L', type=str, default='scarpa.errlog', help='location of the log file')
    parser.add_argument('--resume', type=str, default='', help='resume a project')
    args = vars(parser.parse_args(argv))

    if args['resume'] == '' and args['project_dir'] == '' and args['url'] == '':
        raise Exception('please specify an action, --help for more information')

    if args['resume'] != '':
        if args['project_dir'] != '':
            loadConfig(args['project_dir'] + CONFIG_FILE)
        else:
            loadConfig(CONFIG_FILE)
    else:
        if os.path.isabs(args['project_dir']):
            args['project_dir'] = os.path.abspath(args['project_dir'])
        if not args['project_dir'].endswith('/'):
            args['project_dir'] += '/'
        if args['domain'] == '':
            args['domain'] = args['url']

    if args['project_dir'] == '':
        raise Exception('invalid project directory')
    if args['url'] == '':
        raise Exception('invalid url')
    
    if args['resume']:
        print('resume this project')
        loadConfig(args['project_dir'])
    else:
        makeDir(args['project_dir'])
        global _config
        _config = imm.make_dict(args)
        dumpConfig(args['project_dir'])


def dumpConfig(configFilePath):
    import configparser as cp
    config = cp.ConfigParser()
    config['CONFIG'] = globalConfig()
    with open(configFilePath + CONFIG_FILE, 'w') as f:
        config.write(f)

def loadConfig(configFilePath):
    import configparser as cp
    config = cp.ConfigParser()
    config.section()
    _config = cp.read(configFilePath + CONFIG_FILE)
