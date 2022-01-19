node {
    stage('Checkout') {
        def GITHASH = checkout(scm).GIT_COMMIT
        env.GITID = GITHASH.take(7)
        sh "echo ${GITID}"
    }
    stage('Build Image') {
        sh '''
            # find the short git SHA
            echo ${BUILD_NUMBER}
            echo ${GITID}
            #GITID=$(echo ${GIT_COMMIT} | cut -c1-7)
            #echo ${GITID}
            # build the demo using the existing Dockerfile and tag the image with the short git SHA
            docker build -t nimeshkb/sysdig-dev:${GITID} .            
        '''
    }
    stage('Push Image to Dev') {
        withCredentials([usernamePassword(credentialsId: 'docker-repository-credentials', passwordVariable: 'dockerhubPassword', usernameVariable: 'dockerhubUsername')]) {
            sh '''
                # docker login
                echo "logging in to Dockerhub"
                docker login -u ${dockerhubUsername} -p ${dockerhubPassword}
                docker push nimeshkb/sysdig-dev:${GITID}
                # add image to sysdig_secure_images file
                echo nimeshkb/sysdig-dev:${GITID} > sysdig_secure_images
            '''
        }
    }
    stage('Scanning Image') {
        sh '''
            sysdig engineCredentialsId: 'sysdig-secure-api-credentials', name: 'sysdig_secure_images', inlineScanning: true           
        '''
            
        }
    }
    stage('Push Successfully Scanned Image to Prod') {
        sh '''
            # docker tag the dev image to prod image
            docker tag nimeshkb/sysdig-jenkins-dev:${GITID} nimeshkb/sysdig:${GITID}
            docker push nimeshkb/sysdig:${GITID}           
        '''
    }
    stage('Deploy App') {
        sh '''
            # deploy the app
            gcloud container clusters get-credentials sysdig-cicd-cluster --zone us-east1-c --project vibrant-tree-219615
            kubectl set image deployment/sysdig-jenkins sysdig-jenkins=samgabrail/sysdig-jenkins:${GITID}          
        '''
    }
}


