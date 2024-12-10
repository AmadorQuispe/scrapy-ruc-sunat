from CodigoUsuario.CuTexto import *
from EntidadNegocio.EnSUNAT import EnSUNAT
from utils.common import *
import requests
import sys
import traceback

    

    

    
def init_consult_mult_ruc(path:str):        
    urlInicial = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"

    is_success, message_error, sesion,num_random = get_session_ramdom("46568855")
    if(is_success):
        rucs = read_txt_one_col(path=path)
        print("se ha iniciando consultas. Espere ...")
        for ruc in rucs:
            correct,datos = ConsultarContenidoRUC(sesion, urlInicial, ruc, num_random)
            if(correct):
                line = f'{datos.RUC}|{datos.EstadoContribuyente}|{datos.TipoContribuyente}'
                write_txt('resultado_ro.txt',line)
            else:
                print(f"Error al consultar {ruc}")
        
    

def ObtenerDatosRUC(contenidoHTML):
    oEnSUNAT = EnSUNAT()
    nombreInicio = ""
    nombreFin = ""
    posicion = 0
    arrResultado = list()

    nombreInicio = "<HEAD><TITLE>"
    nombreFin = "</TITLE></HEAD>"
    contenidoBusqueda = ExtraerContenidoEntreTagString(contenidoHTML, 0, nombreInicio, nombreFin)    
    if (contenidoBusqueda == ".:: Pagina de Mensajes ::."):
        nombreInicio = "<p class=\"error\">"
        nombreFin = "</p>"
        oEnSUNAT.TipoRespuesta = 2
        oEnSUNAT.MensajeRespuesta = ExtraerContenidoEntreTagString(contenidoHTML, 0, nombreInicio, nombreFin)
    elif (contenidoBusqueda == ".:: Pagina de Error ::."):
        nombreInicio = "<p class=\"error\">"
        nombreFin = "</p>"
        oEnSUNAT.TipoRespuesta = 3
        oEnSUNAT.MensajeRespuesta = ExtraerContenidoEntreTagString(contenidoHTML, 0, nombreInicio, nombreFin)
    else:
        oEnSUNAT.TipoRespuesta = 2

        nombreInicio = "<div class=\"list-group\">"
        nombreFin = "<div class=\"panel-footer text-center\">"
        contenidoBusqueda = ExtraerContenidoEntreTagString(contenidoHTML, 0, nombreInicio, nombreFin)        
        if (contenidoBusqueda == ""):
            nombreInicio = "<strong>"
            nombreFin = "</strong>"
            oEnSUNAT.MensajeRespuesta = ExtraerContenidoEntreTagString(contenidoHTML, 0, nombreInicio, nombreFin)
            if(oEnSUNAT.MensajeRespuesta == ""):
                oEnSUNAT.MensajeRespuesta = "No se puede obtener los datos del RUC, porque no existe la clase principal \"list-group\" en el contenido HTML"
        else:
            nombreInicio = "<h4 class=\"list-group-item-heading\">"
            nombreFin = "</h4>"
            posicion = 0

            arrResultado = ExtraerContenidoEntreTag(contenidoHTML, posicion, nombreInicio, nombreFin, False)
            if(len(arrResultado)> 0):
                posicion = int(arrResultado[0])
                arrResultado = ExtraerContenidoEntreTag(contenidoHTML, posicion, nombreInicio, nombreFin, False)                
                posicion = int(arrResultado[0])
                oEnSUNAT.RUC = arrResultado[1]
                oEnSUNAT.TipoRespuesta = 1
            else:
                oEnSUNAT.MensajeRespuesta = "No se puede obtener la \"Razon Social\", porque no existe la clase \"list-group-item-heading\" en el contenido HTML"

            if(oEnSUNAT.TipoRespuesta == 1):
                '''
                # Mensaje cuando el estado es "BAJA DE OFICIO" caso contrario inicia con "Tipo Contribuyente"
                # Tipo Contribuyente
                # Nombre Comercial
                # Fecha de Inscripción
                # Fecha de Inicio de Actividades
                # Estado del Contribuyente
                # Condición del Contribuyente
                # Domicilio Fiscal
                # Sistema Emisión de Comprobante
                # Actividad Comercio Exterior
                # Sistema Contabilidiad
                # Emisor electrónico desde:
                # Comprobantes Electrónicos:
                # Afiliado al PLE desde
                # n/a
                '''
                lCadena = list()
                nombreInicio = "<p class=\"list-group-item-text\">"
                nombreFin = "</p>"
                posicion = 0
                arrResultado = ExtraerContenidoEntreTag(contenidoHTML, posicion, nombreInicio, nombreFin, False)
                while(len(arrResultado)>0):
                    posicion = int(arrResultado[0])
                    lCadena.append(arrResultado[1].strip())
                    arrResultado = ExtraerContenidoEntreTag(contenidoHTML, posicion, nombreInicio, nombreFin, False)
                # print(lCadena)
                if(len(lCadena) == 0):
                    oEnSUNAT.TipoRespuesta = 2
                    oEnSUNAT.MensajeRespuesta = "No se puede obtener los datos básicos, porque no existe la clase \"list-group-item-text\" en el contenido HTML"
                else:
                    inicio = 0 
                    if(len(lCadena) > 15): # Si estado es "BAJA DE OFICIO" caso contrario es 14 -----Toque
                        inicio = 1
                    oEnSUNAT.TipoContribuyente = lCadena[inicio]
                    oEnSUNAT.NombreComercial = lCadena[inicio + 1]
                    oEnSUNAT.FechaInscripcion = lCadena[inicio + 2]
                    oEnSUNAT.FechaInicioActividades = lCadena[inicio + 3]
                    oEnSUNAT.EstadoContribuyente = lCadena[inicio + 4]
                    oEnSUNAT.CondicionContribuyente = lCadena[inicio + 5]
                    oEnSUNAT.DomicilioFiscal = lCadena[inicio + 6]
                    oEnSUNAT.SistemaEmisionComprobante = lCadena[inicio + 7]
                    oEnSUNAT.ActividadComercioExterior = lCadena[inicio + 8]
                    oEnSUNAT.SistemaContabilidiad = lCadena[inicio + 9]
                    oEnSUNAT.EmisorElectrónicoDesde = lCadena[inicio + 10]
                    oEnSUNAT.ComprobantesElectronicos = lCadena[inicio + 11]
                    oEnSUNAT.AfiliadoPLEDesde = lCadena[inicio + 12]                    
                    '''
                    # Actividad(es) Económica(s)
                    # Comprobantes de Pago c/aut. de impresión (F. 806 u 816)
                    # Sistema de Emisión Electrónica # (opcional, em algunos casos no aparece)
                    # Padrones 
                    '''
                    lCadena = list()
                    nombreInicio = "<tbody>"
                    nombreFin = "</tbody>"
                    posicion = 0
                    arrResultado = ExtraerContenidoEntreTag(contenidoHTML, posicion, nombreInicio, nombreFin, False)
                    while(len(arrResultado)>0):
                        posicion = int(arrResultado[0])
                        lCadena.append(arrResultado[1].strip().replace('\r\n', ' ').replace('\t', ' '))
                        arrResultado = ExtraerContenidoEntreTag(contenidoHTML, posicion, nombreInicio, nombreFin, False)
                    if(len(lCadena) == 0):
                        oEnSUNAT.TipoRespuesta = 2
                        oEnSUNAT.MensajeRespuesta = "No se puede obtener los datos de las tablas, porque no existe el tag \"tbody\" en el contenido HTML"
                    else:
                        oEnSUNAT.ActividadesEconomicas = lCadena[0]
                        oEnSUNAT.ComprobantesPago = lCadena[1]
                        if(len(lCadena) == 4):
                            oEnSUNAT.SistemaEmisionElectrónica = lCadena[2]
                            oEnSUNAT.Padrones = lCadena[3]
                        else:
                            oEnSUNAT.Padrones = lCadena[2]

    return oEnSUNAT

def ConsultarContenidoRUC(sesion, urlReferencia, numeroRUC, numeroRandom):
    is_success = False
    datos = None

    payload={}
    headers = {
        'Host': 'e-consultaruc.sunat.gob.pe',
        'Origin': 'https://e-consultaruc.sunat.gob.pe',
        'Referer': urlReferencia,
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    url = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias?accion=consPorRuc&nroRuc=%s&contexto=ti-it&modo=1&numRnd=%s" % (numeroRUC, numeroRandom)
    response = sesion.request("POST", url, headers=headers, data=payload, verify=True)
    contenidoHTML = response.text    

    if(response.status_code == 200):
        oEnSUNAT = ObtenerDatosRUC(contenidoHTML)
        if (oEnSUNAT.TipoRespuesta == 1):
            datos = oEnSUNAT
            is_success = True
        else:
            datos = None
            is_success = False
    else:
        print("Ocurrió un inconveniente (%s) al consultar los datos del RUC %s.\r\nDetalle: %s" % (response.status_code, numeroRUC, contenidoHTML))
    
    return is_success,datos

def get_session_ramdom(dni):
    is_success = False
    message_error = ""
    sesion = None
    num_ramdom = ""
    try:
        initial_url = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"
        payload={}
        headers = {
            'Host': 'e-consultaruc.sunat.gob.pe',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        }

        sesion = requests.Session()
        response = sesion.request("GET", initial_url, headers=headers, data=payload, verify=True)

        if(response.status_code == 200):
            payload={}
            headers = {
                'Host': 'e-consultaruc.sunat.gob.pe',
                'Origin': 'https://e-consultaruc.sunat.gob.pe',
                'Referer': initial_url,
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                'sec-ch-ua-mobile': '?0',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            }
            url = f"https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias?accion=consPorTipdoc&razSoc=&nroRuc=&nrodoc={dni}&contexto=ti-it&modo=1&search1=&rbtnTipo=1&tipdoc=1&search2={dni}&search3=&codigo="
            
            nIntents = 0
            status_code = 401
            body_resp = ''
            # Validamos que intente hasta 3 veces si el código de respuesta es 401 Unauthorized
            while(nIntents < 3 and status_code == 401):
                response = sesion.request("POST", url, headers=headers, data=payload, verify=True)
                status_code = response.status_code
                body_resp = response.text 
                nIntents = nIntents + 1
            if(status_code == 200):
                num_ramdom = ExtraerContenidoEntreTagString(body_resp, 0, "name=\"numRnd\" value=\"", "\">")              
                is_success = True
            else:
                message_error = "Ocurrió un inconveniente (%s) al consultar el número ramdom del RUC %s.\r\nDetalle: %s" % (response.status_code, dni, body_resp)                
        else:
            message_error = "Ocurrió un inconveniente (%s) al consultar la página principal con el RUC %s.\r\nDetalle: %s" % (response.status_code, dni, response.text)
        return is_success, message_error, sesion,num_ramdom
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        print("Ocurrió el error \"%s\" al obtener los datos del RUC.\nDetalle: %s" % (str(sys.exc_info()[1]), tbinfo))
        message_error = "Ocurrió el error \"%s\" al obtener los datos del RUC.\nDetalle: %s" % (str(sys.exc_info()[1]), tbinfo)
    
    


if __name__ == '__main__':
    ruta = input("ingrese la ruta del base :")
    init_consult_mult_ruc(ruta)
    print("Consulta terminada...")
    input("Presione una tecla ENTER para terminar...")