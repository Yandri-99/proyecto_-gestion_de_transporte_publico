# Transporte Público API

Proyecto universitario de una API REST para gestionar transporte público hecho con Django y DRF.

## Requisitos

- Python 3.12 o superior
- PostgreSQL (opcional, se puede usar SQLite para pruebas)
- uv (gestor de paquetes, como pip pero mas rapido)

## Como instalar y ejecutar

```bash
# 1. Clonar el repo
git clone <url-del-repo>
cd proyecto_-gestion_de_transporte_publico

# 2. Crear entorno virtual
uv venv

# 3. Activar el entorno
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate

# 4. Instalar dependencias
uv sync

# 5. Copiar el archivo de configuracion
cp .env.example .env
# Editar .env con tus datos si usas PostgreSQL

# 6. Migrar la base de datos
uv run python manage.py migrate

# 7. Crear superusuario (admin)
uv run python manage.py createsuperuser

# 8. Iniciar servidor
uv run python manage.py runserver
```

### Para usar PostgreSQL

En el `.env` poner:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=transporte
DB_USER=transporte
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
```

## Endpoints de la API

### Autenticación
| Metodo | Endpoint | Que hace | Token |
|--------|----------|----------|-------|
| POST | `/api/auth/register/` | Registrar usuario nuevo | No |
| POST | `/api/auth/login/` | Iniciar sesion y obtener JWT | No |
| POST | `/api/auth/token/refresh/` | Refrescar token | No |
| POST | `/api/auth/token/verify/` | Verificar si token es valido | No |
| POST | `/api/auth/logout/` | Cerrar sesion | Si |

### Usuarios (solo admin)
| Metodo | Endpoint | Que hace |
|--------|----------|----------|
| GET | `/api/users/` | Listar todos los usuarios |
| GET | `/api/users/{id}/` | Ver detalle de usuario |
| PATCH | `/api/users/{id}/` | Actualizar usuario |
| DELETE | `/api/users/{id}/` | Eliminar usuario |
| GET | `/api/users/profile/` | Ver mi perfil |
| PATCH | `/api/users/profile/` | Editar mi perfil |
| POST | `/api/users/change-password/` | Cambiar mi contraseña |

### Rutas
| Metodo | Endpoint | Que hace | Permiso |
|--------|----------|----------|---------|
| GET | `/api/routes/` | Listar rutas | Usuario normal |
| POST | `/api/routes/` | Crear ruta | Staff |
| GET | `/api/routes/{id}/` | Detalle de ruta | Usuario normal |
| PATCH | `/api/routes/{id}/` | Actualizar ruta | Staff |
| DELETE | `/api/routes/{id}/` | Eliminar ruta | Staff |
| GET | `/api/routes/{id}/trips/` | Viajes de esa ruta | Usuario normal |
| GET | `/api/routes/stats/` | Estadisticas | Usuario normal |

### Buses
| Metodo | Endpoint | Que hace | Permiso |
|--------|----------|----------|---------|
| GET | `/api/buses/` | Listar buses | Usuario normal |
| POST | `/api/buses/` | Crear bus | Staff |
| GET | `/api/buses/{id}/` | Detalle de bus | Usuario normal |
| PATCH | `/api/buses/{id}/` | Actualizar bus | Staff |
| DELETE | `/api/buses/{id}/` | Eliminar bus | Staff |
| GET | `/api/buses/available/` | Buses disponibles | Usuario normal |
| GET | `/api/buses/stats/` | Estadisticas | Usuario normal |

### Conductores
| Metodo | Endpoint | Que hace | Permiso |
|--------|----------|----------|---------|
| GET | `/api/drivers/` | Listar conductores | Usuario normal |
| POST | `/api/drivers/` | Crear conductor | Staff |
| GET | `/api/drivers/{id}/` | Detalle de conductor | Usuario normal |
| PATCH | `/api/drivers/{id}/` | Actualizar conductor | Staff |
| DELETE | `/api/drivers/{id}/` | Eliminar conductor | Staff |
| GET | `/api/drivers/available/` | Conductores disponibles | Usuario normal |
| GET | `/api/drivers/stats/` | Estadisticas | Usuario normal |

### Viajes
| Metodo | Endpoint | Que hace | Permiso |
|--------|----------|----------|---------|
| GET | `/api/trips/` | Listar viajes | Usuario normal |
| POST | `/api/trips/` | Crear viaje | Staff |
| GET | `/api/trips/{id}/` | Detalle de viaje | Usuario normal |
| PATCH | `/api/trips/{id}/` | Actualizar viaje | Staff |
| DELETE | `/api/trips/{id}/` | Eliminar viaje | Staff |
| POST | `/api/trips/{id}/start/` | Iniciar viaje | Admin |
| POST | `/api/trips/{id}/complete/` | Completar viaje | Admin |
| POST | `/api/trips/{id}/cancel/` | Cancelar viaje | Admin |
| GET | `/api/trips/schedule/` | Proximos viajes | Usuario normal |
| GET | `/api/trips/stats/` | Estadisticas | Admin |

### Tickets
| Metodo | Endpoint | Que hace | Permiso |
|--------|----------|----------|---------|
| GET | `/api/tickets/` | Listar tickets | Usuario normal (solo los suyos) |
| POST | `/api/tickets/` | Comprar ticket | Usuario normal |
| GET | `/api/tickets/{id}/` | Detalle de ticket | Usuario normal |
| PATCH | `/api/tickets/{id}/` | Actualizar ticket | Usuario normal |
| DELETE | `/api/tickets/{id}/` | Eliminar ticket | Usuario normal |
| POST | `/api/tickets/{id}/cancel/` | Cancelar ticket | Admin |
| GET | `/api/tickets/stats/` | Estadisticas | Admin |

### Paradas
| Metodo | Endpoint | Que hace | Permiso |
|--------|----------|----------|---------|
| GET | `/api/stops/` | Listar paradas | Usuario normal |
| POST | `/api/stops/` | Crear parada | Staff |
| GET | `/api/stops/{id}/` | Detalle de parada | Usuario normal |
| PATCH | `/api/stops/{id}/` | Actualizar parada | Staff |
| DELETE | `/api/stops/{id}/` | Eliminar parada | Staff |

### Health
| Metodo | Endpoint | Que hace |
|--------|----------|----------|
| GET | `/api/health/` | Verificar que el server funciona |

### Filtros y paginacion

En los endpoints de listar se puede usar:

- `?search=algo` — busca en los campos de texto
- `?is_active=true` — filtrar por campo especifico
- `?page=2&page_size=20` — paginacion (default 10, maximo 100)
- `?ordering=name` o `?ordering=-created_at` — ordenar

## Autenticacion

Usamos JWT (JSON Web Tokens). Primero hay que loguearse para obtener el token y luego mandarlo en el header.

### Ejemplos con curl

**1. Registrarse:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "juan", "email": "juan@mail.com", "password": "Pass1234!", "password2": "Pass1234!"}'
```

**2. Iniciar sesion:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "juan", "password": "Pass1234!"}'
```

Esto devuelve un access_token y un refresh_token.

**3. Usar el token para consultar:**
```bash
curl http://localhost:8000/api/routes/ \
  -H "Authorization: Bearer <el_access_token>"
```

**4. Crear un bus (solo staff):**
```bash
curl -X POST http://localhost:8000/api/buses/ \
  -H "Authorization: Bearer <token_de_staff>" \
  -H "Content-Type: application/json" \
  -d '{"plate": "PCC-1234", "brand": "Mercedes", "model": "Sprinter", "year": 2022, "capacity": 40}'
```

## Modelos (7 entidades)

1. **User** — Usuarios (viene con Django)
2. **Route** — Rutas de transporte (origen, destino, precio, etc)
3. **Bus** — Buses (placa, marca, capacidad, etc)
4. **Driver** — Conductores (ligados a un usuario)
5. **Trip** — Viajes programados (ruta + bus + conductor + horario)
6. **Ticket** — Boletos comprados por usuarios
7. **Stop** — Paradas intermedias en una ruta

## Despliegue

Esta desplegado en un DigitalOcean Droplet con CI/CD usando GitHub Actions:

- **URL**: `https://llumiquingatransporte.site/api/`
- **Health**: `https://llumiquingatransporte.site/api/health/`

Cuando se hace push a main, automaticamente se corren los tests y si todo bien se despliega.

## Tests

```bash
uv run python manage.py test transporte --verbosity=2
```

## Coleccion de Thunder Client

En el archivo `thunder-collection.json` estan todos los endpoints listos para importar en Thunder Client (extension de VS Code) o Postman.