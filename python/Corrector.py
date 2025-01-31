import numpy as np

class Corrector:
   
   # store regressors
   def __init__(self,mcclf,dataclf,X,Y,diz=False):
      self.diz=diz #Flag for distribution with discrete 0, i.e. Isolation
      self.mcqtls   = np.array([clf.predict(X) for clf in mcclf])
      self.dataqtls = np.array([clf.predict(X) for clf in dataclf])

      self.Y = Y
      
   # correction is actually done here
   def correctEvent(self,iev):

      mcqtls = self.mcqtls[:,iev]
      dataqtls = self.dataqtls[:,iev]
      Y = self.Y[iev]
      
      if self.diz and Y == 0.:
         return 0.

      qmc =0
      
      while qmc < len(mcqtls): # while + if, to avoid bumping the range
         if mcqtls[qmc] < Y:
            qmc+=1
         else:
            break

      if qmc == 0:
         qmc_low,qdata_low   = 0,0                              # all shower shapes have a lower bound at 0
         qmc_high,qdata_high = mcqtls[qmc],dataqtls[qmc]
      elif qmc < len(mcqtls):
         qmc_low,qdata_low   = mcqtls[qmc-1],dataqtls[qmc-1]
         qmc_high,qdata_high = mcqtls[qmc],dataqtls[qmc]
      else:
         qmc_low,qdata_low   = mcqtls[qmc-1],dataqtls[qmc-1]
         qmc_high,qdata_high = mcqtls[len(mcqtls)-1]*1.2,dataqtls[len(dataqtls)-1]*1.2
         # to set the value for the highest quantile 20% higher
                                                                       
      return (qdata_high-qdata_low)/(qmc_high-qmc_low) * (Y - qmc_low) + qdata_low

   def __call__(self):
      return np.array([ self.correctEvent(iev) for iev in range(self.Y.size) ]).ravel()

def applyCorrection(mcclf,dataclf,X,Y,diz=False):
   return Corrector(mcclf,dataclf,X,Y,diz)()
