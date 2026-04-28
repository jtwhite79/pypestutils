"""Tests for pestutilslib module."""

import logging
from pathlib import PureWindowsPath

import numpy as np
import pytest

from pypestutils.pestutilslib import PestUtilsLib


def _grid2d(n: int = 10, dx: float = 100.0):
    """Return a square (n x n) grid suitable for fieldgen2d_sva tests."""
    xs = (np.arange(n, dtype=np.float64) + 0.5) * dx
    ys = (np.arange(n, dtype=np.float64) + 0.5) * dx
    xx, yy = np.meshgrid(xs, ys, indexing="ij")
    ec = xx.ravel(order="F")
    nc = yy.ravel(order="F")
    nnode = ec.size
    return {
        "ec": ec,
        "nc": nc,
        "area": float(dx * dx),
        "active": np.ones(nnode, dtype=np.int32),
        "mean": 0.0,
        "var": 1.0,
        "aa": 3.0 * dx,
        "anis": 1.0,
        "bearing": 0.0,
        "transtype": 0,
        "avetype": 2,  # exp
        "power": 1.0,
        "nnode": nnode,
    }


def _grid3d(n: int = 6, dx: float = 100.0, dz: float = 10.0):
    """Return a small (n x n x 2) grid suitable for fieldgen3d_sva tests."""
    nz = 2
    xs = (np.arange(n, dtype=np.float64) + 0.5) * dx
    ys = (np.arange(n, dtype=np.float64) + 0.5) * dx
    zs = (np.arange(nz, dtype=np.float64) + 0.5) * dz
    xx, yy, zz = np.meshgrid(xs, ys, zs, indexing="ij")
    ec = xx.ravel(order="F")
    nc = yy.ravel(order="F")
    zc = zz.ravel(order="F")
    nnode = ec.size
    return {
        "ec": ec,
        "nc": nc,
        "zc": zc,
        "area": float(dx * dx),
        "height": dz,
        "active": np.ones(nnode, dtype=np.int32),
        "mean": 0.0,
        "var": 1.0,
        "ahmax": 3.0 * dx,
        "ahmin": 3.0 * dx,
        "avert": 2.0 * dz,
        "bearing": 0.0,
        "dip": 0.0,
        "rake": 0.0,
        "transtype": 0,
        "avetype": 2,
        "power": 1.0,
        "nnode": nnode,
    }


def test_init_del():
    lib = PestUtilsLib()
    del lib


def test_init_logger(caplog):
    caplog.set_level(logging.DEBUG)
    lib = PestUtilsLib(logger_level=logging.INFO)
    assert len(caplog.records) == 0
    lib.initialize_randgen(123)
    assert len(caplog.records) > 0


def test_create_char_array():
    lib = PestUtilsLib()
    filein = PureWindowsPath("path") / "to" / "a" / "file.txt"
    char_ar = lib.create_char_array(bytes(filein), "LENFILENAME")
    assert char_ar.value == rb"path\to\a\file.txt"
    gridname = "mygrid"
    char_ar = lib.create_char_array(gridname, "LENGRIDNAME")
    assert char_ar.value == b"mygrid"
    with pytest.raises(ValueError):
        lib.create_char_array("foo", "lengridname")
    with pytest.raises(TypeError):
        lib.create_char_array(1, "LENGRIDNAME")


def test_inquire_modflow_binary_file_specs(): ...


def test_retrieve_error_message(): ...


def test_install_structured_grid(): ...


def test_get_cell_centres_structured(): ...


def test_uninstall_structured_grid(): ...


def test_free_all_memory(): ...


def test_interp_from_structured_grid(): ...


def test_interp_to_obstime(): ...


def test_install_mf6_grid_from_file(): ...


def test_get_cell_centres_mf6(): ...


def test_uninstall_mf6_grid(): ...


def test_calc_mf6_interp_factors(): ...


def test_interp_from_mf6_depvar_file(): ...


def test_extract_flows_from_cbc_file(): ...


def test_calc_kriging_factors_2d(): ...


def test_calc_kriging_factors_auto_2d(): ...


def test_calc_kriging_factors_3d(): ...


def test_krige_using_file(): ...


def test_build_covar_matrix_2d(): ...


def test_build_covar_matrix_3d(): ...


def test_calc_structural_overlay_factors(): ...


def test_interpolate_blend_using_file(): ...


def test_ipd_interpolate_2d(): ...


def test_ipd_interpolate_3d(): ...


def test_initialize_randgen():
    lib = PestUtilsLib()
    lib.initialize_randgen(123)


def test_fieldgen2d_sva():
    lib = PestUtilsLib()
    lib.initialize_randgen(123)
    g = _grid2d()
    out = lib.fieldgen2d_sva(
        g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
        g["aa"], g["anis"], g["bearing"],
        g["transtype"], g["avetype"], g["power"], nreal=3,
    )
    assert out.shape == (g["nnode"], 3)
    assert np.all(np.isfinite(out))


def test_fieldgen3d_sva():
    lib = PestUtilsLib()
    lib.initialize_randgen(123)
    g = _grid3d()
    out = lib.fieldgen3d_sva(
        g["ec"], g["nc"], g["zc"], g["area"], g["height"], g["active"],
        g["mean"], g["var"], g["ahmax"], g["ahmin"], g["avert"],
        g["bearing"], g["dip"], g["rake"],
        g["transtype"], g["avetype"], g["power"], nreal=3,
    )
    assert out.shape == (g["nnode"], 3)
    assert np.all(np.isfinite(out))


# ----------------------------------------------------------------------------
# Tests for fill_stdnormal, fieldgen2d_sva_iid, fieldgen3d_sva_iid
# ----------------------------------------------------------------------------


def test_fill_stdnormal_shape_and_finite():
    lib = PestUtilsLib()
    lib.initialize_randgen(123)
    arr = lib.fill_stdnormal(50, 4)
    assert arr.shape == (50, 4)
    assert arr.dtype == np.float64
    assert arr.flags.f_contiguous
    assert np.all(np.isfinite(arr))


def test_fill_stdnormal_reproducible():
    lib1 = PestUtilsLib()
    lib1.initialize_randgen(7)
    a1 = lib1.fill_stdnormal(20, 3)
    lib2 = PestUtilsLib()
    lib2.initialize_randgen(7)
    a2 = lib2.fill_stdnormal(20, 3)
    np.testing.assert_array_equal(a1, a2)


def test_fieldgen2d_sva_iid_equivalence():
    """Original fieldgen2d_sva must match fieldgen2d_sva_iid driven by fill_stdnormal."""
    g = _grid2d()
    nreal = 4

    lib_a = PestUtilsLib()
    lib_a.initialize_randgen(2024)
    field_orig = lib_a.fieldgen2d_sva(
        g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
        g["aa"], g["anis"], g["bearing"],
        g["transtype"], g["avetype"], g["power"], nreal=nreal,
    )

    lib_b = PestUtilsLib()
    lib_b.initialize_randgen(2024)
    diid = lib_b.fill_stdnormal(g["nnode"], nreal)
    field_iid = lib_b.fieldgen2d_sva_iid(
        g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
        g["aa"], g["anis"], g["bearing"],
        g["transtype"], g["avetype"], g["power"], diid,
    )
    np.testing.assert_array_equal(field_orig, field_iid)


def test_fieldgen2d_sva_iid_no_seed_required():
    """The _iid variant must not require initialize_randgen."""
    g = _grid2d()
    rng = np.random.default_rng(12345)
    diid = rng.standard_normal(size=(g["nnode"], 2))
    lib = PestUtilsLib()
    field = lib.fieldgen2d_sva_iid(
        g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
        g["aa"], g["anis"], g["bearing"],
        g["transtype"], g["avetype"], g["power"], diid,
    )
    assert field.shape == (g["nnode"], 2)
    assert np.all(np.isfinite(field))


def test_fieldgen2d_sva_iid_deterministic():
    """Same diid in two fresh PestUtilsLib instances must give identical fields."""
    g = _grid2d()
    rng = np.random.default_rng(99)
    diid = rng.standard_normal(size=(g["nnode"], 3))

    def run():
        lib = PestUtilsLib()
        return lib.fieldgen2d_sva_iid(
            g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
            g["aa"], g["anis"], g["bearing"],
            g["transtype"], g["avetype"], g["power"], diid,
        )

    np.testing.assert_array_equal(run(), run())


def test_fieldgen2d_sva_iid_linearity_transtype0():
    """For transtype=0 (mean=0), the field is linear in diid."""
    g = _grid2d()
    g["mean"] = 0.0  # explicit, so linear superposition holds
    rng = np.random.default_rng(0)
    d1 = rng.standard_normal(size=(g["nnode"], 1))
    d2 = rng.standard_normal(size=(g["nnode"], 1))
    a, b = 0.7, -1.3

    lib = PestUtilsLib()
    f1 = lib.fieldgen2d_sva_iid(
        g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
        g["aa"], g["anis"], g["bearing"],
        g["transtype"], g["avetype"], g["power"], d1,
    )
    f2 = lib.fieldgen2d_sva_iid(
        g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
        g["aa"], g["anis"], g["bearing"],
        g["transtype"], g["avetype"], g["power"], d2,
    )
    fcomb = lib.fieldgen2d_sva_iid(
        g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
        g["aa"], g["anis"], g["bearing"],
        g["transtype"], g["avetype"], g["power"], a * d1 + b * d2,
    )
    np.testing.assert_allclose(fcomb, a * f1 + b * f2, rtol=1e-10, atol=1e-10)


def test_fieldgen2d_sva_iid_mean_variance_recovery():
    """With many realisations the ensemble mean/variance approach the targets."""
    g = _grid2d()
    g["mean"] = 5.0
    g["var"] = 4.0
    nreal = 800
    rng = np.random.default_rng(42)
    diid = rng.standard_normal(size=(g["nnode"], nreal))

    lib = PestUtilsLib()
    field = lib.fieldgen2d_sva_iid(
        g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
        g["aa"], g["anis"], g["bearing"],
        g["transtype"], g["avetype"], g["power"], diid,
    )
    # Ensemble mean across realisations should be close to 5 (loose tolerance).
    assert abs(field.mean() - 5.0) < 0.2
    # Per-node sample variance should be close to 4 (loose tolerance).
    sample_var = field.var(axis=1, ddof=1).mean()
    assert abs(sample_var - 4.0) < 0.5


def test_fieldgen2d_sva_iid_validation():
    g = _grid2d()
    lib = PestUtilsLib()

    # Wrong nnode
    bad_diid = np.zeros((g["nnode"] + 1, 2))
    with pytest.raises(ValueError, match="first dimension"):
        lib.fieldgen2d_sva_iid(
            g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
            g["aa"], g["anis"], g["bearing"],
            g["transtype"], g["avetype"], g["power"], bad_diid,
        )

    # Non-finite values
    bad_diid = np.zeros((g["nnode"], 1))
    bad_diid[0, 0] = np.nan
    with pytest.raises(ValueError, match="non-finite"):
        lib.fieldgen2d_sva_iid(
            g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
            g["aa"], g["anis"], g["bearing"],
            g["transtype"], g["avetype"], g["power"], bad_diid,
        )

    # Higher-dim input
    bad_diid = np.zeros((g["nnode"], 2, 2))
    with pytest.raises(ValueError, match="ndim"):
        lib.fieldgen2d_sva_iid(
            g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
            g["aa"], g["anis"], g["bearing"],
            g["transtype"], g["avetype"], g["power"], bad_diid,
        )


def test_fieldgen2d_sva_iid_accepts_1d_diid():
    """A 1D diid of length nnode must be treated as a single realisation."""
    g = _grid2d()
    rng = np.random.default_rng(1)
    diid_1d = rng.standard_normal(size=g["nnode"])
    diid_2d = diid_1d.reshape(-1, 1)

    lib = PestUtilsLib()
    f_1d = lib.fieldgen2d_sva_iid(
        g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
        g["aa"], g["anis"], g["bearing"],
        g["transtype"], g["avetype"], g["power"], diid_1d,
    )
    f_2d = lib.fieldgen2d_sva_iid(
        g["ec"], g["nc"], g["area"], g["active"], g["mean"], g["var"],
        g["aa"], g["anis"], g["bearing"],
        g["transtype"], g["avetype"], g["power"], diid_2d,
    )
    assert f_1d.shape == (g["nnode"], 1)
    np.testing.assert_array_equal(f_1d, f_2d)


def test_fieldgen3d_sva_iid_equivalence():
    g = _grid3d()
    nreal = 3

    lib_a = PestUtilsLib()
    lib_a.initialize_randgen(2024)
    field_orig = lib_a.fieldgen3d_sva(
        g["ec"], g["nc"], g["zc"], g["area"], g["height"], g["active"],
        g["mean"], g["var"], g["ahmax"], g["ahmin"], g["avert"],
        g["bearing"], g["dip"], g["rake"],
        g["transtype"], g["avetype"], g["power"], nreal=nreal,
    )

    lib_b = PestUtilsLib()
    lib_b.initialize_randgen(2024)
    diid = lib_b.fill_stdnormal(g["nnode"], nreal)
    field_iid = lib_b.fieldgen3d_sva_iid(
        g["ec"], g["nc"], g["zc"], g["area"], g["height"], g["active"],
        g["mean"], g["var"], g["ahmax"], g["ahmin"], g["avert"],
        g["bearing"], g["dip"], g["rake"],
        g["transtype"], g["avetype"], g["power"], diid,
    )
    np.testing.assert_array_equal(field_orig, field_iid)


def test_fieldgen3d_sva_iid_no_seed_required():
    g = _grid3d()
    rng = np.random.default_rng(7)
    diid = rng.standard_normal(size=(g["nnode"], 2))
    lib = PestUtilsLib()
    field = lib.fieldgen3d_sva_iid(
        g["ec"], g["nc"], g["zc"], g["area"], g["height"], g["active"],
        g["mean"], g["var"], g["ahmax"], g["ahmin"], g["avert"],
        g["bearing"], g["dip"], g["rake"],
        g["transtype"], g["avetype"], g["power"], diid,
    )
    assert field.shape == (g["nnode"], 2)
    assert np.all(np.isfinite(field))


def test_fieldgen3d_sva_iid_deterministic():
    g = _grid3d()
    rng = np.random.default_rng(101)
    diid = rng.standard_normal(size=(g["nnode"], 2))

    def run():
        lib = PestUtilsLib()
        return lib.fieldgen3d_sva_iid(
            g["ec"], g["nc"], g["zc"], g["area"], g["height"], g["active"],
            g["mean"], g["var"], g["ahmax"], g["ahmin"], g["avert"],
            g["bearing"], g["dip"], g["rake"],
            g["transtype"], g["avetype"], g["power"], diid,
        )

    np.testing.assert_array_equal(run(), run())


def test_fieldgen3d_sva_iid_linearity_transtype0():
    g = _grid3d()
    g["mean"] = 0.0
    rng = np.random.default_rng(2)
    d1 = rng.standard_normal(size=(g["nnode"], 1))
    d2 = rng.standard_normal(size=(g["nnode"], 1))
    a, b = 0.4, 0.9

    lib = PestUtilsLib()
    args = (
        g["ec"], g["nc"], g["zc"], g["area"], g["height"], g["active"],
        g["mean"], g["var"], g["ahmax"], g["ahmin"], g["avert"],
        g["bearing"], g["dip"], g["rake"],
        g["transtype"], g["avetype"], g["power"],
    )
    f1 = lib.fieldgen3d_sva_iid(*args, d1)
    f2 = lib.fieldgen3d_sva_iid(*args, d2)
    fcomb = lib.fieldgen3d_sva_iid(*args, a * d1 + b * d2)
    np.testing.assert_allclose(fcomb, a * f1 + b * f2, rtol=1e-10, atol=1e-10)


def test_fieldgen3d_sva_iid_validation():
    g = _grid3d()
    lib = PestUtilsLib()
    bad_diid = np.zeros((g["nnode"] + 1, 2))
    with pytest.raises(ValueError, match="first dimension"):
        lib.fieldgen3d_sva_iid(
            g["ec"], g["nc"], g["zc"], g["area"], g["height"], g["active"],
            g["mean"], g["var"], g["ahmax"], g["ahmin"], g["avert"],
            g["bearing"], g["dip"], g["rake"],
            g["transtype"], g["avetype"], g["power"], bad_diid,
        )
