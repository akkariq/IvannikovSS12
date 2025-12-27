[file name]: Comparison.hs
[file content begin]
{-# LANGUAGE BangPatterns #-}
module Main where

import Data.List (sortBy)
import Text.Printf (printf)

-- Модель данных
data User = User { userId :: Int, userName :: String, userEmail :: String }
    deriving (Show)

data Product = Product { productId :: Int, productName :: String, productPrice :: Double, productCategory :: String }
    deriving (Show)

data OrderItem = OrderItem { itemProduct :: Product, itemQuantity :: Int }
    deriving (Show)

data Order = Order { orderId :: Int, orderUser :: User, orderItems :: Maybe [OrderItem], orderStatus :: String }
    deriving (Show)

-- Типы ошибок для обработки
data OrderError = 
      NullItems
    | EmptyItems
    | InvalidPrice String Double
    | InvalidQuantity String Int
    | NegativeTotal Double
    | CalculationError String
    deriving (Show, Eq)

-- Пример данных с потенциальными ошибками
users :: [User]
users = [
    User 1 "John Doe" "john@example.com",
    User 2 "Jane Smith" "jane@example.com"
    ]

products :: [Product]
products = [
    Product 1 "iPhone" 999.99 "electronics",
    Product 2 "MacBook" 1999.99 "electronics",
    Product 3 "T-shirt" 29.99 "clothing",
    Product 4 "Defective" (0/0) "electronics",  -- NaN
    Product 5 "Infinite" (1/0) "electronics",   -- Infinity
    Product 6 "Free" 0.0 "clothing",
    Product 7 "Negative" (-10.0) "electronics"
    ]

orders :: [Order]
orders = [
    -- Корректный заказ
    Order 1 (users !! 0) (Just [
        OrderItem (products !! 0) 1,
        OrderItem (products !! 2) 2
    ]) "completed",
    -- Заказ с пустым списком
    Order 2 (users !! 1) (Just []) "empty",
    -- Заказ с Nothing
    Order 3 (users !! 0) Nothing "null",
    -- Заказ с NaN ценой
    Order 4 (users !! 1) (Just [
        OrderItem (products !! 3) 1
    ]) "error",
    -- Заказ с Infinite ценой
    Order 5 (users !! 0) (Just [
        OrderItem (products !! 4) 1
    ]) "error",
    -- Заказ с отрицательной ценой
    Order 6 (users !! 1) (Just [
        OrderItem (products !! 6) 1
    ]) "error",
    -- Заказ с отрицательным количеством
    Order 7 (users !! 0) (Just [
        OrderItem (products !! 0) (-1)
    ]) "error",
    -- Заказ с нулевым количеством
    Order 8 (users !! 1) (Just [
        OrderItem (products !! 0) 0
    ]) "error"
    ]

-- Вспомогательные функции для проверки значений
isValidPrice :: Double -> Bool
isValidPrice price = not (isNaN price) && not (isInfinite price) && price >= 0

isValidQuantity :: Int -> Bool
isValidQuantity qty = qty > 0

-- Задание 3: Обработка ошибок в Haskell
-- Вариант 1: Maybe (для простых случаев)
safeCalculateTotalMaybe :: Order -> Maybe Double
safeCalculateTotalMaybe order = do
    -- do-нотация для Maybe автоматически обрабатывает Nothing
    items <- orderItems order  -- Извлекаем из Maybe, если Nothing -> весь результат Nothing
    
    if null items
        then Nothing
        else do
            let totals = map calculateItemTotal items
            sequence totals >>= Just . sum
  where
    calculateItemTotal :: OrderItem -> Maybe Double
    calculateItemTotal item = do
        let price = productPrice (itemProduct item)
            quantity = itemQuantity item
        
        if not (isValidPrice price)
            then Nothing
            else if not (isValidQuantity quantity)
                then Nothing
                else Just (price * fromIntegral quantity)

-- Вариант 2: Either (с информацией об ошибке)
safeCalculateTotalEither :: Order -> Either OrderError Double
safeCalculateTotalEither order = 
    case orderItems order of
        Nothing -> Left NullItems
        Just items -> 
            if null items
                then Left EmptyItems
                else calculate items
  where
    calculate :: [OrderItem] -> Either OrderError Double
    calculate = foldM calculateItem 0.0
    
    calculateItem :: Double -> OrderItem -> Either OrderError Double
    calculateItem acc item = do
        let price = productPrice (itemProduct item)
            quantity = itemQuantity item
            productName = productName (itemProduct item)
        
        -- Проверка цены
        if isNaN price
            then Left $ InvalidPrice productName price
            else if isInfinite price
                then Left $ InvalidPrice productName price
                else if price < 0
                    then Left $ InvalidPrice productName price
                    -- Проверка количества
                    else if quantity <= 0
                        then Left $ InvalidQuantity productName quantity
                        else do
                            let itemTotal = price * fromIntegral quantity
                            
                            -- Проверка на переполнение
                            if isInfinite itemTotal
                                then Left $ CalculationError $ 
                                     "Overflow for product " ++ productName
                                else Right (acc + itemTotal)

-- Вариант 3: Использование Either с монадическими операциями
safeCalculateTotalMonadic :: Order -> Either OrderError Double
safeCalculateTotalMonadic order = do
    items <- maybe (Left NullItems) Right (orderItems order)
    
    if null items
        then Left EmptyItems
        else foldM processItem 0.0 items
  where
    processItem :: Double -> OrderItem -> Either OrderError Double
    processItem acc item = do
        let price = productPrice (itemProduct item)
            quantity = itemQuantity item
            pname = productName (itemProduct item)
        
        -- Используем guard для проверок
        when (isNaN price || isInfinite price || price < 0) $
            Left $ InvalidPrice pname price
        
        when (quantity <= 0) $
            Left $ InvalidQuantity pname quantity
        
        let itemTotal = price * fromIntegral quantity
        
        when (isInfinite itemTotal) $
            Left $ CalculationError $ "Overflow for " ++ pname
        
        Right (acc + itemTotal)
    
    when :: Bool -> Either OrderError () -> Either OrderError ()
    when condition action = if condition then action else Right ()

-- Вариант 4: Пользовательский монадический тип
newtype SafeCalculation a = SafeCalculation { runSafe :: Either OrderError a }
    deriving (Show, Eq)

instance Functor SafeCalculation where
    fmap f (SafeCalculation x) = SafeCalculation (fmap f x)

instance Applicative SafeCalculation where
    pure = SafeCalculation . Right
    (SafeCalculation f) <*> (SafeCalculation x) = SafeCalculation (f <*> x)

instance Monad SafeCalculation where
    (SafeCalculation x) >>= f = SafeCalculation $ x >>= runSafe . f

safeCalculateTotalCustom :: Order -> SafeCalculation Double
safeCalculateTotalCustom order = do
    items <- SafeCalculation $ 
        case orderItems order of
            Nothing -> Left NullItems
            Just xs -> if null xs then Left EmptyItems else Right xs
    
    foldM processItem 0.0 items
  where
    processItem :: Double -> OrderItem -> SafeCalculation Double
    processItem acc item = do
        let price = productPrice (itemProduct item)
            quantity = itemQuantity item
            pname = productName (itemProduct item)
        
        -- Проверка цены
        if isNaN price || isInfinite price || price < 0
            then SafeCalculation $ Left $ InvalidPrice pname price
            -- Проверка количества
            else if quantity <= 0
                then SafeCalculation $ Left $ InvalidQuantity pname quantity
                else do
                    let itemTotal = price * fromIntegral quantity
                    
                    -- Проверка на переполнение
                    if isInfinite itemTotal
                        then SafeCalculation $ Left $ 
                             CalculationError $ "Overflow for " ++ pname
                        else return (acc + itemTotal)

-- Вариант 5: Использование монады Except из transformers
import Control.Monad.Except

safeCalculateTotalExcept :: Order -> Except OrderError Double
safeCalculateTotalExcept order = do
    items <- case orderItems order of
        Nothing -> throwError NullItems
        Just xs -> if null xs then throwError EmptyItems else return xs
    
    foldM processItem 0.0 items
  where
    processItem :: Double -> OrderItem -> Except OrderError Double
    processItem acc item = do
        let price = productPrice (itemProduct item)
            quantity = itemQuantity item
            pname = productName (itemProduct item)
        
        -- Проверки с использованием монадических операций
        when (isNaN price || isInfinite price || price < 0) $
            throwError $ InvalidPrice pname price
        
        when (quantity <= 0) $
            throwError $ InvalidQuantity pname quantity
        
        let itemTotal = price * fromIntegral quantity
        
        when (isInfinite itemTotal) $
            throwError $ CalculationError $ "Overflow for " ++ pname
        
        return (acc + itemTotal)

-- Демонстрация обработки ошибок
demonstrateErrorHandling :: IO ()
demonstrateErrorHandling = do
    putStrLn "\n" ++ replicate 60 '='
    putStrLn "ОБРАБОТКА ОШИБОК В HASKELL"
    putStrLn replicate 60 '='
    
    mapM_ processOrder orders
  where
    processOrder :: Order -> IO ()
    processOrder order = do
        putStrLn $ "\nЗаказ #" ++ show (orderId order) ++ 
                  " (статус: " ++ orderStatus order ++ "):"
        
        -- Вариант 1: Maybe
        case safeCalculateTotalMaybe order of
            Nothing -> putStrLn "  Maybe: Ошибка - невозможно вычислить"
            Just total -> printf "  Maybe: Успех - %.2f\n" total
        
        -- Вариант 2: Either
        case safeCalculateTotalEither order of
            Left err -> putStrLn $ "  Either: Ошибка - " ++ show err
            Right total -> printf "  Either: Успех - %.2f\n" total
        
        -- Вариант 3: Монадический
        case safeCalculateTotalMonadic order of
            Left err -> putStrLn $ "  Monadic: Ошибка - " ++ show err
            Right total -> printf "  Monadic: Успех - %.2f\n" total
        
        -- Вариант 4: Пользовательская монада
        case runSafe (safeCalculateTotalCustom order) of
            Left err -> putStrLn $ "  Custom: Ошибка - " ++ show err
            Right total -> printf "  Custom: Успех - %.2f\n" total
        
        -- Вариант 5: Except
        case runExcept (safeCalculateTotalExcept order) of
            Left err -> putStrLn $ "  Except: Ошибка - " ++ show err
            Right total -> printf "  Except: Успех - %.2f\n" total

-- Пример цепочки вычислений с обработкой ошибок
processOrderChain :: Order -> Either OrderError (Double, Double)
processOrderChain order = do
    total <- safeCalculateTotalEither order
    let discounted = if total > 1000 then total * 0.9 else total
    
    if discounted < 0
        then Left $ NegativeTotal discounted
        else Right (total, discounted)

-- Основная функция
main :: IO ()
main = do
    putStrLn "=== HASKELL - Обработка заказов с обработкой ошибок ==="
    
    demonstrateErrorHandling
    
    putStrLn "\n" ++ replicate 60 '='
    putStrLn "ПРИМЕР ЦЕПОЧКИ ВЫЧИСЛЕНИЙ"
    putStrLn replicate 60 '='
    
    mapM_ processChain orders
  where
    processChain :: Order -> IO ()
    processChain order = do
        case processOrderChain order of
            Left err -> 
                putStrLn $ "Заказ #" ++ show (orderId order) ++ 
                          ": ошибка - " ++ show err
            Right (original, discounted) ->
                printf "Заказ #%d: оригинал=%.2f, со скидкой=%.2f\n" 
                       (orderId order) original discounted
    
    putStrLn "\n" ++ replicate 60 '='
    putStrLn "ПРЕИМУЩЕСТВА HASKELL ДЛЯ ОБРАБОТКИ ОШИБОК"
    putStrLn replicate 60 '='
    
    putStrLn $ unlines
        [ ""
        , "1. Maybe a - для значений, которые могут отсутствовать"
        , "   • Just value - значение присутствует"
        , "   • Nothing - значение отсутствует"
        , ""
        , "2. Either a b - для операций, которые могут завершиться ошибкой"
        , "   • Left error - операция завершилась ошибкой"
        , "   • Right value - операция успешна"
        , ""
        , "3. do-нотация - удобная композиция операций с ошибками"
        , "   • Автоматическая обработка Nothing/Left"
        , "   • Чистый код без явных проверок"
        , ""
        , "4. Монады - абстракция для последовательных вычислений"
        , "   • Maybe монада - игнорирует Nothing"
        , "   • Either монада - передает Left"
        , "   • ExceptT - монада-трансформер для исключений"
        , ""
        , "5. Паттерн-матчинг - исчерпывающая обработка всех случаев"
        , "   • Компилятор проверяет все варианты"
        , "   • Невозможно забыть обработать ошибку"
        , ""
        , "6. Чистота - ошибки являются значениями, а не побочными эффектами"
        , "   • Предсказуемое поведение"
        , "   • Легко тестировать"
        , "   • Композируемость"
        ]
    
    putStrLn $ replicate 60 '='
    putStrLn "СРАВНЕНИЕ С ДРУГИМИ ЯЗЫКАМИ"
    putStrLn $ replicate 60 '='
    
    putStrLn $ unlines
        [ ""
        , "Haskell:     Maybe/Either, монадический стиль, проверка при компиляции"
        , "Scala:       Option/Try/Either, for-comprehension, проверка при компиляции"
        , "Rust:        Option/Result, ? оператор, проверка при компиляции"
        , "Python:      try/except/Optional, проверка во время выполнения"
        , "JavaScript:  try/catch/Promise, проверка во время выполнения"
        , ""
        , "Ключевое отличие Haskell:"
        , "  • Нет исключений как побочных эффектов"
        , "  • Все ошибки - значения"
        , "  • Компилятор заставляет обрабатывать все случаи"
        , "  • Чисто функциональный подход"
        ]
[file content end]