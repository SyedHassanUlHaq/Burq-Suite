import time, eel, os, glob, sys, tkinter, json, psutil, socket, requests, re, subprocess as sp, tkinter.filedialog as filedialog

from scripts.replacer import replacer
from scripts.reverter import reverter
from icecream import ic
from distutils.dir_util import copy_tree
from scripts.comparison import call
from scripts.logCompare import LogComparator
from scripts.cleanlify import cleanELF
from contextlib import closing
from apiConfig import URL

@eel.expose
def closeRecentRecord(id):
    print('closeRecentRecord')

    with open("records") as f:
        records = f.read().split("\n")

    projectToClose = records[int(id)]

    # delete this from records
    records.remove(projectToClose)

    with open("records", "w") as f:
        f.write("\n".join(records))

@eel.expose
def openRecentProject(id):
    print('openRecentProject')

    with open("records") as f:
        records = f.read().split("\n")

    projectToOpen = records[int(id)]

    proj, type = projectToOpen.split(",")

    with open("web/pathfile","w") as f:
        f.write(proj)

    with open("web/pathfilev","w") as f:
        f.write(type)

    eel.goToMain()

@eel.expose
def getRecords(debug=True):

    if debug:
        ic('getRecords')

    with open("records") as f:
        records = f.read()

    projects = []
    types = []

    for record in records.split("\n")[: -1]:
        proj, type = record.split(",")
        projects.append(proj.split("/")[-1])
        types.append(type)

    eel.displayRecords(projects,types)

@eel.expose
def runTests(core, iss, tests, projName, projPath, debug=False):
    print('runTests')

    if debug:
        ic(projName, projPath)
        ic(core, iss, tests)

    root_path = os.getcwd()
    ibex_test_path = "cores/ibex/"
    swerv_test__path = "cores/swerv/"
    tests_status = []
    perOccurProgress = (100 // len(tests)) // 2
    currentProgress = 0

    if core == "swerv":
        print('swerv')
        os.chdir(swerv_test__path)

        if debug:
            ic(os.getcwd())

        for test in tests:
            # check if test directory exists
            if os.path.isdir(test) == False:
                # create test directory
                os.mkdir(test)

            os.chdir(test)
            os.system("export RISCV=/opt/riscv32")

            os.system(f"export whisper={currentRootDir}/SweRV-ISS/build-Linux/./whisper")

            os.system(f"export RV_ROOT={currentRootDir}/cores/swerv")
            os.system("export PATH=/opt/riscv32/bin:$PATH")
            os.system(f"make -f $RV_ROOT/tools/Makefile TEST={test}")
            currentProgress += perOccurProgress
            progressTick(currentProgress)
            os.system(f"$whisper --logfile {test}.log {test}.exe --configfile ./snapshots/default/whisper.json")
            currentProgress += perOccurProgress
            progressTick(currentProgress)
            ic(os.getcwd())
            #check is test.log and exec.log exists
            ic(os.path.isfile(f"{test}.log"))
            ic(os.path.isfile("exec.log"))
            status = call(f"{test}.log", "exec.log")
            tests_status.append(status)

    elif core == "ibex":
        print('ibex')
        os.chdir(f"{currentRootDir}/{ibex_test_path}")
        perOccurProgress = (100 // len(tests)) // 2
        currentProgress = 0
        
        makefile_str = """PROGRAM = testname
                          PROGRAM_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
                          # Any extra source files to include in the build. Use the upper case .S
                          # extension for assembly files
                          EXTRA_SRCS :=

                          include ${PROGRAM_DIR}/../common/common.mk"""

        testroot="testcases/Riscv_tests"
        for test in tests:
            ic(test)
            os.chdir(f"{currentRootDir}/{ibex_test_path}")
            os.chdir("examples/sw/simple_system/")
            if os.path.isdir(test):
                # rm test directory
                os.system(f"rm -rf {test}")
            
                
            try:    
                os.mkdir(test)
                copy_tree(f"{currentRootDir}/{testroot}/{test}", f"{test}")
                

                os.chdir(test)
                file = open("Makefile", "w+")
                file.write(makefile_str.replace("testname", test))
                file.close()
                os.system("make")
                # check test.elf exists
                ic(os.path.isfile(f"{test}.elf"))
                ic(os.system("ls"))
                os.chdir(f"{currentRootDir}/{ibex_test_path}")
                os.system("fusesoc --cores-root=. run --target=sim --setup --build lowrisc:ibex:ibex_simple_system --RV32E=0 --RV32M=ibex_pkg::RV32MFast")
                os.system(f"./build/lowrisc_ibex_ibex_simple_system_0/sim-verilator/Vibex_simple_system [-t] --meminit=ram,examples/sw/simple_system/{test}/{test}.elf")
                currentProgress += perOccurProgress
                progressTick(currentProgress)
                os.chdir(f"{currentRootDir}/{ibex_test_path}/examples/sw/simple_system/{test}")
                os.system(f"spike --isa=rv32gc -m0x10000:0x30000,0x100000:0x100000 --log-commits -l {test}.elf 2> {test}.log")
                spike_ibex = LogComparator()
                core_ibex  = LogComparator()
                core_ibex.ibexLogExtract(f"{currentRootDir}/{ibex_test_path}/trace_core_00000000.log")#ibex core path
                spike_ibex.spikeLogExtract(f"{test}.log")
                if spike_ibex.match(core_ibex):
                    tests_status.append("PASSED")
                else:
                    tests_status.append("FAILED")
                currentProgress += perOccurProgress
                progressTick(currentProgress)
            except:
                tests_status.append("COMPILATION ERROR")
                currentProgress += perOccurProgress
                progressTick(currentProgress)
                currentProgress += perOccurProgress
                progressTick(currentProgress)
        


            
                
            

        
            
        os.chdir(currentRootDir)
        os.chdir(projPath)
        os.mkdir(projName)
        os.chdir(projName)
        report_str = ""
        report_str += f"Core,{core}\n"
        report_str += f"Iss,{iss}\n"
        report_str += "\n"
        report_str += "Test, Test Status\n"
        for i,t in enumerate(tests):
            report_str += f"{t},{tests_status[i]}\n"
        file = open("test_results.csv", "w+")
        file.write(report_str)
        file.close()
        os.chdir(currentRootDir)
        file = open("web/pathfile", "w")
        file.write(f"{projPath}/{projName}")
        file.close()
        file = open("web/pathfilev", "w")
        file.write("prebuilt_verification")
        file.close()
        file = open("records", "w+")
        file.write(f"{projPath}/{projName},prebuilt_verification\n")
        file.close()
        
        eel.goToMain()

       
            

        # for test in tests:
        #     copy_tree(f"{swerv_test__path}/{test}", "/tmp/testcases/")
        # os.chdir("web/swerv")
        # os.system(f"export RV_ROOT={os.getcwd()}")
        
        # os.system("make -f $RV_ROOT/tools/Makefile TEST_DIR=/tmp/testcases/")
        
        # #sp.Popen("make -f $RV_ROOT/tools/Makefile TEST_DIR=/tmp/testcases/".split())
        # #sp.Popen()

        
        # os.chdir(root_path)
        # eel.changeProgressBar(50)

    # if iss == "whisper":
    #     print("q")

    #     # os.chdir("web/whisper")
    #     print("r")
    #     # os.system(f"export whisper={os.getcwd()}/./whisper")
    #     print("w")
    #     os.chdir(root_path)

    #     for test in tests:
    #         ic(test)
    #         os.chdir(f"{swerv_test__path}/{test}")
    #         os.system(f"$whisper --logfile BubbleSort.log BubbleSort.exe --configfile ./snapshots/default/whisper.json")
    #         os.system(f"riscv32-unknown-elf-gcc -mabi=ilp32 -march=rv32imc -nostdlib -g -o {test} {test}.c")
    #         os.system(f"$whisper {test}")
    #         os.chdir(root_path)
    #     eel.changeProgressBar(100)

@eel.expose
def stop_everything():
    print('stop_everything')
    replacer() 
    os.system("./scripts/openMain.sh")
    # eel.start('index.html', mode='custom', cmdline_args=['node_modules/electron/dist/electron', '.'], port=8005)

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

@eel.expose
def socdetail():
    print('socdetail')
    yourproject = list1[-1]
    b = list2[-1]

    with open("web/pathfile", "w") as f:
        f.write(f"{yourproject}/{b}")
   
    os.chdir(yourproject)
    
    os.system(f"mkdir {b}")
   
    os.chdir(b)
    
    os.system(f"touch {b}.c")
    # list the files in the directory
    os.system("ls")

    with open(f"{b}.c", "w") as f:
        f.write("// write your code here \n")

    os.chdir(currentRootDir)
    
    with open("records", "w+") as f:
        f.write(f"{yourproject}/{b},custom_test\n")

    os.chdir(f"{currentRootDir}")
    eel.goToMain()

@eel.expose
def pyverification():
    print('pyverification')
    yourproject=list1[-1]
    
    aa = os.system(f"cd {yourproject}")
    b = list2[-1]

    with open("web/pathfile", "w") as f:
        f.write(f"{yourproject}/{b}")

    os.system(f"cp -a web/verification {yourproject}/{b}")
    eel.goToMain()

@eel.expose
def selectFolder(projectnamee, debug=True):

    if debug:
        ic('selectFolder')

    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    directory_path = filedialog.askdirectory()

    if debug:
        ic(directory_path)

    list1.clear()

    if debug:
        ic(list1)

    list1.append(directory_path)

    if debug:
        ic(list1)
        ic(projectnamee)

    list2.append(projectnamee)

    if debug:
        ic(list2)
    
    eel.select_js(list1[-1])

@eel.expose
def selectFolder1(debug=True):

    if debug:
        ic('selectFolder1')

    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    directory_path = filedialog.askdirectory()

    if debug:
        ic(directory_path)

    listuploadcore.clear()
    
    if debug:
        ic(listuploadcore)

    listuploadcore.append(directory_path)

    if debug:
        ic(listuploadcore)
   
    eel.select_js1(listuploadcore[-1])

@eel.expose
def selecttest():
    print("selecttest")
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    directory_path = filedialog.askdirectory()
    print(directory_path)
    testcasepath.clear()
    print(testcasepath)
    testcasepath.append(directory_path)
    ic(testcasepath)
   
    eel.select_jstestcase(testcasepath[-1])

@eel.expose
def selectlogfile():
    print("selectlogfile")
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    directory_path = filedialog.askdirectory()
    print(directory_path)
    logfilepath.clear()
    print(logfilepath)
    logfilepath.append(directory_path)
    ic(logfilepath)
   
    eel.select_jslog(logfilepath[-1])

  
    
    
#copy corefiles in ser seleted path
def copycorefiles():
    print('copycorefiles')
    
    yourproject=list1[-1]
    
    aa=os.system(f"cd {yourproject}")
    bb=listuploadcore[-1]
    b=list2[-1]
   
    os.system(f"cp bb  {yourproject}/{b}")
    

@eel.expose
def verCoreTest(listver):
    print('verCoreTest')
    i=listver[-1]
    if i=="SWERV-EH1":
        eel.testswerv()
        print(i)
    if i=="IBEX":
        eel.testibex()
        print(i)

@eel.expose
def getlistswerv():
    print('getlistswerv')
    namelist=[]
    root="cores/swerv/testbench/tests/"
    root1="testcases/User_Defined_Tests/"
    # get list of directory names from root
    for dirname in os.listdir(root):    
    # for path in filepaths:
        # a=path.split("/")
        ic(dirname)
        namelist.append(dirname)
    for dirname in os.listdir(root1):    
    # for path in filepaths:
        # a=path.split("/")
        ic(dirname)
        namelist.append(dirname)
        
    print(namelist)
    eel.showSwervTests(namelist)

@eel.expose
def getlistibex():
    print('getlistibex')
    namelist=[]
    root="testcases/Riscv_tests"
    root1="testcases/Riscv_tests"
    root2="testcases/User_Defined_Tests"              
    filepaths = [os.path.join(root,i) for i in os.listdir(root)]
    filepaths1 = [os.path.join(root1,i) for i in os.listdir(root1)]
    filepaths2 = [os.path.join(root1,i) for i in os.listdir(root2)]
    for path in filepaths:
        ic(path)
        a=path.split("/")
        namelist.append(a[-1])
        
    print(namelist,"po")
    for path in filepaths1:
        a=path.split("/")
        namelist.append(a[-1])
    for path in filepaths2:
        a=path.split("/")
        namelist.append(a[-1])
        
    print(namelist,"po")
    eel.showIbexTests(namelist)

@eel.expose
def datasend(listt, debug=True):

    if debug:
        ic('datasend')

    with open("web/pathfilev", "w") as f:
        f.write(listt[0])

    if debug:
        ic(listt)

@eel.expose
def genCore(isa,ext,bus):
    print('genCore')
    driverKey= f"corei{bus}"

    file = open("web/driver", "w")
    file.write(driverKey)
    file.close()

@eel.expose
def floatingpointtest():
    print('floatingpointtest')
    namelist=[]
    #root="web/swerv/testbench/tests/Floating_point_tests_for_azadi"
    root="testcases/Floating_point_tests_for_azadi"
    # get list of directory names from root
    for dirname in os.listdir(root):    
    # for path in filepaths:
        # a=path.split("/")
        ic(dirname)
        namelist.append(dirname)
        
    print(namelist)
    eel.showfloatingTests(namelist)

@eel.expose
def merlvectortest():
    print('merlvectortest')
    namelist=[]
    #root="web/swerv/testbench/tests/Floating_point_tests_for_azadi"
    root="testcases/MERL_vector_Tests"
    # get list of directory names from root
    for dirname in os.listdir(root):    
    # for path in filepaths:
        # a=path.split("/")
        ic(dirname)
        namelist.append(dirname)
        
    print(namelist)
    eel.showMerlTests(namelist)

@eel.expose
def riscvtest():
    print('riscvtest')
    namelist=[]
    #root="web/swerv/testbench/tests/Floating_point_tests_for_azadi"
    root="testcases/Riscv_tests"
    # get list of directory names from root
    for dirname in os.listdir(root):    
    # for path in filepaths:
        # a=path.split("/")
        ic(dirname)
        namelist.append(dirname)
        
    print(namelist)
    eel.showriscvTests(namelist)

@eel.expose
def selfcheckingvectortest():
    print('selfcheckingvectortest')
    namelist=[]
        #root="web/swerv/testbench/tests/Floating_point_tests_for_azadi"
    root="testcases/Self-Checking-vector-tests"
    # get list of directory names from root
    for dirname in os.listdir(root):    
    # for path in filepaths:
        # a=path.split("/")
        ic(dirname)
        namelist.append(dirname)
        
    print(namelist)
    eel.showselfcheckingvectorTests(namelist)

@eel.expose
def usertest(debug=True):
    namelist = []
    #root="web/swerv/testbench/tests/Floating_point_tests_for_azadi"
    root = "./testcases/User_Defined_Tests"

    # Get list of directory names from root
    for dirname in os.listdir(root):    
    # for path in filepaths:
        # a=path.split("/")
        if debug:
            ic(dirname)

        namelist.append(dirname)
        
    if debug:
        ic(namelist)

    eel.usersTests(namelist)

@eel.expose
def swervtest():
    print('swervtest')
    namelist=[]
        #root="web/swerv/testbench/tests/Floating_point_tests_for_azadi"
    root="testcases/Swerv_Tests"
    # get list of directory names from root
    for dirname in os.listdir(root):    
    # for path in filepaths:
        # a=path.split("/")
        ic(dirname)
        namelist.append(dirname)
        
    print(namelist)
    eel.showswervTests(namelist)

@eel.expose
def burqgeneratedtest():
    print('burqgeneratedtest')
    os.system(f"{currentRootDir}")

    namelist=[]
   
        #root="web/swerv/testbench/tests/Floating_point_tests_for_azadi"
    root="testcases/BURQ_Generated_Tests"
    # get list of directory names from root
    for dirname in os.listdir(root):    
    # for path in filepaths:
        # a=path.split("/")
        ic(dirname)
        namelist.append(dirname)
        
    print(namelist)
    eel.showburqTests(namelist)

@eel.expose
def dvtest(debug=True):
    
    if debug:
        ic('dvtest')

    tests = [
        "riscv_arithmetic_basic_test",
        "riscv_rand_instr_test",
        "riscv_jump_stress_test",
        "riscv_loop_test",
        "riscv_rand_jump_test",
        "riscv_mmu_stress_test",
        "riscv_no_fence_test",
        "riscv_illegal_instr_test",
        "riscv_ebreak_test",
        "riscv_ebreak_debug_mode_test",
        "riscv_full_interrupt_test",
        "riscv_csr_test",
        "riscv_unaligned_load_store_test"
    ]

    eel.showdvTests(tests)

# @eel.expose
# def enduploadcore(config, tests, types):
#     time.sleep(5)
#     progressTick(11.11)
#     time.sleep(5)
#     progressTick(22.22)
#     time.sleep(5)
#     progressTick(33.33)
#     time.sleep(5)
#     progressTick(44.44)
#     time.sleep(5)
#     progressTick(55.55)
#     time.sleep(5)
#     progressTick(66.66)
#     time.sleep(5)
#     progressTick(77.77)
#     time.sleep(5)
#     progressTick(88.88)
#     time.sleep(5)
#     progressTick(99.99)


@eel.expose
def enduploadcore(config, tests, types, debug=False):
    ic('enduploadcore')
    ic(config, tests, types)
   
    with open("web/pathfile", "w") as f:
        f.write(f"{config['path']}/{config['name']}")

    with open("web/pathfilev", "w") as f:
        f.write("custom_verification")

    uploadedcore = listuploadcore[-1]

    if debug:
        ic(uploadedcore)
    
    os.makedirs(f"{config['path']}/{config['name']}")
    os.makedirs(f"{config['path']}/{config['name']}/core")
    copy_tree(uploadedcore, f"{config['path']}/{config['name']}/core/")

    with open(f"{config['path']}/{config['name']}/config.json", "w+") as f:
        json.dump(config, f)

    testStatuses = []
    progress_step = (len(tests) / 100) / 3
    progress = 0

    if config["swerv"] == "": 

        if debug:
            ic("Custom core selected")

        extension_flags = "rv32" + "".join(config["extensions"])
        os.makedirs(f"{config['path']}/{config['name']}/tmp")
        os.path.exists(f"{config['path']}/{config['name']}/tmp")
        os.chdir(f"{config['path']}/{config['name']}")
        proj_dir = os.getcwd()

        if debug:
            ic(proj_dir)

        os.makedirs("logs")


        for i, test in enumerate(tests):

            # ISS Sim
            try:

                if types == "RISCV_DV_Tests":
                    ic("RISCV_DV_Tests")
                    os.chdir(f"{currentRootDir}/dv")
                    os.system(f"python3 run.py --iss spike --simulator pyflow --target {extension_flags} -o {config['path']}/{config['name']}/tmp/{test}_out -i 1  --test {test}")
                    os.chdir(f"{config['path']}/{config['name']}")

                else:
                    os.system(f"cp -r {currentRootDir}/testcases/{types}/{test} tmp/{test}")
                    os.system(f"python3 {currentRootDir}/dv/run.py --iss spike --simulator pyflow --target {extension_flags} --output tmp/{test}_out --c_test tmp/{test}/{test}.c")
                processes = psutil.pids()
                anyStillRunningSpikeProcess = list(filter(lambda x:psutil.Process(x).name() == "spike", processes))

                if len(anyStillRunningSpikeProcess) != 0:

                    for spikeProcessID in anyStillRunningSpikeProcess:
                        psutil.Process(spikeProcessID).kill()

                progress += progress_step
                progressTick(progress)

                # CORE Sim
                if config["testFormat"] == "asm":

                    if types != "RISCV_DV_Tests":
                        os.system(f"riscv64-unknown-elf-objdump -d {config['path']}/{config['name']}/tmp/{test}_out/directed_c_test/{test}.o > {config['path']}/{config['name']}/core/{config['hexDir']}/test.elf")

                    else:
                        ic(os.getcwd())
                        os.system(f"riscv64-unknown-elf-objdump -d {config['path']}/{config['name']}/tmp/{test}_out/asm_test/{test}_0.o > {config['path']}/{config['name']}/core/{config['hexDir']}/test.elf")

                    #print("cimpileeeeeeeeeee")
                    #hexCode, asmCode =  cleanELF(f"{config['path']}/{config['name']}/{test}.elf")


                    #hexFW = open(f"{config['path']}/{config['name']}/core/{config['hexDir']}", "w+")
                    #hexFW.write("\n".join(hexCode))
                    #hexFW.close()
                    #if config["asmDir"] != "":
                    #    asmFW = open(f"{config['path']}/{config['name']}/core/{config['asmDir']}", "w+")
                    #    asmFW.write("".join(asmCode))
                    #    asmFW.close()
                    #os.system(f"rm {config['path']}/{config['name']}/{test}.elf")
                    os.chdir(f"{config['path']}/{config['name']}/core")
                    #print("comamdmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
                    os.system(config["command"])
                else:
                    print("coreepattt")
                    os.system(f"cp -r {config['path']}/{config['name']}/tmp/{test} {config['path']}/{config['name']}/core/{config['testDir']}")
                    os.chdir(f"{config['path']}/{config['name']}/core")
                    os.system(config["command"].replace("{testname}", test))
                progress += progress_step
                progressTick(progress)

                os.chdir(f"{proj_dir}")
                ic(config["logFormat"])
                if config["logFormat"] == "csv":
                    # os.system(f"python3 {currentRootDir}/dv/scripts/instr_trace_compare.py --csv_file_1 {config['path']}/{config['name']}/tmp/{test}.csv --csv_file_2 {config['path']}/{config['name']}/core/{config['logFile']} --log {config['path']}/{config['name']}/{test}_compare_out.log")
                    # logFW = open(f"{config['path']}/{config['name']}/{test}_compare_out.log")
                    # logFWContent = logFW.readlines()
                    # logFW.close()
                    # os.system(f"rm {config['path']}/{config['name']}/{test}_compare_out.log")
                    spikeObj = LogComparator()
                    coreObj  = LogComparator()
                    if types!= "RISCV_DV_Tests":
                        spikeObj.spikeLogExtract(f"{config['path']}/{config['name']}/tmp/{test}_out/spike_sim/{test}.log")
                    else:
                        spikeObj.spikeLogExtract(f"{config['path']}/{config['name']}/tmp/{test}_out/spike_sim/test.0.log")
                    coreObj.coreLogExtract(f"{config['path']}/{config['name']}/core/{config['logFile']}")
                    if spikeObj.match(coreObj):
                        testStatuses.append("[PASSED]")
                    else:
                        testStatuses.append("[FAILED]")
                    os.system(f"mkdir {config['path']}/{config['name']}/logs/{test}")
                    os.system(f"cp {config['path']}/{config['name']}/tmp/{test}_out/spike_sim/{test}.log {config['path']}/{config['name']}/logs/{test}")
                    os.system(f"cp {config['path']}/{config['name']}/core/{config['logFile']} {config['path']}/{config['name']}/logs/{test}")
                else:
                    pass # CONVERT TO CSV AND COMPARE
                progress += progress_step
                progressTick(progress)
            except:
                testStatuses.append("[Incompatble with your Core Configuration]")
                progress += progress_step * 3
                progressTick(progress)
            
            
        
        os.chdir(f"{proj_dir}")
        #os.system("rm -rf tmp")
        # if len(list(filter(lambda x:x=="[PASSED]" or x=="[Incompatble with your Core Configuration]", testStatuses))) == len(testStatuses):
        #     os.system("rm -rf failed_logs")
        
        report_str = ""
        report_str += f"Core,{config['name']}\n"
        report_str += f"Iss,Spike\n"
        report_str += "\n"
        report_str += "Test, Test Status\n"
        

    else: # if swerv based
        RV_ROOT = f"{config['path']}/{config['name']}/core/"
        WHISPER = f"{currentRootDir}/SweRV-ISS/build-Linux/./whisper"
        for test in tests:
            if os.path.exists(f"{config['path']}/{config['name']}/core/testbench/tests/{test}"):
                # del the folder
                os.system(f"rm -rf {config['path']}/{config['name']}/core/{test}")
            os.system(f"cp -r {currentRootDir}/testcases/{types}/{test} {config['path']}/{config['name']}/core/testbench/tests/{test}")

            if os.path.exists(f"{config['path']}/{config['name']}/core/{test}"):
                # del the folder
                os.system(f"rm -rf {config['path']}/{config['name']}/core/{test}")
            os.mkdir(f"{config['path']}/{config['name']}/core/{test}")

            os.chdir(f"{config['path']}/{config['name']}/core/{test}")
            os.system(f"make -f {RV_ROOT}/tools/Makefile TEST={test}")
            progress += progress_step
            progressTick(progress)

            os.system(f"{WHISPER} --logfile {test}.log {test}.exe --configfile ./snapshots/default/whisper.json")
            progress += progress_step
            progressTick(progress)
            ic(os.path.isfile(f"{test}.log"))
            ic(os.path.isfile("exec.log"))
            status = call(f"{test}.log", "exec.log")
            testStatuses.append(status)
        report_str = ""
        report_str += f"Core,{config['name']}\n"
        report_str += f"Iss,Whisper\n"
        report_str += "\n"
        report_str += "Test, Test Status\n"
    
    ic(tests)
    ic(testStatuses)
    for i,t in enumerate(tests):
        report_str += f"{t},{testStatuses[i]}\n"
    file = open(f"{config['path']}/{config['name']}/test_results.csv", "w+")
    file.write(report_str)
    file.close()

    file = open(f"{currentRootDir}/records", "w+")
    file.write(f"{config['path']}/{config['name']},custom_core_verification\n")
    file.close()
    
    os.chdir(currentRootDir)
    eel.goToMain()











def progressTick(progress):
    print('progressTick')
    if progress < 20:
        eel.updateProgressBar(progress, "#f63a0f")
    elif progress < 40:
        eel.updateProgressBar(progress, "#f27011")
    elif progress < 60:
        eel.updateProgressBar(progress, "#f2b01e")
    elif progress < 80:
        eel.updateProgressBar(progress, "#f2d31b")
    elif progress < 100:
        eel.updateProgressBar(progress, "#86e01e")


#dv test select
@eel.expose
def selectdvtest(dvtestlist):
    print('selectdvtest')
    print(dvtestlist)

def validateUserCredentials(username, password):
    return username.isalpha() and password != "" and len(password) >= 8 and len(username) >= 3

@eel.expose
def pleaseLogin(username, password, debug=True):
    
    if debug:

        if username == "admin" and password == "admin":
            eel.loginSuccess()

        else:
            eel.throwAlert("Username or Password is incorrect")

    else:

        if not validateUserCredentials(username, password):
            eel.throwAlert("Invalid username or password. Please try again.")

        else:

            try:
                r = requests.post(URL, json={"username": username.lower(), "password": password})

            except:
                eel.throwAlert("Connection Error!\nPlease check your internet connection and try again.")

            if r.json()["status"] == "success":
                eel.loginSuccess()

            else:
                eel.throwAlert("Username or Password is incorrect")

@eel.expose
def enduploadcore__(getcommand,tests1,testcase,logfile,swerv,testtype):
    print('enduploadcore__')
    ic(swerv)
    tests_status=[]
    listcommands=[]
    ic(tests1)
    ic(getcommand)

    yourproject=list1[-1]
    b=list2[-1]
    file1=open("web/pathfile","w")
    file1.write(f"{yourproject}/{b}")
    file1.close()
    uploadedcore=listuploadcore[-1]
    ic(uploadedcore)
    #getpathcurrent=os.system("pwd")

   
    os.chdir(yourproject)
    
    
    os.system(f"mkdir {b}")

   

   
    os.chdir(b)
    os.system(f"cp -a {uploadedcore}  {yourproject}/{b}")
    os.chdir(f"{currentRootDir}")
    
   # if iss=="spike":
    # os.system("export PATH=/opt/riscv/bin:$PATH")
    # os.system("export PATH=/opt/riscv/riscv64-unknown-elf/bin:$PATH")


    # for test in tests1:
    #     ic(test)
    #     yy=getcommand.replace("testname",test)
    #     listcommands.append(yy)
    #     ic(yy)
    #     basename=os.path.basename(f"{p}")
    
    #     p=listuploadcore[-1]
    #     os.system(f"cp -a web/testcases/Self-Checking-Tests/{test} {yourproject}/{b}/{testcase}")
    #     os.chdir(f"{yourproject}/{b}/{testcase}/{test}")
    #     os.system(f"riscv64-unknown-elf-gcc -o {test} {test}.c")
    #     os.system(f"spike pk {test} > exec.log")
    #     os.chdir(f"{getpathcurrent}")
    #     os.chdir(f"{p}")
    #     os.system(f"{yy}")
    #     status = call(f"{yourproject}/{b}/{logfile}/{test}.log", f"{yourproject}/{b}/{testcase}/{test}/exec.log")
    #     tests_status.append(status)


        
    #     #command skipe
        
        


    #     #command for whisper
        
        
    # 
    # =os.path.basename(f"{p}")
    # os.chdir(f"{yourproject}")
    # report_str = ""
    # report_str += f"Core:{basename}\n"
    # report_str += "Iss:Spike\n"
    # for i,t in enumerate(tests1):
    #     report_str += f"{t}:{tests_status[i]}\n"
    # file = open("test_results.report", "w+")
    # file.write(report_str[:-1])
    # file.close()
    # os.chdir(currentRootDir)
    # file = open("web/pathfile", "w")
    # file.write(f"{yourproject}/{b}")
    # file.close()
    # file = open("web/pathfilev", "w")
    # file.write("uploadcore_verification")
    # file.close()
    # file = open("records", "w+")
    # file.write(f"{yourproject}/{b},upload_verification\n")
    # file.close()
    # eel.goToMain()


# if iss=="whisper":
    #os.system("export PATH=/opt/riscv/bin:$PATH")
    #os.system("export PATH=/opt/riscv/riscv64-unknown-elf/bin:$PATH")

#make -f $RV_ROOT/tools/Makefile TEST=BubbleSort
    if swerv=="swervbased":
        os.system("export RISCV=/opt/riscv64")

        os.system(f"export whisper='{currentRootDir}/Verification/SweRV-ISS/build-Linux/./whisper'")

        os.system(f"export RV_ROOT='{currentRootDir}/cores/swerv'")
        os.system("export PATH=/opt/riscv64/bin:$PATH")
        for test in tests1:
            ic(test)
            #yy=getcommand.replace("testname",test)
            #listcommands.append(yy)
            #ic(yy)
            p=listuploadcore[-1]
            basename=os.path.basename(f"{p}")
            ic(basename)
            ic(yourproject)
            ic(b)
            os.system(f"cp -a testcases/User_Defined_Tests/{test} {yourproject}/{b}/{testcase}")
        
        
            os.system(f"cp -a testcases/Swerv_Tests/{test} {yourproject}/{b}/{testcase}")
            os.chdir(f"{yourproject}/{b}/{basename}")
            #command skipe
            os.system(f"mkdir {test}")
            os.chdir(f"{test}")
            os.system(f"make -f $RV_ROOT/tools/Makefile TEST={test}")

            os.system(f"$whisper --logfile {test}.log {test}.exe --configfile ./snapshots/default/whisper.json")
        

        
            status = call(f"{test}.log", "exec.log")
            tests_status.append(status)
        basename=os.path.basename(f"{p}")
        os.chdir(f"{yourproject}/{b}")
        report_str = ""
        report_str += f"Core:{basename}\n"
        report_str += "Iss:Whisper\n"
        for i,t in enumerate(tests1):
            report_str += f"{t}:{tests_status[i]}\n"
        file = open("test_results.report", "w+")
        file.write(report_str[:-1])
        file.close()
        os.chdir(currentRootDir)
        file = open("web/pathfile", "w")
        file.write(f"{yourproject}/{b}")
        file.close()
        file = open("web/pathfilev", "w")
        file.write("uploadcore_verification")
        file.close()
        file = open("records", "w+")
        file.write(f"{yourproject}/{b},upload_verification\n")
        file.close()
        eel.goToMain()
    else:
        #os.system("export PATH=/opt/riscv/bin:$PATH")
        #os.system("export PATH=/opt/riscv/riscv64-unknown-elf/bin:$PATH")


        for test in tests1:
            ic(test)
            yy=getcommand.replace("testname",test)
            listcommands.append(yy)
            ic(yy)
            p=listuploadcore[-1]
            basename=os.path.basename(f"{p}")
            ic(testtype)
        
           
            os.system(f"cp -a testcases/{testtype}/{test} {yourproject}/{b}/{testcase}")
           
            
            os.system(f"riscv64-unknown-elf-gcc -o {test} {test}.c")
           # os.system(f"spike pk {test} > exec.log")
            os.chdir(f"{currentRootDir}")
            os.chdir(f"{p}")
            os.system(f"{yy}")
            os.chdir(f"{yourproject}/{b}/{testcase}/{test}")
            
            for file in glob.glob("*.log"):
                ic(file)
            
            status = call(f"{yourproject}/{b}/{testcase}/{test}/{file}",f"{yourproject}/{b}/{basename}/exec.log" )
            tests_status.append(status)


            
            #command skipe
            
            


            #command for whisper
            
        basename=os.path.basename(f"{p}")
        os.chdir(f"{yourproject}/{b}")
        report_str = ""
        report_str += f"Core:{basename}\n"
        report_str += "Iss:Spike\n"
        for i,t in enumerate(tests1):
            report_str += f"{t}:{tests_status[i]}\n"
        file = open("test_results.report", "w+")
        file.write(report_str[:-1])
        file.close()
        os.chdir(currentRootDir)
        file = open("web/pathfile", "w")
        file.write(f"{yourproject}/{b}")
        file.close()
        file = open("web/pathfilev", "w")
        file.write("uploadcore_verification")
        file.close()
        file = open("records", "w+")
        file.write(f"{yourproject}/{b},upload_verification\n")
        file.close()
        eel.goToMain()




        


    #place testcase in test case folder
    #make folder with testcase name
    #run command
    #got to log file path
    # run iss command 

reverter()

# def find_free_port():
#     with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
#         s.bind(('', 0))
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         return s.getsockname()[1]
if __name__ == '__main__':
    eel.init('web')

    list1 = ["a"]
    list2 = []
    listuploadcore = []

    currentRootDir = os.getcwd()
    ic(currentRootDir)
    testcasepath=[]
    logfilepath=[]

    eel.start('splash.html', mode='custom', cmdline_args=['node_modules/electron/dist/electron', '.'], port=8012)
