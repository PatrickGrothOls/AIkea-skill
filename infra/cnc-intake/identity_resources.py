"""Scope: Provision an invitation-only Cognito identity boundary for native clients."""


class IdentityResources:
    CALLBACK = "http://localhost:8766/callback"

    def resources(self):
        return {
            "UserPool": {"Type": "AWS::Cognito::UserPool", "Properties": {
                "UserPoolName": "aikea-cnc-intake", "UsernameAttributes": ["email"],
                "UserPoolTags": {"Service": "aikea-cnc-intake"},
                "AutoVerifiedAttributes": ["email"], "UsernameConfiguration": {"CaseSensitive": False},
                "AdminCreateUserConfig": {"AllowAdminCreateUserOnly": True},
                "Policies": {"PasswordPolicy": {"MinimumLength": 14, "RequireLowercase": True,
                                                "RequireUppercase": True, "RequireNumbers": True, "RequireSymbols": True}},
                "AccountRecoverySetting": {"RecoveryMechanisms": [{"Name": "verified_email", "Priority": 1}]}}},
            "Scope": {"Type": "AWS::Cognito::UserPoolResourceServer", "Properties": {
                "UserPoolId": {"Ref": "UserPool"}, "Identifier": "aikea", "Name": "CNC quote uploads",
                "Scopes": [{"ScopeName": "submit", "ScopeDescription": "Submit your own CNC quote package"}]}},
            "Client": {"Type": "AWS::Cognito::UserPoolClient", "DependsOn": "Scope", "Properties": {
                "UserPoolId": {"Ref": "UserPool"}, "ClientName": "aikea-native-viewer", "GenerateSecret": False,
                "AllowedOAuthFlowsUserPoolClient": True, "AllowedOAuthFlows": ["code"],
                "AllowedOAuthScopes": ["openid", "email", "aikea/submit"], "SupportedIdentityProviders": ["COGNITO"],
                "CallbackURLs": [self.CALLBACK], "ExplicitAuthFlows": ["ALLOW_REFRESH_TOKEN_AUTH"],
                "EnableTokenRevocation": True, "PreventUserExistenceErrors": "ENABLED",
                "AccessTokenValidity": 5, "IdTokenValidity": 5, "RefreshTokenValidity": 1,
                "TokenValidityUnits": {"AccessToken": "minutes", "IdToken": "minutes", "RefreshToken": "days"}}},
            "Domain": {"Type": "AWS::Cognito::UserPoolDomain", "Properties": {
                "UserPoolId": {"Ref": "UserPool"}, "Domain": {"Fn::Sub": "aikea-cnc-${AWS::AccountId}"}}},
        }
