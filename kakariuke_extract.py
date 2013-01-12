#encoding:utf-8
import sys

#このプログラムの説明-------------
#名詞-動詞の係り受けペアを取り出し、頻度の高い順でカウントと共に出力する
#名詞連続は一つの名詞としている

#説明ここまで------------------


wc={}#フレーズペアを記憶させる辞書

#形態素解析を格納する辞書
dic={}
#dic['num']={}#文節番号
dic['word']={}#単語
dic['depend']={}#係り受け先
dic['pos']={}#品詞
lst=[]#番号を格納するリスト


#関数------------------------------

#1文章における係り受けを格納するdic{}と名詞動詞の文節番号を格納するlstの初期化
def shokika(dic,lst):
  dic={}
# dic['num']={}
  dic['word']={}
  dic['depend']={}
  dic['pos']={}
  lst=[]
  return dic,lst
#EOSの時の処理
#名詞と動詞のペアを組み合わせてカウントする
def noun_verb(dic,lst,wc):
    #dic{}に格納された名詞と動詞をペアにする
    for j in lst:
      #フレーズとして結合された名詞-動詞をwc{}のカウントに加える
      #名詞、動詞以外は文節番号が割り振られないので名詞の係り受け先が動詞以外だとキーが存在しない。そのため、係り受け先のキーが存在しているかという条件が必要。 
      if dic['pos'][j]=='名詞':
        noun_depend=int(dic['depend'][j])
        if dic['pos'].has_key(noun_depend) and dic['pos'][noun_depend]=='動詞':
          pair=dic['word'][j]+'-'+dic['word'][int(noun_depend)]
          wc.setdefault(pair,0)
          wc[pair]+=1
#*の時の処理
#jとdependを取り出す
def j_depend(line):
  line=line.strip().split(' ')
  j=int(line[1])#文節番号
  depend=line[2].split('D')[0] #Dが邪魔なので文字列として読み込み取り除く 
  return j,depend


#関数ここまで-----------------------------------------



#以下ループ-----------------------------------------
#一行づつ読み込んでいき処理する
while(True):
  line=sys.stdin.readline()

  if line.startswith('*'):
    #j番目の文節、どこの文節にdependしているのかを取り出す
    j,depend=j_depend(line)
 
  elif line.startswith('EOS'):
    #名詞と動詞のペアを組み合わせカウントする
    noun_verb(dic,lst,wc)        
    #dic{}とlst[]を初期化する
    dic,lst=shokika(dic,lst)

  elif line.startswith('#'):
    continue
  
  #もう読み込むものがなければ処理を終わらせる
  elif line==(""):
    break

  #文節だったら以下の処理を行う
  else:
    line=line.strip().split('\t')
    detail=line[1].split(',')
    pos=detail[0]
    #名詞動詞以外の品詞の場合は無視
    if pos!='動詞' and pos!='名詞':
      continue
    #名詞と動詞はdic{}に格納させる
    #動詞の場合の処理--------------------------
    elif pos=='動詞':
      #dic{}に要素を追加する
      dic['pos'][j]=pos
      word=detail[4]
      dic['word'][j]=word
      dic['depend'][j]=depend
      #リストに文節番号を追加する
      lst.append(j)
      #動詞の場合の処理ここまで----------------
    #名詞の場合の処理-------------------------------------
    elif pos=='名詞':
      #名詞以外のものがくるまでwordを合成し続ける
        #dic{}に要素を追加する
        dic['pos'][j]=pos
        dic['depend'][j]=depend
        word=line[0]
        dic['word'][j]=word
        #リストに文節番号を追加する
        lst.append(j)
        #次の行を読み込み、さらに名詞が続くようならループ
        #文節でないならば適切な処理をした後にループを出る
        line=sys.stdin.readline()
        if line.startswith('#'):
          continue
        elif line.startswith('*'):
          #jとdependを格納する関数
          j,depend=j_depend(line)
        elif line.startswith('EOS'):      
          noun_verb(dic,lst,wc)
          #dic{}とlst[]を初期化する
          dic,lst=shokika(dic,lst)
        #文節が来る場合
        else:
          line=line.strip().split('\t')
          detail=line[1].split(',')
          pos=detail[0]
          while pos=='名詞':
            word=line[0]
            dic['word'][j]=dic['word'][j]+word
            line=sys.stdin.readline()
            if line.startswith('#'):
              break
            elif line.startswith('*'):        
              j,depend=j_depend(line)
              break
            elif line.startswith('EOS'):
              noun_verb(dic,lst,wc)
              #dic{}とlst[]を初期化する
              dic,lst=shokika(dic,lst)
              break
            else:
              line=line.strip().split('\t')
              detail=line[1].split(',')
              pos=detail[0]
              #名詞場合の処理ここまで-----------------------------
    
#ここの時点でwc{}に(名詞-動詞:頻度)の辞書が出来ている
for phrase,count in sorted(wc.items(),key=lambda x:x[1], reverse=True):
  print phrase,count
