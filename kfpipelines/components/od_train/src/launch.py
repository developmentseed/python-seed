"""
Launcher to kick off model training within Kubeflow Pipelines.
"""

import sys
import os
import os.path as op
import json
import subprocess

import numpy as np
import tensorflow as tf
from absl import flags, app, logging

flags.DEFINE_string('pipeline_config_path', None, 'Local or GCS path to the OD model config.')
flags.DEFINE_string('model_dir', None, 'Local or GCS path to location for saving model checkpoints.')
flags.DEFINE_integer('num_train_steps', None, 'Total number of training steps to take.')
flags.DEFINE_integer('sample_1_of_n_eval_examples', None,
                     'During evaluation, sample 1/n of the total samples. E.g., "4" means use a quarter of the samples.')
flags.DEFINE_string('eval_dir', None, 'Local or GCS path to location for evaluation. Usually `model_dir/eval_0`')
flags.DEFINE_string('eval_checkpoint_metric', None, 'Name of loss metric used  to select the best checkpoint.')
flags.DEFINE_enum('metric_objective_type', None, ['min', 'max'], 'Select `eval_checkpoint_metric` based on `max` or `min`.')

FLAGS = flags.FLAGS


def init_tensorboard(model_dir):
    """Write necessary json file to initialize the launch of Tensorboard"""
    logging.info('Initializing tensorboard directory.')
    metadata = {'outputs' : [{'type': 'tensorboard', 'source': model_dir}]}

    with open('/mlpipeline-ui-metadata.json', 'w') as f:
        json.dump(metadata, f)

    logging.info('Finished initializing tensorboard directory.')


def run_training(pipeline_config_path, model_dir, num_train_steps,
                 sample_1_of_n_eval_examples):
    """Run a complete training experiment for TF's OD API"""

    logging.info('Starting model training process.')
    with subprocess.Popen(['python', '/tensorflow/models/research/object_detection/model_main.py',
                           '--pipeline_config_path', pipeline_config_path,
                           '--model_dir', model_dir,
                           '--num_train_steps', str(num_train_steps),  # Popen takes only string inputs
                           '--sample_1_of_n_eval_examples', str(sample_1_of_n_eval_examples),
                           '--alsologtostderr'],
                          bufsize=1,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          universal_newlines=True) as proc:

        for line in proc.stderr:
            print(line, end='')
        for line in proc.stdout:
            print(line, end='')

    if proc.returncode != 0:
        raise RuntimeError(f'Error at runtime with code: {proc.returncode}.')
    else:
        print('Finished training successfully.')


def identify_best_checkpoint(metric_name, objective_type, ckpt_dir):
    """Find the best checkpoint path based on a metric of interest"""

    metric_vals = []
    checkpoint_names = []

    logging.info('Identifying best checkpoint.')

    # Find fpath of TF Events file annd make sure there's only 1
    if not tf.io.gfile.isdir(ckpt_dir):
        raise ValueError(f'Could not find checkpoint directory for evaluation: {ckpt_dir}')
    event_paths = [op.join(ckpt_dir, fname) for fname in
                   tf.io.gfile.listdir(ckpt_dir) if 'tfevents' in fname]
    if not len(event_paths) == 1:
        raise RuntimeError(f'Found incorrect number of TF Events files: {event_paths}. Require only 1.')

    # Iterate through all tensorboard events looking for metric of interest
    for e in tf.train.summary_iterator(event_paths[0]):
        for v in e.summary.value:
            if v.tag == metric_name:
                metric_vals.append(v.simple_value)
            if v.tag == 'checkpoint_path':
                checkpoint_names.append(v.tensor.string_val[0].decode('utf-8'))

    # Find checkpoint fpath based on min or max
    best_ind = np.argmax(metric_vals) if objective_type == 'max' else np.argmin(metric_vals)
    best_perf = {'metrics': [{'name': metric_name,
                              'numberValue': metric_vals[best_ind]}]}

    logging.info('Returning best checkpoint name.')

    return checkpoint_names[best_ind], best_perf


def main(_):

    logging.info('Flags:')
    for temp_flag in FLAGS.get_key_flags_for_module(sys.argv[0]):
        logging.info(f'\t{temp_flag.name}: {temp_flag.value}')

    # Write the json file needed to kick off TensorBoard
    init_tensorboard(FLAGS.model_dir)

    # Run training
    run_training(pipeline_config_path=FLAGS.pipeline_config_path,
                 model_dir=FLAGS.model_dir,
                 num_train_steps=FLAGS.num_train_steps,
                 sample_1_of_n_eval_examples=FLAGS.sample_1_of_n_eval_examples)

    # Get the best checkpoint and its performance
    best_ckpt, best_perf = \
            identify_best_checkpoint(metric_name=FLAGS.eval_checkpoint_metric,
                                     objective_type=FLAGS.metric_objective_type,
                                     ckpt_dir=FLAGS.eval_dir)

    # Write the best checkpoint to disk
    logging.info(f'Best checkpoint file: {best_ckpt}')
    with open('/output.txt', 'w') as f:
        f.write(best_ckpt)

    # Write metrics to disk
    logging.info(f'Performance at best checkpoint: {best_perf}')
    with open('/mlpipeline-metrics.json', 'w') as f:
        json.dump(best_perf, f)


if __name__ == '__main__':
    app.run(main)
