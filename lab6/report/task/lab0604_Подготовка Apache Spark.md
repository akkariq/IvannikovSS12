# Подробная инструкция по установке и запуску Apache Spark на Ubuntu

## Предварительные требования

### 1. Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Установка Java (требуется для Spark)
```bash
# Установка OpenJDK 11 (рекомендуемая версия)
sudo apt install openjdk-11-jdk -y

# Проверка установки
java -version
javac -version
```

### 3. Настройка переменных окружения Java
```bash
# Добавьте в ~/.bashrc или ~/.profile
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

## Установка Apache Spark

### Способ 1: Установка из официального сайта (рекомендуется)

#### 1. Скачивание Spark
```bash
# Установка wget если нет
sudo apt install wget -y

# Скачивание последней версии Spark (проверьте актуальную версию на сайте)
cd /tmp
wget https://downloads.apache.org/spark/spark-3.4.0/spark-3.4.0-bin-hadoop3.tgz

# Или используйте более новую версию, если доступна
# wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
```

#### 2. Распаковка и установка
```bash
# Распаковка
tar -xzf spark-3.4.0-bin-hadoop3.tgz

# Перемещение в системную директорию
sudo mv spark-3.4.0-bin-hadoop3 /opt/spark

# Установка прав
sudo chown -R $USER:$USER /opt/spark
```

#### 3. Настройка переменных окружения Spark
```bash
# Добавьте в ~/.bashrc
echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
echo 'export PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH' >> ~/.bashrc
echo 'export PYSPARK_PYTHON=python3' >> ~/.bashrc
source ~/.bashrc
```

### Способ 2: Установка через sbt (для Scala разработки)

#### 1. Установка sbt
```bash
# Установка sbt
echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | sudo tee /etc/apt/sources.list.d/sbt.list
echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | sudo tee /etc/apt/sources.list.d/sbt_old.list
curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add
sudo apt update
sudo apt install sbt -y
```

#### 2. Создание проекта Scala с Spark
```bash
# Создание структуры проекта
mkdir -p ~/spark-project/src/main/scala
cd ~/spark-project

# Создание build.sbt
cat > build.sbt << 'EOF'
name := "spark-project"
version := "1.0"
scalaVersion := "2.13.10"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "3.4.0",
  "org.apache.spark" %% "spark-sql" % "3.4.0"
)
EOF

# Создание структуры директорий
mkdir -p src/main/scala
```

## Проверка установки

### 1. Проверка Spark Shell (Scala)
```bash
# Запуск Spark Shell
cd /opt/spark
./bin/spark-shell

# Внутри Spark Shell выполните тестовые команды:
val data = Array(1, 2, 3, 4, 5)
val distData = sc.parallelize(data)
distData.reduce(_ + _)

# Выход: :quit
```

### 2. Проверка PySpark (Python)
```bash
# Установка Python3 если нет
sudo apt install python3 python3-pip -y

# Запуск PySpark
./bin/pyspark

# Тестовые команды в PySpark:
data = [1, 2, 3, 4, 5]
distData = sc.parallelize(data)
distData.reduce(lambda a, b: a + b)

# Выход: exit()
```

### 3. Запуск тестового приложения
```bash
# Пример запуска встроенного примера
./bin/run-example SparkPi 10
```

## Настройка для лабораторной работы

### 1. Создание рабочей директории
```bash
mkdir -p ~/scala-lab/src/main/scala
cd ~/scala-lab
```

### 2. Создание файла build.sbt
```bash
cat > build.sbt << 'EOF'
name := "scala-fp-lab"
version := "1.0"
scalaVersion := "2.13.10"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "3.4.0",
  "org.apache.spark" %% "spark-sql" % "3.4.0"
)

// Для лучшей производительности
fork in run := true
outputStrategy := Some(StdoutOutput)
EOF
```

### 3. Создание структуры проекта
```bash
mkdir -p src/main/scala
```

### 4. Копирование файлов лабораторной работы
Создайте все файлы из задания (`BasicScala.scala`, `Collections.scala` и т.д.) в директории `src/main/scala/`

## Запуск лабораторной работы

### 1. Компиляция проекта
```bash
cd ~/scala-lab
sbt compile
```

### 2. Запуск отдельных модулей
```bash
# Запуск базовых примеров
sbt "runMain BasicScala"
sbt "runMain Collections"
sbt "runMain ErrorHandling"
sbt "runMain PatternMatching"
```

### 3. Запуск Spark примеров
```bash
# Запуск Spark примера (требует установленного Spark)
sbt "runMain SparkExample"
```

### 4. Создание JAR файла для запуска на кластере
```bash
sbt package
```

## Устранение常见 проблем

### 1. Проблемы с памятью
```bash
# Если возникают ошибки памяти, настройте параметры JVM
echo 'export SPARK_DRIVER_MEMORY=2g' >> ~/.bashrc
echo 'export SPARK_EXECUTOR_MEMORY=2g' >> ~/.bashrc
source ~/.bashrc
```

### 2. Проблемы с Java версией
```bash
# Проверка альтернатив Java
sudo update-alternatives --config java

# Установка конкретной версии если нужно
sudo apt install openjdk-8-jdk -y
```

### 3. Проблемы с правами доступа
```bash
# Если проблемы с правами на /opt/spark
sudo chmod -R 755 /opt/spark
sudo chown -R $USER:$USER /opt/spark
```

### 4. Проблемы с сетью (если загрузка блокируется)
```bash
# Альтернативные зеркала для загрузки Spark
wget https://archive.apache.org/dist/spark/spark-3.4.0/spark-3.4.0-bin-hadoop3.tgz
```

## Проверка работоспособности полного пайплайна

### 1. Тестовый скрипт
Создайте файл `test_spark.sh`:
```bash
#!/bin/bash
echo "=== Testing Spark Installation ==="

# Test Java
echo "Java version:"
java -version

# Test Spark
echo "Spark version:"
/opt/spark/bin/spark-submit --version

# Test basic functionality
echo "Running basic Spark test..."
/opt/spark/bin/spark-shell --master local[2] << EOF
val data = 1 to 100
val rdd = sc.parallelize(data)
println("Sum: " + rdd.reduce(_ + _))
System.exit(0)
EOF

echo "=== Test completed ==="
```

### 2. Запуск теста
```bash
chmod +x test_spark.sh
./test_spark.sh
```

## Дополнительные настройки (опционально)

### 1. Установка Hadoop (если нужен HDFS)
```bash
# Базовая установка Hadoop
sudo apt install hadoop -y
```

### 2. Настройка исторического сервера Spark
```bash
# Копирование конфигурации
cp /opt/spark/conf/spark-defaults.conf.template /opt/spark/conf/spark-defaults.conf

# Добавление в spark-defaults.conf
echo "spark.eventLog.enabled true" >> /opt/spark/conf/spark-defaults.conf
echo "spark.eventLog.dir file:///tmp/spark-events" >> /opt/spark/conf/spark-defaults.conf
echo "spark.history.fs.logDirectory file:///tmp/spark-events" >> /opt/spark/conf/spark-defaults.conf

# Создание директории для логов
mkdir -p /tmp/spark-events
```

### 3. Запуск исторического сервера
```bash
/opt/spark/sbin/start-history-server.sh
```

Эта инструкция позволит вам установить и настроить полнофункциональное окружение Spark для выполнения лабораторной работы. После установки вы сможете запускать все предоставленные примеры кода.