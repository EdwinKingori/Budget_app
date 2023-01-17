class Category:
  
  def __init__(self, name):
    self.name = name
    self.ledger = list()

  def __repr__(self):
    
    display_menu = self.name.center(30, '*') + '\n'
    for element in self.ledger:
        row = f"{element['description'][:23]:23}{element['amount']:7.2f}"
        display_menu += row + '\n'
    display_menu += "Total: " + str(self.get_balance())
    return display_menu
  

  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})
    
  def withdraw(self, amount, description=""):
    if (self.check_funds(amount)):
      self.ledger.append ({"amount": -amount, "description": description})
      return True; 
    return False

  def get_balance(self):
    total_amount = 0
    for i in self.ledger:
      total_amount = i["amount"] + total_amount
    return total_amount
    

  def transfer(self, amount, category):
    if (self.check_funds (amount)):
      self.withdraw(amount, "Transfer to"+ category.name)
      category.deposit(amount, "Transfer From "+ self.name)
      return True;
    return False

  def check_funds(self, amount):
    if (self.get_balance() >= amount):
      return True;
    return False
    
  def get_withdrawls(self):
    total = 0
    for item in self.ledger:
      if item["amount"] < 0:
        total+= item["amount"]
    return total

def truncate(n):
  multiplier = 10
  return int(n * multiplier) / multiplier

def getTotals(categories):
  total = 0
  breakdown = []
  for category in categories:
      total += category.get_withdrawls()
      breakdown.append(category.get_withdrawls())
    
  #Breakdown of spending rounded down to nearest 10th
  rounded = list(map(lambda x: truncate(x/total), breakdown))
  return rounded

def create_spend_chart(categories):
  res = "Percentage spent by category\n"
  i = 100
  totals = getTotals(categories)
  while i >= 0:
    cat_spaces = " "
    for total in totals:
      if total * 100 >= i:
        cat_spaces += "o  "
                #print(categories[totals.index(total)].name)
      else:
        cat_spaces += "   "
    res+= str(i).rjust(3) + "|" + cat_spaces + ("\n")
    i-=10
    
  dashes = "-" + "---"*len(categories)
  names = []
  x_axis = ""
  for category in categories:
      names.append(category.name)
  maxi = max(names, key=len)
  for x in range(len(maxi)):
    nameStr = '     '
    for name in names:
      if x >= len(name):
        nameStr += "   "
      else:
        nameStr += name[x] + "  "
    nameStr += '\n'
    x_axis += nameStr

  res+= dashes.rjust(len(dashes)+4) + "\n" + x_axis
  return res