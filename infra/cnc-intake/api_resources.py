"""Scope: Expose only scoped JWT-authorized HTTP routes to the intake Lambda."""


class ApiResources:
    def resources(self):
        resources = {
            "Api": {"Type": "AWS::ApiGatewayV2::Api", "Properties": {"Name": "aikea-cnc-intake", "ProtocolType": "HTTP",
                                                                       "Tags": {"Service": "aikea-cnc-intake"}}},
            "Authorizer": {"Type": "AWS::ApiGatewayV2::Authorizer", "Properties": {
                "ApiId": {"Ref": "Api"}, "Name": "AIkeaUser", "AuthorizerType": "JWT",
                "IdentitySource": ["$request.header.Authorization"], "JwtConfiguration": {
                    "Audience": [{"Ref": "Client"}],
                    "Issuer": {"Fn::Sub": "https://cognito-idp.${AWS::Region}.amazonaws.com/${UserPool}"}}}},
            "Integration": {"Type": "AWS::ApiGatewayV2::Integration", "Properties": {
                "ApiId": {"Ref": "Api"}, "IntegrationType": "AWS_PROXY", "PayloadFormatVersion": "2.0",
                "IntegrationUri": {"Fn::GetAtt": ["Gateway", "Arn"]}, "TimeoutInMillis": 29000}},
            "Stage": {"Type": "AWS::ApiGatewayV2::Stage", "Properties": {
                "ApiId": {"Ref": "Api"}, "StageName": "$default", "AutoDeploy": True,
                "DefaultRouteSettings": {"ThrottlingBurstLimit": 5, "ThrottlingRateLimit": 2}}},
            "Invoke": {"Type": "AWS::Lambda::Permission", "Properties": {
                "FunctionName": {"Ref": "Gateway"}, "Action": "lambda:InvokeFunction",
                "Principal": "apigateway.amazonaws.com", "SourceAccount": {"Ref": "AWS::AccountId"},
                "SourceArn": {"Fn::Sub": "arn:${AWS::Partition}:execute-api:${AWS::Region}:${AWS::AccountId}:${Api}/*/POST/requests*"}}},
        }
        for name, route in {"BeginRoute": "POST /requests", "CompleteRoute": "POST /requests/{request_id}/complete"}.items():
            resources[name] = {"Type": "AWS::ApiGatewayV2::Route", "Properties": {
                "ApiId": {"Ref": "Api"}, "RouteKey": route, "AuthorizationType": "JWT",
                "AuthorizerId": {"Ref": "Authorizer"}, "AuthorizationScopes": ["aikea/submit"],
                "Target": {"Fn::Join": ["/", ["integrations", {"Ref": "Integration"}]]}}}
        return resources
