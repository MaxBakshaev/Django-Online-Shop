document.addEventListener('DOMContentLoaded', function() {
    const dropdownButton = document.getElementById('dropdownButton');
    const dropdownContent = document.getElementById('navbar-vertical');

    dropdownButton.addEventListener('click', function(event) {
        event.preventDefault(); // предотвращаем переход по ссылке
        dropdownContent.classList.toggle('show');
        event.stopPropagation(); // предотвращаем всплытие события
    });

    // Закрываем выпадающее меню при клике вне его
    window.addEventListener('click', function(event) {
        if (dropdownContent.classList.contains('show')) {
            dropdownContent.classList.remove('show');
        }
    });
});