#%%
import math

#%%
def inputNumber(message):
    '''Input Value and check if it is a number

    Parameters:
    arg (str): Message to display on input

    InputParameter:
    Positive non-zero Number
    
    Returns:
    int:Returning Value
    '''
    while True:
        try:
            userInput = float(input(message))
            if userInput <= 0:
                raise ValueError()
        except ValueError:
            print("This is not a positive non-zero number! Try Again")
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
        userInput = input("Terrain Category as per Table 4.1 (0 to 4) : ")
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
        print("Value entered is not an integer between 0 and 4. Try Again")

def inputConnecType():
    '''Input Connection Type, validate its input and return Damping Factor delta_s

    Parameters:
    None

    Returns (in this order):
    delta_s : Logarithmic decrement of structural damping in the fundamental mode
    '''
    while True:
        userInput = input("Primary plate connections perpendicular to longitudinal axis for Damping\n\
            1=[welded] 2=[high resistance bolts] 3=[ordinary bolts] 4=[Enter number...] : ")
        if userInput.isdigit() and 1 <= int(userInput) <= 4:
            if int(userInput) == 1:
                return 0.02
            elif int(userInput) == 2:
                return 0.03
            elif int(userInput) == 3:
                return 0.05
            elif int(userInput) == 4:
                return inputNumber("Please enter a structural damping factor [0 to 0.15 typ] : ")
        print("Value entered is not an integer between 1 and 3. Try Again")

# %%
#Ask for input
z = inputNumber("Enter the height above ground 'z' in metres : ")
z_s = inputNumber("Reference Height for determining structural factor 'z_s' in metres : ")
b = inputNumber("Length of Beam perpendicular to the wind 'b' in metres : ")
h = inputNumber("Height of beam 'h' in metres : ")
n = inputNumber("Natural Frequency of TODO: DET VERT/HORIZ bending frequency 'n' in Hz : ")
vb = inputNumber("Basic Wind speed 'vb' in m/s: ")
z0, zmin = inputTerrain()
mass = inputNumber("Enter the mass per unit area of beam at the mid-span 'mass' in kg/m : ")
cf = inputNumber("Aerodynamic shape factor 'cf' : ")
delta_s = inputConnecType()

# %%
# Mean Wind
c0 = 1.0 # Sec 4.3.3 assumed, as upwind slope typically < 3 degrees
z0ii = 0.05 #Sec 4.3.2
kr = 0.19 * (z0 / z0ii)**0.07 # Eq 4.5
cr = kr * math.log(max(zmin, z) / z0) #Cl 4.3.1 Terrain Roughness
vm = cr * c0 * vb #Eq 4.3

#%%
#Sec 4.4 Iv(z) The turbulence intensity at height z is 
#defined as the Standard Deviation of the turbulence divided 
#by the wind velocity
kl = 1.0 # Sec 4.4(1) assumed
Iv = kl / (c0 * math.log(z / z0))

#%%
#Sec B.1 (1) Wind Turbulence
zt = 200 #(m) Reference Height
Lt = 300 #(m) Reference Length
alpha = 0.67 + 0.05 * math.log(z0)
L = Lt * (max(zmin, z)/ zt)**alpha

# %%
#Sec B.1 (2) Wind Distribution over frequencies - Power spectral function
fL = n*L/vm
SL = 6.8 * fL/(1 + 10.2 * fL)**(5/3)

#%%
# F.5 Logarithmic decrement of damping
delta_d = 0 #Assumed no special damping devices
dens_air = 1.25 #(kg/m3)
delta_a = cf * dens_air * vm / (2 * n * mass)
delta = delta_s + delta_a + delta_d

# %%
# B.2 Structural Factors
B2 = 1 / (1 + 0.9 * ((b + h) / L)**0.63) #Eq B.3 Background Factor allow lack full pressure correlation
nh = 4.6 * h * fL / L
nb = 4.6 * b * fL / L
Rh = 1/nh - 1/(2*nh**2) * (1 - math.exp(-2*nh)) #Eq B.7 Aerodynamic admittance function (h)
Rb = 1/nb - 1/(2*nb**2) * (1 - math.exp(-2*nb)) #Eq B.8 Aerodynamic admittance function (b)
R2 = math.pi**2 * SL * Rh * Rb / (2 * delta) #Eq B.6 Resonance response Factor
v = n * math.sqrt(R2/(B2+R2)) #(Hz) Eq B.5 Up-crossing Frequency
T = 600 #(s) Eq B.4 Averaging time for mean wind velocity
kp = max(math.sqrt(2 * math.log(v * T)) + 0.6 / math.sqrt(2 * math.log(v * T)),3)
cs = (1 + 7 * Iv * math.sqrt(B2)) / (1 + 7 * Iv) #size factor
cd = (1 + 2 * kp * Iv * math.sqrt(B2 + R2)) / (1 + 7 * Iv * math.sqrt(B2)) #dynamic factor
cs_cd = (1 + 2 * kp * Iv * math.sqrt(B2 + R2))/ (1 + 7 * Iv) #combined size and dynamic factor
print(f'The structural factor is:\n'
f'cs_cd = {cs_cd:3.2f}:\n'
f'cs = {cs:7.2f}\n'
f'cd = {cd:7.2f}')