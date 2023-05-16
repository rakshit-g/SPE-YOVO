pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build and Test Frontend') {
      steps {
        dir(path: 'client') {
          sh 'npm install --legacy-peer-deps'
          // sh 'npm run test'
          sh 'npm run build'
        }
      }
    }

    stage('Build and Test Backend') {
      steps {
        dir(path: 'backend') {
          sh 'pwd' 
          sh 'pip3 install -r requirements.txt'
          sh 'python3 server.py &'
        }
      }
    }
    stage('Containerize Frontend') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'a1e5a121-5455-410f-9e53-c0af6a006fde', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
          dir(path: 'client') {
            sh 'docker build -t $USERNAME/yovo-frontend-image .'
            sh 'docker login -u $USERNAME -p $PASSWORD'
            sh 'docker push $USERNAME/yovo-frontend-image'
          }
        }
      }
    }

    stage('Containerize Backend') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'a1e5a121-5455-410f-9e53-c0af6a006fde', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
          dir(path: 'backend') {
            sh 'docker build -t $USERNAME/yovo-backend-image .'
            sh 'docker login -u $USERNAME -p $PASSWORD'
            sh 'docker push $USERNAME/yovo-backend-image'
          }
        }
      }
    }
   }
 }
    
