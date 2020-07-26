#%%
def inputNumber(message):
    '''Input Value and check if it is a number

    Parameters:
    arg (str): Message to display on input
    
    Returns:
    int:Returning Value
    '''
    while True:
        try:
            userInput = float(input(message))
        except ValueError:
            print("This is not a number! Try Again")
            continue
        else:
            return userInput
            break

# %%
def inputTerrain():
    '''Input Terrain Category, validate its input and return z0 and zmin

    Parameters:
    None

    Returns (in this order):
    z0: Returning Value
    zmin: Returning Value
    '''
    while True:
        userInput = input("Terrain Category as per Table 4.1 (0 to 4):")
        if userInput.isdigit() and 0 <= int(userInput) <= 4:
            if int(userInput) == 0:
                return 0.003, 1
            elif int(userInput) == 1:
                return 0.01, 1
            elif int(userInput) == 2:
                return 0.05, 2
            elif int(userInput) == 3:
                return 0.3, 5
            elif int(userInput) == 4:
                return 1, 10
        print("Value entered is not an integer between 0 and 4")

inputTerrain()
# %%
#Ask for input
z = inputNumber("Enter the height above ground 'z' in metres:")
z_s = inputNumber("Reference Height for determining structural factor 'z_s' in metres:")
b = inputNumber("Length of Beam perpendicular to the wind 'b' in metres:")
h = inputNumber("Height of beam 'h' in metres:")
n = inputNumber("Natural Frequency of TODO: DET VERT/HORIZ bending frequency 'n' in Hz)
z0, zmin = inputTerrain()
#%%
'''Sec 4.4 Iv(z) The turbulence intensity at height z is 
defined as the Standard Deviation of the turbulence divided 
by the wind velocity
Assumptions:
kl = 1.0 : Sec 4.4(1)'''
