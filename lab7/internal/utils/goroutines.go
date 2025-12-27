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