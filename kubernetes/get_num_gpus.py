# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 15:54:45 2016

@author: lanlin
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json
from jsonpath_rw import parse

def main(args):
    info = json.loads(args.out_json)
    jsonpath_expr = parse(
        'items[*].status.allocatable.["alpha.kubernetes.io/nvidia-gpu"]')
    num_gpus = [int(match.value) for match in jsonpath_expr.find(info)]
    print(sum(num_gpus))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="")
    
    parser.add_argument(
        "--out_json")
        
    args = parser.parse_args()
    main(args)
