[01] from t100.core.simulator import Simulator
[02] from t100.core.base_components import *
[03] 
[04] 
[05] if __name__=='__main__':
[06]     
[07]     execution_time_expression = \
                                   lambda _ : 60+random.randint(-30,+30)
[08]     creation_tax_expression = lambda _ : 2.0/(60*5)
[09] 
[10]     acc = 0
[11]     q = Queue()
[12]     s = Source(output=q, 
[13]                creation_tax_expression=creation_tax_expression, 
[14]                execution_time_expression=execution_time_expression)
[15]     
[16]     p = Process(inputs=[q])
[17] 
[18]     steps_number = 60*60
[19] 
[20]     simul = Simulator(components=[q,s,p])
[21]     simul.run(untill=steps_number)
[22]     q_size = len(simul.components['queue'][0])
[23]     
[24]     print q_size
[25]     
 