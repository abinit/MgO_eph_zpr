#!/usr/bin/env python
r"""
Computation of Phonons, BECS and Eps_inf for MgO
==================================================

This example shows how to compute phonons with DFPT
Symmetries are taken into account: only q-points in the IBZ are generated.
The final results (out_DDB, out_DVDB) will be produced automatically at the end of the run
and saved in the ``outdata/`` directory of work[1].
"""

import sys
import os
import abipy.abilab as abilab
import abipy.data as abidata

from abipy import flowtk

def make_scf_input():
    """
    This function constructs the input file for the GS calculation:
    """

    # Initialize MgO structure from abinit variables.
    structure = abilab.Structure.from_abivars(
        acell=3 * [4.252718 * abilab.units.ang_to_bohr],
        rprim=[0.0000000000, 0.5000000000, 0.5000000000,
               0.5000000000, 0.0000000000, 0.5000000000,
               0.5000000000, 0.5000000000, 0.0000000000],
        natom=2,
        ntypat=2,
        typat=[1, 2],
        znucl=[12, 8],
        xred=[0.0000000000, 0.0000000000, 0.0000000000,
              0.5000000000, 0.5000000000, 0.5000000000]
    )

    # NC pseudos assumed in currect working directory.
    pseudos = ["Mg-sp-gw.psp8", "O.psp8"]

    # Input for GS part.
    gs_inp = abilab.AbinitInput(structure, pseudos=pseudos)

    gs_inp.set_vars(
        nband=12,
        paral_kgb=0,
        ecut=35.0,        # Too low. Should be ~50
        ngkpt=[4, 4, 4],  # Too coarse
        nshiftk=1,        # Gamma-centered mesh. Important to have the CBM/VBM!
        shiftk=[0, 0, 0],
        tolvrs=1.0e-10,
        diemac=9.0,
        nstep=150,
        nbdbuf=4,
        prtpot=1,        # Print potential for Sternheimer
        iomode=3,        # Produce output files in netcdf format.
    )

    return gs_inp


def build_flow(options):
    """
    Create a `Flow` for phonon calculations. The flow has two works.

    - work[0]: GS + NSCF along a k-path
    - work[1]: DFPT work with phonons on a 4x4x4, BECS and eps_inf
    """
    # Working directory (default is the name of the script with '.py' removed and "run_" replaced by "flow_")
    if not options.workdir:
        options.workdir = os.path.basename(__file__).replace(".py", "").replace("run_", "flow_")

    flow = flowtk.Flow(workdir=options.workdir)

    # Build input for GS calculation and create first work with 1 ScfTask.
    gs_inp = make_scf_input()
    work = flow.register_scf_task(gs_inp)
    scf_task = work[0]

    # Build new input for NSCF calculation with k-path (automatically selected by AbiPy)
    # Used to plot the KS band structure
    nscf_kpath_inp = gs_inp.new_with_vars(
        nband=12,
        tolwfr=1e-18,
        iscf=-2,
    )
    nscf_kpath_inp.set_kpath(ndivsm=10)
    work.register_nscf_task(nscf_kpath_inp, deps={scf_task: "DEN"})

    # Q-mesh for phonons. In this case k-mesh == q-mesh
    ngqpt = [4, 4, 4]

    # Create work for phonon calculationwith a [4, 4, 4] q-mesh.
    # Electric field and Born effective charges are also computed.
    ph_work = flowtk.PhononWork.from_scf_task(scf_task, ngqpt, is_ngqpt=True, with_becs=True)

    flow.register_work(ph_work)
    flow.allocate()
    flow.use_smartio()

    return flow

@flowtk.flow_main
def main(options):
    """
    This is our main function that will be invoked by the script.
    flow_main is a decorator implementing the command line interface.
    Command line args are stored in `options`.
    """
    return build_flow(options)


if __name__ == "__main__":
    sys.exit(main())
