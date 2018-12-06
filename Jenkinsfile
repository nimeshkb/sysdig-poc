node {
    stage('Checkout') {
        def GITID = checkout(scm).GIT_COMMIT
        echo ${GITID}
    }
    stage('Build Image') {
        sh '''
            # find the short git SHA
            echo ${BUILD_NUMBER}
            echo ${GITID}
            #GITID=$(echo ${GIT_COMMIT} | cut -c1-7)
            #echo ${GITID}
            # build the demo using the existing Dockerfile and tag the image with the short git SHA
            docker build -t samgabrail/sysdig-jenkins-dev:${GITID} .            
        '''
    }
    stage('Push Image to Dev') {
        withCredentials([usernamePassword(credentialsId: 'docker-repository-credentials', passwordVariable: 'dockerhubPassword', usernameVariable: 'dockerhubUsername')]) {
            sh '''
                # docker login
                echo "logging in to Dockerhub"
                docker login -u ${dockerhubUsername} -p ${dockerhubPassword}
                docker push samgabrail/sysdig-jenkins-dev:${GITID}
                # add image to sysdig_secure_images file
                echo samgabrail/sysdig-jenkins-dev:${GITID} > sysdig_secure_images
            '''
        }
    }
    stage('Scanning Image') {
        anchore 'sysdig_secure_images'
    }
    stage('Push Successfully Scanned Image to Prod') {
        sh '''
            # docker tag the dev image to prod image
            docker tag samgabrail/sysdig-jenkins-dev:${GITID} samgabrail/sysdig-jenkins:${GITID}
            docker push samgabrail/sysdig-jenkins:${GITID}           
        '''
    }
}

