# Пример реализации авторизации на фронтенде

## 1. Логин и сохранение токенов

```typescript
// authService.ts
interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number; // секунды (900 = 15 минут)
}

async function login(email: string, password: string): Promise<LoginResponse> {
  const response = await fetch('http://localhost:8000/api/v0/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    throw new Error('Ошибка входа');
  }

  const data: LoginResponse = await response.json();
  
  // Сохраняем токены
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  localStorage.setItem('token_expires_at', 
    String(Date.now() + data.expires_in * 1000)
  );

  return data;
}
```

## 2. Автоматическое обновление access token

```typescript
// authService.ts
async function refreshAccessToken(): Promise<string> {
  const refreshToken = localStorage.getItem('refresh_token');
  
  if (!refreshToken) {
    throw new Error('Refresh token не найден');
  }

  const response = await fetch('http://localhost:8000/api/v0/auth/refresh', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  if (!response.ok) {
    // Refresh token истек - нужно залогиниться заново
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    throw new Error('Сессия истекла. Требуется повторный вход');
  }

  const data: LoginResponse = await response.json();
  
  // Обновляем токены
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  localStorage.setItem('token_expires_at', 
    String(Date.now() + data.expires_in * 1000)
  );

  return data.access_token;
}
```

## 3. HTTP клиент с автоматическим обновлением токена

```typescript
// apiClient.ts
async function apiRequest(
  url: string, 
  options: RequestInit = {}
): Promise<Response> {
  let accessToken = localStorage.getItem('access_token');
  const expiresAt = Number(localStorage.getItem('token_expires_at') || 0);

  // Проверяем, истек ли токен (с запасом в 1 минуту)
  if (!accessToken || Date.now() >= expiresAt - 60000) {
    try {
      accessToken = await refreshAccessToken();
    } catch (error) {
      // Редирект на страницу логина
      window.location.href = '/login';
      throw error;
    }
  }

  // Добавляем токен в заголовки
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`,
    ...options.headers,
  };

  let response = await fetch(url, {
    ...options,
    headers,
  });

  // Если получили 401, пробуем обновить токен и повторить запрос
  if (response.status === 401) {
    try {
      accessToken = await refreshAccessToken();
      response = await fetch(url, {
        ...options,
        headers: {
          ...headers,
          'Authorization': `Bearer ${accessToken}`,
        },
      });
    } catch (error) {
      window.location.href = '/login';
      throw error;
    }
  }

  return response;
}

// Пример использования
async function getMyProfile() {
  const response = await apiRequest('http://localhost:8000/api/v0/me');
  return response.json();
}

async function getClients() {
  const response = await apiRequest('http://localhost:8000/api/v0/clients');
  return response.json();
}
```

## 4. React Hook пример

```typescript
// useAuth.ts
import { useState, useEffect } from 'react';

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = () => {
      const accessToken = localStorage.getItem('access_token');
      const expiresAt = Number(localStorage.getItem('token_expires_at') || 0);
      
      if (accessToken && Date.now() < expiresAt) {
        setIsAuthenticated(true);
      } else if (accessToken) {
        // Токен истек, пробуем обновить
        refreshAccessToken()
          .then(() => setIsAuthenticated(true))
          .catch(() => setIsAuthenticated(false));
      } else {
        setIsAuthenticated(false);
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const data = await login(email, password);
    setIsAuthenticated(true);
    return data;
  };

  const logout = async () => {
    const accessToken = localStorage.getItem('access_token');
    
    if (accessToken) {
      await fetch('http://localhost:8000/api/v0/auth/logout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
      });
    }

    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('token_expires_at');
    setIsAuthenticated(false);
  };

  return { isAuthenticated, loading, login, logout };
}
```

## 5. Полный пример компонента логина (React)

```typescript
// LoginPage.tsx
import { useState } from 'react';
import { useAuth } from './useAuth';

export function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await login(email, password);
      // Редирект на главную страницу
      window.location.href = '/';
    } catch (err) {
      setError('Неверный email или пароль');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Пароль"
        required
      />
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <button type="submit">Войти</button>
    </form>
  );
}
```

## Важные моменты:

1. **Access token живет 15 минут** - нужно обновлять автоматически
2. **Refresh token живет 7 дней** - храните его безопасно
3. **При 401 ошибке** - пробуйте обновить токен перед редиректом на логин
4. **При logout** - вызывайте `/api/v0/auth/logout` чтобы удалить refresh token из Redis
5. **Храните токены** в localStorage или httpOnly cookies (безопаснее)


