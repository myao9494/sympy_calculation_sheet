from sympy import Symbol,pi,Eq
from IPython.display import display
from sympy.interactive import printing
printing.init_printing(use_latex=True)
import pandas as pd
import re

σmax= Symbol('σ_max')
eσmax= Symbol('σ_max')
MPa= Symbol('(MPa)')
Mmax= Symbol('M_max')
eMmax= Symbol('M_max')
N_mm= Symbol('(N \cdot mm)')
Z= Symbol('Z')
eZ= Symbol('Z')
mm3= Symbol('({mm^3})')
F= Symbol('F')
eF= Symbol('F')
N= Symbol('(N)')
L= Symbol('L')
eL= Symbol('L')
mm= Symbol('(mm)')

paramater_dict= {
    "σmax":["曲げ応力","MPa"],
    "Mmax":["曲げモーメント","N_mm"],
    "Z":["断面係数","mm3"],
    "F":["荷重","N"],
    "L":["梁の長さ","mm"]
    }

def create_symbol():
    global paramater_dict
    out = []
    out_g = []
    for para in paramater_dict:
        #パラメータを作る　二文字以上の場合は下付文字にする　e付は数式表示用
        if len(para) !=1:
            temp = para[:1]+"_"+para[1:]
        else:
            temp = para
        out_g.append(para)

        #単位を作成する 数字は上付きにして、_は・に変換する
        unit = paramater_dict[para][1]
        numerical_list = re.findall('[0-9]' , unit)

        if len(numerical_list) != 0:
            t = numerical_list[0]
            unit = unit.replace(t,"^"+t)
            unit =  "{" + unit +"}"
        elif unit.find("_") != 0:
            unit = unit.replace("_"," \cdot ")

        unit = "(" + unit + ")"
        out.append([para,temp])
        out.append(["e"+para,temp])
        out.append([paramater_dict[para][1],unit])

        df = pd.DataFrame(out)
        df = df.drop_duplicates()
        out = df.values.tolist()
    for elm in out:
        print(elm[0] +"= Symbol('" +elm[1] +"')" )
    g=""
    for elm in out_g:
        g = g + elm +","
    print("global "+ g[:-1])

def siki_hyoji(atai,unit_opp = True):
    ns = globals()
    hidari = ns["e"+atai]
    migi = ns[atai]
    unit = ns[paramater_dict[atai][1]]
    if unit_opp == True:
        siki = Eq(hidari,migi*unit)
    else:
        siki = Eq(hidari,migi)
    return siki

def katamochi_bari(paramater):
    """片持ち梁の計算書ネタを作成します
    
    Arguments:
        paramater {list} -- [荷重,長さ,断面係数]
    """
    
    global σmax,Mmax,Z,F,L
    print("曲げ応力は以下の式で表される")
    σmax = Mmax/Z
    Mmax = F*L
    display(siki_hyoji("σmax",False),siki_hyoji("Mmax",False))

    print("各パラメータの値を以下に示す")
    F = paramater[0]
    L = paramater[1]
    Z = paramater[2]
    display(siki_hyoji("F"),siki_hyoji("L"),siki_hyoji("Z"))

    print("以上より")
    Mmax = F*L
    σmax = Mmax/Z
    σmax = round(σmax)
    display(siki_hyoji("Mmax"),siki_hyoji("σmax"))

if __name__ == "__main__":
    create_symbol()
    paramater = [1000,500,1609]
    katamochi_bari(paramater)