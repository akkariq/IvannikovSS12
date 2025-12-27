package worker

import (
    "context"
    "sync"
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