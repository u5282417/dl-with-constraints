import os
import sys 
import time
import copy 

import settings
import argparse
import itertools
parser = argparse.ArgumentParser(description = 'Config creator')  
parser.add_argument('--template_params_file',help='template config',type=str,required=True)
parser.add_argument('--out_dir',help='directory where generated files will be written', type=str, default = '.')
parser.add_argument('--exp_dir',help='sub-directory for the logs', type=str, required = True)

args = parser.parse_args()
all_params = []
names = []
short_names = []
jobs = list(itertools.product(*all_params))

assert len(names) == len(all_params)
additional_names = ['percent_data','num_epochs','grad_norm','ddlr','dd_increase_freq_by','dd_decay_lr_after']
additional_short_names = ['pct','ne','gn','ddlr','ifb','dlra']
additional_job_list = [
                        [1,250,10.0,0.0,0,0], # baseline
                        [1,250,3.5,0.05,1,1], # constraint learning
                        [1,250,3.5,0.05,1,5], # constraint learning
                        [1,250,3.5,0.05,1,10], # constraint learning
                        [1,250,3.5,0.05,10,1], # constraint learning
                        [1,250,3.5,0.05,10,5], # constraint learning
                        [1,250,3.5,0.05,10,10], # constraint learning
                        
                        [5,200,10.0,0.0,0,0], # baseline
                        [5,200,3.5,0.05,1,1], # constraint learning
                        [5,200,3.5,0.05,1,5], # constraint learning
                        [5,200,3.5,0.05,1,10], # constraint learning
                        [5,200,3.5,0.05,10,1], # constraint learning
                        [5,200,3.5,0.05,10,5], # constraint learning
                        [5,200,3.5,0.05,10,10], # constraint learning
                        
                        [10,200,10.0,0.0,0,0], # baseline
                        [10,200,3.5,0.05,1,1], # constraint learning
                        [10,200,3.5,0.05,1,5], # constraint learning
                        [10,200,3.5,0.05,1,10], # constraint learning
                        [10,200,3.5,0.05,10,1], # constraint learning
                        [10,200,3.5,0.05,10,5], # constraint learning
                        [10,200,3.5,0.05,10,10] # constraint learning
                    ]

names = names + additional_names
short_names = short_names + additional_short_names
assert len(names) == len(short_names)
all_jobs = list(itertools.product(jobs,additional_job_list))
sorted_names = copy.deepcopy(names)
sorted_names.sort()

if not os.path.exists(args.out_dir):
    os.makedirs(args.out_dir)

fh = open(args.template_params_file)
f0 = fh.read()
fh.close()
print('Creating {} config files in {}. Model logs will be in: {}'.format(len(all_jobs), args.out_dir, args.exp_dir))
for this_job in all_jobs:
    this_job = list(itertools.chain(*this_job))
    f = copy.deepcopy(f0)
    print(this_job)
    suffix = ''
    f = f.replace('${exp_dir}',str(args.exp_dir))
    for jn in range(len(names)):
        f = f.replace('${'+names[jn]+'}',str(this_job[jn]))
        suffix += '_'+short_names[jn]+str(this_job[jn])
    #
    file_name = os.path.basename(args.template_params_file)
    fh = open(os.path.join(args.out_dir,file_name+suffix+'.jsonnet'),'w')
    print(f,file=fh)
    fh.close()


