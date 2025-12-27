**Лабораторная работа 6. Функциональное программирование. Часть 1. Введение в Haskell**

**Цель работы:** Ознакомиться с основами функционального программирования, изучить базовый синтаксис Haskell, освоить основные концепции: чистые функции, иммутабельность, рекурсию, pattern matching и работу со списками.

**Задачи:**
1. Изучить базовый синтаксис Haskell и систему типов
2. Освоить создание чистых функций и использование рекурсии
3. Научиться работать со списками и pattern matching
4. Изучить основные функции высшего порядка
5. Освоить работу с кортежами и алгебраическими типами данных

**Теоретическая часть**

**Функциональное программирование: основные концепции**
Функциональное программирование (ФП) — парадигма программирования, в которой процесс вычисления рассматривается как вычисление значений функций.

**Основные понятия:**
*   **Чистые функции** - функции, которые для одинаковых входных данных всегда возвращают одинаковый результат и не имеют побочных эффектов
*   **Иммутабельность** - данные не изменяются после создания
*   **Функции высшего порядка** - функции, которые принимают другие функции в качестве аргументов или возвращают их как результат
*   **Рекурсия** - основной способ организации циклических вычислений
*   **Pattern matching** - сопоставление с образцом для декомпозиции данных

**Система типов Haskell:**
*   **Статическая типизация** - типы проверяются на этапе компиляции
*   **Вывод типов** - компилятор автоматически определяет типы выражений
*   **Алгебраические типы данных** - пользовательские типы, создаваемые программистом

**Порядок выполнения работы**

**1. Установка и настройка окружения**

```bash
# Установка Haskell на Ubuntu
sudo apt update
sudo apt install haskell-platform ghc cabal-install

# Проверка установки
ghc --version
```

**2. Базовый синтаксис и функции**

Создайте файл `basics.hs`:

```haskell
-- Простые функции
square :: Int -> Int
square x = x * x

-- Функция с двумя параметрами
add :: Int -> Int -> Int
add x y = x + y

-- Условные выражения
absolute :: Int -> Int
absolute x = if x >= 0 then x else -x

-- Охрана (guard)
grade :: Int -> String
grade score
    | score >= 90 = "Excellent"
    | score >= 75 = "Good"
    | score >= 60 = "Satisfactory"
    | otherwise   = "Fail"
```

**3. Рекурсия и работа со списками**

Создайте файл `recursion.hs`:

```haskell
-- Рекурсивный факториал
factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- Рекурсивная сумма списка
sumList :: [Int] -> Int
sumList [] = 0
sumList (x:xs) = x + sumList xs

-- Длина списка через рекурсию
length' :: [a] -> Int
length' [] = 0
length' (_:xs) = 1 + length' xs

-- Фибоначчи
fibonacci :: Int -> Int
fibonacci 0 = 0
fibonacci 1 = 1
fibonacci n = fibonacci (n-1) + fibonacci (n-2)
```

**4. Pattern matching и кортежи**

Создайте файл `patterns.hs`:

```haskell
-- Pattern matching для кортежей
addVectors :: (Double, Double) -> (Double, Double) -> (Double, Double)
addVectors (x1, y1) (x2, y2) = (x1 + x2, y1 + y2)

-- Работа с троичными кортежами
first :: (a, b, c) -> a
first (x, _, _) = x

second :: (a, b, c) -> b
second (_, y, _) = y

third :: (a, b, c) -> c
third (_, _, z) = z

-- Pattern matching в case выражениях
describeList :: [a] -> String
describeList xs = case xs of
    [] -> "Empty list"
    [x] -> "Singleton list"
    xs -> "Long list"
```

**5. Функции высшего порядка**

Создайте файл `higher_order.hs`:

```haskell
-- Применение функции к каждому элементу
map' :: (a -> b) -> [a] -> [b]
map' _ [] = []
map' f (x:xs) = f x : map' f xs

-- Фильтрация списка
filter' :: (a -> Bool) -> [a] -> [a]
filter' _ [] = []
filter' p (x:xs)
    | p x       = x : filter' p xs
    | otherwise = filter' p xs

-- Свертка (fold)
foldl' :: (b -> a -> b) -> b -> [a] -> b
foldl' _ acc [] = acc
foldl' f acc (x:xs) = foldl' f (f acc x) xs

-- Композиция функций
compose :: (b -> c) -> (a -> b) -> a -> c
compose f g x = f (g x)
```

**6. Алгебраические типы данных**

Создайте файл `types.hs`:

```haskell
-- Перечисление
data Day = Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday
    deriving (Show, Eq)

isWeekend :: Day -> Bool
isWeekend Saturday = True
isWeekend Sunday = True
isWeekend _ = False

-- Продуктовый тип
data Point = Point Double Double
    deriving (Show)

distance :: Point -> Point -> Double
distance (Point x1 y1) (Point x2 y2) = sqrt ((x2 - x1)^2 + (y2 - y1)^2)

-- Рекурсивный тип данных (список)
data List a = Empty | Cons a (List a)
    deriving (Show)

-- Функция для преобразования нашего списка в стандартный
toStandardList :: List a -> [a]
toStandardList Empty = []
toStandardList (Cons x xs) = x : toStandardList xs
```

**7. Практические задания**

**Задание 1:** Реализуйте функцию, которая вычисляет количество четных чисел в списке

```haskell
countEven :: [Int] -> Int
countEven = undefined  -- Замените на свою реализацию
```

**Задание 2:** Создайте функцию, которая возвращает список квадратов только положительных чисел

```haskell
positiveSquares :: [Int] -> [Int]
positiveSquares = undefined  -- Замените на свою реализацию
```

**Задание 3:** Реализуйте алгоритм пузырьковой сортировки

```haskell
bubbleSort :: [Int] -> [Int]
bubbleSort = undefined  -- Замените на свою реализацию
```

**Пример выполнения программы:**

```haskell
-- main.hs
module Main where

import Basics
import Recursion
import Patterns
import HigherOrder
import Types

main :: IO ()
main = do
    putStrLn "=== Демонстрация работы функций ==="
    
    -- Базовые функции
    print $ square 5
    print $ grade 85
    
    -- Рекурсия
    print $ factorial 5
    print $ sumList [1, 2, 3, 4, 5]
    
    -- Pattern matching
    print $ addVectors (1, 2) (3, 4)
    
    -- Функции высшего порядка
    print $ map' square [1, 2, 3, 4]
    print $ filter' even [1, 2, 3, 4, 5, 6]
    
    -- Алгебраические типы
    print $ distance (Point 0 0) (Point 3 4)
    print $ isWeekend Saturday
```

**Компиляция и выполнение:**

```bash
# Компиляция
ghc -o haskell_demo main.hs

# Запуск
./haskell_demo

# Или интерпретатор
ghci
:load main.hs
main
```

**Критерии оценки**

**Удовлетворительно:**
*   Установлено и настроено окружение Haskell
*   Реализованы базовые функции (факториал, сумма списка)
*   Выполнены простые задания на рекурсию

**Хорошо:**
*   Корректно реализованы функции высшего порядка (map, filter)
*   Использован pattern matching для работы с кортежами
*   Созданы простые алгебраические типы данных
*   Выполнены все практические задания

**Отлично:**
*   Реализованы сложные рекурсивные алгоритмы
*   Эффективно использованы функции высшего порядка
*   Созданы сложные алгебраические типы данных
*   Код хорошо структурирован и документирован
*   Реализованы дополнительные задания по выбору

**Контрольные вопросы**
1.  Что такое чистая функция и каковы ее свойства?
2.  Чем рекурсия в Haskell отличается от итераций в императивных языках?
3.  Как работает pattern matching и для чего он используется?
4.  Что такое функции высшего порядка? Приведите примеры.
5.  Какие преимущества дает статическая типизация в Haskell?

**Рекомендованная литература**
1.  "Learn You a Haskell for Great Good!" Miran Lipovača
2.  "Real World Haskell" Bryan O'Sullivan, Don Stewart, John Goerzen
3.  Официальная документация Haskell https://www.haskell.org/documentation/
