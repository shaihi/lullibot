messerd_distance_step = 5
def my_ditection():
  cordinate = 0,0
  return cordinate
  
def stopEngine():
  '''to stop the engine we will print "S"'''
  print("S")


'''
this function is going to the detected dead bird 
:inpu:cordinate for where the bird is 
:return: none
''' 
def goto_dead_bird(cordinate):
  print("detected a bird and going to it")
  #to tell the arduino we need to go we will print to the serial gt
  
  print("GT")
  print(cordinate)

  
'''
this function is changing the direction of the engine
:input: the engine direction
:return: none
'''
def change_direction(flag):
  #print("changing direction")
  if flag == "Y":
    flag = "N"
    #print(flag)
  else:
    flag = "Y"
   # print(flag)
  print("C")
  return flag

    
'''
this function is stoping imidiatly the mechin 
:input: none
:output: none
''' 
def immediate_stop():
  imidiate_stop_button = 0
  #print("checking if the imidiate button was preest")
  inpt = int(input())
  if inpt == 1:
    stopEngine()
    imidiate_stop_button = 1
  return imidiate_stop_button
'''
this function is starting the engines
:input: none
:output: none
'''
def driveRobot(flag):
  #print("sending move command to Arduino")
  print(flag)
  return 
'''
main function 
'''
def main():
  step_counter = 0
  flag = "Y"
  imd = immediate_stop()
  while  imd == 0:
    driveRobot(flag)
    if flag == "Y":
      step_counter =  step_counter + messerd_distance_step
    elif flag == "N":
      step_counter =  step_counter - messerd_distance_step
    if step_counter <= 90 and step_counter >= 0:
      print(step_counter)
    else:
      change_direction(flag)
    if detect_bird():
      goto_dead_bird()
    #else:
      #print("there are no dead birds")
    imd = immediate_stop()

if _name_ == "_main_":
  main()
