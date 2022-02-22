APIAstro --- estudiando transitos exoplanetarios en la web
---------------------------------------------

**Autor: Roy Van der Westhuizen (royvdw@uc.cl)**

**Colaboradores**: Juan Pablo Sepúlveda.

**Advisors**: Andres Jordan (andres.jordan@uai.cl); Nestor Espinoza (nespinoza@stsci.edu).

# Introduccion
--------------

APIAstro es una aplicacion que permite ajustar transitos exoplanetarios "a mano", moviendo cursores para entender 
como las propiedades de un planeta impactan la curva de luz observada. Esta aplicacion fue desarrollada por 
Roy Van der Westhuizen, en lo que fue su tesis de licenciatura. El estudio de su tesis se encuentra en este mismo 
repositorio (`Tesis.pdf`).

Este repositorio fue subido por Nestor Espinoza a peticion de Roy Van der Westhuizen.

# Dependencias
-----------------

Para usar APIAstro, es necesario instalar las siguientes dependencias:

    numpy
    flask
    werkzeug
    batman-package

# Usando APIAstro
-----------------

Usar APIAstro es simple. Simplemente se debe ejecutar el script `astro.py` dentro de `web/astro` (e.g., `python astro.py`); eso lanzara una aplicacion que se 
puede visualizar en http://127.0.0.1:5000/.

Desde ahi, se puede subir una curva de luz en "Paso 1" --- una curva de ejemplo se encuentra en `web/astro/DATOS.dat`. El formato de cualquier otra curva de luz 
que se quiera ocupar debe seguir el mismo formato de ese archivo. Luego, se sube la curva haciendo click en "Paso 2" --- y listo! 

# Creditos
----------

Todos los creditos de uso de APIAstro deben ir a Roy Van der Westhuizen (royvdw@uc.cl). Si se quiere citar en un texto academico, la referencia sugerida es:

    Van der Westhuizen, R. (2015). Taller de Exoplanetas. Propuesta de un laboratorio virtual interactivo: APIastro [Tesis de Licenciatura, Pontificia Universidad Catolica de Chile]

O, en ingles:

    Van der Westhuizen, R. (2015). Taller de Exoplanetas. Propuesta de un laboratorio virtual interactivo: APIastro [Undergraduate thesis, Pontificia Universidad Catolica de Chile]

