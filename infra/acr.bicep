@description('Name of the Azure Container Registry')
param acrName string

@description('Azure region for the Container Registry')
param location string

@description('Resource tags')
param tags object = {}

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: toLower(acrName)
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
  }
}

output acrResourceId string = acr.id
output acrLoginServer string = acr.properties.loginServer
