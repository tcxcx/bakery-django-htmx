Bakery App
==========

Se requiere crear una aplicación interna para una pastelería. Por esta razón es importante **desactivar** la opción de **SignUp** ya que los usuarios van 
a ser administrados directamente por el administrador del sistema. 

El objetivo de la aplicación es manejar las recetas de la pastelería y calcular el costo de producción de cada producto.

Estructura del Sistema
-----------------------

El sistema se puede dividir en dos secciones: 

- **Administración**: sección donde se ingresa la información de los Proveedor, Insumos y Productos. 
- **Margen de Ganancia**: sección donde se muestra el costo de producción de un Producto y su margen de ganancia. 

Administración
---------------

- Se debe almacenar el ``nombre``, ``ruc``, ``correo``, ``teléfono`` y ``dirección`` de los ``Proveedores``. 
- Un ``Proveedor`` puede proveer de uno o muchos ``Insumos``. 
    
    - Para simplificar el modelo, se va a considerar que un ``Insumo`` solo puede ser provisto por un ``Proveedor``. 

- Se debe almacenar el ``nombre`` y el ``precio`` de los ``Insumos``. 

    - Para simplificar el modelo se va considerar que todos los precios son ingresados en **[$/g]**, 
      incluso los líquidos. Por ejemplo, el insumo leche entera tiene un costo de $0.05 por gramo. 

- Para administrar los ``Productos`` se debe ingresar su ``nombre``, ``tipo de producto``, ``precio de venta``, ``forma`` y ``dimensiones``. 
  El producto es el producto final que vende la pastelería. 

    - El ``tipo de producto`` se administra con otro modelo. El ``Producto`` puede tener solo un ``Tipo De Producto`` (i.e: torta de celebración, cheesecake, etc.) 
    - La forma solo tiene dos posibles opciones: **Circular** y **Rectangular**. 
    - En caso de tener forma **Circular** las dimensiones que se deben almacenar son: ``diámetro`` y ``alto``  
    - En caso de tener forma **Rectangular** las dimensiones son: ``largo` , ``ancho`` y ``alto``. 
    - Las dimensiones siempre se ingresan en **[cm]** 

- El ``Tipo de Producto`` solo tiene ``nombre``. Un tipo de producto puede tener muchos productos. 
- Un ``Producto`` puede tener una o muchas ``Preparaciones``, y una ``Preparación`` solo puede tener un ``Producto``. 
  Las preparaciones guardan información de las partes individuales que componen un producto. Por ejemplo, 
  un Carrot Cake está compuesto de: Bizcocho, Frosting, Zanahorias Caramelizadas. 
- Una ``Preparación`` utiliza uno o muchos Insumos. Por ejemplo, el Bizcocho usa: mantequilla, harina, azúcar, nueces, etc. 
  Pero a su vez un ``Insumo`` puede ser utilizado por una o muchas ``Preparaciones``. 
- Es importante almacenar la ``cantidad`` de cada insumo que se utiliza en una preparación. 
  Por ejemplo: En el Bizcocho del Carrot Cake se utilizan 10g de azúcar, 150g de harina, 50g de leche, 10g de agua, etc. 

    - La cantidad siempre se ingresa en [g] 

Margen de Ganancia
-------------------

- Se debe construir una interfaz (Dashboard) donde se muestre una tabla con la siguiente información: 
  - Producto 
  - Forma 
  - Dimensiones  
  - Costo Total 
  - Precio de Venta 
  - Margen (en %) 
- El Margen se obtiene con la fórmula: ``(precio_venta - costo_total) / precio_venta * 100``

Consideraciones Generales
--------------------------

- Todas las tablas deben tener filtros relevantes 
- Por motivos de auditoría todos los modelos deben almacenar: ``created_by``, ``created_at``, ``updated_by``, ``updated_at``. 

Consideraciones de Tecnología
------------------------------

Los siguientes paquetes ya están instalados en el proyecto: 

- `django-tables2 <https://github.com/jieter/django-tables2>`_
- `django-filter <https://github.com/carltongibson/django-filter>`_
- `django-htmx <https://github.com/adamchainz/django-htmx>`_
- `django-author <https://github.com/lambdalisue/django-author>`_
- `django-bootstrap-datepicker-plus <https://github.com/monim67/django-bootstrap-datepicker-plus>`_
- `htmx <https://htmx.org/>`_ (Instalado en package.json y bundled con Gulp)

Si se requieren paquetes adicionales, puedes instalarlos sin ninguna restricción. 

La solución implementada debe cumplir los siguientes puntos: 

- Para hacer la UI más dinámica se utiliza el framework ``htmx``. 

    - Se debe utilizar ``htmx`` para filtrar las tablas sin hacer un full page reload. 
    - En las tablas cuando se ordena por una columna y el pagination debe ser manejado por ``htmx`` para no hacer un full page reload. 
    - Crear por lo menos un modal con un formulario con ``htmx`` para la creación o edición de algún modelo. 

- Las tablas se deben implementar con ``django-tables2``. 
- Para los filtros utilizar ``django-filters``. 
- Los campos de auditoría se pueden implementar con ``django-author``. 
- Utilizar ``django-crispy-forms`` para la creación de formularios. 
- Si se elige el Bonus 2, utilizar ``django-bootstrap-datepicker-plus`` para los datetime fields.
- Utilizar ``pytest`` para las pruebas 

    - El proyecto debe tener un coverage de por lo menos el 90% 

Recursos Útiles
---------------

HTMX

- `Modal forms with Django+HTMX <https://blog.benoitblanchon.fr/django-htmx-modal-form/>`_
- `django-htmx en GitHub <https://github.com/adamchainz/django-htmx/tree/main>`_
- `Responsive table with Django and htmx <https://enzircle.com/responsive-table-with-django-and-htmx>`_
- `dj-htmx-fun <https://github.com/joashxu/dj-htmx-fun>`_
- `How to Create a Responsive Table with HTMX and Django <https://hackernoon.com/how-to-create-a-responsive-table-with-htmx-and-django>`_

Django Crispy Forms

- `Advanced Form Rendering with Django Crispy Forms <https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html>`_

Pytest

- `Playlist de YouTube sobre Pytest <https://www.youtube.com/playlist?list=PLOLrQ9Pn6caw3ilqDR8_qezp76QuEOlHY>`_
- `Python Pytest and Django Course <https://github.com/veryacademy/pytest-mastery-with-django>`_
- `Simplified Django Tests With Pytest and Pytest FactoryBoy <https://schegel.net/posts/simplied-django-tests-with-pytest-and-pytest-factoryboy/>`_

Bonus
------

Se debe implementar por lo menos uno de los siguientes Bonus.

Opción 1: Margen de Ganancia Histórico y con Proyección
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El precio de los insumos varía con el tiempo, lo que puede provocar que el precio de venta del producto también varíe en el tiempo. Por lo tanto, el margen de utilidad de un producto es dinámico.

- Para poder obtener valores estadísticos y realizar proyecciones de venta, se requiere almacenar el precio histórico de los Insumos y Productos.

    - Los precios deben tener un rango de vigencia: ``vigente_desde`` y ``vigente_hasta``.

- Tener cuidado en no permitir que existan periodos de tiempo sin un precio de Insumo o Producto vigente.
    
    - Evitar situaciones donde la vigencia de un producto sea del 01/01/2024 al 10/01/2024 y el siguiente periodo sea del 15/01/2024 al 01/02/2024.

- En el Dashboard de Margen de Ganancia, mostrar por defecto los valores en la fecha actual.
- Agregar un filtro por fecha donde al cambiar la fecha se vean los valores de Costo Total, Precio de Venta y Margen de la fecha seleccionada.

Opción 2: Producto con Variaciones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un mismo producto puede ser vendido en distintas presentaciones. Con presentaciones nos referimos a distintos tamaños de un producto. Por ejemplo, se puede vender un Pie de Manzana de 15cm, 25cm y 30cm.

- Un producto puede tener 1 o muchas variaciones.
- Un producto siempre debe tener una variación principal.
- El usuario únicamente debe ingresar las dimensiones de la variación y las cantidades de insumos que dicha variación utiliza se calculan en base a la variación principal.
    
    - Para facilitar el modelo: 
    
        - Se considera que la forma de un producto es constante. Por ejemplo, si el Pie de Manzana es ingresado con forma Circular, todas sus variaciones van a tener forma circular.
        - El Alto es constante.
        - En otras palabras, la variación solo se define en base al diámetro si la forma es Circular; y el Largo y Ancho si la forma es Rectangular.

    - Para ajustar la cantidad de insumos que se utiliza en una variación, se debe encontrar el cambio proporcional entre el área de superficie de la variación principal y la variación deseada. Por ejemplo, si la forma es Circular: ``(Dvariación / 2)² / (Dprincipal / 2)²``.

- Se requiere de un UI donde se pueda ver la cantidad de Insumos que se utiliza en cada variación.
- En el UI de Margen de Ganancia, se debe mostrar todas las variaciones de los productos.
