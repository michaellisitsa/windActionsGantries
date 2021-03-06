#%%
import math
from bisect import bisect_right

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

def inputTerrainIh(z):
    '''Input Terrain Category, validate its input and output an interpolated graph for Turbulence intensity

    Parameters:
    None

    Returns (in this order):
    Iz: Returning Value
    '''
    while True:
        h_vals = [0.,5.,10.,15.,20.,30.,40.,50.,75.,100.,150.,200.]
        intensity = [[.165,.165,.157,.152,.147,.140,.133,.128,.118,.108,.095,.085],
                            [.196,.196,.183,.176,.171,.162,.156,.151,.140,.131,.117,.107],
                            [.271,.271,.239,.225,.215,.203,.195,.188,.176,.166,.150,.139],
                            [.342,.342,.342,.342,.342,.305,.285,.270,.248,.233,.210,.196]]
        userInput = input("Terrain Category as per Table 6.1 (1 to 4) : ")
        if userInput.isdigit() and 1 <= int(userInput) <= 4:
            if int(userInput) == 1:
                interp = Interpolate(h_vals,intensity[0])
                return interp(z)
            elif int(userInput) == 2:
                interp = Interpolate(h_vals,intensity[1])
                return interp(z)
            elif int(userInput) == 3:
                interp = Interpolate(h_vals,intensity[2])
                return interp(z)
            elif int(userInput) == 4:
                interp = Interpolate(h_vals,intensity[3])
                return interp(z)
        print("Value entered is not an integer between 1 and 4. Try Again")

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

def inputPrintYesNo(message,string):
    '''Input y [yes] or n [no] and if yes, print out intermediate values in calculation'''
    while True:
        userInput = input(message)
        if userInput == "y":
            return string
        elif userInput == "n":
            return None
        print("Value entered is not \"y\" or \"n\". Try Again")

def inputDampingAS():
    '''Input ULS/SLS and type of structure, validate its input and return Damping Factor delta2

    Parameters:
    None

    Returns (in this order):
    delta_2 : Logarithmic decrement of structural damping in the fundamental mode
    '''
    while True:
        userInput = input("Input structural type and case for damping calculations AS1170 Cl6.2.2\n\
            1=[steel ULS] 2=[steel SLS deflection] 3=[steel SLS acceleration]\n\
                4=[concrete ULS] 5=[concrete SLS deflection] 6=[concrete SLS acceleration]\n\
                7=[Enter number...] : ")
        if userInput.isdigit() and 1 <= int(userInput) <= 7:
            if int(userInput) == 1:
                return 0.02
            elif int(userInput) == 2:
                return 0.012
            elif int(userInput) == 3:
                return 0.01
            elif int(userInput) == 4:
                return 0.03
            elif int(userInput) == 5:
                return 0.015
            elif int(userInput) == 6:
                return 0.01
            elif int(userInput) == 7:
                return inputNumber("Please enter a structural damping factor [0 to 0.3 typ] : ")
        print("Value entered is not an integer between 1 and 7. Try Again")

#Linear interpolation function to get value at a point given a set of x and y points
class Interpolate:
    def __init__(self, x_list, y_list):
        if any(y - x <= 0 for x, y in zip(x_list, x_list[1:])):
            raise ValueError("x_list must be in strictly ascending order!")
        self.x_list = x_list
        self.y_list = y_list
        intervals = zip(x_list, x_list[1:], y_list, y_list[1:])
        self.slopes = [(y2 - y1) / (x2 - x1) for x1, x2, y1, y2 in intervals]

    def __call__(self, x):
        if not (self.x_list[0] <= x <= self.x_list[-1]):
            raise ValueError("x out of bounds!")
        if x == self.x_list[-1]:
            return self.y_list[-1]
        i = bisect_right(self.x_list, x) - 1
        return self.y_list[i] + self.slopes[i] * (x - self.x_list[i])



# %%
class wind_calcs:
    def __init__(self,z,b,h,n,vb,cf):
        self.z = z
        self.b = b
        self.h = h
        self.n = n
        self.vb = vb
        self.cf = cf
        self.ro = 1.25 #kg/m3 air density

    def EN1991(self,z0,zmin,delta_s,mass):
        self.z0 = z0
        self.zmin = zmin
        self.delta_s = delta_s
        self.mass = mass

        #Mean Wind Speed
        self.c0 = 1 # Sec 4.3.3 assumed, as upwind slope typically < 3 degrees
        z0ii = 0.05 #Sec 4.3.2
        self.kr = 0.19 * (z0 / z0ii)**0.07 # Eq 4.5
        self.cr = self.kr * math.log(max(zmin, self.z) / z0) #Cl 4.3.1 Terrain Roughness
        self.vm = self.cr * self.c0 * self.vb #Eq 4.3

    def cd_cs(self,z_s):

        #Sec 4.4 Iv(z) The turbulence intensity at height z is 
        #defined as the Standard Deviation of the turbulence divided 
        #by the wind velocity
        kl = 1.0 # Sec 4.4(1) assumed
        Iv = kl / (self.c0 * math.log(self.z / self.z0))

        #Sec B.1 (1) Wind Turbulence
        zt = 200 #(m) Reference Height
        Lt = 300 #(m) Reference Length
        alpha = 0.67 + 0.05 * math.log(self.z0)
        L = Lt * (max(self.zmin, self.z)/ zt)**alpha

        #Sec B.1 (2) Wind Distribution over frequencies - Power spectral function
        fL = self.n*L/self.vm
        SL = 6.8 * fL/(1 + 10.2 * fL)**(5/3)

        # F.5 Logarithmic decrement of damping
        delta_d = 0 #Assumed no special damping devices
        dens_air = 1.25 #(kg/m3)
        delta_a = self.cf * dens_air * self.vm / (2 * self.n * self.mass/self.h)
        delta = delta_s + delta_a + delta_d

        # B.2 Structural Factors
        B2 = 1 / (1 + 0.9 * ((self.b + self.h) / L)**0.63) #Eq B.3 Background Factor allow lack full pressure correlation
        nh = 4.6 * self.h * fL / L
        nb = 4.6 * self.b * fL / L
        Rh = 1/nh - 1/(2*nh**2) * (1 - math.exp(-2*nh)) #Eq B.7 Aerodynamic admittance function (h)
        Rb = 1/nb - 1/(2*nb**2) * (1 - math.exp(-2*nb)) #Eq B.8 Aerodynamic admittance function (b)
        R2 = math.pi**2 * SL * Rh * Rb / (2 * delta) #Eq B.6 Resonance response Factor
        v = self.n * math.sqrt(R2/(B2+R2)) #(Hz) Eq B.5 Up-crossing Frequency
        T = 600 #(s) Eq B.4 Averaging time for mean wind velocity
        kp = max(math.sqrt(2 * math.log(v * T)) + 0.6 / math.sqrt(2 * math.log(v * T)),3)
        cs = (1 + 7 * Iv * math.sqrt(B2)) / (1 + 7 * Iv) #size factor
        cd = (1 + 2 * kp * Iv * math.sqrt(B2 + R2)) / (1 + 7 * Iv * math.sqrt(B2)) #dynamic factor
        cs_cd = (1 + 2 * kp * Iv * math.sqrt(B2 + R2))/ (1 + 7 * Iv) #combined size and dynamic factor
        print(f'The structural factor is:\n'
        f'cs_cd = {cs_cd:3.2f}:\n'
        f'cs = {cs:7.2f}\n'
        f'cd = {cd:7.2f}')

        # Ask user whether intermediate results are required:
        print(inputPrintYesNo("Do you want to see the intermediate values? y = [YES] n = [NO]: ",
                            f'TURBULENCE, SPECTRAL FUNC & DAMPING\n'
                            f'kr={self.kr:10.2f}\n'
                            f'cr={self.cr:10.2f}\n'
                            f'vm={self.vm:10.2f}\n'
                            f'Iv={Iv:10.2f}\n'
                            f'alpha={alpha:7.2f}\n'
                            f'L={L:11.2f}\n'
                            f'fL={fL:10.2f}\n'
                            f'SL={SL:10.2f}\n'
                            f'delta_s={self.delta_s:5.2f}\n'
                            f'delta_a={delta_a:5.2f}\n\n'
                            f'STRUCTURAL FACTORS INPUTS:\n'
                            f'B2={B2:10.2f}\n'
                            f'nh={nh:10.2f}\n'
                            f'nb={nb:10.2f}\n'
                            f'Rh={Rh:10.2f}\n'
                            f'Rb={Rb:10.2f}\n'
                            f'R2={R2:10.2f}\n'
                            f'v={v:11.2f}\n'
                            f'T={T:11.2f}\n'
                            f'kp={kp:10.2f}'))

    def Vortex(self,d):
        b = self.h #height of beam variable definition
        l = self.b #Length of beam variable redefinition
        #Read Graph of Strouhal Number Table E.1 EN1991.1.4
        db_vals = [0,1,2,3,4,5,10]
        St_vals = [.12,.12,.06,.06,.15,.11,.09]
        interp = Interpolate(db_vals,St_vals)
        St = interp(d/b)

        #Critical Wind Velocity vcrit,i
        vcrit = b * self.n / St

        #Scruton Number [Ratio structural mass to fluid mass]
        #The ability of the structure to absorb and dissipate the energy
        #from vortex shedding depends on the structural damping
        Sc = 2 * self.delta_s * self.mass / (self.ro * b**2)

        #Reynolds Number
        v = 15 * 10**-6 #m2/s kinematic velocity of air
        Re = b * vcrit / v

        #Vortex Shedding Action
        #APPROACH 1
        K = 0.1 #Table E.5 for simply supported structure
        #Correlation Length E 1.5.2.3
        #clat Calculations Table E.2 & E.3
        clat0 = 1.1
        if vcrit_ratio := vcrit/self.vm <= 0.83:
            clat = clat0
        elif vcrit_ratio <= 1.25:
            clat = (3 - 2.4 * vcrit_ratio) * clat0
        else:
            clat = 0
        
        #TODO - Check whether manually collating mode shape factors is needed in certain structures
        #Refer Table E.5 for n and m mode shape factors
        #Refer Table F.1 for phi.iy.s

        #Calculate correlation lenght factor on assumption of Lj length.
        Lj_div_b =  6.0 #TODO CHECK assumption. Based on Sigmund spreadsheets example 30-G
        lamda = l / b
        Kw = min(math.cos(math.pi / 2 * (1 - (Lj_div_b) / lamda)),0.6)
        #Max displacement over time of the point with phi_iy = 1
        Yfmax = b * (1 / St**2) * (1 / Sc) * K * Kw * clat #E.7

        #Inertia force per unit length
        phi_iys = 1 #at midspan normalised
        Fw = self.mass * (2 * math.pi * self.n)**2 * phi_iys * Yfmax

        print(f"The maximum displacement over time of a point with phi_iy = 1 is:\n"
            f"Yfmax={Yfmax:7.3f} m\n"
            f"The inertia force per unit length at distance s along beam [taken as midspan] is:\n"
            f"Fw={Fw:10.0f} N/m")

        # Ask user whether intermediate results are required:
        print(inputPrintYesNo("Do you want to see the intermediate values? y = [YES] n = [NO]: ",
                            f'delta_s={self.delta_s:5.2f}\n'
                            f'kr={self.kr:10.2f}\n'
                            f'cr={self.cr:10.2f}\n'
                            f'vm={self.vm:10.2f}\n'
                            f'St={St:10.2f}\n'
                            f'vcrit={vcrit:7.2f}\n'
                            f'Sc={Sc:10.2f}\n'
                            f'Re={Re:10.0f}\n'
                            f'K={K:11.2f}\n'
                            f'clat0={clat0:7.2f}\n'
                            f'clat={clat:8.2f}\n'
                            f'lamda={lamda:7.2f}\n'
                            f'Kw={Kw:10.2f}'))

    def Cdyntower(self,Ih,bsh,Vdes,delta2):
        # Convert values from EN terminology to AS1170
        s = self.z
        h2 = self.z
        gv = 3.4
        na = self.n

        #Background Factor Eq 6.2(2)
        Lh = 85 * (h2 / 10)**0.25
        Bs = 1 / (1 + math.sqrt(0.26 * (h2 - s)**2 + 0.46 * bsh**2) / Lh)

        #Height and Peak Factors for the response
        Hs = 1 + (s / h2)**2
        gR = math.sqrt(1.2 + 2 * math.log(600 * na))

        #Size Reduction Factor Eq6.2(5)
        N = na * Lh * (1 + gv * Ih) / Vdes
        S = 1 / ((1 + 3.5 * na * h2 * (1 + gv * Ih) / Vdes) * (1 + 4 * na * bsh * (1 + gv * Ih) / Vdes))

        #Dynamic Factor
        Et = math.pi * N / (1 + 70.8 * N**2)**(5 / 6)
        Cdyn = (1 + 2 * Ih * math.sqrt(gv**2 * Bs + Hs * gR**2 * S * Et / delta2)) / (1 + 2 * gv * Ih)

        print(f'The Cdyn Dynamic factor is:\n'
        f'Cdyn = {Cdyn:9.2f}')
        
        # Ask user whether intermediate results are required:
        print(inputPrintYesNo("Do you want to see the intermediate values? y = [YES] n = [NO]: ",
                            f'Ih={Ih:10.2f}\n'
                            f'delta2={delta2:6.2f}\n'
                            f's={s:11.2f}\n'
                            f'gv={gv:10.2f}\n'
                            f'n={na:11.2f}\n'
                            f'Lh={Lh:10.2f}\n'
                            f'Bs={Bs:10.2f}\n'
                            f'Hs={Hs:10.2f}\n'
                            f'gR={gR:10.2f}\n'
                            f'N={N:11.2f}\n'
                            f'S={S:11.2f}\n'
                            f'Et={Et:10.2f}\n'))

#%%
func = wind_calcs(z := inputNumber("Enter the height above ground 'z' in metres : "),
                inputNumber("Length of Beam perpendicular to the wind 'b' in metres : "),
                inputNumber("Height of beam 'h' in metres : "),
                inputNumber("Natural Frequency 'n' in Hz : "),
                inputNumber("Mean Wind speed 10 min ave [refer Durst Curve for conversion from 3s] 'vb' in m/s: "),
                inputNumber("Aerodynamic shape factor 'cf' : "))

if inputPrintYesNo("\nConduct EN1991.1.4 calculations y = [Yes] n = [No] : ",True):
    func.EN1991(inputTerrain()[0],
            inputTerrain()[1],
            delta_s := inputConnecType(),
            mass := inputNumber("Enter the mass per unit metre of beam at the mid-span 'mass' in kg/m : "))

    if inputPrintYesNo("\nConduct cd_cs calculation AnnB EN1991.1.4 [applies to cantilevers / beams with constant sign]\n\
        y = [YES] n = [NO] : ",True):
        func.cd_cs(inputNumber("Reference Height for determining structural factor 'z_s' in metres : "))

    if inputPrintYesNo("\nConduct Vortex Shedding Calculation as per EN1991.1.4 [simply supported beams only]\n\
        y = [YES] n = [NO] : ",True):
        func.Vortex(inputNumber("Horizontal width of section 'd' in metres : "))

if inputPrintYesNo("\nConduct Cdyn calculation Sec6 AS1170.2 [applies to cantilever structures with even mass distribution]\n\
     y = [YES] n = [NO] : ",True):
    func.Cdyntower(inputTerrainIh(z),
            inputNumber("What is the average breadth of the cantilever structure 'bsh' and 'b0h' in metres : "),
            inputNumber("What is the wind gust speed for a 0.2s interval as per AS1170.2 Cl 2.3 in m/s : "),
            inputDampingAS())   

input("Press Any Key to Exit!")