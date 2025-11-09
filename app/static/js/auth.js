// app/static/js/auth.js
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const loginModalEl = document.getElementById('loginModal');
    const registerModalEl = document.getElementById('registerModal');
    const loginModal = loginModalEl ? bootstrap.Modal.getOrCreateInstance(loginModalEl) : null;
    const registerModal = registerModalEl ? bootstrap.Modal.getOrCreateInstance(registerModalEl) : null;

    const showMessage = (id, text, type = 'danger') => {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = text;
    el.className = `text-${type}`;
    el.classList.add('show');
    setTimeout(() => {
        el.classList.remove('show');
    }, 3000);
};

    // === РЕГИСТРАЦИЯ (обновлённый payload) ===
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(registerForm);
            const payload = {
                first_name: formData.get('first_name'),
                last_name: formData.get('last_name'),
                email: formData.get('email'),
                password: formData.get('password'),
                phone: formData.get('phone') || null  // Опционально
            };

            // Простая фронт-валидация
            if (payload.password.length < 6) {
                showMessage('registerMessage', 'Пароль должен быть минимум 6 символов', 'danger');
                return;
            }

            try {
                const response = await fetch('/api/v1/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();

                if (!response.ok) {
                    showMessage('registerMessage', data.detail || 'Ошибка регистрации', 'danger');
                    return;
                }

                showMessage('registerMessage', 'Регистрация успешна! Сейчас откроется вход.', 'success');
                setTimeout(() => {
                    registerModal.hide();
                    loginModal.show();
                }, 2000);
            } catch (err) {
                showMessage('registerMessage', 'Ошибка сети', 'danger');
                console.error(err);
            }
        });
    }

    // === ВХОД (без изменений) ===
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);
            const payload = new URLSearchParams();
            payload.append('username', formData.get('email'));
            payload.append('password', formData.get('password'));

            try {
                const response = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: payload
                });

                const data = await response.json();

                if (!response.ok) {
                    showMessage('loginMessage', data.detail || 'Неверный email или пароль', 'danger');
                    return;
                }

                showMessage('loginMessage', 'Вход успешен! Обновляем страницу...', 'success');
                setTimeout(() => {
                    loginModal.hide();
                    location.reload();
                }, 1500);
            } catch (err) {
                showMessage('loginMessage', 'Ошибка сети', 'danger');
                console.error(err);
            }
        });
    }
});