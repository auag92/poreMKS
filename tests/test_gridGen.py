from pathlib import Path

import ase.io as aio
import numpy as np
from toolz.curried import pipe

import atommks.grid_generator as gen
import atommks.porosity as pore


def test_edtGen():

    r_Ox = 1.35
    r_Si = 1.35

    len_pixel = 10

    fname = Path(__file__).parents[1] / "datasets" / "iza_zeolites" / "MFI.cif"

    rep = [1, 1, 1]
    atom = pipe(fname, lambda fname: aio.read(fname), lambda x: x.repeat(rep))

    radii = {"Si": r_Si, "O": r_Ox}
    S = gen.grid_maker(
        atom, len_pixel=10, atomic_radii=radii, full=False, fft=False
    )[0]

    assert S.shape == (202, 198, 133)

    padval = ((1, 1), (1, 1), (0, 0))

    S_dgrid = pipe(
        S,
        lambda s: np.pad(s, padval, "constant", constant_values=0),
        lambda s: pore.dgrid(s, len_pixel=len_pixel),
    )

    pld = pore.get_pld(S_dgrid)
    assert np.allclose(pld, 2.61718, atol=1e-3)

    lcd = pore.get_lcd(S_dgrid)
    assert np.allclose(lcd, 6.79705, atol=1e-3)


def test_fftGen():

    r_Ox = 1.35
    r_Si = 1.35

    len_pixel = 10

    fname = Path(__file__).parents[1] / "datasets" / "iza_zeolites" / "MFI.cif"

    rep = [1, 1, 1]
    atom = pipe(fname, lambda fname: aio.read(fname), lambda x: x.repeat(rep))

    radii = {"Si": r_Si, "O": r_Ox}
    S = gen.grid_maker(
        atom, len_pixel=10, atomic_radii=radii, full=False, fft=True
    )[0]

    assert S.shape == (202, 198, 133)

    padval = ((1, 1), (1, 1), (0, 0))

    S_dgrid = pipe(
        S,
        lambda s: np.pad(s, padval, "constant", constant_values=0),
        lambda s: pore.dgrid(s, len_pixel=len_pixel),
    )

    pld = pore.get_pld(S_dgrid)
    assert np.allclose(pld, 2.6171875, atol=1e-3)

    lcd = pore.get_lcd(S_dgrid)
    assert np.allclose(lcd, 6.7230939, atol=1e-3)
