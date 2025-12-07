pipeline {
    agent any

    stages {
        stage('Cleanup & Setup') {
            steps {
                // Чистим старые контейнеры, если они есть
                sh 'docker stop project-frontend project-backend test-runner || true'
                sh 'docker rm project-frontend project-backend test-runner || true'
                // Пересоздаем сеть
                sh 'docker network create app-network || true'
            }
        }

        stage('Build & Run App') {
            steps {
                // 1. Бэкенд (Собираем и запускаем)
                sh 'docker build -t my-ds-backend ./backend'
                sh 'docker run -d --name project-backend --network app-network -p 5000:5000 my-ds-backend'
                
                // 2. Фронтенд (Собираем и запускаем)
                sh 'docker build -t my-ds-frontend ./frontend'
                sh 'docker run -d --name project-frontend --network app-network -p 80:80 my-ds-frontend'
                
                // Ждем 15 секунд, пока модель обучится
                sh 'sleep 15'
            }
        }

        stage('Run Playwright Tests') {
            steps {
                // Собираем образ для тестов
                sh 'docker build -f Dockerfile.test -t my-test-runner .'
                
                // Запускаем тесты
                sh 'docker run --rm --network app-network --name test-runner my-test-runner pytest e2e_tests/test_frontend.py'
            }
        }
    }
}
