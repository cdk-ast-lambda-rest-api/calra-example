from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as _lambda_python,
    aws_apigateway as apigateway,
)
from calra_cdk import ResourceBuilder
from constructs import Construct

class CalraExampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        builder = ResourceBuilder()
        lambda_path = 'lambdas'

        restapi = apigateway.RestApi(
            self, 'calra-RestApi',
            rest_api_name= 'calra-restApi')
        root_resource = restapi.root

        layer = _lambda_python.PythonLayerVersion(
            self, "calra-lambda",
            entry="./layers/calra_lambda",
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_10, _lambda.Runtime.PYTHON_3_11]
        )
        builder.add_common_layer(layer)


        default_role = iam.Role(
            self, "calra-role",
            assumed_by= iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies= [
                iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')            
            ]
        )
        builder.set_default_role(default_role)

        builder.set_default_timeout(Duration.seconds(60))
        builder.set_default_runtime(_lambda.Runtime.PYTHON_3_10)
        builder.add_common_environment("URL", "http://example.com")
        builder.add_custom_environment("DB_NAME_CATS", "cats")
        builder.add_custom_environment("DB_NAME_DOGS", "dogs")

        builder.build(self, root_resource, lambda_path, print_tree=True)