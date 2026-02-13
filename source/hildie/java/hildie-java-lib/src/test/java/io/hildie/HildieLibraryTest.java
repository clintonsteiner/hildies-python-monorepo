package io.hildie;

/**
 * Simple test class for HildieLibrary
 * Run with: java -cp bin io.hildie.HildieLibraryTest
 */
public class HildieLibraryTest {

    public static void testGreet() {
        String result = HildieLibrary.greet("World");
        String expected = "Hello from Hildie Java Library, World!";
        assert result.equals(expected) : "greet test failed: " + result;
        System.out.println("✓ testGreet passed");
    }

    public static void testAdd() {
        int result = HildieLibrary.add(2, 3);
        int expected = 5;
        assert result == expected : "add test failed: " + result;
        System.out.println("✓ testAdd passed");
    }

    public static void main(String[] args) {
        System.out.println("Running HildieLibrary tests...");
        testGreet();
        testAdd();
        System.out.println("All tests passed!");
    }
}
