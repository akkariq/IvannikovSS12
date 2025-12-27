use std::rc::Rc;

// Функциональный список
#[derive(Debug)]
enum List<T> {
    Empty,
    Cons(T, Rc<List<T>>),
}

impl<T> List<T> {
    fn new() -> Self {
        List::Empty
    }
    
    fn prepend(self, elem: T) -> Self {
        List::Cons(elem, Rc::new(self))
    }
    
    fn head(&self) -> Option<&T> {
        match self {
            List::Cons(head, _) => Some(head),
            List::Empty => None,
        }
    }
    
    fn tail(&self) -> Option<&List<T>> {
        match self {
            List::Cons(_, tail) => Some(tail),
            List::Empty => None,
        }
    }
    
    fn iter(&self) -> ListIter<T> {
        ListIter { current: self }
    }
}

// Итератор для функционального списка
struct ListIter<'a, T> {
    current: &'a List<T>,
}

impl<'a, T> Iterator for ListIter<'a, T> {
    type Item = &'a T;
    
    fn next(&mut self) -> Option<Self::Item> {
        match self.current {
            List::Cons(head, tail) => {
                self.current = tail;
                Some(head)
            }
            List::Empty => None,
        }
    }
}

fn demonstrate_functional_structures() {
    println!("\n=== Функциональные структуры данных ===");
    
    // Создание списка в функциональном стиле
    let list = List::new()
        .prepend(3)
        .prepend(2)
        .prepend(1);
    
    println!("Функциональный список: {:?}", list);
    
    // Итерация по списку
    println!("Элементы списка:");
    for elem in list.iter() {
        println!("- {}", elem);
    }
    
    // Голова и хвост
    if let Some(head) = list.head() {
        println!("Голова списка: {}", head);
    }
    
    if let Some(tail) = list.tail() {
        println!("Хвост списка: {:?}", tail);
    }
}

// Неизменяемая структура данных
#[derive(Debug, Clone)]
struct ImmutablePoint {
    x: f64,
    y: f64,
}

impl ImmutablePoint {
    fn new(x: f64, y: f64) -> Self {
        ImmutablePoint { x, y }
    }
    
    // Вместо мутации возвращаем новую структуру
    fn translate(&self, dx: f64, dy: f64) -> Self {
        ImmutablePoint {
            x: self.x + dx,
            y: self.y + dy,
        }
    }
    
    fn distance(&self, other: &ImmutablePoint) -> f64 {
        ((self.x - other.x).powi(2) + (self.y - other.y).powi(2)).sqrt()
    }
}

fn main() {av
    demonstrate_functional_structures();
    
    // Демонстрация неизменяемой точки
    let point1 = ImmutablePoint::new(0.0, 0.0);
    let point2 = point1.translate(3.0, 4.0);
    
    println!("Расстояние между {:?} и {:?} = {:.2}", point1, point2, point1.distance(&point2));
}