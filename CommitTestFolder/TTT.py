grid = [[" "," "," "],[" "," "," "],[" "," "," "]]
def victoryCheck(grid): 
  for i in grid: 
    if i[0]==i[1]==i[2] and i[0] != " ": 
      return i[0]
  for i in range(3): 
    if grid[0][i]==grid[1][i]==grid[2][i] and grid[0][i]!=" ": 
      return grid[0][i]
  if grid[0][2]==grid[1][1]==grid[2][0] and grid[1][1]!=" ": 
    return grid[1][1]
  if grid[0][0]==grid[1][1]==grid[2][2] and grid[1][1]!=" ": 
    return grid[1][1]
  return None
for i in grid: 
    print(i)
while 1: 
  p1guess = int(input("Enter a number 1-9: "))
  grid[(p1guess-1)//3][(p1guess-1)%3] = "X"
  for i in grid: 
    print(i)
  if victoryCheck(grid) == "X": 
    print("Player 1 won!")
    break
  full = True
  for i in range(3): 
    for j in range(3): 
      if grid[i][j] == " ": 
        full = False
  if full == True: 
    print("Tie!")
    break
  
  p2guess = int(input("Enter a number 1-9: "))
  grid[(p2guess-1)//3][(p2guess-1)%3] = "O"
  for i in grid: 
    print(i)
  if victoryCheck(grid) == "O": 
    print("Player 2 won!")
    break