# Casos de prueba – Smoke Test de Inicio de Sesión (SauceDemo)

**Aplicación:** https://www.saucedemo.com/
**Módulo:** Inicio de sesión
**Tipo de prueba:** Smoke test (validación rápida de que el flujo crítico funciona)
**Datos de prueba:** usuarios públicos que la propia aplicación muestra en su pantalla de login

| ID | Escenario del alcance | Caso |
|---|---|---|
| SMK-01 | 1. Login exitoso con credenciales válidas | Login exitoso con usuario y contraseña válidos |
| SMK-02 | 2. Login fallido con contraseña incorrecta | Login con contraseña incorrecta |
| SMK-03 | 3. Validación de campos obligatorios | Login sin usuario |
| SMK-04 | 3. Validación de campos obligatorios | Login sin contraseña |
| SMK-05 | 3. Validación de campos obligatorios | Login con ambos campos vacíos |

---

## SMK-01 Login exitoso con credenciales válidas
**Precondición:** el usuario `standard_user` existe y no está bloqueado

**Pasos**
1. Abrir https://www.saucedemo.com/
2. Escribir usuario `standard_user`
3. Escribir contraseña `secret_sauce`
4. Clic en "Login"

**Resultado esperado**
- El sistema redirige a la página de productos (la URL contiene `/inventory.html`)
- Se muestra el título "Products"
- Se muestra la lista de productos

---

## SMK-02 Login fallido con contraseña incorrecta
**Precondición:** el usuario `standard_user` existe

**Pasos**
1. Abrir https://www.saucedemo.com/
2. Escribir usuario `standard_user`
3. Escribir contraseña `clave_incorrecta`
4. Clic en "Login"

**Resultado esperado**
- El usuario permanece en la página de login
- Se muestra el mensaje: `Epic sadface: Username and password do not match any user in this service`

---

## SMK-03 Validación de campo obligatorio: usuario vacío
**Precondición:** ninguna

**Pasos**
1. Abrir https://www.saucedemo.com/
2. Dejar el usuario vacío
3. Escribir contraseña `secret_sauce`
4. Clic en "Login"

**Resultado esperado**
- El usuario permanece en la página de login
- Se muestra el mensaje: `Epic sadface: Username is required`

---

## SMK-04 Validación de campo obligatorio: contraseña vacía
**Precondición:** ninguna

**Pasos**
1. Abrir https://www.saucedemo.com/
2. Escribir usuario `standard_user`
3. Dejar la contraseña vacía
4. Clic en "Login"

**Resultado esperado**
- El usuario permanece en la página de login
- Se muestra el mensaje: `Epic sadface: Password is required`

---

## SMK-05 Validación de campos obligatorios: ambos vacíos
**Precondición:** ninguna

**Pasos**
1. Abrir https://www.saucedemo.com/
2. Dejar usuario y contraseña vacíos
3. Clic en "Login"

**Resultado esperado**
- El usuario permanece en la página de login
- Se muestra el mensaje: `Epic sadface: Username is required` (la aplicación valida primero el usuario)
