package utils

import (
	"context"
	"testing"
	"time"
)

func TestMergeChannels(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()
	
	ch1 := make(chan int, 3)
	ch2 := make(chan int, 3)
	
	// Заполняем каналы ДО запуска MergeChannels
	for i := 0; i < 3; i++ {
		ch1 <- i
		ch2 <- i + 3
	}
	
	// Закрываем каналы ДО запуска MergeChannels
	close(ch1)
	close(ch2)
	
	// Объединяем каналы
	merged := MergeChannels(ctx, ch1, ch2)
	
	// Собираем результаты
	var results []int
	for val := range merged {
		results = append(results, val)
	}
	
	// Проверяем - должно быть 6 значений
	if len(results) != 6 {
		t.Errorf("Expected 6 values, got %d", len(results))
	}
}

func TestSafeMergeChannels(t *testing.T) {
	ch1 := make(chan int, 3)
	ch2 := make(chan int, 3)
	
	// Заполняем каналы
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
	
	// Объединяем каналы
	merged := SafeMergeChannels(ch1, ch2)
	
	// Собираем результаты
	var results []int
	for val := range merged {
		results = append(results, val)
	}
	
	if len(results) != 6 {
		t.Errorf("Expected 6 values, got %d", len(results))
	}
}

func TestMergeChannels_Empty(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()
	
	ch1 := make(chan int)
	ch2 := make(chan int)
	
	// Сразу закрываем каналы
	close(ch1)
	close(ch2)
	
	merged := MergeChannels(ctx, ch1, ch2)
	
	// Должен быть закрыт
	select {
	case _, ok := <-merged:
		if ok {
			t.Error("Channel should be closed")
		}
	case <-time.After(50 * time.Millisecond):
		// OK
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