#Arbol bajo nivel
def nodo(valor):
    return (valor, [])

def agregar_nodo(padre, hijo):
    if padre == hijo:
        return
    if buscar_en_arbol(padre, hijo):
        return
    return padre[1].append(hijo)

def buscar_en_arbol(fuente, objetivo, resultado=False):
    if resultado is True:
        return resultado
    resultado = fuente == objetivo
    hijos = fuente[1]
    if len(hijos) == 0:
        return resultado
    for hijo in hijos:
        resultado = hijo == objetivo
        if len(hijo[1]) != 0:
            resultado = buscar_en_arbol(hijo[1][0], objetivo, resultado)
    return resultado

def buscar_en_arbol_por_campo(campo: str, valor: str, nodo: (dict, list[nodo]), resultado=None):
    if resultado is not None:
        return resultado
    if dict.get(nodo[0], campo) is not None and nodo[0][campo] == valor:
        resultado = nodo
        return resultado
    if len(nodo[1]) > 0:
        hijos = nodo[1]
        for hijo in hijos:
            resultado = buscar_en_arbol_por_campo(campo, valor, hijo, resultado)
    return resultado

#TODO: Nombre funciones repensar
def buscar_nodo_padre(arbol, nodo, padre=None):
    if len(arbol[1]) > 0:
        hijos = arbol[1]
        for hijo in hijos:
            if hijo == nodo:
                padre = arbol
                return padre
            padre = eliminar_nodo(hijo, nodo)
    return padre

def eliminar_nodo(arbol, nodo):
    padre = buscar_nodo_padre(arbol, nodo)
    if padre is not None:
        hijos = nodo[1]
        for hijo in hijos:
            padre[1].append(hijo)
        padre[1].remove(nodo)

#Organizacion alto nivel

##empleado
def buscar_empleado_por_dni(org, dni):
    return buscar_en_arbol_por_campo("dni", dni, org)

def crear_empleado(nombre, dni, puesto):
    return nodo({'nombre': nombre, 'dni': dni,'puesto': puesto})

def modificar_empleado(org, dni, nuevo_nombre=None, nuevo_dni=None, nuevo_puesto=None):
    empleado = buscar_empleado_por_dni(org, dni)
    if empleado is not None:
        if nuevo_nombre is not None:
            empleado[0]["nombre"] = nuevo_nombre
        if nuevo_dni is not None:
            empleado_con_nuevo_dni = buscar_empleado_por_dni(org, nuevo_dni)
            if empleado_con_nuevo_dni is not None:
                print("Ya existe un empleado registrado con ese DNI")
            else:
                empleado[0]["dni"] = nuevo_dni
        if nuevo_puesto is not None:
            empleado[0]["puesto"] = nuevo_puesto

def eliminar_empleado(org, dni):
    empleado = buscar_empleado_por_dni(org, dni)
    if empleado is not None:
        if empleado in org[1]:
            print("El CEO no puede ser eliminado")
        else:
            eliminar_nodo(org, empleado)
            print("Se elimino el empleado")

def listar_empleados(jefe, padding=0):
    pad_str = " " * padding;
    if padding == 0:
        print(f"{pad_str}Nombre: {jefe[0]['nombre']} DNI: {jefe[0]['dni']} Puesto: {jefe[0]['puesto']}")
    if len(jefe[1]) > 0:
        subordinados = jefe[1]
        pad_str = (" " * 2) + pad_str;
        for subordinado in subordinados:
            print(f"{pad_str}Nombre: {subordinado[0]['nombre']} DNI: {subordinado[0]['dni']} Puesto: {subordinado[0]['puesto']}")
            if len(subordinado[1]) > 0:
                listar_empleados(subordinado, padding+2)

def agregar_subordinados(organizacion, dni_superior, subordinado):
    superior = buscar_empleado_por_dni(organizacion, dni_superior)
    if superior is not None:
        #verificar que no exista un empleado con el dni del subordinado
        agregar_nodo(superior, subordinado)
    return organizacion


##organizacion
def crear_organizacion(nombre):
    return nodo({'organizacion': nombre})

def designar_ceo(organizacion, nombre, dni):
    ceo = crear_empleado(nombre, dni, "CEO")
    if len(organizacion[1]) == 0:
        agregar_nodo(organizacion, ceo)

#CLI
organizaciones = []
def iniciar_programa(organizaciones):
    option = 0

    while(option != "9"):
        print("    Seleccione una opción: ")
        print("1.- Agregar nueva organización")
        if len(organizaciones) > 0:
            print("2.- Administrar organización")
        print("9.- Salir")
        option = input()
        match option:
            case "1":
                nombre_organizacion = input("Introduzca el nombre de la organización: ")
                organizaciones.append(crear_organizacion(nombre_organizacion))
                for organizacion in organizaciones:
                    print(organizacion[0]["organizacion"])
            case "2":
                if len(organizaciones) > 0:
                    imprimir_menu_seleccionar_organizacion(organizaciones)
            case "9":
                return
            case _: option = "None"
        
def imprimir_menu_seleccionar_organizacion(organizaciones):
    
        opcion = None
        while(opcion == None):
            print("Seleccione una organización")
            contador = 1
            for organizacion in organizaciones:
                print(f"Seleccione {contador} para la organización {organizacion[0]['organizacion']}")
                contador += 1
            print("0.- Salir")
            opcion = input()
            
            try:
                if opcion == "0":
                    return
                opcion_numero = int(opcion)
                if opcion_numero > 0 and (opcion_numero <= len(organizaciones)):
                    organizacion = organizaciones[opcion_numero - 1]
                    print(f"Seleccionó la organización {organizacion[0]['organizacion']}")
                    imprimir_menu_administrar_organizacion(organizacion)
                opcion = None
            except ValueError:
                print("Debe ingresar una opción válida")
                opcion = None

def imprimir_menu_administrar_organizacion(organizacion):
    def agregar_ceo(organizacion):
        nombre_ceo = input("Ingrese el nombre del CEO: ")
        dni_ceo = input("Ingrese el DNI del ceo: ")
        designar_ceo( organizacion, nombre_ceo, dni_ceo)
    
    def agregar_empleado(organizacion):
        dni_superior = input("Ingrese el DNI del superior de este empleado: ")
        superior = buscar_empleado_por_dni(organizacion, dni_superior)
        if superior is not None:
            nombre_empleado = input("Ingrese el nombre del empleado: ")
            dni_empleado = input("Ingrese el DNI del empleado: ")
            puesto_empleado = input("Ingrese el puesto del empleado: ")
            empleado = crear_empleado(nombre_empleado, dni_empleado, puesto_empleado)
            #validar que el dni no este en uso por otro empleado
            agregar_subordinados(organizacion, dni_superior, empleado)
        else:
            print("No se encontro un empleado con ese DNI")
    
    def modificar_empleado_cli(organizacion):
        texto_menu = """1.- Modificar nombre\n2.- Modificar DNI\n3.- Modificar puesto\n4.- Salir"""
        dni_empleado = input("Ingrese el DNI del usuario que desea modificar: ")
        empleado = buscar_empleado_por_dni(organizacion, dni_empleado)
        if empleado is None:
            print("No se encontro un empleado con ese DNI en esta organización")
        else:
            opcion = None
            while(opcion == None):
                print(texto_menu)
                opcion = input()
                match opcion:
                    case "1":
                        nuevo_nombre = input("Ingrese el nuevo nombre del usuario: ")
                        modificar_empleado(organizacion, dni_empleado, nuevo_nombre)
                        opcion = None
                    case "2":
                        nuevo_dni = input("Ingrese el nuevo DNI del usuario: ")
                        modificar_empleado(organizacion, dni_empleado, nuevo_dni=nuevo_dni)
                        opcion = None
                    case "3":
                        nuevo_puesto = input("Ingrese el nuevo puesto del usuario: ")
                        modificar_empleado(organizacion, dni_empleado, nuevo_puesto=nuevo_puesto)
                        opcion = None
                    case "4":
                        return
                    case _:
                        opcion = None
    
    def eliminar_empleado_cli(organizacion):
        dni_usuario_eliminar = input("Ingrese el DNI del usuario que desea eliminar: ")
        usuario_eliminar = buscar_empleado_por_dni(organizacion, dni_usuario_eliminar)
        if usuario_eliminar is None:
            print("No se encontro un empleado con ese DNI")
        else:
            eliminar_empleado(organizacion, dni_usuario_eliminar)

    opcion = None
    while(opcion == None):
        texto_menu_sin_ceo = """1.- Agregar CEO
2.- Salir"""
        texto_menu_con_ceo = """1.- Listar empleados
2.- Agregar empleado
3.- Modificar empleado
4.- Eliminar empleado
5.- Salir"""
        if len(organizacion[1]) == 0:
            print(texto_menu_sin_ceo)
        else:
            print(texto_menu_con_ceo)
        
        opcion = input()
        
        if len(organizacion[1]) == 0:
            if(opcion == "1"):
                agregar_ceo(organizacion)
            else:
                if(opcion != "2"):
                    print("Debe ingresar una opción válida")
                    opcion = None
        else: 
            match opcion:
                case "1":
                    listar_empleados(organizacion[1][0])
                case "2":
                    agregar_empleado(organizacion)
                case "3":
                    modificar_empleado_cli(organizacion)
                case "4":
                    eliminar_empleado_cli(organizacion)
                case _:
                    print("Debe ingresar una opción válida")
            if(opcion != "5"):
                opcion = None

iniciar_programa(organizaciones)