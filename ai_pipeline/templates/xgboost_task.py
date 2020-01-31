# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Executes model training and evaluation."""

import argparse
import logging
import os
import sys
import xgboost as xgb

from trainer import model
from trainer import utils
from {{model_path}} import get_data


def _parse_arguments(argv):
    """Parses execution arguments and replaces default values.

    Args:
      argv: Input arguments from sys.

    Returns:
      Dictionary of parsed arguments.
    """
    parser = argparse.ArgumentParser()
    {% for arg in args %}
    parser.add_argument(
        "--{{arg.name}}",
        help="{{arg.help}}",
        default="{{arg.default}}")
    {% endfor %}
    args, _ = parser.parse_known_args(args=argv[1:])
    return args


def _train_and_evaluate(estimator, dataset, output_dir):
    """Runs model training and evaluation."""
    x_train, y_train = dataset
    estimator.fit(x_train, y_train)

    model_output_path = os.path.join(output_dir, "model.joblib")
    utils.dump_object(estimator, model_output_path)
    print("Model written to {}".format(model_output_path))


def run_experiment(args):
    """Testbed for running model training and evaluation."""
    dataset = get_data()
    estimator = model.get_estimator(args)
    _train_and_evaluate(estimator, dataset, args.model_dir)


def main():
    """Entry point."""
    args = _parse_arguments(sys.argv)
    logging.basicConfig(level="INFO")
    run_experiment(args)


if __name__ == "__main__":
    main()