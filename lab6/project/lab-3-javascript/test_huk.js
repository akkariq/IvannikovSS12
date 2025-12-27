// Пример использования для лабораторной
const UserForm = () => {
    const { values, errors, handleChange, handleSubmit } = useForm({
        name: '',
        email: '',
        age: ''
    });

    const onSubmit = (formData) => {
        console.log('Данные формы:', formData);
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <input
                value={values.name}
                onChange={(e) => handleChange('name', e.target.value)}
                placeholder="Имя"
            />
            {errors.name && <span>{errors.name}</span>}
            
            <input
                value={values.email}
                onChange={(e) => handleChange('email', e.target.value)}
                placeholder="Email"
            />
            {errors.email && <span>{errors.email}</span>}
            
            <button type="submit">Отправить</button>
        </form>
    );
};

export { useForm, processUsers, UserForm };