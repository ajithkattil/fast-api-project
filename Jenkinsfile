@Library('jenkins-ci-library') _
Map config = [
    name     : 'recipes-api-service',
    helm        : [
        environment     : 'staging',
        updateDependency: true,
    ],
    environment     : 'staging',
    namespace   : 'wms',
    maintenance : [:],  
    isReleaseBranch: true,         
    deploy      : [
        'cs-stg' : [
            ask             : false,
            environment     : 'staging',
            kubernetes      : true,
            createVersionTag: false,
            notifyRollbar   : true,
            notifyGithub    : true,
            isReleaseBranch : true, 
            scope           : ['branch'],
            image: '442426862663.dkr.ecr.us-east-1.amazonaws.com/freshrealm/'
        ],
    ],
    docker: [
        skip: true
    ],
]
pipelineLibraries config