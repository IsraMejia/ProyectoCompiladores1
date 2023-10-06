import sys
from token_an import *
class Scanner:

    palabras_reservadas = {
        "asignacion"    : ["=", "Simbolo de asignacion, dos seguidos es comparacion de igualdad"],
        "menor_que"     : ["<", "Comparacion de menor que"],
        "mayor_que"     : [">", "Comparacion de mayor que"], 
        "suma"          : ["+", "operador de suma"],
        "resta"         : ["-", "operador de resta"],
        "asterisco"     : ["*", "operador de asterisco"],
        "diagonal"      : ["/", "operador diagonal o slash"], 
        "porcentaje"    : ["%", "operador de porcentaje"],
        "comillas"      : ['\"', "signo de comillas"], 
        "dob_diagonal_inv"  : ['\\', "operador de doble diagonal invertida o slash invertido"], 
        "admiracion"    : ["!", "Signo de admiracion, si tiene un != sera distinto a "],
        "a_parentesis"  : ['(', "abrir parentesis"],
        "c_parentesis"  : [')', "cerrar parentesis"],
        "punto"         : [".", "Simbolo de punto"], 
        "salto_linea"   : ["\n", "Salto de linea"], 
        "fin_linea"     : ["\0", "Fin de linea"],  
        "sangria"       : ["\t", "Fin de linea"],  
        "retorno_carro" : ["\r", "retorno de carro, sobreescribe el inicio de la linea"], 
        "fin_sentencia" : [";", "Fin de una sentencia"]
    }

    def __init__(self, codigo):
        self.codigo = codigo 
        self.caracterActual = ''    
        self.posicionActual = -1    
        self.sigCaracter()


    def sigCaracter(self):
        self.posicionActual += 1
        if self.posicionActual >= len(self.codigo):
            self.caracterActual = '\0'   
        else:
            self.caracterActual = self.codigo[self.posicionActual]


    def revisaSigCaracter(self):
        if self.posicionActual + 1 >= len(self.codigo):
            return '\0'
        return self.codigo[self.posicionActual+1]
 
    def eTerminarAnalisis(self, message):
        sys.exit("Se encontro un Error Lexico en el codigo proporcionado: " + message)
		
        
    def omitirEspaciosVacios(self):
        while (self.caracterActual == ' ' or 
               self.caracterActual == '\t' or 
               self.caracterActual == '\r'):
                self.sigCaracter()
		
     
    def omitirComentarios(self):
        if self.caracterActual == '#':
            while self.caracterActual != '\n':
                self.sigCaracter()


    def caracterAToken(self,):

        self.omitirEspaciosVacios()
        self.omitirComentarios()
        token = None

        #Reglas de nuestro alfabeto, asi como deteccion de tokens
        
        if self.caracterActual == self.palabras_reservadas['suma'][0] :
            token = Token(self.caracterActual, TipodeTokens.SUMA)

        elif self.caracterActual == self.palabras_reservadas['fin_sentencia'][0]:
            token = Token(self.caracterActual, TipodeTokens.FIN)

        elif self.caracterActual == self.palabras_reservadas['resta'][0] :
            token = Token(self.caracterActual, TipodeTokens.RESTA)

        elif self.caracterActual == self.palabras_reservadas['asterisco'][0] :
            token = Token(self.caracterActual, TipodeTokens.ASTERISCO)
            
        elif self.caracterActual == self.palabras_reservadas['diagonal'][0] :
            token = Token(self.caracterActual, TipodeTokens.DIAGONAL)

        #Reglas de asignacion o comparacion de igual igualdad
        elif self.caracterActual == self.palabras_reservadas['asignacion'][0] :
            # Compruebe si este token es = o ==
            if self.revisaSigCaracter() == self.palabras_reservadas['asignacion'][0]: 
                lastChar = self.caracterActual
                self.sigCaracter()
                token = Token(lastChar + self.caracterActual, TipodeTokens.IGUAL)
            else:
                token = Token(self.caracterActual, TipodeTokens.ASIGNACION) 


        #Reglas de comparadores
        elif self.caracterActual == self.palabras_reservadas['mayor_que'][0]  :
            # Compruebe si este token es > o >=
            if self.revisaSigCaracter() == self.palabras_reservadas['asignacion'][0] :
                lastChar = self.caracterActual
                self.sigCaracter()
                token = Token(lastChar + self.caracterActual, TipodeTokens.MAYORIGUAL)
            else:
                token = Token(self.caracterActual, TipodeTokens.MAYOR)

        elif self.caracterActual == self.palabras_reservadas['menor_que'][0] : 
                if self.revisaSigCaracter() == self.palabras_reservadas['asignacion'][0]:
                    lastChar = self.caracterActual
                    self.sigCaracter()
                    token = Token(lastChar + self.caracterActual, TipodeTokens.MENORIGUAL)
                else:
                    token = Token(self.caracterActual, TipodeTokens.MENORQUE)

        elif self.caracterActual == self.palabras_reservadas['admiracion'][0] :
            if self.revisaSigCaracter() == self.palabras_reservadas['asignacion'][0] :
                lastChar = self.caracterActual
                self.sigCaracter()
                token = Token(lastChar + self.caracterActual, TipodeTokens.DISTINTOA) 
            else:
                self.eTerminarAnalisis(" caracter invalido" + self.revisaSigCaracter())

        #Reglas para cadenas de texto entre comillas
        elif self.caracterActual == self.palabras_reservadas['comillas'][0] : 
            self.sigCaracter()
            posicionInicial = self.posicionActual
            #Revisamos caracteres calidos dentro de comillas
            while self.caracterActual != self.palabras_reservadas['comillas'][0] : 
                if (self.caracterActual == self.palabras_reservadas['retorno_carro'][0]     or 
                    self.caracterActual == self.palabras_reservadas['salto_linea'][0]       or 
                    self.caracterActual == self.palabras_reservadas['sangria'][0]           or 
                    self.caracterActual == self.palabras_reservadas['dob_diagonal_inv'][0]  or 
                    self.caracterActual == self.palabras_reservadas['porcentaje'][0] ):
                        self.eTerminarAnalisis("No se perrmite caracteres especiales en cadenas")

                self.sigCaracter()
            textoIdentificado = self.codigo[posicionInicial : self.posicionActual]  
            token = Token(textoIdentificado, TipodeTokens.STRING)



        #Reglas para numeros
        elif self.caracterActual.isdigit(): 
            posicionInicial = self.posicionActual
            while self.revisaSigCaracter().isdigit():
                self.sigCaracter()
            #Revisamos si tenemos valores decimales validos
            if self.revisaSigCaracter() == '.':  
                self.sigCaracter() 
                if not self.revisaSigCaracter().isdigit():  
                    self.eTerminarAnalisis("No se permite caracteres dentro de un numero")
                while self.revisaSigCaracter().isdigit():
                    self.sigCaracter()

            textoIdentificado = self.codigo[posicionInicial : self.posicionActual + 1] 
            token = Token(textoIdentificado, TipodeTokens.NUMERO)



        #Reglas para caracteres de texto
        elif self.caracterActual.isalpha(): 
            posicionInicial = self.posicionActual
            while self.revisaSigCaracter().isalnum():
                self.sigCaracter() #En caso de ser alfanumerico continua revisando cada los caracteres

            #Se guarda la cadena de alfanumericos que tienen que iniciar con una letra
            textoIdentificado = self.codigo[posicionInicial : self.posicionActual + 1]  
            
            palabraReservada = Token.ifPalabraReservada(textoIdentificado) 
            if palabraReservada == None: # Es variable
                token = Token(textoIdentificado, TipodeTokens.VARIABLE)
            else:   # palabraReservada
                token = Token(textoIdentificado, palabraReservada)

        elif self.caracterActual == self.palabras_reservadas['salto_linea'][0]  : 
            token = Token('\\n', TipodeTokens.NUEVA_LINEA)
        
        elif self.caracterActual == self.palabras_reservadas['fin_linea'][0]  :
            token = Token('', TipodeTokens.FIN_DE_LINEA)
        else: #Token desconosido
            self.eTerminarAnalisis("Token no valido " + self.caracterActual)
			
        self.sigCaracter()
        return token

 
