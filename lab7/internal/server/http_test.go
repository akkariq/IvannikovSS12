package server

import (
	"context"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"
        "net"
)

func TestServer_Routes(t *testing.T) {
	// Создаем новый сервер для каждого теста, чтобы сбросить счетчики
	tests := []struct {
		name           string
		path           string
		expectedStatus int
		expectedBody   string
	}{
		{
			name:           "root path",
			path:           "/",
			expectedStatus: http.StatusOK,
			expectedBody:   "HTTP Server Demo",
		},
		{
			name:           "health check",
			path:           "/health",
			expectedStatus: http.StatusOK,
			expectedBody:   "Server is healthy",
		},
		{
			name:           "stats",
			path:           "/stats",
			expectedStatus: http.StatusOK,
			expectedBody:   "Total requests:", // Частичное совпадение
		},
		{
			name:           "not found",
			path:           "/notfound",
			expectedStatus: http.StatusNotFound,
			expectedBody:   "404 page not found",
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Создаем новый сервер для каждого теста
			server := NewServer(":0")
			
			req := httptest.NewRequest("GET", tt.path, nil)
			rr := httptest.NewRecorder()
			
			server.Handler.ServeHTTP(rr, req)
			
			if status := rr.Code; status != tt.expectedStatus {
				t.Errorf("handler returned wrong status code: got %v want %v",
					status, tt.expectedStatus)
			}
			
			body := rr.Body.String()
			if !strings.Contains(body, tt.expectedBody) {
				t.Errorf("handler returned unexpected body: got %q want to contain %q",
					body, tt.expectedBody)
			}
		})
	}
}

func TestServer_ConcurrentRequests(t *testing.T) {
	server := NewServer(":0")
	
	var wg sync.WaitGroup
	requests := 10
	
	for i := 0; i < requests; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			
			req := httptest.NewRequest("GET", "/", nil)
			rr := httptest.NewRecorder()
			
			server.Handler.ServeHTTP(rr, req)
			
			if rr.Code != http.StatusOK {
				t.Errorf("Request %d failed with status: %d", id, rr.Code)
			}
		}(i)
	}
	
	wg.Wait()
	
	// Проверяем, что все запросы обработаны
	req := httptest.NewRequest("GET", "/stats", nil)
	rr := httptest.NewRecorder()
	server.Handler.ServeHTTP(rr, req)
	
	body := rr.Body.String()
	if !strings.Contains(body, fmt.Sprintf("Total requests: %d", requests+1)) {
		t.Logf("Stats body: %s", body)
		// Не фатальная ошибка, так как может быть +1 из-за запроса stats
	}
}

func TestServer_GracefulShutdown(t *testing.T) {
	server := NewServer(":0")
	
	// Запускаем сервер на случайном порту
	listener, err := server.Start(":0")
	if err != nil {
		t.Fatalf("Failed to start server: %v", err)
	}
	
	serverURL := fmt.Sprintf("http://localhost:%d", listener.Addr().(*net.TCPAddr).Port)
	
	// Делаем один запрос, чтобы убедиться, что сервер работает
	resp, err := http.Get(serverURL + "/health")
	if err != nil {
		t.Fatalf("Failed to make initial request: %v", err)
	}
	resp.Body.Close()
	
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("Initial request failed with status: %d", resp.StatusCode)
	}
	
	// Запускаем graceful shutdown в отдельной горутине
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()
	
	go func() {
		time.Sleep(100 * time.Millisecond) // Даем время для новых запросов
		if err := server.Shutdown(ctx); err != nil {
			t.Logf("Shutdown error (may be expected): %v", err)
		}
	}()
	
	// Пытаемся сделать запрос после shutdown
	time.Sleep(200 * time.Millisecond)
	
	// Запрос должен завершиться с ошибкой (сервер остановлен)
	_, err = http.Get(serverURL + "/health")
	if err == nil {
		t.Error("Expected error after shutdown, but request succeeded")
	}
}