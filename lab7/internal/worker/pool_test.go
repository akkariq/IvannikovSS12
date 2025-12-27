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