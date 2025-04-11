# 🤖 RPA para Calificación Automatizada de Prácticas y Exámenes en Python

Este proyecto propone una solución de **Automatización Robótica de Procesos (RPA)** aplicada a la **calificación automática** de prácticas y exámenes en el curso de **Algoritmos y Estructuras de Datos en Python** 

Mediante el uso de **OCR, Flask, GPT-4** y **JPlag**, se automatiza todo el proceso de revisión de ejercicios de programación, permitiendo una evaluación rápida, objetiva y detallada, con detección de plagio incluida.

---

## 🎯 Objetivos

- ⚙️ Automatizar la calificación de ejercicios en Python con GPT-4 (API de OpenAI).
- 📄 Extraer texto de ejercicios en imagen usando **OCR (Tesseract)**.
- 📊 Proporcionar retroalimentación inmediata y detallada a los estudiantes.
- 🔍 Detectar plagio entre códigos usando **JPlag**.
- 🖥️ Permitir carga masiva de códigos y visualización organizada de notas por criterios.
- 🌐 Crear una interfaz web accesible para docentes y estudiantes con **Flask**.

---

## 🛠️ Tecnologías y Herramientas

| Herramienta       | Propósito                                     |
|-------------------|-----------------------------------------------|
| 🐍 Python         | Lenguaje principal del sistema                |
| 🧠 OpenAI API     | Evaluación de código y retroalimentación      |
| 📷 Tesseract OCR  | Reconocimiento de caracteres desde imágenes   |
| 🧰 Flask          | Backend web y lógica de negocio               |
| 🐘 MySQL          | Base de datos de usuarios, ejercicios y notas |
| 🧪 JPlag          | Detección de similitudes y plagio             |
| 🖼️ Pillow (PIL)   | Preprocesamiento de imágenes                  |

---

## 🧩 Arquitectura del Sistema

```text
        +---------------------+             +---------------------+
        |   Interfaz Web     | <---------> |     Backend Flask    |
        +---------------------+             +---------------------+
                |                                    |
     +--------------------+                +---------------------+
     | Archivos .py / img |  OCR/Tesseract |      GPT-4 (OpenAI) |
     +--------------------+                +---------------------+
                |                                    |
           +-----------+                      +------------------+
           |  MySQL DB | <------------------> |     JPlag        |
           +-----------+                      +------------------+
```

---

## 📋 Flujo de Trabajo

1. **Carga de evaluación** (docente sube imágenes o archivos `.py`)
2. **OCR extrae texto** de imágenes (si corresponde)
3. **GPT-4 evalúa código** según: *Correctitud*, *Eficiencia*, *Legibilidad*
4. **JPlag analiza similitudes** entre códigos
5. **Notas y retroalimentación** se registran y muestran en interfaz
6. **Docente accede a reportes por criterios y totales**

---

## 📈 Resultados Esperados

- 🕒 **Reducción del 80% del tiempo de calificación**
- 🎯 Evaluación **uniforme, objetiva y sin sesgos**
- 🔐 Mejora de la **integridad académica** al reducir el plagio
- 📚 Optimización del rol del docente para enfoque pedagógico

---

## 🚀 Futuras Mejores

- Soporte para más lenguajes de programación (C++, Java, JavaScript)
- Integración de reportes de análisis de desempeño por estudiante
- Personalización avanzada de criterios por curso
- Revisión manual asistida como opción secundaria



## 📚 Citas y Referencias

Incluye revisión de literatura sobre RPA en educación, industria y servicios. Para detalles, ver sección de referencias del [artículo completo](#).

---
