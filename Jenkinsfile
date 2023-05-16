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
          sh 'npm install'
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
          sh 'python3 app.py &'
          sh 'python3 -m unittest discover tests'
        }
      }
    }
   }
 }
    
