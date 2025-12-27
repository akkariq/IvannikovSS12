// main.go
package main

import (
	"context"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"os"
	"os/signal"
	"sync"
	"sync/atomic"
	"syscall"
	"time"
)

func main() {
	fmt.Println("=== Лабораторная работа: Асинхронное программирование в Go ===")
	fmt.Println("=== Все реализации объединены в одной программе ===")
        fmt.Println()
	
	var wg sync.WaitGroup
	
	// 1. Демонстрация небуферизованных каналов
	wg.Add(1)
	go func() {
		defer wg.Done()
		fmt.Println("1. Демонстрация небуферизованных каналов:")
		demoUnbufferedChannels()
	}()
	
	// 2. Асинхронная очередь задач (буферизованный канал)
	wg.Add(1)
	go func() {
		defer wg.Done()
		fmt.Println("\n2. Асинхронная очередь задач (буферизованный канал):")
		demoBufferedChannels()
	}()
	
	// 3. Select с таймаутом
	wg.Add(1)
	go func() {
		defer wg.Done()
		fmt.Println("\n3. Select с таймаутом:")
		demoSelectTimeout()
	}()
	
	// 4. Worker Pool (базовый)
	wg.Add(1)
	go func() {
		defer wg.Done()
		fmt.Println("\n4. Worker Pool (базовый):")
		demoWorkerPoolBasic()
	}()
	
	// 5. Worker Pool с обработкой результатов
	wg.Add(1)
	go func() {
		defer wg.Done()
		fmt.Println("\n5. Worker Pool с параллельной обработкой результатов:")
		demoWorkerPoolWithResults()
	}()
	
	// 6. Fan-out/Fan-in паттерн
	wg.Add(1)
	go func() {
		defer wg.Done()
		fmt.Println("\n6. Fan-out/Fan-in паттерн:")
		demoFanOutFanIn()
	}()
	
	wg.Wait()
	
	// 7. HTTP сервер
	fmt.Println("\n7. HTTP сервер с graceful shutdown:")
	fmt.Println("   Сервер запускается на порту :8080")
	fmt.Println("   Доступные эндпоинты:")
	fmt.Println("   - /          - основная страница")
	fmt.Println("   - /slow      - медленный запрос")
	fmt.Println("   - /health    - проверка здоровья")
	fmt.Println("\n   Для остановки сервера нажмите Ctrl+C")
	
	// Запускаем HTTP сервер в отдельной горутине
	serverWg := sync.WaitGroup{}
	serverWg.Add(1)
	go func() {
		defer serverWg.Done()
		startHTTPServer()
	}()
	
	// Ожидаем сигнала завершения
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt, syscall.SIGTERM)
	
	// Таймер для демонстрации
	timer := time.NewTimer(120 * time.Second)
	
	select {
	case <-stop:
		fmt.Println("\nПолучен сигнал завершения")
	case <-timer.C:
		fmt.Println("\nДемонстрация завершена по таймауту")
	}
	
	fmt.Println("Программа завершена!")
}

// === 1. Демонстрация небуферизованных каналов ===
func demoUnbufferedChannels() {
	ch := make(chan string)
	var wg sync.WaitGroup
	
	// Запускаем 2 производителя
	for i := 1; i <= 2; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for j := 1; j <= 3; j++ {
				message := fmt.Sprintf("Сообщение %d от производителя %d", j, id)
				ch <- message
				time.Sleep(time.Duration(id) * 200 * time.Millisecond)
			}
		}(i)
	}
	
	// Запускаем 2 потребителя
	for i := 1; i <= 2; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for j := 1; j <= 3; j++ {
				message := <-ch
				fmt.Printf("  Потребитель %d получил: %s\n", id, message)
				time.Sleep(150 * time.Millisecond)
			}
		}(i)
	}
	
	wg.Wait()
	close(ch)
	fmt.Println("  Все сообщения обработаны!")
}

// === 2. Асинхронная очередь задач ===
type Task struct {
	ID   int
	Name string
}

func demoBufferedChannels() {
	taskQueue := make(chan Task, 10)
	rand.Seed(time.Now().UnixNano())
	
	var producerWg sync.WaitGroup
	var workersWg sync.WaitGroup
	
	// Воркеры
	for i := 1; i <= 3; i++ {
		workersWg.Add(1)
		go func(id int) {
			defer workersWg.Done()
			for task := range taskQueue {
				processingTime := time.Duration(rand.Intn(300)+100) * time.Millisecond
				time.Sleep(processingTime)
				fmt.Printf("  Воркер %d: %s за %v\n", id, task.Name, processingTime)
			}
		}(i)
	}
	
	// Производитель
	producerWg.Add(1)
	go func() {
		defer producerWg.Done()
		for i := 1; i <= 10; i++ {
			task := Task{
				ID:   i,
				Name: fmt.Sprintf("Задача-%d", i),
			}
			taskQueue <- task
			time.Sleep(time.Duration(rand.Intn(150)) * time.Millisecond)
		}
	}()
	
	producerWg.Wait()
	close(taskQueue)
	workersWg.Wait()
}

// === 3. Select с таймаутом ===
func demoSelectTimeout() {
	ch1 := make(chan string)
	ch2 := make(chan string)
	
	go func() {
		for i := 1; i <= 3; i++ {
			time.Sleep(1 * time.Second)
			ch1 <- fmt.Sprintf("Сообщение %d из ch1", i)
		}
	}()
	
	go func() {
		for i := 1; i <= 2; i++ {
			time.Sleep(2 * time.Second)
			ch2 <- fmt.Sprintf("Сообщение %d из ch2", i)
		}
	}()
	
	for i := 1; i <= 5; i++ {
		select {
		case msg1 := <-ch1:
			fmt.Printf("  Получено: %s\n", msg1)
		case msg2 := <-ch2:
			fmt.Printf("  Получено: %s\n", msg2)
		case <-time.After(1500 * time.Millisecond):
			fmt.Println("  Таймаут: нет сообщений 1.5 секунды")
			return
		}
	}
}

// === 4. Worker Pool (базовый) ===
func demoWorkerPoolBasic() {
	numWorkers := 3
	numTasks := 8
	
	tasks := make(chan int, numTasks)
	results := make(chan string, numTasks)
	
	var wg sync.WaitGroup
	
	// Запуск воркеров
	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for task := range tasks {
				time.Sleep(time.Duration(rand.Intn(500)+200) * time.Millisecond)
				results <- fmt.Sprintf("Воркер %d выполнил задачу %d", id, task)
			}
		}(i)
	}
	
	// Отправка задач
	go func() {
		for i := 1; i <= numTasks; i++ {
			tasks <- i
		}
		close(tasks)
	}()
	
	// Закрытие results после завершения воркеров
	go func() {
		wg.Wait()
		close(results)
	}()
	
	// Вывод результатов
	for result := range results {
		fmt.Printf("  %s\n", result)
	}
}

// === 5. Worker Pool с обработкой результатов ===
type ProcessResult struct {
	TaskID   int
	WorkerID int
	Output   string
}

func demoWorkerPoolWithResults() {
	numWorkers := 2
	numTasks := 6
	
	tasks := make(chan int, numTasks)
	results := make(chan ProcessResult, numTasks)
	formattedResults := make(chan string, numTasks)
	
	var workerWg sync.WaitGroup
	var processorWg sync.WaitGroup
	
	// Воркеры
	for i := 1; i <= numWorkers; i++ {
		workerWg.Add(1)
		go func(id int) {
			defer workerWg.Done()
			for task := range tasks {
				workTime := time.Duration(rand.Intn(400)+100) * time.Millisecond
				time.Sleep(workTime)
				
				results <- ProcessResult{
					TaskID:   task,
					WorkerID: id,
					Output:   fmt.Sprintf("Задача %d обработана", task),
				}
			}
		}(i)
	}
	
	// Процессоры результатов (2 штуки)
	for i := 1; i <= 2; i++ {
		processorWg.Add(1)
		go func(id int) {
			defer processorWg.Done()
			for result := range results {
				time.Sleep(time.Duration(rand.Intn(100)+50) * time.Millisecond)
				formattedResults <- fmt.Sprintf("Процессор %d: %s (воркер %d)", 
					id, result.Output, result.WorkerID)
			}
		}(i)
	}
	
	// Отправка задач
	go func() {
		for i := 1; i <= numTasks; i++ {
			tasks <- i
		}
		close(tasks)
	}()
	
	// Закрытие каналов
	go func() {
		workerWg.Wait()
		close(results)
		processorWg.Wait()
		close(formattedResults)
	}()
	
	// Вывод результатов
	for result := range formattedResults {
		fmt.Printf("  %s\n", result)
	}
}

// === 6. Fan-out/Fan-in паттерн ===
func demoFanOutFanIn() {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	
	// Fan-out: несколько производителей
	producer1 := makeProducer(ctx, 1)
	producer2 := makeProducer(ctx, 2)
	
	// Worker pool
	worker1 := makeWorker(ctx, producer1, 1)
	worker2 := makeWorker(ctx, producer2, 2)
	
	// Fan-in: объединение результатов
	results := mergeResults(ctx, worker1, worker2)
	
	// Чтение результатов
	for result := range results {
		fmt.Printf("  Результат: %d\n", result)
	}
}

func makeProducer(ctx context.Context, id int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for i := 1; i <= 3; i++ {
			select {
			case out <- i * id:
				time.Sleep(200 * time.Millisecond)
			case <-ctx.Done():
				return
			}
		}
	}()
	return out
}

func makeWorker(ctx context.Context, in <-chan int, id int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range in {
			select {
			case out <- n * 2:
				time.Sleep(100 * time.Millisecond)
			case <-ctx.Done():
				return
			}
		}
	}()
	return out
}

func mergeResults(ctx context.Context, inputs ...<-chan int) <-chan int {
	var wg sync.WaitGroup
	out := make(chan int)
	
	for _, input := range inputs {
		wg.Add(1)
		go func(c <-chan int) {
			defer wg.Done()
			for n := range c {
				select {
				case out <- n:
				case <-ctx.Done():
					return
				}
			}
		}(input)
	}
	
	go func() {
		wg.Wait()
		close(out)
	}()
	
	return out
}

// === 7. HTTP сервер ===
var (
	requestCount    int64
	activeRequests  int32
	serverStartTime = time.Now()
)

func handler(w http.ResponseWriter, r *http.Request) {
	atomic.AddInt32(&activeRequests, 1)
	defer atomic.AddInt32(&activeRequests, -1)
	
	id := atomic.AddInt64(&requestCount, 1)
	
	switch r.URL.Path {
	case "/":
		fmt.Fprintf(w, "Request #%d\nActive: %d\nUptime: %v",
			id, atomic.LoadInt32(&activeRequests), time.Since(serverStartTime))
	case "/slow":
		time.Sleep(2 * time.Second)
		fmt.Fprintf(w, "Slow request #%d", id)
	case "/health":
		fmt.Fprintf(w, "OK\nTotal: %d\nActive: %d",
			atomic.LoadInt64(&requestCount), atomic.LoadInt32(&activeRequests))
	default:
		http.NotFound(w, r)
	}
}

func startHTTPServer() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", handler)
	
	server := &http.Server{
		Addr:         ":8080",
		Handler:      mux,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
	}
	
	go func() {
		log.Println("HTTP сервер запущен на :8080")
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatal(err)
		}
	}()
	
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
	<-quit
	
	log.Println("Остановка сервера...")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	
	if err := server.Shutdown(ctx); err != nil {
		log.Printf("Ошибка остановки: %v", err)
	}
	
	log.Println("Сервер остановлен")
}