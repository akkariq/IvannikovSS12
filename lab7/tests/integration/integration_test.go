package integration

import (
	"context"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"

	"myproject/internal/server"
	"myproject/internal/utils"
	"myproject/internal/worker"
)

func TestIntegration_BasicComponents(t *testing.T) {
	fmt.Println("=== Интеграционный тест базовых компонентов ===")

	// 1. Тестируем utils.Counter
	t.Run("Utils Counter", func(t *testing.T) {
		counter := &utils.Counter{}
		var wg sync.WaitGroup

		for i := 0; i < 10; i++ {
			wg.Add(1)
			go func(id int) {
				defer wg.Done()
				counter.Increment()
				fmt.Printf("  Горутина %d увеличила счетчик\n", id)
			}(i)
		}

		wg.Wait()

		if counter.Value() != 10 {
			t.Errorf("Counter expected 10, got %d", counter.Value())
		}
	})

	// 2. Тестируем worker pool
	t.Run("Worker Pool", func(t *testing.T) {
		pool := worker.NewWorkerPool(3)
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()

		tasks := []worker.Task{
			{ID: 1, Data: "task1"},
			{ID: 2, Data: "task2"},
			{ID: 3, Data: "task3"},
		}

		processor := func(task worker.Task) worker.Result {
			time.Sleep(50 * time.Millisecond)
			return worker.Result{
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
				t.Errorf("Task %d failed: %v", result.TaskID, result.Error)
			}
		}
	})

	// 3. Тестируем HTTP сервер (статически)
	t.Run("HTTP Server Static", func(t *testing.T) {
		srv := server.NewServer(":0")

		// Тестируем health endpoint
		req := httptest.NewRequest("GET", "/health", nil)
		rr := httptest.NewRecorder()
		srv.Handler.ServeHTTP(rr, req)

		if status := rr.Code; status != http.StatusOK {
			t.Errorf("handler returned wrong status code: got %v want %v",
				status, http.StatusOK)
		}

		expected := "Server is healthy"
		if !strings.Contains(rr.Body.String(), expected) {
			t.Errorf("handler returned unexpected body: got %q want to contain %q",
				rr.Body.String(), expected)
		}
	})
}

func TestIntegration_WorkerPoolWithMockHTTPServer(t *testing.T) {
	// Создаем мок-сервер для тестирования
	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	}))
	defer mockServer.Close()

	// Создаем worker pool
	pool := worker.NewWorkerPool(3)
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	tasks := []worker.Task{
		{ID: 1, Data: mockServer.URL + "/test1"},
		{ID: 2, Data: mockServer.URL + "/test2"},
		{ID: 3, Data: mockServer.URL + "/test3"},
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

func TestIntegration_ConcurrentAccess(t *testing.T) {
	// Тест конкурентного доступа к разным компонентам
	srv := server.NewServer(":0")
	var wg sync.WaitGroup

	// Конкурентные запросы к серверу
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			req := httptest.NewRequest("GET", "/health", nil)
			rr := httptest.NewRecorder()
			srv.Handler.ServeHTTP(rr, req)

			if rr.Code != http.StatusOK {
				t.Errorf("Request %d failed with status: %d", id, rr.Code)
			}
		}(i)
	}

	// Конкурентные операции с Counter
	counter := &utils.Counter{}
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			counter.Increment()
		}(i)
	}

	wg.Wait()

	// Проверяем, что все операции завершились
	if counter.Value() != 5 {
		t.Errorf("Counter expected 5, got %d", counter.Value())
	}
}

func TestIntegration_ErrorHandling(t *testing.T) {
	// Тест обработки ошибок
	pool := worker.NewWorkerPool(2)
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	tasks := []worker.Task{
		{ID: 1, Data: "valid"},
		{ID: 2, Data: "error"},
	}

	processor := func(task worker.Task) worker.Result {
		if task.Data.(string) == "error" {
			return worker.Result{
				TaskID: task.ID,
				Error:  fmt.Errorf("simulated error"),
			}
		}
		return worker.Result{
			TaskID: task.ID,
			Output: "success",
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
		t.Errorf("Expected 1 success and 1 error, got %d success and %d errors",
			successCount, errorCount)
	}
}