package server

import (
	"context"
	"fmt"
	"net"
	"net/http"
	"sync/atomic"
	"time"
)

type Server struct {
	Handler http.Handler
	server  *http.Server
	port    string
	
	// Статистика
	totalRequests   int64
	activeRequests  int32
	startTime       time.Time
}

func NewServer(port string) *Server {
	mux := http.NewServeMux()
	server := &Server{
		Handler: mux,
		port:    port,
		startTime: time.Now(),
	}
	
	// Регистрируем обработчики
	mux.HandleFunc("/", server.handleRoot)
	mux.HandleFunc("/health", server.handleHealth)
	mux.HandleFunc("/stats", server.handleStats)
	mux.HandleFunc("/slow", server.handleSlow)
	
	return server
}

func (s *Server) handleRoot(w http.ResponseWriter, r *http.Request) {
	// Если путь не "/", возвращаем 404
	if r.URL.Path != "/" {
		http.NotFound(w, r)
		return
	}
	
	atomic.AddInt32(&s.activeRequests, 1)
	defer atomic.AddInt32(&s.activeRequests, -1)
	
	requestID := atomic.AddInt64(&s.totalRequests, 1)
	
	time.Sleep(50 * time.Millisecond)
	
	fmt.Fprintf(w, "HTTP Server Demo\n\n")
	fmt.Fprintf(w, "Request ID: %d\n", requestID)
	fmt.Fprintf(w, "Active requests: %d\n", atomic.LoadInt32(&s.activeRequests))
	fmt.Fprintf(w, "Uptime: %v\n", time.Since(s.startTime).Round(time.Second))
}

func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	atomic.AddInt32(&s.activeRequests, 1)
	defer atomic.AddInt32(&s.activeRequests, -1)
	
	atomic.AddInt64(&s.totalRequests, 1)
	w.WriteHeader(http.StatusOK)
	fmt.Fprint(w, "Server is healthy\n")
}

func (s *Server) handleStats(w http.ResponseWriter, r *http.Request) {
	atomic.AddInt32(&s.activeRequests, 1)
	defer atomic.AddInt32(&s.activeRequests, -1)
	
	atomic.AddInt64(&s.totalRequests, 1)
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "Server Statistics:\n")
	fmt.Fprintf(w, "Total requests: %d\n", atomic.LoadInt64(&s.totalRequests))
	fmt.Fprintf(w, "Active requests: %d\n", atomic.LoadInt32(&s.activeRequests))
	fmt.Fprintf(w, "Uptime: %v\n", time.Since(s.startTime).Round(time.Second))
	fmt.Fprintf(w, "Start time: %v\n", s.startTime.Format("2006-01-02 15:04:05"))
}

func (s *Server) handleSlow(w http.ResponseWriter, r *http.Request) {
	atomic.AddInt32(&s.activeRequests, 1)
	defer atomic.AddInt32(&s.activeRequests, -1)
	
	atomic.AddInt64(&s.totalRequests, 1)
	time.Sleep(2 * time.Second)
	fmt.Fprintf(w, "Slow request completed after 2 seconds\n")
}

func (s *Server) Start(addr string) (net.Listener, error) {
	if addr == "" {
		addr = s.port
	}
	
	listener, err := net.Listen("tcp", addr)
	if err != nil {
		return nil, err
	}
	
	s.server = &http.Server{
		Addr:    listener.Addr().String(),
		Handler: s.Handler,
	}
	
	go func() {
		if err := s.server.Serve(listener); err != nil && err != http.ErrServerClosed {
			fmt.Printf("Server error: %v\n", err)
		}
	}()
	
	return listener, nil
}

func (s *Server) Shutdown(ctx context.Context) error {
	if s.server != nil {
		return s.server.Shutdown(ctx)
	}
	return nil
}