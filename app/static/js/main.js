// app/static/js/main.js
document.addEventListener('DOMContentLoaded', () => {
    // Установка минимальных дат
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[type="date"]').forEach(input => {
        input.min = today;
    });

    // Анимация модалок при открытии
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', () => {
            const modalDialog = modal.querySelector('.modal-dialog');
            modalDialog.classList.add('animate__animated', 'animate__zoomIn', 'animate__fast');
        });
        modal.addEventListener('hide.bs.modal', () => {
            const modalDialog = modal.querySelector('.modal-dialog');
            modalDialog.classList.remove('animate__animated', 'animate__zoomIn', 'animate__fast');
        });
    });

    // Обработка сообщений об ошибках/успехе (если бэкенд вернёт flash-сообщения)
    // Пример: если в шаблоне есть <div id="message">{{ message }}</div>
    const messageDiv = document.getElementById('loginMessage') || document.getElementById('registerMessage');
    if (messageDiv && messageDiv.textContent.trim()) {
        messageDiv.style.display = 'block';
        setTimeout(() => {
            messageDiv.classList.add('animate__animated', 'animate__fadeOut');
            messageDiv.addEventListener('animationend', () => {
                messageDiv.style.display = 'none';
            });
        }, 3000);
    }
});