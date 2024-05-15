# Welcome to Calra Simple Example CDK Python project!

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

Deploy

```
$ cdk deploy
```

Destroy

```
$ cdk destroy
```

## Use of CALRA inside a CDK Python project!

Adding [calra-cdk](https://pypi.org/project/calra-cdk/) inside your CDK Stack can simplify the creation of resources for AWS Lambda Functions and Rest API resources. You can set default, common or custom values for IAM Roles, Runtimes, Timeouts, Layers, Environment values, VPCs and Security Groups.

On the same note, [calra-lambda](https://pypi.org/project/calra-lambda/) is used to give annotations to each Lambda Function. This annotation, in the format of decorators provided by the package, will help you set custom values, descriptions, and the HTTP Method the API Gateway will create the resource for.

Over this Simple Example, we'll se a bare minimun configuration of an example Stack using the CALRA packages, so you can get the grasp of how feasible it is to automate the creation of your Lambdas and Rest API resources.

On calra_example/calra_example_stack.py

```python
    [...] # Other Imports
    from calra_cdk import ResourceBuilder
    class CalraExampleStack(Stack):

        def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
            super().__init__(scope, construct_id, **kwargs)

            builder = ResourceBuilder()
            lambda_path = 'lambdas'

            restapi = apigateway.RestApi(
                self, 'calra-RestApi',
                rest_api_name= 'calra-restApi')
            root_resource = restapi.root

            builder.set_default_timeout(Duration.seconds(60))
            builder.set_default_runtime(_lambda.Runtime.PYTHON_3_10)
            builder.add_common_environment("URL", "http://example.com")
            builder.add_custom_environment("DB_NAME_CATS", "cats")
            builder.add_custom_environment("DB_NAME_DOGS", "dogs")

            builder.build(self, root_resource, lambda_path, print_tree=True)
```

Over this example, we defined a ResourceBuilder instance and then added some basic configuration, setting a default timeout that every Lambda will be assigned if not overriden with a custom value. Then some other defaults like runtime and one common and two customs environment variables.

Secondly, our lambda directory consists of one index.py file with two lambda handlers.

On lambdas/index.py

```python
    [...] # Other Imports
    from calra_lambda import *

    @GET('/dogs')
    @runtime('python3.11')
    @name('LBD-DOGS-GET')
    @memory_size(256)
    def lambda_handler(event, context):
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Hello World from /dogs!'
            })
        }
        return response

    @GET('/cats')
    @environment('DB_NAME_CATS')
    @description("This Lambda implements functionality for the CATS service")
    @timeout(30)
    @name('LBD-CATS-GET')
    def cat_handler(event, context):
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': f"Hello from cats handler GET. There is a custom environment called DB_NAME_CATS of value.. {os.environ['DB_NAME_CATS']}"
            })
        }
        return response
```

You can easily identify the decorators assigned to each handler. First, the /dogs GET endpoint will run on a predefined custom runtime with python3.11, opposed to the default specified before python3.10. Keep in mind there are predefined custom runtimes going from 'python3.8' to 'python3.12'. This handler also receives a custom memory size of 256 and a name.

Secondly, the /cats GET endpoint will be assigned the cat_handler with a timeout of 30s and a custom environment variable among other things such as name and description. Finally the default timeout of 60 is overriden with a custom timeout of 30 seconds.

So, our REST API will have a tree structure of:

```
    /
        /dogs (GET)
        /cats (GET)
```

In this simple example we saw how some configuration and annotation can relieve us from a lot of defining and writing Constructs for Lambda and Rest API resources in a scalable manner, keeping your stack code clean while also adding custom configuration to fit the needs of each Lambda.

Please feel free to use this example as a model to start using CALRA packages as solutions for your needs regarding Lambda and Rest API resource creation and personalization.
