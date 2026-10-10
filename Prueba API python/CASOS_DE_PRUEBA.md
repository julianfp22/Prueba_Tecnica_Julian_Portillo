# Casos de prueba – API de usuarios (ReqRes)

**API:** https://reqres.in/api/
**Tipo de prueba:** funcional de API (caja negra), automatizada con Python + pytest + requests
**Datos de prueba:** `{"name": "Test User", "job": "Automation Engineer"}`

| ID | Tipo | Método y endpoint | Caso |
|---|---|---|---|
| API-01 | Requerido | POST /users | Crear usuario retorna 201 |
| API-02 | Adicional | POST /users | La respuesta refleja `name` y `job` e incluye `id` y `createdAt` |
| API-03 | Adicional | POST /users | Datos variados (acentos, caracteres especiales, texto largo) se reflejan sin alterarse |
| API-04 | Adicional | POST /users | Dos creaciones seguidas generan ids distintos |
| API-05 | Adicional | POST /users | La respuesta es JSON y llega en menos de 5 segundos |
| API-06 | Requerido | POST /users + GET /users/{id} | Flujo completo: crear, extraer el id y consultarlo |
| API-07 | Adicional | GET /users/2 | Usuario existente: 200 y estructura válida (JSON Schema) |
| API-08 | Adicional | GET /users/23 | Usuario inexistente: 404 |
| API-09 | Adicional | GET /users?page=2 | Listado paginado: 200, página 2 y datos presentes |
| API-10 | Adicional | PUT /users/2 | Actualizar usuario: 200, datos reflejados y `updatedAt` |
| API-11 | Adicional | DELETE /users/2 | Eliminar usuario: 204 sin contenido |

---

## API-01 Crear usuario retorna 201 (requerido)
**Precondición:** la API está disponible

**Pasos**
1. Enviar POST a `/users` con el cuerpo `{"name": "Test User", "job": "Automation Engineer"}`

**Resultado esperado**
- El código de estado HTTP es 201

---

## API-02 La respuesta del POST refleja los datos enviados
**Precondición:** la API está disponible

**Pasos**
1. Enviar POST a `/users` con los datos de prueba

**Resultado esperado**
- Código 201
- `name` es "Test User" y `job` es "Automation Engineer"
- La respuesta incluye un `id` no vacío
- La respuesta incluye `createdAt` con formato de fecha ISO 8601

---

## API-03 Datos variados se reflejan sin alterarse
**Precondición:** la API está disponible

**Pasos**
1. Enviar POST a `/users` con cada uno de estos pares: nombre con acentos y ñ, nombre con caracteres especiales, nombre muy largo (200 caracteres)

**Resultado esperado**
- Código 201 en todos los casos
- `name` y `job` de la respuesta son idénticos a lo enviado

---

## API-04 Dos creaciones generan ids distintos
**Precondición:** la API está disponible

**Pasos**
1. Enviar POST a `/users` con los datos de prueba
2. Enviar de nuevo el mismo POST

**Resultado esperado**
- Ambas respuestas son 201
- Los dos `id` son distintos

---

## API-05 Formato y tiempo de respuesta
**Precondición:** la API está disponible

**Pasos**
1. Enviar POST a `/users` con los datos de prueba

**Resultado esperado**
- La cabecera `Content-Type` contiene `application/json`
- La respuesta llega en menos de 5 segundos

---

## API-06 Flujo completo: crear y consultar el usuario (requerido)
**Precondición:** la API está disponible

**Pasos**
1. Enviar POST a `/users` con los datos de prueba
2. Extraer el `id` de la respuesta
3. Enviar GET a `/users/{id}` con ese id

**Resultado esperado**
- El POST responde 201
- El GET responde 200
- El `name` y el `job` del usuario consultado son los mismos que se enviaron en el POST

**Nota:** la documentación de ReqRes indica que `POST /users` es "echoed, not persisted" (se repite lo enviado, pero no se guarda). Por eso se espera que el GET del paso 3 responda 404. La prueba se marca como `xfail` para dejar el hallazgo documentado sin ocultarlo. Ver README.

---

## API-07 Consultar un usuario existente
**Precondición:** el usuario con id 2 existe en la API

**Pasos**
1. Enviar GET a `/users/2`

**Resultado esperado**
- Código 200
- `data.id` es 2
- La estructura cumple el esquema: `data` con `id` (entero), `email`, `first_name` y `last_name` (texto)

---

## API-08 Consultar un usuario inexistente
**Precondición:** el usuario con id 23 no existe

**Pasos**
1. Enviar GET a `/users/23`

**Resultado esperado**
- Código 404

---

## API-09 Listado paginado
**Precondición:** la API está disponible

**Pasos**
1. Enviar GET a `/users?page=2`

**Resultado esperado**
- Código 200
- `page` es 2
- `data` es una lista con al menos un usuario

---

## API-10 Actualizar un usuario
**Precondición:** el usuario con id 2 existe

**Pasos**
1. Enviar PUT a `/users/2` con `{"name": "Test User", "job": "QA Lead"}`

**Resultado esperado**
- Código 200
- `name` y `job` reflejan lo enviado
- La respuesta incluye `updatedAt`

---

## API-11 Eliminar un usuario
**Precondición:** el usuario con id 2 existe

**Pasos**
1. Enviar DELETE a `/users/2`

**Resultado esperado**
- Código 204
- El cuerpo de la respuesta está vacío
