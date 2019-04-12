from multiprocessing import Pool
from multiprocessing import freeze_support
import os 

def run_process(process):
	os.system('python ' + process)

def main():
	freeze_support()
	processes = ('wearable_data.py', 'skel.py')
	pool = Pool(processes=len(processes))
	pool.map(run_process, processes)

if __name__ == "__main__": 
	main()