# Recicla Fácil

## Descripción General

*Recicla Fácil* es una plataforma web que facilita el reciclaje al conectar a los usuarios con puntos de reciclaje cercanos y les permite medir el impacto ambiental de sus esfuerzos. Con una interfaz intuitiva y herramientas educativas, el objetivo es promover un estilo de vida más sostenible al hacer del reciclaje un hábito accesible y motivador.

## Problema que resuelve

La falta de información sobre puntos de reciclaje y el desconocimiento del impacto positivo del reciclaje desalientan su práctica. *Recicla Fácil* aborda esto proporcionando datos claros y visualizando los beneficios ambientales.

## Características clave

1. **Mapa de reciclaje:**
   - Usa la API de Google Maps para mostrar puntos de reciclaje cercanos, indicando qué materiales acepta cada lugar (plástico, vidrio, papel, etc.).
   - Los usuarios pueden sugerir nuevos puntos de reciclaje para mejorar la base de datos.

2. **Registro de actividades:**
   - Interfaz sencilla para registrar manualmente lo reciclado (e.g., "5 botellas de plástico", "2 kg de papel").
   - Historial personal para rastrear los avances individuales.

3. **Calculadora de impacto:**
   - Traduce las actividades registradas a métricas de impacto ambiental, como el ahorro estimado de CO₂ y energía.
   - Visualización del impacto acumulado a lo largo del tiempo mediante gráficos sencillos.

4. **Educación y consejos:**
   - Consejos prácticos sobre reciclaje y reducción de residuos.
   - Información sobre los efectos positivos del reciclaje en el cambio climático.

## Beneficio social

Empodera a los usuarios con información y herramientas para reciclar de manera efectiva, creando un impacto positivo en su comunidad y ayudando a reducir emisiones de gases de efecto invernadero.

---

## Plan de Proyecto

### 1. Preparación del Proyecto
- Crear un entorno virtual y preparar el repositorio en Git.
- Instalar Flask y bibliotecas necesarias:
  ```bash
  pip install flask flask_sqlalchemy flask_wtf
  ```
- Crear la estructura básica del proyecto:
  ```
  /project
    ├── static/         # Archivos CSS/JS
    ├── templates/      # Archivos HTML
    ├── app.py          # Archivo principal
    ├── models.py       # Modelos para la base de datos
    ├── forms.py        # Formularios con Flask-WTF
    └── config.py       # Configuración de la app
  ```

### 2. Funcionalidades Principales
1. **Registro de Usuarios**  
   - Formulario de registro y autenticación.
   - Base de datos para almacenar usuarios.

2. **Registro de Actividades**
   - Formulario para que los usuarios ingresen actividades como:
     - Cantidad de plástico reciclado.
     - Distancia recorrida caminando o en bicicleta.
   - Almacenar los datos en una base de datos.

3. **Visualización de Impacto**
   - Página de usuario con gráficos (usando `matplotlib` o `chart.js`) que muestren el impacto acumulado:
     - CO₂ ahorrado.
     - Comparativa con promedios globales.

4. **Educación y Consejos**
   - Mostrar mensajes personalizados con base en las actividades registradas:
     - "¡Has ahorrado suficiente CO₂ para cargar un teléfono 100 veces!"
     - Consejos para mejorar el impacto.

### 3. Diseño UI/UX
- Crear una plantilla base con **Bootstrap** para diseño responsivo.
- Páginas clave:
  - **Inicio:** Explicación de la plataforma y motivación para registrarse.
  - **Perfil:** Panel personalizado con gráficos y registro de actividades.
  - **Mapa:** Integración con Google Maps para encontrar puntos de reciclaje.

### 4. Iteraciones Avanzadas
- Añadir **gamificación**: Ranking global de usuarios basado en puntos por actividades sostenibles.
- Integrar un API público para obtener datos climáticos y comparativas.
- Optimizar el sitio web para SEO y accesibilidad.
