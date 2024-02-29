import random
class Card:
  def __init__(self,suit=0):
    self.suit=suit
  suit_names=['Padda','Karta','Fluga','Sporðdreki','Könguló','Kakkalakki','Rotta','Leðurblaka']

  def __str__(self):
    #Finn tegund með kvóta
    return '%s' % (Card.suit_names[self.suit//8])

  def __eq__(self,other):
    if str(self) == str(other): return True
    else: return False

  def __lt__(self,other):
    if self.suit<other.suit: return True

    return False

class Deck:
  def __init__(self):
    self.cards=[]
    for suit in range(64):
      card=Card(suit)
      self.cards.append(card)

  def __str__(self):
    res=[]
    for card in self.cards:
      res.append(str(card))
    return '\n'.join(res)

  def pop_card(self):
    return self.cards.pop()

  def remove_card(self,other):
    #Léleg aðferð kannski hægt að bæta
    for card in self.cards:
      if str(card)==str(other): return self.cards.remove(card)
    print('Spil er ekki í stokknum')
    return

  def add_card(self,suit):
    self.cards.append(suit)

  def shuffle(self):
    random.shuffle(self.cards)

  def move_cards(self,hand,num):
    for i in range(num):
      hand.add_card(self.pop_card())

  def __contains__(self,other):
    for card in self.cards:
      if str(card)==str(other): return True
    return False

  def sort(self):
    no=[]
    for card in self.cards: no.append(card.suit)
    no.sort()
    return [Card(i) for i in no]

  def __len__(self):
    return len(self.cards)
  
def gefa(num_players):

  players=[None]*num_players
  #bua til stokk
  stokkur=Deck()
  stokkur.shuffle()
  
  leikmenn_dict={}

  for i in range(num_players):
    nafn=input('Nafn leikmanns:')
    players[i]=(Hand(nafn),Hand(nafn+'_uti'))
    leikmenn_dict[nafn]=[players[i][0],players[i][1]]
    stokkur.move_cards(players[i][0],64//num_players) # gefa spil
    ertolva=input('Er tölvan að spila fyrrnefnda leikmann? (Já/Nei)')
    if ertolva=='Já': players[i][0].tolva=1
    else: players[i][0].tolva=0
  if 64&num_players!=0:
    for j in range(64%num_players):
      stokkur.move_cards(players[j][0],1)
  return players,leikmenn_dict

def hefurtapad(leikmadur):
  #nota væntanlega bara dictionary til að halda telja fjölda sorta sem leikmadur hefur
  spilabordi={}
  for card in leikmenn[leikmadur][1].cards:
    if str(card) in spilabordi:
      spilabordi[str(card)]+=1
      if spilabordi[str(card)]==4:
        print(leikmadur+' er með fjögur eins spil! Þú varst '+endir(card)+'!')
        return False
    else:
      spilabordi[str(card)]=1
      if len(spilabordi)==8:
        print(leikmadur+' er með eitt af hverri sort og tapar!')
        return False
  return True

def endir(card):
  if str(card)[-1]=='a': return str(card)+'ður'
  if str(card)[-1]=='i': return str(card)[:-1]+'aður'
  else: return str(card)+'aður'

def lausir(players,tolva):
  free=[]
  if tolva==1:
    for i in players:
      if i[0].tag==0: free.append(i[0].label)
    return free
  else:
    for i in players:
      if i[0].tag==1: print(' *'+i[0].label+'* ',end='')
      else: print(' '+i[0].label+' ',end='')
    print()
    return None
  
def umferd(target,spil,giver,cnt,fj):
  #target og giver eru strengir (nöfn) ekki hand objects!
  #spil er listi, spil[0] er raunverulega spilið og spil[1] er það sem giver segir að það sé
  #target er manneskja sem fær spilið, giver er manneskja sem gefur
  #ef allir nema einn hafa seð spilið verur viðkomandi að giska
  if cnt==fj-1:
    gisk=input(target+' er síðasti leikmaður! Er spilið '+str(spil[1])+' eins og '+giver+' segir? (Já/Nei)')
    return rett_rangt(gisk,target,giver)
  else:
    prentabord(players)
    akvordun=input(target + ' fékk '+str(spil[1])+' frá '+giver+ '. Hvað viltu gera? (Giska/Gefa)')
    leikmenn[target][0].tag=1
    if akvordun=='Gefa':
      cnt+=1
      print('Þú skoðar spilið og sérð að það er '+str(spil[0]))
      lausir(players,leikmenn[target][0].tolva)
      targetnew=input('Hverjum viltu gefa spilið?')
      #athuga hvort leikmaður megi fa spilið
      while(leikmenn[targetnew][0].tag==1):
        print('Þessi leikmaður hefur þegar séð spilið!')
        targetnew=input('Hverjum viltu gefa spilið?')

      spil[1]=Card(flokkar[input('Hvað viltu segja að spilið sé?')])
      leikmenn[targetnew][0].tag=1
      if leikmenn[targetnew][0].tolva==0: return umferd(targetnew,spil,target,cnt,fj)
      else: return tolvaumferd(targetnew,spil,target,cnt,fj)
    else:
      gisk=input('Er spilið '+str(spil[1])+' eins og '+giver+' segir? (Já/Nei)')
      return rett_rangt(gisk,target,giver)
    

def rett_rangt(gisk,target,giver):
  if gisk=='Já':
    if spil[0]==spil[1]:
      print('Spilið var '+str(spil[0])+'! '+giver+' fær spilið!')
      leikmenn[giver][1].add_card(spil[0])
      return hefurtapad(giver)
    else:
      print('Spilið var '+str(spil[0])+'! '+target+' fær spilið!')
      leikmenn[target][1].add_card(spil[0])
      return hefurtapad(target)
  else:
    if spil[0]!=spil[1]:
      print('Spilið var '+str(spil[0])+', ekki '+str(spil[1])+'! '+giver+' fær spilið!')
      leikmenn[giver][1].add_card(spil[0])
      return hefurtapad(giver)
    else:
      print('Spilið var '+str(spil[0])+'! '+target+' fær spilið!')
      leikmenn[target][1].add_card(spil[0])
      return hefurtapad(target)
    
def prentabord(players):
  #players er listinn af tuples með öllum leikmönnum
  #lengstu spilin eru 10 bókstafir
  lina=''
  bunkar=[None]*len(players)
  for i in range(len(players)):
    bunkar[i]=players[i][1].sort()
    if i!=len(players)-1:
      lina+=players[i][0].label+' '*max(10-len(players[i][0].label),len(players[i][0].label))+'|'
      print(players[i][0].label+' '*max(10-len(players[i][0].label),len(players[i][0].label))+'|',end='')
    else:
      lina+=players[i][0].label+' '*max(10-len(players[i][0].label),len(players[i][0].label))
      print(players[i][0].label+' '*max(10-len(players[i][0].label),len(players[i][0].label)))
  print('-'*len(lina))
  lina_listi=lina.split('|')
  lina_listi=[len(i) for i in lina_listi] #lengd dálka
  #nu þarf að prenta spilin sjálf sem eru á borðinu
  #kannski er best að sorta hvern bunka (0->63), gera svo lista af listum og prenta út
  #sort aðferðin í Deck() skilar lista röðuðum (0->63) Card() objects
  #bunkar er búið til og höndum raðað að ofan
  max_bunki=max([len(i) for i in bunkar])
  for i in bunkar:
    if len(i)<max_bunki: 
      for j in range(max_bunki-len(i)):
        i.append(-1)
  for j in range(max_bunki):
    cnt=0
    for i in bunkar:
      if cnt==len(players)-1:
        if i[j]==-1: 
          print(' '*lina_listi[cnt])
          cnt+=1
        else:
          print(str(i[j])+' '*(lina_listi[cnt]-len(str(i[j]))))
          cnt+=1
      else:
        if i[j]==-1: 
          print(' '*lina_listi[cnt]+'|',end='')
          cnt+=1
        else:
          print(str(i[j])+' '*(lina_listi[cnt]-len(str(i[j])))+'|',end='')
          cnt+=1
  print('-'*len(lina))

def tolvaumferd(target,spil,giver,cnt,fj):
  gisk_moguleikar=['Já','Nei']
  akvordun_moguleikar=['Giska','Gefa']
  if cnt==fj-1:
    gisk=gisk_moguleikar[random.randint(0,1)]
    if gisk=='Já': print(target+' fékk spil frá '+giver+' og giskar að það sé '+str(spil[1])+'!')
    else: print(target+' fékk spil frá '+giver+' og giskar að það sé ekki '+str(spil[1])+'!')
    return rett_rangt(gisk,target,giver)
  else:
    akvordun=akvordun_moguleikar[random.randint(0,1)]
    leikmenn[target][0].tag=1
    if akvordun=='Gefa':
      cnt+=1
      available=lausir(players,leikmenn[target][0].tolva)
      targetnew=random.choice(available)
      spil[1]=Card(random.randint(0,63))
      print(target+' skoðar spilið, segir að það sé '+str(spil[1])+' og gefur '+targetnew)
      leikmenn[targetnew][0].tag=1
      if leikmenn[targetnew][0].tolva==0: return umferd(targetnew,spil,target,cnt,fj)
      else: return tolvaumferd(targetnew,spil,target,cnt,fj)
    else:
      gisk=gisk_moguleikar[random.randint(0,1)]
      if gisk=='Já': print(target+' fékk '+str(spil[1])+' frá '+giver+' og giskar að það sé '+str(spil[1])+'!')
      else: print(target+' fékk '+str(spil[1])+' frá '+giver+' og giskar að það sé ekki '+str(spil[1])+'!')
      return rett_rangt(gisk,target,giver)

def kakkalakkapoker():
  game=True
  num_players=int(input('Hversu margir eru leikmennirnir?'))
  global players,leikmenn
  players,leikmenn=gefa(num_players)
  global flokkar
  flokkar={'Padda':0,'Karta':8,'Fluga':16,'Sporðdreki':24,'Könguló':32,'Kakkalakki':40,'Rotta':48,'Leðurblaka':56}
  while(game):
    for i in range(num_players):
      prentabord(players)
      for j in range(num_players):
        players[j][0].tag=0
      if players[i][0].tolva==1:
        print(players[i][0].label+' á að gera!')
        tolva_spil=[]
        for card in players[i][0].cards: tolva_spil.append(card.suit)
        spil_gefa=Card(random.choice(tolva_spil))
        players[i][0].remove_card(spil_gefa)
        players[i][0].tag=1
        available=lausir(players,players[i][0].tolva)
        target=random.choice(available)
        spil_segja=Card(random.randint(0,63))

        cnt=1
        global spil
        spil=[spil_gefa,spil_segja]
        print(players[i][0].label+' gefur '+target+' spil og segir að það sé '+str(spil[1]))
        #leikmenn er dictionary sem er nafn->hand object (spil á hendi) (28.1.23)
        if leikmenn[target][0].tolva==1: game=tolvaumferd(target,spil,players[i][0].label,cnt,num_players)
        else: game=umferd(target,spil,players[i][0].label,cnt,num_players)
        if not game: break
      else:
        print(players[i][0].label+' á að gera!')
        for j in players[i][0].sort(): print(str(j))
        spil_gefa=Card(flokkar[input('Hvaða spil viltu gefa?')])
        #ath. hvort leikmaður se með spilið
        while spil_gefa not in players[i][0]: spil_gefa=Card(flokkar[input('Þú ert ekki með svona spil! Hvaða spil viltu gefa?')])
        players[i][0].remove_card(spil_gefa)
        players[i][0].tag=1
        available=lausir(players,players[i][0].tolva)
        target=input('Hverjum viltu gefa spilið?')
        spil_segja=Card(flokkar[input('Hvað viltu segja að spilið sé?')])

        cnt=1
        spil=[spil_gefa,spil_segja]
        if leikmenn[target][0].tolva==1: game=tolvaumferd(target,spil,players[i][0].label,cnt,num_players)
        else: game=umferd(target,spil,players[i][0].label,cnt,num_players)
        if not game: break
    prentabord(players)

if __name__ == "__main__":
  kakkalakkapoker()