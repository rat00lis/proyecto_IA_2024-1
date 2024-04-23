# Proyecto IA 2024-1
Proyecto de IA 2048
Integrantes:
- Bruno Arce R.
- Oliver Brito A.
- Emilio Ramos M.
- Luis Valenzuela C.

## Una breve descripción del problema que abordarán.
El proyecto consiste en la resolución del juego 2048 mediante el uso de inteligencia artificial.
Particularmente se considerará la implementación de un modelo (o varios) de aprendizaje por refuerzo.

## Variables?
- Descripción del ambiente: El ambiente de juego es discreto, estático y estocástico.
- Representación concreta del estado del juego, representada por una estructura de datos: Para cada jugada se conoce el estado de la matriz que compone al juego 2048, teniendo acceso a todos los valores y posiciones de las "fichas".
- Descripción de las acciones que puede tomar el agente: Acciones discretas, en cada jugada el agente puede decidir en qué dirección empujar todas las fichas (siendo estas direcciones: arriba, abajo, izquierda, derecha). Estos movimientos están restringidos a la existencia de un posible movimiento en esa dirección, es decir, si no existe ninguna ficha que es pueda mover hacia arriba, ese movimiento está bloqueado.
- Representación concreta de las acciones: Al ser acciones discretas, los posibles valores que estas pueden tomar son: arriba, abajo, izquierda, derecha. Estas pueden representarse ya sea por un número o un caracter.

## Recompensa
Para cada movimiento, el agente calculará la recompensa de ese movimiento y el siguiente que realizará. La recompensa está compuesta por el valor de todas las celdas que han sido fusionadas en ese movimiento.

## Penalización
- A cada recompensa, se le restará su penalización, que consiste en la suma de todas las celdas que se han movido en esa jugada.
- Adicionalmente, se sumará una penalización si el agente intenta hacer un movimiento ilegal o que no produzca ningún resultado.
