# TENIS 2D  

## Documento de Diseño de Juego (GDD)

**Integrantes**: Mauro Bermudez

**Correo electrónico**: [bcantomauro@gmail.com](mailto:bcantomauro@gmail.com)

**Versión**: 2.0 (final para la entrega)

**Fecha**: 12/11/2015

1. ## Resumen Ejecutivo 

* **Título del Juego**: ARKANOID TENIS.

* **Género**: Deportes / Arcade Competitivo

* **Plataforma** **Objetivo**: PC (Windows 10, Pygame)

* **Público Objetivo**: Jugadores casuales, fans del tenis y de los juegos retro y arcade, edad 10+

* **Propuesta Única de Venta (USP)**: Un juego de tenis rápido y competitivo estilo arkanoid, con estética isométrica, controles simples y acción inmediata, ideal para partidas cortas uno contra uno o contra la IA.

2. ## Concepto del Juego 

   1. ### Visión General

   ARKNAOID TENIS es un juego deportivo de perspectiva isométrica donde dos jugadores (jugador vs jugador o jugador vs IA) se enfrentan en un partido de tenis tipo arcade.

   El objetivo es golpear la pelota de forma precisa y anotar puntos cuando el oponente no logra devolverla. El enfoque es la velocidad, reflejos y precisión, sin reglas realistas, sino diversión inmediata.

   2. ### Pilares de Diseño 

* **Pilar 1 – Jugabilidad rápida y fluida:** partidas cortas y fluidas.

* **Pilar 2 – Controles intuitivos:** cualquiera puede aprender a jugar en segundos.

* **Pilar 3 – Competencia local o contra IA:** desafíos accesibles pero intensos.

* **Pilar 4 – Estilo retro moderno:** mezcla de pixel art y vista isométrica para sensación arcade.

  3. ### Inspiraciones y Referencias 

* Pong (Atari, 1972\)* – Simplicidad y adicción.

* Virtua Tennis (SEGA, 2000\)* – Dinamismo en los intercambios.

* Arknaoid (Taito, 1986).

* Juegos de *arcade deportivos 2D* de los años 90\.

3. ## Mecánicas de Juego (Gameplay) 

   1. ### Bucle de Jugabilidad Principal (Core Gameplay Loop) 

1. **Movimiento:** el jugador se desplaza por su lado de la cancha.

2. **Golpe:** cuando la pelota se acerca, el jugador debe impactar con ella para devolver el golpe.

3. **Respuesta:** el oponente intenta devolverla.

4. **Punto:** si la pelota pasa los límites del campo o el rival no llega, se otorga un punto.

5. **Recompensa:** el jugador avanza hacia la victoria hasta alcanzar el puntaje objetivo (7 por defecto).

   2. ### Mecánicas Detalladas        **Movimiento del Jugador:**

* Movimiento en plano 2D con proyección isométrica.

* P1: teclas WASD, P2: Flechas.

* IA usa movimiento automático siguiendo la pelota.

  **Sistema de “Golpeo”:**  
* El jugador golpea automáticamente cuando la pelota colisiona con su zona de impacto (rectángulo).

* Rebotes en los bordes laterales.

* Si la pelota sale por el fondo contrario, el jugador anota.

  **Sistema de Progresión:**  
* Sin progresión por niveles; el progreso se mide por puntaje dentro del partido.  
  Posibilidad futura: ranking local o marcador histórico.  
  

    
  **Mecánicas Únicas:**  
* Perspectiva isométrica: convierte un plano 2D simple en una cancha con profundidad visual.

* IA dinámica: el oponente controla su posición según la trayectoria de la pelota.

* Auto-reset tras punto: jugadores y pelota se reubican automáticamente.

  3. ### Controles 

| Acción           | Teclado (P1)          | Teclado (P2)          | Joystick (Futuro)     | Táctil (Futuro)       |
|:-----------------|:----------------------|:----------------------|:----------------------|:----------------------|
| Moverse          | W, A, S, D            | Flechas               | Análogo Izquierdo     | Joystick en pantalla  |
| Golpear          | Automático (colisión) | Automático (colisión) | Automático (colisión) | Automático (colisión) |
| Menú             | ESC                   | ESC                   | Start                 | Botón Menú            |
| Seleccionar menú | ENTER                 | ENTER                 | X                     | Touch al menú         |


4. ## Mundo y Narrativa 

   1. ## Historia y Argumento 

El juego no posee narrativa tradicional; su enfoque es puramente competitivo y arcade.

El “mundo” se limita a la cancha, representando la esencia del deporte: reflejos, precisión y adrenalina.

### Personajes 

**Jugador 1 (P1):**

* **Rol:** protagonista (controlado por humano).

* **Descripción:** deportista casual.

* **Habilidades:** velocidad y control manual.

**Jugador 2 (P2 / IA):**

* **Rol:** oponente (jugador o IA).

* **Descripción:** rival con inteligencia básica.

* **Habilidades:** sigue la posición de la pelota para anticipar golpes.

  ### Entorno y Niveles

    
  **Cancha Principal:**

* **Descripción Visual:** fondo verde con líneas blancas, red amarilla para mejor distinción. A los laterales la tribuna con espectadores.
Estilo pixel art.

* **Objetivos:** anotar puntos hasta alcanzar el puntaje objetivo (7 por defecto).

* **Desafíos:** rebotes rápidos, reflejos, dificultad de la IA.

3. ## Arte y Sonido 

   ### Dirección de Arte

* **Estilo:** Prototipo isométrico con jugadores realizados en pixel art; la pelota usa una imagen de color solido para poder distinguirse en la cancha.
* **Jugadores:** Sprites creados manualmente dentro del sitio web https://www.pixilart.com/ , tomando como referencia una imagen generada por IA, dos/tres frames de movimiento + uno de swing.

* **Paleta de Colores:**

  * Verde/amarillo para la cancha (tranquilidad y enfoque).

  * Blanco para líneas y pelota (claridad).

  * Ropa de jugadores con contrastes para legibilidad (azul para el jugador 1, y rojo para el jugador 2).

* **Inspiración Visual:** *Neo Geo Pocket Tennis*, *Super Tennis (SNES)*, *Mini Tennis Mobile*.

  ### Diseño de Sonido y Música


**Efectos de Sonido:**


* Sonido de navegación en el menú.
* Golpe a la pelota.
* Festejos del público al llegar al fin de cada partido.
* Sonido ambiente de estadio durante el partido.


4. ## Interfaz de Usuario (UI) y Experiencia de Usuario (UX) 

   ### Flujo de Pantallas

**Pantalla de Título → Menú Principal → Selección de Modo (1P/2P) → Juego → Resultado → Menú Principal**

### HUD (Heads-Up Display)  


**Marcador superior:** puntos de cada jugador.

Indicador de quien hizo el tanto.

**Texto “GANA EL JUGADOR (JUGADOR1 / JUGADOR2)” al finalizar el partido.**

	  
	

### Menús

**Menú Principal:** Jugar: 1 JUGADOR (VS IA), 2 JUGADORES, Salir.

**Menú Pausa:** Opcion "Reanudar", para poder retomar el juego en cualquier momento. Volver al menu principal y Salir del Juego.




### Modelo de Monetización

**Gratis (Freeware / Proyecto académico).**

**Futuro opcional:**

Versión comercial con skins y multijugador online. 

Agregar publicidad en las tribunas.

5. ## Fuentes de los Assets

Esta sección es crucial para llevar un control de los recursos utilizados, sus licencias y atribuciones.

| Nombre del Asset    | Descripción del Asset                                                            | Tipo   | Origen/Fuente (URL)                                                                                         | Licencia           | Costo    |  
|:--------------------|:---------------------------------------------------------------------------------|:-------|:------------------------------------------------------------------------------------------------------------|:-------------------|:---------|
| Festejo             | Sonido de festejo que se reproduce al llegar a 7 puntos                          | Audio  | https://pixabay.com/sound-effects/search/stadium/ "Crowd cheering"                                          | CC0                | Gratuito |  
| Golpe               | Sonido al golpear la pelota                                                      | Audio  | https://freesound.org/people/InspectorJ/sounds/411641/                                                      | CC0                | Gratuito   |  
| Ambiente            | Sonido ambiente durante el partido                                               | Audio  | https://pixabay.com/sound-effects/search/stadium/ "Soccer Stadium 10"                                       | CC0                | Gratuito   |  
| Jugadores y tribuna | Sprites propios (blue/red con 3 frames cada uno), y crowd/crowd2 para la tribuna | PNG    | Producción propia                                                                                           | —                  | —        |
| Ball                | Imagen de color solido para la pelota.                                           | PNG    | Producción propia                                                                                           | —                  | —        |
| Menu                | Sonido al desplazarse y/o ejecutar una acción del menú                           |        | https://pixabay.com/sound-effects/search/game%20menu/ "Menu Selection"                                      | CC0                | Gratuito   |
| Logo                | Logo para la ventana del juego                                                   | PNG    | Producción propia                                                                                           | -                  | -        |
| Fireworks           | Fuegos artificiales distribuidos por la pantalla para el fin de cada partido.    | PNG    | https://opengameart.org/content/fireworks                                                                   | CC0                | Gratuito   |
| Press Start 2P      | Fuente para todo el juego                                                        | Fuente | https://fonts.google.com/specimen/Press+Start+2P                                                            | Open Font License  | Gratuito   |

—

6. ## Control de Cambios

Este registro es vital para documentar cómo evoluciona el documento y las decisiones clave del proyecto.

| Versión   | Descripción del Cambio                                                      |  
|:----------|:----------------------------------------------------------------------------|
| 1.0.0     | Creación inicial del documento.                                             |  
| 1.0.1     | Implementación de la cancha, assets básicos para los jugadores y la pelota. |  
| 1.0.2     | Implementación de colisiones y físicas de rebote de la pelota.              |
| 1.1.0     | Implementación del movimiento de la IA.                                     |
| 1.2       | Ajustes al documento y creación del menú principal.                         |
| 1.2.1     | Implementación de sonidos para todas las pantallas.                         |
| 1.2.2     | Ajustar mecánicas de juego: físicas de rebote, movimiento de la IA.         |
| 1.3       | Creación de los spritesheets para los jugadores y tribuna.                  |
| 2.0 FINAL | Ajustes en detalles visuales.                                               |

