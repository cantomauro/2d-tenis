# TENIS 2D  

## Documento de Diseño de Juego (GDD)

**Integrantes**: Mauro Bermudez

**Correo electrónico**: [bcantomauro@gmail.com](mailto:bcantomauro@gmail.com)

**Versión**: 1.0.0

**Fecha**: 2025-10-15

1. ## Resumen Ejecutivo 

* **Título del Juego**: Tenis 2D

* **Género**: Deportes / Arcade Competitivo

* **Plataforma** **Objetivo**: PC (Windows 10, Pygame)

* **Público Objetivo**: Jugadores casuales, fans de los juegos retro y arcade, edad 10+

* **Propuesta Única de Venta (USP)**: Un juego de tenis rápido y competitivo con estética isométrica, controles simples y acción inmediata, ideal para partidas cortas uno contra uno o contra la IA.

2. ## Concepto del Juego 

   1. ### Visión General

   Tenis 2D es un juego deportivo de perspectiva isométrica donde dos jugadores (jugador vs jugador o jugador vs IA) se enfrentan en un partido de tenis tipo arcade.

   El objetivo es golpear la pelota de forma precisa y anotar puntos cuando el oponente no logra devolverla. El enfoque es la velocidad, reflejos y precisión, sin reglas realistas, sino diversión inmediata.

   2. ### Pilares de Diseño 

* **Pilar 1 – Jugabilidad rápida y fluida:** partidas cortas, sin tiempos muertos.

* **Pilar 2 – Controles intuitivos:** cualquiera puede aprender a jugar en segundos.

* **Pilar 3 – Competencia local o contra IA:** desafíos accesibles pero intensos.

* **Pilar 4 – Estilo retro moderno:** mezcla de pixel art y vista isométrica para sensación arcade.

  3. ### Inspiraciones y Referencias 

* *Pong (Atari, 1972\)* – Simplicidad y adicción.

* *Virtua Tennis (SEGA, 2000\)* – Dinamismo en los intercambios.

* *Tennis Clash (Wildlife)* – Velocidad y presentación visual limpia.

* Juegos de *arcade deportivos 2D* de los años 90\.

3. ## Mecánicas de Juego (Gameplay) 

   1. ### Bucle de Jugabilidad Principal (Core Gameplay Loop) 

1. **Movimiento:** el jugador se desplaza por su lado de la cancha.

2. **Golpe:** cuando la pelota se acerca, puede golpearla para enviarla al otro lado.

3. **Respuesta:** el oponente intenta devolverla.

4. **Punto:** si la pelota pasa los límites del campo o el rival no llega, se otorga un punto.

5. **Recompensa:** el jugador avanza hacia la victoria hasta alcanzar el puntaje objetivo (7 por defecto).

   2. ### Mecánicas Detalladas        **Movimiento del Jugador:**

* Movimiento en plano 2D con proyección isométrica.

* P1: teclas WASD, P2: Flechas.

* IA usa movimiento automático siguiendo la pelota.

  **Sistema de “Golpeo”:**  
* El jugador golpea automáticamente cuando la pelota colisiona con su zona de impacto (rectángulo).

* Rebotes realistas en los bordes laterales.

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

* **Descripción Visual:** fondo verde azulado con líneas blancas, y red amarilla para mejor distinción. 
Estilo pixel art.

* **Objetivos:** anotar puntos hasta alcanzar el puntaje objetivo (7 por defecto).

* **Desafíos:** rebotes rápidos, reflejos, dificultad de la IA.

3. ## Arte y Sonido 

   ### Dirección de Arte

* **Estilo:** Prototipo isométrico con placeholders simples (rectángulos coloreados) para los jugadores; la pelota utiliza la animación del paquete Kenney Sports Pack para dar contraste visual.
* **Jugadores:** cuerpos base con overlays de pierna y mano tomados del Kenney Sports Pack (variantes Blue y Red) para simular movimiento sin invertir en una hoja completa.

* **Paleta de Colores:**

  * Verde/amarillo para la cancha (tranquilidad y enfoque).

  * Blanco para líneas y pelota (claridad).

  * Ropa de jugadores con contrastes para legibilidad (azul para el jugador 1, y rojo para el jugador 2).

* **Inspiración Visual:** *Neo Geo Pocket Tennis*, *Super Tennis (SNES)*, *Mini Tennis Mobile*.

  ### Diseño de Sonido y Música

**Música:** base electrónica ligera tipo “chiptune”, loops cortos y enérgicos.

**Efectos de Sonido:**

* Golpe a la pelota.
* Musica relajante tipo retro en el menu principal.

* Festejos del estadio al llegar a los 7 puntos.

* Sonido ambiente de estadio durante el partido.


4. ## Interfaz de Usuario (UI) y Experiencia de Usuario (UX) 

   ### Flujo de Pantallas

**Pantalla de Título → Menú Principal → Selección de Modo (1P/2P) → Juego → Resultado → Menú Principal**

### HUD (Heads-Up Display)  

ADJUNTAR CAPTURAS DE PANTALLA.

**Marcador superior:** puntos de cada jugador.

Indicador de quien hizo el tanto.

**Indicador de velocidad de pelota.**

**Texto “Match Point” / “Game Over”.**

	  
	

### Menús

**Menú Principal:** Jugar, Controles (guía, no se pueden configurar), Salir.

**Menú Pausa:** Reanudar, Reiniciar, Salir.

5. ## Plan de Producción y Monetización 

   ### Hoja de Ruta (Roadmap)

   

Define los hitos principales del desarrollo.  
\* \*\*Prototipo:\*\* \[Fecha\] \- Funcionalidades básicas jugables.  
\* \*\*Vertical Slice:\*\* \[Fecha\] \- Una porción pulida del juego que representa la experiencia final.  
\* \*\*Alfa:\*\* \[Fecha\] \- El juego está completo en cuanto a características, pero necesita pulido y corrección de errores.  
\* \*\*Beta:\*\* \[Fecha\] \- El juego está casi terminado, abierto a pruebas masivas.  
\* \*\*Lanzamiento:\*\* \[Fecha\]

### Modelo de Monetización

**Gratis (Freeware / Proyecto académico).**

Futuro opcional: versión comercial con skins y multijugador online. Publicidad ?

6. ## Fuentes de los Assets

Esta sección es crucial para llevar un control de los recursos utilizados, sus licencias y atribuciones.

| Nombre del Asset                  | Descripción del Asset                                   | Tipo        | Origen/Fuente (URL)                                                   | Licencia          | Costo  |  
|:----------------------------------|:--------------------------------------------------------|:------------|:----------------------------------------------------------------------|:------------------|:-------|
| Festejo                           | Sonido de festejo que se reproduce al llegar a 7 puntos | Audio       | https://pixabay.com/sound-effects/search/stadium/ "Crowd cheering"    | CC0               | Gratis |  
| Golpe                             | Sonido al golpear la pelota                             | Audio       | https://freesound.org/people/InspectorJ/sounds/411641/                | CC0               | Gratis |  
| Ambiente                          | Sonido ambiente durante el partido                      | Audio       | https://pixabay.com/sound-effects/search/stadium/ "Soccer Stadium 10" | CC0               | Gratis |  
| Jugadores y overlays              | Cuerpos base + overlays (piernas/ manos) del Kenney Sports Pack | PNG         | Kenney Sports Pack / `others/spritesheets.zip` | CC0 | Gratis |
| Pelota de tenis                   | Animación de dos frames (Kenney Sports Pack, PNG)       | PNG         | Kenney Sports Pack / `others/spritesheets.zip` | CC0               | Gratis |
| Press Start 2P                    | Fuente para todo el juego                               | Fuente      | https://fonts.google.com/specimen/Press+Start+2P                      | Open Font License | Gratis |

—

7. ## Control de Cambios

Este registro es vital para documentar cómo evoluciona el documento y las decisiones clave del proyecto.

| Versión | Fecha | Autor del Cambio | Descripción del Cambio | Razón del Cambio |  
| :--- | :--- | :--- | :--- | :--- |  
| 1.0.0 | 2025-09-17 | \[Tu Nombre\] | Creación inicial del documento. | Inicio del proyecto. |  
| 1.0.1 | 2025-09-24 | \[Nombre del Artista\] | Se actualizó la sección 5.1 con un nuevo moodboard. | Se definió mejor el estilo visual. |  
| 1.1.0 | 2025-10-05 | \[Tu Nombre\] | Se eliminó la mecánica de "sed" de la sección 3.2. | Tras el playtesting, resultaba tediosa y no aportaba diversión. |

