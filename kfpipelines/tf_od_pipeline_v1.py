"""
Kubeflow Pipeline to run OD training
"""
import os
import os.path as op

from kfp import dsl, components
import kfp.gcp as gcp
from kubernetes.client import V1Toleration

#######################################
# Load custom components
#######################################

###################
# Train Op
comp_train_fname = op.join('components', 'od_train', 'component.yaml')
train_component = components.load_component(filename=comp_train_fname)

###################
# Export Op
comp_export_fname = op.join('components', 'od_export', 'component.yaml')
export_component = components.load_component(filename=comp_export_fname)

########################################
# Define a toleration to a ML node taint 
ml_tol = V1Toleration(effect='NoSchedule', key='mlUseOnly', operator='Equal', value='true')

@dsl.pipeline(name='OD API training/export',
              description='A pipeline to train/export an instance segmentation model.')
def divot_detect_pipeline(
        pipeline_config_path,
        model_dir,
        eval_dir,
        inference_output_directory,
        num_train_steps=10000,
        sample_1_of_n_eval_examples=1,
        inference_input_type='encoded_image_string_tensor',
        eval_checkpoint_metric='loss',
        metric_objective_type='min'):
    """Object detection Kubeflow pipeline."""

    #############
    # Train the model
    train_op = train_component(pipeline_config_path,
                               model_dir,
                               num_train_steps,
                               sample_1_of_n_eval_examples,
                               eval_dir,
                               eval_checkpoint_metric,
                               metric_objective_type).set_gpu_limit(1)
    train_op.add_resource_limit('nvidia.com/gpu', 1)  # `limit` will automatically get mirrored for resource_request
    train_op.add_toleration(ml_tol)  # Add a toleration to our custom ML node taint (so only ML workloads get put on GPUS)
    train_op.add_resource_request('memory', '20Gi')
    train_op.add_resource_limit('memory', '45Gi')
    train_op.set_image_pull_policy('Always')
    train_op.apply(gcp.use_gcp_secret('user-gcp-sa'))


    #############
    # Export model
    export_op = export_component(inference_input_type,
                                 pipeline_config_path,
                                 train_op.outputs['best_checkpoint'],
                                 inference_output_directory).set_gpu_limit(1).after(train_op)
    export_op.add_resource_limit('nvidia.com/gpu', 1)  # `limit` will automatically get mirrored for resource_request
    export_op.add_toleration(ml_tol)  # Add a toleration to our custom ML node taint (so only ML workloads get put on GPUS)
    export_op.add_resource_request('memory', '2Gi')
    export_op.add_resource_limit('memory', '3Gi')
    export_op.set_image_pull_policy('Always')
    export_op.apply(gcp.use_gcp_secret('user-gcp-sa'))


if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(divot_detect_pipeline, __file__ + 'v1_sub.tar.gz')