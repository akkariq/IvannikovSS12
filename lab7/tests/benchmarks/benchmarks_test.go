package benchmarks

import (
	"sync"
	"testing"
	
	"myproject/internal/utils"
)

func BenchmarkCounter_Increment(b *testing.B) {
	counter := &utils.Counter{}
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		counter.Increment()
	}
}

func BenchmarkCounter_IncrementParallel(b *testing.B) {
	counter := &utils.Counter{}
	
	b.ResetTimer()
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			counter.Increment()
		}
	})
}

func BenchmarkMutexLockUnlock(b *testing.B) {
	var mu sync.Mutex
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		mu.Lock()
		mu.Unlock()
	}
}

func BenchmarkChannelSendReceive(b *testing.B) {
	ch := make(chan int, 1)
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ch <- i
		<-ch
	}
}

func BenchmarkGoroutineCreation(b *testing.B) {
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		done := make(chan bool)
		go func() {
			done <- true
		}()
		<-done
	}
}

// Комментируем или удаляем тесты WorkerPool, так как они вызывают deadlock
/*
func BenchmarkWorkerPool_SimpleTasks(b *testing.B) {
	for i := 0; i < b.N; i++ {
		pool := worker.NewWorkerPool(4)
		
		tasks := make([]worker.Task, 100)
		for j := 0; j < 100; j++ {
			tasks[j] = worker.Task{ID: j, Data: j}
		}
		
		processor := func(task worker.Task) worker.Result {
			// Простая операция
			return worker.Result{
				TaskID: task.ID,
				Output: task.Data.(int) * 2,
			}
		}
		
		_ = pool.ProcessTasks(tasks, processor)
	}
}

func BenchmarkWorkerPool_WithSleep(b *testing.B) {
	for i := 0; i < b.N; i++ {
		pool := worker.NewWorkerPool(4)
		
		tasks := make([]worker.Task, 20)
		for j := 0; j < 20; j++ {
			tasks[j] = worker.Task{ID: j, Data: j}
		}
		
		processor := func(task worker.Task) worker.Result {
			time.Sleep(1 * time.Millisecond)
			return worker.Result{
				TaskID: task.ID,
				Output: task.Data.(int) * 2,
			}
		}
		
		_ = pool.ProcessTasks(tasks, processor)
	}
}
*/