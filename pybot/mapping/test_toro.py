"""
Test SLAM interface with Toro
"""
print(__doc__)

# Author: Sudeep Pillai <spillai@csail.mit.edu>
# License: MIT

import numpy as np
from pybot.geometry.rigid_transform import RigidTransform


# Tests
# ======================================================================

def test_solveFromFile():
    import os
    import sys
    import time
    from pytoro import TreeOptimizer3

    
    overrideCovariances = False
    twoDimensions = False

    pg = TreeOptimizer3()

    pg.verboseLevel = 0
    pg.restartOnDivergence = False

    filename = '/home/spillai/perceptual-learning/software/externals/toro-pod/toro/data/3D/sphere_smallnoise.graph'
    print('Loading graph file {}... '.format(filename))
    if not pg.load(filename, overrideCovariances, twoDimensions):
        print('FATAL ERROR: Could not read file. Abrting.')
        sys.exit(1)
    print 'V / E', pg.nvertices, pg.nedges
    print('Done')

    # Reduce nodes
    print('Loading equivalence constraints and collapsing nodes... ')
    pg.loadEquivalences(filename)
    print(' #nodes: {} #edges: {}'.format(pg.nvertices, pg.nedges))

    # Compress indices (-ic) def: false
    print('Compressing indices... ')
    # pg.compressIndices()
    print('Done')

    # Tree type  (-st, -mst) def: st
    print('Incremental tree construction... ')
    pg.buildSimpleTree() # st

    # print('MST construction... ')
    # ppg.buildMST(first_vertex_id) # mst
    print('Done')

    # Initialize on tree (-nib) def: true
    print('Computing initial guess from observations... ')
    pg.initializeOnTree()
    print('Done')

    print('Initializing the optimizer...')
    pg.initializeTreeParameters()
    pg.initializeOptimization(compare_mode='level');
    l = pg.totalPathLength()
    nEdges = pg.nedges
    apl = l / nEdges
    print('Done')
    print('Average path length={}'.format(apl))
    print('Complexity of an iteration={}'.format(l))


    stripped_filename,_ = os.path.splitext(filename)
    print('Saving starting graph... ')
    output = stripped_filename + '-treeopt-initial.graph'
    pg.save(output)
    print('Done')

    output = stripped_filename + '-treeopt-initial.dat'
    pg.saveGnuplot(output)
    print('Done')

    error_output = stripped_filename + '-treeopt-error.dat'
    # ofstream errorStream;


    # ignore preconditioner (-ip)
    ignorePreconditioner = False

    print('**** Starting optimization ****')
    st = time.time()
    corrupted = False
    for j in range(100): 
        pg.iterate([], ignorePreconditioner);
        ei = pg.error()
        error = ei['error']

        print('Iteration {} RotGain={}'.format(j, pg.rotGain))
        print('   global error = {}   error/constraint = {}'.format(error, error / nEdges))
        print('mte={} mre={} are={} ate={}'.format(ei['mte'], ei['mre'], ei['are'], ei['ate']))

        if (ei['mre'] > (np.pi / 2) * (np.pi / 2)):
            corrupted = True
        else: 
            corrupted = False

    print('TOTAL TIME= {} s.'.format(time.time() - st))    


    print('Saving files...(graph file)')
    output = stripped_filename+ '-treeopt-final.graph'
    pg.save(output)
    print('...(gnuplot file)...')
    output = stripped_filename + '-treeopt-final.dat'
    pg.saveGnuplot(output)
    # errorStream.close();
    print('Done')


    

def test_odometryExample(): 
    print("test_odmetryExample\n")
    print("=================================")

    from toro import BaseSLAM

    # Init
    slam = BaseSLAM(verbose=True)

    rt = RigidTransform.random()
    slam.add_incremental_pose_constraint(RigidTransform.random())
    slam.add_incremental_pose_constraint(RigidTransform.random())
    slam.add_incremental_pose_constraint(RigidTransform.random())
    slam.add_incremental_pose_constraint(RigidTransform.random())
    # slam.initialize(p=RandomTransform.identity(), index=0)
    # slam.initialize(p=rt, index=1)
    # slam.add_relative_pose_constraint(0, 1, rt)
    # slam.add_relative_pose_constraint(1, 2, RigidTransform.random())
    # slam.add_relative_pose_constraint(2, 3, RigidTransform.random())
    # slam.add_relative_pose_constraint(3, 4, RigidTransform.random())
    
if __name__ == "__main__": 
    test_odometryExample()
    print('OK')
    # test_solveFromFile()
    # print('OK')
