@description('Name of the user-assigned managed identity')
param identityName string

@description('Azure region')
param location string

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}

output identityResourceId string = identity.id
output clientId string = identity.properties.clientId
output principalId string = identity.properties.principalId
