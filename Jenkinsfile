pipeline {
    agent any

    environment {
        // Указываем путь к docker-compose, если нужно, или просто используем shell
        COMPOSE_PROJECT_NAME = "my-vkr-project"
    }

    stages {
        stage('Checkout') {
            steps {
                // Jenkins сам заберет код из Git, если настроен через SCM
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Run Tests') {
            steps {
                // Запуск тестов внутри контейнера (требование на 5)
                // Сначала поднимаем бэкенд в фоновом режиме для теста или запускаем отдельный раннер
                sh 'docker build -t test-backend ./backend'
                sh 'docker run --rm test-backend pytest test_app.py'
            }
        }

        stage('Deploy') {
            steps {
                // Останавливаем старые контейнеры (если были)
                sh 'docker stop project-frontend || true'
                sh 'docker stop project-backend || true'
                sh 'docker rm project-frontend || true'
                sh 'docker rm project-backend || true'
                sh 'docker network create app-network || true'

                // Запускаем бэкенд
                sh 'docker run -d --name project-backend --network app-network -p 5000:5000 -e ENV_TYPE=prod my-vkr-project_backend' // Тут имя образа должно совпадать с тем, как ты его назвал при билде

                // Запускаем фронтенд
                sh 'docker run -d --name project-frontend --network app-network -p 80:80 my-vkr-project_frontend'
            }
        }
    }

}
