// app/static/js/main.js
document.addEventListener('DOMContentLoaded', () => {
    // Установка минимальных дат
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[type="date"]').forEach(input => {
        input.min = today;
    });

    // Анимация модалок
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', () => {
            const modalDialog = modal.querySelector('.modal-dialog');
            modalDialog.classList.add('animate__animated', 'animate__zoomIn', 'animate__fast Молниеносно');
        });
        modal.addEventListener('hide.bs.modal', () => {
            const modalDialog = modal.querySelector('.modal-dialog');
            modalDialog.classList.remove('animate__animated', 'animate__zoomIn', 'animate__fast');
        });
    });

    // Убрали старую обработку flash-сообщений — теперь всё в auth.js
});