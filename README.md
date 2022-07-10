# Reputacion Digital

### Entrevista Backend

Un microservicio REST-API desarrollado en Flask, y publicado en Heroku.

https://pacific-hamlet-52301.herokuapp.com/

### API Reference

#### Cargar informacion

```http
POST /input/{my_target_field}
```

**my_target_field** puede ser cualquiera de los parametros string mencionados.

El request devuelve el nro id del registro agregado.

| Parameter          | Type     | Description  |
| :----------------- | :------- | :----------- |
| `field_1`          | `string` | **Required** |
| `author`           | `string` | **Required** |
| `description`      | `string` | **Required** |
| `my_numeric_field` | `number` | **Required** |

#### Buscar informacion

```http
  GET /get_data/{id}
```

| Parameter | Type     | Description                        |
| :-------- | :------- | :--------------------------------- |
| `id`      | `number` | **Required**. Id del item a buscar |

Si el id no se encuentra, devuelve una lista vacia.

### Docker

Tambien se encuentran los archivos `Dockerfile` y `docker-compose.yml` para ejecutar una version local, corriendo en containers.
