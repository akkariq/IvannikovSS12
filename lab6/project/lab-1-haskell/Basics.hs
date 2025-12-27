
module Basics where

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