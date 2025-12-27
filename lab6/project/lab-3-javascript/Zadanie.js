import React, { useState, useEffect, useCallback, useMemo } from 'react';

const users = [
    { name: 'John', age: 25, city: 'New York', active: true, email: 'john@example.com' },
    { name: 'Jane', age: 30, city: 'Boston', active: false, email: 'jane@example.com' }
];



const processUsers = (users) => {
    // TODO: Вернуть объект с:
    // - средним возрастом пользователей
    const sredVozrast = (users.reduce((sum, x) => sum + x.age, 0)) / users.length;
    console.log("111",sredVozrast);
    // - количеством пользователей по городу
    const lenLydei = users.length;
    console.log("222",lenLydei);
    // - списком email активных пользователей
    const activMail = users
        .filter(a => a.active)
        .map(a => a.email);
  
    console.log("333",spiisMail);
};

console.log('Vizov:', processUsers(users));


const useForm = (initialValues = {}) => {
    // TODO: Реализовать хук для управления состоянием формы
    // с валидацией и обработкой submit
    const [values, setValues] = useState(initialValues);
    const [errors, setErrors] = useState({});

    const handleChange = useCallback((name, value) => {
        setValues(prev => ({ ...prev, [name]: value }));
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    }, [errors]);

    const handleSubmit = useCallback((onSubmit) => (e) => {
        e.preventDefault();
        const newErrors = {};
        
        Object.keys(values).forEach(key => {
            if (!values[key]) {
                newErrors[key] = 'Поле обязательно';
            }
        });

        setErrors(newErrors);

        if (Object.keys(newErrors).length === 0) {
            onSubmit(values);
        }
    }, [values]);

    const resetForm = useCallback(() => {
        setValues(initialValues);
        setErrors({});
    }, [initialValues]);

    return {
        values,
        errors,
        handleChange,
        handleSubmit,
        resetForm
    };
};


function debounce(func, delay) {
    let timeoutId;
    
    return function(...args) {
        
        clearTimeout(timeoutId);
        
        
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}