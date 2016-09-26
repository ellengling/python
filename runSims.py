#!/usr/bin/env python
"""
------------------------------------------------------------------------
A script that runs the ComPair analysis chain on a multicore system.

Probably not useful in other cases...

Author: Jeremy Perkins (jeremy.s.perkins@nasa.gov)

------------------------------------------------------------------------
"""

import os

def setPath(comPath = ""):

    '''Checks for COMPAIRPATH.  Returns 0 if ok, 1 if bad.'''
    
    if comPath:
        if '~' in comPath:
            os.environ['COMPAIRPATH'] = os.path.expanduser(comPath)
            return 0
        else:
            os.environ['COMPAIRPATH'] = comPath
            return 0
    elif not ('COMPAIRPATH' in os.environ):
        print 'Set or provide COMPAIRPATH'
        return 1
    else:
        return 0

def runCosima(srcFile):

    import subprocess
    import gzip

    print "Running cosima on " + srcFile
    
    p = subprocess.Popen(['cosima',srcFile],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    out, err = p.communicate()

    base = os.path.splitext(os.path.basename(srcFile))

    print "Writing Log for " + srcFile
    with gzip.open(base[0]+'.stdout.gz', 'wb') as f:
        f.write(out)

    if (len(err) > 0):
        print "Errors exist, might want to check " + srcFile
        with gzip.open(base[0]+'.stderr.gz', 'wb') as f:
            f.write(err)

def runRevan(simFile, cfgFile):

    import subprocess
    import gzip

    print "Running revan on " + simFile

    p = subprocess.Popen(['revan', '-f', simFile, '-c', cfgFile, '-n', '-a'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    out, err = p.communicate()

    base = os.path.splitext(os.path.basename(simFile))

    print "Writing Log for " + simFile
    with gzip.open(base[0]+'.revan.stdout.gz', 'wb') as f:
        f.write(out)

    if (len(err) > 0):
        print "Errors exist, might want to check " + simFile
        with gzip.open(base[0]+'.revan.stderr.gz', 'wb') as f:
            f.write(err)

def runRevan_star(files):
    """Convert `f([1,2])` to `f(1,2)` call."""
    return runRevan(*files)

            
def getFiles(searchDir = '', extension = 'source'):

    from glob import glob    

    if not ('COMPAIRPATH' in os.environ):
        print 'Set or provide COMPAIRPATH'
        return ""

    if searchDir:
        return glob(searchDir+'/*.'+extension)
    else:
        return glob(os.environ['COMPAIRPATH']+'/Simulations/PerformancePlotSourceFiles/*.'+extension)

def cli():

    from multiprocessing import Pool
    from itertools import izip, repeat
    
    helpString = "Submits cosima or revan jobs to multiple cores."

    import argparse
    parser = argparse.ArgumentParser(description=helpString)

    parser.add_argument("jobs", type=int, help="The number of jobs you wish to spawn (usually the number of cores on your machine).")
    parser.add_argument("--runCosima", type=bool, default=False, help="Run cosima (default is false)")
    parser.add_argument("--runRevan", type=bool, default=False, help="Run revan (default is false)")
    parser.add_argument("--COMPAIRPATH",help="Path to compair files.  You can set this via an environment variable")
    parser.add_argument("--sourcePath",help="Where the source files live.  If not given, will get from COMPAIRPATH.")
    parser.add_argument("--simPath", help="Where the sim files live (from cosima).")
    parser.add_argument("--revanCfg", help="Revan config file (need full path).")
    parser.add_argument("--partition", nargs=2, type=int, default=[0,-1],
                        help="Python like slice statement to divide lists.  Need to provide two numbers (default is 0 -1).") 
    
    args = parser.parse_args()

    if setPath(args.COMPAIRPATH):
        exit()
    else:
        print "COMPAIRPATH set to " + os.environ['COMPAIRPATH']

    p1,p2 = args.partition
        
    if args.runCosima:
        srcFiles = getFiles(args.sourcePath,'source')
        if not srcFiles:
            print "No source files found"
            exit()
        else:
            print "Got this many source files: " + str(len(srcFiles))
            print "Spawing jobs"
            pool = Pool(processes=args.jobs)
            pool.map(runCosima,srcFiles[p1,p2])

    if args.runRevan:
        simFiles = getFiles(args.simPath,'sim')
        if not args.revanCfg:
            print "Need to specify the config file for revan (--revanCfg)"
            exit()
        elif not simFiles:
            print "No sim files found"
            exit() 
        else:
            print "Got this many sim files: " + str(len(simFiles))
            print "Spawning jobs"
            pool = Pool(processes=args.jobs)
            pool.map(runRevan_star,
                     izip(simFiles[p1,p2],repeat(args.revanCfg)))

if __name__ == '__main__': cli()
    
    
