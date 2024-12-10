def ExtraerContenidoEntreTagString(cadena, posicion, nombreInicio, nombreFin, sensitivo=False):
    respuesta = ""
    if(sensitivo):
        cadena2 = cadena.lower()
        nombreInicio = nombreInicio.lower()
        nombreFin=nombreFin.lower()
        posicionInicio = cadena2.find(nombreInicio, posicion)
        if (posicionInicio > -1):
            posicionInicio += len(nombreInicio)
            posicionFin = cadena2.find(nombreFin, posicionInicio)
            if(posicionFin>-1):
                respuesta = cadena[posicionInicio:posicionFin]
    else:
        posicionInicio = cadena.find(nombreInicio, posicion)
        if (posicionInicio > -1):
            posicionInicio += len(nombreInicio)
            posicionFin = cadena.find(nombreFin, posicionInicio)
            if(posicionFin>-1):
                respuesta = cadena[posicionInicio:posicionFin]
    return respuesta

def ExtraerContenidoEntreTag(cadena, posicion, nombreInicio, nombreFin, sensitivo=False):
    respuesta = list()
    if(sensitivo):
        cadena2 = cadena.lower()
        nombreInicio = nombreInicio.lower()
        nombreFin=nombreFin.lower()
        posicionInicio = cadena2.find(nombreInicio, posicion)
        if (posicionInicio > -1):
            posicionInicio += len(nombreInicio)
            posicionFin = cadena2.find(nombreFin, posicionInicio)
            if(posicionFin>-1):
                posicion = posicionFin + len(nombreFin)
                respuesta = [posicion, cadena[posicionInicio:posicionFin]]
    else:
        posicionInicio = cadena.find(nombreInicio, posicion)
        if (posicionInicio > -1):
            posicionInicio += len(nombreInicio)
            posicionFin = cadena.find(nombreFin, posicionInicio)
            if(posicionFin>-1):
                posicion = posicionFin + len(nombreFin)
                respuesta = [posicion, cadena[posicionInicio:posicionFin]]
    return respuesta