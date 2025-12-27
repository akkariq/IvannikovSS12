### **Лабораторная работа (часть 2): Тестирование асинхронного кода в Go**

**Цель работы:** Освоить методики тестирования конкурентного кода, горутин, каналов и асинхронных операций в Go. Научиться писать надежные тесты для параллельных программ.

**Стек технологий:**
*   **Язык программирования:** Go 1.19+
*   **Операционная система:** Ubuntu 20.04/22.04 LTS
*   **Инструменты:** Go testing framework, `go test`, race detector
*   **Библиотеки:** `testing`, `sync`, `time`, `context`

---

### **Подготовка тестового окружения**

```bash
# Переход в рабочую директорию
cd ~/go/src/lab-async-go

# Создание структуры проекта
mkdir -p internal/worker internal/server internal/utils
mkdir -p tests/integration tests/benchmarks

# Проверка структуры
tree .
```

---

### **Часть 1: Тестирование базовых горутин и каналов**

**1.1. Тестирование простых горутин**

**Файл: `internal/utils/goroutines.go`**
```go
package utils

import (
    "sync"
    "time"
)

type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}

func (c *Counter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.value
}

func ProcessItems(items []int, processor func(int)) {
    var wg sync.WaitGroup
    for _, item := range items {
        wg.Add(1)
        go func(i int) {
            defer wg.Done()
            processor(i)
            time.Sleep(10 * time.Millisecond) // Имитация работы
        }(item)
    }
    wg.Wait()
}
```

**Файл: `internal/utils/goroutines_test.go`**
```go
package utils

import (
    "sync"
    "testing"
    "time"
)

func TestCounter(t *testing.T) {
    counter := &Counter{}
    var wg sync.WaitGroup
    
    // Запускаем 100 горутин для инкремента
    for i := 0; i < 100; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            counter.Increment()
        }()
    }
    
    wg.Wait()
    
    if counter.Value() != 100 {
        t.Errorf("Expected counter value 100, got %d", counter.Value())
    }
}

func TestProcessItems(t *testing.T) {
    items := []int{1, 2, 3, 4, 5}
    processed := make([]int, 0)
    var mu sync.Mutex
    
    processor := func(item int) {
        mu.Lock()
        defer mu.Unlock()
        processed = append(processed, item)
    }
    
    ProcessItems(items, processor)
    
    if len(processed) != len(items) {
        t.Errorf("Expected %d processed items, got %d", len(items), len(processed))
    }
    
    // Проверяем, что все элементы обработаны
    itemMap := make(map[int]bool)
    for _, item := range processed {
        itemMap[item] = true
    }
    
    for _, item := range items {
        if !itemMap[item] {
            t.Errorf("Item %d was not processed", item)
        }
    }
}

func TestProcessItems_RaceCondition(t *testing.T) {
    // Запуск с детектором гонок
    items := make([]int, 100)
    for i := 0; i < 100; i++ {
        items[i] = i
    }
    
    var counter int
    var mu sync.Mutex
    
    processor := func(item int) {
        mu.Lock()
        defer mu.Unlock()
        counter++
    }
    
    ProcessItems(items, processor)
    
    if counter != 100 {
        t.Errorf("Expected 100 processed items, got %d", counter)
    }
}
```

**1.2. Тестирование каналов**

**Файл: `internal/utils/channels.go`**
```go
package utils

import (
    "context"
    "time"
)

func MergeChannels(ctx context.Context, chs ...<-chan int) <-chan int {
    out := make(chan int)
    
    for _, ch := range chs {
        go func(c <-chan int) {
            defer close(out)
            for {
                select {
                case val, ok := <-c:
                    if !ok {
                        return
                    }
                    select {
                    case out <- val:
                    case <-ctx.Done():
                        return
                    }
                case <-ctx.Done():
                    return
                }
            }
        }(ch)
    }
    
    return out
}

func BufferedChannelProcessor(input <-chan int, bufferSize int) <-chan int {
    output := make(chan int, bufferSize)
    
    go func() {
        defer close(output)
        for val := range input {
            output <- val * 2 // Простая обработка
        }
    }()
    
    return output
}
```

**Файл: `internal/utils/channels_test.go`**
```go
package utils

import (
    "context"
    "testing"
    "time"
)

func TestMergeChannels(t *testing.T) {
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()
    
    ch1 := make(chan int)
    ch2 := make(chan int)
    
    go func() {
        defer close(ch1)
        for i := 0; i < 3; i++ {
            ch1 <- i
        }
    }()
    
    go func() {
        defer close(ch2)
        for i := 3; i < 6; i++ {
            ch2 <- i
        }
    }()
    
    merged := MergeChannels(ctx, ch1, ch2)
    
    var results []int
    for val := range merged {
        results = append(results, val)
    }
    
    if len(results) != 6 {
        t.Errorf("Expected 6 values, got %d", len(results))
    }
}

func TestBufferedChannelProcessor(t *testing.T) {
    input := make(chan int, 5)
    
    for i := 1; i <= 5; i++ {
        input <- i
    }
    close(input)
    
    output := BufferedChannelProcessor(input, 3)
    
    expected := []int{2, 4, 6, 8, 10}
    var results []int
    
    for val := range output {
        results = append(results, val)
    }
    
    if len(results) != len(expected) {
        t.Errorf("Expected %d results, got %d", len(expected), len(results))
    }
    
    for i, val := range results {
        if val != expected[i] {
            t.Errorf("Expected %d at position %d, got %d", expected[i], i, val)
        }
    }
}

func TestChannelTimeout(t *testing.T) {
    ch := make(chan int)
    
    select {
    case <-ch:
        t.Error("Should not receive from channel")
    case <-time.After(100 * time.Millisecond):
        // Ожидаемое поведение - таймаут
    }
}
```

---

### **Часть 2: Тестирование Worker Pool**

**Файл: `internal/worker/pool.go`**
```go
package worker

import (
    "context"
    "sync"
    "time"
)

type Task struct {
    ID   int
    Data interface{}
}

type Result struct {
    TaskID int
    Output interface{}
    Error  error
}

type WorkerPool struct {
    workersCount int
    tasks        chan Task
    results      chan Result
    wg           sync.WaitGroup
}

func NewWorkerPool(workers int) *WorkerPool {
    return &WorkerPool{
        workersCount: workers,
        tasks:        make(chan Task, workers*2),
        results:      make(chan Result, workers*2),
    }
}

func (wp *WorkerPool) Start(ctx context.Context, processor func(Task) Result) {
    for i := 0; i < wp.workersCount; i++ {
        wp.wg.Add(1)
        go func(workerID int) {
            defer wp.wg.Done()
            for {
                select {
                case task, ok := <-wp.tasks:
                    if !ok {
                        return
                    }
                    result := processor(task)
                    wp.results <- result
                case <-ctx.Done():
                    return
                }
            }
        }(i)
    }
}

func (wp *WorkerPool) Submit(task Task) {
    wp.tasks <- task
}

func (wp *WorkerPool) GetResults() <-chan Result {
    return wp.results
}

func (wp *WorkerPool) Stop() {
    close(wp.tasks)
    wp.wg.Wait()
    close(wp.results)
}

func (wp *WorkerPool) ProcessTasks(ctx context.Context, tasks []Task, processor func(Task) Result) []Result {
    go wp.Start(ctx, processor)
    
    for _, task := range tasks {
        wp.Submit(task)
    }
    
    var results []Result
    for i := 0; i < len(tasks); i++ {
        select {
        case result := <-wp.results:
            results = append(results, result)
        case <-ctx.Done():
            return results
        }
    }
    
    return results
}
```

**Файл: `internal/worker/pool_test.go`**
```go
package worker

import (
    "context"
    "errors"
    "sync"
    "testing"
    "time"
)

func TestWorkerPool_BasicFunctionality(t *testing.T) {
    pool := NewWorkerPool(3)
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    
    tasks := []Task{
        {ID: 1, Data: "task1"},
        {ID: 2, Data: "task2"},
        {ID: 3, Data: "task3"},
    }
    
    processor := func(task Task) Result {
        time.Sleep(10 * time.Millisecond)
        return Result{
            TaskID: task.ID,
            Output: task.Data.(string) + "_processed",
        }
    }
    
    results := pool.ProcessTasks(ctx, tasks, processor)
    
    if len(results) != len(tasks) {
        t.Errorf("Expected %d results, got %d", len(tasks), len(results))
    }
    
    for _, result := range results {
        if result.Error != nil {
            t.Errorf("Unexpected error: %v", result.Error)
        }
    }
}

func TestWorkerPool_ConcurrentSubmission(t *testing.T) {
    pool := NewWorkerPool(5)
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    
    var wg sync.WaitGroup
    totalTasks := 100
    
    processor := func(task Task) Result {
        time.Sleep(1 * time.Millisecond)
        return Result{
            TaskID: task.ID,
            Output: task.Data.(int) * 2,
        }
    }
    
    go pool.Start(ctx, processor)
    
    // Конкурентная отправка задач
    for i := 0; i < totalTasks; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            pool.Submit(Task{ID: id, Data: id})
        }(i)
    }
    
    wg.Wait()
    
    // Сбор результатов
    results := make(map[int]bool)
    for i := 0; i < totalTasks; i++ {
        select {
        case result := <-pool.GetResults():
            results[result.TaskID] = true
        case <-ctx.Done():
            t.Fatal("Timeout waiting for results")
        }
    }
    
    if len(results) != totalTasks {
        t.Errorf("Expected %d results, got %d", totalTasks, len(results))
    }
}

func TestWorkerPool_ErrorHandling(t *testing.T) {
    pool := NewWorkerPool(2)
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    
    tasks := []Task{
        {ID: 1, Data: "success"},
        {ID: 2, Data: "error"},
    }
    
    processor := func(task Task) Result {
        if task.Data.(string) == "error" {
            return Result{
                TaskID: task.ID,
                Error:  errors.New("processing error"),
            }
        }
        return Result{
            TaskID: task.ID,
            Output: "success_result",
        }
    }
    
    results := pool.ProcessTasks(ctx, tasks, processor)
    
    successCount := 0
    errorCount := 0
    
    for _, result := range results {
        if result.Error != nil {
            errorCount++
        } else {
            successCount++
        }
    }
    
    if successCount != 1 || errorCount != 1 {
        t.Errorf("Expected 1 success and 1 error, got %d success and %d errors", successCount, errorCount)
    }
}

func TestWorkerPool_ContextCancellation(t *testing.T) {
    pool := NewWorkerPool(3)
    ctx, cancel := context.WithCancel(context.Background())
    
    // Отменяем контекст сразу
    cancel()
    
    tasks := []Task{
        {ID: 1, Data: "task1"},
        {ID: 2, Data: "task2"},
    }
    
    processor := func(task Task) Result {
        time.Sleep(100 * time.Millisecond) // Долгая операция
        return Result{TaskID: task.ID}
    }
    
    results := pool.ProcessTasks(ctx, tasks, processor)
    
    // При отмененном контексте должно быть мало или нет результатов
    if len(results) >= len(tasks) {
        t.Error("Expected fewer results due to context cancellation")
    }
}
```

---

### **Часть 3: Тестирование HTTP сервера**

**Файл: `internal/server/http.go`**
```go
package server

import (
    "context"
    "fmt"
    "net/http"
    "sync/atomic"
    "time"
)

type Server struct {
    router      *http.ServeMux
    requestCount int64
    server      *http.Server
}

func NewServer(addr string) *Server {
    s := &Server{
        router: http.NewServeMux(),
    }
    
    s.setupRoutes()
    
    s.server = &http.Server{
        Addr:    addr,
        Handler: s.router,
    }
    
    return s
}

func (s *Server) setupRoutes() {
    s.router.HandleFunc("/", s.handleRoot)
    s.router.HandleFunc("/health", s.handleHealth)
    s.router.HandleFunc("/stats", s.handleStats)
}

func (s *Server) handleRoot(w http.ResponseWriter, r *http.Request) {
    atomic.AddInt64(&s.requestCount, 1)
    time.Sleep(50 * time.Millisecond) // Имитация обработки
    fmt.Fprintf(w, "Hello! Request count: %d\n", atomic.LoadInt64(&s.requestCount))
}

func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    w.Write([]byte("OK"))
}

func (s *Server) handleStats(w http.ResponseWriter, r *http.Request) {
    count := atomic.LoadInt64(&s.requestCount)
    fmt.Fprintf(w, "Total requests: %d", count)
}

func (s *Server) Start() error {
    return s.server.ListenAndServe()
}

func (s *Server) Stop(ctx context.Context) error {
    return s.server.Shutdown(ctx)
}

func (s *Server) GetRequestCount() int64 {
    return atomic.LoadInt64(&s.requestCount)
}
```

**Файл: `internal/server/http_test.go`**
```go
package server

import (
    "context"
    "fmt"
    "io"
    "net/http"
    "net/http/httptest"
    "sync"
    "testing"
    "time"
)

func TestServer_Routes(t *testing.T) {
    server := NewServer(":0")
    
    tests := []struct {
        name       string
        path       string
        wantStatus int
        wantBody   string
    }{
        {
            name:       "root path",
            path:       "/",
            wantStatus: http.StatusOK,
            wantBody:   "Hello! Request count: 1",
        },
        {
            name:       "health check",
            path:       "/health",
            wantStatus: http.StatusOK,
            wantBody:   "OK",
        },
        {
            name:       "stats",
            path:       "/stats",
            wantStatus: http.StatusOK,
            wantBody:   "Total requests: 0",
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest("GET", tt.path, nil)
            w := httptest.NewRecorder()
            
            server.router.ServeHTTP(w, req)
            
            resp := w.Result()
            body, _ := io.ReadAll(resp.Body)
            
            if resp.StatusCode != tt.wantStatus {
                t.Errorf("Expected status %d, got %d", tt.wantStatus, resp.StatusCode)
            }
            
            if string(body) != tt.wantBody && tt.path != "/" {
                // Для корневого пути тело динамическое, пропускаем точную проверку
                t.Errorf("Expected body %q, got %q", tt.wantBody, string(body))
            }
        })
    }
}

func TestServer_ConcurrentRequests(t *testing.T) {
    server := NewServer(":0")
    ts := httptest.NewServer(server.router)
    defer ts.Close()
    
    var wg sync.WaitGroup
    requests := 100
    
    for i := 0; i < requests; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            resp, err := http.Get(ts.URL + "/")
            if err != nil {
                t.Errorf("Request failed: %v", err)
                return
            }
            defer resp.Body.Close()
            
            if resp.StatusCode != http.StatusOK {
                t.Errorf("Expected status 200, got %d", resp.StatusCode)
            }
        }(i)
    }
    
    wg.Wait()
    
    // Проверяем счетчик запросов
    if server.GetRequestCount() != int64(requests) {
        t.Errorf("Expected %d requests, got %d", requests, server.GetRequestCount())
    }
}

func TestServer_GracefulShutdown(t *testing.T) {
    server := NewServer(":0")
    ts := httptest.NewServer(server.router)
    
    ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
    defer cancel()
    
    // Запускаем остановку сервера
    go func() {
        time.Sleep(50 * time.Millisecond)
        if err := server.Stop(ctx); err != nil {
            t.Logf("Shutdown error: %v", err)
        }
    }()
    
    // Пытаемся сделать запрос после shutdown
    time.Sleep(60 * time.Millisecond)
    _, err := http.Get(ts.URL + "/")
    if err == nil {
        t.Error("Expected error after shutdown, but request succeeded")
    }
}
```

---

### **Часть 4: Интеграционные тесты и бенчмарки**

**Файл: `tests/integration/integration_test.go`**
```go
package integration

import (
    "context"
    "net/http"
    "sync"
    "testing"
    "time"
    
    "lab-async-go/internal/server"
    "lab-async-go/internal/worker"
)

func TestIntegration_WorkerPoolWithHTTPServer(t *testing.T) {
    // Запускаем сервер
    srv := server.NewServer(":8081")
    go srv.Start()
    defer srv.Stop(context.Background())
    
    time.Sleep(100 * time.Millisecond) // Даем время серверу запуститься
    
    // Создаем worker pool
    pool := worker.NewWorkerPool(5)
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()
    
    tasks := []worker.Task{
        {ID: 1, Data: "http://localhost:8081/health"},
        {ID: 2, Data: "http://localhost:8081/stats"},
    }
    
    processor := func(task worker.Task) worker.Result {
        resp, err := http.Get(task.Data.(string))
        if err != nil {
            return worker.Result{TaskID: task.ID, Error: err}
        }
        defer resp.Body.Close()
        
        return worker.Result{
            TaskID: task.ID,
            Output: resp.StatusCode,
        }
    }
    
    results := pool.ProcessTasks(ctx, tasks, processor)
    
    for _, result := range results {
        if result.Error != nil {
            t.Errorf("Task %d failed: %v", result.TaskID, result.Error)
        }
        if result.Output != http.StatusOK {
            t.Errorf("Task %d expected status 200, got %v", result.TaskID, result.Output)
        }
    }
}

func TestIntegration_LoadTest(t *testing.T) {
    if testing.Short() {
        t.Skip("Skipping load test in short mode")
    }
    
    srv := server.NewServer(":8082")
    go srv.Start()
    defer srv.Stop(context.Background())
    
    time.Sleep(200 * time.Millisecond)
    
    clients := 50
    requestsPerClient := 20
    var wg sync.WaitGroup
    
    for i := 0; i < clients; i++ {
        wg.Add(1)
        go func(clientID int) {
            defer wg.Done()
            for j := 0; j < requestsPerClient; j++ {
                resp, err := http.Get("http://localhost:8082/")
                if err != nil {
                    t.Logf("Client %d request failed: %v", clientID, err)
                    continue
                }
                resp.Body.Close()
                time.Sleep(10 * time.Millisecond)
            }
        }(i)
    }
    
    wg.Wait()
    
    totalRequests := clients * requestsPerClient
    if srv.GetRequestCount() != int64(totalRequests) {
        t.Errorf("Expected %d requests, got %d", totalRequests, srv.GetRequestCount())
    }
}
```

**Файл: `tests/benchmarks/benchmark_test.go`**
```go
package benchmarks

import (
    "context"
    "sync"
    "testing"
    "time"
    
    "lab-async-go/internal/utils"
    "lab-async-go/internal/worker"
)

func BenchmarkCounter_Increment(b *testing.B) {
    counter := &utils.Counter{}
    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            counter.Increment()
        }
    })
}

func BenchmarkWorkerPool_ProcessTasks(b *testing.B) {
    pool := worker.NewWorkerPool(10)
    ctx := context.Background()
    
    processor := func(task worker.Task) worker.Result {
        time.Sleep(1 * time.Millisecond)
        return worker.Result{
            TaskID: task.ID,
            Output: task.Data.(int) * 2,
        }
    }
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        tasks := make([]worker.Task, 100)
        for j := 0; j < 100; j++ {
            tasks[j] = worker.Task{ID: j, Data: j}
        }
        pool.ProcessTasks(ctx, tasks, processor)
    }
}

func BenchmarkGoroutineCreation(b *testing.B) {
    var wg sync.WaitGroup
    worker := func() {
        defer wg.Done()
        // Легкая работа
        time.Sleep(1 * time.Microsecond)
    }
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        wg.Add(1)
        go worker()
    }
    wg.Wait()
}

func BenchmarkChannelCommunication(b *testing.B) {
    ch := make(chan int, b.N)
    
    // Горутина для чтения
    go func() {
        for range ch {
        }
    }()
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        ch <- i
    }
    close(ch)
}
```

---

### **Часть 5: Запуск тестов и анализ**

**Основные команды для тестирования:**

```bash
# Переход в директорию проекта
cd ~/go/src/lab-async-go

# Запуск unit-тестов
go test ./internal/... -v

# Запуск интеграционных тестов
go test ./tests/integration/... -v

# Запуск бенчмарков
go test ./tests/benchmarks/... -bench=. -benchmem

# Запуск всех тестов с детектором гонок
go test ./... -race

# Запуск тестов с покрытием
go test ./internal/... -coverprofile=coverage.out
go tool cover -html=coverage.out -o coverage.html

# Запуск нагрузочного тестирования
go test -bench=BenchmarkWorkerPool_ProcessTasks -benchtime=10s

# Тестирование в режиме CI (без кэширования)
go test ./... -count=1
```

**Создание Makefile для автоматизации:**

**Файл: `Makefile`**
```makefile
.PHONY: test test-race bench cover clean

test:
    go test ./internal/... -v

test-integration:
    go test ./tests/integration/... -v

test-race:
    go test ./... -race

bench:
    go test ./tests/benchmarks/... -bench=. -benchmem

cover:
    go test ./internal/... -coverprofile=coverage.out
    go tool cover -html=coverage.out -o coverage.html

clean:
    rm -f coverage.out coverage.html
    go clean -testcache

ci: test-race bench
```

---

### **Требования к отчету по тестированию:**

1.  **Код тестов:** Полные исходные тексты всех тестов
2.  **Результаты выполнения:** Скриншоты выполнения `go test -v`
3.  **Покрытие кода:** Отчет `coverage.html`
4.  **Бенчмарки:** Результаты нагрузочного тестирования
5.  **Анализ:** Обнаруженные проблемы и пути их решения
6.  **Рекомендации:** Best practices для тестирования асинхронного кода

### **Критерии оценки:**

*   **Удовлетворительно:** Реализованы базовые unit-тесты (части 1-2)
*   **Хорошо:** Реализованы комплексные тесты с интеграционными тестами (части 1-4)
*   **Отлично:** Полное покрытие тестами + бенчмарки + детектор гонок + CI-конфигурация

**Примечание:** Все тесты должны проходить стабильно, детектор гонок не должен выявлять проблем, покрытие кода должно быть не менее 70%.