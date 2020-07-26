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
#Ask for input
z = inputNumber("Enter the height above ground 'z' in metres:")
z_s = inputNumber("Reference Height for determining structural factor 'z_s' in metres:")
b = inputNumber("Length of Beam perpendicular to the wind 'b' in metres:")
h = inputNumber("Height of beam 'h' in metres:")

# %%
