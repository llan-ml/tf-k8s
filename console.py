# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 16:46:10 2016

@author: lanlin
"""

import os
import argparse
import yaml

HOME = os.environ.get("HOME")

def main(args):
    with open(args.config, "r") as f:
        config = yaml.load(f)
    try:
        k8s_config = config["kubernetes"]
    except KeyError:
        k8s_config = {}
    try:
        tf_config = config["tensorflow"]
    except KeyError:
        tf_config = {}
    
    k8s_args = ["--{} \"{}\"".format(key, value)
        for key, value in k8s_config.iteritems()]
    k8s_args = " ".join(k8s_args) if k8s_args else ""
    tf_args = [(key, value) for key, value in tf_config.iteritems()]
    tf_args = "--parameters \"{}\"".format(tf_args) if tf_args else ""
    render_args = "{} {}".format(k8s_args, tf_args)
    
    os.system("python ./kubernetes/render.py {}".format(render_args))
    copy_files = ["./tensorflow/distribute_tf.py"]
    if "user_model_file" not in tf_config.keys() \
        or tf_config["user_model_file"] == "example_user_model.py":
        copy_files.append("./examples/example_user_model.py")

    work_dir = HOME + "/GPU_cluster_storage/{}/{}".format(
                                                k8s_config["namespace"],
                                                k8s_config["name"])

    os.system("cp {} {}".format(" ".join(copy_files), work_dir))
    os.system("cp {} {}/k8s_config".format("./kubernetes/get_num_gpus.py", work_dir))
    os.system("chmod +x {}/start_cluster.sh".format(work_dir))
    os.system("chmod +x {}/stop_cluster.sh".format(work_dir))
    os.system("chmod +x {}/start_tensorboard.sh".format(work_dir))
    os.system("chmod +x {}/stop_tensorboard.sh".format(work_dir))
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="")
        
    parser.add_argument(
        "--config",
        default="./examples/example_config.yaml")
    
    args = parser.parse_args()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    config=main(args)
