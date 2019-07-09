import pandas as pd
import re

def create_symbol(paramater_dict):
    """パラメータ辞書をインプットとして、sympyのシンボルを作成します

    Arguments:
        paramater_dict {dict} -- "シンボル名"：["パラメータ名","単位"]
    """
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
