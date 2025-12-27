package utils

import (
	"context"
	"sync"
)

// MergeChannels безопасно объединяет несколько каналов в один
func MergeChannels(ctx context.Context, chs ...<-chan int) <-chan int {
	out := make(chan int)
	var wg sync.WaitGroup
	
	// Для каждого входного канала создаем горутину
	for _, ch := range chs {
		wg.Add(1)
		go func(c <-chan int) {
			defer wg.Done()
			
			for {
				select {
				case val, ok := <-c:
					if !ok {
						// Входной канал закрыт
						return
					}
					
					// Пытаемся отправить значение, но с проверкой контекста
					select {
					case out <- val:
						// Успешно отправлено
					case <-ctx.Done():
						// Контекст отменен
						return
					}
					
				case <-ctx.Done():
					// Контекст отменен
					return
				}
			}
		}(ch)
	}
	
	// Отдельная горутина для закрытия выходного канала
	// Это гарантирует, что канал закроется только один раз
	go func() {
		wg.Wait()
		close(out)
	}()
	
	return out
}

// SafeMergeChannels - альтернативная безопасная реализация
func SafeMergeChannels(chs ...<-chan int) <-chan int {
	out := make(chan int)
	var wg sync.WaitGroup
	
	wg.Add(len(chs))
	
	for _, ch := range chs {
		go func(c <-chan int) {
			defer wg.Done()
			for val := range c {
				out <- val
			}
		}(ch)
	}
	
	go func() {
		wg.Wait()
		close(out)
	}()
	
	return out
}

// BufferedChannelProcessor обрабатывает значения из канала
func BufferedChannelProcessor(input <-chan int, bufferSize int) <-chan int {
	output := make(chan int, bufferSize)
	
	go func() {
		defer close(output)
		for val := range input {
			output <- val * 2
		}
	}()
	
	return output
}