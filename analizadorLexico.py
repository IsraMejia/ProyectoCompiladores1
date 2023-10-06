from scanner import *

def main():
    intro = """
        \n\t\tAnalizador Lexico . Proyecto 1 compiladores 
    """
    print(intro)
    codigo = """
            INT x = 10;  
            IF  MJ == 23   THEN     A=X ; 
            IMPRIMIR "HOLA MUNDO";   
              
        """ 
    codigo = codigo + "\n"  
    scanner = Scanner(codigo)

    print(f' A continuacion se muestra el codigo ingresado: \n {codigo} \n\n\nAnalizando ...')
    print("\nSe ha analizado el codigo ingresado, retornando los siguientes tokens:\n")

    token = scanner.caracterAToken()
    while token.tipoToken != TipodeTokens.FIN_DE_LINEA: 
        print(f"\tLeido    {token.caracterToken}   ----Tokenizado a --->    {token.tipoToken} \n")
        token = scanner.caracterAToken()
 
    print("\n\n Tareas finalizadas, vuelva pronto")

main()