use pyo3::prelude::*;
use hildie_lib::{greet, add};

/// Python bindings for Hildie Rust library
#[pymodule]
fn hildie_bindings(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_greet, m)?)?;
    m.add_function(wrap_pyfunction!(py_add, m)?)?;
    m.add_function(wrap_pyfunction!(greet_all, m)?)?;
    Ok(())
}

/// Greet a person (Python binding)
#[pyfunction]
fn py_greet(name: String) -> PyResult<String> {
    Ok(greet(&name))
}

/// Add two numbers (Python binding)
#[pyfunction]
fn py_add(a: i32, b: i32) -> PyResult<i32> {
    Ok(add(a, b))
}

/// Greet multiple people
#[pyfunction]
fn greet_all(names: Vec<String>) -> PyResult<Vec<String>> {
    Ok(names.iter().map(|n| greet(n)).collect())
}
