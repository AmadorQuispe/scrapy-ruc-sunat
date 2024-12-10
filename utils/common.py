
def ruc_validate(ruc):
    isValid = False
    message = ""    
    if(len(ruc) == 11):
        if ruc.isdigit():
            isValid = True
        else:
            message = "El número de RUC '%s' debe contener solo caracteres numéricos" % (ruc)
    else:
        message = "El número de RUC '%s' tiene %d %s y este debe ser de 11 caracteres" % (ruc, len(ruc), "carácter" if len(ruc)==1 else "caracteres")               
    return isValid, message


def read_txt_one_col(path):
    urls = []
    with open(path,'r',encoding='utf-8') as f:
        urls = [l.rstrip() for l in f]               
    f.close()
    return urls

def write_txt(path,line):
    with open(path,'a',encoding='UTF-8') as f:
        f.write(f'{line}\n')
        f.close()

def generate_ruc_by_dni(dni):
    dni = ''.join(dni.split())
    if len(dni)==8 and dni.isnumeric():
        ruc = f'10{dni}'
        sum = 0
        x = 5
        for n in ruc:
            x = 7 if (x==1) else x
            sum += (int(n) * x)
            x-=1
        rest = 11 - (sum % 11)
        fnum = rest -10 if (rest>=10) else rest
        return f'{ruc}{fnum}'   
    else:
        raise ValueError(f'{dni} is not a number or length is greater or less than 8')