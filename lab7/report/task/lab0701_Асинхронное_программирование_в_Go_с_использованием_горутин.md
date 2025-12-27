### **Лабораторная работа (часть 1): Асинхронное программирование в Go с использованием горутин и каналов**

**Цель работы:** Освоить практическое применение горутин, каналов и паттернов параллельного программирования в Go для создания высокопроизводительных асинхронных приложений.

**Стек технологий:**
*   **Язык программирования:** Go 1.19+
*   **Операционная система:** Ubuntu 20.04/22.04 LTS
*   **Инструменты:** Go compiler, Git, терминал Ubuntu
* **Дополнительные пакеты:** Стандартная библиотека Go (`net/http`, `sync`, `context`)

**Теоретическая часть:**
Горутины и каналы — это основные механизмы параллелизма в Go, позволяющие создавать эффективные асинхронные приложения:
1.  **Горутины:** Легковесные потоки, управляемые runtime Go
2.  **Каналы:** Типизированные конвейеры для связи между горутинами
3.  **Паттерны:** Worker Pool, Producer-Consumer, Fan-out/Fan-in

---

### **Подготовка окружения в Ubuntu**

**1. Установка Go:**
```bash
# Обновление пакетов
sudo apt update && sudo apt upgrade -y

# Установка Go
wget https://golang.org/dl/go1.19.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.19.linux-amd64.tar.gz

# Добавление в PATH
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
echo 'export GOPATH=$HOME/go' >> ~/.bashrc
source ~/.bashrc

# Проверка установки
go version
```

**2. Создание рабочей директории:**
```bash
mkdir -p ~/go/src/lab-async-go
cd ~/go/src/lab-async-go
go mod init lab-async-go
```

---

### **Задание на практическую реализацию:**

#### **Часть 1: Базовые горутины и каналы**

**1.1. Простые горутины**
*   **Задача:** Создать программу, запускающую 5 горутин с передачей параметров.
*   **Требования:** Использовать `WaitGroup` для ожидания завершения.
*   **Демонстрация:** Параллельное выполнение задач.

**1.2. Небуферизованные каналы**
*   **Задача:** Реализовать обмен данными между горутинами через каналы.
*   **Требования:** Синхронная коммуникация, блокирующие операции.
*   **Демонстрация:** Синхронизация горутин.

**Код для части 1:**
```go
// basic_goroutines.go
package main

import (
    "fmt"
    "sync"
    "time"
)

func worker(id int, wg *sync.WaitGroup) {
    defer wg.Done()
    fmt.Printf("Worker %d started\n", id)
    time.Sleep(time.Second)
    fmt.Printf("Worker %d completed\n", id)
}

func main() {
    var wg sync.WaitGroup
    
    for i := 1; i <= 5; i++ {
        wg.Add(1)
        go worker(i, &wg)
    }
    
    wg.Wait()
    fmt.Println("All workers completed")
}
```

**Запуск:**
```bash
go run basic_goroutines.go
```

#### **Часть 2: Буферизованные каналы и select**

**2.1. Буферизованные каналы**
*   **Задача:** Реализовать асинхронную очередь задач с буферизованным каналом.
*   **Требования:** Канал с буфером на 10 элементов, неблокирующая отправка.
*   **Демонстрация:** Асинхронная обработка задач.

**2.2. Конструкция select**
*   **Задача:** Обрабатывать сообщения из нескольких каналов с таймаутом.
*   **Требования:** Использовать `select` с `time.After`.
*   **Демонстрация:** Мультиплексирование каналов.

**Код для части 2:**
```go
// channels_select.go
package main

import (
    "fmt"
    "time"
)

func producer(ch chan<- int) {
    for i := 0; i < 10; i++ {
        ch <- i
        fmt.Printf("Produced: %d\n", i)
    }
    close(ch)
}

func consumer(ch <-chan int) {
    for {
        select {
        case val, ok := <-ch:
            if !ok {
                fmt.Println("Channel closed")
                return
            }
            fmt.Printf("Consumed: %d\n", val)
            time.Sleep(500 * time.Millisecond)
        case <-time.After(2 * time.Second):
            fmt.Println("Timeout occurred")
            return
        }
    }
}

func main() {
    ch := make(chan int, 3)
    go producer(ch)
    consumer(ch)
}
```

#### **Часть 3: Паттерн Worker Pool**

**3.1. Пул воркеров**
*   **Задача:** Реализовать пул из 3 воркеров для обработки задач.
*   **Требования:** Канал для задач, канал для результатов, закрытие воркеров.
*   **Демонстрация:** Распределение нагрузки.

**3.2. Обработка результатов**
*   **Задача:** Собрать и обработать результаты от всех воркеров.
*   **Требования:** Использовать отдельный канал для результатов.

**Код для части 3:**
```go
// worker_pool.go
package main

import (
    "fmt"
    "math/rand"
    "sync"
    "time"
)

type Task struct {
    ID int
}

type Result struct {
    TaskID int
    Output string
}

func worker(id int, tasks <-chan Task, results chan<- Result, wg *sync.WaitGroup) {
    defer wg.Done()
    for task := range tasks {
        fmt.Printf("Worker %d processing task %d\n", id, task.ID)
        time.Sleep(time.Duration(rand.Intn(1000)) * time.Millisecond)
        results <- Result{
            TaskID: task.ID,
            Output: fmt.Sprintf("Task %d completed by worker %d", task.ID, id),
        }
    }
}

func main() {
    rand.Seed(time.Now().UnixNano())
    
    numWorkers := 3
    numTasks := 10
    
    tasks := make(chan Task, numTasks)
    results := make(chan Result, numTasks)
    
    var wg sync.WaitGroup
    
    // Запуск воркеров
    for i := 1; i <= numWorkers; i++ {
        wg.Add(1)
        go worker(i, tasks, results, &wg)
    }
    
    // Отправка задач
    for i := 1; i <= numTasks; i++ {
        tasks <- Task{ID: i}
    }
    close(tasks)
    
    // Закрытие results после завершения всех воркеров
    go func() {
        wg.Wait()
        close(results)
    }()
    
    // Обработка результатов
    for result := range results {
        fmt.Printf("Result: %s\n", result.Output)
    }
    
    fmt.Println("All tasks completed")
}
```

#### **Часть 4: Многопоточный веб-сервер**

**4.1. HTTP сервер с горутинами**
*   **Задача:** Создать веб-сервер, обрабатывающий запросы в отдельных горутинах.
*   **Требования:** Обработка 1000+ одновременных подключений.
*   **Демонстрация:** Высокая производительность под нагрузкой.

**4.2. Graceful shutdown**
*   **Задача:** Реализовать корректное завершение работы сервера.
*   **Требования:** Использование `context` для управления жизненным циклом.

**Код для части 4:**
```go
// http_server.go
package main

import (
    "context"
    "fmt"
    "log"
    "net/http"
    "os"
    "os/signal"
    "sync/atomic"
    "time"
)

var requestCount int64

func handler(w http.ResponseWriter, r *http.Request) {
    count := atomic.AddInt64(&requestCount, 1)
    time.Sleep(100 * time.Millisecond) // Имитация обработки
    fmt.Fprintf(w, "Hello! Request #%d\n", count)
    log.Printf("Handled request #%d", count)
}

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/", handler)
    
    server := &http.Server{
        Addr:    ":8080",
        Handler: mux,
    }
    
    // Канал для graceful shutdown
    stop := make(chan os.Signal, 1)
    signal.Notify(stop, os.Interrupt)
    
    go func() {
        log.Println("Server starting on :8080")
        if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("Server error: %v", err)
        }
    }()
    
    <-stop
    log.Println("Shutting down server...")
    
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    
    if err := server.Shutdown(ctx); err != nil {
        log.Printf("Server shutdown error: %v", err)
    }
    
    log.Println("Server stopped")
}
```

**Тестирование сервера:**
```bash
# Запуск сервера
go run http_server.go

# В другом терминале - нагрузочное тестирование
sudo apt install apache2-utils
ab -n 1000 -c 100 http://localhost:8080/
```

#### **Часть 5: Продвинутые паттерны**

**5.1. Fan-out/Fan-in**
*   **Задача:** Реализовать распределение задач между несколькими воркерами и сбор результатов.
*   **Требования:** Множество продюсеров → множество воркеров → один коллектор.

**5.2. Context для отмены операций**
*   **Задача:** Использование context для управления временем жизни горутин.
*   **Требования:** Таймауты, отмена операций.

**Код для части 5:**
```go
// fanout_fanin.go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

func producer(ctx context.Context, id int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for i := 0; i < 5; i++ {
            select {
            case out <- i:
                fmt.Printf("Producer %d: %d\n", id, i)
            case <-ctx.Done():
                fmt.Printf("Producer %d cancelled\n", id)
                return
            }
            time.Sleep(200 * time.Millisecond)
        }
    }()
    return out
}

func worker(ctx context.Context, in <-chan int, id int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case out <- n * n:
                fmt.Printf("Worker %d processed %d\n", id, n)
            case <-ctx.Done():
                fmt.Printf("Worker %d cancelled\n", id)
                return
            }
        }
    }()
    return out
}

func merge(ctx context.Context, inputs ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)
    
    output := func(c <-chan int) {
        defer wg.Done()
        for n := range c {
            select {
            case out <- n:
            case <-ctx.Done():
                return
            }
        }
    }
    
    wg.Add(len(inputs))
    for _, input := range inputs {
        go output(input)
    }
    
    go func() {
        wg.Wait()
        close(out)
    }()
    
    return out
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
    defer cancel()
    
    // Fan-out: несколько продюсеров
    p1 := producer(ctx, 1)
    p2 := producer(ctx, 2)
    
    // Worker pool
    w1 := worker(ctx, p1, 1)
    w2 := worker(ctx, p2, 2)
    
    // Fan-in: объединение результатов
    results := merge(ctx, w1, w2)
    
    for result := range results {
        fmt.Printf("Result: %d\n", result)
    }
    
    fmt.Println("Processing completed")
}
```

---

### **Комплексный пример**

**Файл: `main.go`**
```go
package main

import (
    "fmt"
    "log"
    "net/http"
    "sync"
    "time"
)

func main() {
    fmt.Println("=== Лабораторная работа: Асинхронное программирование в Go ===")
    
    // Демонстрация всех паттернов
    var wg sync.WaitGroup
    
    // 1. Базовые горутины
    wg.Add(1)
    go func() {
        defer wg.Done()
        fmt.Println("\n1. Базовые горутины:")
        demoBasicGoroutines()
    }()
    
    // 2. Worker Pool
    wg.Add(1)
    go func() {
        defer wg.Done()
        fmt.Println("\n2. Worker Pool:")
        demoWorkerPool()
    }()
    
    wg.Wait()
    
    // 3. HTTP сервер
    fmt.Println("\n3. HTTP Сервер:")
    fmt.Println("Запуск сервера на http://localhost:8080")
    fmt.Println("Для тестирования выполните: ab -n 1000 -c 100 http://localhost:8080/")
    
    go startHTTPServer()
    
    // Ожидание завершения
    select {
    case <-time.After(30 * time.Second):
        fmt.Println("Демонстрация завершена")
    }
}

func demoBasicGoroutines() {
    var wg sync.WaitGroup
    for i := 0; i < 3; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            fmt.Printf("Горутина %d работает\n", id)
            time.Sleep(time.Second)
        }(i)
    }
    wg.Wait()
}

func demoWorkerPool() {
    tasks := make(chan int, 5)
    var wg sync.WaitGroup
    
    // Воркеры
    for i := 0; i < 2; i++ {
        wg.Add(1)
        go func(workerID int) {
            defer wg.Done()
            for task := range tasks {
                fmt.Printf("Воркер %d обработал задачу %d\n", workerID, task)
                time.Sleep(500 * time.Millisecond)
            }
        }(i)
    }
    
    // Задачи
    for i := 0; i < 5; i++ {
        tasks <- i
    }
    close(tasks)
    
    wg.Wait()
}

func startHTTPServer() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Время: %s", time.Now().Format("15:04:05"))
    })
    
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

**Запуск:**
```bash
# Сборка и запуск
go build -o async_app main.go
./async_app

# Или напрямую
go run main.go
```

---

### **Требования к отчету:**

1.  **Код:** Полные исходные тексты всех программ
2.  **Скриншоты:** Результаты выполнения в терминале Ubuntu
3.  **Графики:** Производительность сервера под нагрузкой (если возможно)
4.  **Анализ:** Сравнение производительности синхронного и асинхронного подходов
5.  **Объяснение:** Принципы работы каждого паттерна

### **Критерии оценки:**

*   **Удовлетворительно:** Реализованы части 1 и 2
*   **Хорошо:** Реализованы части 1-3 с рабочим HTTP-сервером
*   **Отлично:** Реализованы все части с graceful shutdown и продвинутыми паттернами

**Примечание:** Все программы должны быть протестированы в среде Ubuntu, демонстрировать устойчивость к нагрузке и корректную обработку ошибок.

### **Рекомендуемая литература**

#### **1. Официальная документация и руководства**
- **The Go Programming Language Specification**  
  *Official Specification*  
  https://golang.org/ref/spec  
  *Полное техническое описание языка Go, включая спецификации горутин и каналов.*

- **Effective Go**  
  *Go Documentation Team*  
  https://golang.org/doc/effective_go  
  *Практическое руководство по написанию идиоматичного кода на Go с лучшими практиками работы с горутинами и каналами.*

#### **2. Книги**
- **"The Go Programming Language"**  
  *Alan A. A. Donovan, Brian W. Kernighan*  
  *Addison-Wesley Professional, 2015*  
  *ISBN: 978-0134190440*  
  *Классическое руководство по Go, включающее глубокое рассмотрение конкурентности в главах 8-9.*

- **"Concurrency in Go: Tools and Techniques for Developers"**  
  *Katherine Cox-Buday*  
  *O'Reilly Media, 2017*  
  *ISBN: 978-1491941195*  
  *Специализированная книга по конкурентности в Go, охватывающая горутины, каналы и паттерны параллельного программирования.*

#### **3. Онлайн-ресурсы и статьи**
- **"Go Concurrency Patterns"**  
  *Rob Pike*  
  https://go.dev/talks/2012/concurrency.slide  
  *Презентация одного из создателей Go о паттернах конкурентности с примерами и лучшими практиками.*

- **"Advanced Go Concurrency Patterns"**  
  *Sameer Ajmani*  
  https://go.dev/blog/io2013-adv-concurrency  
  *Статья о продвинутых паттернах конкурентности, включая context, select и управление жизненным циклом горутин.*

- **Go by Example: Goroutines, Channels**  
  *Mark McGranaghan*  
  https://gobyexample.com/goroutines  
  *Практические примеры использования горутин и каналов с пояснениями.*

#### **4. Дополнительные ресурсы**
- **Go Blog: Concurrency**  
  *The Go Authors*  
  https://go.dev/blog/concurrency  
  *Подборка статей о конкурентности от разработчиков языка Go.*

- **"Learning Go Concurrency"**  
  *GitHub Resources*  
  https://github.com/golang/go/wiki/LearningConcurrency  
  *Коллекция материалов, упражнений и примеров для изучения конкурентности в Go.*

**Рекомендуемый порядок изучения:**
1. Начните с "Effective Go" для понимания базовых принципов
2. Изучите главы 8-9 из "The Go Programming Language" 
3. Практикуйтесь с примерами из "Go by Example"
4. Для углубленного изучения используйте "Concurrency in Go"
5. Изучите презентации Роба Пайка для понимания философии конкурентности в Go