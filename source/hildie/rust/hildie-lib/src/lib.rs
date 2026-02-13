//! Hildie Rust Library

/// Greet returns a greeting message
pub fn greet(name: &str) -> String {
    format!("Hello from Hildie Rust Library, {}!", name)
}

/// Add returns the sum of two integers
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_greet() {
        assert_eq!(
            greet("World"),
            "Hello from Hildie Rust Library, World!"
        );
    }

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }
}
