#!/usr/bin/env python3

import os
import sys
import json
import logging
import argparse
import shutil

from system_data import sys_info
from docker_data import calc_cpu, calc_cpu2, calc_blkio_bytes,\
        calc_network_bytes, cb, container_stats

logger = logging.getLogger(__name__)

big_explorer_version = "0.1.1"
big_explorer_output_version = "0.1.1"

def env_var():
    for k, v in os.environ.items():
        yield(f'{k}: {v}')


def progressBar(iteration,total,prefix='',suffix='',decimals=1,length=50,
                fill='█',printEnd="\r"):
    """
    Call in a looop to create terminal progress bar
    @params:
    iteration   -   Required : current iteration (int)
    total       -   Required : total iterations (int)
    prefix      -   Optional : prefix string (Str)
    suffix      -   Optional : suffix string (Str)
    decimas     -   Optional : positive number of decimals in percent
                               complete (int)
    length      -   Optional : character length of bar (int)
    printEnd    -   Optoinal : end character (e.g. "\r","\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * \
                                                     (iteration/float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print new Line on Complete
    if iteration == total:
        print()


def main():
    tmp_output_dir = "./big_explorer_output"
    output_zip_filename = "./big_explorer_output.zip"
    try:
        os.mkdir(tmp_output_dir)
    except OSError:
        # Don't worry about the error if the dir exists. We can always use
        # the existing data!
        print ("")

    parser = argparse.ArgumentParser(
            description="BigID System Data Aggregator"
            )
    parser.add_argument(
            "-c", "--containers", action="store_true", default=None,
            help="Collect Docker statistics for BigID containers"
            )
    parser.add_argument(
            "-s", "--system", action="store_true", default=None,
            help="Collect Application Server system details"
            )
    parser.add_argument(
            "-d", "--datasource", action="store_true", default=None,
            help="Export Data Source configuration details"
            )
    parser.add_argument(
            "-e", "--correlationset", action="store_true", default=None,
            help="Export Correlation Set Configuration details"
            )
    parser.add_argument(
            "-j", "--dsar", action="store_true", default=None,
            help="Export DSAR configuration details"
            )
    parser.add_argument(
            "-a", "--all", action="store_true", default=None,
            help="Collect all data"
            )
    #parser.add_argument(
            #"-l", "--logs", action="store_true", default=None,
            #help="Export BigID Service logs"
            #)


    args = parser.parse_args()

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # May need to check that the length corresponds only to the number of arg
    i, l = 0, len(vars(args))

    if args.system:
        from bigid_data import bigid_release, config
        print("\nFetching System Information...")
        env_data = {
            'bigid_release': bigid_release(),
            'system_information': list(sys_info()),
            'environment_variables': list(env_var())
        }
        # Export Environment Information
        with open(tmp_output_dir + '/environment.json', 'w', \
                  encoding='utf-8') as f:
            json.dump(env_data, f, ensure_ascii=False, indent=4)
        i = l
        progressBar(i, l)

    if args.datasource:
        from bigid_data import config
        print("\nFetching Data Source Configuration...")
        # Export Data Sources
        with open(tmp_output_dir + '/ds_configuration.json', 'w', \
                  encoding='utf-8') as f:
            json.dump(config("ds_connections"), f, ensure_ascii=False,
                      indent=4)
        i = l
        progressBar(i, l)

    if args.correlationset:
        from bigid_data import config
        print("\nFetching Correlation Set Configuration...")
        # Export Correlation Set
        with open(tmp_output_dir + '/cs_configuration.json', 'w', \
                  encoding='utf-8') as f:
            json.dump(config("id_connections"), f, ensure_ascii=False,\
                      indent=4)
        i = l
        progressBar(i, l)

    if args.dsar:
        from bigid_data import config
        print("\nFetching SAR Configuration...")
        # Export DSAR configuration
        with open(tmp_output_dir + '/sar_configuration.json', 'w', \
                  encoding='utf-8') as f:
            json.dump(config("sar/config"), f, ensure_ascii=False,\
                       indent=4)
        i = l
        progressBar(i, l)

    if args.containers:
        print("\nFetching Docker Containers Statistics...")
        # Export Container Information
        with open(tmp_output_dir + '/containers.json', 'w', \
                  encoding='utf-8') as f:
            json.dump(list(container_stats()), f, ensure_ascii=False, indent=4)
        i = l
        progressBar(i, l)

    #if args.logs:
        #from bigid_data import bigid_logs
        #print("\nFetching BigID Service Logs...")
        # Export Services logs
        #bigid_logs()
        #i = l
        #progressBar(i, l)

    if args.all:
        from bigid_data import bigid_release, config
        print("\nFetching System Information...")
        env_data = {
            'bigid_release': bigid_release(),
            'system_information': list(sys_info()),
            'environment_variables': list(env_var())
        }
        # Export Environment Information
        with open(tmp_output_dir + '/environment.json', 'w', \
                  encoding='utf-8') as f:
            json.dump(env_data, f, ensure_ascii=False, indent=4)
        i = l
        progressBar(i, l)
        
        from bigid_data import config
        print("\nFetching Data Source Configuration...")
        # Export Data Sources
        with open(tmp_output_dir + '/ds_configuration.json', 'w', \
                  encoding='utf-8') as f:
            json.dump(config("ds_connections"), f, ensure_ascii=False,
                      indent=4)
        i = l
        progressBar(i, l)
        
        from bigid_data import config
        print("\nFetching Correlation Set Configuration...")
        # Export Correlation Set
        with open(tmp_output_dir + '/cs_configuration.json', 'w', \
                  encoding='utf-8') as f:
            json.dump(config("id_connections"), f, ensure_ascii=False,\
                      indent=4)
        i = l
        progressBar(i, l)
        
        from bigid_data import config
        print("\nFetching SAR Configuration...")
        # Export DSAR configuration
        with open(tmp_output_dir + '/sar_configuration.json', 'w', \
                  encoding='utf-8') as f:
            json.dump(config("sar/config"), f, ensure_ascii=False,\
                       indent=4)
        i = l
        progressBar(i, l)
        
        print("\nFetching Docker Containers Statistics...")
        # Export Container Information
        with open(tmp_output_dir + '/containers.json', 'w', \
                  encoding='utf-8') as f:
            json.dump(list(container_stats()), f, ensure_ascii=False, indent=4)
        i = l
        progressBar(i, l)

    shutil.make_archive("big_explorer_output", 'zip', tmp_output_dir)

    # rm the the tmp output dir
    try:
        shutil.rmtree(tmp_output_dir)
    except OSError:
        # Who cares?
        print ("")


if __name__ == "__main__":
    sys.exit(main())
