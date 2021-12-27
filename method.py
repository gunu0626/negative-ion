from const import *
import numpy as np
from scipy.optimize import fsolve
from scipy.special import erfc

class iterative():
    ### Private method ####     
    def __init__(self, ne, Te, V_sat, I_sat, V_p):
        Tm = 0.1
        self.ne = ne
        self.Te = Te
        self.V_sat = V_sat
        self.I_sat = I_sat
        self.gamma = self.Te/Tm
        self.V_p = V_p
        self.De = np.sqrt(epsilon_0*kB*Te/(e**2*ne)) #electron debye length
        #print("ne : {:.2e}, Te : {}, V_sat : {}, I_sat : {:.2e}".format(ne,Te,V_sat,I_sat))
       
    def __cal_alpha(self,a_0):
        def alpha_s_eqn(a_s):
            return a_0 - a_s*np.exp(-1/2*(1+a_s)/(1+self.gamma*a_s)*(1-self.gamma))
        ans_arr = np.round(fsolve(alpha_s_eqn,np.logspace(-2,2,5)),4)
        ans_arr = np.unique(ans_arr)
        a_s = min(ans_arr)
        print("a_0: {:.4f}\t a_s: {}\t gamma: {:.4f}\t sol_number: {}".format(a_0, a_s, self.gamma, len(ans_arr)))
        return a_s
    
    def __cal_uB(self,a_s):
        uB = np.sqrt(e*self.Te/Mp)*np.sqrt((1+a_s)/(1+self.gamma*a_s))
        return uB
    
    def __cal_r_sh_new(self, Vsat, J):
        pass

    def __cal_r_sh(self, J): 
            r_sh = np.sqrt(4/9*epsilon_0*np.sqrt(2*e/Mp)*(self.V_sat - self.V_p)**1.5/J)
            #r_sh = rp
            return r_sh

    ### Public method ####    
    def iteration(self):
        #print("ne : {:.2e}, Te : {}, V_sat : {}, I_sat : {:.2e}".format(self.ne,self.Te,self.V_sat,self.I_sat))
        count = 0
        a_0 = 3
        r_sh_0 = rp
        S_eff = 2*(np.pi)*r_sh_0*lp
        
        while True:
            MAX_COUNT = 100
            count += 1
            a_s = self.__cal_alpha(a_0)
            uB = self.__cal_uB(a_s) # uB_k
            n_p = self.I_sat/(hr*S_eff*e*uB) # np_k , S_k-1
            comp = a_0 # for loop condition
            a_0 = n_p/self.ne-1 # a_0_k
            J = hr*e*n_p*uB # J_k
            r_sh = self.__cal_r_sh(J)
            S_eff = 2*np.pi*r_sh*lp
            
            #print(count, a_0)
            
            if abs(comp - a_0) < 0.001*a_0:
                return a_0
                break
            if count == MAX_COUNT:
                print('-----------No Convergence!---------------------')
                break
        print('--------------------------------------------------')

class fitting(iterative):
    ### Private_method ### 
    def __init__(self, IV, V, IV_second_derivative):
        self.IV = IV
        self.IV_second_derivative = IV_second_derivative
        if (np.array(IV['V']) == V).all():
            print("File import success")

    ### Public_method ### 
    def positive_ion_current(self, V, ne, nm, Te, Tp, Tm, Vp):
        n_p = ne + nm
        a_0 = nm/ne
        a_s = self.__cal_alpha(a_0)
        uBp = self.__cal_uB(a_s)
        if Vp > V:
            I = -hr*n_p*e*uBp*Seff(V, ne, nm, Te, Tm, Vp)
        else:
            I_Vp = -hr*n_p*e*uBp*Seff(V, ne, nm, Te, Tm, Vp)
            I = I_Vp*np.exp(-(V-Vp)/Tp)
        return -I
    
    def electron_current(self, V, ne, Te, Vp):
        ve = np.sqrt(8*e*Te/np.pi/Me)
        if Vp > V:
            I = e*Ap*ne*ve/4*np.exp(-(Vp - V)/Te)
        else:
            I = e*Ap*ne*ve/2*(2*np.sqrt((V-Vp)/Te/np.pi)+1/2*np.exp((V-Vp)/Te)*erfc((V-Vp)/Te))
        return I
        
    def negative_ion_current(self, V, ne, nm, Te, Tm, Vp):
        uBn = np.sqrt(e*Tm/Mn)
        if Vp > V:
            I_Vp = hr*nm*e*uBn*Seff(V, ne, nm, Te, Tm, Vp) # Seff(V) function 만들기
            I = I_Vp*np.exp(-(Vp - V)/Tm)
            #print('I: {:.4e}'.format(I))
        else:
            I = hr*nm*e*uBn*Seff(V, ne, nm, Te, Tm, Vp)
            #print('I: {:.4e}'.format(I))
        return I

    def total_current(self, V, ne, nm, Te, Tp, Tm, Vp):
        I_total = self.positive_ion_current(V, ne, nm, Te, Tp, Tm, Vp) + \
            self.electron_current(V, ne, Te, Vp) + \
            self.negative_ion_current(V, ne, nm, Te, Tm, Vp)
        return I_total

    def fitting(self):
        # IV 커브 피팅 + 2계 미분 피팅이 정확한 값을 찾아줘야 함
        pass