module Main where

import HigherOrder
import Recursion
import Basics

countEven :: [Int] -> Int
countEven xs = length(filter' even xs)

positiveSquares :: [Int] -> [Int]
positiveSquares xs = map' (^2) (filter' (>0) xs)


bubblePass :: Ord a => [a] -> [a]
bubblePass [] = []
bubblePass [a] = [a]
bubblePass (x:y:xs)
    | x > y = y : bubblePass (x:xs)
    | otherwise = x : bubblePass (y:xs)

bubbleSort :: Ord a => [a] -> [a]
bubbleSort xs 
    | xs == sorted = xs  
    | otherwise = bubbleSort (bubblePass xs)
    where sorted = bubblePass xs


main :: IO ()
main = do
    print $ countEven [1,2,3,4]
    print $ positiveSquares [-3,-2,-1,1,2,3]
    print $ bubbleSort [4,1,2,3]
