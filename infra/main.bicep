targetScope = 'resourceGroup'

@description('Environment name such as dev, qa, or prod')
param environment string

@description('Azure region')
param location string = resourceGroup().location

@description('Project name used for resource naming')
param projectName string = 'sre-platform'

@description('AKS Kubernetes version. Leave empty to use Azure default.')
param kubernetesVersion string = ''

@description('AKS node count')
param nodeCount int = 2

@description('AKS VM size')
param nodeVmSize string = 'Standard_B2s'

@description('Resource tags for cost tracking and governance')
param tags object = {
  project: projectName
  environment: environment
  managedBy: 'bicep'
}

var namePrefix = '${projectName}-${environment}'

module logAnalytics 'loganalytics.bicep' = {
  name: 'deploy-loganalytics'
  params: {
    workspaceName: 'law-${namePrefix}'
    location: location
    tags: tags
  }
}

module acr 'acr.bicep' = {
  name: 'deploy-acr'
  params: {
    acrName: replace('acr${projectName}${environment}', '-', '')
    location: location
    tags: tags
  }
}

module keyVault 'keyvault.bicep' = {
  name: 'deploy-keyvault'
  params: {
    keyVaultName: 'kv-${namePrefix}'
    location: location
    tags: tags
  }
}

module managedIdentity 'managed-identity.bicep' = {
  name: 'deploy-managed-identity'
  params: {
    identityName: 'id-${namePrefix}'
    location: location
    tags: tags
  }
}

module aks 'aks.bicep' = {
  name: 'deploy-aks'
  params: {
    aksName: 'aks-${namePrefix}'
    location: location
    kubernetesVersion: kubernetesVersion
    nodeCount: nodeCount
    nodeVmSize: nodeVmSize
    logAnalyticsWorkspaceResourceId: logAnalytics.outputs.workspaceResourceId
    acrResourceId: acr.outputs.acrResourceId
    tags: tags
  }
}

output aksClusterName string = aks.outputs.aksClusterName
output acrLoginServer string = acr.outputs.acrLoginServer
output keyVaultUri string = keyVault.outputs.keyVaultUri
output managedIdentityClientId string = managedIdentity.outputs.clientId
output logAnalyticsWorkspaceId string = logAnalytics.outputs.workspaceResourceId
