# read all the root files in sim_repo, and make command for each of them, listed in a new file commandList_address.
import os

# save hist/txt after cutting
save_hist_folder = 'path/to/saving/output/directory/'
sim_repo = '/data/snoplus3/SNOplusData/production/Prod_RAT-7.0.15_AmBe_Feb2023'
repo_address = 'path/to/directory/containing/make_hists.exe/'
commandList_address = 'path/to/command_list_file.txt'

file_addresses = []
name = []
out_address_start = save_hist_folder + 'hist'
for filename in os.listdir(sim_repo):
    file_address = os.path.join(sim_repo, filename)
    if os.path.isfile(file_address):
        if file_address[-5:] == '.root':
            file_addresses.append(' ' + file_address)
            name.append(filename[:-5])
print(name)
'''
is_data = false
verbose = false

command_base = repo_address + 'make_hists.exe '
commands = []
for i in range(len(file_addresses)):
    outRoot_address = out_address_start + '_' + str(i) + '.root '
    outText_address = out_address_start + '_' + str(i) + '.txt '
    commands.append(command_base + outRoot_address + outText_address + str(0) + ' ' + str(int(is_data)) + ' ' + str(int(verbose)) + file_addresses[i] + '\n')
        
# Create the job script to run all these commands in a file
with open(commandList_address, 'w') as f:
    command_list = ''.join(commands)
    f.write(command_list)
'''