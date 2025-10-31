"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 1.0.0
"""

from kedro.pipeline import Node, Pipeline, pipeline

from .nodes import split_data, train_model, evaluate_model

def create_pipeline(**kwargs) -> Pipeline:
    pipeline_instance = Pipeline([
        Node(
            func= split_data,
            inputs= ["model_input_table", "params:model_options"],
            outputs= ["X_train", "X_test", "y_train", "y_test"],
            name= "split_data_node",
        ),
        Node(
            func= train_model,
            inputs = ["X_train", "y_train"],
            outputs= "regressor",
            name= "train_model_node",
        ),
        Node(
            func= evaluate_model,
            inputs= ["regressor", "X_test", "y_test"],
            outputs= None,
            name= "evaluate_model_node"
        ),
    ])

    ds_pipeline_1 = pipeline(
        pipeline_instance,
        inputs = "model_input_table",
        namespace = "active_modelling_pipeline",
    )

    ds_pipeline_2 = pipeline(
        pipeline_instance,
        inputs = "model_input_table",
        namespace = "candidate_modelling_pipeline",
    )

    return ds_pipeline_1 + ds_pipeline_2