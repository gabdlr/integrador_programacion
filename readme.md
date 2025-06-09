# Trabajo integrador - Organigrama con árboles

Esta herramienta permite diagramar la estructura de una organización según las relaciones superior -> subordinado.

## Modo de uso
1. Crear una organización
2. Agregar CEO a la organización
3. Manejar los empleados de la organización

### Organización

Puede crear multiples organizaciones, estas solo necesitan un nombre el cual no tiene que ser único.

### CEO

El CEO es la **figura de máxima autoridad** dentro de la organización **debe ser añadido antes que cualquier otro empleado** ya que cualquier otro empleado es un subordinado del mismo, **el CEO puede ser modificado pero no eliminado**.

### Empleado

Los empleados **deben tener un superior** para poder añadirse a la organización, el empleado (al igual que el CEO) cuentan con las propiedades nombre, DNI y puesto, **el DNI debe ser un identificador único** y no pueden añadirse mas de un empleado con el mismo DNI. El mismo empleado **no puede ser añadido como subordinado de dos superiores a la vez** (seran sus superiores todos los empleados que le antecedan dentro de la jerarquía).