package utils

import (
    "sync"
    "testing"
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