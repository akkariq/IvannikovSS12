module Recursion where

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
