from sympy import Symbol,pi,Eq
from IPython.display import display
from sympy.interactive import printing
printing.init_printing(use_latex=True)

import utility

#使用するシンボルはグローバルで定義
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

#使用するパラメータ（utilityを使って、これからシンボルを作る）
paramater_dict= {
    "σmax":["曲げ応力","MPa"],
    "Mmax":["曲げモーメント","N_mm"],
    "Z":["断面係数","mm3"],
    "F":["荷重","N"],
    "L":["梁の長さ","mm"]
    }

def create_symbols():
    global paramater_dict
    utility.create_symbol(paramater_dict)

def siki_hyoji(atai,unit_opp = True):
    """sympyで式を表示する関数です
    　　（ a = b [mm]　の形で返す）
    Arguments:
        atai {str} -- パラメータ名
    
    Keyword Arguments:
        unit_opp {bool} -- 単位の表示有無 (default: {True}単位を表示する)
    
    Returns:
        [sympy] -- sympyの式をかえします
    """
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
    """片持ち梁の計算書ネタを作成します[荷重,長さ,断面係数]
    
    Arguments:
        paramater {list} -- [荷重,長さ,断面係数]
    """
    
    global σmax,Mmax,Z,F,L #global変数を編集可能にする
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
    create_symbols()
    paramater = [1000,500,1609]
    katamochi_bari(paramater)